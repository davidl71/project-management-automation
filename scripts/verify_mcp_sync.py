#!/usr/bin/env python3
"""
Verify MCP features are in sync between FastMCP and stdio server.

This script checks that all tools, resources, and prompts registered in FastMCP
are also registered in the stdio server (and vice versa, with known exceptions).

Usage:
    uv run python scripts/verify_mcp_sync.py
"""

import re
import sys
from pathlib import Path
from typing import Dict, Set, Tuple


def extract_fastmcp_tools(content: str) -> Set[str]:
    """Extract all FastMCP tool function names."""
    tools = set()
    for match in re.finditer(r'@mcp\.tool\(\)', content):
        # Check if commented out
        start_pos = match.start()
        # Look backwards for comment
        line_start = content.rfind('\n', 0, start_pos) + 1
        line = content[line_start:start_pos]
        if line.strip().endswith('#'):
            continue
        
        # Look ahead for function definition
        end_pos = match.end()
        next_section = content[end_pos:end_pos + 500]
        
        # Find function name (handle both sync and async)
        func_match = re.search(r'(?:async\s+)?def\s+(\w+)\(', next_section)
        if func_match:
            func_name = func_match.group(1)
            # Skip call_tool (it's a handler, not a tool)
            if func_name != 'call_tool':
                tools.add(func_name)
    
    return tools


def extract_stdio_tools(content: str) -> Set[str]:
    """Extract all stdio server tool names."""
    return set(re.findall(r'Tool\(\s*name=[\"\'](\w+)[\"\']', content))


def extract_fastmcp_resources(content: str) -> Set[str]:
    """Extract all FastMCP resource URIs."""
    resources = set()
    for match in re.finditer(r'@mcp\.resource\([\"\']([^\"\']+)[\"\']', content):
        # Check if commented out
        start_pos = match.start()
        line_start = content.rfind('\n', 0, start_pos) + 1
        line = content[line_start:start_pos]
        if line.strip().endswith('#'):
            continue
        
        uri = match.group(1)
        # Normalize parameterized URIs (FastMCP uses {param}, stdio might use different format)
        # For now, keep as-is and let comparison handle it
        resources.add(uri)
    
    return resources


def extract_stdio_resources(content: str) -> Set[str]:
    """Extract all stdio server resource URIs."""
    return set(re.findall(r'Resource\(\s*uri=[\"\']([^\"\']+)[\"\']', content))


def extract_fastmcp_prompts(content: str) -> Set[str]:
    """Extract all FastMCP prompt function names."""
    prompts = set()
    for match in re.finditer(r'@mcp\.prompt\(\)', content):
        # Check if commented out
        start_pos = match.start()
        line_start = content.rfind('\n', 0, start_pos) + 1
        line = content[line_start:start_pos]
        if line.strip().endswith('#'):
            continue
        
        # Look ahead for function definition
        end_pos = match.end()
        next_section = content[end_pos:end_pos + 500]
        
        func_match = re.search(r'def\s+(\w+)\(', next_section)
        if func_match:
            prompts.add(func_match.group(1))
    
    return prompts


def extract_stdio_prompts(content: str) -> Set[str]:
    """Extract all stdio server prompt names, excluding commented ones."""
    prompts = set()
    for match in re.finditer(r'Prompt\(\s*name=[\"\'](\w+)[\"\']', content):
        # Check if this line is commented out
        start_pos = match.start()
        # Find the start of the line
        line_start = content.rfind('\n', 0, start_pos) + 1
        line = content[line_start:start_pos]
        # Skip if commented (has # before the Prompt)
        if '#' in line and not line.strip().startswith('#'):
            # Check if # comes before Prompt
            hash_pos = line.find('#')
            prompt_pos = line.find('Prompt')
            if hash_pos < prompt_pos:
                continue
        # Also skip if the line starts with #
        if line.strip().startswith('#'):
            continue
        
        prompts.add(match.group(1))
    
    return prompts


def verify_sync() -> Tuple[bool, Dict[str, list]]:
    """
    Verify MCP features are in sync.
    
    Returns:
        (success: bool, issues: dict)
    """
    server_file = Path("project_management_automation/server.py")
    
    if not server_file.exists():
        print(f"❌ Error: {server_file} not found")
        print("   Run this script from the project root directory")
        return False, {}
    
    content = server_file.read_text()
    
    # Extract features
    fastmcp_tools = extract_fastmcp_tools(content)
    stdio_tools = extract_stdio_tools(content)
    
    fastmcp_resources = extract_fastmcp_resources(content)
    stdio_resources = extract_stdio_resources(content)
    
    fastmcp_prompts = extract_fastmcp_prompts(content)
    stdio_prompts = extract_stdio_prompts(content)
    
    # Known exceptions
    stdio_only_tools = {'server_status'}  # stdio-only utility
    
    # Compare
    issues = {}
    
    # Tools
    missing_tools = fastmcp_tools - stdio_tools
    extra_tools = stdio_tools - fastmcp_tools - stdio_only_tools
    
    if missing_tools:
        issues['tools_missing_in_stdio'] = sorted(missing_tools)
    if extra_tools:
        issues['tools_extra_in_stdio'] = sorted(extra_tools)
    
    # Resources
    # Parameterized resources (with {param}) are handled via pattern matching in stdio server,
    # not listed in list_resources(). Check if they're handled in read_resource().
    
    # Extract parameterized resource patterns from read_resource()
    parameterized_handled = set()
    read_resource_matches = re.finditer(
        r'uri\.startswith\([\"\']([^\"\']+)[\"\']\)|uri\.replace\([\"\']([^\"\']+)[\"\']',
        content
    )
    for match in read_resource_matches:
        pattern = match.group(1) or match.group(2)
        if pattern and '{' not in pattern:  # Base pattern without {param}
            parameterized_handled.add(pattern)
    
    # Check exact matches first
    missing_resources_exact = fastmcp_resources - stdio_resources
    
    # Filter out parameterized resources that are handled via pattern matching
    missing_resources = set()
    for uri in missing_resources_exact:
        # Check if this parameterized resource is handled via pattern matching
        is_parameterized = '{' in uri
        if is_parameterized:
            # Extract base pattern (e.g., "automation://memories/category/" from "automation://memories/category/{category}")
            base_pattern = re.sub(r'/\{[^}]+\}', '/', uri)
            # Check if any handled pattern matches
            handled = any(uri.startswith(p) or base_pattern.startswith(p) for p in parameterized_handled)
            if not handled:
                missing_resources.add(uri)
        else:
            # Non-parameterized resource must be in list_resources()
            missing_resources.add(uri)
    
    extra_resources = stdio_resources - fastmcp_resources
    
    if missing_resources:
        issues['resources_missing_in_stdio'] = sorted(missing_resources)
    if extra_resources:
        issues['resources_extra_in_stdio'] = sorted(extra_resources)
    
    # Prompts
    missing_prompts = fastmcp_prompts - stdio_prompts
    extra_prompts = stdio_prompts - fastmcp_prompts
    
    if missing_prompts:
        issues['prompts_missing_in_stdio'] = sorted(missing_prompts)
    if extra_prompts:
        issues['prompts_extra_in_stdio'] = sorted(extra_prompts)
    
    return len(issues) == 0, issues


def main():
    """Main entry point."""
    print("🔍 Verifying MCP feature synchronization...")
    print()
    
    success, issues = verify_sync()
    
    if issues:
        print("❌ Sync issues found:\n")
        
        if 'tools_missing_in_stdio' in issues:
            print(f"  ⚠ Tools in FastMCP but NOT in stdio server ({len(issues['tools_missing_in_stdio'])}):")
            for tool in issues['tools_missing_in_stdio']:
                print(f"     - {tool}")
            print()
        
        if 'tools_extra_in_stdio' in issues:
            print(f"  ⚠ Tools in stdio server but NOT in FastMCP ({len(issues['tools_extra_in_stdio'])}):")
            for tool in issues['tools_extra_in_stdio']:
                print(f"     - {tool}")
            print()
        
        if 'resources_missing_in_stdio' in issues:
            print(f"  ⚠ Resources in FastMCP but NOT in stdio server ({len(issues['resources_missing_in_stdio'])}):")
            for resource in issues['resources_missing_in_stdio']:
                print(f"     - {resource}")
            print()
        
        if 'resources_extra_in_stdio' in issues:
            print(f"  ⚠ Resources in stdio server but NOT in FastMCP ({len(issues['resources_extra_in_stdio'])}):")
            for resource in issues['resources_extra_in_stdio']:
                print(f"     - {resource}")
            print()
        
        if 'prompts_missing_in_stdio' in issues:
            print(f"  ⚠ Prompts in FastMCP but NOT in stdio server ({len(issues['prompts_missing_in_stdio'])}):")
            for prompt in issues['prompts_missing_in_stdio']:
                print(f"     - {prompt}")
            print()
        
        if 'prompts_extra_in_stdio' in issues:
            print(f"  ⚠ Prompts in stdio server but NOT in FastMCP ({len(issues['prompts_extra_in_stdio'])}):")
            for prompt in issues['prompts_extra_in_stdio']:
                print(f"     - {prompt}")
            print()
        
        print("📖 See docs/MCP_SYNC_GUIDE.md for how to fix these issues")
        return 1
    else:
        # Get counts for success message
        server_file = Path("project_management_automation/server.py")
        content = server_file.read_text()
        
        fastmcp_tools = extract_fastmcp_tools(content)
        stdio_tools = extract_stdio_tools(content)
        fastmcp_resources = extract_fastmcp_resources(content)
        stdio_resources = extract_stdio_resources(content)
        fastmcp_prompts = extract_fastmcp_prompts(content)
        stdio_prompts = extract_stdio_prompts(content)
        
        print("✅ All MCP features are in sync!")
        print()
        print(f"  Tools:    {len(fastmcp_tools):3} FastMCP, {len(stdio_tools):3} stdio")
        print(f"  Resources: {len(fastmcp_resources):3} FastMCP, {len(stdio_resources):3} stdio")
        print(f"  Prompts:  {len(fastmcp_prompts):3} FastMCP, {len(stdio_prompts):3} stdio")
        return 0


if __name__ == "__main__":
    sys.exit(main())

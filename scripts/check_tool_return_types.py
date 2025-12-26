#!/usr/bin/env python3
"""
Static analysis script to check that all MCP tools in server.py return JSON strings.

FastMCP has a bug where it tries to await dict results, causing errors.
All tools must return JSON strings (str) to avoid this issue.

Usage:
    python scripts/check_tool_return_types.py
    uv run python scripts/check_tool_return_types.py
"""

import re
import ast
import json
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
server_file = project_root / "project_management_automation" / "server.py"


def find_tool_functions(content: str) -> list[dict[str, Any]]:
    """Find all @mcp.tool() decorated functions in the file."""
    tools = []
    lines = content.split('\n')
    
    # Find all @mcp.tool() decorators
    for i, line in enumerate(lines):
        if '@mcp.tool()' in line or '@mcp.tool' in line:
            # Look for the function definition after the decorator
            func_start = None
            for j in range(i + 1, min(i + 10, len(lines))):
                if lines[j].strip().startswith('def '):
                    func_start = j
                    break
            
            if func_start:
                # Extract function name
                func_match = re.match(r'\s*def\s+(\w+)', lines[func_start])
                if func_match:
                    func_name = func_match.group(1)
                    
                    # Find function end (next def, class, or significant decrease in indentation)
                    func_end = func_start + 1
                    func_indent = len(lines[func_start]) - len(lines[func_start].lstrip())
                    
                    for j in range(func_start + 1, len(lines)):
                        line_stripped = lines[j].strip()
                        if not line_stripped or line_stripped.startswith('#'):
                            continue
                        
                        current_indent = len(lines[j]) - len(lines[j].lstrip())
                        if current_indent <= func_indent:
                            if line_stripped.startswith(('def ', 'class ', '@')):
                                func_end = j
                                break
                            elif current_indent < func_indent:
                                func_end = j
                                break
                    else:
                        func_end = len(lines)
                    
                    tools.append({
                        'name': func_name,
                        'line': func_start + 1,
                        'body': '\n'.join(lines[func_start:func_end]),
                        'body_lines': lines[func_start:func_end]
                    })
    
    return tools


def check_return_pattern(tool: dict[str, Any]) -> dict[str, Any]:
    """
    Check if a tool's return pattern could cause 'await dict' issues.
    
    Returns:
        dict with keys: tool_name, issues, warnings, return_type_hint, return_statements
    """
    result = {
        'tool_name': tool['name'],
        'line': tool['line'],
        'issues': [],
        'warnings': [],
        'return_type_hint': None,
        'return_statements': []
    }
    
    body = tool['body']
    lines = tool['body_lines']
    
    # Check return type hint
    func_def_match = re.match(r'\s*def\s+\w+\s*\([^)]*\)\s*->\s*([^:]+)', body)
    if func_def_match:
        return_type = func_def_match.group(1).strip()
        result['return_type_hint'] = return_type
        
        # Check if return type is str
        if 'str' not in return_type:
            result['warnings'].append(
                f"Return type hint is '{return_type}', not 'str'. "
                f"Tools should return str (JSON string) to avoid FastMCP issues."
            )
    
    # Find all return statements
    return_pattern = r'return\s+(.+)'
    for i, line in enumerate(lines):
        match = re.search(return_pattern, line)
        if match:
            return_expr = match.group(1).strip()
            result['return_statements'].append({
                'line': tool['line'] + i,
                'expression': return_expr,
                'full_line': line.strip()
            })
            
            # Check for problematic patterns
            # 1. Direct dict return (problematic)
            if return_expr.startswith('{') or return_expr.startswith('dict('):
                result['issues'].append(
                    f"Line {tool['line'] + i}: Returns dict directly: {return_expr[:50]}"
                )
            
            # 2. Variable that might be a dict
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', return_expr):
                var_name = return_expr
                func_body_before = '\n'.join(lines[:i+1])
                func_body_all = '\n'.join(lines)
                
                # Check if variable is assigned from a function that returns JSON string
                # Common patterns: _function() returns JSON string, or json.dumps() was called
                if f'json.dumps({var_name}' in func_body_before:
                    continue  # Already wrapped
                
                # Check if assigned from underlying function (they return JSON strings)
                # Pattern: result = _function(...)
                assignment_pattern = rf'{var_name}\s*=\s*_?(\w+)\([^)]*\)'
                if re.search(assignment_pattern, func_body_all):
                    # Check if there's a comment indicating it's already a JSON string
                    if 'JSON string' in func_body_all or 'json string' in func_body_all.lower():
                        continue  # Comment indicates it's safe
                    # Check if it's from an underlying function (convention: they return JSON)
                    match = re.search(assignment_pattern, func_body_all)
                    if match and (match.group(1).startswith('_') or 'tool' in match.group(1).lower()):
                        continue  # Likely from underlying tool function (returns JSON)
                
                # Check if it's a string literal assignment (f-string, etc.)
                string_assignment_pattern = rf'{var_name}\s*=\s*["\']|{var_name}\s*=\s*f["\']'
                if re.search(string_assignment_pattern, func_body_all):
                    continue  # String literal, safe
                
                # Only warn if we can't determine it's safe
                result['warnings'].append(
                    f"Line {tool['line'] + i}: Returns variable '{var_name}' directly. "
                    f"Ensure it's a JSON string, not a dict. (May be safe if from underlying function)"
                )
            
            # 3. Function call - check if it returns JSON string
            elif '(' in return_expr:
                # Check for json.dumps (good)
                if 'json.dumps' in return_expr:
                    continue  # Good pattern
                
                # Check for underlying function calls (might return dict)
                func_call_match = re.match(r'^_?(\w+)\(', return_expr)
                if func_call_match:
                    func_name = func_call_match.group(1)
                    # Check if it's a consolidated tool function (they return JSON strings)
                    if func_name.startswith('_'):
                        result['warnings'].append(
                            f"Line {tool['line'] + i}: Returns result from '{func_name}(...)'. "
                            f"Ensure the underlying function returns a JSON string."
                        )
    
    return result


def main():
    """Main analysis runner."""
    print("=" * 70)
    print("Static Analysis: MCP Tool Return Types")
    print("=" * 70)
    print()
    print("Checking that all @mcp.tool() decorated functions return JSON strings")
    print("to avoid FastMCP 'await dict' errors.")
    print()
    
    if not server_file.exists():
        print(f"❌ Server file not found: {server_file}")
        return 1
    
    content = server_file.read_text()
    
    # Find all tool functions
    tools = find_tool_functions(content)
    
    if not tools:
        print("❌ No @mcp.tool() decorated functions found")
        return 1
    
    print(f"Found {len(tools)} tool functions\n")
    
    # Check each tool
    results = []
    for tool in tools:
        result = check_return_pattern(tool)
        results.append(result)
    
    # Report results
    issues_count = sum(len(r['issues']) for r in results)
    warnings_count = sum(len(r['warnings']) for r in results)
    
    print("=" * 70)
    print("Analysis Results Summary")
    print("=" * 70)
    print(f"Total tools:     {len(results)}")
    print(f"❌ Issues:       {issues_count}")
    print(f"⚠️  Warnings:     {warnings_count}")
    print()
    
    # Show tools with issues
    tools_with_issues = [r for r in results if r['issues']]
    if tools_with_issues:
        print("❌ TOOLS WITH ISSUES (return dicts directly):")
        print("-" * 70)
        for result in tools_with_issues:
            print(f"  {result['tool_name']} (line {result['line']})")
            for issue in result['issues']:
                print(f"    - {issue}")
            print()
    
    # Show tools with warnings
    tools_with_warnings = [r for r in results if r['warnings']]
    if tools_with_warnings:
        print("⚠️  TOOLS WITH WARNINGS (might return non-JSON strings):")
        print("-" * 70)
        for result in tools_with_warnings:
            print(f"  {result['tool_name']} (line {result['line']})")
            for warning in result['warnings']:
                print(f"    - {warning}")
            if result['return_statements']:
                print(f"    Return statements:")
                for ret in result['return_statements']:
                    print(f"      Line {ret['line']}: {ret['full_line']}")
            print()
    
    # Show tools that look good
    clean_tools = [r for r in results if not r['issues'] and not r['warnings']]
    if clean_tools:
        print(f"✅ CLEAN TOOLS ({len(clean_tools)} tools appear to return JSON strings correctly)")
        print()
    
    # Exit with error code if any issues
    if issues_count > 0:
        print("=" * 70)
        print(f"❌ ANALYSIS FAILED: {issues_count} issue(s) found")
        print("=" * 70)
        return 1
    else:
        print("=" * 70)
        if warnings_count > 0:
            print(f"⚠️  ANALYSIS COMPLETE: No critical issues, but {warnings_count} warning(s)")
        else:
            print("✅ ANALYSIS PASSED: All tools appear to return JSON strings correctly")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())


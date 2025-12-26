#!/usr/bin/env python3
"""
Compare server.py structure with minimal FastMCP sample.

Highlights key differences that might cause issues.
"""

from pathlib import Path
import re

project_root = Path(__file__).parent.parent
server_file = project_root / "project_management_automation" / "server.py"
sample_file = project_root / "test_minimal_mcp_server.py"

def analyze_server_structure(file_path: Path) -> dict:
    """Analyze server structure."""
    content = file_path.read_text()
    lines = content.split('\n')
    
    result = {
        'file': file_path.name,
        'total_lines': len(lines),
        'fastmcp_init_line': None,
        'first_tool_line': None,
        'tool_count': 0,
        'has_lifespan': False,
        'has_middleware': False,
        'imports_before_init': [],
        'code_between_init_and_tools': 0,
        'tool_registration_pattern': None
    }
    
    # Find FastMCP initialization
    for i, line in enumerate(lines):
        if 'FastMCP(' in line or 'FastMCP(' in line:
            result['fastmcp_init_line'] = i + 1
            result['has_lifespan'] = 'lifespan=' in line
            break
    
    # Find first tool
    for i, line in enumerate(lines):
        if '@mcp.tool()' in line or '@mcp.tool' in line:
            result['first_tool_line'] = i + 1
            break
    
    # Count tools
    result['tool_count'] = len(re.findall(r'@mcp\.tool\(\)', content))
    
    # Check for middleware
    result['has_middleware'] = 'middleware' in content.lower() and 'Middleware' in content
    
    # Calculate code between init and first tool
    if result['fastmcp_init_line'] and result['first_tool_line']:
        result['code_between_init_and_tools'] = result['first_tool_line'] - result['fastmcp_init_line'] - 1
    
    # Find imports before FastMCP init
    if result['fastmcp_init_line']:
        for i in range(min(result['fastmcp_init_line'] - 1, 500)):
            line = lines[i].strip()
            if line.startswith('import ') or line.startswith('from '):
                result['imports_before_init'].append((i + 1, line[:80]))
    
    # Check tool registration pattern
    if 'def register_tools' in content:
        result['tool_registration_pattern'] = 'function_call'
    elif '@mcp.tool()' in content:
        result['tool_registration_pattern'] = 'decorator'
    else:
        result['tool_registration_pattern'] = 'unknown'
    
    return result

def compare_structures(our_server: dict, sample_server: dict) -> dict:
    """Compare two server structures."""
    differences = {
        'significant_differences': [],
        'warnings': [],
        'similarities': []
    }
    
    # Compare initialization
    if our_server['has_lifespan'] and not sample_server['has_lifespan']:
        differences['warnings'].append(
            f"✅ Our server uses lifespan (line {our_server['fastmcp_init_line']}), "
            f"sample doesn't - this is fine, it's optional"
        )
    
    # Compare code complexity
    our_complexity = our_server['code_between_init_and_tools']
    sample_complexity = sample_server['code_between_init_and_tools']
    
    if our_complexity > sample_complexity * 10:
        differences['significant_differences'].append(
            f"⚠️  Much more code between FastMCP init and first tool: "
            f"{our_complexity} lines (ours) vs {sample_complexity} lines (sample). "
            f"This might cause issues if tools need to be registered immediately."
        )
    
    # Compare tool count
    if our_server['tool_count'] > 0 and sample_server['tool_count'] > 0:
        differences['similarities'].append(
            f"Both servers register tools with @mcp.tool() decorator"
        )
    
    # Compare registration pattern
    if our_server['tool_registration_pattern'] != sample_server['tool_registration_pattern']:
        differences['warnings'].append(
            f"Tool registration pattern differs: "
            f"{our_server['tool_registration_pattern']} (ours) vs "
            f"{sample_server['tool_registration_pattern']} (sample)"
        )
    
    # Check for middleware (only in our server)
    if our_server['has_middleware'] and not sample_server['has_middleware']:
        differences['warnings'].append(
            f"✅ Our server uses middleware, sample doesn't - this is fine, it's a FastMCP 2 feature"
        )
    
    return differences

def main():
    """Main comparison."""
    print("=" * 70)
    print("Server Structure Comparison")
    print("=" * 70)
    print()
    
    # Analyze our server
    if not server_file.exists():
        print(f"❌ Server file not found: {server_file}")
        return 1
    
    our_server = analyze_server_structure(server_file)
    
    # Analyze sample server
    if sample_file.exists():
        sample_server = analyze_server_structure(sample_file)
    else:
        print(f"⚠️  Sample file not found: {sample_file}")
        print("Using minimal structure for comparison")
        sample_server = {
            'file': 'minimal_sample',
            'total_lines': 20,
            'fastmcp_init_line': 8,
            'first_tool_line': 11,
            'tool_count': 4,
            'has_lifespan': False,
            'has_middleware': False,
            'code_between_init_and_tools': 2,
            'tool_registration_pattern': 'decorator'
        }
    
    # Print analysis
    print("Our Server (server.py):")
    print("-" * 70)
    print(f"  Total lines:              {our_server['total_lines']:,}")
    print(f"  FastMCP init line:        {our_server['fastmcp_init_line']}")
    print(f"  First tool line:          {our_server['first_tool_line']}")
    print(f"  Code between init/tools:  {our_server['code_between_init_and_tools']:,} lines")
    print(f"  Tool count:               {our_server['tool_count']}")
    print(f"  Has lifespan:             {our_server['has_lifespan']}")
    print(f"  Has middleware:           {our_server['has_middleware']}")
    print(f"  Registration pattern:     {our_server['tool_registration_pattern']}")
    print()
    
    print("Sample Server (test_minimal_mcp_server.py):")
    print("-" * 70)
    print(f"  Total lines:              {sample_server['total_lines']}")
    print(f"  FastMCP init line:        {sample_server['fastmcp_init_line']}")
    print(f"  First tool line:          {sample_server['first_tool_line']}")
    print(f"  Code between init/tools:  {sample_server['code_between_init_and_tools']} lines")
    print(f"  Tool count:               {sample_server['tool_count']}")
    print(f"  Has lifespan:             {sample_server['has_lifespan']}")
    print(f"  Has middleware:           {sample_server['has_middleware']}")
    print(f"  Registration pattern:     {sample_server['tool_registration_pattern']}")
    print()
    
    # Compare
    differences = compare_structures(our_server, sample_server)
    
    print("=" * 70)
    print("Comparison Results")
    print("=" * 70)
    print()
    
    if differences['significant_differences']:
        print("⚠️  SIGNIFICANT DIFFERENCES:")
        print("-" * 70)
        for diff in differences['significant_differences']:
            print(f"  {diff}")
        print()
    
    if differences['warnings']:
        print("📋 NOTES:")
        print("-" * 70)
        for warning in differences['warnings']:
            print(f"  {warning}")
        print()
    
    if differences['similarities']:
        print("✅ SIMILARITIES:")
        print("-" * 70)
        for similarity in differences['similarities']:
            print(f"  {similarity}")
        print()
    
    # Summary
    print("=" * 70)
    print("Key Structural Differences")
    print("=" * 70)
    print()
    print("1. COMPLEXITY:")
    print(f"   - Sample: ~{sample_server['code_between_init_and_tools']} lines between init and tools")
    print(f"   - Ours:   ~{our_server['code_between_init_and_tools']:,} lines between init and tools")
    print()
    print("2. FEATURES:")
    print(f"   - Sample: Basic FastMCP server")
    print(f"   - Ours:   FastMCP + lifespan + middleware + stdio fallback")
    print()
    print("3. TOOL REGISTRATION:")
    print(f"   - Sample: Direct @mcp.tool() decorators at module level")
    print(f"   - Ours:   @mcp.tool() decorators after middleware/resources setup")
    print()
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())


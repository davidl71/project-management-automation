#!/usr/bin/env python3
"""Analyze patterns between working and broken tools."""

import re
from pathlib import Path

server_file = Path(__file__).parent / "project_management_automation" / "server.py"

working_tools = [
    "task_workflow",
    "estimation", 
    "ollama",
    "mlx",
    "git_tools",
    "session",
    "memory_maint",
]

broken_tools = [
    "infer_session_mode",
    "add_external_tool_hints",
    "automation",
    "tool_catalog",
    "workflow_mode",
    "context",
    "recommend",
    "analyze_alignment",
    "security",
    "generate_config",
    "setup_hooks",
    "prompt_tracking",
    "health",
    "check_attribution",
    "report",
    "task_analysis",
    "testing",
    "lint",
    "memory",
    "task_discovery",
]

def analyze_tool_decorators(tool_name: str) -> dict:
    """Analyze decorators and implementation for a tool."""
    with open(server_file) as f:
        content = f.read()
    
    # Find the tool definition
    pattern = rf"(@ensure_json_string\s+)?@mcp\.tool\(\)\s+(async\s+)?def {tool_name}\("
    match = re.search(pattern, content)
    
    if not match:
        return {"found": False}
    
    start_pos = match.start()
    
    # Check decorators
    has_ensure_json = "@ensure_json_string" in content[max(0, start_pos-100):start_pos]
    is_async = "async def" in match.group(0)
    
    # Find the function body
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if f"def {tool_name}(" in line:
            # Get next 30 lines
            func_body = '\n'.join(lines[i:i+30])
            
            # Check return patterns
            has_simple_return = f"return _{tool_name}(" in func_body or f"return _{tool_name.replace('_', '_')}(" in func_body
            has_conditional_returns = func_body.count("return") > 2
            
            return {
                "found": True,
                "has_ensure_json": has_ensure_json,
                "is_async": is_async,
                "has_simple_return": has_simple_return,
                "has_conditional_returns": has_conditional_returns,
                "return_count": func_body.count("return"),
            }
    
    return {"found": False}

print("="*80)
print("TOOL PATTERN ANALYSIS")
print("="*80)
print()

print("WORKING TOOLS:")
print("-" * 80)
working_patterns = {}
for tool in working_tools:
    analysis = analyze_tool_decorators(tool)
    working_patterns[tool] = analysis
    print(f"{tool}:")
    print(f"  @ensure_json_string: {analysis.get('has_ensure_json', 'N/A')}")
    print(f"  async: {analysis.get('is_async', 'N/A')}")
    print(f"  simple return: {analysis.get('has_simple_return', 'N/A')}")
    print()

print("\nBROKEN TOOLS:")
print("-" * 80)
broken_patterns = {}
for tool in broken_tools[:5]:  # Check first 5
    analysis = analyze_tool_decorators(tool)
    broken_patterns[tool] = analysis
    print(f"{tool}:")
    print(f"  @ensure_json_string: {analysis.get('has_ensure_json', 'N/A')}")
    print(f"  async: {analysis.get('is_async', 'N/A')}")
    print(f"  simple return: {analysis.get('has_simple_return', 'N/A')}")
    print()

print("\nPATTERN COMPARISON:")
print("-" * 80)

working_has_ensure = sum(1 for p in working_patterns.values() if p.get('has_ensure_json'))
broken_has_ensure = sum(1 for p in broken_patterns.values() if p.get('has_ensure_json'))

print(f"Working tools with @ensure_json_string: {working_has_ensure}/{len(working_tools)}")
print(f"Broken tools with @ensure_json_string: {broken_has_ensure}/{len(broken_tools)}")


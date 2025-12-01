#!/usr/bin/env python3
"""
Check all MCP tools for conditional logic that might cause FastMCP issues.

Scans all @mcp.tool() decorated functions in server.py for:
- if/elif/else statements
- Conditional returns
- Dynamic imports within tool functions
- Complex control flow that might confuse FastMCP

This helps identify tools that might have the same "object dict can't be used in 'await' expression" error.
"""

import ast
import re
from pathlib import Path
from typing import Any

# Add project root to path
script_dir = Path(__file__).resolve().parent
repo_root = script_dir.parent
sys_path = str(repo_root)
import sys
sys.path.insert(0, sys_path)


def find_mcp_tool_functions(file_path: Path) -> list[dict[str, Any]]:
    """Parse server.py and find all @mcp.tool() decorated functions."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    tree = ast.parse(content, filename=str(file_path))
    tools = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if function has @mcp.tool() decorator
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Attribute):
                        if (isinstance(decorator.func.value, ast.Name) and 
                            decorator.func.value.id == 'mcp' and
                            decorator.func.attr == 'tool'):
                            tools.append({
                                'name': node.name,
                                'line': node.lineno,
                                'node': node
                            })
                            break
    
    return tools


def analyze_function_for_conditional_logic(func_node: ast.FunctionDef) -> dict[str, Any]:
    """Analyze a function for problematic patterns."""
    issues = {
        'has_if_elif_else': False,
        'if_count': 0,
        'elif_count': 0,
        'else_count': 0,
        'conditional_returns': [],
        'dynamic_imports': [],
        'complexity_score': 0,
        'lines_with_conditionals': []
    }
    
    # Count conditionals
    for node in ast.walk(func_node):
        if isinstance(node, ast.If):
            issues['has_if_elif_else'] = True
            issues['if_count'] += 1
            issues['lines_with_conditionals'].append(node.lineno)
            
            # Check for elif
            if node.orelse:
                for orelse_node in node.orelse:
                    if isinstance(orelse_node, ast.If):
                        issues['elif_count'] += 1
                    elif isinstance(orelse_node, (ast.Return, ast.Expr)):
                        issues['else_count'] += 1
            else:
                # No else clause, but if exists
                pass
    
    # Check for conditional returns (returns inside if blocks)
    for node in ast.walk(func_node):
        if isinstance(node, ast.If):
            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    issues['conditional_returns'].append({
                        'line': child.lineno,
                        'in_if': True
                    })
    
    # Check for dynamic imports (imports inside function body, not at top)
    for node in ast.walk(func_node):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Check if this import is inside the function (not at module level)
            parent = None
            for parent_node in ast.walk(func_node):
                for child in ast.iter_child_nodes(parent_node):
                    if child is node:
                        parent = parent_node
                        break
                if parent:
                    break
            
            if parent and not isinstance(parent, ast.Module):
                issues['dynamic_imports'].append({
                    'line': node.lineno,
                    'module': getattr(node, 'module', None) or 'unknown'
                })
    
    # Calculate complexity score
    issues['complexity_score'] = (
        issues['if_count'] * 2 +
        issues['elif_count'] * 1.5 +
        issues['else_count'] * 1 +
        len(issues['conditional_returns']) * 1.5 +
        len(issues['dynamic_imports']) * 2
    )
    
    return issues


def check_tool_implementation(file_path: Path, tool_name: str, line_num: int) -> dict[str, Any]:
    """Check the actual implementation of a tool function."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the function definition
    func_start = None
    func_end = None
    indent_level = None
    
    # Find function start (line_num is 1-indexed, list is 0-indexed)
    for i in range(line_num - 1, len(lines)):
        line = lines[i]
        if f'def {tool_name}(' in line:
            func_start = i
            # Calculate indent level
            indent_level = len(line) - len(line.lstrip())
            break
    
    if func_start is None:
        return {'error': f'Could not find function {tool_name} at line {line_num}'}
    
    # Find function end (next function or class at same indent level, or end of file)
    func_lines = []
    for i in range(func_start, len(lines)):
        line = lines[i]
        current_indent = len(line) - len(line.lstrip())
        
        # Check if we've hit another function/class at same or lower indent
        if i > func_start and current_indent <= indent_level:
            if line.strip() and (line.strip().startswith('def ') or line.strip().startswith('@') or line.strip().startswith('class ')):
                func_end = i
                break
        
        func_lines.append(line)
    
    if func_end is None:
        func_end = len(lines)
    
    func_body = ''.join(lines[func_start:func_end])
    
    # Check for problematic patterns using regex (simpler than AST for this)
    issues = {
        'has_if_elif_else': False,
        'if_count': len(re.findall(r'\bif\s+', func_body)),
        'elif_count': len(re.findall(r'\belif\s+', func_body)),
        'else_count': len(re.findall(r'\belse\s*:', func_body)),
        'has_action_param': 'action' in func_body and 'action: str' in func_body,
        'has_conditional_action': bool(re.search(r'if\s+action\s*==', func_body, re.IGNORECASE)),
        'has_multiple_returns': func_body.count('return ') > 1,
        'has_try_except': 'try:' in func_body,
        'function_length': func_end - func_start,
        'code_snippet': '\n'.join(lines[func_start:min(func_start+20, func_end)])
    }
    
    issues['has_if_elif_else'] = issues['if_count'] > 0
    
    return issues


def main():
    """Main analysis function."""
    server_file = repo_root / 'project_management_automation' / 'server.py'
    
    if not server_file.exists():
        print(f"❌ Server file not found: {server_file}")
        return
    
    print("🔍 Scanning MCP tools for conditional logic patterns...\n")
    
    # Find all @mcp.tool() decorated functions
    tools = find_mcp_tool_functions(server_file)
    
    print(f"Found {len(tools)} MCP tools\n")
    print("=" * 80)
    
    # Analyze each tool
    tools_with_issues = []
    tools_without_issues = []
    
    for tool in tools:
        tool_name = tool['name']
        line_num = tool['line']
        
        # Check implementation
        issues = check_tool_implementation(server_file, tool_name, line_num)
        
        if issues.get('error'):
            print(f"⚠️  {tool_name}: {issues['error']}")
            continue
        
        # Determine if tool has problematic patterns
        has_issues = (
            issues['has_if_elif_else'] and
            (issues['has_conditional_action'] or issues['if_count'] > 1 or issues['has_multiple_returns'])
        )
        
        tool_info = {
            'name': tool_name,
            'line': line_num,
            'issues': issues,
            'has_problems': has_issues
        }
        
        if has_issues:
            tools_with_issues.append(tool_info)
        else:
            tools_without_issues.append(tool_info)
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"📊 SUMMARY")
    print("=" * 80)
    print(f"Total tools: {len(tools)}")
    print(f"⚠️  Tools with conditional logic: {len(tools_with_issues)}")
    print(f"✅ Tools without issues: {len(tools_without_issues)}")
    
    # Print tools with issues
    if tools_with_issues:
        print("\n" + "=" * 80)
        print("⚠️  TOOLS WITH CONDITIONAL LOGIC (Potential FastMCP Issues)")
        print("=" * 80)
        
        for tool in sorted(tools_with_issues, key=lambda x: x['line']):
            issues = tool['issues']
            print(f"\n🔴 {tool['name']} (line {tool['line']})")
            print(f"   - If statements: {issues['if_count']}")
            print(f"   - Elif statements: {issues['elif_count']}")
            print(f"   - Else statements: {issues['else_count']}")
            print(f"   - Has 'action' parameter: {issues['has_action_param']}")
            print(f"   - Conditional on action: {issues['has_conditional_action']}")
            print(f"   - Multiple returns: {issues['has_multiple_returns']}")
            print(f"   - Function length: {issues['function_length']} lines")
            if issues['has_try_except']:
                print(f"   - ⚠️  Has try/except block")
            print(f"   - Code preview:")
            print("     " + "\n     ".join(issues['code_snippet'].split('\n')[:5]))
    
    # Print tools without issues (summary only)
    print("\n" + "=" * 80)
    print("✅ TOOLS WITHOUT CONDITIONAL LOGIC (Safe)")
    print("=" * 80)
    safe_tool_names = [t['name'] for t in tools_without_issues]
    print(f"\nTotal: {len(safe_tool_names)} tools")
    if len(safe_tool_names) <= 20:
        for name in sorted(safe_tool_names):
            print(f"  ✅ {name}")
    else:
        print(f"  (First 20 of {len(safe_tool_names)}):")
        for name in sorted(safe_tool_names)[:20]:
            print(f"  ✅ {name}")
        print(f"  ... and {len(safe_tool_names) - 20} more")
    
    # Generate recommendation
    print("\n" + "=" * 80)
    print("💡 RECOMMENDATIONS")
    print("=" * 80)
    
    if tools_with_issues:
        print("\n⚠️  Tools with conditional logic should be refactored:")
        print("   1. Split tools with 'action' parameter into separate tools")
        print("   2. Simplify tools with multiple if/elif/else branches")
        print("   3. Move conditional logic to helper functions")
        print("   4. Use @ensure_json_string decorator (already applied)")
        print("\n   Example: run_automation(action='sprint') → run_sprint_automation()")
    
    print("\n✅ Best practices for FastMCP tools:")
    print("   - Simple, single-purpose functions")
    print("   - Direct return of underlying function result")
    print("   - No conditional logic based on parameters")
    print("   - @ensure_json_string decorator applied")
    
    # Write detailed report
    report_path = repo_root / 'docs' / 'TOOL_CONDITIONAL_LOGIC_ANALYSIS.md'
    with open(report_path, 'w') as f:
        f.write("# Tool Conditional Logic Analysis\n\n")
        f.write(f"*Generated: {Path(__file__).stat().st_mtime}*\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total tools: {len(tools)}\n")
        f.write(f"- Tools with conditional logic: {len(tools_with_issues)}\n")
        f.write(f"- Tools without issues: {len(tools_without_issues)}\n\n")
        
        if tools_with_issues:
            f.write("## Tools with Conditional Logic\n\n")
            for tool in sorted(tools_with_issues, key=lambda x: x['line']):
                issues = tool['issues']
                f.write(f"### {tool['name']} (line {tool['line']})\n\n")
                f.write(f"- If statements: {issues['if_count']}\n")
                f.write(f"- Elif statements: {issues['elif_count']}\n")
                f.write(f"- Else statements: {issues['else_count']}\n")
                f.write(f"- Has 'action' parameter: {issues['has_action_param']}\n")
                f.write(f"- Conditional on action: {issues['has_conditional_action']}\n")
                f.write(f"- Multiple returns: {issues['has_multiple_returns']}\n")
                f.write(f"- Function length: {issues['function_length']} lines\n\n")
                f.write("```python\n")
                f.write(issues['code_snippet'])
                f.write("\n```\n\n")
        
        f.write("## Tools Without Issues\n\n")
        for tool in sorted(tools_without_issues, key=lambda x: x['name']):
            f.write(f"- ✅ {tool['name']}\n")
    
    print(f"\n📄 Detailed report written to: {report_path}")


if __name__ == '__main__':
    main()


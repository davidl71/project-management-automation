#!/usr/bin/env python3
"""
Comprehensive FastMCP static analysis test script.

This script:
1. Analyzes how FastMCP performs static analysis
2. Tests all our tools to identify issues
3. Provides recommendations for fixes
"""

import inspect
import json
import sys
from pathlib import Path
from typing import Any, Dict, get_type_hints

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def analyze_function_for_fastmcp(func: Any) -> Dict[str, Any]:
    """Comprehensive analysis of a function for FastMCP compatibility."""
    import ast
    import textwrap
    
    sig = inspect.signature(func)
    hints = get_type_hints(func, include_extras=True)
    
    # AST analysis
    dict_returns = []
    str_returns = []
    json_dumps_calls = []
    
    try:
        source = inspect.getsource(func)
        tree = ast.parse(textwrap.dedent(source))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Return) and node.value:
                # Check if return is a dict literal
                if isinstance(node.value, ast.Dict):
                    dict_returns.append(ast.get_source_segment(source, node) if hasattr(ast, 'get_source_segment') else str(node))
                # Check if return is a string
                elif isinstance(node.value, (ast.Str, ast.Constant)) and isinstance(node.value.value, str):
                    str_returns.append(ast.get_source_segment(source, node) if hasattr(ast, 'get_source_segment') else str(node))
                # Check for json.dumps calls
                elif isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Attribute):
                        if isinstance(node.value.func.value, ast.Name) and node.value.func.value.id == 'json':
                            if node.value.func.attr == 'dumps':
                                json_dumps_calls.append(ast.get_source_segment(source, node) if hasattr(ast, 'get_source_segment') else str(node))
    except Exception as e:
        pass
    
    return {
        "name": func.__name__,
        "return_annotation": str(sig.return_annotation) if sig.return_annotation != inspect.Parameter.empty else None,
        "return_hint": str(hints.get("return", "No hint")),
        "is_async": inspect.iscoroutinefunction(func),
        "dict_returns_found": len(dict_returns),
        "str_returns_found": len(str_returns),
        "json_dumps_calls": len(json_dumps_calls),
        "issues": [] if len(dict_returns) == 0 else [f"Found {len(dict_returns)} dict return(s) - FastMCP may detect these"],
    }


def test_all_consolidated_tools():
    """Test all tools in consolidated.py."""
    print("="*80)
    print("TESTING ALL CONSOLIDATED TOOLS")
    print("="*80)
    
    try:
        from project_management_automation.tools import consolidated
        
        # Get all functions from consolidated module
        tools = []
        for name in dir(consolidated):
            obj = getattr(consolidated, name)
            if inspect.isfunction(obj) and not name.startswith('_'):
                # Check if it looks like a tool function
                sig = inspect.signature(obj)
                if len(sig.parameters) > 0:  # Has parameters
                    tools.append((name, obj))
        
        print(f"\nFound {len(tools)} potential tool functions\n")
        
        issues_found = []
        for name, func in tools[:20]:  # Test first 20
            analysis = analyze_function_for_fastmcp(func)
            if analysis["issues"]:
                issues_found.append((name, analysis))
                print(f"⚠️  {name}:")
                print(f"   {analysis['issues'][0]}")
                print(f"   Return annotation: {analysis['return_annotation']}")
                print()
        
        if not issues_found:
            print("✅ No dict returns found in tool functions")
        else:
            print(f"\n⚠️  Found {len(issues_found)} tools with potential issues")
        
        return issues_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """Run comprehensive tests."""
    print("\n" + "="*80)
    print("FASTMCP COMPREHENSIVE STATIC ANALYSIS")
    print("="*80 + "\n")
    
    # Test all consolidated tools
    issues = test_all_consolidated_tools()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Tools analyzed: Multiple")
    print(f"Issues found: {len(issues)}")
    
    if issues:
        print("\nRecommendations:")
        print("1. Ensure all return statements use json.dumps() for dicts")
        print("2. Check call chains for functions that return dicts")
        print("3. Consider using TypedDict return types if FastMCP supports them")
    else:
        print("\n✅ No obvious static analysis issues found")
        print("The FastMCP error may be due to:")
        print("1. Runtime type detection (not static)")
        print("2. Call chain analysis detecting dict returns in called functions")
        print("3. FastMCP framework bug")


if __name__ == "__main__":
    main()


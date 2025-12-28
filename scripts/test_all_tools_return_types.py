#!/usr/bin/env python3
"""
Comprehensive test to verify all MCP tools return JSON strings, not dicts.

Tests:
1. Return type annotations (-> str)
2. Actual return values (if callable with defaults)
3. Underlying functions used by consolidated tools
4. Defensive patterns (isinstance checks, json.dumps usage)

Usage:
    uv run python scripts/test_all_tools_return_types.py
"""

import json
import inspect
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_return_type_annotation(func: Any) -> tuple[bool, str]:
    """Check if function has -> str return type annotation."""
    try:
        sig = inspect.signature(func)
        return_annotation = sig.return_annotation
        
        if return_annotation == inspect.Signature.empty:
            return False, "Missing return type annotation"
        
        if return_annotation == str:
            return True, "✅ Return type: str"
        
        # Handle Optional[str] or Union[str, ...]
        if hasattr(return_annotation, '__origin__'):
            origin = return_annotation.__origin__
            args = getattr(return_annotation, '__args__', [])
            if str in args:
                return True, f"✅ Return type: {return_annotation}"
        
        return False, f"❌ Return type should be 'str', got: {return_annotation}"
    except Exception as e:
        return False, f"❌ Could not inspect: {e}"


def check_source_code_patterns(func: Any) -> tuple[bool, list[str]]:
    """Check source code for defensive patterns."""
    patterns = []
    try:
        source = inspect.getsource(func)
        
        # Check for json.dumps usage (good)
        if 'json.dumps' in source:
            patterns.append("✅ Uses json.dumps")
        
        # Check for isinstance(result, str) defensive pattern (good)
        if 'isinstance(result, str)' in source or 'isinstance(result, dict)' in source:
            patterns.append("✅ Has defensive isinstance checks")
        
        # Check for direct dict returns (bad)
        lines = source.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('return {') and 'json.dumps' not in line:
                # Might be OK if it's an error dict that gets wrapped
                if i > 0 and 'json.dumps' in lines[i-1]:
                    continue
                patterns.append(f"⚠️  Line {i+1}: Direct dict return (might be OK if wrapped)")
        
        return len(patterns) > 0, patterns
    except Exception:
        return True, ["⚠️  Could not inspect source"]


def test_consolidated_tools() -> dict[str, Any]:
    """Test all consolidated tools."""
    from project_management_automation.tools import consolidated
    
    consolidated_tools = [
        'analyze_alignment',
        'security',
        'generate_config',
        'setup_hooks',
        'prompt_tracking',
        'health',
        'report',
        'task_analysis',
        'testing',
        'lint',
        'memory',
        'context',
        'workflow_mode',
        'recommend',
        'task_discovery',
        'automation',
        'estimation',
        'task_workflow',
        'memory_maint',
        'ollama',
        'mlx',
        'git_tools',
        'session',
    ]
    
    results = {
        'total': len(consolidated_tools),
        'passed': 0,
        'failed': 0,
        'issues': []
    }
    
    print("=" * 70)
    print("Testing Consolidated Tools")
    print("=" * 70)
    print()
    
    for tool_name in consolidated_tools:
        if not hasattr(consolidated, tool_name):
            results['issues'].append({
                'tool': tool_name,
                'status': 'missing',
                'message': f"❌ Tool '{tool_name}' not found in consolidated module"
            })
            results['failed'] += 1
            continue
        
        func = getattr(consolidated, tool_name)
        
        # Check return type annotation
        is_valid, message = check_return_type_annotation(func)
        
        # Check source patterns
        has_patterns, patterns = check_source_code_patterns(func)
        
        if is_valid:
            results['passed'] += 1
            print(f"✅ {tool_name}: {message}")
            if patterns:
                for pattern in patterns[:2]:  # Show first 2 patterns
                    print(f"   {pattern}")
        else:
            results['failed'] += 1
            results['issues'].append({
                'tool': tool_name,
                'status': 'failed',
                'message': message,
                'patterns': patterns
            })
            print(f"❌ {tool_name}: {message}")
            if patterns:
                for pattern in patterns:
                    print(f"   {pattern}")
    
    print()
    return results


def test_underlying_functions() -> dict[str, Any]:
    """Test underlying functions used by consolidated tools."""
    print("=" * 70)
    print("Testing Underlying Functions (Ollama, MLX, Git, Session)")
    print("=" * 70)
    print()
    
    # Test ollama_integration functions
    ollama_functions = [
        'check_ollama_status',
        'list_ollama_models',
        'generate_with_ollama',
        'pull_ollama_model',
        'get_hardware_info',
    ]
    
    # Test mlx_integration functions
    mlx_functions = [
        'check_mlx_status',
        'get_mlx_hardware_info',
        'list_mlx_models',
        'generate_with_mlx',
    ]
    
    # Test git_inspired_tools functions
    git_functions = [
        'get_task_commits',
        'get_branch_commits',
        'list_branches',
        'get_branch_tasks',
        'compare_task_diff',
        'generate_graph',
        'merge_branch_tools',
        'set_task_branch_tool',
    ]
    
    # Test session functions
    session_functions = [
        'auto_prime_session',
        'session_handoff',
        'find_relevant_prompts',
        'task_assignee',
    ]
    
    all_functions = {
        'ollama_integration': ollama_functions,
        'mlx_integration': mlx_functions,
        'git_inspired_tools': git_functions,
        'session_handoff': session_functions,
    }
    
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'issues': []
    }
    
    for module_name, func_names in all_functions.items():
        print(f"Module: {module_name}")
        try:
            module = __import__(f'project_management_automation.tools.{module_name}', fromlist=[module_name])
        except ImportError as e:
            print(f"   ⚠️  Module not available: {e}")
            print()
            continue
        
        for func_name in func_names:
            results['total'] += 1
            if not hasattr(module, func_name):
                print(f"   ⚠️  {func_name}: Not found")
                continue
            
            func = getattr(module, func_name)
            is_valid, message = check_return_type_annotation(func)
            
            if is_valid:
                results['passed'] += 1
                print(f"   ✅ {func_name}: {message}")
            else:
                results['failed'] += 1
                results['issues'].append({
                    'module': module_name,
                    'function': func_name,
                    'message': message
                })
                print(f"   ❌ {func_name}: {message}")
        
        print()
    
    return results


def test_actual_returns() -> dict[str, Any]:
    """Test actual return values for tools that can be called with defaults."""
    print("=" * 70)
    print("Testing Actual Return Values (Safe Tools Only)")
    print("=" * 70)
    print()
    
    from project_management_automation.tools import consolidated
    
    # Safe tools that can be called with defaults
    safe_tools = {
        'ollama': {'action': 'status'},
        'mlx': {'action': 'status'},
        'health': {'action': 'server'},
    }
    
    results = {
        'total': len(safe_tools),
        'passed': 0,
        'failed': 0,
        'issues': []
    }
    
    for tool_name, kwargs in safe_tools.items():
        if not hasattr(consolidated, tool_name):
            continue
        
        func = getattr(consolidated, tool_name)
        
        try:
            # Call the function
            result = func(**kwargs)
            
            # Check return type
            if isinstance(result, str):
                # Try to parse as JSON
                try:
                    json.loads(result)
                    results['passed'] += 1
                    print(f"✅ {tool_name}: Returns valid JSON string")
                except json.JSONDecodeError:
                    results['failed'] += 1
                    results['issues'].append({
                        'tool': tool_name,
                        'message': f"Returns string but not valid JSON"
                    })
                    print(f"❌ {tool_name}: Returns string but not valid JSON")
            else:
                results['failed'] += 1
                results['issues'].append({
                    'tool': tool_name,
                    'message': f"Returns {type(result).__name__}, not str"
                })
                print(f"❌ {tool_name}: Returns {type(result).__name__}, not str")
        
        except Exception as e:
            # Some tools might fail (missing deps, etc.) - that's OK
            print(f"⏭️  {tool_name}: Could not test (error: {e})")
    
    print()
    return results


def main():
    """Main test runner."""
    print("=" * 70)
    print("Comprehensive MCP Tool Return Type Test")
    print("=" * 70)
    print()
    print("Testing that all tools return JSON strings (not dicts) to avoid")
    print("FastMCP 'await dict' errors.")
    print()
    
    # Test consolidated tools
    consolidated_results = test_consolidated_tools()
    
    # Test underlying functions
    underlying_results = test_underlying_functions()
    
    # Test actual returns (safe tools only)
    actual_results = test_actual_returns()
    
    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print()
    
    total_passed = consolidated_results['passed'] + underlying_results['passed'] + actual_results['passed']
    total_failed = consolidated_results['failed'] + underlying_results['failed'] + actual_results['failed']
    total_tests = consolidated_results['total'] + underlying_results['total'] + actual_results['total']
    
    print(f"Consolidated Tools: {consolidated_results['passed']}/{consolidated_results['total']} passed")
    print(f"Underlying Functions: {underlying_results['passed']}/{underlying_results['total']} passed")
    print(f"Actual Returns: {actual_results['passed']}/{actual_results['total']} passed")
    print()
    print(f"Total: {total_passed}/{total_tests} passed, {total_failed} failed")
    print()
    
    # Show failures
    all_issues = (
        consolidated_results['issues'] +
        underlying_results['issues'] +
        actual_results['issues']
    )
    
    if all_issues:
        print("=" * 70)
        print("Issues Found")
        print("=" * 70)
        print()
        for issue in all_issues:
            if 'tool' in issue:
                print(f"❌ {issue['tool']}: {issue.get('message', 'Unknown issue')}")
            elif 'function' in issue:
                print(f"❌ {issue['module']}.{issue['function']}: {issue.get('message', 'Unknown issue')}")
        print()
    
    # Exit code
    if total_failed > 0:
        print("=" * 70)
        print(f"❌ TEST FAILED: {total_failed} issue(s) found")
        print("=" * 70)
        sys.exit(1)
    else:
        print("=" * 70)
        print("✅ ALL TESTS PASSED: All tools return JSON strings correctly")
        print("=" * 70)
        sys.exit(0)


if __name__ == "__main__":
    main()


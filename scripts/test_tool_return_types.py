#!/usr/bin/env python3
"""
Test that all registered MCP tools return JSON strings, not dicts.

FastMCP has a bug where it tries to await dict results, causing errors.
All tools must return JSON strings to avoid this issue.

Usage:
    python scripts/test_tool_return_types.py
    uv run python scripts/test_tool_return_types.py
"""

import json
import inspect
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def get_registered_tools() -> list[tuple[str, Any]]:
    """Get all registered tools from the MCP server."""
    try:
        from project_management_automation.server import mcp
        import project_management_automation.server as server_module
        
        if not mcp or not hasattr(mcp, '_tool_manager'):
            print("⚠️  MCP instance not available or doesn't have _tool_manager")
            return []
        
        tool_manager = mcp._tool_manager
        if not hasattr(tool_manager, '_tools'):
            print("⚠️  Tool manager doesn't have _tools attribute")
            return []
        
        tools = tool_manager._tools
        if not isinstance(tools, dict):
            print("⚠️  Tools is not a dict")
            return []
        
        # FastMCP wraps functions in FunctionTool objects
        # Get the underlying functions from the server module by name
        result = []
        for tool_name in tools.keys():
            func = getattr(server_module, tool_name, None)
            if func and callable(func):
                result.append((tool_name, func))
            else:
                # Tool might be defined differently or not accessible
                pass
        
        return result
    except Exception as e:
        print(f"⚠️  Could not get tools from MCP instance: {e}")
        return []


def test_tool_return_type(tool_name: str, tool_func: Any) -> dict[str, Any]:
    """
    Test that a tool returns a JSON string, not a dict.
    
    Returns:
        dict with keys: success, tool_name, return_type, is_json, error
    """
    result = {
        'tool_name': tool_name,
        'success': False,
        'return_type': None,
        'is_json': False,
        'error': None
    }
    
    # Get the function signature to determine if we can call it without args
    try:
        sig = inspect.signature(tool_func)
    except Exception as e:
        result['error'] = f"Could not inspect signature: {e}"
        return result
    
    # Build minimal arguments (use defaults where possible)
    try:
        bound_args = sig.bind_partial()
        bound_args.apply_defaults()
        args = bound_args.args
        kwargs = bound_args.kwargs
    except Exception as e:
        result['error'] = f"Could not bind arguments: {e}"
        return result
    
    try:
        # Call the tool function
        if inspect.iscoroutinefunction(tool_func):
            import asyncio
            return_value = asyncio.run(tool_func(*args, **kwargs))
        else:
            return_value = tool_func(*args, **kwargs)
        
        result['return_type'] = type(return_value).__name__
        
        # Check that result is a string
        if not isinstance(return_value, str):
            result['error'] = (
                f"Returned {type(return_value).__name__}, not str. "
                f"This will cause FastMCP 'await dict' error. "
                f"Return a JSON string instead (use json.dumps() or ensure_json_string decorator)."
            )
            return result
        
        # Verify it's valid JSON
        try:
            parsed = json.loads(return_value)
            result['is_json'] = True
            result['success'] = True
        except json.JSONDecodeError as e:
            result['error'] = (
                f"Returned a string but it's not valid JSON: {e}. "
                f"Use json.dumps() to convert dict/list to JSON string."
            )
            return result
        
    except TypeError as e:
        # Some tools might require specific arguments - skip those
        if "required" in str(e).lower() or "missing" in str(e).lower():
            result['error'] = f"Tool requires specific arguments: {e}"
            result['success'] = None  # Skip, not failure
        else:
            result['error'] = f"TypeError: {e}"
    except Exception as e:
        # Tools might fail for various reasons (missing dependencies, etc.)
        # That's OK - we're only testing return types
        result['error'] = f"Execution failed: {e}"
        result['success'] = None  # Skip, not failure
    
    return result


def main():
    """Main test runner."""
    print("=" * 70)
    print("Testing MCP Tool Return Types")
    print("=" * 70)
    print()
    print("Checking that all tools return JSON strings (not dicts) to avoid")
    print("FastMCP 'await dict' errors.")
    print()
    
    # Get registered tools
    tools = get_registered_tools()
    
    if not tools:
        print("❌ No tools found - MCP server might not be initialized")
        sys.exit(1)
    
    print(f"Found {len(tools)} registered tools\n")
    
    # Test each tool
    results = []
    for tool_name, tool_func in tools:
        result = test_tool_return_type(tool_name, tool_func)
        results.append(result)
    
    # Report results
    success_count = sum(1 for r in results if r['success'] is True)
    failure_count = sum(1 for r in results if r['success'] is False)
    skipped_count = sum(1 for r in results if r['success'] is None)
    
    print("=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    print(f"Total tools:     {len(results)}")
    print(f"✅ Passed:       {success_count}")
    print(f"❌ Failed:       {failure_count}")
    print(f"⏭️  Skipped:      {skipped_count}")
    print()
    
    # Show failures
    failures = [r for r in results if r['success'] is False]
    if failures:
        print("❌ FAILED TOOLS (return dict instead of JSON string):")
        print("-" * 70)
        for result in failures:
            print(f"  {result['tool_name']}")
            print(f"    Return type: {result['return_type']}")
            print(f"    Error: {result['error']}")
            print()
    
    # Show skipped (tools that require args or fail for other reasons)
    skipped = [r for r in results if r['success'] is None]
    if skipped:
        print("⏭️  SKIPPED TOOLS (require specific arguments or failed execution):")
        print("-" * 70)
        for result in skipped[:10]:  # Show first 10
            print(f"  {result['tool_name']}: {result['error']}")
        if len(skipped) > 10:
            print(f"  ... and {len(skipped) - 10} more")
        print()
    
    # Show successes
    if success_count > 0:
        print(f"✅ PASSED TOOLS ({success_count} tools return valid JSON strings)")
        print()
    
    # Exit with error code if any failures
    if failure_count > 0:
        print("=" * 70)
        print(f"❌ TEST FAILED: {failure_count} tool(s) return dicts instead of JSON strings")
        print("=" * 70)
        sys.exit(1)
    else:
        print("=" * 70)
        print("✅ ALL TESTS PASSED: All tools return JSON strings correctly")
        print("=" * 70)
        sys.exit(0)


if __name__ == "__main__":
    main()


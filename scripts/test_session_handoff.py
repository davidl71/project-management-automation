#!/usr/bin/env python3
"""
Test script for session handoff tool fixes.

This script tests the session handoff functionality to verify that:
1. All functions return proper JSON strings
2. Async operations are handled safely
3. Error handling works correctly
4. No dicts are returned that could cause await errors

Usage:
    python scripts/test_session_handoff.py
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from project_management_automation.tools.session_handoff import (
    session_handoff,
    resume_session,
    get_latest_handoff,
    list_handoffs,
    end_session,
)


def test_json_return_values():
    """Test that all functions return valid JSON strings, not dicts."""
    print("=" * 60)
    print("Testing JSON return values...")
    print("=" * 60)
    
    results = []
    
    # Test resume_session
    try:
        result = resume_session()
        assert isinstance(result, str), f"resume_session returned {type(result)}, expected str"
        parsed = json.loads(result)
        assert isinstance(parsed, dict), "Parsed result should be a dict"
        results.append(("resume_session", True, "Returns valid JSON string"))
        print("✓ resume_session returns valid JSON string")
    except Exception as e:
        results.append(("resume_session", False, str(e)))
        print(f"✗ resume_session failed: {e}")
    
    # Test get_latest_handoff
    try:
        result = get_latest_handoff()
        assert isinstance(result, str), f"get_latest_handoff returned {type(result)}, expected str"
        parsed = json.loads(result)
        results.append(("get_latest_handoff", True, "Returns valid JSON string"))
        print("✓ get_latest_handoff returns valid JSON string")
    except Exception as e:
        results.append(("get_latest_handoff", False, str(e)))
        print(f"✗ get_latest_handoff failed: {e}")
    
    # Test list_handoffs
    try:
        result = list_handoffs(limit=3)
        assert isinstance(result, str), f"list_handoffs returned {type(result)}, expected str"
        parsed = json.loads(result)
        results.append(("list_handoffs", True, "Returns valid JSON string"))
        print("✓ list_handoffs returns valid JSON string")
    except Exception as e:
        results.append(("list_handoffs", False, str(e)))
        print(f"✗ list_handoffs failed: {e}")
    
    # Test session_handoff wrapper with various actions
    actions = ["resume", "latest", "list"]
    for action in actions:
        try:
            result = session_handoff(action=action, limit=2)
            assert isinstance(result, str), f"session_handoff({action}) returned {type(result)}, expected str"
            parsed = json.loads(result)
            results.append((f"session_handoff({action})", True, "Returns valid JSON string"))
            print(f"✓ session_handoff('{action}') returns valid JSON string")
        except Exception as e:
            results.append((f"session_handoff({action})", False, str(e)))
            print(f"✗ session_handoff('{action}') failed: {e}")
    
    # Test error handling with invalid action
    try:
        result = session_handoff(action="invalid_action")
        assert isinstance(result, str), "Error case should still return JSON string"
        parsed = json.loads(result)
        assert "error" in parsed, "Error response should contain 'error' field"
        results.append(("session_handoff(error)", True, "Returns valid JSON string on error"))
        print("✓ session_handoff returns valid JSON string on error")
    except Exception as e:
        results.append(("session_handoff(error)", False, str(e)))
        print(f"✗ session_handoff error handling failed: {e}")
    
    return results


def test_async_safety():
    """Test that async operations are handled safely."""
    print("\n" + "=" * 60)
    print("Testing async safety...")
    print("=" * 60)
    
    results = []
    
    # Import the helper function
    try:
        from project_management_automation.tools.session_handoff import _run_async_safe
        import asyncio
        
        # Test that helper exists and is callable
        assert callable(_run_async_safe), "_run_async_safe should be callable"
        results.append(("_run_async_safe exists", True, "Helper function available"))
        print("✓ _run_async_safe helper function exists")
        
        # Test that it can handle a simple async function
        async def simple_async():
            return "test_result"
        
        try:
            result = _run_async_safe(simple_async())
            assert result == "test_result", f"Expected 'test_result', got {result}"
            results.append(("_run_async_safe works", True, "Can run async functions safely"))
            print("✓ _run_async_safe can execute async functions")
        except Exception as e:
            results.append(("_run_async_safe works", False, str(e)))
            print(f"✗ _run_async_safe execution failed: {e}")
            
    except ImportError as e:
        results.append(("_run_async_safe import", False, str(e)))
        print(f"✗ Could not import _run_async_safe: {e}")
    
    return results


def test_error_handling():
    """Test error handling returns JSON strings."""
    print("\n" + "=" * 60)
    print("Testing error handling...")
    print("=" * 60)
    
    results = []
    
    # Test that unknown actions return proper error JSON
    try:
        result = session_handoff(action="unknown_action_xyz")
        assert isinstance(result, str), "Should return JSON string on error"
        parsed = json.loads(result)
        assert "error" in parsed or "success" in parsed, "Should contain error or success field"
        results.append(("Error handling", True, "Returns JSON string on errors"))
        print("✓ Error handling returns valid JSON strings")
    except Exception as e:
        results.append(("Error handling", False, str(e)))
        print(f"✗ Error handling test failed: {e}")
    
    return results


def print_summary(all_results):
    """Print test summary."""
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    total = len(all_results)
    passed = sum(1 for _, success, _ in all_results if success)
    failed = total - passed
    
    print(f"\nTotal tests: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    
    if failed > 0:
        print("\nFailed tests:")
        for name, success, message in all_results:
            if not success:
                print(f"  - {name}: {message}")
    
    print("\n" + "=" * 60)
    
    return failed == 0


def main():
    """Run all tests."""
    print("Session Handoff Tool Test Suite")
    print("=" * 60)
    print(f"Testing session handoff fixes...")
    print(f"Project root: {project_root}")
    print()
    
    all_results = []
    
    # Run all test suites
    all_results.extend(test_json_return_values())
    all_results.extend(test_async_safety())
    all_results.extend(test_error_handling())
    
    # Print summary
    success = print_summary(all_results)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

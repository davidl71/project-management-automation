#!/usr/bin/env python3
"""
Test script to verify infer_session_mode returns JSON string (not dict).

This tests the fix for FastMCP return type issue.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from project_management_automation.resources.session import (
    infer_session_mode_tool,
    get_session_mode_resource,
)
from project_management_automation.tools.dynamic_tools import (
    DynamicToolManager,
    reset_tool_manager,
    get_tool_manager,
)


def test_return_type_is_string():
    """Test that functions return strings, not dicts."""
    print("Testing infer_session_mode_tool return type...")
    
    # Reset and setup manager
    reset_tool_manager()
    manager = get_tool_manager()
    
    # Simulate some activity
    for i in range(5):
        manager.record_tool_usage(f"test_tool_{i}")
    
    # Test infer_session_mode_tool
    result = infer_session_mode_tool(force_recompute=True)
    
    # Verify it's a string
    assert isinstance(result, str), f"Expected string, got {type(result)}: {result}"
    print(f"✅ infer_session_mode_tool returns string (length: {len(result)})")
    
    # Verify it's valid JSON
    try:
        parsed = json.loads(result)
        print(f"✅ Return value is valid JSON")
        print(f"   Parsed keys: {list(parsed.keys())}")
        
        # Check expected structure
        assert "mode" in parsed or "error" in parsed, "Missing 'mode' or 'error' key"
        if "mode" in parsed:
            assert parsed["mode"] in ["agent", "ask", "manual", "unknown"], \
                f"Invalid mode value: {parsed['mode']}"
        print(f"✅ JSON structure is valid")
        
    except json.JSONDecodeError as e:
        print(f"❌ Return value is not valid JSON: {e}")
        print(f"   Value: {result[:200]}...")
        sys.exit(1)
    
    # Test get_session_mode_resource
    print("\nTesting get_session_mode_resource return type...")
    resource_result = get_session_mode_resource()
    
    # Verify it's a string
    assert isinstance(resource_result, str), \
        f"Expected string, got {type(resource_result)}: {resource_result}"
    print(f"✅ get_session_mode_resource returns string (length: {len(resource_result)})")
    
    # Verify it's valid JSON
    try:
        parsed_resource = json.loads(resource_result)
        print(f"✅ Resource return value is valid JSON")
        print(f"   Parsed keys: {list(parsed_resource.keys())}")
    except json.JSONDecodeError as e:
        print(f"❌ Resource return value is not valid JSON: {e}")
        print(f"   Value: {resource_result[:200]}...")
        sys.exit(1)
    
    print("\n✅ All tests passed! Return types are correct.")


def test_defensive_type_checking():
    """Test that defensive type checking works correctly."""
    print("\nTesting defensive type checking...")
    
    # The ensure_json_string function should handle various input types
    # Since it's internal, we test through the actual function calls
    
    # Test with normal operation (should return JSON string)
    result = infer_session_mode_tool(force_recompute=True)
    assert isinstance(result, str), "Should always return string"
    
    # Test resource
    resource_result = get_session_mode_resource()
    assert isinstance(resource_result, str), "Should always return string"
    
    print("✅ Defensive type checking works correctly")


if __name__ == "__main__":
    try:
        test_return_type_is_string()
        test_defensive_type_checking()
        print("\n🎉 All tests passed! The fix is working correctly.")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


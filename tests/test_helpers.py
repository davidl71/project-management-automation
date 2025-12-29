"""
Shared Test Helpers

Common assertion helpers and utilities for test files.
Reduces boilerplate and standardizes test patterns.
"""

import json
from typing import Any, Optional


def assert_success_response(result_str: str, expected_data_keys: Optional[list[str]] = None) -> dict[str, Any]:
    """
    Assert that a tool response indicates success.
    
    Args:
        result_str: JSON string response from tool
        expected_data_keys: Optional list of keys that should exist in 'data'
    
    Returns:
        Parsed result dictionary
    
    Raises:
        AssertionError: If response doesn't indicate success
    """
    result = json.loads(result_str)
    assert result['success'] is True, f"Expected success=True, got {result.get('success')}"
    assert 'data' in result, "Response missing 'data' key"
    
    if expected_data_keys:
        for key in expected_data_keys:
            assert key in result['data'], f"Missing expected key '{key}' in data"
    
    return result


def assert_error_response(
    result_str: str, 
    expected_error_contains: Optional[str] = None
) -> dict[str, Any]:
    """
    Assert that a tool response indicates an error.
    
    Args:
        result_str: JSON string response from tool
        expected_error_contains: Optional substring that should be in error message
    
    Returns:
        Parsed result dictionary
    
    Raises:
        AssertionError: If response doesn't indicate error
    """
    result = json.loads(result_str)
    assert result['success'] is False, f"Expected success=False, got {result.get('success')}"
    assert 'error' in result, "Response missing 'error' key"
    
    if expected_error_contains:
        error_obj = result.get('error', {})
        # Handle both dict and string error formats
        if isinstance(error_obj, dict):
            error_msg = error_obj.get('message', str(error_obj))
        else:
            error_msg = str(error_obj)
        assert expected_error_contains.lower() in error_msg.lower(), \
            f"Expected error to contain '{expected_error_contains}', got '{error_msg}'"
    
    return result


def assert_dry_run_response(result_str: str) -> dict[str, Any]:
    """
    Assert that a tool response indicates a dry run was performed.
    
    Args:
        result_str: JSON string response from tool
    
    Returns:
        Parsed result dictionary
    
    Raises:
        AssertionError: If response doesn't indicate dry run
    """
    result = assert_success_response(result_str)
    assert result.get('data', {}).get('dry_run') is True, \
        "Expected dry_run=True in response data"
    return result


def assert_custom_output_path(result_str: str, expected_path: str) -> dict[str, Any]:
    """
    Assert that a tool response includes a custom output path.
    
    Args:
        result_str: JSON string response from tool
        expected_path: Path that should be in the response
    
    Returns:
        Parsed result dictionary
    
    Raises:
        AssertionError: If path not found in response
    """
    result = assert_success_response(result_str)
    report_path = result.get('data', {}).get('report_path', '')
    assert expected_path in report_path, \
        f"Expected path '{expected_path}' not found in report_path '{report_path}'"
    return result


def parse_json_response(result_str: str) -> dict[str, Any]:
    """
    Parse a JSON string response, handling both dict and str inputs.
    
    Args:
        result_str: JSON string or dict response
    
    Returns:
        Parsed dictionary
    """
    if isinstance(result_str, dict):
        return result_str
    return json.loads(result_str)


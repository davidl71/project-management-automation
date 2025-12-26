#!/usr/bin/env python3
"""Test if @ensure_json_string decorator causes the issue."""

import json
from fastmcp import FastMCP

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Replicate our @ensure_json_string decorator
import functools
import inspect

def ensure_json_string(func):
    """Decorator to ensure function returns JSON string."""
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            if isinstance(result, str):
                return result
            return json.dumps(result, indent=2)
        return async_wrapper
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, str):
                return result
            return json.dumps(result, indent=2)
        return wrapper

# Test 1: Without decorator (should work)
@mcp.tool()
def test_no_decorator() -> str:
    """Test without decorator."""
    return "no decorator result"

# Test 2: With decorator (like our code)
@ensure_json_string
@mcp.tool()
def test_with_decorator() -> str:
    """Test with decorator."""
    return "decorator result"

# Test 3: With decorator returning dict
@ensure_json_string
@mcp.tool()
def test_decorator_dict() -> str:
    """Test with decorator returning dict."""
    return {"status": "success", "message": "dict result"}

# Test 4: Decorator order reversed (decorator after @mcp.tool)
@mcp.tool()
@ensure_json_string
def test_reversed_order() -> str:
    """Test with decorator order reversed."""
    return "reversed order result"

if __name__ == "__main__":
    # Run the server
    mcp.run()


#!/usr/bin/env python3
"""Test if calling underlying functions causes the issue."""

import json
from fastmcp import FastMCP

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Simulate our pattern: underlying function in separate module
def _underlying_function() -> str:
    """Underlying function that returns a string."""
    return "underlying result"

# Simulate our pattern: underlying function returning dict
def _underlying_dict() -> dict:
    """Underlying function that returns a dict."""
    return {"status": "success", "message": "from underlying"}

# Simulate our pattern: underlying function returning JSON string
def _underlying_json() -> str:
    """Underlying function that returns JSON string."""
    return json.dumps({"status": "success", "message": "json from underlying"})

# Test 1: Tool calling underlying function directly (like our code)
@mcp.tool()
def test_call_underlying() -> str:
    """Tool that calls underlying function."""
    return _underlying_function()

# Test 2: Tool calling underlying function with decorator
def ensure_json_string(func):
    """Decorator to ensure function returns JSON string."""
    import functools
    import inspect
    
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

@ensure_json_string
@mcp.tool()
def test_decorator_underlying() -> str:
    """Tool with decorator calling underlying function."""
    return _underlying_function()

# Test 3: Tool calling underlying function that returns dict
@ensure_json_string
@mcp.tool()
def test_decorator_underlying_dict() -> str:
    """Tool with decorator calling underlying function that returns dict."""
    return _underlying_dict()

# Test 4: Tool calling underlying function that returns JSON string
@ensure_json_string
@mcp.tool()
def test_decorator_underlying_json() -> str:
    """Tool with decorator calling underlying function that returns JSON string."""
    return _underlying_json()

# Test 5: Tool with complex call chain (like our automation tool)
def _level1() -> dict:
    """Level 1 function."""
    return {"level": 1, "data": "test"}

def _level2() -> dict:
    """Level 2 function that calls level 1."""
    result = _level1()
    return {"level": 2, "nested": result}

@ensure_json_string
@mcp.tool()
def test_complex_chain() -> str:
    """Tool with complex call chain."""
    return _level2()

if __name__ == "__main__":
    # Run the server
    mcp.run()


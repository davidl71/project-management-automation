#!/usr/bin/env python3
"""Test if importing from separate module causes the issue."""

# Simulate our import structure
import json
from fastmcp import FastMCP

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Simulate importing from a separate module (like consolidated.py)
# In a real scenario, this would be: from .tools.consolidated import automation as _automation

def _underlying_from_module() -> str:
    """Function in a separate module that returns a string."""
    return json.dumps({"status": "success", "message": "from module"})

# Test: Tool that calls function from "module" (simulated)
@mcp.tool()
def test_module_import() -> str:
    """Tool that calls function from separate module."""
    return _underlying_from_module()

# Test with decorator
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
def test_decorator_module_import() -> str:
    """Tool with decorator calling function from module."""
    return _underlying_from_module()

# Test: Simulate our exact pattern - wrapper calling imported function
_imported_function = _underlying_from_module  # Simulate: from module import func as _func

@ensure_json_string
@mcp.tool()
def test_wrapper_pattern() -> str:
    """Tool that matches our exact wrapper pattern."""
    return _imported_function()

if __name__ == "__main__":
    # Run the server
    mcp.run()


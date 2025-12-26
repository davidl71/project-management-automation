#!/usr/bin/env python3
"""Test if dynamic imports inside functions cause the issue."""

import json
from fastmcp import FastMCP

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Simulate our pattern: dynamic import inside function
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

# Create a separate module-like function
def _daily_function() -> str:
    """Simulate run_daily_automation."""
    return json.dumps({"status": "success", "message": "daily result"})

# Test: Tool with dynamic import inside (like our automation function)
@ensure_json_string
@mcp.tool()
def test_dynamic_import(action: str = "daily") -> str:
    """Tool with dynamic import inside function - matches our pattern."""
    if action == "daily":
        # Dynamic import inside function (like our code)
        _daily = _daily_function  # Simulate: from .daily_automation import run_daily_automation
        result = _daily()
        return result if isinstance(result, str) else json.dumps(result, indent=2)
    else:
        return json.dumps({"error": "Unknown action"}, indent=2)

# Test: Tool with actual dynamic import
@ensure_json_string
@mcp.tool()
def test_real_dynamic_import() -> str:
    """Tool with actual dynamic import statement."""
    # This simulates: from .daily_automation import run_daily_automation
    # But we can't do that in a test file, so we'll simulate it differently
    import sys
    import importlib
    
    # Try to import something dynamically
    try:
        # Import json module dynamically (safe test)
        json_module = importlib.import_module('json')
        result = json_module.dumps({"status": "success", "message": "dynamic import"})
        return result
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

if __name__ == "__main__":
    # Run the server
    mcp.run()


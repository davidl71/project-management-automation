#!/usr/bin/env python3
"""Test if import timing causes the issue."""

import json
import sys
from typing import Optional
from fastmcp import FastMCP

# Create FastMCP FIRST (like our server does)
mcp = FastMCP("Test Server")

# THEN import (like our server does in register_tools)
print("DEBUG: About to import automation function", file=sys.stderr, flush=True)

# Simulate importing from consolidated.py
def _automation(
    action: str = "daily",
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
) -> str:
    """Simulated automation function."""
    return json.dumps({"status": "success", "action": action}, indent=2)

print("DEBUG: Imported automation function", file=sys.stderr, flush=True)

# NOW register tool (like our server does)
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
def automation_tool(
    action: str = "daily",
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
) -> str:
    """Automation tool - registered AFTER FastMCP init and import."""
    print("DEBUG: automation_tool called", file=sys.stderr, flush=True)
    return _automation(action=action, tasks=tasks, include_slow=include_slow)

print("DEBUG: Registered automation_tool", file=sys.stderr, flush=True)

if __name__ == "__main__":
    # Run the server
    mcp.run()


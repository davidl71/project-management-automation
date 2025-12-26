#!/usr/bin/env python3
"""Test exact replication of our automation tool pattern."""

import json
from fastmcp import FastMCP
from typing import Optional

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Replicate our exact pattern
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

# Simulate _automation from consolidated.py
def _automation(
    action: str = "daily",
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
) -> str:
    """Simulate automation function from consolidated.py."""
    if action == "daily":
        # Simulate: from .daily_automation import run_daily_automation
        def run_daily_automation(tasks, include_slow, dry_run, output_path):
            return json.dumps({"status": "success", "tasks_run": 0}, indent=2)
        
        result = run_daily_automation(tasks, include_slow, False, None)
        return result if isinstance(result, str) else json.dumps(result, indent=2)
    else:
        return json.dumps({"error": "Unknown action"}, indent=2)

# Replicate our exact server.py pattern
@ensure_json_string
@mcp.tool()
def automation(
    action: str = "daily",
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
) -> str:
    """Exact replication of our automation tool."""
    if _automation is None:
        return json.dumps({
            "success": False,
            "error": "automation tool not available - import failed"
        }, indent=2)
    
    # This is our exact pattern
    return _automation(
        action=action,
        tasks=tasks,
        include_slow=include_slow,
    )

if __name__ == "__main__":
    # Run the server
    mcp.run()


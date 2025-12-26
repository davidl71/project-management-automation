#!/usr/bin/env python3
"""Minimal MCP server with REAL import from daily_automation.py."""

import json
import sys
from typing import Optional
from fastmcp import FastMCP

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Try to import the REAL run_daily_automation
try:
    # Add project path
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    from project_management_automation.tools.daily_automation import run_daily_automation
    REAL_IMPORT_AVAILABLE = True
    print("DEBUG: Successfully imported run_daily_automation", file=sys.stderr, flush=True)
except Exception as e:
    REAL_IMPORT_AVAILABLE = False
    print(f"DEBUG: Failed to import run_daily_automation: {e}", file=sys.stderr, flush=True)
    
    # Fallback mock
    def run_daily_automation(tasks, include_slow, dry_run, output_path):
        return json.dumps({"status": "error", "error": "Import failed"}, indent=2)

# Copy the exact automation function from consolidated.py
def automation(
    action: str = "daily",
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
    dry_run: bool = False,
    output_path: Optional[str] = None,
) -> str:
    """Unified automation tool - with REAL import."""
    print("DEBUG [test_real_import automation] ENTRY", file=sys.stderr, flush=True)
    
    if action == "daily":
        print("DEBUG [test_real_import automation] action=daily branch", file=sys.stderr, flush=True)
        print("DEBUG [test_real_import automation] Calling REAL run_daily_automation", file=sys.stderr, flush=True)
        result = run_daily_automation(tasks, include_slow, dry_run, output_path)
        print(f"DEBUG [test_real_import automation] run_daily_automation returned: type={type(result)}", file=sys.stderr, flush=True)
        final_result = result if isinstance(result, str) else json.dumps(result, indent=2)
        print(f"DEBUG [test_real_import automation] RETURNING: type={type(final_result)}", file=sys.stderr, flush=True)
        return final_result
    else:
        return json.dumps({"error": "Unknown action"}, indent=2)

# Replicate our exact server.py pattern
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
    dry_run: bool = False,
    output_path: Optional[str] = None,
) -> str:
    """Automation tool with REAL import."""
    print("DEBUG [test_real_import automation_tool] ENTRY", file=sys.stderr, flush=True)
    result = automation(
        action=action,
        tasks=tasks,
        include_slow=include_slow,
        dry_run=dry_run,
        output_path=output_path,
    )
    print(f"DEBUG [test_real_import automation_tool] Returning: type={type(result)}", file=sys.stderr, flush=True)
    return result

if __name__ == "__main__":
    # Run the server
    mcp.run()


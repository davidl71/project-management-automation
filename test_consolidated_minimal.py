#!/usr/bin/env python3
"""Minimal MCP server with consolidated.py automation function."""

import json
import sys
from typing import Optional
from fastmcp import FastMCP

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Copy the exact automation function from consolidated.py
def automation(
    action: str = "daily",
    # daily params
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
    # nightly params
    max_tasks_per_host: int = 5,
    max_parallel_tasks: int = 10,
    priority_filter: Optional[str] = None,
    tag_filter: Optional[list[str]] = None,
    # sprint params
    max_iterations: int = 10,
    auto_approve: bool = True,
    extract_subtasks: bool = True,
    run_analysis_tools: bool = True,
    run_testing_tools: bool = True,
    # discover params
    min_value_score: float = 0.7,
    # common params
    dry_run: bool = False,
    output_path: Optional[str] = None,
    notify: bool = False,
) -> str:
    """
    Unified automation tool - COPIED FROM consolidated.py
    
    This is the exact function from consolidated.py to test if it causes the bug.
    """
    print("DEBUG [test_consolidated_minimal automation] ENTRY", file=sys.stderr, flush=True)
    print(f"DEBUG [test_consolidated_minimal automation] action={action}, tasks={tasks}", file=sys.stderr, flush=True)
    
    if action == "daily":
        print("DEBUG [test_consolidated_minimal automation] action=daily branch", file=sys.stderr, flush=True)
        # Simulate: from .daily_automation import run_daily_automation
        # For testing, we'll create a mock function
        def run_daily_automation(tasks, include_slow, dry_run, output_path):
            """Mock run_daily_automation that returns a string."""
            return json.dumps({
                "success": True,
                "data": {
                    "tasks_run": 0,
                    "tasks_succeeded": 0,
                    "tasks_failed": 0,
                    "success_rate": 100.0,
                    "duration_seconds": 0,
                }
            }, indent=2)
        
        print("DEBUG [test_consolidated_minimal automation] Calling run_daily_automation", file=sys.stderr, flush=True)
        result = run_daily_automation(tasks, include_slow, dry_run, output_path)
        print(f"DEBUG [test_consolidated_minimal automation] run_daily_automation returned: type={type(result)}", file=sys.stderr, flush=True)
        final_result = result if isinstance(result, str) else json.dumps(result, indent=2)
        print(f"DEBUG [test_consolidated_minimal automation] RETURNING (daily): type={type(final_result)}, len={len(final_result) if isinstance(final_result, str) else 'N/A'}", file=sys.stderr, flush=True)
        return final_result
    
    elif action == "nightly":
        # Mock nightly function
        def run_nightly_task_automation(**kwargs):
            return json.dumps({"status": "success", "message": "nightly mock"}, indent=2)
        
        result = run_nightly_task_automation(
            max_tasks_per_host=max_tasks_per_host,
            max_parallel_tasks=max_parallel_tasks,
            priority_filter=priority_filter,
            tag_filter=tag_filter,
            dry_run=dry_run,
            notify=notify,
        )
        return result if isinstance(result, str) else json.dumps(result, indent=2)
    
    elif action == "sprint":
        # Mock sprint function
        def sprint_automation(**kwargs):
            return json.dumps({"status": "success", "message": "sprint mock"}, indent=2)
        
        result = sprint_automation(
            max_iterations=max_iterations,
            auto_approve=auto_approve,
            extract_subtasks=extract_subtasks,
            run_analysis_tools=run_analysis_tools,
            run_testing_tools=run_testing_tools,
            priority_filter=priority_filter,
            tag_filter=tag_filter,
            dry_run=dry_run,
            output_path=output_path,
            notify=notify,
        )
        return result if isinstance(result, str) else json.dumps(result, indent=2)
    
    elif action == "discover":
        # Mock discover function
        def find_automation_opportunities(min_value_score, output_path):
            return json.dumps({"status": "success", "message": "discover mock"}, indent=2)
        
        result = find_automation_opportunities(min_value_score, output_path)
        return result if isinstance(result, str) else json.dumps(result, indent=2)
    
    else:
        return json.dumps({
            "status": "error",
            "error": f"Unknown automation action: {action}. Use 'daily', 'nightly', 'sprint', or 'discover'.",
        }, indent=2)


# Replicate our exact server.py pattern with decorator
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

# Register with FastMCP using our exact pattern
@ensure_json_string
@mcp.tool()
def automation_tool(
    action: str = "daily",
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
    max_tasks_per_host: int = 5,
    max_parallel_tasks: int = 10,
    priority_filter: Optional[str] = None,
    tag_filter: Optional[list[str]] = None,
    max_iterations: int = 10,
    auto_approve: bool = True,
    extract_subtasks: bool = True,
    run_analysis_tools: bool = True,
    run_testing_tools: bool = True,
    min_value_score: float = 0.7,
    dry_run: bool = False,
    output_path: Optional[str] = None,
    notify: bool = False,
) -> str:
    """Automation tool - exact replication of server.py pattern."""
    print("DEBUG [test_consolidated_minimal automation_tool] ENTRY", file=sys.stderr, flush=True)
    
    # Call the underlying function (like our server.py does)
    result = automation(
        action=action,
        tasks=tasks,
        include_slow=include_slow,
        max_tasks_per_host=max_tasks_per_host,
        max_parallel_tasks=max_parallel_tasks,
        priority_filter=priority_filter,
        tag_filter=tag_filter,
        max_iterations=max_iterations,
        auto_approve=auto_approve,
        extract_subtasks=extract_subtasks,
        run_analysis_tools=run_analysis_tools,
        run_testing_tools=run_testing_tools,
        min_value_score=min_value_score,
        dry_run=dry_run,
        output_path=output_path,
        notify=notify,
    )
    
    print(f"DEBUG [test_consolidated_minimal automation_tool] Returning: type={type(result)}", file=sys.stderr, flush=True)
    return result

if __name__ == "__main__":
    # Run the server
    mcp.run()


"""
Tool Count Health Check

Monitors the number of registered MCP tools against the design constraint (≤30).
Can be run as part of daily automation or triggered by context primer.

Design Goal: Keep tool count ≤30 to prevent context pollution in AI workflows.
"""

import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Design constraint
MAX_TOOL_COUNT = 30

# Tool categories for consolidation suggestions
CONSOLIDATION_CANDIDATES = {
    "assignee": [
        "assign_todo2_task",
        "unassign_todo2_task",
        "list_todo2_tasks_by_assignee",
        "get_todo2_workload_summary",
        "bulk_assign_todo2_tasks",
        "auto_assign_todo2_background_tasks",
    ],
    "security": [
        "scan_dependency_security",
        "fetch_dependabot_alerts",
        "generate_security_report",
    ],
    "testing": [
        "run_tests",
        "analyze_test_coverage",
        "check_definition_of_done",
    ],
    "memory": [
        "save_memory",
        "recall_memory",
        "search_memories",
    ],
}


def _count_registered_tools() -> Dict[str, Any]:
    """Count tools registered in the MCP server."""
    try:
        # Try to import from server to get actual count
        from project_management_automation.server import mcp
        
        # Get tool count from MCP instance
        if hasattr(mcp, '_tools'):
            tools = list(mcp._tools.keys())
            return {
                "count": len(tools),
                "tools": tools,
                "source": "mcp_instance",
            }
    except Exception as e:
        logger.debug(f"Could not get tools from MCP instance: {e}")
    
    # Fallback: estimate from known registrations
    estimated_count = 25 + 6 + 2 + 2  # server.py + assignee + auto_primer + prompt_discovery
    return {
        "count": estimated_count,
        "tools": [],
        "source": "estimated",
        "note": "Could not access MCP instance, using estimate",
    }


def check_tool_count_health(
    include_suggestions: bool = True,
    create_task: bool = False
) -> str:
    """
    [HINT: Tool count health. Checks if tool count exceeds 30. Returns count, status, consolidation suggestions.]

    Check if the MCP server tool count exceeds the design constraint (≤30).

    Args:
        include_suggestions: Include consolidation suggestions if over limit
        create_task: Create a Todo2 task if over limit

    Returns:
        JSON with tool count health status

    Example:
        check_tool_count_health()
        → {"count": 35, "limit": 30, "status": "over_limit", "suggestions": [...]}
    """
    start_time = time.time()

    try:
        tool_info = _count_registered_tools()
        count = tool_info["count"]
        
        # Determine status
        if count <= MAX_TOOL_COUNT:
            status = "healthy"
            message = f"Tool count ({count}) is within limit (≤{MAX_TOOL_COUNT})"
        elif count <= MAX_TOOL_COUNT + 5:
            status = "warning"
            message = f"Tool count ({count}) is slightly over limit ({MAX_TOOL_COUNT})"
        else:
            status = "over_limit"
            message = f"Tool count ({count}) exceeds limit ({MAX_TOOL_COUNT}) - consolidation needed"

        result = {
            "count": count,
            "limit": MAX_TOOL_COUNT,
            "status": status,
            "message": message,
            "source": tool_info["source"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        # Add suggestions if over limit
        if status in ["warning", "over_limit"] and include_suggestions:
            suggestions = []
            for category, tools in CONSOLIDATION_CANDIDATES.items():
                if len(tools) > 1:
                    suggestions.append({
                        "category": category,
                        "tools": tools,
                        "suggestion": f"Consolidate {len(tools)} {category} tools into 1 tool with action= parameter",
                        "savings": len(tools) - 1,
                    })
            
            result["consolidation_suggestions"] = suggestions
            result["potential_savings"] = sum(s["savings"] for s in suggestions)

        # Create task if requested and over limit
        if create_task and status in ["warning", "over_limit"]:
            try:
                from project_management_automation.utils import find_project_root
                import json as json_mod
                from pathlib import Path
                
                project_root = find_project_root()
                todo2_file = project_root / ".todo2" / "state.todo2.json"
                
                if todo2_file.exists():
                    state = json_mod.loads(todo2_file.read_text())
                    todos = state.get("todos", [])
                    
                    # Check if task already exists
                    existing = [t for t in todos if "tool count" in t.get("name", "").lower()]
                    if not existing:
                        from project_management_automation.utils import annotate_task_project, get_current_project_id
                        project_id = get_current_project_id(project_root)
                        new_task = annotate_task_project({
                            "id": f"TOOL-COUNT-{int(time.time())}",
                            "name": f"Consolidate tools: {count} exceeds limit of {MAX_TOOL_COUNT}",
                            "long_description": f"Tool count health check detected {count} tools, exceeding the design limit of {MAX_TOOL_COUNT}.\n\nConsolidation suggestions:\n" + "\n".join(f"- {s['suggestion']}" for s in result.get("consolidation_suggestions", [])),
                            "status": "Todo",
                            "priority": "high",
                            "tags": ["automation", "consolidation", "tool-count"],
                            "created": datetime.utcnow().isoformat() + "Z",
                            "lastModified": datetime.utcnow().isoformat() + "Z",
                        }, project_id)
                        todos.append(new_task)
                        state["todos"] = todos
                        todo2_file.write_text(json_mod.dumps(state, indent=2))
                        result["task_created"] = new_task["id"]
            except Exception as e:
                logger.warning(f"Could not create task: {e}")
                result["task_error"] = str(e)

        duration = time.time() - start_time
        result["duration_ms"] = round(duration * 1000, 2)

        return json.dumps(result, indent=2)

    except Exception as e:
        logger.error(f"Error checking tool count health: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "limit": MAX_TOOL_COUNT,
        }, indent=2)


def get_tool_count_for_context_primer() -> Dict[str, Any]:
    """
    Get tool count info for inclusion in context primer.
    Returns a compact dict suitable for context priming.
    """
    tool_info = _count_registered_tools()
    count = tool_info["count"]
    
    return {
        "tool_count": count,
        "limit": MAX_TOOL_COUNT,
        "status": "healthy" if count <= MAX_TOOL_COUNT else "over_limit",
        "over_by": max(0, count - MAX_TOOL_COUNT),
    }


# Register with daily automation
DAILY_AUTOMATION_TASK = {
    "task_id": "tool_count_health",
    "task_name": "Tool Count Health Check",
    "function": check_tool_count_health,
    "default_args": {"include_suggestions": True, "create_task": True},
    "category": "health",
    "is_slow": False,
}


__all__ = [
    "check_tool_count_health",
    "get_tool_count_for_context_primer",
    "MAX_TOOL_COUNT",
    "DAILY_AUTOMATION_TASK",
]


"""
MCP Resource Handler for Automation Status

Provides resource access to automation server status and health.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def get_status_resource() -> str:
    """
    Get automation server status as resource.

    Returns:
        JSON string with server status, tools, and health information
    """
    try:
        # Check if tools are available by checking if tool files exist
        tools_dir = Path(__file__).parent.parent / 'tools'
        tool_files = [
            'docs_health.py',
            'todo2_alignment.py',
            'duplicate_detection.py',
            'dependency_security.py',
            'automation_opportunities.py',
            'todo_sync.py',
            'pwa_review.py'
        ]

        tools_available = all((tools_dir / tool_file).exists() for tool_file in tool_files)
        error_handler_available = (Path(__file__).parent.parent / 'error_handler.py').exists()

        status = {
            "server": "project-management-automation",
            "version": "0.1.6",
            "status": "operational",
            "mcp_available": True,  # Assumed if resource is being called
            "tools_available": tools_available,
            "error_handling_available": error_handler_available,
            "timestamp": datetime.now().isoformat(),
            "tools": {
                "total": 20 if tools_available else 1,
                "high_priority": 5 if tools_available else 0,
                "medium_priority": 13 if tools_available else 0,
                "low_priority": 1 if tools_available else 0,
                "available": [
                    "server_status",
                    "check_documentation_health_tool",
                    "analyze_todo2_alignment_tool",
                    "detect_duplicate_tasks_tool",
                    "scan_dependency_security_tool",
                    "find_automation_opportunities_tool",
                    "sync_todo_tasks_tool",
                    "review_pwa_config_tool",
                    "add_external_tool_hints_tool",
                    "run_daily_automation_tool",
                    "validate_ci_cd_workflow_tool",
                    "batch_approve_tasks_tool",
                    "run_nightly_task_automation_tool",
                    "check_working_copy_health_tool",
                    "resolve_task_clarification_tool",
                    "resolve_multiple_clarifications_tool",
                    "list_tasks_awaiting_clarification_tool",
                    "setup_git_hooks_tool",
                    "setup_pattern_triggers_tool",
                    "simplify_rules_tool"
                ] if tools_available else ["server_status"]
            }
        }

        return json.dumps(status, indent=2)

    except Exception as e:
        logger.error(f"Error getting status resource: {e}")
        return json.dumps({
            "server": "project-management-automation",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

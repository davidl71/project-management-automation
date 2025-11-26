"""
MCP Tool Wrapper for Sprint Automation

Wraps SprintAutomation to expose as MCP tool.
"""

import json
import logging
import time
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)

# Import error handler
try:
    from ..error_handler import (
        format_success_response,
        format_error_response,
        log_automation_execution,
        ErrorCode
    )
except ImportError:
    import sys
    server_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(server_dir))
    try:
        from error_handler import (
            format_success_response,
            format_error_response,
            log_automation_execution,
            ErrorCode
        )
    except ImportError:
        def format_success_response(data, message=None):
            return {"success": True, "data": data, "timestamp": time.time()}
        def format_error_response(error, error_code, include_traceback=False):
            return {"success": False, "error": {"code": str(error_code), "message": str(error)}}
        def log_automation_execution(name, duration, success, error=None):
            logger.info(f"{name}: {duration:.2f}s, success={success}")
        class ErrorCode:
            AUTOMATION_ERROR = "AUTOMATION_ERROR"


def sprint_automation(
    max_iterations: int = 10,
    auto_approve: bool = True,
    extract_subtasks: bool = True,
    run_analysis_tools: bool = True,
    run_testing_tools: bool = True,
    priority_filter: Optional[str] = None,
    tag_filter: Optional[List[str]] = None,
    dry_run: bool = False,
    output_path: Optional[str] = None
) -> str:
    """
    Systematically sprint through project processing all background-capable tasks.

    Args:
        max_iterations: Maximum sprint iterations (default: 10)
        auto_approve: Auto-approve tasks without clarification (default: true)
        extract_subtasks: Extract subtasks from parent tasks (default: true)
        run_analysis_tools: Run docs health, alignment, duplicates (default: true)
        run_testing_tools: Run tests and coverage (default: true)
        priority_filter: Only process high/medium/low priority (optional)
        tag_filter: Only process tasks with specific tags (optional)
        dry_run: Preview mode without making changes (default: false)
        output_path: Path for sprint report (default: docs/SPRINT_AUTOMATION_REPORT.md)

    Returns:
        JSON string with sprint automation results including:
        - Subtasks extracted
        - Tasks auto-approved
        - Tasks processed
        - Analysis results
        - Testing results
        - AI wishlist
        - Human wishlist
        - Human contribution opportunities
        - Blockers identified
        - Sprint report path
    """
    start_time = time.time()

    try:
        from project_management_automation.scripts.automate_sprint import SprintAutomation
        from project_management_automation.utils import find_project_root
        
        project_root = find_project_root(Path(__file__).parent.parent.parent.parent)

        config = {
            'max_iterations': max_iterations,
            'auto_approve': auto_approve,
            'extract_subtasks': extract_subtasks,
            'run_analysis_tools': run_analysis_tools,
            'run_testing_tools': run_testing_tools,
            'priority_filter': priority_filter,
            'tag_filter': tag_filter,
            'dry_run': dry_run
        }

        automation = SprintAutomation(config, project_root)
        results = automation.run()

        # Format response
        # Results are nested: results['results']['results'] contains sprint_results
        inner_results = results.get('results', {})
        sprint_results = inner_results.get('results', {}) if isinstance(inner_results, dict) else {}
        response_data = {
            'iterations': inner_results.get('iterations', 0),
            'subtasks_extracted': sprint_results.get('subtasks_extracted', 0),
            'tasks_auto_approved': sprint_results.get('tasks_auto_approved', 0),
            'tasks_processed': sprint_results.get('tasks_processed', 0),
            'tasks_completed': sprint_results.get('tasks_completed', 0),
            'blockers_count': len(sprint_results.get('blockers_identified', [])),
            'human_contributions_count': len(sprint_results.get('human_contributions', [])),
            'ai_wishlist_count': len(sprint_results.get('ai_wishlist', [])),
            'human_wishlist_count': len(sprint_results.get('human_wishlist', [])),
            'report_path': str(output_path or (project_root / 'docs' / 'SPRINT_AUTOMATION_REPORT.md')),
            'blockers': sprint_results.get('blockers_identified', [])[:10],
            'human_contributions': sprint_results.get('human_contributions', [])[:10],
            'ai_wishlist': sprint_results.get('ai_wishlist', [])[:10],
            'human_wishlist': sprint_results.get('human_wishlist', [])[:10]
        }

        duration = time.time() - start_time
        log_automation_execution('sprint_automation', duration, True)

        return json.dumps(format_success_response(response_data), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution('sprint_automation', duration, False, e)

        error_response = format_error_response(e, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)


"""
MCP Tool Wrapper for Test Runner

Wraps TestRunner to expose as MCP tool.
"""

import json
import logging
import time
from pathlib import Path
from typing import Optional

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


def run_tests(
    test_path: Optional[str] = None,
    test_framework: str = "auto",
    verbose: bool = True,
    coverage: bool = False,
    output_path: Optional[str] = None
) -> str:
    """
    Execute test suites with flexible options.

    Args:
        test_path: Path to test file/directory (default: tests/)
        test_framework: pytest, unittest, ctest, or auto (default: auto)
        verbose: Show detailed output (default: true)
        coverage: Generate coverage report (default: false)
        output_path: Path for test results (default: test-results/)

    Returns:
        JSON string with test execution results
    """
    start_time = time.time()

    try:
        from project_management_automation.scripts.automate_run_tests import TestRunner
        from project_management_automation.utils import find_project_root
        
        project_root = find_project_root(Path(__file__).parent.parent.parent.parent)

        config = {
            'test_path': test_path or 'tests/',
            'test_framework': test_framework,
            'verbose': verbose,
            'coverage': coverage,
            'output_path': output_path or 'test-results/'
        }

        runner = TestRunner(config, project_root)
        results = runner.run()

        # Format response
        response_data = {
            'framework': results.get('results', {}).get('framework', 'unknown'),
            'tests_run': results.get('results', {}).get('tests_run', 0),
            'tests_passed': results.get('results', {}).get('tests_passed', 0),
            'tests_failed': results.get('results', {}).get('tests_failed', 0),
            'tests_skipped': results.get('results', {}).get('tests_skipped', 0),
            'duration': results.get('results', {}).get('duration', 0),
            'output_file': results.get('results', {}).get('output_file'),
            'coverage_file': results.get('results', {}).get('coverage_file'),
            'status': results.get('results', {}).get('status', 'unknown')
        }

        duration = time.time() - start_time
        log_automation_execution('run_tests', duration, True)

        return json.dumps(format_success_response(response_data), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution('run_tests', duration, False, e)

        error_response = format_error_response(e, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)


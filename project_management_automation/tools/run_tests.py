"""
MCP Tool Wrapper for Test Runner

Wraps TestRunner to expose as MCP tool.

Memory Integration:
- Saves test failures for debugging patterns
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def _save_test_run_memory(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save test run results as memory for debugging patterns."""
    try:
        from .session_memory import save_session_insight

        passed = response_data.get('tests_passed', 0)
        failed = response_data.get('tests_failed', 0)
        skipped = response_data.get('tests_skipped', 0)
        total = passed + failed + skipped

        # Only save if there were failures or it's a significant run
        if failed == 0 and total < 10:
            return {"success": True, "skipped": "no_failures_small_run"}

        content = f"""Test run completed.

## Results
- Total: {total}
- Passed: {passed} ✅
- Failed: {failed} {'❌' if failed > 0 else ''}
- Skipped: {skipped}
- Duration: {response_data.get('duration', 0):.2f}s

## Framework
{response_data.get('framework', 'unknown')}

## Output
{response_data.get('output_file', 'N/A')}
"""

        category = "debug" if failed > 0 else "insight"
        status = f"❌ {failed} failed" if failed > 0 else f"✅ {passed} passed"

        return save_session_insight(
            title=f"Tests: {status}",
            content=content,
            category=category,
            metadata={"type": "test_run", "passed": passed, "failed": failed}
        )
    except ImportError:
        logger.debug("Session memory not available for saving test run")
        return {"success": False, "error": "Memory system not available"}

# Import error handler
try:
    from ..error_handler import ErrorCode, format_error_response, format_success_response, log_automation_execution
except ImportError:
    import sys
    server_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(server_dir))
    try:
        from error_handler import ErrorCode, format_error_response, format_success_response, log_automation_execution
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

        project_root = find_project_root()

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

        # ═══ MEMORY INTEGRATION: Save test results ═══
        memory_result = _save_test_run_memory(response_data)
        if memory_result.get('success'):
            response_data['memory_saved'] = memory_result.get('memory_id')

        return json.dumps(format_success_response(response_data), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution('run_tests', duration, False, e)

        error_response = format_error_response(e, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)


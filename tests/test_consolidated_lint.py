"""
Unit Tests for Lint Consolidated Tool

Tests for lint action in consolidated.py.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import shared test helpers
from tests.test_helpers import parse_json_response


class TestLintTool:
    """Tests for lint consolidated tool."""

    @patch('project_management_automation.tools.linter.run_linter')
    def test_lint_run_action(self, mock_run):
        """Test run action routes correctly."""
        from project_management_automation.tools.consolidated import lint

        mock_run.return_value = json.dumps({
            "success": True,
            "data": {"issues": [], "total": 0}
        })

        result = lint(action="run", path="project_management_automation/")
        result_dict = parse_json_response(result)

        mock_run.assert_called_once()
        assert isinstance(result, str)

    @patch('project_management_automation.tools.problems_advisor.analyze_problems_tool')
    def test_lint_analyze_action(self, mock_analyze):
        """Test analyze action routes correctly."""
        from project_management_automation.tools.consolidated import lint

        mock_analyze.return_value = json.dumps({
            "success": True,
            "data": {"analysis": {}}
        })

        result = lint(action="analyze", problems_json='{"problems": []}')
        result_dict = parse_json_response(result)

        mock_analyze.assert_called_once()
        assert isinstance(result, str)

    def test_lint_invalid_action(self):
        """Test invalid action returns error."""
        from project_management_automation.tools.consolidated import lint

        result = lint(action="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error" or "Unknown lint action" in str(result_dict)


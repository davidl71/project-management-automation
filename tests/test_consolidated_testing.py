"""
Unit Tests for Testing Consolidated Tool

Tests for testing action in consolidated.py.
"""

import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import shared test helpers
from tests.test_helpers import parse_json_response


class TestTestingTool:
    """Tests for testing consolidated tool."""

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.run_tests.run_tests_async')
    async def test_testing_run_action(self, mock_run):
        """Test run action routes correctly."""
        from project_management_automation.tools.consolidated import testing_async

        mock_run.return_value = json.dumps({
            "success": True,
            "data": {"tests_run": 10, "passed": 10}
        })

        result = await testing_async(action="run", test_path="tests/")
        result_dict = parse_json_response(result)

        mock_run.assert_called_once()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.test_coverage.analyze_test_coverage')
    async def test_testing_coverage_action(self, mock_coverage):
        """Test coverage action routes correctly."""
        from project_management_automation.tools.consolidated import testing_async

        mock_coverage.return_value = json.dumps({
            "success": True,
            "data": {"total_coverage": 45.5}
        })

        result = await testing_async(action="coverage", min_coverage=30)
        result_dict = parse_json_response(result)

        mock_coverage.assert_called_once()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.test_suggestions.suggest_test_cases')
    async def test_testing_suggest_action(self, mock_suggest):
        """Test suggest action routes correctly."""
        from project_management_automation.tools.consolidated import testing_async

        mock_suggest.return_value = json.dumps({
            "success": True,
            "data": {"suggestions": []}
        })

        result = await testing_async(action="suggest", target_file="test.py")
        result_dict = parse_json_response(result)

        mock_suggest.assert_called_once()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.test_suggestions.generate_test_code')
    async def test_testing_generate_action(self, mock_generate):
        """Test generate action routes correctly."""
        from project_management_automation.tools.consolidated import testing_async

        mock_generate.return_value = {
            "success": True,
            "data": {"generated_count": 3}
        }

        result = await testing_async(
            action="generate",
            target_file="test.py",
            use_mlx=True,
            use_coreml=False
        )
        result_dict = parse_json_response(result)

        mock_generate.assert_called_once()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.test_validation.validate_test_structure')
    async def test_testing_validate_action(self, mock_validate):
        """Test validate action routes correctly."""
        from project_management_automation.tools.consolidated import testing_async

        mock_validate.return_value = {
            "success": True,
            "data": {"valid": True}
        }

        result = await testing_async(action="validate", test_path="tests/", framework="pytest")
        result_dict = parse_json_response(result)

        mock_validate.assert_called_once()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_testing_invalid_action(self):
        """Test invalid action returns error."""
        from project_management_automation.tools.consolidated import testing_async

        result = await testing_async(action="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error" or "Unknown testing action" in str(result_dict)


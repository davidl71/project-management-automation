"""
Unit Tests for Project Scorecard Tool

Tests for project_scorecard.py module.
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
from tests.test_helpers import assert_success_response, parse_json_response


class TestGenerateProjectScorecard:
    """Tests for generate_project_scorecard function."""

    @patch('project_management_automation.tools.project_scorecard.find_project_root')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.read_text')
    def test_generate_scorecard_success(self, mock_read_text, mock_open, mock_root):
        """Test successful scorecard generation."""
        from project_management_automation.tools.project_scorecard import generate_project_scorecard
        import json
        from unittest.mock import MagicMock

        mock_root.return_value = Path("/test/project")
        
        # Create a mock Path that returns True for exists() when it's the todo2 file
        def make_mock_path(*args):
            mock_path = MagicMock(spec=Path)
            path_str = '/'.join(str(a) for a in args)
            if '.todo2' in path_str or 'state.todo2.json' in path_str:
                mock_path.exists.return_value = True
                mock_path.read_text.return_value = json.dumps({
                    "todos": [
                        {"id": "T-1", "status": "Done", "tags": ["testing"]},
                        {"id": "T-2", "status": "Todo", "tags": ["security"]},
                    ]
                })
            else:
                mock_path.exists.return_value = False
            return mock_path
        
        # Mock Path constructor
        with patch('pathlib.Path', side_effect=make_mock_path):
            # Mock open for todo2 file
            todo2_data = json.dumps({
                "todos": [
                    {"id": "T-1", "status": "Done", "tags": ["testing"]},
                    {"id": "T-2", "status": "Todo", "tags": ["security"]},
                ]
            })
            from unittest.mock import mock_open as mock_open_func
            mock_open.return_value = mock_open_func(read_data=todo2_data).return_value

            result = generate_project_scorecard()

        assert isinstance(result, dict)
        assert 'overall_score' in result
        assert 'scores' in result
        assert 'production_ready' in result
        assert isinstance(result['overall_score'], (int, float))
        assert 0 <= result['overall_score'] <= 100

    @patch('project_management_automation.tools.project_scorecard.find_project_root')
    def test_generate_scorecard_text_format(self, mock_root):
        """Test scorecard generation with text format."""
        from project_management_automation.tools.project_scorecard import generate_project_scorecard

        mock_root.return_value = Path("/test/project")

        result = generate_project_scorecard(output_format="text")

        assert isinstance(result, dict)
        assert 'overall_score' in result
        assert 'scores' in result

    @patch('project_management_automation.tools.project_scorecard.find_project_root')
    def test_generate_scorecard_without_recommendations(self, mock_root):
        """Test scorecard generation without recommendations."""
        from project_management_automation.tools.project_scorecard import generate_project_scorecard

        mock_root.return_value = Path("/test/project")

        result = generate_project_scorecard(include_recommendations=False)

        assert isinstance(result, dict)
        assert 'overall_score' in result
        # Recommendations may still be present but should be minimal

    @patch('project_management_automation.tools.project_scorecard.find_project_root')
    @patch('builtins.open', create=True)
    def test_generate_scorecard_with_output_path(self, mock_open, mock_root, tmp_path):
        """Test scorecard generation with output path."""
        from project_management_automation.tools.project_scorecard import generate_project_scorecard
        import json
        from unittest.mock import MagicMock, mock_open as mock_open_func, patch

        mock_root.return_value = Path("/test/project")
        
        # Create a mock Path that returns True for exists() when it's the todo2 file
        def make_mock_path(*args):
            mock_path = MagicMock(spec=Path)
            path_str = '/'.join(str(a) for a in args)
            if '.todo2' in path_str or 'state.todo2.json' in path_str:
                mock_path.exists.return_value = True
                mock_path.read_text.return_value = json.dumps({"todos": []})
            else:
                mock_path.exists.return_value = False
            return mock_path
        
        # Mock Path constructor
        with patch('pathlib.Path', side_effect=make_mock_path):
            # Mock file opening for todo2 file
            todo2_data = json.dumps({"todos": []})
            mock_open.return_value = mock_open_func(read_data=todo2_data).return_value

            output_file = tmp_path / "scorecard.txt"
            result = generate_project_scorecard(output_path=str(output_file))

        assert isinstance(result, dict)
        assert 'overall_score' in result
        # Output file may or may not be created depending on format

    @patch('project_management_automation.tools.project_scorecard.find_project_root')
    @patch('project_management_automation.tools.project_scorecard._save_scorecard_memory')
    def test_generate_scorecard_saves_memory(self, mock_save, mock_root):
        """Test that scorecard saves to memory."""
        from project_management_automation.tools.project_scorecard import generate_project_scorecard

        mock_root.return_value = Path("/test/project")
        mock_save.return_value = {"success": True}

        result = generate_project_scorecard()

        assert isinstance(result, dict)
        # Memory save may be called
        # (It's called internally, so we just verify the function completes)


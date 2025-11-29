"""
Unit Tests for Linter Tool

Tests for linter.py module (13% coverage → target: 80%+).
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestLinterTool:
    """Tests for linter tool."""

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_ruff_success(self, mock_subprocess, mock_find_root):
        """Test successful ruff linter run."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        
        # Mock ruff output (JSON format)
        mock_output = json.dumps([
            {
                'code': 'E501',
                'message': 'Line too long',
                'location': {'row': 10, 'column': 80},
                'filename': 'test.py'
            }
        ])
        
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=mock_output,
            stderr=""
        )
        
        result_str = run_linter(linter="ruff", path="/test/project", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['linter'] == 'ruff'
        assert result['data']['total_issues'] == 1
        assert len(result['data']['problems']) == 1

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_with_fix(self, mock_subprocess, mock_find_root):
        """Test linter run with auto-fix enabled."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([]),
            stderr=""
        )
        
        result_str = run_linter(linter="ruff", fix=True, analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['fix_applied'] is True
        # Verify --fix flag was passed
        assert '--fix' in ' '.join(mock_subprocess.call_args[0][0])

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_with_select_ignore(self, mock_subprocess, mock_find_root):
        """Test linter run with select and ignore options."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([]),
            stderr=""
        )
        
        result_str = run_linter(
            linter="ruff",
            select="E,F",
            ignore="E501",
            analyze=False
        )
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Verify select and ignore flags were passed
        call_args = mock_subprocess.call_args[0][0]
        assert '--select' in call_args
        assert '--ignore' in call_args

    @patch('project_management_automation.utils.find_project_root')
    def test_run_linter_unknown_linter(self, mock_find_root):
        """Test linter run with unknown linter."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        
        result_str = run_linter(linter="unknown_linter", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'Unknown linter' in result['error']['message']

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_not_found(self, mock_subprocess, mock_find_root):
        """Test linter run when linter not installed."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.side_effect = FileNotFoundError("ruff: command not found")
        
        result_str = run_linter(linter="ruff", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'not found' in result['error']['message'].lower()

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_timeout(self, mock_subprocess, mock_find_root):
        """Test linter run timeout handling."""
        from project_management_automation.tools.linter import run_linter
        import subprocess

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.side_effect = subprocess.TimeoutExpired("ruff", 120)
        
        result_str = run_linter(linter="ruff", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'timeout' in result['error']['message'].lower()

    @patch('subprocess.run')
    def test_get_linter_status(self, mock_subprocess):
        """Test getting linter status."""
        from project_management_automation.tools.linter import get_linter_status

        # Mock ruff available
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout="ruff 0.1.0",
            stderr=""
        )
        
        result_str = get_linter_status()
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert 'linters' in result['data']
        assert 'recommended' in result['data']

    @patch('subprocess.run')
    def test_get_linter_status_not_available(self, mock_subprocess):
        """Test linter status when linters not available."""
        from project_management_automation.tools.linter import get_linter_status

        mock_subprocess.side_effect = FileNotFoundError()
        
        result_str = get_linter_status()
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Should still return status, just with available=False
        assert 'linters' in result['data']

    def test_parse_ruff_output(self):
        """Test parsing ruff JSON output."""
        from project_management_automation.tools.linter import _parse_ruff_output

        ruff_output = json.dumps([
            {
                'code': 'E501',
                'message': 'Line too long',
                'location': {'row': 10, 'column': 80},
                'filename': 'test.py'
            },
            {
                'code': 'W291',
                'message': 'Trailing whitespace',
                'location': {'row': 5, 'column': 10},
                'filename': 'test2.py'
            }
        ])
        
        problems = _parse_ruff_output(ruff_output)
        
        assert len(problems) == 2
        assert problems[0]['code'] == 'E501'
        assert problems[0]['severity'] == 'error'  # E prefix = error
        assert problems[1]['severity'] == 'warning'  # W prefix = warning

    def test_parse_ruff_output_empty(self):
        """Test parsing empty ruff output."""
        from project_management_automation.tools.linter import _parse_ruff_output

        problems = _parse_ruff_output("")
        assert problems == []

    def test_parse_ruff_output_invalid_json(self):
        """Test parsing invalid JSON gracefully."""
        from project_management_automation.tools.linter import _parse_ruff_output

        problems = _parse_ruff_output("invalid json")
        assert problems == []

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
        assert 'timed out' in result['error']['message'].lower()

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

    def test_parse_ruff_output_text_fallback(self):
        """Test parsing ruff text output as fallback."""
        from project_management_automation.tools.linter import _parse_ruff_output

        text_output = "test.py:10:80: E501 Line too long"
        problems = _parse_ruff_output(text_output)
        
        assert len(problems) == 1
        assert problems[0]['file'] == 'test.py'
        assert problems[0]['line'] == 10
        assert problems[0]['severity'] == 'warning'

    def test_parse_ruff_output_with_fix_available(self):
        """Test parsing ruff output with fix information."""
        from project_management_automation.tools.linter import _parse_ruff_output

        ruff_output = json.dumps([
            {
                'code': 'F401',
                'message': 'Unused import',
                'location': {'row': 5, 'column': 1},
                'filename': 'test.py',
                'fix': {'edits': []}
            }
        ])
        
        problems = _parse_ruff_output(ruff_output)
        assert problems[0]['fix_available'] is True

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_flake8(self, mock_subprocess, mock_find_root):
        """Test flake8 linter run."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([]),
            stderr=""
        )
        
        result_str = run_linter(linter="flake8", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['linter'] == 'flake8'
        # Verify flake8 command was used
        call_args = mock_subprocess.call_args[0][0]
        assert 'flake8' in call_args

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    @patch('project_management_automation.tools.linter._save_linter_memory')
    def test_run_linter_saves_memory(self, mock_save_memory, mock_subprocess, mock_find_root):
        """Test that linter results are saved to memory."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([
                {'code': 'E501', 'message': 'Line too long', 'location': {'row': 1, 'column': 80}, 'filename': 'test.py'}
            ]),
            stderr=""
        )
        mock_save_memory.return_value = {'success': True, 'memory_id': 'mem-123'}
        
        result_str = run_linter(linter="ruff", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data'].get('memory_saved') == 'mem-123'
        mock_save_memory.assert_called_once()

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    @patch('project_management_automation.tools.problems_advisor.analyze_problems_tool')
    def test_run_linter_with_analyze(self, mock_analyze, mock_subprocess, mock_find_root):
        """Test linter run with analyze_problems integration."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([
                {'code': 'E501', 'message': 'Line too long', 'location': {'row': 1, 'column': 80}, 'filename': 'test.py'}
            ]),
            stderr=""
        )
        mock_analyze.return_value = json.dumps({
            'success': True,
            'data': {'categories': {'error': 1}}
        })
        
        result_str = run_linter(linter="ruff", analyze=True)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert 'analysis' in result['data']
        mock_analyze.assert_called_once()

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_categorizes_by_severity(self, mock_subprocess, mock_find_root):
        """Test that issues are categorized by severity."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([
                {'code': 'E501', 'message': 'Error', 'location': {'row': 1, 'column': 1}, 'filename': 'test.py'},
                {'code': 'W291', 'message': 'Warning', 'location': {'row': 2, 'column': 1}, 'filename': 'test.py'},
                {'code': 'F401', 'message': 'Fatal', 'location': {'row': 3, 'column': 1}, 'filename': 'test.py'},
            ]),
            stderr=""
        )
        
        result_str = run_linter(linter="ruff", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        by_severity = result['data']['by_severity']
        assert by_severity.get('error', 0) >= 1
        assert by_severity.get('warning', 0) >= 1

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_categorizes_by_code(self, mock_subprocess, mock_find_root):
        """Test that issues are categorized by code prefix."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([
                {'code': 'E501', 'message': 'Error', 'location': {'row': 1, 'column': 1}, 'filename': 'test.py'},
                {'code': 'W291', 'message': 'Warning', 'location': {'row': 2, 'column': 1}, 'filename': 'test.py'},
            ]),
            stderr=""
        )
        
        result_str = run_linter(linter="ruff", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        by_category = result['data']['by_category']
        assert by_category.get('error', 0) >= 1
        assert by_category.get('warning', 0) >= 1

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_counts_files(self, mock_subprocess, mock_find_root, tmp_path):
        """Test that files are counted correctly."""
        from project_management_automation.tools.linter import run_linter

        # Create a test directory with Python files
        test_dir = tmp_path / "test_project"
        test_dir.mkdir()
        (test_dir / "test1.py").write_text("# test")
        (test_dir / "test2.py").write_text("# test")
        
        mock_find_root.return_value = test_dir
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([]),
            stderr=""
        )
        
        result_str = run_linter(linter="ruff", path=str(test_dir), analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['files_checked'] >= 2

    @patch('subprocess.run')
    def test_get_linter_status_multiple_linters(self, mock_subprocess):
        """Test getting status for multiple linters."""
        from project_management_automation.tools.linter import get_linter_status

        def side_effect(cmd, **kwargs):
            if cmd[0] == 'ruff':
                return Mock(returncode=0, stdout="ruff 0.1.0", stderr="")
            elif cmd[0] == 'flake8':
                return Mock(returncode=0, stdout="flake8 6.0.0", stderr="")
            else:
                raise FileNotFoundError()
        
        mock_subprocess.side_effect = side_effect
        
        result_str = get_linter_status()
        result = json.loads(result_str)
        
        assert result['success'] is True
        linters = result['data']['linters']
        assert linters.get('ruff', {}).get('available') is True
        assert linters.get('flake8', {}).get('available') is True
        assert result['data']['recommended'] == 'ruff'

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_limits_problems(self, mock_subprocess, mock_find_root):
        """Test that problems list is limited to 50."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        # Create 60 problems
        many_problems = [
            {'code': f'E{i}', 'message': f'Error {i}', 'location': {'row': i, 'column': 1}, 'filename': 'test.py'}
            for i in range(60)
        ]
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps(many_problems),
            stderr=""
        )
        
        result_str = run_linter(linter="ruff", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['total_issues'] == 60
        assert len(result['data']['problems']) == 50  # Limited to 50
        # But problems_json should have all 60
        problems_json = json.loads(result['data']['problems_json'])
        assert len(problems_json) == 60

    @patch('project_management_automation.utils.find_project_root')
    @patch('subprocess.run')
    def test_run_linter_handles_exception(self, mock_subprocess, mock_find_root):
        """Test that exceptions are handled gracefully."""
        from project_management_automation.tools.linter import run_linter

        mock_find_root.return_value = Path("/test/project")
        mock_subprocess.side_effect = Exception("Unexpected error")
        
        result_str = run_linter(linter="ruff", analyze=False)
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

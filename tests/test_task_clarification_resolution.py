"""
Unit Tests for Task Clarification Resolution Tool

Tests for task_clarification_resolution.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import sys
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestTaskClarificationResolutionTool:
    """Tests for task clarification resolution tool."""

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    @patch('project_management_automation.tools.task_clarification_resolution.subprocess.run')
    def test_resolve_task_clarification_success(self, mock_subprocess, mock_exists, mock_find_root):
        """Test successful task clarification resolution."""
        from project_management_automation.tools.task_clarification_resolution import resolve_task_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout="✅ Updated task T-1",
            stderr=""
        )
        
        result = resolve_task_clarification(
            task_id="T-1",
            clarification="What approach?",
            decision="Use approach A"
        )
        
        assert result['status'] == 'success'
        assert result['task_id'] == 'T-1'
        assert result['moved_to_todo'] is True

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    def test_resolve_task_clarification_script_not_found(self, mock_exists, mock_find_root):
        """Test when script doesn't exist."""
        from project_management_automation.tools.task_clarification_resolution import resolve_task_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = False
        
        result = resolve_task_clarification(
            task_id="T-1",
            clarification="What approach?",
            decision="Use approach A"
        )
        
        assert result['status'] == 'error'
        assert 'Script not found' in result['error']

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    @patch('project_management_automation.tools.task_clarification_resolution.subprocess.run')
    def test_resolve_task_clarification_dry_run(self, mock_subprocess, mock_exists, mock_find_root):
        """Test dry run mode."""
        from project_management_automation.tools.task_clarification_resolution import resolve_task_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(returncode=0, stdout="Preview: Would update", stderr="")
        
        result = resolve_task_clarification(
            task_id="T-1",
            clarification="What approach?",
            decision="Use approach A",
            dry_run=True
        )
        
        assert result['dry_run'] is True
        assert result['moved_to_todo'] is False  # Dry run doesn't move

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    @patch('project_management_automation.tools.task_clarification_resolution.subprocess.run')
    def test_resolve_task_clarification_no_move(self, mock_subprocess, mock_exists, mock_find_root):
        """Test without moving to Todo."""
        from project_management_automation.tools.task_clarification_resolution import resolve_task_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(returncode=0, stdout="Updated", stderr="")
        
        result = resolve_task_clarification(
            task_id="T-1",
            clarification="What approach?",
            decision="Use approach A",
            move_to_todo=False
        )
        
        assert result['status'] == 'success'
        # Should not move even if successful
        assert result['moved_to_todo'] is False

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    @patch('project_management_automation.tools.task_clarification_resolution.subprocess.run')
    def test_resolve_task_clarification_script_error(self, mock_subprocess, mock_exists, mock_find_root):
        """Test when script returns error."""
        from project_management_automation.tools.task_clarification_resolution import resolve_task_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Task not found"
        )
        
        result = resolve_task_clarification(
            task_id="T-999",
            clarification="What approach?",
            decision="Use approach A"
        )
        
        assert result['status'] == 'error'
        assert 'error' in result

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    @patch('project_management_automation.tools.task_clarification_resolution.subprocess.run')
    def test_resolve_task_clarification_timeout(self, mock_subprocess, mock_exists, mock_find_root):
        """Test timeout handling."""
        from project_management_automation.tools.task_clarification_resolution import resolve_task_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.side_effect = subprocess.TimeoutExpired("cmd", 30)
        
        result = resolve_task_clarification(
            task_id="T-1",
            clarification="What approach?",
            decision="Use approach A"
        )
        
        assert result['status'] == 'error'
        assert 'timed out' in result['error'].lower()

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    @patch('project_management_automation.tools.task_clarification_resolution.subprocess.run')
    @patch('project_management_automation.tools.task_clarification_resolution.tempfile.NamedTemporaryFile')
    def test_resolve_multiple_clarifications_success(self, mock_tempfile, mock_subprocess, mock_exists, mock_find_root):
        """Test resolving multiple clarifications."""
        from project_management_automation.tools.task_clarification_resolution import resolve_multiple_clarifications

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        # Mock temp file
        mock_file = Mock()
        mock_file.name = "/tmp/decisions.json"
        mock_tempfile.return_value.__enter__.return_value = mock_file
        
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout="✅ Updated task T-1\n✅ Updated task T-2",
            stderr=""
        )
        
        decisions = {
            "T-1": {"clarification": "Q1", "decision": "A1"},
            "T-2": {"clarification": "Q2", "decision": "A2"}
        }
        
        result = resolve_multiple_clarifications(decisions)
        
        assert result['status'] == 'success'
        assert result['tasks_processed'] == 2
        assert result['tasks_updated'] == 2

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    def test_list_tasks_awaiting_clarification_success(self, mock_exists, mock_find_root):
        """Test listing tasks awaiting clarification."""
        from project_management_automation.tools.task_clarification_resolution import list_tasks_awaiting_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        # Mock state file
        state_data = {
            'todos': [
                {
                    'id': 'T-1',
                    'name': 'Task 1',
                    'status': 'Review',
                    'priority': 'high',
                    'long_description': 'Clarification Required: **What approach?**'
                },
                {
                    'id': 'T-2',
                    'name': 'Task 2',
                    'status': 'Todo',
                    'priority': 'medium',
                    'long_description': 'No clarification needed'
                }
            ]
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(state_data))):
            result = list_tasks_awaiting_clarification()
        
        assert result['status'] == 'success'
        assert result['total_tasks'] == 1
        assert len(result['tasks']) == 1
        assert result['tasks'][0]['task_id'] == 'T-1'

    @patch('project_management_automation.tools.task_clarification_resolution.find_project_root')
    @patch('project_management_automation.tools.task_clarification_resolution.Path.exists')
    def test_list_tasks_awaiting_clarification_no_file(self, mock_exists, mock_find_root):
        """Test when state file doesn't exist."""
        from project_management_automation.tools.task_clarification_resolution import list_tasks_awaiting_clarification

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = False
        
        result = list_tasks_awaiting_clarification()
        
        assert result['status'] == 'error'
        assert 'State file not found' in result['error']

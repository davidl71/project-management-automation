"""
Unit Tests for Batch Task Approval Tool

Tests for batch_task_approval.py module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestBatchTaskApprovalTool:
    """Tests for batch task approval tool."""

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    @patch('subprocess.run')
    def test_batch_approve_tasks_success(self, mock_subprocess, mock_exists, mock_find_root):
        """Test successful batch task approval."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout="Approved 3 tasks\n• TASK-1: Task 1\n• TASK-2: Task 2\n• TASK-3: Task 3",
            stderr=""
        )
        
        result = batch_approve_tasks(status="Review", new_status="Todo", dry_run=False)
        
        assert result['success'] is True
        assert result['approved_count'] == 3
        assert len(result['task_ids']) == 3
        assert result['status_from'] == 'Review'
        assert result['status_to'] == 'Todo'
        assert result['dry_run'] is False

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    @patch('subprocess.run')
    def test_batch_approve_tasks_dry_run(self, mock_subprocess, mock_exists, mock_find_root):
        """Test dry run mode."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout="• TASK-1: Task 1\n• TASK-2: Task 2",
            stderr=""
        )
        
        result = batch_approve_tasks(dry_run=True)
        
        assert result['success'] is True
        assert result['dry_run'] is True
        assert result['approved_count'] == 2

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    def test_batch_approve_tasks_script_not_found(self, mock_exists, mock_find_root):
        """Test when batch script doesn't exist."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = False
        
        result = batch_approve_tasks()
        
        assert result['success'] is False
        assert 'not found' in result['error'].lower()
        assert result['approved_count'] == 0

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    @patch('subprocess.run')
    def test_batch_approve_tasks_with_filter_tag(self, mock_subprocess, mock_exists, mock_find_root):
        """Test with filter tag."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(returncode=0, stdout="Approved 1 tasks", stderr="")
        
        result = batch_approve_tasks(filter_tag="research", dry_run=False)
        
        assert result['success'] is True
        # Verify --filter-tag was passed
        call_args = mock_subprocess.call_args[0][0]
        assert '--filter-tag' in call_args
        assert 'research' in call_args

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    @patch('subprocess.run')
    def test_batch_approve_tasks_with_task_ids(self, mock_subprocess, mock_exists, mock_find_root):
        """Test with specific task IDs."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(returncode=0, stdout="Approved 2 tasks", stderr="")
        
        result = batch_approve_tasks(task_ids=['TASK-1', 'TASK-2'], dry_run=False)
        
        assert result['success'] is True
        # Verify --task-ids was passed
        call_args = mock_subprocess.call_args[0][0]
        assert '--task-ids' in call_args

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    @patch('subprocess.run')
    def test_batch_approve_tasks_script_failure(self, mock_subprocess, mock_exists, mock_find_root):
        """Test when script execution fails."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: Invalid status"
        )
        
        result = batch_approve_tasks()
        
        assert result['success'] is False
        assert 'failed' in result['error'].lower()
        assert result['approved_count'] == 0

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    @patch('subprocess.run')
    def test_batch_approve_tasks_timeout(self, mock_subprocess, mock_exists, mock_find_root):
        """Test timeout handling."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.side_effect = subprocess.TimeoutExpired("script", 30)
        
        result = batch_approve_tasks()
        
        assert result['success'] is False
        assert 'timed out' in result['error'].lower()
        assert result['approved_count'] == 0

    @patch('project_management_automation.tools.batch_task_approval.find_project_root')
    @patch('pathlib.Path.exists')
    @patch('subprocess.run')
    def test_batch_approve_tasks_without_clarification_none(self, mock_subprocess, mock_exists, mock_find_root):
        """Test with clarification_none=False."""
        from project_management_automation.tools.batch_task_approval import batch_approve_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_subprocess.return_value = Mock(returncode=0, stdout="Approved 1 tasks", stderr="")
        
        result = batch_approve_tasks(clarification_none=False, dry_run=False)
        
        assert result['success'] is True
        # Verify --clarification-none was NOT passed
        call_args = mock_subprocess.call_args[0][0]
        assert '--clarification-none' not in call_args

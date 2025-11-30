"""
Unit Tests for Todo Sync Tool

Tests for todo_sync.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestTodoSyncTool:
    """Tests for todo sync tool."""

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_todo_sync.TodoSyncAutomation')
    def test_sync_todo_tasks_success(self, mock_sync_class, mock_find_root):
        """Test successful todo sync."""
        from project_management_automation.tools.todo_sync import sync_todo_tasks

        mock_find_root.return_value = Path("/test/project")
        
        # Mock sync automation instance
        mock_sync = Mock()
        mock_sync.run.return_value = {
            'results': {
                'matches': [{'id': '1'}, {'id': '2'}],
                'conflicts': [{'id': '3'}],
                'new_shared_todos': [{'id': '4'}],
                'new_todo2_tasks': [{'id': '5'}, {'id': '6'}],
                'updates': [{'id': '7'}]
            },
            'status': 'success'
        }
        mock_sync_class.return_value = mock_sync
        
        result_str = sync_todo_tasks(dry_run=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['dry_run'] is False
        assert result['data']['matches_found'] == 2
        assert result['data']['conflicts_detected'] == 1
        assert result['data']['new_shared_todos'] == 1
        assert result['data']['new_todo2_tasks'] == 2
        assert result['data']['updates_performed'] == 1

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_todo_sync.TodoSyncAutomation')
    def test_sync_todo_tasks_dry_run(self, mock_sync_class, mock_find_root):
        """Test dry run mode."""
        from project_management_automation.tools.todo_sync import sync_todo_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_sync = Mock()
        mock_sync.run.return_value = {
            'results': {
                'matches': [],
                'conflicts': [],
                'new_shared_todos': [],
                'new_todo2_tasks': [],
                'updates': []
            },
            'status': 'success'
        }
        mock_sync_class.return_value = mock_sync
        
        result_str = sync_todo_tasks(dry_run=True)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['dry_run'] is True

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_todo_sync.TodoSyncAutomation')
    def test_sync_todo_tasks_custom_output_path(self, mock_sync_class, mock_find_root):
        """Test with custom output path."""
        from project_management_automation.tools.todo_sync import sync_todo_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_sync = Mock()
        mock_sync.run.return_value = {
            'results': {
                'matches': [],
                'conflicts': [],
                'new_shared_todos': [],
                'new_todo2_tasks': [],
                'updates': []
            },
            'status': 'success'
        }
        mock_sync_class.return_value = mock_sync
        
        result_str = sync_todo_tasks(output_path="/custom/path/sync.md")
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert '/custom/path/sync.md' in result['data']['report_path']

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_todo_sync.TodoSyncAutomation')
    def test_sync_todo_tasks_error(self, mock_sync_class, mock_find_root):
        """Test error handling."""
        from project_management_automation.tools.todo_sync import sync_todo_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_sync = Mock()
        mock_sync.run.side_effect = Exception("Sync failed")
        mock_sync_class.return_value = mock_sync
        
        result_str = sync_todo_tasks()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_todo_sync.TodoSyncAutomation')
    def test_sync_todo_tasks_empty_results(self, mock_sync_class, mock_find_root):
        """Test with empty sync results."""
        from project_management_automation.tools.todo_sync import sync_todo_tasks

        mock_find_root.return_value = Path("/test/project")
        mock_sync = Mock()
        mock_sync.run.return_value = {
            'results': {
                'matches': [],
                'conflicts': [],
                'new_shared_todos': [],
                'new_todo2_tasks': [],
                'updates': []
            },
            'status': 'success'
        }
        mock_sync_class.return_value = mock_sync
        
        result_str = sync_todo_tasks()
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['matches_found'] == 0
        assert result['data']['conflicts_detected'] == 0

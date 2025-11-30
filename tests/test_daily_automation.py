"""
Unit Tests for Daily Automation Tool

Tests for daily_automation.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestDailyAutomationTool:
    """Tests for daily automation tool."""

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_daily.DailyAutomation')
    def test_run_daily_automation_success(self, mock_automation_class, mock_find_root):
        """Test successful daily automation run."""
        from project_management_automation.tools.daily_automation import run_daily_automation

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'status': 'success',
            'results': {
                'summary': {
                    'success_rate': 100.0,
                    'duration_seconds': 5.2
                },
                'tasks_run': [
                    {'task_id': 'docs_health', 'task_name': 'Documentation Health', 'status': 'success', 'duration_seconds': 2.1}
                ],
                'tasks_succeeded': ['docs_health'],
                'tasks_failed': []
            }
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = run_daily_automation()
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['tasks_run'] == 1
        assert result['data']['tasks_succeeded'] == 1
        assert result['data']['success_rate'] == 100.0

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_daily.DailyAutomation')
    def test_run_daily_automation_with_custom_tasks(self, mock_automation_class, mock_find_root):
        """Test with custom task list."""
        from project_management_automation.tools.daily_automation import run_daily_automation

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'status': 'success',
            'results': {
                'summary': {'success_rate': 100.0, 'duration_seconds': 3.0},
                'tasks_run': [],
                'tasks_succeeded': [],
                'tasks_failed': []
            }
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = run_daily_automation(tasks=['docs_health', 'todo2_alignment'])
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Verify config was passed correctly
        call_args = mock_automation_class.call_args[0]
        assert 'docs_health' in call_args[0]['tasks']

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_daily.DailyAutomation')
    def test_run_daily_automation_dry_run(self, mock_automation_class, mock_find_root):
        """Test dry run mode."""
        from project_management_automation.tools.daily_automation import run_daily_automation

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'status': 'success',
            'results': {
                'summary': {'success_rate': 0.0, 'duration_seconds': 0.0},
                'tasks_run': [],
                'tasks_succeeded': [],
                'tasks_failed': []
            }
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = run_daily_automation(dry_run=True)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['dry_run'] is True

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_daily.DailyAutomation')
    def test_run_daily_automation_with_slow_tasks(self, mock_automation_class, mock_find_root):
        """Test including slow tasks."""
        from project_management_automation.tools.daily_automation import run_daily_automation

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'status': 'success',
            'results': {
                'summary': {'success_rate': 100.0, 'duration_seconds': 10.0},
                'tasks_run': [],
                'tasks_succeeded': [],
                'tasks_failed': []
            }
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = run_daily_automation(include_slow=True)
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Verify include_slow was passed
        call_args = mock_automation_class.call_args[0]
        assert call_args[0]['include_slow'] is True

    @patch('project_management_automation.utils.find_project_root')
    def test_run_daily_automation_project_root_error(self, mock_find_root):
        """Test error handling when project root not found."""
        from project_management_automation.tools.daily_automation import run_daily_automation

        mock_find_root.side_effect = Exception("Project root error")
        
        result_str = run_daily_automation()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_daily.DailyAutomation')
    def test_run_daily_automation_automation_error(self, mock_automation_class, mock_find_root):
        """Test error handling when automation fails."""
        from project_management_automation.tools.daily_automation import run_daily_automation

        mock_find_root.return_value = Path("/test/project")
        mock_automation_class.side_effect = Exception("Automation error")
        
        result_str = run_daily_automation()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_daily.DailyAutomation')
    def test_run_daily_automation_custom_output_path(self, mock_automation_class, mock_find_root):
        """Test with custom output path."""
        from project_management_automation.tools.daily_automation import run_daily_automation

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'status': 'success',
            'results': {
                'summary': {'success_rate': 100.0, 'duration_seconds': 2.0},
                'tasks_run': [],
                'tasks_succeeded': [],
                'tasks_failed': []
            }
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = run_daily_automation(output_path="/custom/report.md")
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert '/custom/report.md' in result['data']['report_path']

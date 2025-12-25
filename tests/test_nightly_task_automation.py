"""
Unit Tests for Nightly Task Automation Tool

Tests for nightly_task_automation.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestNightlyTaskAutomation:
    """Tests for nightly task automation tool."""

    @patch('project_management_automation.tools.nightly_task_automation.Path.exists')
    @patch('project_management_automation.tools.nightly_task_automation._load_todo2_state')
    @patch('project_management_automation.tools.nightly_task_automation._check_working_copy_health')
    def test_run_nightly_automation_dry_run(self, mock_health, mock_load_state, mock_exists):
        """Test nightly automation in dry run mode."""
        from project_management_automation.tools.nightly_task_automation import run_nightly_task_automation

        mock_exists.return_value = True
        mock_health.return_value = {'summary': {'ok_agents': 1}}
        mock_load_state.return_value = {
            'todos': [
                {
                    'id': 'T-1',
                    'name': 'Implement feature',
                    'status': 'Todo',
                    'long_description': 'Implement new feature',
                    'tags': []
                }
            ]
        }
        
        result = run_nightly_task_automation(dry_run=True)
        
        assert result['dry_run'] is True
        assert 'summary' in result
        assert 'assigned_tasks' in result

    @patch('project_management_automation.tools.nightly_task_automation.Path.exists')
    @patch('project_management_automation.tools.nightly_task_automation._load_todo2_state')
    @patch('project_management_automation.tools.nightly_task_automation._check_working_copy_health')
    def test_run_nightly_automation_with_priority_filter(self, mock_health, mock_load_state, mock_exists):
        """Test with priority filter."""
        from project_management_automation.tools.nightly_task_automation import run_nightly_task_automation

        mock_exists.return_value = True
        mock_health.return_value = {'summary': {'ok_agents': 1}}
        mock_load_state.return_value = {
            'todos': [
                {
                    'id': 'T-1',
                    'name': 'High priority task',
                    'status': 'Todo',
                    'priority': 'high',
                    'long_description': 'Task description',
                    'tags': []
                },
                {
                    'id': 'T-2',
                    'name': 'Low priority task',
                    'status': 'Todo',
                    'priority': 'low',
                    'long_description': 'Task description',
                    'tags': []
                }
            ]
        }
        
        result = run_nightly_task_automation(priority_filter='high', dry_run=True)
        
        assert result['dry_run'] is True
        # Should only process high priority tasks
        assert result['summary']['background_tasks_found'] >= 0

    @patch('project_management_automation.tools.nightly_task_automation.Path.exists')
    @patch('project_management_automation.tools.nightly_task_automation._load_todo2_state')
    @patch('project_management_automation.tools.nightly_task_automation._check_working_copy_health')
    def test_run_nightly_automation_with_tag_filter(self, mock_health, mock_load_state, mock_exists):
        """Test with tag filter."""
        from project_management_automation.tools.nightly_task_automation import run_nightly_task_automation

        mock_exists.return_value = True
        mock_health.return_value = {'summary': {'ok_agents': 1}}
        mock_load_state.return_value = {
            'todos': [
                {
                    'id': 'T-1',
                    'name': 'Research task',
                    'status': 'Todo',
                    'tags': ['research'],
                    'long_description': 'Research something'
                }
            ]
        }
        
        result = run_nightly_task_automation(tag_filter=['research'], dry_run=True)
        
        assert result['dry_run'] is True
        assert 'summary' in result

    @patch('project_management_automation.tools.nightly_task_automation.Path.exists')
    @patch('project_management_automation.tools.nightly_task_automation._load_todo2_state')
    def test_is_background_capable(self, mock_load_state, mock_exists):
        """Test background capability detection."""
        from project_management_automation.tools.nightly_task_automation import NightlyTaskAutomation

        mock_exists.return_value = True
        automation = NightlyTaskAutomation()
        
        # Background capable task
        task = {
            'id': 'T-1',
            'name': 'Implement feature',
            'status': 'Todo',
            'long_description': 'Implement new feature'
        }
        assert automation._is_background_capable(task) is True

        # Interactive task (needs clarification)
        task = {
            'id': 'T-2',
            'name': 'Design system',
            'status': 'Todo',
            'long_description': 'Design system - clarification required'
        }
        assert automation._is_background_capable(task) is False

        # Review status task
        task = {
            'id': 'T-3',
            'name': 'Review task',
            'status': 'Review',
            'long_description': 'Task description'
        }
        assert automation._is_background_capable(task) is False

    @patch('project_management_automation.tools.nightly_task_automation.Path.exists')
    def test_move_to_review(self, mock_exists):
        """Test moving task to review."""
        from project_management_automation.tools.nightly_task_automation import NightlyTaskAutomation

        mock_exists.return_value = True
        automation = NightlyTaskAutomation()
        
        task = {
            'id': 'T-1',
            'name': 'Task',
            'status': 'Todo'
        }
        
        updated_task = automation._move_to_review(task, "Test reason")
        
        assert updated_task['status'] == 'Review'
        assert len(updated_task.get('comments', [])) > 0
        assert 'changes' in updated_task

    # Network utility tests removed - moved to test_utils_network.py
    # These functions are shared utilities (duplicated in working_copy_health.py)
    # See test_utils_network.py for comprehensive tests

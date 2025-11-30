"""
Unit Tests for External Tool Hints Tool

Tests for external_tool_hints.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestExternalToolHintsTool:
    """Tests for external tool hints tool."""

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_external_tool_hints.ExternalToolHintsAutomation')
    def test_add_external_tool_hints_success(self, mock_automation_class, mock_find_root):
        """Test successful external tool hints addition."""
        from project_management_automation.tools.external_tool_hints import add_external_tool_hints

        mock_find_root.return_value = Path("/test/project")
        
        # Mock automation instance
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'results': {
                'files_scanned': 10,
                'files_modified': 5,
                'files_skipped': 2,
                'hints_added': ['file1.md', 'file2.md'],
                'hints_skipped': ['file3.md']
            },
            'status': 'success'
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = add_external_tool_hints(dry_run=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['files_scanned'] == 10
        assert result['data']['files_modified'] == 5
        assert result['data']['files_skipped'] == 2
        assert result['data']['hints_added_count'] == 2
        assert result['data']['hints_skipped_count'] == 1
        assert result['data']['dry_run'] is False

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_external_tool_hints.ExternalToolHintsAutomation')
    def test_add_external_tool_hints_dry_run(self, mock_automation_class, mock_find_root):
        """Test dry run mode."""
        from project_management_automation.tools.external_tool_hints import add_external_tool_hints

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'results': {
                'files_scanned': 5,
                'files_modified': 0,
                'files_skipped': 0,
                'hints_added': [],
                'hints_skipped': []
            },
            'status': 'success'
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = add_external_tool_hints(dry_run=True)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['dry_run'] is True
        assert result['data']['files_modified'] == 0

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_external_tool_hints.ExternalToolHintsAutomation')
    def test_add_external_tool_hints_custom_output_path(self, mock_automation_class, mock_find_root):
        """Test with custom output path."""
        from project_management_automation.tools.external_tool_hints import add_external_tool_hints

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'results': {
                'files_scanned': 0,
                'files_modified': 0,
                'files_skipped': 0,
                'hints_added': [],
                'hints_skipped': []
            },
            'status': 'success'
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = add_external_tool_hints(output_path="/custom/path/report.md")
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert '/custom/path/report.md' in result['data']['report_path']

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_external_tool_hints.ExternalToolHintsAutomation')
    def test_add_external_tool_hints_custom_min_file_size(self, mock_automation_class, mock_find_root):
        """Test with custom min_file_size."""
        from project_management_automation.tools.external_tool_hints import add_external_tool_hints

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.return_value = {
            'results': {
                'files_scanned': 0,
                'files_modified': 0,
                'files_skipped': 0,
                'hints_added': [],
                'hints_skipped': []
            },
            'status': 'success'
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = add_external_tool_hints(min_file_size=100)
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Verify config was passed with min_file_size
        call_args = mock_automation_class.call_args
        assert call_args[0][0]['min_file_size'] == 100

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_external_tool_hints.ExternalToolHintsAutomation')
    def test_add_external_tool_hints_error(self, mock_automation_class, mock_find_root):
        """Test error handling."""
        from project_management_automation.tools.external_tool_hints import add_external_tool_hints

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        mock_automation.run.side_effect = Exception("Automation failed")
        mock_automation_class.return_value = mock_automation
        
        result_str = add_external_tool_hints()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.scripts.automate_external_tool_hints.ExternalToolHintsAutomation')
    def test_add_external_tool_hints_hints_limit(self, mock_automation_class, mock_find_root):
        """Test that hints_added is limited to 10."""
        from project_management_automation.tools.external_tool_hints import add_external_tool_hints

        mock_find_root.return_value = Path("/test/project")
        mock_automation = Mock()
        # Create 15 hints
        hints_added = [f'file{i}.md' for i in range(15)]
        mock_automation.run.return_value = {
            'results': {
                'files_scanned': 15,
                'files_modified': 15,
                'files_skipped': 0,
                'hints_added': hints_added,
                'hints_skipped': []
            },
            'status': 'success'
        }
        mock_automation_class.return_value = mock_automation
        
        result_str = add_external_tool_hints()
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert len(result['data']['hints_added']) == 10  # Limited to 10

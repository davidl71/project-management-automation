"""
Unit Tests for Pattern Triggers Tool

Tests for pattern_triggers.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestPatternTriggersTool:
    """Tests for pattern triggers tool."""

    @patch('project_management_automation.tools.pattern_triggers.find_project_root')
    @patch('project_management_automation.tools.pattern_triggers.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_setup_pattern_triggers_default(self, mock_file, mock_exists, mock_find_root):
        """Test setup with default patterns."""
        from project_management_automation.tools.pattern_triggers import setup_pattern_triggers

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        result_str = setup_pattern_triggers()
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert result['dry_run'] is False
        assert len(result['patterns_configured']) > 0

    @patch('project_management_automation.tools.pattern_triggers.find_project_root')
    def test_setup_pattern_triggers_dry_run(self, mock_find_root):
        """Test dry run mode."""
        from project_management_automation.tools.pattern_triggers import setup_pattern_triggers

        mock_find_root.return_value = Path("/test/project")
        
        result_str = setup_pattern_triggers(dry_run=True)
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert result['dry_run'] is True
        assert len(result['patterns_configured']) > 0

    @patch('project_management_automation.tools.pattern_triggers.find_project_root')
    @patch('project_management_automation.tools.pattern_triggers.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_setup_pattern_triggers_custom_patterns(self, mock_file, mock_exists, mock_find_root):
        """Test with custom patterns."""
        from project_management_automation.tools.pattern_triggers import setup_pattern_triggers

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        custom_patterns = {
            "file_patterns": {
                "*.py": {
                    "on_change": "run_linter_tool"
                }
            }
        }
        
        result_str = setup_pattern_triggers(patterns=custom_patterns)
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert len(result['patterns_configured']) > 0

    @patch('project_management_automation.tools.pattern_triggers.find_project_root')
    @patch('project_management_automation.tools.pattern_triggers.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_setup_pattern_triggers_from_config_file(self, mock_file, mock_exists, mock_find_root):
        """Test loading patterns from config file."""
        from project_management_automation.tools.pattern_triggers import setup_pattern_triggers

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        config_data = {
            "file_patterns": {
                "*.md": {"on_change": "check_docs"}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
            result_str = setup_pattern_triggers(config_path="/custom/config.json")
            result = json.loads(result_str)
        
        assert result['status'] == 'success'

    @patch('project_management_automation.tools.pattern_triggers.find_project_root')
    @patch('project_management_automation.tools.pattern_triggers.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_setup_pattern_triggers_write_error(self, mock_file, mock_exists, mock_find_root):
        """Test error handling when writing config fails."""
        from project_management_automation.tools.pattern_triggers import setup_pattern_triggers

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_file.side_effect = IOError("Write failed")
        
        result_str = setup_pattern_triggers()
        result = json.loads(result_str)
        
        assert result['status'] == 'error'
        assert 'error' in result

    def test_get_default_patterns(self):
        """Test default pattern generation."""
        from project_management_automation.tools.pattern_triggers import _get_default_patterns

        patterns = _get_default_patterns()
        
        assert 'file_patterns' in patterns
        assert 'git_events' in patterns
        assert 'task_status_changes' in patterns
        assert len(patterns['file_patterns']) > 0

    def test_extract_tools(self):
        """Test tool extraction from patterns."""
        from project_management_automation.tools.pattern_triggers import _extract_tools

        pattern_config = {
            "*.py": {
                "on_change": "run_linter_tool"
            },
            "pre_commit": {
                "tools": ["check_docs", "run_tests"]
            }
        }
        
        tools = _extract_tools(pattern_config)
        
        assert 'run_linter_tool' in tools
        assert 'check_docs' in tools
        assert 'run_tests' in tools

    @patch('project_management_automation.tools.pattern_triggers.Path.exists')
    def test_setup_git_hooks_integration_no_git(self, mock_exists):
        """Test git hooks integration when .git doesn't exist."""
        from project_management_automation.tools.pattern_triggers import _setup_git_hooks_integration

        mock_exists.return_value = False
        results = {}
        
        _setup_git_hooks_integration(Path("/test"), {"git_events": {}}, results)
        
        assert len(results.get('patterns_skipped', [])) > 0

    def test_generate_file_watcher_script(self):
        """Test file watcher script generation."""
        from project_management_automation.tools.pattern_triggers import _generate_file_watcher_script

        file_patterns = {
            "*.py": {"on_change": "run_linter"}
        }
        
        script = _generate_file_watcher_script(file_patterns)
        
        assert '#!/usr/bin/env python3' in script
        assert 'automa_patterns.json' in script
        assert 'file_patterns' in script

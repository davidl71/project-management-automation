"""
Unit Tests for Git Hooks Tool

Tests for git_hooks.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestGitHooksTool:
    """Tests for git hooks tool."""

    @patch('project_management_automation.tools.git_hooks.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.chmod')
    @patch('json.load')
    def test_setup_git_hooks_success(self, mock_json_load, mock_chmod, mock_file, mock_exists):
        """Test successful git hooks setup."""
        from project_management_automation.tools.git_hooks import setup_git_hooks

        # Mock .git/hooks directory exists
        mock_exists.return_value = True
        
        # Mock MCP config
        mock_json_load.return_value = {
            'mcpServers': {
                'exarp': {
                    'command': '/path/to/exarp.sh'
                }
            }
        }
        
        result_str = setup_git_hooks(hooks=['pre-commit'], dry_run=False)
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert len(result['hooks_configured']) == 1
        assert result['hooks_configured'][0]['hook'] == 'pre-commit'

    @patch('project_management_automation.tools.git_hooks.Path.exists')
    def test_setup_git_hooks_no_git_dir(self, mock_exists):
        """Test when .git/hooks directory doesn't exist."""
        from project_management_automation.tools.git_hooks import setup_git_hooks

        mock_exists.return_value = False
        
        result_str = setup_git_hooks()
        result = json.loads(result_str)
        
        assert result['status'] == 'error'
        assert 'not found' in result['error'].lower()

    @patch('project_management_automation.tools.git_hooks.Path.exists')
    def test_setup_git_hooks_dry_run(self, mock_exists):
        """Test dry run mode."""
        from project_management_automation.tools.git_hooks import setup_git_hooks

        mock_exists.return_value = True
        
        result_str = setup_git_hooks(hooks=['pre-commit', 'pre-push'], dry_run=True)
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert result['dry_run'] is True
        assert len(result['hooks_configured']) == 2
        # In dry run, should have 'would_create' instead of 'file'
        assert 'would_create' in result['hooks_configured'][0]

    @patch('project_management_automation.tools.git_hooks.Path.exists')
    def test_setup_git_hooks_all_hooks(self, mock_exists):
        """Test setting up all hooks."""
        from project_management_automation.tools.git_hooks import setup_git_hooks

        mock_exists.return_value = True
        
        result_str = setup_git_hooks(hooks=None, dry_run=True)  # None = all hooks
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert len(result['hooks_configured']) == 4  # All 4 default hooks

    @patch('project_management_automation.tools.git_hooks.Path.exists')
    def test_setup_git_hooks_unknown_hook(self, mock_exists):
        """Test with unknown hook type."""
        from project_management_automation.tools.git_hooks import setup_git_hooks

        mock_exists.return_value = True
        
        result_str = setup_git_hooks(hooks=['unknown-hook'], dry_run=True)
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert len(result['hooks_skipped']) == 1
        assert result['hooks_skipped'][0]['reason'] == 'Unknown hook type'

    @patch('project_management_automation.tools.git_hooks.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.chmod')
    @patch('json.load')
    def test_setup_git_hooks_write_error(self, mock_json_load, mock_chmod, mock_file, mock_exists):
        """Test error handling when writing hook file fails."""
        from project_management_automation.tools.git_hooks import setup_git_hooks

        mock_exists.return_value = True
        mock_json_load.return_value = {'mcpServers': {}}
        mock_file.side_effect = IOError("Permission denied")
        
        result_str = setup_git_hooks(hooks=['pre-commit'], dry_run=False)
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        # Should have skipped the hook due to error
        assert len(result['hooks_skipped']) == 1
        assert 'Failed to create hook' in result['hooks_skipped'][0]['reason']

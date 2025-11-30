"""
Unit Tests for Working Copy Health Tool

Tests for working_copy_health.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestWorkingCopyHealthTool:
    """Tests for working copy health tool."""

    @patch('project_management_automation.tools.working_copy_health.subprocess.run')
    @patch('os.environ.get')
    def test_check_working_copy_health_local_ok(self, mock_env, mock_subprocess):
        """Test local working copy health check - clean."""
        from project_management_automation.tools.working_copy_health import check_working_copy_health

        mock_env.return_value = "{}"  # No remote agents
        
        # Mock git commands
        def mock_git(cmd, **kwargs):
            if 'status' in cmd:
                return Mock(returncode=0, stdout="", stderr="")
            elif 'branch' in cmd:
                return Mock(returncode=0, stdout="main\n", stderr="")
            elif 'log' in cmd:
                return Mock(returncode=0, stdout="abc123 Commit message\n", stderr="")
            elif 'fetch' in cmd:
                return Mock(returncode=0, stdout="", stderr="")
            elif 'rev-list' in cmd:
                return Mock(returncode=0, stdout="0\n", stderr="")
            return Mock(returncode=0, stdout="", stderr="")
        
        mock_subprocess.side_effect = mock_git
        
        result = check_working_copy_health(check_remote=False)
        
        assert 'summary' in result
        assert 'agents' in result
        assert 'local' in result['agents']
        assert result['agents']['local']['status'] == 'ok'

    @patch('project_management_automation.tools.working_copy_health.subprocess.run')
    @patch('os.environ.get')
    def test_check_working_copy_health_with_changes(self, mock_env, mock_subprocess):
        """Test working copy with uncommitted changes."""
        from project_management_automation.tools.working_copy_health import check_working_copy_health

        mock_env.return_value = "{}"
        
        def mock_git(cmd, **kwargs):
            if 'status' in cmd:
                return Mock(returncode=0, stdout="M file1.py\nA file2.py\n", stderr="")
            elif 'branch' in cmd:
                return Mock(returncode=0, stdout="main\n", stderr="")
            elif 'log' in cmd:
                return Mock(returncode=0, stdout="abc123 Commit\n", stderr="")
            elif 'fetch' in cmd:
                return Mock(returncode=0, stdout="", stderr="")
            elif 'rev-list' in cmd:
                return Mock(returncode=0, stdout="0\n", stderr="")
            return Mock(returncode=0, stdout="", stderr="")
        
        mock_subprocess.side_effect = mock_git
        
        result = check_working_copy_health(check_remote=False)
        
        assert result['agents']['local']['has_uncommitted_changes'] is True
        assert len(result['agents']['local']['uncommitted_files']) > 0
        assert result['agents']['local']['status'] == 'warning'

    @patch('project_management_automation.tools.working_copy_health.subprocess.run')
    @patch('os.environ.get')
    def test_check_working_copy_health_behind_remote(self, mock_env, mock_subprocess):
        """Test working copy behind remote."""
        from project_management_automation.tools.working_copy_health import check_working_copy_health

        mock_env.return_value = "{}"
        
        def mock_git(cmd, **kwargs):
            if 'status' in cmd:
                return Mock(returncode=0, stdout="", stderr="")
            elif 'branch' in cmd:
                return Mock(returncode=0, stdout="main\n", stderr="")
            elif 'log' in cmd:
                return Mock(returncode=0, stdout="abc123 Commit\n", stderr="")
            elif 'fetch' in cmd:
                return Mock(returncode=0, stdout="", stderr="")
            elif 'rev-list' in cmd:
                if 'HEAD..origin/main' in ' '.join(cmd):
                    return Mock(returncode=0, stdout="3\n", stderr="")  # 3 commits behind
                else:
                    return Mock(returncode=0, stdout="0\n", stderr="")
            return Mock(returncode=0, stdout="", stderr="")
        
        mock_subprocess.side_effect = mock_git
        
        result = check_working_copy_health(check_remote=False)
        
        assert result['agents']['local']['behind_remote'] == 3
        assert result['agents']['local']['status'] == 'warning'

    @patch('project_management_automation.tools.working_copy_health.subprocess.run')
    @patch('os.environ.get')
    def test_check_working_copy_health_specific_agent(self, mock_env, mock_subprocess):
        """Test checking specific agent."""
        from project_management_automation.tools.working_copy_health import check_working_copy_health

        mock_env.return_value = "{}"
        
        def mock_git(cmd, **kwargs):
            return Mock(returncode=0, stdout="", stderr="")
        
        mock_subprocess.side_effect = mock_git
        
        result = check_working_copy_health(agent_name="local", check_remote=False)
        
        assert 'local' in result['agents']
        assert len(result['agents']) == 1

    @patch('project_management_automation.tools.working_copy_health.subprocess.run')
    @patch('os.environ.get')
    def test_check_working_copy_health_git_error(self, mock_env, mock_subprocess):
        """Test error handling when git command fails."""
        from project_management_automation.tools.working_copy_health import check_working_copy_health

        mock_env.return_value = "{}"
        mock_subprocess.side_effect = subprocess.TimeoutExpired("git", 5)
        
        result = check_working_copy_health(check_remote=False)
        
        assert 'local' in result['agents']
        assert result['agents']['local']['status'] == 'error'

    @patch('socket.gethostname')
    @patch('socket.getfqdn')
    def test_get_local_ip_addresses(self, mock_fqdn, mock_hostname):
        """Test local IP address detection."""
        from project_management_automation.tools.working_copy_health import _get_local_ip_addresses

        mock_hostname.return_value = 'testhost'
        mock_fqdn.return_value = 'testhost.local'
        
        ips = _get_local_ip_addresses()
        
        assert isinstance(ips, list)
        assert 'testhost' in ips

    @patch('socket.gethostname')
    def test_is_local_host(self, mock_hostname):
        """Test local host detection."""
        from project_management_automation.tools.working_copy_health import _is_local_host

        mock_hostname.return_value = 'testhost'
        
        assert _is_local_host('localhost') is True
        assert _is_local_host('127.0.0.1') is True
        assert _is_local_host('testhost') is True

    def test_generate_recommendations(self):
        """Test recommendation generation."""
        from project_management_automation.tools.working_copy_health import _generate_recommendations

        # Agent with uncommitted changes
        results = {
            'agent1': {
                'status': 'warning',
                'has_uncommitted_changes': True,
                'uncommitted_files': ['file1.py', 'file2.py']
            }
        }
        recommendations = _generate_recommendations(results)
        assert len(recommendations) > 0
        assert 'Commit' in recommendations[0]

        # Agent behind remote
        results = {
            'agent2': {
                'status': 'warning',
                'behind_remote': 5
            }
        }
        recommendations = _generate_recommendations(results)
        assert any('Pull' in r for r in recommendations)

        # All clean
        results = {
            'agent3': {
                'status': 'ok',
                'has_uncommitted_changes': False,
                'behind_remote': 0,
                'ahead_remote': 0
            }
        }
        recommendations = _generate_recommendations(results)
        assert any('clean' in r.lower() for r in recommendations)

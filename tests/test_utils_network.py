"""
Unit Tests for Network Utility Functions

Tests for shared network utility functions used across multiple tools.
These functions are currently duplicated in:
- project_management_automation.tools.nightly_task_automation
- project_management_automation.tools.working_copy_health

TODO: Refactor to move these functions to a shared utils module.
"""

import pytest
from unittest.mock import patch
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestGetLocalIPAddresses:
    """Tests for _get_local_ip_addresses utility function."""

    @patch('socket.gethostname')
    @patch('socket.getfqdn')
    def test_get_local_ip_addresses_from_nightly_module(self, mock_fqdn, mock_hostname):
        """Test local IP address detection from nightly_task_automation module."""
        from project_management_automation.tools.nightly_task_automation import _get_local_ip_addresses

        mock_hostname.return_value = 'testhost'
        mock_fqdn.return_value = 'testhost.local'
        
        ips = _get_local_ip_addresses()
        
        assert isinstance(ips, list)
        assert 'testhost' in ips

    @patch('socket.gethostname')
    @patch('socket.getfqdn')
    def test_get_local_ip_addresses_from_working_copy_module(self, mock_fqdn, mock_hostname):
        """Test local IP address detection from working_copy_health module."""
        from project_management_automation.tools.working_copy_health import _get_local_ip_addresses

        mock_hostname.return_value = 'testhost'
        mock_fqdn.return_value = 'testhost.local'
        
        ips = _get_local_ip_addresses()
        
        assert isinstance(ips, list)
        assert 'testhost' in ips


class TestIsLocalHost:
    """Tests for _is_local_host utility function."""

    @patch('socket.gethostname')
    def test_is_local_host_from_nightly_module(self, mock_hostname):
        """Test local host detection from nightly_task_automation module."""
        from project_management_automation.tools.nightly_task_automation import _is_local_host

        mock_hostname.return_value = 'testhost'
        
        assert _is_local_host('localhost') is True
        assert _is_local_host('127.0.0.1') is True
        assert _is_local_host('testhost') is True

    @patch('socket.gethostname')
    def test_is_local_host_from_working_copy_module(self, mock_hostname):
        """Test local host detection from working_copy_health module."""
        from project_management_automation.tools.working_copy_health import _is_local_host

        mock_hostname.return_value = 'testhost'
        
        assert _is_local_host('localhost') is True
        assert _is_local_host('127.0.0.1') is True
        assert _is_local_host('testhost') is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


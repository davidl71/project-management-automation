"""
Pytest Configuration for MCP Server Tests

Provides fixtures and test configuration.
"""

import sys
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def project_root_path():
    """Fixture providing project root path."""
    return project_root


@pytest.fixture
def server_path():
    """Fixture providing server.py path."""
    return Path(__file__).parent.parent / 'server.py'


@pytest.fixture
def mcp_config_path():
    """Fixture providing MCP config path."""
    return project_root / '.cursor' / 'mcp.json'


@pytest.fixture
def mock_project_root():
    """
    Mock project root finder.
    
    Returns a mock that patches find_project_root to return a test project path.
    Usage:
        def test_something(mock_project_root):
            # mock_project_root is already patched
            from project_management_automation.tools.some_tool import tool_function
            result = tool_function()
    """
    test_project_path = Path("/test/project")
    with patch('project_management_automation.utils.find_project_root', return_value=test_project_path) as mock:
        yield mock


@pytest.fixture
def mock_automation_run():
    """
    Helper to create mock automation instances with run() method.
    
    Usage:
        def test_tool(mock_automation_run):
            mock_instance = mock_automation_run({'status': 'success', 'results': {}})
            with patch('project_management_automation.scripts.automate_X.AutomationClass', return_value=mock_instance):
                result = tool_function()
    """
    def _create_mock(return_value):
        """Create a mock automation instance with run() method."""
        mock = Mock()
        mock.run.return_value = return_value
        return mock
    return _create_mock


@pytest.fixture
def mock_mcp_client():
    """
    Mock MCP client for testing MCP-dependent tools.
    
    Usage:
        def test_mcp_tool(mock_mcp_client):
            mock_mcp_client.call_tool.return_value = {'result': 'test'}
            # Test tool that uses MCP client
    """
    mock_client = Mock()
    mock_client.call_tool = Mock(return_value={'result': 'success'})
    mock_client.list_tools = Mock(return_value=[])
    mock_client.list_resources = Mock(return_value=[])
    return mock_client

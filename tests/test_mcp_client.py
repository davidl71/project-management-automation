"""
Unit Tests for MCPClient Class

Tests MCP client functionality for calling other MCP servers.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from pathlib import Path
import sys
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestMCPClient:
    """Tests for MCPClient class."""

    @patch('builtins.open', create=True)
    @patch('project_management_automation.scripts.base.mcp_client.Path')
    def test_mcp_client_init(self, mock_path, mock_open):
        """Test MCPClient initialization."""
        from project_management_automation.scripts.base.mcp_client import MCPClient
        import json

        # Mock config file
        mock_config_file = Mock()
        mock_config_file.exists.return_value = True
        mock_config_file.__truediv__ = lambda self, other: mock_config_file
        mock_path.return_value = mock_config_file

        # Mock file open and json.load
        mock_file = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=None)
        mock_file.read.return_value = '{"mcpServers": {"test": {}}}'
        mock_open.return_value = mock_file

        # Create client
        client = MCPClient(project_root=Path("/test/project"))

        # Assertions
        assert client.project_root == Path("/test/project")
        # Config should be loaded (empty dict if file doesn't exist, or parsed JSON)
        assert isinstance(client.mcp_config, dict)

    def test_mcp_client_no_config(self):
        """Test MCPClient with no config file."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        # Create client with non-existent config
        client = MCPClient(project_root=Path("/nonexistent/project"))

        # Should handle gracefully with empty config
        assert client.mcp_config == {}

    @patch('project_management_automation.scripts.base.mcp_client.logger')
    def test_call_tractatus_thinking_not_configured(self, mock_logger):
        """Test Tractatus Thinking call when not configured."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        client = MCPClient(project_root=Path("/test"))
        client.mcp_config = {}  # No tractatus_thinking configured

        result = client.call_tractatus_thinking("start", concept="test")

        assert result is None
        mock_logger.warning.assert_called()

    @patch('project_management_automation.scripts.base.mcp_client.logger')
    def test_call_tractatus_thinking_configured(self, mock_logger):
        """Test Tractatus Thinking call when configured."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        client = MCPClient(project_root=Path("/test"))
        client.mcp_config = {"tractatus_thinking": {}}

        result = client.call_tractatus_thinking("start", concept="test concept")

        assert result is not None
        assert 'session_id' in result
        assert 'concept' in result
        assert result['concept'] == "test concept"

    @patch('project_management_automation.scripts.base.mcp_client.logger')
    def test_call_sequential_thinking_not_configured(self, mock_logger):
        """Test Sequential Thinking call when not configured."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        client = MCPClient(project_root=Path("/test"))
        client.mcp_config = {}  # No sequential_thinking configured

        result = client.call_sequential_thinking("start", problem="test")

        assert result is None
        mock_logger.warning.assert_called()

    @patch('project_management_automation.scripts.base.mcp_client.logger')
    def test_call_sequential_thinking_configured(self, mock_logger):
        """Test Sequential Thinking call when configured."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        client = MCPClient(project_root=Path("/test"))
        client.mcp_config = {"sequential_thinking": {}}

        result = client.call_sequential_thinking("start", problem="test problem")

        assert result is not None
        assert 'session_id' in result
        assert 'problem' in result
        assert result['problem'] == "test problem"
        assert 'steps' in result

    def test_extract_components_simple(self):
        """Test simple component extraction."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        client = MCPClient(project_root=Path("/test"))

        # Test with × separator
        components = client._extract_components_simple("A × B × C")
        assert len(components) >= 3

        # Test with * separator
        components = client._extract_components_simple("A * B * C")
        assert len(components) >= 3

        # Test with no separator
        components = client._extract_components_simple("Simple concept")
        assert isinstance(components, list)

    def test_plan_steps_simple(self):
        """Test simple step planning."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        client = MCPClient(project_root=Path("/test"))

        steps = client._plan_steps_simple("How do we implement X?")
        assert isinstance(steps, list)
        assert len(steps) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


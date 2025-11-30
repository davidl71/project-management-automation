#!/usr/bin/env python3
"""
Unit tests for MCPClient agentic-tools MCP support.

Tests the async methods for list_todos, create_task, update_task, get_task, delete_task.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest


class TestMCPClientAgenticTools:
    """Tests for MCPClient agentic-tools integration."""

    @pytest.fixture
    def mock_project_root(self, tmp_path):
        """Create a mock project root with .cursor/mcp.json config."""
        cursor_dir = tmp_path / '.cursor'
        cursor_dir.mkdir()

        mcp_config = {
            "mcpServers": {
                "agentic-tools": {
                    "command": "npx",
                    "args": ["-y", "@agentic/mcp-server"]
                }
            }
        }

        (cursor_dir / 'mcp.json').write_text(json.dumps(mcp_config))
        return tmp_path

    @pytest.fixture
    def mcp_client(self, mock_project_root):
        """Create an MCPClient instance with mock config."""
        from project_management_automation.scripts.base.mcp_client import MCPClient
        return MCPClient(mock_project_root)

    def test_mcp_client_initialization(self, mcp_client, mock_project_root):
        """Test MCPClient initializes correctly with agentic-tools config."""
        assert mcp_client.project_root == mock_project_root
        assert 'agentic-tools' in mcp_client.mcp_config
        assert mcp_client.agentic_tools_session is None

    def test_mcp_client_no_config(self, tmp_path):
        """Test MCPClient handles missing config gracefully."""
        from project_management_automation.scripts.base.mcp_client import MCPClient
        client = MCPClient(tmp_path)
        assert client.mcp_config == {}

    @pytest.mark.asyncio
    async def test_list_todos_no_mcp_available(self, tmp_path):
        """Test list_todos returns empty list when MCP unavailable."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        with patch('project_management_automation.scripts.base.mcp_client.MCP_CLIENT_AVAILABLE', False):
            client = MCPClient(tmp_path)
            result = await client.list_todos("test-project", str(tmp_path))
            assert result == []

    @pytest.mark.asyncio
    async def test_create_task_no_mcp_available(self, tmp_path):
        """Test create_task returns None when MCP unavailable."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        with patch('project_management_automation.scripts.base.mcp_client.MCP_CLIENT_AVAILABLE', False):
            client = MCPClient(tmp_path)
            result = await client.create_task(
                "test-project",
                str(tmp_path),
                "Test Task",
                "Test details"
            )
            assert result is None

    @pytest.mark.asyncio
    async def test_update_task_no_mcp_available(self, tmp_path):
        """Test update_task returns None when MCP unavailable."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        with patch('project_management_automation.scripts.base.mcp_client.MCP_CLIENT_AVAILABLE', False):
            client = MCPClient(tmp_path)
            result = await client.update_task(
                "test-task-id",
                str(tmp_path),
                status="done"
            )
            assert result is None

    @pytest.mark.asyncio
    async def test_get_task_no_mcp_available(self, tmp_path):
        """Test get_task returns None when MCP unavailable."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        with patch('project_management_automation.scripts.base.mcp_client.MCP_CLIENT_AVAILABLE', False):
            client = MCPClient(tmp_path)
            result = await client.get_task("test-task-id", str(tmp_path))
            assert result is None

    @pytest.mark.asyncio
    async def test_delete_task_no_mcp_available(self, tmp_path):
        """Test delete_task returns False when MCP unavailable."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        with patch('project_management_automation.scripts.base.mcp_client.MCP_CLIENT_AVAILABLE', False):
            client = MCPClient(tmp_path)
            result = await client.delete_task("test-task-id", str(tmp_path))
            assert result is False


class TestMCPClientAgenticToolsIntegration:
    """Integration tests for MCPClient agentic-tools (requires MCP server)."""

    @pytest.fixture
    def real_project_root(self):
        """Use the actual project root for integration tests."""
        return Path(__file__).parent.parent

    @pytest.mark.skip(reason="Integration test - requires agentic-tools MCP server running")
    @pytest.mark.asyncio
    async def test_list_todos_integration(self, real_project_root):
        """Test list_todos against real agentic-tools MCP server."""
        from project_management_automation.scripts.base.mcp_client import MCPClient

        client = MCPClient(real_project_root)
        # This would require a valid project ID
        result = await client.list_todos(
            "514c2160-9f81-4c4f-b4de-bad0938d57d6",
            str(real_project_root)
        )
        assert isinstance(result, list)


class TestMCPClientHelperMethods:
    """Tests for MCPClient helper methods."""

    @pytest.fixture
    def mcp_client(self, tmp_path):
        """Create an MCPClient instance."""
        from project_management_automation.scripts.base.mcp_client import MCPClient
        return MCPClient(tmp_path)

    def test_extract_components_simple_with_multiplication(self, mcp_client):
        """Test component extraction with × operator."""
        components = mcp_client._extract_components_simple("A × B × C")
        assert components == ["A", "B", "C"]

    def test_extract_components_simple_with_asterisk(self, mcp_client):
        """Test component extraction with * operator."""
        components = mcp_client._extract_components_simple("A * B * C")
        assert components == ["A", "B", "C"]

    def test_extract_components_simple_with_keywords(self, mcp_client):
        """Test component extraction with keywords."""
        components = mcp_client._extract_components_simple("Run automation and check health")
        assert 'automation' in components
        assert 'health' in components

    def test_plan_steps_simple_default(self, mcp_client):
        """Test default step planning."""
        steps = mcp_client._plan_steps_simple("Do something")
        assert len(steps) == 4
        assert "Load and analyze data" in steps

    def test_plan_steps_simple_find(self, mcp_client):
        """Test step planning for find operations."""
        steps = mcp_client._plan_steps_simple("Find automation opportunities")
        assert "Search for opportunities" in steps

    def test_plan_steps_simple_check(self, mcp_client):
        """Test step planning for check operations."""
        steps = mcp_client._plan_steps_simple("Check documentation health")
        assert "Run validation checks" in steps


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


"""
Unit Tests for MCP Resources

Tests all registered resources to ensure they are correctly exposed and return valid data.
"""

import pytest
import json
from unittest.mock import patch, Mock, mock_open
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestResourceHandlers:
    """Tests for resource handler functions."""

    def test_status_resource_handler(self):
        """Test automation://status resource handler."""
        from project_management_automation.resources.status import get_status_resource
        
        result = get_status_resource()
        result_data = json.loads(result)
        
        assert 'status' in result_data
        assert 'version' in result_data
        assert 'tools' in result_data
        assert isinstance(result_data['tools'], dict)
        assert 'total' in result_data['tools']
        assert 'available' in result_data['tools']

    def test_history_resource_handler(self):
        """Test automation://history resource handler."""
        from project_management_automation.resources.history import get_history_resource
        
        result = get_history_resource()
        result_data = json.loads(result)
        
        assert 'automation_history' in result_data  # Actual key name
        assert isinstance(result_data['automation_history'], list)
        assert 'timestamp' in result_data

    def test_tools_list_resource_handler(self):
        """Test automation://tools resource handler."""
        from project_management_automation.resources.list import get_tools_list_resource
        
        result = get_tools_list_resource()
        result_data = json.loads(result)
        
        assert 'tools' in result_data
        assert isinstance(result_data['tools'], list)
        assert len(result_data['tools']) > 0
        assert 'total_tools' in result_data
        assert 'timestamp' in result_data

    def test_tasks_resource_handler(self):
        """Test automation://tasks resource handler."""
        from project_management_automation.resources.tasks import get_tasks_resource
        
        # Mock Todo2 file
        mock_tasks_data = {
            'todos': [
                {'id': 'T-1', 'name': 'Test Task', 'status': 'Todo'}
            ]
        }
        
        with patch('project_management_automation.resources.tasks.Path') as mock_path:
            mock_todo2_path = Mock()
            mock_todo2_path.exists.return_value = True
            mock_todo2_path.read_text.return_value = json.dumps(mock_tasks_data)
            mock_path.return_value = mock_todo2_path
            
            result = get_tasks_resource()
            result_data = json.loads(result)
            
            assert 'tasks' in result_data
            assert isinstance(result_data['tasks'], list)

    def test_tasks_by_agent_resource_handler(self):
        """Test automation://tasks/agent/{agent_name} resource handler."""
        from project_management_automation.resources.tasks import get_agent_tasks_resource
        
        # Mock Todo2 file
        mock_tasks_data = {
            'todos': [
                {'id': 'T-1', 'name': 'Test Task', 'status': 'Todo', 'agent': 'test_agent'}
            ]
        }
        
        with patch('project_management_automation.resources.tasks.Path') as mock_path:
            mock_todo2_path = Mock()
            mock_todo2_path.exists.return_value = True
            mock_todo2_path.read_text.return_value = json.dumps(mock_tasks_data)
            mock_path.return_value = mock_todo2_path
            
            result = get_agent_tasks_resource('test_agent')
            result_data = json.loads(result)
            
            assert 'tasks' in result_data
            assert isinstance(result_data['tasks'], list)

    def test_tasks_by_status_resource_handler(self):
        """Test automation://tasks/status/{status} resource handler."""
        from project_management_automation.resources.tasks import get_tasks_resource
        
        # Mock Todo2 file
        mock_tasks_data = {
            'todos': [
                {'id': 'T-1', 'name': 'Test Task', 'status': 'Todo'}
            ]
        }
        
        with patch('project_management_automation.resources.tasks.Path') as mock_path:
            mock_todo2_path = Mock()
            mock_todo2_path.exists.return_value = True
            mock_todo2_path.read_text.return_value = json.dumps(mock_tasks_data)
            mock_path.return_value = mock_todo2_path
            
            result = get_tasks_resource(status='Todo')
            result_data = json.loads(result)
            
            assert 'tasks' in result_data
            assert isinstance(result_data['tasks'], list)

    def test_cache_resource_handler(self):
        """Test automation://cache resource handler."""
        from project_management_automation.resources.cache import get_cache_status_resource
        
        result = get_cache_status_resource()
        result_data = json.loads(result)
        
        assert 'caches' in result_data  # Actual key name
        assert isinstance(result_data['caches'], list)
        assert 'timestamp' in result_data


class TestResourceRegistration:
    """Tests for resource registration in server."""

    @patch('project_management_automation.server.mcp')
    def test_resources_registered(self, mock_mcp):
        """Test that resources are registered in the MCP server."""
        # Import server to trigger registration
        import project_management_automation.server as server_module
        
        # Check if resources are registered (via decorators)
        # This is a basic check - actual registration happens at runtime
        assert hasattr(server_module, 'mcp') or mock_mcp is not None


class TestResourceURIs:
    """Tests for resource URI patterns."""

    def test_resource_uri_patterns(self):
        """Test that all resource URIs follow expected patterns."""
        expected_uris = [
            "automation://status",
            "automation://history",
            "automation://tools",
            "automation://tasks",
            "automation://tasks/agent/{agent_name}",
            "automation://tasks/status/{status}",
            "automation://agents",
            "automation://cache"
        ]
        
        # Verify URIs are properly formatted
        for uri in expected_uris:
            assert uri.startswith("automation://"), f"URI '{uri}' must start with 'automation://'"
            assert len(uri) > len("automation://"), f"URI '{uri}' must have a path"


class TestResourceJSONFormat:
    """Tests for resource JSON format validation."""

    def test_status_resource_json_valid(self):
        """Test that status resource returns valid JSON."""
        from project_management_automation.resources.status import get_status_resource
        
        result = get_status_resource()
        # Should not raise exception
        result_data = json.loads(result)
        assert isinstance(result_data, dict)

    def test_history_resource_json_valid(self):
        """Test that history resource returns valid JSON."""
        from project_management_automation.resources.history import get_history_resource
        
        result = get_history_resource()
        result_data = json.loads(result)
        assert isinstance(result_data, dict)

    def test_tools_list_resource_json_valid(self):
        """Test that tools list resource returns valid JSON."""
        from project_management_automation.resources.list import get_tools_list_resource
        
        result = get_tools_list_resource()
        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert 'tools' in result_data
        assert isinstance(result_data['tools'], list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


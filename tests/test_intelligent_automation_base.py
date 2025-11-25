"""
Unit Tests for IntelligentAutomationBase Class

Tests base class functionality for automation scripts.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
from abc import ABC
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestIntelligentAutomationBase:
    """Tests for IntelligentAutomationBase class."""

    def test_base_class_abstract(self):
        """Test that IntelligentAutomationBase is abstract."""
        from project_management_automation.scripts.base.intelligent_automation_base import IntelligentAutomationBase

        # Cannot instantiate abstract class directly
        with pytest.raises(TypeError):
            IntelligentAutomationBase({}, "Test", Path("/test"))

    def test_base_class_init(self):
        """Test IntelligentAutomationBase initialization."""
        from project_management_automation.scripts.base.intelligent_automation_base import IntelligentAutomationBase

        # Create a concrete implementation for testing
        class TestAutomation(IntelligentAutomationBase):
            def _execute_analysis(self) -> dict:
                return {'status': 'success', 'results': {}}
            
            def _get_tractatus_concept(self) -> str:
                return "Test concept"
            
            def _get_sequential_thinking_problem(self) -> str:
                return "Test problem"
            
            def _generate_insights(self, analysis_results: dict) -> dict:
                return {'insights': []}
            
            def _generate_report(self, analysis_results: dict, insights: dict) -> str:
                return "Test report"

        config = {'test': 'value'}
        project_root = Path("/test/project")
        
        automation = TestAutomation(config, "Test Automation", project_root)

        # Assertions
        assert automation.automation_name == "Test Automation"
        assert automation.project_root == project_root
        assert automation.config == config
        assert automation.results is not None
        assert 'automation_name' in automation.results

    @patch('project_management_automation.scripts.base.intelligent_automation_base.get_mcp_client')
    @patch('project_management_automation.scripts.base.intelligent_automation_base.MCP_AVAILABLE', True)
    def test_tractatus_analysis(self, mock_get_mcp_client):
        """Test Tractatus Thinking analysis."""
        from project_management_automation.scripts.base.intelligent_automation_base import IntelligentAutomationBase

        # Mock MCP client
        mock_client = Mock()
        mock_client.call_tractatus_thinking.return_value = {
            'session_id': 'test_session',
            'concept': 'test',
            'components': ['A', 'B', 'C']
        }
        mock_get_mcp_client.return_value = mock_client

        class TestAutomation(IntelligentAutomationBase):
            def _execute_analysis(self) -> dict:
                return {'status': 'success', 'results': {}}
            
            def _get_tractatus_concept(self) -> str:
                return "Test concept"

        automation = TestAutomation({}, "Test", Path("/test"))
        automation._tractatus_analysis()

        # Should have called Tractatus Thinking
        mock_client.call_tractatus_thinking.assert_called()

    @patch('project_management_automation.scripts.base.intelligent_automation_base.get_mcp_client')
    @patch('project_management_automation.scripts.base.intelligent_automation_base.MCP_AVAILABLE', True)
    def test_sequential_planning(self, mock_get_mcp_client):
        """Test Sequential Thinking planning."""
        from project_management_automation.scripts.base.intelligent_automation_base import IntelligentAutomationBase

        # Mock MCP client
        mock_client = Mock()
        mock_client.call_sequential_thinking.return_value = {
            'session_id': 'test_session',
            'problem': 'test',
            'steps': ['step1', 'step2']
        }
        mock_get_mcp_client.return_value = mock_client

        class TestAutomation(IntelligentAutomationBase):
            def _execute_analysis(self) -> dict:
                return {'status': 'success', 'results': {}}
            
            def _get_sequential_thinking_problem(self) -> str:
                return "How do we test this?"

        automation = TestAutomation({}, "Test", Path("/test"))
        automation._sequential_planning()

        # Should have called Sequential Thinking
        mock_client.call_sequential_thinking.assert_called()

    @patch('project_management_automation.scripts.base.intelligent_automation_base.MCP_AVAILABLE', False)
    def test_run_method(self):
        """Test run() method execution."""
        from project_management_automation.scripts.base.intelligent_automation_base import IntelligentAutomationBase

        class TestAutomation(IntelligentAutomationBase):
            def _execute_analysis(self) -> dict:
                return {
                    'status': 'success',
                    'results': {'test': 'data'},
                    'findings': ['finding1'],
                    'recommendations': ['recommendation1']
                }
            
            def _get_tractatus_concept(self) -> str:
                return "Test concept"
            
            def _get_sequential_thinking_problem(self) -> str:
                return "Test problem"

        automation = TestAutomation({}, "Test", Path("/test"))
        result = automation.run()

        # Assertions
        assert result is not None
        assert result['status'] == 'success'
        assert 'results' in result
        assert 'workflow_steps' in result
        assert 'findings' in result
        assert 'recommendations' in result

    @patch('project_management_automation.scripts.base.intelligent_automation_base.MCP_AVAILABLE', False)
    def test_run_with_error(self):
        """Test run() method error handling."""
        from project_management_automation.scripts.base.intelligent_automation_base import IntelligentAutomationBase

        class TestAutomation(IntelligentAutomationBase):
            def _execute_analysis(self) -> dict:
                raise Exception("Test error")
            
            def _get_tractatus_concept(self) -> str:
                return "Test concept"
            
            def _get_sequential_thinking_problem(self) -> str:
                return "Test problem"

        automation = TestAutomation({}, "Test", Path("/test"))
        
        # Should raise exception (or handle gracefully)
        with pytest.raises(Exception):
            result = automation.run()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


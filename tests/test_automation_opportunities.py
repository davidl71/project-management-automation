"""
Unit Tests for Automation Opportunities Tool

Tests for automation_opportunities.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestAutomationOpportunitiesTool:
    """Tests for automation opportunities tool."""

    @patch('project_management_automation.tools.automation_opportunities.find_project_root')
    @patch('project_management_automation.tools.automation_opportunities.AutomationOpportunityFinder')
    def test_find_automation_opportunities_success(self, mock_finder_class, mock_find_root):
        """Test successful automation opportunity finding."""
        from project_management_automation.tools.automation_opportunities import find_automation_opportunities

        mock_find_root.return_value = Path("/test/project")
        
        # Mock finder instance
        mock_finder = Mock()
        mock_finder.run.return_value = {
            'results': {
                'opportunities': [
                    {'score': 8.5, 'name': 'Test Opportunity 1'},
                    {'score': 6.0, 'name': 'Test Opportunity 2'},
                    {'score': 4.0, 'name': 'Test Opportunity 3'}
                ],
                'high_priority': [{'score': 8.5}],
                'medium_priority': [{'score': 6.0}],
                'low_priority': [{'score': 4.0}],
                'existing_automations': 5
            },
            'status': 'success'
        }
        mock_finder_class.return_value = mock_finder
        
        result_str = find_automation_opportunities(min_value_score=0.7)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['total_opportunities'] == 3
        assert result['data']['filtered_opportunities'] == 2  # Only scores >= 7.0
        assert result['data']['high_priority_count'] == 1
        assert result['data']['existing_automations'] == 5

    @patch('project_management_automation.tools.automation_opportunities.find_project_root')
    @patch('project_management_automation.tools.automation_opportunities.AutomationOpportunityFinder')
    def test_find_automation_opportunities_custom_output_path(self, mock_finder_class, mock_find_root):
        """Test with custom output path."""
        from project_management_automation.tools.automation_opportunities import find_automation_opportunities

        mock_find_root.return_value = Path("/test/project")
        mock_finder = Mock()
        mock_finder.run.return_value = {
            'results': {
                'opportunities': [],
                'high_priority': [],
                'medium_priority': [],
                'low_priority': [],
                'existing_automations': 0
            },
            'status': 'success'
        }
        mock_finder_class.return_value = mock_finder
        
        result_str = find_automation_opportunities(output_path="/custom/path/report.md")
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert '/custom/path/report.md' in result['data']['report_path']

    @patch('project_management_automation.tools.automation_opportunities.find_project_root')
    @patch('project_management_automation.tools.automation_opportunities.AutomationOpportunityFinder')
    def test_find_automation_opportunities_custom_threshold(self, mock_finder_class, mock_find_root):
        """Test with custom min_value_score threshold."""
        from project_management_automation.tools.automation_opportunities import find_automation_opportunities

        mock_find_root.return_value = Path("/test/project")
        mock_finder = Mock()
        mock_finder.run.return_value = {
            'results': {
                'opportunities': [
                    {'score': 8.5, 'name': 'High'},
                    {'score': 5.0, 'name': 'Low'}
                ],
                'high_priority': [],
                'medium_priority': [],
                'low_priority': [],
                'existing_automations': 0
            },
            'status': 'success'
        }
        mock_finder_class.return_value = mock_finder
        
        # Threshold 0.5 means score >= 5.0
        result_str = find_automation_opportunities(min_value_score=0.5)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['filtered_opportunities'] == 2  # Both pass threshold

    @patch('project_management_automation.tools.automation_opportunities.find_project_root')
    @patch('project_management_automation.tools.automation_opportunities.AutomationOpportunityFinder')
    def test_find_automation_opportunities_error(self, mock_finder_class, mock_find_root):
        """Test error handling."""
        from project_management_automation.tools.automation_opportunities import find_automation_opportunities

        mock_find_root.return_value = Path("/test/project")
        mock_finder = Mock()
        mock_finder.run.side_effect = Exception("Test error")
        mock_finder_class.return_value = mock_finder
        
        result_str = find_automation_opportunities()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.tools.automation_opportunities.find_project_root')
    @patch('project_management_automation.tools.automation_opportunities.AutomationOpportunityFinder')
    def test_find_automation_opportunities_top_10_limit(self, mock_finder_class, mock_find_root):
        """Test that top_opportunities is limited to 10."""
        from project_management_automation.tools.automation_opportunities import find_automation_opportunities

        mock_find_root.return_value = Path("/test/project")
        mock_finder = Mock()
        # Create 15 opportunities
        opportunities = [{'score': 8.0 + i * 0.1, 'name': f'Opp {i}'} for i in range(15)]
        mock_finder.run.return_value = {
            'results': {
                'opportunities': opportunities,
                'high_priority': [],
                'medium_priority': [],
                'low_priority': [],
                'existing_automations': 0
            },
            'status': 'success'
        }
        mock_finder_class.return_value = mock_finder
        
        result_str = find_automation_opportunities(min_value_score=0.5)
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert len(result['data']['top_opportunities']) == 10

"""
Unit Tests for PWA Review Tool

Tests for pwa_review.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestPWAReviewTool:
    """Tests for PWA review tool."""

    @patch('project_management_automation.tools.pwa_review.find_project_root')
    @patch('project_management_automation.tools.pwa_review.load_config')
    @patch('project_management_automation.tools.pwa_review.PWAAnalyzer')
    def test_review_pwa_config_success(self, mock_analyzer_class, mock_load_config, mock_find_root):
        """Test successful PWA review."""
        from project_management_automation.tools.pwa_review import review_pwa_config

        mock_find_root.return_value = Path("/test/project")
        mock_load_config.return_value = {'output_path': 'docs/pwa.md'}
        
        # Mock analyzer instance
        mock_analyzer = Mock()
        mock_analyzer.run.return_value = True
        mock_analyzer.analyze_pwa_structure.return_value = {
            'components': ['Component1', 'Component2'],
            'hooks': ['useHook1'],
            'api_integrations': ['API1'],
            'pwa_features': ['feature1', 'feature2'],
            'missing_features': ['missing1']
        }
        mock_analyzer.load_todo2_tasks.return_value = []
        mock_analyzer.analyze_todo2_alignment.return_value = {
            'goal_aligned': 5,
            'pwa_related': 3
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        result_str = review_pwa_config()
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['components_count'] == 2
        assert result['data']['hooks_count'] == 1
        assert result['data']['api_integrations_count'] == 1
        assert len(result['data']['pwa_features']) == 2
        assert len(result['data']['missing_features']) == 1
        assert result['data']['goal_aligned_tasks'] == 5
        assert result['data']['pwa_related_tasks'] == 3

    @patch('project_management_automation.tools.pwa_review.find_project_root')
    @patch('project_management_automation.tools.pwa_review.load_config')
    @patch('project_management_automation.tools.pwa_review.PWAAnalyzer')
    def test_review_pwa_config_custom_output_path(self, mock_analyzer_class, mock_load_config, mock_find_root):
        """Test with custom output path."""
        from project_management_automation.tools.pwa_review import review_pwa_config

        mock_find_root.return_value = Path("/test/project")
        mock_load_config.return_value = {'output_path': 'docs/pwa.md'}
        mock_analyzer = Mock()
        mock_analyzer.run.return_value = True
        mock_analyzer.analyze_pwa_structure.return_value = {
            'components': [],
            'hooks': [],
            'api_integrations': [],
            'pwa_features': [],
            'missing_features': []
        }
        mock_analyzer.load_todo2_tasks.return_value = []
        mock_analyzer.analyze_todo2_alignment.return_value = {
            'goal_aligned': 0,
            'pwa_related': 0
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        result_str = review_pwa_config(output_path="/custom/pwa.md")
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Verify output_path was set in config
        assert mock_load_config.return_value['output_path'] == '/custom/pwa.md'

    @patch('project_management_automation.tools.pwa_review.find_project_root')
    @patch('project_management_automation.tools.pwa_review.load_config')
    @patch('project_management_automation.tools.pwa_review.PWAAnalyzer')
    def test_review_pwa_config_custom_config_path(self, mock_analyzer_class, mock_load_config, mock_find_root):
        """Test with custom config path."""
        from project_management_automation.tools.pwa_review import review_pwa_config

        mock_find_root.return_value = Path("/test/project")
        mock_load_config.return_value = {'output_path': 'docs/pwa.md'}
        mock_analyzer = Mock()
        mock_analyzer.run.return_value = True
        mock_analyzer.analyze_pwa_structure.return_value = {
            'components': [],
            'hooks': [],
            'api_integrations': [],
            'pwa_features': [],
            'missing_features': []
        }
        mock_analyzer.load_todo2_tasks.return_value = []
        mock_analyzer.analyze_todo2_alignment.return_value = {
            'goal_aligned': 0,
            'pwa_related': 0
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        result_str = review_pwa_config(config_path="/custom/config.json")
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Verify load_config was called with custom path
        mock_load_config.assert_called_with(Path("/custom/config.json"))

    @patch('project_management_automation.tools.pwa_review.find_project_root')
    @patch('project_management_automation.tools.pwa_review.load_config')
    @patch('project_management_automation.tools.pwa_review.PWAAnalyzer')
    def test_review_pwa_config_analyzer_fails(self, mock_analyzer_class, mock_load_config, mock_find_root):
        """Test when analyzer.run() returns False."""
        from project_management_automation.tools.pwa_review import review_pwa_config

        mock_find_root.return_value = Path("/test/project")
        mock_load_config.return_value = {'output_path': 'docs/pwa.md'}
        mock_analyzer = Mock()
        mock_analyzer.run.return_value = False  # Analysis failed
        mock_analyzer_class.return_value = mock_analyzer
        
        result_str = review_pwa_config()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.tools.pwa_review.find_project_root')
    @patch('project_management_automation.tools.pwa_review.load_config')
    @patch('project_management_automation.tools.pwa_review.PWAAnalyzer')
    def test_review_pwa_config_error(self, mock_analyzer_class, mock_load_config, mock_find_root):
        """Test error handling."""
        from project_management_automation.tools.pwa_review import review_pwa_config

        mock_find_root.return_value = Path("/test/project")
        mock_load_config.side_effect = Exception("Config load failed")
        
        result_str = review_pwa_config()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.tools.pwa_review.find_project_root')
    @patch('project_management_automation.tools.pwa_review.load_config')
    @patch('project_management_automation.tools.pwa_review.PWAAnalyzer')
    def test_review_pwa_config_empty_analysis(self, mock_analyzer_class, mock_load_config, mock_find_root):
        """Test with empty PWA analysis results."""
        from project_management_automation.tools.pwa_review import review_pwa_config

        mock_find_root.return_value = Path("/test/project")
        mock_load_config.return_value = {'output_path': 'docs/pwa.md'}
        mock_analyzer = Mock()
        mock_analyzer.run.return_value = True
        mock_analyzer.analyze_pwa_structure.return_value = {}
        mock_analyzer.load_todo2_tasks.return_value = []
        mock_analyzer.analyze_todo2_alignment.return_value = {}
        mock_analyzer_class.return_value = mock_analyzer
        
        result_str = review_pwa_config()
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['components_count'] == 0
        assert result['data']['status'] == 'success'

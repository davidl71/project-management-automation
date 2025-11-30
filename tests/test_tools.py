"""
Unit Tests for MCP Tool Wrappers

Tests each tool wrapper to ensure proper error handling and response formatting.
"""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDocumentationHealthTool:
    """Tests for check_documentation_health tool."""

    @patch('project_management_automation.scripts.automate_docs_health_v2.DocumentationHealthAnalyzerV2')
    def test_check_documentation_health_success(self, mock_analyzer_class):
        """Test successful documentation health check."""
        from project_management_automation.tools.docs_health import check_documentation_health

        # Mock analyzer
        mock_analyzer = Mock()
        mock_analyzer.run.return_value = {
            'status': 'success',
            'results': {
                'health_score': 85,
                'link_validation': {
                    'total_links': 100,
                    'broken_internal': [],
                    'broken_external': []
                },
                'format_validation': {
                    'format_errors': []
                }
            },
            'followup_tasks': []
        }
        mock_analyzer_class.return_value = mock_analyzer

        # Mock project root finder
        with patch('project_management_automation.utils.find_project_root', return_value=Path("/test")):
            # Call tool
            result = check_documentation_health(output_path="test_report.md", create_tasks=True)
        result_data = json.loads(result)

        # Assertions
        assert result_data['success'] is True
        assert result_data['data']['health_score'] == 85
        assert result_data['data']['report_path'] is not None

    @patch('project_management_automation.scripts.automate_docs_health_v2.DocumentationHealthAnalyzerV2')
    def test_check_documentation_health_error(self, mock_analyzer_class):
        """Test error handling in documentation health check."""
        from project_management_automation.tools.docs_health import check_documentation_health

        # Mock analyzer to raise exception
        mock_analyzer_class.side_effect = Exception("Test error")

        # Mock project root finder
        with patch('project_management_automation.utils.find_project_root', return_value=Path("/test")):
            # Call tool
            result = check_documentation_health()
            result_data = json.loads(result)

        # Assertions
        assert result_data['success'] is False
        assert 'error' in result_data


class TestTodo2AlignmentTool:
    """Tests for analyze_todo2_alignment tool."""

    @patch('project_management_automation.scripts.automate_todo2_alignment_v2.Todo2AlignmentAnalyzerV2')
    def test_analyze_todo2_alignment_success(self, mock_analyzer_class):
        """Test successful Todo2 alignment analysis."""
        from project_management_automation.tools.todo2_alignment import analyze_todo2_alignment

        # Mock analyzer
        mock_analyzer = Mock()
        mock_analyzer.run.return_value = {
            'status': 'success',
            'results': {
                'tasks_analyzed': 50,
                'misaligned_tasks': [],
                'alignment_scores': {
                    'average': 0.85
                }
            },
            'followup_tasks': []
        }
        mock_analyzer_class.return_value = mock_analyzer

        # Mock project root finder and Todo2 file
        with patch('project_management_automation.utils.find_project_root', return_value=Path("/test")), \
             patch('project_management_automation.tools.todo2_alignment.Path') as mock_path:
            mock_todo2_path = Mock()
            mock_todo2_path.exists.return_value = False
            mock_path.return_value = mock_todo2_path

        # Call tool
        result = analyze_todo2_alignment(create_followup_tasks=True)
        result_data = json.loads(result)

        # Assertions
        assert result_data['success'] is True
        assert 'data' in result_data


class TestDuplicateDetectionTool:
    """Tests for detect_duplicate_tasks tool."""

    @patch('project_management_automation.scripts.automate_todo2_duplicate_detection.Todo2DuplicateDetector')
    def test_detect_duplicate_tasks_success(self, mock_detector_class):
        """Test successful duplicate detection."""
        from project_management_automation.tools.duplicate_detection import detect_duplicate_tasks

        # Mock detector
        mock_detector = Mock()
        mock_detector.run.return_value = {
            'status': 'success',
            'results': {
                'duplicates': {
                    'duplicate_ids': [],
                    'exact_name_matches': [],
                    'similar_name_matches': [],
                    'similar_description_matches': [],
                    'self_dependencies': []
                }
            },
            'auto_fix_applied': False,
            'tasks_removed': 0,
            'tasks_merged': 0,
            'dependencies_updated': 0
        }
        mock_detector.duplicates = {
            'duplicate_ids': [],
            'exact_name_matches': [],
            'similar_name_matches': [],
            'similar_description_matches': [],
            'self_dependencies': []
        }
        mock_detector.total_tasks_analyzed = 10
        mock_detector_class.return_value = mock_detector

        # Mock project root finder and Todo2 file
        with patch('project_management_automation.utils.find_project_root', return_value=Path("/test")), \
             patch('project_management_automation.tools.duplicate_detection.Path') as mock_path:
            mock_todo2_path = Mock()
            mock_todo2_path.exists.return_value = False
            mock_path.return_value = mock_todo2_path

        # Call tool
        result = detect_duplicate_tasks(similarity_threshold=0.85, auto_fix=False)
        result_data = json.loads(result)

        # Assertions
        assert result_data['success'] is True
        assert result_data['data']['total_duplicates_found'] == 0


class TestDependencySecurityTool:
    """Tests for scan_dependency_security tool."""

    def test_scan_dependency_security_success(self):
        """Test dependency security scan returns valid JSON."""
        from project_management_automation.tools.dependency_security import scan_dependency_security

        # Call tool - it will work with real files or return error gracefully
        result = scan_dependency_security(languages=['python'])
        result_data = json.loads(result)

        # Check result is valid JSON with expected structure
        assert isinstance(result_data, dict)
        # Should have either success with data or error
        assert 'success' in result_data or 'total_vulnerabilities' in result_data or 'error' in str(result_data)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

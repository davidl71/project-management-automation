"""
Unit Tests for CodeQL Security Tool

Tests for codeql_security.py module (0% coverage → target: 80%+).
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestCodeQLSecurity:
    """Tests for CodeQL security integration."""

    @patch('project_management_automation.tools.codeql_security.find_project_root')
    def test_get_codeql_status_no_config(self, mock_find_root):
        """Test CodeQL status when no configuration exists."""
        from project_management_automation.tools.codeql_security import get_codeql_status

        mock_find_root.return_value = Path("/test/project")
        
        # Mock Path.exists to return False for all CodeQL files
        with patch('pathlib.Path.exists', return_value=False):
            result = get_codeql_status()
        
        assert result['configured'] is False
        assert result['workflow_exists'] is False
        assert result['config_exists'] is False
        assert result['alerts']['total'] == 0
        assert len(result['recommendations']) > 0

    @patch('project_management_automation.tools.codeql_security.find_project_root')
    def test_get_codeql_status_with_workflow(self, mock_find_root):
        """Test CodeQL status when workflow exists."""
        from project_management_automation.tools.codeql_security import get_codeql_status

        mock_find_root.return_value = Path("/test/project")
        
        def exists_side_effect(path):
            if '.github/workflows/codeql.yml' in str(path) or '.github/workflows/codeql-analysis.yml' in str(path):
                return True
            return False
        
        with patch('pathlib.Path.exists', side_effect=exists_side_effect):
            result = get_codeql_status()
        
        assert result['workflow_exists'] is True
        assert result['configured'] is True

    @patch('project_management_automation.tools.codeql_security.find_project_root')
    @patch('pathlib.Path.read_text')
    def test_get_codeql_status_parses_languages(self, mock_read_text, mock_find_root):
        """Test CodeQL status parses languages from config."""
        from project_management_automation.tools.codeql_security import get_codeql_status

        mock_find_root.return_value = Path("/test/project")
        mock_read_text.return_value = """
        languages:
          - python
          - javascript
        """
        
        def exists_side_effect(path):
            return 'codeql-config.yml' in str(path) or 'codeql.yml' in str(path)
        
        with patch('pathlib.Path.exists', side_effect=exists_side_effect):
            result = get_codeql_status()
        
        assert 'python' in result['languages'] or 'javascript' in result['languages']

    @patch('project_management_automation.tools.codeql_security.find_project_root')
    @patch('subprocess.run')
    def test_get_codeql_status_with_gh_cli(self, mock_subprocess, mock_find_root):
        """Test CodeQL status with GitHub CLI integration."""
        from project_management_automation.tools.codeql_security import get_codeql_status

        mock_find_root.return_value = Path("/test/project")
        
        # Mock gh CLI response
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps({
                'data': {
                    'repository': {
                        'vulnerabilityAlerts': {
                            'totalCount': 5,
                            'nodes': []
                        }
                    }
                }
            })
        )
        
        with patch('pathlib.Path.exists', return_value=True):
            result = get_codeql_status()
        
        # Should attempt to fetch alerts if gh CLI available
        mock_subprocess.assert_called()

    @patch('project_management_automation.tools.codeql_security.find_project_root')
    def test_get_codeql_status_error_handling(self, mock_find_root):
        """Test CodeQL status handles errors gracefully."""
        from project_management_automation.tools.codeql_security import get_codeql_status

        mock_find_root.side_effect = Exception("Project root not found")
        
        # Should not raise exception
        result = get_codeql_status()
        
        assert isinstance(result, dict)
        assert 'configured' in result

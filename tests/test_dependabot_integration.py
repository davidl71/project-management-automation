"""
Unit Tests for Dependabot Integration Tool

Tests for dependabot_integration.py module (0% coverage → target: 80%+).
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestDependabotIntegration:
    """Tests for Dependabot integration."""

    @patch('subprocess.run')
    def test_fetch_dependabot_alerts_success(self, mock_subprocess):
        """Test successful Dependabot alerts fetch."""
        from project_management_automation.tools.dependabot_integration import fetch_dependabot_alerts

        # Mock gh CLI JSONL response (one alert per line)
        mock_response = json.dumps({
            'package': 'requests',
            'severity': 'HIGH',
            'cve': 'CVE-2023-12345',
            'state': 'OPEN',
            'ecosystem': 'python'
        })
        
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=mock_response,
            stderr=""
        )
        
        result = fetch_dependabot_alerts(repo="test/repo", state="open")
        
        assert result['success'] is True
        assert result['total_alerts'] == 1
        assert len(result['alerts']) == 1
        assert result['by_severity']['high'] == 1
        mock_subprocess.assert_called()

    @patch('subprocess.run')
    def test_fetch_dependabot_alerts_no_gh_cli(self, mock_subprocess):
        """Test Dependabot alerts when gh CLI not available."""
        from project_management_automation.tools.dependabot_integration import fetch_dependabot_alerts

        mock_subprocess.side_effect = FileNotFoundError("gh: command not found")
        
        result = fetch_dependabot_alerts(repo="test/repo")
        
        assert result['success'] is False
        assert 'gh CLI' in result.get('error', '').lower() or 'not found' in result.get('error', '').lower()
        assert 'hint' in result

    @patch('subprocess.run')
    def test_fetch_dependabot_alerts_api_error(self, mock_subprocess):
        """Test Dependabot alerts handles API errors."""
        from project_management_automation.tools.dependabot_integration import fetch_dependabot_alerts

        mock_subprocess.return_value = Mock(
            returncode=1,
            stderr="API rate limit exceeded"
        )
        
        result = fetch_dependabot_alerts(repo="test/repo")
        
        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.tools.dependabot_integration.fetch_dependabot_alerts')
    def test_get_unified_security_report(self, mock_fetch_alerts):
        """Test unified security report generation."""
        from project_management_automation.tools.dependabot_integration import get_unified_security_report

        mock_fetch_alerts.return_value = {
            'success': True,
            'total_alerts': 3,
            'by_severity': {'high': 2, 'medium': 1, 'critical': 0, 'low': 0},
            'alerts': [
                {
                    'package': 'requests',
                    'severity': 'HIGH',
                    'cve': 'CVE-2023-12345',
                    'state': 'OPEN',
                    'ecosystem': 'python'
                }
            ]
        }
        
        result = get_unified_security_report(repo="test/repo", include_dismissed=False)
        
        assert 'total_vulnerabilities' in result
        assert 'by_severity' in result
        assert 'alerts' in result
        assert result['total_vulnerabilities'] == 3

    def test_security_vulnerability_dataclass(self):
        """Test SecurityVulnerability dataclass."""
        from project_management_automation.tools.dependabot_integration import SecurityVulnerability

        vuln = SecurityVulnerability(
            package="requests",
            severity="high",
            cve="CVE-2023-12345",
            source="dependabot",
            state="open",
            ecosystem="python",
            description="Test vulnerability",
            fix_available=True,
            fixed_version="2.31.0"
        )
        
        assert vuln.package == "requests"
        assert vuln.severity == "high"
        assert vuln.cve == "CVE-2023-12345"
        assert vuln.fix_available is True

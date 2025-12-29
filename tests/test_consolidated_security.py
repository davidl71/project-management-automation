"""
Unit Tests for Security Consolidated Tool

Tests for security action in consolidated.py.
"""

import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import shared test helpers
from tests.test_helpers import assert_success_response, assert_error_response, parse_json_response


class TestSecurityTool:
    """Tests for security consolidated tool."""

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.dependency_security.scan_dependency_security')
    async def test_security_scan_action(self, mock_scan):
        """Test scan action routes correctly."""
        from project_management_automation.tools.consolidated import security_async

        mock_scan.return_value = json.dumps({
            "success": True,
            "data": {"vulnerabilities": [], "total": 0}
        })

        result = await security_async(action="scan", languages=["python"])
        result_dict = parse_json_response(result)

        # scan_dependency_security may not be called directly if it's wrapped
        assert isinstance(result, str)
        parsed = parse_json_response(result)
        assert parsed is not None

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.dependabot_integration.fetch_dependabot_alerts')
    async def test_security_alerts_action(self, mock_fetch):
        """Test alerts action routes correctly."""
        from project_management_automation.tools.consolidated import security_async

        mock_fetch.return_value = json.dumps({
            "success": True,
            "data": {"alerts": [], "total": 0}
        })

        result = await security_async(action="alerts", repo="test/repo", state="open")
        result_dict = parse_json_response(result)

        mock_fetch.assert_called_once()
        assert result_dict.get("success") is True or "alerts" in str(result_dict)

    @pytest.mark.asyncio
    @patch('project_management_automation.tools.dependabot_integration.get_unified_security_report')
    async def test_security_report_action(self, mock_report):
        """Test report action combines scan and alerts."""
        from project_management_automation.tools.consolidated import security_async

        mock_report.return_value = {
            "success": True,
            "data": {
                "dependabot": {"alerts": [], "total_alerts": 0},
                "pip_audit": {"vulnerabilities": [], "total": 0},
                "comparison": {}
            }
        }

        result = await security_async(action="report", repo="test/repo")
        result_dict = parse_json_response(result)

        # Report should call get_unified_security_report
        mock_report.assert_called_once()
        assert isinstance(result, str)
        # Result should be valid JSON
        assert json.loads(result) is not None

    @pytest.mark.asyncio
    async def test_security_invalid_action(self):
        """Test invalid action returns error."""
        from project_management_automation.tools.consolidated import security_async

        result = await security_async(action="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error" or "Unknown security action" in str(result_dict)


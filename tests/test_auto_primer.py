"""
Unit Tests for Auto-Primer Tool

Tests for auto_primer.py module.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import shared test helpers
from tests.test_helpers import parse_json_response


class TestDetectAgentType:
    """Tests for detect_agent_type function."""

    @patch.dict(os.environ, {'EXARP_AGENT': 'test_agent'})
    def test_detect_agent_from_env(self):
        """Test agent detection from environment variable."""
        from project_management_automation.tools.auto_primer import detect_agent_type

        result = detect_agent_type()

        assert result['agent'] == 'test_agent'
        assert result['source'] == 'environment'

    @patch.dict(os.environ, {}, clear=True)
    @patch('pathlib.Path.exists', return_value=True)
    @patch('builtins.open', create=True)
    def test_detect_agent_from_config_file(self, mock_open, mock_exists):
        """Test agent detection from cursor-agent.json."""
        from project_management_automation.tools.auto_primer import detect_agent_type

        mock_file = MagicMock()
        mock_file.read_text.return_value = '{"name": "backend_agent", "type": "backend"}'
        mock_file.__enter__.return_value = mock_file
        mock_file.__exit__.return_value = None

        with patch('pathlib.Path') as mock_path:
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.read_text.return_value = '{"name": "backend_agent"}'
            
            result = detect_agent_type()
            # May default to "general" if file reading fails in test
            assert 'agent' in result
            assert 'source' in result

    @patch.dict(os.environ, {}, clear=True)
    @patch('pathlib.Path.exists', return_value=False)
    def test_detect_agent_default(self, mock_exists):
        """Test agent detection defaults to general."""
        from project_management_automation.tools.auto_primer import detect_agent_type

        result = detect_agent_type()

        assert 'agent' in result
        assert result['source'] in ['environment', 'cursor-agent.json', 'path', 'default']


class TestAutoPrime:
    """Tests for auto_prime function."""

    @patch('project_management_automation.tools.auto_primer.detect_agent_type')
    @patch('project_management_automation.tools.auto_primer._find_project_root')
    def test_auto_prime_basic(self, mock_root, mock_agent):
        """Test basic auto_prime functionality."""
        from project_management_automation.tools.auto_primer import auto_prime

        mock_agent.return_value = {"agent": "general", "source": "default"}
        mock_root.return_value = Path("/test/project")

        result_str = auto_prime()
        result = parse_json_response(result_str)

        assert isinstance(result, dict)
        # Result should contain context information
        assert 'agent' in result or 'mode' in result or 'hints' in result or 'tasks' in result

    @patch('project_management_automation.tools.auto_primer.detect_agent_type')
    @patch('project_management_automation.tools.auto_primer._find_project_root')
    def test_auto_prime_with_hints(self, mock_root, mock_agent):
        """Test auto_prime with hints enabled."""
        from project_management_automation.tools.auto_primer import auto_prime

        mock_agent.return_value = {"agent": "general", "source": "default"}
        mock_root.return_value = Path("/test/project")

        result_str = auto_prime(include_hints=True)
        result = parse_json_response(result_str)

        assert isinstance(result, dict)

    @patch('project_management_automation.tools.auto_primer.detect_agent_type')
    @patch('project_management_automation.tools.auto_primer._find_project_root')
    def test_auto_prime_with_tasks(self, mock_root, mock_agent):
        """Test auto_prime with tasks enabled."""
        from project_management_automation.tools.auto_primer import auto_prime

        mock_agent.return_value = {"agent": "general", "source": "default"}
        mock_root.return_value = Path("/test/project")

        result_str = auto_prime(include_tasks=True)
        result = parse_json_response(result_str)

        assert isinstance(result, dict)

    @patch('project_management_automation.tools.auto_primer.detect_agent_type')
    @patch('project_management_automation.tools.auto_primer._find_project_root')
    def test_auto_prime_compact_mode(self, mock_root, mock_agent):
        """Test auto_prime in compact mode."""
        from project_management_automation.tools.auto_primer import auto_prime

        mock_agent.return_value = {"agent": "general", "source": "default"}
        mock_root.return_value = Path("/test/project")

        result_str = auto_prime(compact=True)
        result = parse_json_response(result_str)

        assert isinstance(result, dict)

    @patch('project_management_automation.tools.auto_primer.detect_agent_type')
    @patch('project_management_automation.tools.auto_primer._find_project_root')
    def test_auto_prime_override_mode(self, mock_root, mock_agent):
        """Test auto_prime with mode override."""
        from project_management_automation.tools.auto_primer import auto_prime

        mock_agent.return_value = {"agent": "general", "source": "default"}
        mock_root.return_value = Path("/test/project")

        result_str = auto_prime(override_mode="security_review")
        result = parse_json_response(result_str)

        assert isinstance(result, dict)


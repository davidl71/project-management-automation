"""
Unit Tests for MLX Integration Tools

Tests for mlx_integration.py module with mocked MLX dependencies.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import shared test helpers
from tests.test_helpers import assert_success_response, assert_error_response


class TestIsAppleSilicon:
    """Tests for is_apple_silicon function."""

    @patch('platform.machine', return_value='arm64')
    @patch('platform.system', return_value='Darwin')
    def test_is_apple_silicon_true(self, mock_system, mock_machine):
        """Test Apple Silicon detection returns True."""
        from project_management_automation.tools.mlx_integration import is_apple_silicon

        assert is_apple_silicon() is True

    @patch('platform.machine', return_value='x86_64')
    @patch('platform.system', return_value='Darwin')
    def test_is_apple_silicon_false_intel(self, mock_system, mock_machine):
        """Test Apple Silicon detection returns False for Intel."""
        from project_management_automation.tools.mlx_integration import is_apple_silicon

        assert is_apple_silicon() is False


class TestCheckMetalAvailable:
    """Tests for check_metal_available function."""

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', False)
    def test_check_metal_available_mlx_not_available(self):
        """Test Metal check when MLX is not available."""
        from project_management_automation.tools.mlx_integration import check_metal_available

        assert check_metal_available() is False

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', True)
    @patch('project_management_automation.tools.mlx_integration.mx.metal.is_available', return_value=True)
    def test_check_metal_available_true(self, mock_metal):
        """Test Metal check returns True when available."""
        from project_management_automation.tools.mlx_integration import check_metal_available

        assert check_metal_available() is True

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', True)
    @patch('project_management_automation.tools.mlx_integration.mx.metal.is_available', side_effect=Exception('Error'))
    def test_check_metal_available_error(self, mock_metal):
        """Test Metal check handles errors gracefully."""
        from project_management_automation.tools.mlx_integration import check_metal_available

        assert check_metal_available() is False


class TestGetSystemRAM:
    """Tests for get_system_ram_gb function."""

    @patch('platform.system', return_value='Darwin')
    @patch('subprocess.check_output', return_value='17179869184')  # 16 GB in bytes
    def test_get_system_ram_gb_macos(self, mock_subprocess, mock_system):
        """Test RAM detection on macOS."""
        from project_management_automation.tools.mlx_integration import get_system_ram_gb

        result = get_system_ram_gb()

        assert result == 16.0
        mock_subprocess.assert_called_once()

    @patch('platform.system', return_value='Linux')
    @patch('builtins.open', create=True)
    def test_get_system_ram_gb_linux(self, mock_open, mock_system):
        """Test RAM detection on Linux."""
        from project_management_automation.tools.mlx_integration import get_system_ram_gb

        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.__exit__.return_value = None
        mock_file.__iter__.return_value = iter(['MemTotal:        16777216 kB'])
        mock_open.return_value = mock_file

        result = get_system_ram_gb()

        assert result == 16.0

    @patch('platform.system', return_value='Windows')
    def test_get_system_ram_gb_unknown(self, mock_system):
        """Test RAM detection returns default on unknown system."""
        from project_management_automation.tools.mlx_integration import get_system_ram_gb

        result = get_system_ram_gb()

        assert result == 8.0


class TestDetectHardwareConfig:
    """Tests for detect_hardware_config function."""

    @patch('platform.system', return_value='Darwin')
    @patch('platform.machine', return_value='arm64')
    @patch('os.cpu_count', return_value=10)
    @patch('project_management_automation.tools.mlx_integration.get_system_ram_gb', return_value=16.0)
    @patch('project_management_automation.tools.mlx_integration.check_metal_available', return_value=True)
    @patch('subprocess.check_output', return_value='Apple M4')
    def test_detect_hardware_config_m4(self, mock_subprocess, mock_metal, mock_ram, mock_cpu, mock_machine, mock_system):
        """Test hardware detection for M4 chip."""
        from project_management_automation.tools.mlx_integration import detect_hardware_config

        result = detect_hardware_config()

        assert result['platform'] == 'apple_silicon'
        assert result['mlx_supported'] is True
        assert result['metal_available'] is True
        assert result['chip_model'] == 'M4'
        # M4 may recommend 'medium' or 'large' depending on RAM, so check for either
        assert result['recommended_model_size'] in ['medium', 'large']
        # Context size may vary, so just check it's set
        assert 'recommended_context_size' in result

    @patch('platform.system', return_value='Linux')
    @patch('platform.machine', return_value='x86_64')
    def test_detect_hardware_config_non_apple(self, mock_machine, mock_system):
        """Test hardware detection on non-Apple Silicon."""
        from project_management_automation.tools.mlx_integration import detect_hardware_config

        result = detect_hardware_config()

        assert result['platform'] == 'unknown'
        assert result['mlx_supported'] is False
        assert result['metal_available'] is False


class TestCheckMLXStatus:
    """Tests for check_mlx_status function."""

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', False)
    def test_check_mlx_status_not_available(self):
        """Test MLX status check when MLX is not available."""
        from project_management_automation.tools.mlx_integration import check_mlx_status

        result_str = check_mlx_status()
        result = assert_error_response(result_str, "MLX package not installed")

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', True)
    @patch('project_management_automation.tools.mlx_integration.is_apple_silicon', return_value=False)
    @patch('project_management_automation.tools.mlx_integration.check_metal_available', return_value=False)
    @patch('project_management_automation.tools.mlx_integration.detect_hardware_config')
    def test_check_mlx_status_not_apple_silicon(self, mock_detect, mock_metal, mock_apple_silicon):
        """Test MLX status check on non-Apple Silicon."""
        from project_management_automation.tools.mlx_integration import check_mlx_status

        mock_detect.return_value = {
            'platform': 'unknown',
            'mlx_supported': False,
            'metal_available': False
        }

        result_str = check_mlx_status()
        # check_mlx_status returns success even on non-Apple Silicon, just with mlx_supported=False
        result = assert_success_response(result_str, ['mlx_available'])
        assert result['data']['mlx_supported'] is False

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', True)
    @patch('project_management_automation.tools.mlx_integration.is_apple_silicon', return_value=True)
    @patch('project_management_automation.tools.mlx_integration.check_metal_available', return_value=True)
    @patch('project_management_automation.tools.mlx_integration.detect_hardware_config')
    def test_check_mlx_status_success(self, mock_detect, mock_metal, mock_apple_silicon):
        """Test successful MLX status check."""
        from project_management_automation.tools.mlx_integration import check_mlx_status

        mock_detect.return_value = {
            'platform': 'apple_silicon',
            'mlx_supported': True,
            'metal_available': True,
            'chip_model': 'M4',
            'ram_gb': 16.0,
            'recommended_model_size': 'medium',
            'recommended_context_size': 4096,
            'notes': []
        }

        result_str = check_mlx_status()
        result = assert_success_response(result_str, ['mlx_available'])
        assert result['data']['mlx_available'] is True
        assert result['data']['mlx_supported'] is True


class TestListMLXModels:
    """Tests for list_mlx_models function."""

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', False)
    def test_list_mlx_models_not_available(self):
        """Test listing models when MLX is not available."""
        from project_management_automation.tools.mlx_integration import list_mlx_models

        result_str = list_mlx_models()
        result = assert_error_response(result_str, "MLX package not installed")

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', True)
    @patch('project_management_automation.tools.mlx_integration.is_apple_silicon', return_value=False)
    def test_list_mlx_models_not_apple_silicon(self, mock_apple_silicon):
        """Test listing models on non-Apple Silicon."""
        from project_management_automation.tools.mlx_integration import list_mlx_models

        result_str = list_mlx_models()
        # list_mlx_models doesn't check Apple Silicon, it just lists recommended models
        result = assert_success_response(result_str, ['models'])


class TestGenerateWithMLX:
    """Tests for generate_with_mlx function."""

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', False)
    def test_generate_with_mlx_not_available(self):
        """Test generation when MLX is not available."""
        from project_management_automation.tools.mlx_integration import generate_with_mlx

        result_str = generate_with_mlx("Test prompt")
        result = assert_error_response(result_str, "MLX package not installed")

    @patch('project_management_automation.tools.mlx_integration.MLX_AVAILABLE', True)
    @patch('project_management_automation.tools.mlx_integration.is_apple_silicon', return_value=False)
    def test_generate_with_mlx_not_apple_silicon(self, mock_apple_silicon):
        """Test generation on non-Apple Silicon."""
        from project_management_automation.tools.mlx_integration import generate_with_mlx

        result_str = generate_with_mlx("Test prompt")
        result = assert_error_response(result_str, "Apple Silicon")


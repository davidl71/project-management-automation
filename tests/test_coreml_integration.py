"""
Unit Tests for Core ML Integration Tools

Tests for coreml_integration.py module with mocked Core ML dependencies.
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


class TestCheckCoreMLAvailability:
    """Tests for check_coreml_availability function."""

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', True)
    @patch('project_management_automation.tools.coreml_integration.is_apple_silicon', return_value=True)
    @patch('project_management_automation.tools.coreml_integration.get_chip_model', return_value='Apple M4')
    def test_check_coreml_availability_success(self, mock_chip, mock_apple_silicon):
        """Test successful Core ML availability check."""
        from project_management_automation.tools.coreml_integration import check_coreml_availability

        result = check_coreml_availability()

        assert result['coreml_available'] is True
        assert result['apple_silicon'] is True
        assert result['neural_engine_support'] is True
        assert 'M4' in result['chip_model']

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', False)
    def test_check_coreml_availability_not_installed(self):
        """Test Core ML availability check when package is not installed."""
        from project_management_automation.tools.coreml_integration import check_coreml_availability

        result = check_coreml_availability()

        assert result['coreml_available'] is False
        assert 'Install coremltools' in str(result.get('notes', []))

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', True)
    @patch('project_management_automation.tools.coreml_integration.is_apple_silicon', return_value=False)
    def test_check_coreml_availability_not_apple_silicon(self, mock_apple_silicon):
        """Test Core ML availability check on non-Apple Silicon."""
        from project_management_automation.tools.coreml_integration import check_coreml_availability

        result = check_coreml_availability()

        assert result['coreml_available'] is True
        assert result['apple_silicon'] is False
        assert 'Apple Silicon' in str(result.get('notes', []))


class TestIsAppleSilicon:
    """Tests for is_apple_silicon function."""

    @patch('platform.machine', return_value='arm64')
    @patch('platform.system', return_value='Darwin')
    def test_is_apple_silicon_true(self, mock_system, mock_machine):
        """Test Apple Silicon detection returns True."""
        from project_management_automation.tools.coreml_integration import is_apple_silicon

        assert is_apple_silicon() is True

    @patch('platform.machine', return_value='x86_64')
    @patch('platform.system', return_value='Darwin')
    def test_is_apple_silicon_false_intel(self, mock_system, mock_machine):
        """Test Apple Silicon detection returns False for Intel."""
        from project_management_automation.tools.coreml_integration import is_apple_silicon

        assert is_apple_silicon() is False

    @patch('platform.machine', return_value='arm64')
    @patch('platform.system', return_value='Linux')
    def test_is_apple_silicon_false_linux(self, mock_system, mock_machine):
        """Test Apple Silicon detection returns False for Linux."""
        from project_management_automation.tools.coreml_integration import is_apple_silicon

        assert is_apple_silicon() is False


class TestGetChipModel:
    """Tests for get_chip_model function."""

    @patch('subprocess.check_output', return_value='Apple M4')
    def test_get_chip_model_success(self, mock_subprocess):
        """Test successful chip model detection."""
        from project_management_automation.tools.coreml_integration import get_chip_model

        result = get_chip_model()

        assert result == 'Apple M4'
        mock_subprocess.assert_called_once()

    @patch('subprocess.check_output', side_effect=Exception('Command failed'))
    def test_get_chip_model_error(self, mock_subprocess):
        """Test chip model detection with error."""
        from project_management_automation.tools.coreml_integration import get_chip_model

        result = get_chip_model()

        assert result == 'Unknown'


class TestListCoreMLModels:
    """Tests for list_coreml_models function."""

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', False)
    def test_list_coreml_models_not_available(self):
        """Test listing models when Core ML is not available."""
        from project_management_automation.tools.coreml_integration import list_coreml_models

        result_str = list_coreml_models()
        result = assert_error_response(result_str, "Core ML not available")

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', True)
    @patch('project_management_automation.tools.coreml_integration.is_apple_silicon', return_value=False)
    def test_list_coreml_models_not_apple_silicon(self, mock_apple_silicon):
        """Test listing models on non-Apple Silicon."""
        from project_management_automation.tools.coreml_integration import list_coreml_models

        result_str = list_coreml_models()
        result = assert_error_response(result_str, "Apple Silicon devices")

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', True)
    @patch('project_management_automation.tools.coreml_integration.is_apple_silicon', return_value=True)
    @patch('pathlib.Path.exists', return_value=False)
    @patch('pathlib.Path.rglob', return_value=[])
    def test_list_coreml_models_no_models_found(self, mock_rglob, mock_exists, mock_apple_silicon):
        """Test listing models when no models are found."""
        from project_management_automation.tools.coreml_integration import list_coreml_models

        result_str = list_coreml_models()
        result = assert_success_response(result_str, ['models', 'count'])
        assert result['data']['count'] == 0


class TestPredictWithCoreML:
    """Tests for predict_with_coreml function."""

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', False)
    def test_predict_with_coreml_not_available(self):
        """Test prediction when Core ML is not available."""
        from project_management_automation.tools.coreml_integration import predict_with_coreml

        result_str = predict_with_coreml("test.mlmodel", {"input": "test"})
        result = assert_error_response(result_str, "Core ML not available")

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', True)
    @patch('project_management_automation.tools.coreml_integration.is_apple_silicon', return_value=False)
    def test_predict_with_coreml_not_apple_silicon(self, mock_apple_silicon):
        """Test prediction on non-Apple Silicon."""
        from project_management_automation.tools.coreml_integration import predict_with_coreml

        result_str = predict_with_coreml("test.mlmodel", {"input": "test"})
        result = assert_error_response(result_str, "Apple Silicon devices")

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', True)
    @patch('project_management_automation.tools.coreml_integration.is_apple_silicon', return_value=True)
    def test_predict_with_coreml_file_not_found(self, mock_apple_silicon):
        """Test prediction when model file is not found."""
        from project_management_automation.tools.coreml_integration import predict_with_coreml

        # Try to import coremltools, skip test if not available
        try:
            import coremltools as ct
        except ImportError:
            pytest.skip("coremltools not available")

        # Mock FileNotFoundError when loading model
        with patch.object(ct.models, 'MLModel', side_effect=FileNotFoundError("Model file not found")):
            result_str = predict_with_coreml("nonexistent.mlmodel", {"input": "test"})
            result = assert_error_response(result_str, "not found")


class TestGetCoreMLHardwareInfo:
    """Tests for get_coreml_hardware_info function."""

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', False)
    def test_get_coreml_hardware_info_not_available(self):
        """Test hardware info when Core ML is not available."""
        from project_management_automation.tools.coreml_integration import get_coreml_hardware_info

        result_str = get_coreml_hardware_info()
        result = assert_error_response(result_str, "Core ML not available")

    @patch('project_management_automation.tools.coreml_integration.CORE_ML_AVAILABLE', True)
    @patch('project_management_automation.tools.coreml_integration.check_coreml_availability')
    @patch('project_management_automation.tools.coreml_integration.is_apple_silicon', return_value=True)
    def test_get_coreml_hardware_info_success(self, mock_apple_silicon, mock_check):
        """Test successful hardware info retrieval."""
        from project_management_automation.tools.coreml_integration import get_coreml_hardware_info

        mock_check.return_value = {
            'coreml_available': True,
            'apple_silicon': True,
            'chip_model': 'Apple M4',
            'neural_engine_support': True,
            'notes': []
        }

        result_str = get_coreml_hardware_info()
        result = assert_success_response(result_str, ['coreml_available', 'apple_silicon'])
        assert result['data']['coreml_available'] is True

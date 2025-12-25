"""
Unit Tests for Ollama Integration Tools

Tests for ollama_integration.py module with mocked Ollama client.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestCheckOllamaStatus:
    """Tests for check_ollama_status function."""

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_check_ollama_status_success(self, mock_ollama_module):
        """Test successful Ollama status check."""
        from project_management_automation.tools.ollama_integration import check_ollama_status

        # Mock Ollama client and list response
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.model = "llama3.2:latest"
        mock_response = MagicMock()
        mock_response.models = [mock_model]
        mock_client.list.return_value = mock_response
        mock_ollama_module.Client.return_value = mock_client

        result_str = check_ollama_status()
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['status'] == 'running'
        assert result['data']['model_count'] == 1
        assert 'llama3.2:latest' in result['data']['models']

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_check_ollama_status_connection_error(self, mock_ollama_module):
        """Test Ollama status check with connection error."""
        from project_management_automation.tools.ollama_integration import check_ollama_status

        # Mock connection error
        mock_client = MagicMock()
        mock_client.list.side_effect = ConnectionError("Connection refused")
        mock_ollama_module.Client.return_value = mock_client

        result_str = check_ollama_status()
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'error' in result
        assert 'not running' in result['error']['message'].lower() or 'connection' in result['error']['message'].lower()

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', False)
    def test_check_ollama_status_package_not_available(self):
        """Test Ollama status check when package is not installed."""
        from project_management_automation.tools.ollama_integration import check_ollama_status

        result_str = check_ollama_status()
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not installed' in result['error']['message'].lower()

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_check_ollama_status_with_custom_host(self, mock_ollama_module):
        """Test Ollama status check with custom host."""
        from project_management_automation.tools.ollama_integration import check_ollama_status

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.models = []
        mock_client.list.return_value = mock_response
        mock_ollama_module.Client.return_value = mock_client

        result_str = check_ollama_status(host="http://remote:11434")
        result = json.loads(result_str)

        assert result['success'] is True
        mock_ollama_module.Client.assert_called_once_with(host="http://remote:11434")


class TestListOllamaModels:
    """Tests for list_ollama_models function."""

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_list_ollama_models_success(self, mock_ollama_module):
        """Test successful model listing."""
        from project_management_automation.tools.ollama_integration import list_ollama_models

        # Create mock model objects
        mock_model1 = MagicMock()
        mock_model1.model = "llama3.2:latest"
        mock_model1.size = 2000000000
        mock_model1.digest = "abc123def456"
        mock_model1.modified_at = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_model1.model_dump.return_value = {
            "model": "llama3.2:latest",
            "size": 2000000000,
            "digest": "abc123def456",
            "modified_at": mock_model1.modified_at,
        }

        mock_model2 = MagicMock()
        mock_model2.model = "codellama:7b"
        mock_model2.size = 3800000000
        mock_model2.digest = "xyz789ghi012"
        mock_model2.modified_at = datetime(2025, 1, 2, 12, 0, 0, tzinfo=timezone.utc)
        mock_model2.model_dump.return_value = {
            "model": "codellama:7b",
            "size": 3800000000,
            "digest": "xyz789ghi012",
            "modified_at": mock_model2.modified_at,
        }

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.models = [mock_model1, mock_model2]
        mock_client.list.return_value = mock_response
        mock_ollama_module.Client.return_value = mock_client

        result_str = list_ollama_models()
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['count'] == 2
        assert len(result['data']['models']) == 2
        assert result['data']['models'][0]['name'] == "llama3.2:latest"
        assert result['data']['models'][0]['size'] == 2000000000
        assert result['data']['models'][1]['name'] == "codellama:7b"

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_list_ollama_models_empty(self, mock_ollama_module):
        """Test model listing with no models."""
        from project_management_automation.tools.ollama_integration import list_ollama_models

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.models = []
        mock_client.list.return_value = mock_response
        mock_ollama_module.Client.return_value = mock_client

        result_str = list_ollama_models()
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['count'] == 0
        assert result['data']['models'] == []

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', False)
    def test_list_ollama_models_package_not_available(self):
        """Test model listing when package is not installed."""
        from project_management_automation.tools.ollama_integration import list_ollama_models

        result_str = list_ollama_models()
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not installed' in result['error']['message'].lower()


class TestGetHardwareInfo:
    """Tests for get_hardware_info function."""

    @patch('project_management_automation.tools.ollama_integration.platform.system')
    @patch('project_management_automation.tools.ollama_integration.platform.machine')
    @patch('project_management_automation.tools.ollama_integration.os.cpu_count')
    @patch('project_management_automation.tools.ollama_integration.subprocess.check_output')
    def test_get_hardware_info_apple_silicon(self, mock_check_output, mock_cpu_count, mock_machine, mock_system):
        """Test hardware info detection for Apple Silicon."""
        from project_management_automation.tools.ollama_integration import get_hardware_info

        mock_system.return_value = "Darwin"
        mock_machine.return_value = "arm64"
        mock_cpu_count.return_value = 10
        # Mock sysctl calls: first for RAM (hw.memsize), second for chip model
        # RAM detection returns text (16GB = 17179869184 bytes)
        # Chip model detection returns text
        def check_output_side_effect(*args, **kwargs):
            cmd = args[0] if args else []
            if "hw.memsize" in cmd:
                return "17179869184"  # Return as text string
            elif "machdep.cpu.brand_string" in cmd:
                return "Apple M1 Pro"  # Return chip model as text
            return ""
        mock_check_output.side_effect = check_output_side_effect

        result_str = get_hardware_info()
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['platform'] == 'apple_silicon'
        assert result['data']['architecture'] == 'arm64'
        assert result['data']['cpu_cores'] == 10
        assert result['data']['gpu_available'] is True
        assert result['data']['gpu_type'] == 'metal'
        assert result['data']['recommended_settings']['num_gpu'] is not None

    @patch('project_management_automation.tools.ollama_integration.platform.system')
    @patch('project_management_automation.tools.ollama_integration.platform.machine')
    @patch('project_management_automation.tools.ollama_integration.os.cpu_count')
    @patch('project_management_automation.tools.ollama_integration.subprocess.check_output')
    def test_get_hardware_info_intel_mac(self, mock_check_output, mock_cpu_count, mock_machine, mock_system):
        """Test hardware info detection for Intel Mac."""
        from project_management_automation.tools.ollama_integration import get_hardware_info

        mock_system.return_value = "Darwin"
        mock_machine.return_value = "x86_64"
        mock_cpu_count.return_value = 8
        # Mock RAM detection (returns text string)
        mock_check_output.return_value = "17179869184"  # 16GB RAM as text

        result_str = get_hardware_info()
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['platform'] == 'intel'
        assert result['data']['architecture'] == 'x86_64'
        assert result['data']['cpu_cores'] == 8
        assert result['data']['gpu_available'] is False
        assert result['data']['gpu_type'] is None

    @patch('project_management_automation.tools.ollama_integration.platform.system')
    @patch('project_management_automation.tools.ollama_integration.platform.machine')
    @patch('project_management_automation.tools.ollama_integration.os.cpu_count')
    @patch('project_management_automation.tools.ollama_integration.subprocess.check_output')
    def test_get_hardware_info_ram_detection_fallback(self, mock_check_output, mock_cpu_count, mock_machine, mock_system):
        """Test hardware info with RAM detection failure (should use default)."""
        from project_management_automation.tools.ollama_integration import get_hardware_info
        import subprocess

        mock_system.return_value = "Darwin"
        mock_machine.return_value = "arm64"
        mock_cpu_count.return_value = 8
        # Mock both subprocess calls to fail (RAM detection and chip model detection)
        # Use FileNotFoundError which is caught and handled gracefully
        mock_check_output.side_effect = FileNotFoundError("sysctl not found")

        result_str = get_hardware_info()
        result = json.loads(result_str)

        assert result['success'] is True
        # Should still work with default RAM value
        assert 'ram_gb' in result['data']


class TestGenerateWithOllama:
    """Tests for generate_with_ollama function."""

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    @patch('project_management_automation.tools.ollama_integration.detect_hardware_config')
    def test_generate_with_ollama_success(self, mock_detect_hw, mock_ollama_module):
        """Test successful text generation."""
        from project_management_automation.tools.ollama_integration import generate_with_ollama

        # Mock hardware detection (called internally)
        mock_detect_hw.return_value = {
            "platform": "apple_silicon",
            "cpu_cores": 10,
            "ram_gb": 16.0,
            "gpu_available": True,
            "gpu_type": "metal",
            "recommended_num_threads": 9,
            "recommended_num_gpu": 40,
            "recommended_context_size": 8192,
            "ram_optimizations": {"recommended_context_size": 8192, "enable_flash_attention": True},
        }

        # Mock Ollama client
        mock_client = MagicMock()
        mock_response = {"response": "Generated text response"}
        mock_client.generate.return_value = mock_response
        mock_ollama_module.Client.return_value = mock_client

        result_str = generate_with_ollama(
            prompt="Test prompt",
            model="llama3.2",
        )
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['response'] == "Generated text response"
        assert result['data']['model'] == "llama3.2"
        # Verify hardware optimizations were applied
        assert result['data']['performance_options']['num_gpu'] == 40
        assert result['data']['performance_options']['num_threads'] == 9

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_generate_with_ollama_model_not_found(self, mock_ollama_module):
        """Test generation with non-existent model."""
        from project_management_automation.tools.ollama_integration import generate_with_ollama

        mock_client = MagicMock()
        mock_client.generate.side_effect = Exception("model not found")
        mock_ollama_module.Client.return_value = mock_client

        result_str = generate_with_ollama(
            prompt="Test",
            model="nonexistent-model",
        )
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    @patch('project_management_automation.tools.ollama_integration.detect_hardware_config')
    def test_generate_with_ollama_streaming(self, mock_detect_hw, mock_ollama_module):
        """Test generation with streaming enabled."""
        from project_management_automation.tools.ollama_integration import generate_with_ollama

        mock_detect_hw.return_value = {
            "platform": "linux",
            "cpu_cores": 4,
            "ram_gb": 8.0,
            "gpu_available": False,
            "gpu_type": None,
            "recommended_num_threads": 4,
            "recommended_num_gpu": None,
            "recommended_context_size": 4096,
            "ram_optimizations": {},
        }

        # Mock streaming response - client.generate() with stream=True returns an iterator
        mock_client = MagicMock()
        mock_chunks = [
            {"response": "Hello "},
            {"response": "world"},
        ]
        # When stream=True, generate() returns an iterator that yields chunks
        mock_client.generate.return_value = iter(mock_chunks)
        mock_ollama_module.Client.return_value = mock_client

        result_str = generate_with_ollama(
            prompt="Hello",
            model="llama3.2",
            stream=True,
        )
        result = json.loads(result_str)

        # Verify streaming was used and response was concatenated
        assert result['success'] is True
        assert result['data']['response'] == "Hello world"
        # Verify generate was called with stream=True
        mock_client.generate.assert_called_once()
        call_kwargs = mock_client.generate.call_args[1]
        assert call_kwargs.get('stream') is True

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', False)
    def test_generate_with_ollama_package_not_available(self):
        """Test generation when package is not installed."""
        from project_management_automation.tools.ollama_integration import generate_with_ollama

        result_str = generate_with_ollama(prompt="Test", model="llama3.2")
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not installed' in result['error']['message'].lower()


class TestPullOllamaModel:
    """Tests for pull_ollama_model function."""

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_pull_ollama_model_success(self, mock_ollama_module):
        """Test successful model pull."""
        from project_management_automation.tools.ollama_integration import pull_ollama_model

        mock_client = MagicMock()
        mock_client.pull.return_value = {"status": "success"}
        mock_ollama_module.Client.return_value = mock_client

        result_str = pull_ollama_model(model="llama3.2")
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['model'] == "llama3.2"
        mock_client.pull.assert_called_once_with("llama3.2")

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_integration.ollama')
    def test_pull_ollama_model_connection_error(self, mock_ollama_module):
        """Test model pull with connection error."""
        from project_management_automation.tools.ollama_integration import pull_ollama_model

        mock_client = MagicMock()
        mock_client.pull.side_effect = ConnectionError("Connection refused")
        mock_ollama_module.Client.return_value = mock_client

        result_str = pull_ollama_model(model="llama3.2")
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'error' in result

    @patch('project_management_automation.tools.ollama_integration.OLLAMA_AVAILABLE', False)
    def test_pull_ollama_model_package_not_available(self):
        """Test model pull when package is not installed."""
        from project_management_automation.tools.ollama_integration import pull_ollama_model

        result_str = pull_ollama_model(model="llama3.2")
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not installed' in result['error']['message'].lower()


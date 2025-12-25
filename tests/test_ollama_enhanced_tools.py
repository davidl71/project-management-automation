"""
Unit Tests for Ollama Enhanced Tools

Tests for ollama_enhanced_tools.py module with mocked Ollama calls.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestGenerateCodeDocumentation:
    """Tests for generate_code_documentation function."""

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.generate_with_ollama')
    @patch('project_management_automation.tools.ollama_enhanced_tools.Path')
    def test_generate_code_documentation_success(self, mock_path_class, mock_generate_with_ollama):
        """Test successful code documentation generation."""
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation
        from pathlib import Path

        # Mock Path instance
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = "def add(a, b):\n    return a + b"
        mock_path.absolute.return_value = Path("/absolute/test.py")
        mock_path_class.return_value = mock_path

        # Mock Ollama generation
        mock_response = {
            "success": True,
            "data": {
                "response": "def add(a, b):\n    \"\"\"Add two numbers.\"\"\"\n    return a + b"
            }
        }
        mock_generate_with_ollama.return_value = json.dumps(mock_response)

        result_str = generate_code_documentation("test.py", style="google", model="codellama")
        result = json.loads(result_str)

        assert result['success'] is True
        assert 'documentation' in result['data']
        assert 'original_length' in result['data']
        assert 'documented_length' in result['data']
        mock_generate_with_ollama.assert_called_once()

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.Path')
    def test_generate_code_documentation_file_not_found(self, mock_path_class):
        """Test documentation generation with missing file."""
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation
        from pathlib import Path

        # Mock Path instance
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False
        mock_path_class.return_value = mock_path

        result_str = generate_code_documentation("nonexistent.py")
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not found' in result['error']['message'].lower()

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', False)
    def test_generate_code_documentation_package_not_available(self):
        """Test documentation generation when Ollama package is not available."""
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation

        result_str = generate_code_documentation("test.py")
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not available' in result['error']['message'].lower()

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.generate_with_ollama')
    @patch('project_management_automation.tools.ollama_enhanced_tools.Path')
    def test_generate_code_documentation_with_output_path(self, mock_path_class, mock_generate_with_ollama):
        """Test documentation generation with output file."""
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation
        from pathlib import Path

        # Mock input Path instance
        mock_input_path = MagicMock(spec=Path)
        mock_input_path.exists.return_value = True
        mock_input_path.read_text.return_value = "def test(): pass"
        mock_input_path.absolute.return_value = Path("/input/test.py")
        
        # Mock output Path instance
        mock_output_path = MagicMock(spec=Path)
        mock_output_path.absolute.return_value = Path("/output/test.py")
        
        # Make Path() return appropriate instance based on argument
        def path_side_effect(path_str):
            if "output" in str(path_str):
                return mock_output_path
            return mock_input_path
        
        mock_path_class.side_effect = path_side_effect

        mock_response = {
            "success": True,
            "data": {"response": "def test():\n    \"\"\"Test function.\"\"\"\n    pass"}
        }
        mock_generate_with_ollama.return_value = json.dumps(mock_response)

        result_str = generate_code_documentation("test.py", output_path="output.py")
        result = json.loads(result_str)

        assert result['success'] is True
        assert 'output_path' in result['data']
        # Verify output file was written
        mock_output_path.write_text.assert_called_once()


class TestAnalyzeCodeQuality:
    """Tests for analyze_code_quality function."""

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.generate_with_ollama')
    @patch('project_management_automation.tools.ollama_enhanced_tools.Path')
    def test_analyze_code_quality_success(self, mock_path_class, mock_generate_with_ollama):
        """Test successful code quality analysis."""
        from project_management_automation.tools.ollama_enhanced_tools import analyze_code_quality
        from pathlib import Path

        # Mock Path instance
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = "def bad_code():\n    x = 1\n    return x"
        mock_path.absolute.return_value = Path("/absolute/test.py")
        mock_path_class.return_value = mock_path

        # Mock LLM response with JSON
        mock_llm_response = {
            "quality_score": 75,
            "code_smells": ["Unused variable"],
            "performance_issues": [],
            "security_concerns": [],
            "best_practice_violations": [],
            "maintainability": "good",
            "suggestions": ["Use descriptive variable names"]
        }

        mock_response = {
            "success": True,
            "data": {"response": json.dumps(mock_llm_response)}
        }
        mock_generate_with_ollama.return_value = json.dumps(mock_response)

        result_str = analyze_code_quality("test.py", include_suggestions=True)
        result = json.loads(result_str)

        assert result['success'] is True
        assert 'analysis' in result['data']
        # The analysis should contain the parsed JSON
        analysis = result['data']['analysis']
        assert analysis.get('quality_score') == 75

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.generate_with_ollama')
    @patch('project_management_automation.tools.ollama_enhanced_tools.Path')
    def test_analyze_code_quality_with_markdown_json(self, mock_path_class, mock_generate_with_ollama):
        """Test code quality analysis with markdown-wrapped JSON response."""
        from project_management_automation.tools.ollama_enhanced_tools import analyze_code_quality
        from pathlib import Path

        # Mock Path instance
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = "def test(): pass"
        mock_path.absolute.return_value = Path("/absolute/test.py")
        mock_path_class.return_value = mock_path

        # Mock LLM response wrapped in markdown code block
        mock_json = {"quality_score": 80, "code_smells": []}
        mock_llm_response_text = f"```json\n{json.dumps(mock_json)}\n```"

        mock_response = {
            "success": True,
            "data": {"response": mock_llm_response_text}
        }
        mock_generate_with_ollama.return_value = json.dumps(mock_response)

        result_str = analyze_code_quality("test.py")
        result = json.loads(result_str)

        assert result['success'] is True
        analysis = result['data']['analysis']
        assert analysis.get('quality_score') == 80

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.Path')
    def test_analyze_code_quality_file_not_found(self, mock_path_class):
        """Test code quality analysis with missing file."""
        from project_management_automation.tools.ollama_enhanced_tools import analyze_code_quality
        from pathlib import Path

        # Mock Path instance
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False
        mock_path_class.return_value = mock_path

        result_str = analyze_code_quality("nonexistent.py")
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not found' in result['error']['message'].lower()


class TestEnhanceContextSummary:
    """Tests for enhance_context_summary function."""

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.generate_with_ollama')
    def test_enhance_context_summary_with_dict(self, mock_generate_with_ollama):
        """Test context summary enhancement with dict input."""
        from project_management_automation.tools.ollama_enhanced_tools import enhance_context_summary

        input_data = {"tasks": 10, "completed": 5, "status": "in_progress"}

        mock_response = {
            "success": True,
            "data": {"response": "Summary: 10 tasks, 5 completed, in progress"}
        }
        mock_generate_with_ollama.return_value = json.dumps(mock_response)

        result_str = enhance_context_summary(input_data, level="brief")
        result = json.loads(result_str)

        assert result['success'] is True
        assert 'summary' in result['data']
        assert result['data']['level'] == "brief"
        mock_generate_with_ollama.assert_called_once()

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.generate_with_ollama')
    def test_enhance_context_summary_with_list(self, mock_generate_with_ollama):
        """Test context summary enhancement with list input."""
        from project_management_automation.tools.ollama_enhanced_tools import enhance_context_summary

        input_data = ["task1", "task2", "task3"]

        mock_response = {
            "success": True,
            "data": {"response": "Summary: 3 items"}
        }
        mock_generate_with_ollama.return_value = json.dumps(mock_response)

        result_str = enhance_context_summary(input_data, level="detailed")
        result = json.loads(result_str)

        assert result['success'] is True
        assert result['data']['level'] == "detailed"

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', True)
    @patch('project_management_automation.tools.ollama_enhanced_tools.generate_with_ollama')
    def test_enhance_context_summary_with_string(self, mock_generate_with_ollama):
        """Test context summary enhancement with string input."""
        from project_management_automation.tools.ollama_enhanced_tools import enhance_context_summary

        input_data = "Raw text data to summarize"

        mock_response = {
            "success": True,
            "data": {"response": "Summarized text"}
        }
        mock_generate_with_ollama.return_value = json.dumps(mock_response)

        result_str = enhance_context_summary(input_data)
        result = json.loads(result_str)

        assert result['success'] is True

    @patch('project_management_automation.tools.ollama_enhanced_tools.OLLAMA_AVAILABLE', False)
    def test_enhance_context_summary_package_not_available(self):
        """Test context summary when Ollama package is not available."""
        from project_management_automation.tools.ollama_enhanced_tools import enhance_context_summary

        result_str = enhance_context_summary({"data": "test"})
        result = json.loads(result_str)

        assert result['success'] is False
        assert 'not available' in result['error']['message'].lower()


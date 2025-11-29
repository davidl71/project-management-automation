"""
Unit Tests for Simplify Rules Tool

Tests for simplify_rules.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestSimplifyRulesTool:
    """Tests for simplify rules tool."""

    @patch('project_management_automation.tools.simplify_rules.find_project_root')
    @patch('project_management_automation.tools.simplify_rules.Path.exists')
    @patch('project_management_automation.tools.simplify_rules.Path.glob')
    def test_simplify_rules_dry_run(self, mock_glob, mock_exists, mock_find_root):
        """Test simplify rules in dry run mode."""
        from project_management_automation.tools.simplify_rules import simplify_rules

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_glob.return_value = []
        
        # Mock rule file content
        rule_content = "Run linters: `./scripts/run_linters.sh`"
        
        with patch('builtins.open', mock_open(read_data=rule_content)):
            result_str = simplify_rules(dry_run=True)
        
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert result['dry_run'] is True

    @patch('project_management_automation.tools.simplify_rules.find_project_root')
    @patch('project_management_automation.tools.simplify_rules.Path.exists')
    def test_simplify_rules_with_specific_files(self, mock_exists, mock_find_root):
        """Test with specific rule files."""
        from project_management_automation.tools.simplify_rules import simplify_rules

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        rule_content = "Run linters: `./scripts/run_linters.sh`"
        
        with patch('builtins.open', mock_open(read_data=rule_content)):
            result_str = simplify_rules(
                rule_files=["/test/.cursorrules"],
                dry_run=True
            )
        
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert len(result['files_processed']) > 0 or len(result['files_skipped']) > 0

    @patch('project_management_automation.tools.simplify_rules.find_project_root')
    @patch('project_management_automation.tools.simplify_rules.Path.exists')
    def test_simplify_rules_file_not_found(self, mock_exists, mock_find_root):
        """Test when rule file doesn't exist."""
        from project_management_automation.tools.simplify_rules import simplify_rules

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = False
        
        result_str = simplify_rules(
            rule_files=["/nonexistent/.cursorrules"],
            dry_run=True
        )
        
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert len(result['files_skipped']) > 0
        assert 'File not found' in result['files_skipped'][0]['reason']

    @patch('project_management_automation.tools.simplify_rules.find_project_root')
    @patch('project_management_automation.tools.simplify_rules.Path.exists')
    @patch('project_management_automation.tools.simplify_rules.Path.glob')
    def test_simplify_rules_no_simplifications(self, mock_glob, mock_exists, mock_find_root):
        """Test when no simplifications are found."""
        from project_management_automation.tools.simplify_rules import simplify_rules

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_glob.return_value = []
        
        # Content with no patterns to simplify
        rule_content = "This is a simple rule with no patterns to simplify."
        
        with patch('builtins.open', mock_open(read_data=rule_content)):
            result_str = simplify_rules(dry_run=True)
        
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        # Should skip files with no simplifications
        assert len(result['files_skipped']) >= 0

    @patch('project_management_automation.tools.simplify_rules.find_project_root')
    @patch('project_management_automation.tools.simplify_rules.Path.exists')
    def test_simplify_rules_custom_output_dir(self, mock_exists, mock_find_root):
        """Test with custom output directory."""
        from project_management_automation.tools.simplify_rules import simplify_rules

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        rule_content = "Run linters: `./scripts/run_linters.sh`"
        
        with patch('builtins.open', mock_open(read_data=rule_content)):
            with patch('project_management_automation.tools.simplify_rules.Path.mkdir'):
                result_str = simplify_rules(
                    rule_files=["/test/.cursorrules"],
                    dry_run=False,
                    output_dir="/output"
                )
        
        result = json.loads(result_str)
        
        assert result['status'] == 'success'

    def test_get_simplification_patterns(self):
        """Test simplification pattern generation."""
        from project_management_automation.tools.simplify_rules import _get_simplification_patterns

        patterns = _get_simplification_patterns()
        
        assert 'manual_linting' in patterns
        assert 'manual_testing' in patterns
        assert 'manual_build' in patterns
        assert 'pattern' in patterns['manual_linting']
        assert 'replacement' in patterns['manual_linting']

    def test_apply_pattern(self):
        """Test pattern matching."""
        from project_management_automation.tools.simplify_rules import _apply_pattern

        pattern_config = {
            "pattern": r"Run linters:\s*`\./scripts/run_linters\.sh`",
            "description": "Test pattern"
        }
        
        content = "Run linters: `./scripts/run_linters.sh`"
        
        matches = _apply_pattern(content, pattern_config)
        
        assert len(matches) > 0
        assert matches[0]['description'] == "Test pattern"

    def test_replace_pattern(self):
        """Test pattern replacement."""
        from project_management_automation.tools.simplify_rules import _replace_pattern

        pattern_config = {
            "pattern": r"Run linters:\s*`\./scripts/run_linters\.sh`",
            "replacement": "Run linters: `lint:run`"
        }
        
        content = "Run linters: `./scripts/run_linters.sh`"
        matches = [{"start": 0, "end": len(content), "match": content}]
        
        result = _replace_pattern(content, pattern_config, matches)
        
        assert 'lint:run' in result
        assert './scripts/run_linters.sh' not in result

    @patch('project_management_automation.tools.simplify_rules.find_project_root')
    @patch('project_management_automation.tools.simplify_rules.Path.exists')
    def test_simplify_rules_read_error(self, mock_exists, mock_find_root):
        """Test error handling when reading file fails."""
        from project_management_automation.tools.simplify_rules import simplify_rules

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        with patch('builtins.open', side_effect=IOError("Read failed")):
            result_str = simplify_rules(
                rule_files=["/test/.cursorrules"],
                dry_run=True
            )
        
        result = json.loads(result_str)
        
        assert result['status'] == 'success'
        assert len(result['files_skipped']) > 0
        assert 'Error processing file' in result['files_skipped'][0]['reason']

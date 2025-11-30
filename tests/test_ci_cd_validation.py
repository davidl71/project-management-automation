"""
Unit Tests for CI/CD Validation Tool

Tests for ci_cd_validation.py module.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import sys
import yaml

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestCICDValidationTool:
    """Tests for CI/CD validation tool."""

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.tools.ci_cd_validation.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_validate_ci_cd_workflow_success(self, mock_file, mock_exists, mock_find_root):
        """Test successful workflow validation."""
        from project_management_automation.tools.ci_cd_validation import validate_ci_cd_workflow

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        # Mock valid workflow YAML
        workflow_yaml = {
            'name': 'CI',
            'on': ['push', 'pull_request'],
            'jobs': {
                'test': {
                    'runs-on': 'ubuntu-latest',
                    'steps': []
                }
            }
        }
        mock_file.return_value.read.return_value = yaml.dump(workflow_yaml)
        
        result_str = validate_ci_cd_workflow(workflow_path=".github/workflows/ci.yml")
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['workflow_valid'] is True
        assert result['data']['overall_status'] in ['valid', 'issues_found']

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.tools.ci_cd_validation.Path.exists')
    def test_validate_ci_cd_workflow_file_not_found(self, mock_exists, mock_find_root):
        """Test when workflow file doesn't exist."""
        from project_management_automation.tools.ci_cd_validation import validate_ci_cd_workflow

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = False
        
        result_str = validate_ci_cd_workflow(workflow_path="/nonexistent/workflow.yml")
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['workflow_valid'] is False
        assert result['data']['overall_status'] == 'failed'

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.tools.ci_cd_validation.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_validate_ci_cd_workflow_invalid_yaml(self, mock_file, mock_exists, mock_find_root):
        """Test with invalid YAML syntax."""
        from project_management_automation.tools.ci_cd_validation import validate_ci_cd_workflow

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = "invalid: yaml: [unclosed"
        
        result_str = validate_ci_cd_workflow()
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert result['data']['workflow_valid'] is False
        assert len(result['data']['issues']) > 0

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.tools.ci_cd_validation.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_validate_ci_cd_workflow_without_runners(self, mock_file, mock_exists, mock_find_root):
        """Test validation without runner checks."""
        from project_management_automation.tools.ci_cd_validation import validate_ci_cd_workflow

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        workflow_yaml = {'name': 'CI', 'on': ['push'], 'jobs': {}}
        mock_file.return_value.read.return_value = yaml.dump(workflow_yaml)
        
        result_str = validate_ci_cd_workflow(check_runners=False)
        result = json.loads(result_str)
        
        assert result['success'] is True
        # Runner config should not be checked
        assert 'runner_config_valid' not in result['data'] or result['data'].get('runner_config_valid') is None

    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.tools.ci_cd_validation.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_validate_ci_cd_workflow_custom_output_path(self, mock_file, mock_exists, mock_find_root):
        """Test with custom output path."""
        from project_management_automation.tools.ci_cd_validation import validate_ci_cd_workflow

        mock_find_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        workflow_yaml = {'name': 'CI', 'on': ['push'], 'jobs': {}}
        mock_file.return_value.read.return_value = yaml.dump(workflow_yaml)
        
        result_str = validate_ci_cd_workflow(output_path="/custom/report.md")
        result = json.loads(result_str)
        
        assert result['success'] is True
        assert '/custom/report.md' in result['data']['report_path']

    @patch('project_management_automation.utils.find_project_root')
    def test_validate_ci_cd_workflow_error(self, mock_find_root):
        """Test error handling."""
        from project_management_automation.tools.ci_cd_validation import validate_ci_cd_workflow

        mock_find_root.side_effect = Exception("Project root error")
        
        result_str = validate_ci_cd_workflow()
        result = json.loads(result_str)
        
        assert result['success'] is False
        assert 'error' in result

    def test_validate_runner_configs(self):
        """Test runner config validation."""
        from project_management_automation.tools.ci_cd_validation import _validate_runner_configs

        # Valid runner config
        workflow = {
            'jobs': {
                'test': {
                    'runs-on': 'ubuntu-latest'
                }
            }
        }
        result = _validate_runner_configs(workflow)
        assert result['runner_config_valid'] is True

        # Invalid: self-hosted without labels
        workflow = {
            'jobs': {
                'test': {
                    'runs-on': 'self-hosted'
                }
            }
        }
        result = _validate_runner_configs(workflow)
        assert result['runner_config_valid'] is False
        assert len(result['runner_issues']) > 0

    def test_validate_job_dependencies(self):
        """Test job dependency validation."""
        from project_management_automation.tools.ci_cd_validation import _validate_job_dependencies

        # Valid dependencies
        workflow = {
            'jobs': {
                'build': {},
                'test': {'needs': ['build']}
            }
        }
        result = _validate_job_dependencies(workflow)
        assert result['job_dependencies_valid'] is True

        # Invalid: depends on non-existent job
        workflow = {
            'jobs': {
                'test': {'needs': ['nonexistent']}
            }
        }
        result = _validate_job_dependencies(workflow)
        assert result['job_dependencies_valid'] is False
        assert len(result['job_dependency_issues']) > 0

    def test_validate_matrix_builds(self):
        """Test matrix build validation."""
        from project_management_automation.tools.ci_cd_validation import _validate_matrix_builds

        # Valid matrix
        workflow = {
            'jobs': {
                'test': {
                    'strategy': {
                        'matrix': {'os': ['ubuntu', 'windows']}
                    }
                }
            }
        }
        result = _validate_matrix_builds(workflow)
        assert result['matrix_builds_valid'] is True

        # Invalid: empty matrix
        workflow = {
            'jobs': {
                'test': {
                    'strategy': {
                        'matrix': {}
                    }
                }
            }
        }
        result = _validate_matrix_builds(workflow)
        assert result['matrix_builds_valid'] is False

    def test_validate_triggers(self):
        """Test trigger validation."""
        from project_management_automation.tools.ci_cd_validation import _validate_triggers

        # Valid triggers
        workflow = {'on': ['push', 'pull_request']}
        result = _validate_triggers(workflow)
        assert result['triggers_valid'] is True

        # Invalid: no triggers
        workflow = {}
        result = _validate_triggers(workflow)
        assert result['triggers_valid'] is False

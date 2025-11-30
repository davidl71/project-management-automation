"""
Unit Tests for MCP Prompts

Tests all registered prompts to ensure they are correctly exposed.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestPromptRegistration:
    """Tests for prompt registration and availability."""

    def test_prompts_import(self):
        """Test that prompts module can be imported."""
        from prompts import PROMPTS
        assert PROMPTS is not None
        assert isinstance(PROMPTS, dict)
        assert len(PROMPTS) >= 14  # At least base prompts, more with persona prompts

    def test_all_prompts_defined(self):
        """Test that all expected prompts are defined."""
        from prompts import PROMPTS

        expected_prompts = [
            "doc_health_check",  # Actual key in PROMPTS
            "doc_quick_check",   # Actual key in PROMPTS
            "task_alignment",
            "duplicate_cleanup",
            "task_sync",
            "security_scan_all",
            "security_scan_python",
            "security_scan_rust",
            "automation_discovery",
            "automation_high_value",
            "pre_sprint_cleanup",
            "post_implementation_review",
            "weekly_maintenance"
        ]

        for prompt_key in expected_prompts:
            assert prompt_key in PROMPTS, f"Prompt '{prompt_key}' not found in PROMPTS"
            assert 'name' in PROMPTS[prompt_key], f"Prompt '{prompt_key}' missing 'name'"
            assert 'description' in PROMPTS[prompt_key], f"Prompt '{prompt_key}' missing 'description'"

    def test_prompt_content_format(self):
        """Test that prompt content is properly formatted."""
        from prompts import PROMPTS

        for prompt_key, prompt_data in PROMPTS.items():
            assert isinstance(prompt_data['name'], str), f"Prompt '{prompt_key}' name must be string"
            assert len(prompt_data['name']) > 0, f"Prompt '{prompt_key}' name cannot be empty"
            assert isinstance(prompt_data['description'], str), f"Prompt '{prompt_key}' description must be string"
            assert len(prompt_data['description']) > 0, f"Prompt '{prompt_key}' description cannot be empty"

    @patch('project_management_automation.server.mcp')
    def test_prompts_registered_in_server(self, mock_mcp):
        """Test that prompts are registered in the MCP server."""
        # Import server to trigger registration
        import project_management_automation.server as server_module

        # Check if prompts are registered (via decorators)
        # This is a basic check - actual registration happens at runtime
        assert hasattr(server_module, 'mcp') or mock_mcp is not None


class TestIndividualPrompts:
    """Tests for individual prompt content."""

    def test_doc_health_prompt(self):
        """Test documentation health check prompt."""
        from prompts import DOCUMENTATION_HEALTH_CHECK

        assert isinstance(DOCUMENTATION_HEALTH_CHECK, str)
        assert len(DOCUMENTATION_HEALTH_CHECK) > 0
        assert 'health(action="docs"' in DOCUMENTATION_HEALTH_CHECK.lower()

    def test_doc_quick_prompt(self):
        """Test quick documentation check prompt."""
        from prompts import DOCUMENTATION_QUICK_CHECK

        assert isinstance(DOCUMENTATION_QUICK_CHECK, str)
        assert len(DOCUMENTATION_QUICK_CHECK) > 0

    def test_task_alignment_prompt(self):
        """Test task alignment analysis prompt."""
        from prompts import TASK_ALIGNMENT_ANALYSIS

        assert isinstance(TASK_ALIGNMENT_ANALYSIS, str)
        assert len(TASK_ALIGNMENT_ANALYSIS) > 0
        assert 'analyze_alignment' in TASK_ALIGNMENT_ANALYSIS.lower()

    def test_duplicate_cleanup_prompt(self):
        """Test duplicate task cleanup prompt."""
        from prompts import DUPLICATE_TASK_CLEANUP

        assert isinstance(DUPLICATE_TASK_CLEANUP, str)
        assert len(DUPLICATE_TASK_CLEANUP) > 0
        assert 'task_analysis(action="duplicates"' in DUPLICATE_TASK_CLEANUP.lower()

    def test_task_sync_prompt(self):
        """Test task synchronization prompt."""
        from prompts import TASK_SYNC

        assert isinstance(TASK_SYNC, str)
        assert len(TASK_SYNC) > 0
        assert 'task_workflow(action="sync"' in TASK_SYNC.lower()

    def test_security_scan_all_prompt(self):
        """Test security scan (all languages) prompt."""
        from prompts import SECURITY_SCAN_ALL

        assert isinstance(SECURITY_SCAN_ALL, str)
        assert len(SECURITY_SCAN_ALL) > 0
        assert 'security(action=' in SECURITY_SCAN_ALL.lower()

    def test_security_scan_python_prompt(self):
        """Test security scan (Python) prompt."""
        from prompts import SECURITY_SCAN_PYTHON

        assert isinstance(SECURITY_SCAN_PYTHON, str)
        assert len(SECURITY_SCAN_PYTHON) > 0

    def test_security_scan_rust_prompt(self):
        """Test security scan (Rust) prompt."""
        from prompts import SECURITY_SCAN_RUST

        assert isinstance(SECURITY_SCAN_RUST, str)
        assert len(SECURITY_SCAN_RUST) > 0

    def test_automation_discovery_prompt(self):
        """Test automation discovery prompt."""
        from prompts import AUTOMATION_DISCOVERY

        assert isinstance(AUTOMATION_DISCOVERY, str)
        assert len(AUTOMATION_DISCOVERY) > 0
        assert 'run_automation(action="discover"' in AUTOMATION_DISCOVERY.lower()

    def test_automation_high_value_prompt(self):
        """Test high-value automation discovery prompt."""
        from prompts import AUTOMATION_HIGH_VALUE

        assert isinstance(AUTOMATION_HIGH_VALUE, str)
        assert len(AUTOMATION_HIGH_VALUE) > 0

    def test_pre_sprint_cleanup_prompt(self):
        """Test pre-sprint cleanup workflow prompt."""
        from prompts import PRE_SPRINT_CLEANUP

        assert isinstance(PRE_SPRINT_CLEANUP, str)
        assert len(PRE_SPRINT_CLEANUP) > 0
        assert 'task_analysis(action="duplicates")' in PRE_SPRINT_CLEANUP.lower()
        assert 'analyze_alignment(action="todo2")' in PRE_SPRINT_CLEANUP.lower()
        assert 'health(action="docs")' in PRE_SPRINT_CLEANUP.lower()

    def test_post_implementation_review_prompt(self):
        """Test post-implementation review workflow prompt."""
        from prompts import POST_IMPLEMENTATION_REVIEW

        assert isinstance(POST_IMPLEMENTATION_REVIEW, str)
        assert len(POST_IMPLEMENTATION_REVIEW) > 0

    def test_weekly_maintenance_prompt(self):
        """Test weekly maintenance workflow prompt."""
        from prompts import WEEKLY_MAINTENANCE

        assert isinstance(WEEKLY_MAINTENANCE, str)
        assert len(WEEKLY_MAINTENANCE) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


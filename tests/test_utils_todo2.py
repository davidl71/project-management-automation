"""
Unit Tests for Todo2 Utilities

Tests for git project ID detection, task filtering, and task annotation.
"""

import subprocess

# Add project root to path
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from project_management_automation.utils.todo2_utils import (
    _normalize_git_remote,
    annotate_task_project,
    filter_tasks_by_project,
    get_repo_project_id,
    task_belongs_to_project,
)


class TestNormalizeGitRemote:
    """Tests for _normalize_git_remote function."""

    def test_https_url(self):
        """Test normalizing HTTPS GitHub URL."""
        url = "https://github.com/owner/repo.git"
        assert _normalize_git_remote(url) == "owner/repo"

    def test_https_url_no_git_suffix(self):
        """Test normalizing HTTPS URL without .git suffix."""
        url = "https://github.com/owner/repo"
        assert _normalize_git_remote(url) == "owner/repo"

    def test_ssh_url(self):
        """Test normalizing SSH GitHub URL."""
        url = "git@github.com:owner/repo.git"
        assert _normalize_git_remote(url) == "owner/repo"

    def test_ssh_url_no_git_suffix(self):
        """Test normalizing SSH URL without .git suffix."""
        url = "git@github.com:owner/repo"
        assert _normalize_git_remote(url) == "owner/repo"

    def test_empty_url(self):
        """Test normalizing empty URL returns None."""
        assert _normalize_git_remote("") is None
        assert _normalize_git_remote(None) is None

    def test_whitespace_handling(self):
        """Test URL with whitespace is trimmed."""
        url = "  https://github.com/owner/repo.git  \n"
        assert _normalize_git_remote(url) == "owner/repo"

    def test_gitlab_url(self):
        """Test normalizing GitLab URL."""
        url = "https://gitlab.com/owner/repo.git"
        assert _normalize_git_remote(url) == "owner/repo"

    def test_nested_repo_path(self):
        """Test URL with nested path."""
        url = "https://github.com/org/subgroup/repo.git"
        # Should take first two path components after host
        result = _normalize_git_remote(url)
        assert result == "org/subgroup"


class TestGetRepoProjectId:
    """Tests for get_repo_project_id function."""

    @patch('project_management_automation.utils.todo2_utils.subprocess.run')
    @patch('project_management_automation.utils.find_project_root')
    def test_success(self, mock_find_root, mock_run):
        """Test successful git remote detection."""
        mock_find_root.return_value = Path("/project")
        mock_run.return_value = MagicMock(
            stdout="https://github.com/owner/repo.git\n",
            returncode=0
        )

        result = get_repo_project_id()

        assert result == "owner/repo"
        mock_run.assert_called_once()

    @patch('project_management_automation.utils.todo2_utils.subprocess.run')
    @patch('project_management_automation.utils.find_project_root')
    def test_git_command_fails(self, mock_find_root, mock_run):
        """Test handling when git command fails."""
        mock_find_root.return_value = Path("/project")
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")

        result = get_repo_project_id()

        assert result is None

    @patch('project_management_automation.utils.todo2_utils.subprocess.run')
    @patch('project_management_automation.utils.find_project_root')
    def test_git_not_found(self, mock_find_root, mock_run):
        """Test handling when git executable not found."""
        mock_find_root.return_value = Path("/project")
        mock_run.side_effect = FileNotFoundError("git not found")

        result = get_repo_project_id()

        assert result is None

    @patch('project_management_automation.utils.todo2_utils.subprocess.run')
    @patch('project_management_automation.utils.find_project_root')
    def test_with_custom_project_root(self, mock_find_root, mock_run):
        """Test with custom project root path."""
        custom_root = Path("/custom/project")
        mock_find_root.return_value = custom_root
        mock_run.return_value = MagicMock(
            stdout="git@github.com:org/project.git\n",
            returncode=0
        )

        result = get_repo_project_id(custom_root)

        assert result == "org/project"
        mock_find_root.assert_called_once_with(custom_root)


class TestTaskBelongsToProject:
    """Tests for task_belongs_to_project function."""

    def test_task_matches_project(self):
        """Test task with matching project ID."""
        task = {"id": "T-1", "project_id": "owner/repo"}
        assert task_belongs_to_project(task, "owner/repo") is True

    def test_task_different_project(self):
        """Test task with different project ID."""
        task = {"id": "T-1", "project_id": "other/project"}
        assert task_belongs_to_project(task, "owner/repo") is False

    def test_task_no_project_id(self):
        """Test task without project ID (unassigned)."""
        task = {"id": "T-1", "name": "Test task"}
        assert task_belongs_to_project(task, "owner/repo") is True

    def test_no_filter_project_id(self):
        """Test when no filter project ID is provided."""
        task = {"id": "T-1", "project_id": "any/project"}
        assert task_belongs_to_project(task, None) is True

    def test_both_none(self):
        """Test when both task and filter have no project ID."""
        task = {"id": "T-1"}
        assert task_belongs_to_project(task, None) is True


class TestFilterTasksByProject:
    """Tests for filter_tasks_by_project function."""

    def test_filter_matching_tasks(self):
        """Test filtering returns matching tasks."""
        tasks = [
            {"id": "T-1", "project_id": "owner/repo"},
            {"id": "T-2", "project_id": "other/project"},
            {"id": "T-3", "project_id": "owner/repo"},
        ]

        result = filter_tasks_by_project(tasks, "owner/repo")

        assert len(result) == 2
        assert result[0]["id"] == "T-1"
        assert result[1]["id"] == "T-3"

    def test_include_unassigned_tasks(self):
        """Test including tasks without project ID."""
        tasks = [
            {"id": "T-1", "project_id": "owner/repo"},
            {"id": "T-2"},  # No project_id
            {"id": "T-3", "project_id": "other/project"},
        ]

        result = filter_tasks_by_project(tasks, "owner/repo", include_unassigned=True)

        assert len(result) == 2
        assert result[0]["id"] == "T-1"
        assert result[1]["id"] == "T-2"

    def test_exclude_unassigned_tasks(self):
        """Test excluding tasks without project ID."""
        tasks = [
            {"id": "T-1", "project_id": "owner/repo"},
            {"id": "T-2"},  # No project_id
            {"id": "T-3", "project_id": "owner/repo"},
        ]

        result = filter_tasks_by_project(tasks, "owner/repo", include_unassigned=False)

        assert len(result) == 2
        assert result[0]["id"] == "T-1"
        assert result[1]["id"] == "T-3"

    def test_no_project_filter(self):
        """Test when no project filter is applied."""
        tasks = [
            {"id": "T-1", "project_id": "owner/repo"},
            {"id": "T-2", "project_id": "other/project"},
            {"id": "T-3"},
        ]

        result = filter_tasks_by_project(tasks, None)

        assert len(result) == 3

    def test_empty_task_list(self):
        """Test filtering empty task list."""
        result = filter_tasks_by_project([], "owner/repo")
        assert result == []

    def test_with_logger(self):
        """Test filtering with logger for debug messages."""
        import logging
        logger = logging.getLogger("test")

        tasks = [
            {"id": "T-1", "project_id": "other/project"},
        ]

        result = filter_tasks_by_project(tasks, "owner/repo", logger=logger)

        assert len(result) == 0


class TestAnnotateTaskProject:
    """Tests for annotate_task_project function."""

    def test_annotate_new_task(self):
        """Test annotating task without existing project ID."""
        task = {"id": "T-1", "name": "Test task"}

        result = annotate_task_project(task, "owner/repo")

        assert result["project_id"] == "owner/repo"
        assert result["id"] == "T-1"

    def test_annotate_overwrites_existing(self):
        """Test annotating overwrites existing project ID."""
        task = {"id": "T-1", "project_id": "old/project"}

        result = annotate_task_project(task, "new/project")

        assert result["project_id"] == "new/project"

    def test_annotate_with_none(self):
        """Test annotating with None project ID."""
        task = {"id": "T-1", "project_id": "existing/project"}

        result = annotate_task_project(task, None)

        # Should not change existing project_id
        assert result["project_id"] == "existing/project"

    def test_returns_same_dict(self):
        """Test that annotate modifies and returns the same dict."""
        task = {"id": "T-1"}

        result = annotate_task_project(task, "owner/repo")

        assert result is task


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


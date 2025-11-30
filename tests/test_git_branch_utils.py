"""
Unit tests for Git-inspired branch utilities.

Tests branch extraction, assignment, filtering, and statistics.
"""

import pytest

from project_management_automation.utils.branch_utils import (
    MAIN_BRANCH,
    create_branch_tag,
    extract_branch_from_tags,
    filter_tasks_by_branch,
    get_all_branch_statistics,
    get_all_branches,
    get_branch_statistics,
    get_task_branch,
    set_task_branch,
)


class TestBranchExtraction:
    """Tests for branch extraction from tags."""

    def test_extract_branch_from_tags_found(self):
        """Test extracting branch from tags."""
        tags = ["bugfix", "branch:feature-auth", "high-priority"]
        branch = extract_branch_from_tags(tags)
        assert branch == "feature-auth"

    def test_extract_branch_from_tags_not_found(self):
        """Test extracting branch when not present."""
        tags = ["bugfix", "high-priority"]
        branch = extract_branch_from_tags(tags)
        assert branch is None

    def test_extract_branch_from_empty_tags(self):
        """Test extracting branch from empty tags."""
        branch = extract_branch_from_tags([])
        assert branch is None

    def test_get_task_branch_with_tag(self):
        """Test getting branch from task with branch tag."""
        task = {
            "id": "task-123",
            "tags": ["branch:feature-auth", "high-priority"],
        }
        branch = get_task_branch(task)
        assert branch == "feature-auth"

    def test_get_task_branch_main(self):
        """Test getting branch defaults to main."""
        task = {
            "id": "task-123",
            "tags": ["high-priority"],
        }
        branch = get_task_branch(task)
        assert branch == MAIN_BRANCH

    def test_get_task_branch_no_tags(self):
        """Test getting branch from task without tags."""
        task = {"id": "task-123"}
        branch = get_task_branch(task)
        assert branch == MAIN_BRANCH


class TestBranchAssignment:
    """Tests for branch assignment to tasks."""

    def test_set_task_branch_adds_tag(self):
        """Test setting branch adds tag."""
        task = {"id": "task-123", "tags": ["bugfix"]}
        result = set_task_branch(task, "feature-auth")

        assert "branch:feature-auth" in result["tags"]
        assert get_task_branch(result) == "feature-auth"

    def test_set_task_branch_removes_old_tag(self):
        """Test setting branch removes old branch tag."""
        task = {"id": "task-123", "tags": ["branch:old-feature", "bugfix"]}
        result = set_task_branch(task, "new-feature")

        assert "branch:old-feature" not in result["tags"]
        assert "branch:new-feature" in result["tags"]

    def test_set_task_branch_to_main(self):
        """Test setting branch to main removes branch tag."""
        task = {"id": "task-123", "tags": ["branch:feature-auth", "bugfix"]}
        result = set_task_branch(task, MAIN_BRANCH)

        assert not any(tag.startswith("branch:") for tag in result.get("tags", []))
        assert get_task_branch(result) == MAIN_BRANCH

    def test_create_branch_tag(self):
        """Test creating branch tag string."""
        assert create_branch_tag("feature-auth") == "branch:feature-auth"
        assert create_branch_tag(MAIN_BRANCH) == ""


class TestBranchFiltering:
    """Tests for filtering tasks by branch."""

    def test_filter_tasks_by_branch(self):
        """Test filtering tasks by branch."""
        tasks = [
            {"id": "task-1", "tags": ["branch:feature-auth"]},
            {"id": "task-2", "tags": ["branch:bugfix-login"]},
            {"id": "task-3", "tags": []},  # Main branch
            {"id": "task-4", "tags": ["branch:feature-auth"]},
        ]

        filtered = filter_tasks_by_branch(tasks, "feature-auth")
        assert len(filtered) == 2
        assert all(t["id"] in ("task-1", "task-4") for t in filtered)

    def test_filter_tasks_main_branch(self):
        """Test filtering tasks for main branch."""
        tasks = [
            {"id": "task-1", "tags": ["branch:feature-auth"]},
            {"id": "task-2", "tags": []},
            {"id": "task-3", "tags": ["bugfix"]},
        ]

        filtered = filter_tasks_by_branch(tasks, MAIN_BRANCH)
        assert len(filtered) == 2
        assert all(t["id"] in ("task-2", "task-3") for t in filtered)

    def test_get_all_branches(self):
        """Test getting all unique branches."""
        tasks = [
            {"id": "task-1", "tags": ["branch:feature-auth"]},
            {"id": "task-2", "tags": ["branch:bugfix-login"]},
            {"id": "task-3", "tags": []},  # Main branch
            {"id": "task-4", "tags": ["branch:feature-auth"]},
        ]

        branches = get_all_branches(tasks)
        assert MAIN_BRANCH in branches
        assert "feature-auth" in branches
        assert "bugfix-login" in branches
        assert len(branches) == 3


class TestBranchStatistics:
    """Tests for branch statistics."""

    def test_get_branch_statistics(self):
        """Test getting statistics for a branch."""
        tasks = [
            {"id": "task-1", "tags": ["branch:feature-auth"], "status": "todo"},
            {"id": "task-2", "tags": ["branch:feature-auth"], "status": "in_progress"},
            {"id": "task-3", "tags": ["branch:feature-auth"], "status": "completed"},
        ]

        stats = get_branch_statistics(tasks, "feature-auth")

        assert stats["branch"] == "feature-auth"
        assert stats["task_count"] == 3
        assert stats["completed_count"] == 1
        assert stats["completion_rate"] == pytest.approx(33.33, abs=0.01)
        assert stats["by_status"]["todo"] == 1
        assert stats["by_status"]["in_progress"] == 1
        assert stats["by_status"]["completed"] == 1

    def test_get_all_branch_statistics(self):
        """Test getting statistics for all branches."""
        tasks = [
            {"id": "task-1", "tags": ["branch:feature-auth"], "status": "todo"},
            {"id": "task-2", "tags": ["branch:feature-auth"], "status": "completed"},
            {"id": "task-3", "tags": []},  # Main branch
        ]

        all_stats = get_all_branch_statistics(tasks)

        assert MAIN_BRANCH in all_stats
        assert "feature-auth" in all_stats
        assert all_stats["feature-auth"]["task_count"] == 2
        assert all_stats[MAIN_BRANCH]["task_count"] == 1

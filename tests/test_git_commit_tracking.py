"""
Unit tests for Git-inspired commit tracking.

Tests commit creation, retrieval, filtering, and storage.
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from project_management_automation.utils.commit_tracking import (
    CommitTracker,
    TaskCommit,
    get_commit_tracker,
    track_task_create,
    track_task_delete,
    track_task_status_change,
    track_task_update,
)


class TestTaskCommit:
    """Tests for TaskCommit class."""

    def test_create_commit(self):
        """Test creating a commit."""
        commit = TaskCommit(
            task_id="task-123",
            message="Create task: Test",
            old_state={},
            new_state={"id": "task-123", "name": "Test"},
            author="user",
            branch="main",
        )

        assert commit.task_id == "task-123"
        assert commit.message == "Create task: Test"
        assert commit.old_state == {}
        assert commit.new_state == {"id": "task-123", "name": "Test"}
        assert commit.author == "user"
        assert commit.branch == "main"
        assert commit.id is not None
        assert isinstance(commit.timestamp, datetime)

    def test_commit_to_dict(self):
        """Test converting commit to dictionary."""
        commit = TaskCommit(
            task_id="task-123",
            message="Test commit",
            old_state={"a": 1},
            new_state={"a": 2},
        )
        commit_dict = commit.to_dict()

        assert commit_dict["task_id"] == "task-123"
        assert commit_dict["message"] == "Test commit"
        assert commit_dict["old_state"] == {"a": 1}
        assert commit_dict["new_state"] == {"a": 2}
        assert "id" in commit_dict
        assert "timestamp" in commit_dict

    def test_commit_from_dict(self):
        """Test creating commit from dictionary."""
        commit_dict = {
            "id": "commit-123",
            "task_id": "task-123",
            "message": "Test commit",
            "old_state": {"a": 1},
            "new_state": {"a": 2},
            "timestamp": "2025-01-26T10:00:00",
            "author": "user",
            "branch": "main",
        }

        commit = TaskCommit.from_dict(commit_dict)

        assert commit.id == "commit-123"
        assert commit.task_id == "task-123"
        assert commit.message == "Test commit"
        assert commit.old_state == {"a": 1}
        assert commit.new_state == {"a": 2}
        assert commit.author == "user"
        assert commit.branch == "main"


class TestCommitTracker:
    """Tests for CommitTracker class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_create_commit(self, temp_dir):
        """Test creating and storing a commit."""
        tracker = CommitTracker(project_root=temp_dir)

        commit = tracker.create_commit(
            task_id="task-123",
            message="Create task: Test",
            new_state={"id": "task-123", "name": "Test"},
            author="user",
        )

        assert commit.task_id == "task-123"
        assert commit.id is not None

        # Verify commit is stored
        commits = tracker.get_commits_for_task("task-123")
        assert len(commits) == 1
        assert commits[0].id == commit.id

    def test_get_commits_for_task(self, temp_dir):
        """Test retrieving commits for a task."""
        tracker = CommitTracker(project_root=temp_dir)

        # Create multiple commits
        tracker.create_commit("task-123", "Create task", new_state={"id": "task-123"})
        tracker.create_commit("task-123", "Update task", old_state={}, new_state={"id": "task-123", "status": "done"})
        tracker.create_commit("task-456", "Create task", new_state={"id": "task-456"})

        commits = tracker.get_commits_for_task("task-123")
        assert len(commits) == 2
        assert all(c.task_id == "task-123" for c in commits)

    def test_get_commits_for_branch(self, temp_dir):
        """Test retrieving commits for a branch."""
        tracker = CommitTracker(project_root=temp_dir)

        tracker.create_commit("task-1", "Create", new_state={}, branch="feature-auth")
        tracker.create_commit("task-2", "Update", old_state={}, new_state={}, branch="feature-auth")
        tracker.create_commit("task-3", "Create", new_state={}, branch="main")

        commits = tracker.get_commits_for_branch("feature-auth")
        assert len(commits) == 2
        assert all(c.branch == "feature-auth" for c in commits)

    def test_get_latest_commit(self, temp_dir):
        """Test getting latest commit for a task."""
        tracker = CommitTracker(project_root=temp_dir)

        commit1 = tracker.create_commit("task-123", "Create", new_state={})
        commit2 = tracker.create_commit("task-123", "Update", old_state={}, new_state={})

        latest = tracker.get_latest_commit_for_task("task-123")
        assert latest is not None
        assert latest.id == commit2.id

    def test_get_task_state_at_time(self, temp_dir):
        """Test getting task state at a specific time."""
        tracker = CommitTracker(project_root=temp_dir)

        time1 = datetime(2025, 1, 26, 10, 0, 0)
        time2 = datetime(2025, 1, 26, 11, 0, 0)

        # Create commits with specific timestamps
        commit1 = TaskCommit(
            task_id="task-123",
            message="Create",
            new_state={"status": "todo"},
            timestamp=time1,
        )
        commit2 = TaskCommit(
            task_id="task-123",
            message="Update",
            old_state={"status": "todo"},
            new_state={"status": "done"},
            timestamp=time2,
        )

        tracker._load_commits()
        commits = tracker._load_commits()
        commits.extend([commit1, commit2])
        tracker._save_commits(commits)

        state_before = tracker.get_task_state_at_time("task-123", datetime(2025, 1, 26, 10, 30, 0))
        assert state_before == {"status": "todo"}

        state_after = tracker.get_task_state_at_time("task-123", datetime(2025, 1, 26, 11, 30, 0))
        assert state_after == {"status": "done"}


class TestCommitTrackingFunctions:
    """Tests for commit tracking helper functions."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_track_task_create(self, temp_dir):
        """Test tracking task creation."""
        with patch("project_management_automation.utils.commit_tracking.get_commit_tracker") as mock_get:
            tracker = CommitTracker(project_root=temp_dir)
            mock_get.return_value = tracker

            task_data = {"id": "task-123", "name": "Test Task"}
            commit = track_task_create("task-123", task_data, author="user", branch="main")

            assert commit.task_id == "task-123"
            assert "Create task" in commit.message
            assert commit.new_state == task_data

    def test_track_task_update(self, temp_dir):
        """Test tracking task update."""
        with patch("project_management_automation.utils.commit_tracking.get_commit_tracker") as mock_get:
            tracker = CommitTracker(project_root=temp_dir)
            mock_get.return_value = tracker

            old_state = {"id": "task-123", "status": "todo"}
            new_state = {"id": "task-123", "status": "done"}

            commit = track_task_update("task-123", old_state, new_state, author="user")

            assert commit.task_id == "task-123"
            assert "Update task" in commit.message
            assert commit.old_state == old_state
            assert commit.new_state == new_state

    def test_track_task_delete(self, temp_dir):
        """Test tracking task deletion."""
        with patch("project_management_automation.utils.commit_tracking.get_commit_tracker") as mock_get:
            tracker = CommitTracker(project_root=temp_dir)
            mock_get.return_value = tracker

            old_state = {"id": "task-123", "name": "Test Task"}
            commit = track_task_delete("task-123", old_state, author="user")

            assert commit.task_id == "task-123"
            assert "Delete task" in commit.message
            assert commit.old_state == old_state
            assert commit.new_state == {}

    def test_track_task_status_change(self, temp_dir):
        """Test tracking status change."""
        with patch("project_management_automation.utils.commit_tracking.get_commit_tracker") as mock_get:
            tracker = CommitTracker(project_root=temp_dir)
            mock_get.return_value = tracker

            task_data = {"id": "task-123", "name": "Test Task", "status": "done"}

            commit = track_task_status_change("task-123", "todo", "done", task_data, author="user")

            assert commit.task_id == "task-123"
            assert "Change status" in commit.message
            assert commit.old_state["status"] == "todo"
            assert commit.new_state["status"] == "done"

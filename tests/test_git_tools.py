"""
Unit tests for Git-inspired tools (diff, graph, merge).

Tests task diff, git graph visualization, and branch merging.
"""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from project_management_automation.tools.branch_merge import (
    MergeConflict,
    detect_merge_conflicts,
    merge_branches,
    preview_merge,
    resolve_conflict,
)
from project_management_automation.tools.git_graph import (
    generate_commit_graph,
    generate_graphviz_dot,
    generate_text_graph,
)
from project_management_automation.tools.task_diff import (
    compare_task_versions,
    diff_task_states,
    format_diff_output,
    get_task_history,
)
from project_management_automation.utils.commit_tracking import CommitTracker, TaskCommit


class TestTaskDiff:
    """Tests for task diff functionality."""

    def test_diff_task_states_changed(self):
        """Test diffing task states with changes."""
        old_state = {"id": "task-123", "status": "todo", "priority": "high"}
        new_state = {"id": "task-123", "status": "done", "priority": "medium"}

        diff = diff_task_states(old_state, new_state)

        assert "status" in diff["changed"]
        assert "priority" in diff["changed"]
        assert diff["changed"]["status"]["old"] == "todo"
        assert diff["changed"]["status"]["new"] == "done"

    def test_diff_task_states_added(self):
        """Test diffing task states with added fields."""
        old_state = {"id": "task-123"}
        new_state = {"id": "task-123", "tags": ["bugfix"]}

        diff = diff_task_states(old_state, new_state)

        assert "tags" in diff["added"]
        assert diff["added"]["tags"] == ["bugfix"]

    def test_diff_task_states_removed(self):
        """Test diffing task states with removed fields."""
        old_state = {"id": "task-123", "tags": ["bugfix"]}
        new_state = {"id": "task-123"}

        diff = diff_task_states(old_state, new_state)

        assert "tags" in diff["removed"]
        assert diff["removed"]["tags"] == ["bugfix"]

    def test_format_diff_output(self):
        """Test formatting diff output."""
        diff = {
            "changed": {"status": {"old": "todo", "new": "done"}},
            "added": {"tags": ["bugfix"]},
            "removed": {},
            "unchanged": {"id": "task-123"},
        }

        output = format_diff_output(diff, task_name="Test Task")

        assert "Test Task" in output
        assert "Changed Fields" in output
        assert "todo" in output
        assert "done" in output


class TestGitGraph:
    """Tests for Git graph visualization."""

    def test_generate_text_graph(self):
        """Test generating text graph."""
        commits = [
            TaskCommit(
                task_id="task-1",
                message="Create task: Test",
                new_state={},
                timestamp=datetime(2025, 1, 26, 10, 0, 0),
                branch="main",
            ),
            TaskCommit(
                task_id="task-1",
                message="Update task: Test",
                old_state={},
                new_state={},
                timestamp=datetime(2025, 1, 26, 11, 0, 0),
                branch="main",
            ),
        ]

        graph = generate_text_graph(commits)

        assert "Commit History Graph" in graph
        assert "Create task: Test" in graph
        assert "Update task: Test" in graph

    def test_generate_graphviz_dot(self):
        """Test generating Graphviz DOT format."""
        commits = [
            TaskCommit(
                task_id="task-1",
                message="Create task",
                new_state={},
                timestamp=datetime(2025, 1, 26, 10, 0, 0),
                branch="main",
            ),
        ]

        dot = generate_graphviz_dot(commits)

        assert "digraph commit_history" in dot
        assert "Create task" in dot


class TestBranchMerge:
    """Tests for branch merging functionality."""

    def test_detect_merge_conflicts(self):
        """Test detecting merge conflicts."""
        source_tasks = [
            {"id": "task-1", "name": "Task 1", "status": "done"},
            {"id": "task-2", "name": "Task 2", "status": "todo"},
        ]
        target_tasks = [
            {"id": "task-1", "name": "Task 1", "status": "todo"},  # Conflict: different status
            {"id": "task-3", "name": "Task 3", "status": "todo"},
        ]

        conflicts = detect_merge_conflicts(source_tasks, target_tasks)

        assert len(conflicts) == 1
        assert conflicts[0].task_id == "task-1"
        assert "status" in conflicts[0].conflict_fields

    def test_resolve_conflict_newer(self):
        """Test resolving conflict using newer strategy."""
        conflict = MergeConflict(
            task_id="task-1",
            source_state={"id": "task-1", "status": "done", "lastModified": "2025-01-26T11:00:00"},
            target_state={"id": "task-1", "status": "todo", "lastModified": "2025-01-26T10:00:00"},
            conflict_fields=["status"],
        )

        resolved = resolve_conflict(conflict, strategy="newer")

        assert resolved["status"] == "done"  # Source is newer

    def test_resolve_conflict_source(self):
        """Test resolving conflict using source strategy."""
        conflict = MergeConflict(
            task_id="task-1",
            source_state={"id": "task-1", "status": "done"},
            target_state={"id": "task-1", "status": "todo"},
            conflict_fields=["status"],
        )

        resolved = resolve_conflict(conflict, strategy="source")

        assert resolved["status"] == "done"

    def test_resolve_conflict_target(self):
        """Test resolving conflict using target strategy."""
        conflict = MergeConflict(
            task_id="task-1",
            source_state={"id": "task-1", "status": "done"},
            target_state={"id": "task-1", "status": "todo"},
            conflict_fields=["status"],
        )

        resolved = resolve_conflict(conflict, strategy="target")

        assert resolved["status"] == "todo"

    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            todo2_dir = project_root / ".todo2"
            todo2_dir.mkdir()

            # Create initial Todo2 state
            state_file = todo2_dir / "state.todo2.json"
            state_file.write_text(
                json.dumps({
                    "todos": [
                        {"id": "task-1", "name": "Task 1", "tags": ["branch:feature-auth"], "status": "done"},
                        {"id": "task-2", "name": "Task 2", "tags": [], "status": "todo"},
                    ]
                }, indent=2)
            )

            yield project_root

    def test_preview_merge(self, temp_project):
        """Test preview merge (dry run)."""
        with patch("project_management_automation.tools.branch_merge.find_project_root", return_value=temp_project):
            preview = preview_merge("feature-auth", "main")

            assert preview["source_branch"] == "feature-auth"
            assert preview["target_branch"] == "main"
            assert "would_merge" in preview
            assert "conflicts" in preview

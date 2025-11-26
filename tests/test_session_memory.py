"""
Unit tests for the AI Session Memory System.

Tests cover:
- Memory creation and storage
- Memory retrieval by various filters
- Search functionality
- Resource handlers
- Tool functions
- Wisdom integration
"""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest


class TestMemoryCategories:
    """Test memory category definitions."""

    def test_memory_categories_defined(self):
        """All expected categories should be defined."""
        from project_management_automation.resources.memories import MEMORY_CATEGORIES

        expected = ["debug", "research", "architecture", "preference", "insight"]
        assert MEMORY_CATEGORIES == expected

    def test_category_count(self):
        """Should have exactly 5 categories."""
        from project_management_automation.resources.memories import MEMORY_CATEGORIES

        assert len(MEMORY_CATEGORIES) == 5


class TestMemoryCreation:
    """Test memory creation functionality."""

    def test_create_memory_basic(self):
        """Should create a memory with required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory

                memory = create_memory(
                    title="Test Memory",
                    content="This is test content",
                    category="debug",
                )

                assert memory["title"] == "Test Memory"
                assert memory["content"] == "This is test content"
                assert memory["category"] == "debug"
                assert "id" in memory
                assert "created_at" in memory
                assert "session_date" in memory
                assert memory["linked_tasks"] == []

    def test_create_memory_with_task_link(self):
        """Should create memory linked to a task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory

                memory = create_memory(
                    title="Task Debug",
                    content="Fixed issue",
                    category="debug",
                    linked_tasks=["task-123", "task-456"],
                )

                assert memory["linked_tasks"] == ["task-123", "task-456"]

    def test_create_memory_invalid_category_fallback(self):
        """Should fallback to 'insight' for invalid category."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory

                memory = create_memory(
                    title="Test",
                    content="Content",
                    category="invalid_category",
                )

                assert memory["category"] == "insight"

    def test_create_memory_persists_to_file(self):
        """Memory should be saved to JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory

                memory = create_memory(
                    title="Persistent Memory",
                    content="Should be saved",
                    category="research",
                )

                # Check file exists
                memory_file = Path(tmpdir) / ".exarp" / "memories" / f"{memory['id']}.json"
                assert memory_file.exists()

                # Check content
                with open(memory_file) as f:
                    saved = json.load(f)
                assert saved["title"] == "Persistent Memory"


class TestMemoryRetrieval:
    """Test memory retrieval and filtering."""

    def _create_test_memories(self, tmpdir):
        """Helper to create test memories."""
        from project_management_automation.resources.memories import create_memory

        memories = []
        memories.append(
            create_memory(title="Debug 1", content="Debug content", category="debug", linked_tasks=["task-1"])
        )
        memories.append(create_memory(title="Research 1", content="Research content", category="research"))
        memories.append(
            create_memory(
                title="Architecture 1", content="Architecture content", category="architecture", linked_tasks=["task-1"]
            )
        )
        return memories

    def test_get_memory_by_id(self):
        """Should retrieve memory by ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory, get_memory_by_id

                created = create_memory(title="Test", content="Content", category="debug")

                retrieved = get_memory_by_id(created["id"])

                assert retrieved is not None
                assert retrieved["id"] == created["id"]
                assert retrieved["title"] == "Test"

    def test_get_memory_by_id_not_found(self):
        """Should return None for non-existent ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import get_memory_by_id

                result = get_memory_by_id("non-existent-id")

                assert result is None


class TestMemorySearch:
    """Test memory search functionality."""

    def test_search_by_title(self):
        """Should find memories by title match."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory, search_memories

                create_memory(title="Import Error Fix", content="Fixed import", category="debug")
                create_memory(title="Other Memory", content="Something else", category="research")

                results = search_memories("Import")

                assert len(results) >= 1
                assert any("Import" in m["title"] for m in results)

    def test_search_by_content(self):
        """Should find memories by content match."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory, search_memories

                create_memory(title="Memory 1", content="unique_search_term here", category="debug")
                create_memory(title="Memory 2", content="Other content", category="research")

                results = search_memories("unique_search_term")

                assert len(results) >= 1

    def test_search_respects_limit(self):
        """Should respect limit parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory, search_memories

                for i in range(10):
                    create_memory(title=f"Test Memory {i}", content="test content", category="debug")

                results = search_memories("test", limit=3)

                assert len(results) <= 3


class TestMemoryResources:
    """Test MCP resource handlers."""

    def test_get_memories_resource(self):
        """Should return all memories as JSON resource."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory, get_memories_resource

                create_memory(title="Test 1", content="Content 1", category="debug")
                create_memory(title="Test 2", content="Content 2", category="research")

                result_json = get_memories_resource()
                result = json.loads(result_json)

                assert "memories" in result
                assert "total" in result
                assert "categories" in result
                assert result["total"] >= 2

    def test_get_memories_by_category_resource(self):
        """Should filter memories by category."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import (
                    create_memory,
                    get_memories_by_category_resource,
                )

                create_memory(title="Debug 1", content="Content", category="debug")
                create_memory(title="Research 1", content="Content", category="research")

                result_json = get_memories_by_category_resource("debug")
                result = json.loads(result_json)

                assert result["category"] == "debug"
                assert all(m["category"] == "debug" for m in result["memories"])

    def test_get_memories_by_task_resource(self):
        """Should filter memories by task ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import (
                    create_memory,
                    get_memories_by_task_resource,
                )

                create_memory(title="Task Memory", content="Content", category="debug", linked_tasks=["task-xyz"])
                create_memory(title="Other Memory", content="Content", category="debug")

                result_json = get_memories_by_task_resource("task-xyz")
                result = json.loads(result_json)

                assert result["task_id"] == "task-xyz"
                assert all("task-xyz" in m["linked_tasks"] for m in result["memories"])

    def test_get_recent_memories_resource(self):
        """Should return recent memories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory, get_recent_memories_resource

                create_memory(title="Recent", content="Content", category="debug")

                result_json = get_recent_memories_resource(hours=24)
                result = json.loads(result_json)

                assert result["hours"] == 24
                assert "memories" in result

    def test_get_session_memories_resource(self):
        """Should return session memories for a date."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import (
                    create_memory,
                    get_session_memories_resource,
                )

                today = datetime.now().strftime("%Y-%m-%d")
                create_memory(title="Today Memory", content="Content", category="debug")

                result_json = get_session_memories_resource(today)
                result = json.loads(result_json)

                assert result["session_date"] == today
                assert "summary" in result


class TestSessionMemoryTools:
    """Test session memory MCP tools."""

    def test_save_session_insight(self):
        """Should save insight via tool function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.tools.session_memory import save_session_insight

                result = save_session_insight(
                    title="Test Insight",
                    content="Insight content",
                    category="insight",
                )

                assert result["success"] is True
                assert "memory_id" in result

    def test_save_session_insight_with_task(self):
        """Should link insight to task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.tools.session_memory import save_session_insight

                result = save_session_insight(
                    title="Task Insight",
                    content="Linked to task",
                    category="debug",
                    task_id="task-abc",
                )

                assert result["success"] is True
                assert "task-abc" in result["linked_tasks"]

    def test_recall_task_context(self):
        """Should recall memories for a task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.tools.session_memory import save_session_insight, recall_task_context

                # Create memories linked to task
                save_session_insight(title="Debug 1", content="Fix", category="debug", task_id="task-recall")
                save_session_insight(title="Research 1", content="Research", category="research", task_id="task-recall")

                result = recall_task_context("task-recall")

                assert result["success"] is True
                assert result["total_memories"] >= 2

    def test_search_session_memories(self):
        """Should search memories via tool."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.tools.session_memory import (
                    save_session_insight,
                    search_session_memories,
                )

                save_session_insight(title="Searchable Memory", content="unique_term", category="debug")

                result = search_session_memories("unique_term")

                assert result["success"] is True
                assert result["total_results"] >= 1

    def test_generate_session_summary(self):
        """Should generate session summary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.tools.session_memory import (
                    save_session_insight,
                    generate_session_summary,
                )

                save_session_insight(title="Summary Test", content="Content", category="insight")

                result = generate_session_summary()

                assert result["success"] is True
                assert "narrative" in result
                assert "memories_count" in result


class TestWisdomIntegration:
    """Test wisdom resource integration."""

    def test_get_wisdom_resource_structure(self):
        """Should return combined wisdom structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import get_wisdom_resource

                result_json = get_wisdom_resource()
                result = json.loads(result_json)

                assert "memories" in result
                assert "consultations" in result
                assert "combined_insights" in result

    def test_wisdom_resource_merges_timeline(self):
        """Should merge memories and consultations in timeline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create advisor logs directory
            log_dir = Path(tmpdir) / ".exarp" / "advisor_logs"
            log_dir.mkdir(parents=True, exist_ok=True)

            # Create a test consultation log
            log_file = log_dir / f"consultations_{datetime.now().strftime('%Y-%m')}.jsonl"
            consultation = {
                "timestamp": datetime.now().isoformat(),
                "advisor_name": "Test Advisor",
                "quote": "Test wisdom quote",
                "context": "Test context",
            }
            with open(log_file, "w") as f:
                f.write(json.dumps(consultation) + "\n")

            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.resources.memories import create_memory, get_wisdom_resource

                create_memory(title="Test Memory", content="Content", category="insight")

                result_json = get_wisdom_resource()
                result = json.loads(result_json)

                # Should have both memories and consultations
                assert result["memories"]["total"] >= 1
                assert result["consultations"]["total"] >= 1


class TestSprintMemories:
    """Test sprint-related memory functions."""

    def test_get_memories_for_sprint(self):
        """Should get sprint-relevant memories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "project_management_automation.resources.memories.find_project_root",
                return_value=Path(tmpdir),
            ):
                from project_management_automation.tools.session_memory import (
                    save_session_insight,
                    get_memories_for_sprint,
                )

                # Create various memories
                save_session_insight(title="Blocker Found", content="Task blocked by dependency", category="insight")
                save_session_insight(title="Debug Fix", content="Fixed the bug", category="debug")

                result = get_memories_for_sprint()

                assert result["success"] is True
                assert "blockers_mentioned" in result
                assert "debug_solutions" in result
                assert "patterns_observed" in result


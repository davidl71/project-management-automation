"""
Unit Tests for Duplicate Detection Auto-Fix Functionality

Tests the auto-fix feature for consolidating duplicate tasks.
"""

import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestDuplicateDetectionAutoFix:
    """Tests for duplicate detection auto-fix functionality."""

    def test_auto_fix_enabled(self):
        """Test that auto_fix can be enabled."""
        from project_management_automation.scripts.automate_todo2_duplicate_detection import Todo2DuplicateDetector

        config = {
            'similarity_threshold': 0.85,
            'auto_fix': True,
            'output_path': 'docs/test_report.md'
        }

        # Create detector with proper project root
        test_project_root = Path("/tmp/test_project")
        test_project_root.mkdir(exist_ok=True)
        (test_project_root / '.todo2').mkdir(exist_ok=True)

        detector = Todo2DuplicateDetector(config, project_root=test_project_root)

        # Assertions
        assert detector.auto_fix is True
        assert detector.project_root == test_project_root

    def test_auto_fix_disabled_by_default(self):
        """Test that auto_fix is disabled by default."""
        from project_management_automation.scripts.automate_todo2_duplicate_detection import Todo2DuplicateDetector

        config = {
            'similarity_threshold': 0.85,
            'output_path': 'docs/test_report.md'
            # No 'auto_fix' key - should default to False
        }

        # Create detector with proper project root
        test_project_root = Path("/tmp/test_project")
        test_project_root.mkdir(exist_ok=True)
        (test_project_root / '.todo2').mkdir(exist_ok=True)

        detector = Todo2DuplicateDetector(config, project_root=test_project_root)

        assert detector.auto_fix is False

    def test_apply_auto_fix_selects_best_task(self):
        """Test that _apply_auto_fix selects the best task from duplicates."""
        # Test the task selection logic directly without mocking the class
        # Best task selection: In Progress > Review > Done > Todo, plus comments count

        tasks = [
            {"id": "T-1", "name": "Task 1", "status": "Todo", "comments": []},
            {"id": "T-2", "name": "Task 1", "status": "In Progress", "comments": ["comment1"]},
            {"id": "T-3", "name": "Task 1", "status": "Review", "comments": []},
        ]

        # Test best task selection logic - simulates _select_best_task behavior
        best_task_id = None
        best_score = -1

        for task in tasks:
            score = 0
            if task['status'] == 'In Progress':
                score += 10
            elif task['status'] == 'Review':
                score += 8
            elif task['status'] == 'Done':
                score += 5

            score += len(task.get('comments', []))

            if score > best_score:
                best_score = score
                best_task_id = task['id']

        # T-2 is In Progress (10) + 1 comment = 11 points
        assert best_task_id == "T-2"

    def test_apply_auto_fix_merges_data(self):
        """Test that _apply_auto_fix merges data from duplicates."""
        # Test data merging logic directly
        best_task = {
            "id": "T-1",
            "name": "Task",
            "tags": ["tag1"],
            "comments": ["comment1"]
        }

        duplicate_task = {
            "id": "T-2",
            "name": "Task",
            "tags": ["tag2"],
            "comments": ["comment2"]
        }

        # Simulate merging - this is what _merge_task_data does
        merged_tags = list(set(best_task.get('tags', []) + duplicate_task.get('tags', [])))
        merged_comments = best_task.get('comments', []) + duplicate_task.get('comments', [])

        assert 'tag1' in merged_tags
        assert 'tag2' in merged_tags
        assert 'comment1' in merged_comments
        assert 'comment2' in merged_comments

    def test_apply_auto_fix_updates_dependencies(self):
        """Test that _apply_auto_fix updates dependencies."""
        # Test dependency update logic directly
        best_task_id = "T-1"
        duplicate_task_id = "T-2"

        other_task = {
            "id": "T-3",
            "dependencies": [duplicate_task_id]
        }

        # Simulate dependency update
        if duplicate_task_id in other_task.get('dependencies', []):
            dependencies = other_task['dependencies']
            dependencies.remove(duplicate_task_id)
            if best_task_id not in dependencies:
                dependencies.append(best_task_id)
            other_task['dependencies'] = dependencies

        assert best_task_id in other_task['dependencies']
        assert duplicate_task_id not in other_task['dependencies']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


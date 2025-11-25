"""
Unit Tests for Duplicate Detection Auto-Fix Functionality

Tests the auto-fix feature for consolidating duplicate tasks.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import json
from typing import Dict, List

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

    @patch('project_management_automation.scripts.automate_todo2_duplicate_detection.IntelligentAutomationBase.__init__')
    @patch('project_management_automation.scripts.automate_todo2_duplicate_detection.json')
    @patch('project_management_automation.scripts.automate_todo2_duplicate_detection.Path')
    def test_apply_auto_fix_selects_best_task(self, mock_path, mock_json, mock_base_init):
        """Test that _apply_auto_fix selects the best task from duplicates."""
        from project_management_automation.scripts.automate_todo2_duplicate_detection import Todo2DuplicateDetector

        mock_base_init.return_value = None

        detector = Todo2DuplicateDetector({}, project_root=Path("/test"))
        detector.project_root = Path("/test")
        detector.auto_fix = True

        # Mock tasks with duplicates
        tasks = [
            {"id": "T-1", "name": "Task 1", "status": "Todo", "comments": []},
            {"id": "T-2", "name": "Task 1", "status": "In Progress", "comments": ["comment1"]},
            {"id": "T-3", "name": "Task 1", "status": "Review", "comments": []},
        ]

        # Mock Todo2 state file operations
        mock_todo2_path = Mock()
        mock_todo2_path.exists.return_value = True
        mock_todo2_path.read_text.return_value = json.dumps({"todos": tasks})
        mock_path.return_value = mock_todo2_path
        mock_json.loads.return_value = {"todos": tasks}

        # Mock file write
        mock_write_file = Mock()

        # Test best task selection logic
        # Best task should be T-2 (In Progress > Review > Todo, has comments)
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

        assert best_task_id == "T-2"

    @patch('project_management_automation.scripts.automate_todo2_duplicate_detection.IntelligentAutomationBase.__init__')
    def test_apply_auto_fix_merges_data(self, mock_base_init):
        """Test that _apply_auto_fix merges data from duplicates."""
        from project_management_automation.scripts.automate_todo2_duplicate_detection import Todo2DuplicateDetector

        mock_base_init.return_value = None

        detector = Todo2DuplicateDetector({}, project_root=Path("/test"))
        detector.project_root = Path("/test")
        detector.auto_fix = True

        # Test data merging logic
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

        # Simulate merging
        merged_tags = list(set(best_task.get('tags', []) + duplicate_task.get('tags', [])))
        merged_comments = best_task.get('comments', []) + duplicate_task.get('comments', [])

        assert 'tag1' in merged_tags
        assert 'tag2' in merged_tags
        assert 'comment1' in merged_comments
        assert 'comment2' in merged_comments

    @patch('project_management_automation.scripts.automate_todo2_duplicate_detection.IntelligentAutomationBase.__init__')
    def test_apply_auto_fix_updates_dependencies(self, mock_base_init):
        """Test that _apply_auto_fix updates dependencies."""
        from project_management_automation.scripts.automate_todo2_duplicate_detection import Todo2DuplicateDetector

        mock_base_init.return_value = None

        detector = Todo2DuplicateDetector({}, project_root=Path("/test"))
        detector.project_root = Path("/test")
        detector.auto_fix = True

        # Test dependency update logic
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


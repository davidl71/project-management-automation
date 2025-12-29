"""
Unit Tests for Consolidated Automation Tools

Tests for automation, estimation, and task_workflow functions in consolidated_automation.py.
"""

import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import shared test helpers
from tests.test_helpers import (
    assert_error_response,
    assert_success_response,
    parse_json_response,
)

# Import functions to test
from project_management_automation.tools.consolidated_automation import (
    automation,
    estimation,
    task_workflow,
)


class TestAutomation:
    """Tests for automation consolidated tool."""

    @patch('project_management_automation.tools.daily_automation.run_daily_automation')
    def test_automation_daily_action(self, mock_daily):
        """Test daily action routes correctly."""
        mock_daily.return_value = json.dumps({
            "status": "success",
            "tasks_run": 5,
            "results": []
        })

        result = automation(action="daily", tasks=["T-1", "T-2"], include_slow=True)
        result_dict = parse_json_response(result)

        mock_daily.assert_called_once_with(["T-1", "T-2"], True, False, None)
        assert isinstance(result, str)
        assert result_dict.get("status") == "success"

    @patch('project_management_automation.tools.nightly_task_automation.run_nightly_task_automation')
    def test_automation_nightly_action(self, mock_nightly):
        """Test nightly action routes correctly."""
        mock_nightly.return_value = json.dumps({
            "status": "success",
            "tasks_processed": 10
        })

        result = automation(
            action="nightly",
            max_tasks_per_host=5,
            max_parallel_tasks=10,
            priority_filter="high",
            tag_filter=["testing"],
            notify=True
        )
        result_dict = parse_json_response(result)

        mock_nightly.assert_called_once()
        call_kwargs = mock_nightly.call_args[1]
        assert call_kwargs['max_tasks_per_host'] == 5
        assert call_kwargs['max_parallel_tasks'] == 10
        assert call_kwargs['priority_filter'] == "high"
        assert call_kwargs['tag_filter'] == ["testing"]
        assert call_kwargs['notify'] is True
        assert isinstance(result, str)

    @patch('project_management_automation.tools.sprint_automation.sprint_automation')
    def test_automation_sprint_action(self, mock_sprint):
        """Test sprint action routes correctly."""
        mock_sprint.return_value = json.dumps({
            "status": "success",
            "iterations": 3,
            "tasks_completed": 5
        })

        result = automation(
            action="sprint",
            max_iterations=10,
            auto_approve=True,
            extract_subtasks=True,
            run_analysis_tools=True,
            run_testing_tools=True,
            dry_run=False
        )
        result_dict = parse_json_response(result)

        mock_sprint.assert_called_once()
        call_kwargs = mock_sprint.call_args[1]
        assert call_kwargs['max_iterations'] == 10
        assert call_kwargs['auto_approve'] is True
        assert call_kwargs['extract_subtasks'] is True
        assert isinstance(result, str)

    @patch('project_management_automation.tools.automation_opportunities.find_automation_opportunities')
    def test_automation_discover_action(self, mock_discover):
        """Test discover action routes correctly."""
        mock_discover.return_value = json.dumps({
            "status": "success",
            "opportunities": []
        })

        result = automation(action="discover", min_value_score=0.7, output_path="/tmp/report.json")
        result_dict = parse_json_response(result)

        mock_discover.assert_called_once_with(0.7, "/tmp/report.json")
        assert isinstance(result, str)

    def test_automation_invalid_action(self):
        """Test invalid action returns error."""
        result = automation(action="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "invalid" in result_dict.get("error", "").lower()

    @patch('project_management_automation.tools.daily_automation.run_daily_automation')
    def test_automation_daily_error_handling(self, mock_daily):
        """Test error handling in daily action."""
        mock_daily.side_effect = Exception("Test error")

        # Exception will propagate - this tests that errors are not silently swallowed
        with pytest.raises(Exception, match="Test error"):
            automation(action="daily")


class TestEstimation:
    """Tests for estimation consolidated tool."""

    @patch('project_management_automation.tools.task_duration_estimator.estimate_task_duration')
    def test_estimation_estimate_action_statistical(self, mock_estimate):
        """Test estimate action with statistical method."""
        mock_estimate.return_value = 2.5

        result = estimation(
            action="estimate",
            name="Test task",
            details="Test details",
            tags="testing,automation",
            priority="high",
            use_mlx=False,
            use_historical=True
        )
        result_dict = parse_json_response(result)

        assert result_dict.get("estimate_hours") == 2.5
        assert result_dict.get("method") == "statistical"
        assert result_dict.get("name") == "Test task"

    @patch('project_management_automation.tools.mlx_task_estimator.estimate_task_duration_mlx_enhanced')
    def test_estimation_estimate_action_mlx(self, mock_mlx):
        """Test estimate action with MLX enhancement."""
        mock_mlx.return_value = 3.0

        result = estimation(
            action="estimate",
            name="Test task",
            details="Test details",
            tags="testing",
            priority="medium",
            use_mlx=True,
            mlx_weight=0.3
        )
        result_dict = parse_json_response(result)

        assert result_dict.get("estimate_hours") == 3.0
        assert result_dict.get("method") == "mlx_enhanced"

    @patch('project_management_automation.tools.coreml_task_estimator.estimate_task_duration_coreml_enhanced')
    def test_estimation_estimate_action_coreml(self, mock_coreml):
        """Test estimate action with Core ML enhancement."""
        mock_coreml.return_value = 2.8

        result = estimation(
            action="estimate",
            name="Test task",
            details="Test details",
            tags="testing",
            priority="medium",
            use_coreml=True,
            coreml_model_path="models/coreml/task_estimator.json",
            coreml_weight=0.3,
            compute_units="all"
        )
        result_dict = parse_json_response(result)

        assert result_dict.get("estimate_hours") == 2.8
        assert result_dict.get("method") == "coreml_neural_engine"

    def test_estimation_estimate_missing_name(self):
        """Test estimate action without required name parameter."""
        result = estimation(action="estimate", details="Test details")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "name parameter required" in result_dict.get("error", "")

    @patch('project_management_automation.tools.estimation_learner.EstimationLearner')
    def test_estimation_analyze_action(self, mock_learner_class):
        """Test analyze action routes correctly."""
        mock_learner = Mock()
        mock_learner.analyze_estimation_accuracy.return_value = {
            "mae": 0.5,
            "rmse": 0.8,
            "accuracy": 85.0
        }
        mock_learner_class.return_value = mock_learner

        result = estimation(action="analyze")
        result_dict = parse_json_response(result)

        mock_learner.analyze_estimation_accuracy.assert_called_once()
        assert result_dict.get("mae") == 0.5

    @patch('project_management_automation.tools.task_duration_estimator.TaskDurationEstimator')
    def test_estimation_stats_action(self, mock_estimator_class):
        """Test stats action routes correctly."""
        mock_estimator = Mock()
        mock_estimator.get_statistics.return_value = json.dumps({
            "total_tasks": 100,
            "average_hours": 2.5
        })
        mock_estimator_class.return_value = mock_estimator

        result = estimation(action="stats")
        result_dict = parse_json_response(result)

        mock_estimator.get_statistics.assert_called_once()
        assert isinstance(result, str)

    @patch('pathlib.Path.exists')
    @patch('project_management_automation.utils.find_project_root')
    @patch('project_management_automation.tools.mlx_task_estimator.MLXEnhancedTaskEstimator')
    def test_estimation_batch_action(self, mock_estimator_class, mock_root, mock_exists):
        """Test batch action processes multiple tasks."""
        # Setup mocks
        from pathlib import Path
        mock_root.return_value = Path("/test/project")
        mock_exists.return_value = True
        
        mock_estimator = Mock()
        mock_estimator.estimate.return_value = {
            "estimate_hours": 2.0,
            "confidence": 0.8,
            "method": "mlx_enhanced"
        }
        mock_estimator_class.return_value = mock_estimator

        # Mock Todo2 file reading
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
                "todos": [
                    {"id": "T-1", "name": "Task 1", "status": "Todo", "tags": ["test"]},
                    {"id": "T-2", "name": "Task 2", "status": "Todo", "tags": ["test"]}
                ]
            })

            result = estimation(action="batch", use_mlx=True)
            result_dict = parse_json_response(result)

            assert result_dict.get("status") == "success"
            assert result_dict.get("total_tasks") == 2

    def test_estimation_invalid_action(self):
        """Test invalid action returns error."""
        result = estimation(action="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "Unknown estimation action" in result_dict.get("error", "")


class TestTaskWorkflow:
    """Tests for task_workflow consolidated tool."""

    @patch('project_management_automation.tools.todo_sync.sync_todo_tasks')
    def test_task_workflow_sync_action(self, mock_sync):
        """Test sync action routes correctly."""
        mock_sync.return_value = json.dumps({
            "status": "success",
            "synced": 10
        })

        result = task_workflow(action="sync", dry_run=True)
        result_dict = parse_json_response(result)

        mock_sync.assert_called_once_with(True, None)
        assert result_dict.get("status") == "success"

    @patch('project_management_automation.tools.batch_task_approval.batch_approve_tasks')
    def test_task_workflow_approve_action(self, mock_approve):
        """Test approve action routes correctly."""
        mock_approve.return_value = json.dumps({
            "status": "success",
            "approved_count": 5
        })

        result = task_workflow(
            action="approve",
            status="Review",
            new_status="Todo",
            clarification_none=True,
            filter_tag="testing",
            task_ids='["T-1", "T-2"]',
            dry_run=False
        )
        result_dict = parse_json_response(result)

        mock_approve.assert_called_once()
        call_kwargs = mock_approve.call_args[1]
        assert call_kwargs['status'] == "Review"
        assert call_kwargs['new_status'] == "Todo"
        assert call_kwargs['clarification_none'] is True
        assert call_kwargs['filter_tag'] == "testing"
        assert isinstance(result, str)

    @patch('project_management_automation.tools.batch_task_approval.batch_approve_tasks')
    def test_task_workflow_approve_invalid_json(self, mock_approve):
        """Test approve action with invalid task_ids JSON."""
        result = task_workflow(action="approve", task_ids="invalid json")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "Invalid task_ids JSON" in result_dict.get("error", "")

    @patch('project_management_automation.tools.task_clarification_resolution.list_tasks_awaiting_clarification')
    def test_task_workflow_clarify_list_action(self, mock_list):
        """Test clarify list sub_action routes correctly."""
        mock_list.return_value = json.dumps({
            "status": "success",
            "tasks": []
        })

        result = task_workflow(action="clarify", sub_action="list")
        result_dict = parse_json_response(result)

        mock_list.assert_called_once()
        assert isinstance(result, str)

    @patch('project_management_automation.tools.task_clarification_resolution.resolve_task_clarification')
    def test_task_workflow_clarify_resolve_action(self, mock_resolve):
        """Test clarify resolve sub_action routes correctly."""
        mock_resolve.return_value = json.dumps({
            "status": "success",
            "resolved": True
        })

        result = task_workflow(
            action="clarify",
            sub_action="resolve",
            task_id="T-1",
            clarification_text="Test clarification",
            decision="proceed",
            move_to_todo=True
        )
        result_dict = parse_json_response(result)

        mock_resolve.assert_called_once()
        assert isinstance(result, str)

    def test_task_workflow_clarify_resolve_missing_task_id(self):
        """Test clarify resolve without required task_id."""
        result = task_workflow(action="clarify", sub_action="resolve")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "task_id required" in result_dict.get("error", "")

    @patch('project_management_automation.tools.task_clarification_resolution.resolve_multiple_clarifications')
    def test_task_workflow_clarify_batch_action(self, mock_batch):
        """Test clarify batch sub_action routes correctly."""
        mock_batch.return_value = json.dumps({
            "status": "success",
            "resolved": 3
        })

        decisions = [{"task_id": "T-1", "decision": "proceed"}]
        result = task_workflow(
            action="clarify",
            sub_action="batch",
            decisions_json=json.dumps(decisions),
            move_to_todo=True
        )
        result_dict = parse_json_response(result)

        mock_batch.assert_called_once()
        assert isinstance(result, str)

    def test_task_workflow_clarify_batch_invalid_json(self):
        """Test clarify batch with invalid decisions_json."""
        result = task_workflow(action="clarify", sub_action="batch", decisions_json="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "Invalid decisions_json" in result_dict.get("error", "")

    def test_task_workflow_clarify_batch_missing_json(self):
        """Test clarify batch without decisions_json."""
        result = task_workflow(action="clarify", sub_action="batch")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "decisions_json required" in result_dict.get("error", "")

    def test_task_workflow_clarify_invalid_sub_action(self):
        """Test clarify with invalid sub_action."""
        result = task_workflow(action="clarify", sub_action="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "Unknown sub_action" in result_dict.get("error", "")

    @patch('project_management_automation.tools.task_clarity_improver.analyze_task_clarity')
    def test_task_workflow_clarity_action_analyze(self, mock_analyze):
        """Test clarity action with analyze (auto_apply=False)."""
        mock_analyze.return_value = {
            "status": "success",
            "tasks_analyzed": 10
        }

        result = task_workflow(action="clarity", auto_apply=False, output_format="json")
        result_dict = parse_json_response(result)

        mock_analyze.assert_called_once()
        assert isinstance(result, str)

    @patch('project_management_automation.tools.task_clarity_improver.improve_task_clarity')
    def test_task_workflow_clarity_action_improve(self, mock_improve):
        """Test clarity action with improve (auto_apply=True)."""
        mock_improve.return_value = json.dumps({
            "status": "success",
            "tasks_improved": 5
        })

        result = task_workflow(action="clarity", auto_apply=True, output_path="/tmp/report.json")
        result_dict = parse_json_response(result)

        mock_improve.assert_called_once()
        assert isinstance(result, str)

    @patch('project_management_automation.tools.stale_task_cleanup.cleanup_stale_tasks')
    def test_task_workflow_cleanup_action(self, mock_cleanup):
        """Test cleanup action routes correctly."""
        mock_cleanup.return_value = json.dumps({
            "status": "success",
            "cleaned": 3
        })

        result = task_workflow(
            action="cleanup",
            stale_threshold_hours=4.0,
            dry_run=True,
            output_path="/tmp/cleanup.json"
        )
        result_dict = parse_json_response(result)

        mock_cleanup.assert_called_once_with(4.0, True, "/tmp/cleanup.json")
        assert isinstance(result, str)

    def test_task_workflow_invalid_action(self):
        """Test invalid action returns error."""
        result = task_workflow(action="invalid")
        result_dict = parse_json_response(result)

        assert result_dict.get("status") == "error"
        assert "Unknown task_workflow action" in result_dict.get("error", "")


class TestParameterValidation:
    """Tests for parameter validation across all automation tools."""

    def test_automation_invalid_action_type(self):
        """Test automation with invalid action type."""
        # Action should be string, but test with None
        result = automation(action=None)  # type: ignore
        result_dict = parse_json_response(result)

        # Should handle gracefully or return error
        assert isinstance(result, str)

    def test_estimation_invalid_priority(self):
        """Test estimation with invalid priority value."""
        result = estimation(
            action="estimate",
            name="Test",
            priority="invalid_priority"
        )
        result_dict = parse_json_response(result)

        # Should handle invalid priority gracefully
        assert isinstance(result, str)

    def test_estimation_invalid_tags_format(self):
        """Test estimation with various tag formats."""
        # Test with None
        result1 = estimation(action="estimate", name="Test", tags=None)
        assert isinstance(result1, str)

        # Test with empty string
        result2 = estimation(action="estimate", name="Test", tags="")
        assert isinstance(result2, str)

        # Test with comma-separated
        result3 = estimation(action="estimate", name="Test", tags="tag1,tag2,tag3")
        assert isinstance(result3, str)

    def test_task_workflow_invalid_status(self):
        """Test task_workflow with invalid status values."""
        result = task_workflow(
            action="approve",
            status="InvalidStatus",
            new_status="AlsoInvalid"
        )
        result_dict = parse_json_response(result)

        # Should handle invalid status gracefully
        assert isinstance(result, str)

    def test_task_workflow_invalid_stale_threshold(self):
        """Test task_workflow cleanup with invalid threshold."""
        # Test with negative value
        result = task_workflow(action="cleanup", stale_threshold_hours=-1.0)
        assert isinstance(result, str)

        # Test with zero
        result = task_workflow(action="cleanup", stale_threshold_hours=0.0)
        assert isinstance(result, str)


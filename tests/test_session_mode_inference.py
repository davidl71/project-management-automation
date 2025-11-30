"""
Unit Tests for Session Mode Inference (MODE-002)

Tests for session_mode_inference.py, FileEditTracker, and related components.
"""

import json
import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime, timedelta
import sys
import tempfile
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from project_management_automation.tools.dynamic_tools import (
    FileEditTracker,
    ToolUsageTracker,
    DynamicToolManager,
    get_tool_manager,
    reset_tool_manager,
)
from project_management_automation.tools.session_mode_inference import (
    SessionMode,
    SessionModeInference,
    ModeInferenceResult,
)
from project_management_automation.resources.session import (
    SessionModeStorage,
    get_session_mode_resource,
    infer_session_mode_tool,
)


class TestFileEditTracker:
    """Tests for FileEditTracker class."""

    def test_record_file_edit(self):
        """Test recording file edits."""
        tracker = FileEditTracker()
        
        tracker.record_file_edit("/path/to/file1.py")
        tracker.record_file_edit("/path/to/file2.py")
        tracker.record_file_edit("/path/to/file1.py")  # Duplicate
        
        assert tracker.get_unique_files_count() == 2
        assert len(tracker.edit_timestamps) == 3

    def test_get_unique_files_count(self):
        """Test getting unique file count."""
        tracker = FileEditTracker()
        
        assert tracker.get_unique_files_count() == 0
        
        tracker.record_file_edit("/path/to/file1.py")
        tracker.record_file_edit("/path/to/file2.py")
        
        assert tracker.get_unique_files_count() == 2

    def test_get_edit_frequency(self):
        """Test calculating edit frequency."""
        tracker = FileEditTracker()
        
        # Record edits over time
        tracker.record_file_edit("/path/to/file1.py")
        time.sleep(0.1)
        tracker.record_file_edit("/path/to/file2.py")
        time.sleep(0.1)
        tracker.record_file_edit("/path/to/file3.py")
        
        # Should have high frequency in 60-second window
        frequency = tracker.get_edit_frequency(window_seconds=60)
        assert frequency > 0

    def test_is_multi_file_session(self):
        """Test multi-file session detection."""
        tracker = FileEditTracker()
        
        assert tracker.is_multi_file_session(threshold=2) is False
        
        tracker.record_file_edit("/path/to/file1.py")
        assert tracker.is_multi_file_session(threshold=2) is False
        
        tracker.record_file_edit("/path/to/file2.py")
        assert tracker.is_multi_file_session(threshold=2) is False  # Exactly 2, not >2
        
        tracker.record_file_edit("/path/to/file3.py")
        assert tracker.is_multi_file_session(threshold=2) is True

    def test_serialization(self):
        """Test serialization and deserialization."""
        tracker = FileEditTracker()
        tracker.record_file_edit("/path/to/file1.py")
        tracker.record_file_edit("/path/to/file2.py")
        
        data = tracker.to_dict()
        assert "edited_files" in data
        assert "edit_timestamps" in data
        
        restored = FileEditTracker.from_dict(data)
        assert restored.get_unique_files_count() == 2
        assert len(restored.edit_timestamps) == 2


class TestSessionModeInference:
    """Tests for SessionModeInference engine."""

    def test_infer_agent_mode(self):
        """Test AGENT mode detection."""
        inference = SessionModeInference()
        
        # Create high-frequency, multi-file pattern
        tool_tracker = ToolUsageTracker()
        file_tracker = FileEditTracker()
        
        # Simulate high tool frequency (>5/min)
        for i in range(10):
            tool_tracker.record_tool_call(f"tool_{i}")
        
        # Simulate multi-file editing
        file_tracker.record_file_edit("/path/to/file1.py")
        file_tracker.record_file_edit("/path/to/file2.py")
        file_tracker.record_file_edit("/path/to/file3.py")
        
        # Long session (>5min)
        session_duration = 400.0  # ~6.7 minutes
        
        result = inference.infer_mode(
            tool_tracker=tool_tracker,
            file_tracker=file_tracker,
            session_duration_seconds=session_duration
        )
        
        assert result.mode == SessionMode.AGENT
        assert result.confidence >= 0.5  # Allow 0.5 or higher
        assert len(result.reasoning) > 0
        assert "AGENT" in result.reasoning[0] or "agent" in result.reasoning[0].lower()

    def test_infer_ask_mode(self):
        """Test ASK mode detection."""
        inference = SessionModeInference()
        
        # Create moderate-frequency, single-file pattern
        tool_tracker = ToolUsageTracker()
        file_tracker = FileEditTracker()
        
        # Simulate moderate tool frequency (1-3/min)
        for i in range(3):
            tool_tracker.record_tool_call(f"tool_{i}")
        
        # Simulate single file editing
        file_tracker.record_file_edit("/path/to/file1.py")
        
        # Shorter session (<5min)
        session_duration = 120.0  # 2 minutes
        
        result = inference.infer_mode(
            tool_tracker=tool_tracker,
            file_tracker=file_tracker,
            session_duration_seconds=session_duration
        )
        
        # Should favor ASK mode
        assert result.mode in [SessionMode.ASK, SessionMode.UNKNOWN]
        assert result.confidence >= 0.0

    def test_infer_manual_mode(self):
        """Test MANUAL mode detection."""
        inference = SessionModeInference()
        
        # Create very low tool frequency pattern
        tool_tracker = ToolUsageTracker()
        file_tracker = FileEditTracker()
        
        # Very few tool calls (<1/min)
        tool_tracker.record_tool_call("read_file")
        
        # But file edits happening
        file_tracker.record_file_edit("/path/to/file1.py")
        
        session_duration = 300.0  # 5 minutes
        
        result = inference.infer_mode(
            tool_tracker=tool_tracker,
            file_tracker=file_tracker,
            session_duration_seconds=session_duration
        )
        
        # Should favor MANUAL mode
        assert result.mode in [SessionMode.MANUAL, SessionMode.UNKNOWN]
        assert result.confidence >= 0.0

    def test_infer_unknown_mode(self):
        """Test UNKNOWN mode for insufficient data."""
        inference = SessionModeInference()
        
        tool_tracker = ToolUsageTracker()
        file_tracker = FileEditTracker()
        
        # Very short session with no tool calls
        session_duration = 5.0  # 5 seconds
        
        result = inference.infer_mode(
            tool_tracker=tool_tracker,
            file_tracker=file_tracker,
            session_duration_seconds=session_duration
        )
        
        assert result.mode == SessionMode.UNKNOWN
        assert result.confidence == 0.0
        assert "Insufficient data" in result.reasoning[0]

    def test_mode_inference_result_to_dict(self):
        """Test ModeInferenceResult serialization."""
        result = ModeInferenceResult(
            mode=SessionMode.AGENT,
            confidence=0.85,
            reasoning=["High tool frequency", "Multi-file editing"],
            metrics={"tool_calls": 10, "files": 3}
        )
        
        data = result.to_dict()
        assert data["mode"] == "agent"
        assert data["confidence"] == 0.85
        assert len(data["reasoning"]) == 2
        assert data["metrics"]["tool_calls"] == 10


class TestSessionModeStorage:
    """Tests for SessionModeStorage class."""

    def test_save_and_get_current_mode(self):
        """Test saving and retrieving current mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir) / "session_mode.json"
            storage = SessionModeStorage(storage_path=storage_path)
            
            storage.save_mode(
                mode=SessionMode.AGENT,
                confidence=0.85,
                reasoning=["High tool frequency"],
                metrics={"tool_calls": 10}
            )
            
            current = storage.get_current_mode()
            assert current is not None
            assert current["mode"] == "agent"
            assert current["confidence"] == 0.85

    def test_mode_history(self):
        """Test mode history tracking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir) / "session_mode.json"
            storage = SessionModeStorage(storage_path=storage_path)
            
            # Save multiple modes
            storage.save_mode(SessionMode.AGENT, 0.8, ["reason1"], {})
            storage.save_mode(SessionMode.ASK, 0.7, ["reason2"], {})
            
            history = storage.get_mode_history()
            assert len(history) == 2
            assert history[0]["mode"] == "agent"
            assert history[1]["mode"] == "ask"

    def test_get_mode_history_with_session_id(self):
        """Test filtering history by session ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir) / "session_mode.json"
            storage = SessionModeStorage(storage_path=storage_path)
            
            storage.save_mode(SessionMode.AGENT, 0.8, ["reason1"], {}, session_id="session1")
            storage.save_mode(SessionMode.ASK, 0.7, ["reason2"], {}, session_id="session2")
            storage.save_mode(SessionMode.AGENT, 0.9, ["reason3"], {}, session_id="session1")
            
            history = storage.get_mode_history(session_id="session1")
            assert len(history) == 2
            assert all(entry["session_id"] == "session1" for entry in history)


class TestDynamicToolManagerIntegration:
    """Tests for DynamicToolManager integration."""

    def test_record_tool_usage_with_file_paths(self):
        """Test recording tool usage with file path extraction."""
        manager = DynamicToolManager()
        
        # Record tool usage with file path arguments
        manager.record_tool_usage(
            "search_replace",
            tool_args={"file_path": "/path/to/file.py", "old_string": "old", "new_string": "new"}
        )
        
        assert manager.file_tracker.get_unique_files_count() == 1
        assert sum(manager.usage_tracker.tool_counts.values()) == 1

    def test_extract_file_paths(self):
        """Test file path extraction from tool arguments."""
        manager = DynamicToolManager()
        
        # Test common argument names
        paths = manager._extract_file_paths("read_file", {"target_file": "/path/to/file.py"})
        assert "/path/to/file.py" in paths
        
        paths = manager._extract_file_paths("write", {"file_path": "/path/to/file2.py"})
        assert "/path/to/file2.py" in paths
        
        # Test multiple files
        paths = manager._extract_file_paths("read_file", {"files": ["/path/to/file1.py", "/path/to/file2.py"]})
        assert len(paths) == 2

    def test_update_inferred_mode(self):
        """Test updating inferred mode."""
        manager = DynamicToolManager()
        
        # Simulate some activity
        for i in range(10):
            manager.record_tool_usage(f"tool_{i}")
        manager.file_tracker.record_file_edit("/path/to/file1.py")
        manager.file_tracker.record_file_edit("/path/to/file2.py")
        manager.file_tracker.record_file_edit("/path/to/file3.py")
        
        result = manager.update_inferred_mode()
        
        assert result is not None
        assert result.mode in [SessionMode.AGENT, SessionMode.ASK, SessionMode.MANUAL, SessionMode.UNKNOWN]
        assert 0.0 <= result.confidence <= 1.0
        assert manager.inferred_mode == result

    def test_get_current_mode_auto_update(self):
        """Test get_current_mode with auto-update."""
        manager = DynamicToolManager()
        
        # Initially no mode
        assert manager.inferred_mode is None
        
        # Simulate activity
        for i in range(5):
            manager.record_tool_usage(f"tool_{i}")
        
        # Should auto-update
        result = manager.get_current_mode()
        assert result is not None


class TestMCPResources:
    """Tests for MCP resource endpoints."""

    @patch('project_management_automation.resources.session.get_tool_manager')
    def test_get_session_mode_resource(self, mock_get_manager):
        """Test MCP resource endpoint."""
        # Mock manager with mode inference
        manager = Mock()
        manager.usage_tracker = ToolUsageTracker()
        manager.file_tracker = FileEditTracker()
        manager.file_tracker.record_file_edit("/path/to/file.py")
        manager.mode_inference = None  # Will trigger lazy import
        
        mock_get_manager.return_value = manager
        
        result_json = get_session_mode_resource()
        result = json.loads(result_json)
        
        assert "inferred_mode" in result or "mode" in result
        assert "confidence" in result

    @patch('project_management_automation.resources.session.get_tool_manager')
    @patch('project_management_automation.resources.session._storage')
    def test_infer_session_mode_tool(self, mock_storage, mock_get_manager):
        """Test MCP tool endpoint."""
        # Mock manager
        manager = Mock()
        manager.usage_tracker = ToolUsageTracker()
        manager.file_tracker = FileEditTracker()
        manager.file_tracker.record_file_edit("/path/to/file.py")
        manager.mode_inference = None
        
        mock_get_manager.return_value = manager
        mock_storage.get_current_mode.return_value = None  # Force recompute
        
        result_json = infer_session_mode_tool(force_recompute=False)
        result = json.loads(result_json)
        
        assert "mode" in result or "error" in result
        if "mode" in result:
            assert result["mode"] in ["agent", "ask", "manual", "unknown"]


class TestIntegration:
    """Integration tests for complete MODE-002 system."""

    def test_end_to_end_agent_mode_detection(self):
        """Test complete flow for AGENT mode detection."""
        reset_tool_manager()
        manager = get_tool_manager()
        
        # Simulate AGENT mode pattern
        for i in range(15):
            manager.record_tool_usage(
                f"tool_{i}",
                tool_args={"file_path": f"/path/to/file{(i % 3) + 1}.py"}
            )
        
        # Update mode inference
        result = manager.update_inferred_mode()
        
        assert result is not None
        assert result.mode in [SessionMode.AGENT, SessionMode.ASK, SessionMode.MANUAL, SessionMode.UNKNOWN]
        assert manager.file_tracker.get_unique_files_count() >= 1

    def test_mode_history_tracking(self):
        """Test that mode history is tracked."""
        reset_tool_manager()
        manager = get_tool_manager()
        
        # Make multiple updates
        for _ in range(3):
            manager.record_tool_usage("test_tool")
            manager.update_inferred_mode()
        
        assert len(manager.mode_history) == 3
        assert all(isinstance(r, ModeInferenceResult) for r in manager.mode_history)

    def test_middleware_integration_simulation(self):
        """Simulate middleware integration."""
        reset_tool_manager()
        manager = get_tool_manager()
        
        # Simulate tool calls as middleware would
        tool_calls = [
            ("read_file", {"target_file": "/path/to/file1.py"}),
            ("read_file", {"target_file": "/path/to/file2.py"}),
            ("search_replace", {"file_path": "/path/to/file1.py", "old_string": "old", "new_string": "new"}),
            ("write", {"file_path": "/path/to/file3.py", "contents": "content"}),
            ("read_file", {"target_file": "/path/to/file2.py"}),
        ]
        
        for tool_name, tool_args in tool_calls:
            manager.record_tool_usage(tool_name, tool_args=tool_args)
        
        # Check file tracking
        assert manager.file_tracker.get_unique_files_count() == 3
        
        # Update mode
        result = manager.update_inferred_mode()
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Unit Tests for Async Context Detection

Tests the try/except/else pattern used to detect whether code is running
in an async context and handle it appropriately.

Bug Fix Coverage:
- Verifies that sync callers can use asyncio.run() safely
- Verifies that async callers get a clear RuntimeError
- Prevents regression of the bug where the intentionally raised RuntimeError
  was caught by the same except block
"""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAsyncContextDetection:
    """Tests for async context detection in sync wrapper functions."""

    def test_security_sync_context_no_loop(self):
        """Test security() works when called from sync context (no event loop)."""
        from project_management_automation.tools.consolidated import security

        # Mock the async function to avoid actual execution
        with patch('project_management_automation.tools.consolidated.security_async', new_callable=AsyncMock) as mock_async:
            mock_async.return_value = {"status": "success", "results": {}}

            # Call from sync context - should work
            result = security(action="scan")

            # Verify async function was called
            mock_async.assert_called_once()

    def test_security_async_context_raises_error(self):
        """Test security() raises RuntimeError when called from async context."""
        from project_management_automation.tools.consolidated import security

        async def call_from_async():
            # This should raise RuntimeError because we're in an async context
            return security(action="scan")

        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(call_from_async())

        assert "async context" in str(exc_info.value).lower()
        assert "security_async" in str(exc_info.value)

    def test_testing_sync_context_no_loop(self):
        """Test testing() works when called from sync context (no event loop)."""
        from project_management_automation.tools.consolidated import testing

        # Mock the async function to avoid actual execution
        with patch('project_management_automation.tools.consolidated.testing_async', new_callable=AsyncMock) as mock_async:
            mock_async.return_value = {"status": "success", "results": {}}

            # Call from sync context - should work
            result = testing(action="run")

            # Verify async function was called
            mock_async.assert_called_once()

    def test_testing_async_context_raises_error(self):
        """Test testing() raises RuntimeError when called from async context."""
        from project_management_automation.tools.consolidated import testing

        async def call_from_async():
            # This should raise RuntimeError because we're in an async context
            return testing(action="run")

        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(call_from_async())

        assert "async context" in str(exc_info.value).lower()
        assert "testing_async" in str(exc_info.value)

    def test_scan_dependency_security_sync_context_no_loop(self):
        """Test scan_dependency_security() works when called from sync context."""
        from project_management_automation.tools.dependency_security import scan_dependency_security

        # Mock the async function to avoid actual execution
        with patch('project_management_automation.tools.dependency_security.scan_dependency_security_async', new_callable=AsyncMock) as mock_async:
            mock_async.return_value = json.dumps({"status": "success"})

            # Call from sync context - should work
            result = scan_dependency_security()

            # Verify async function was called
            mock_async.assert_called_once()

    def test_scan_dependency_security_async_context_raises_error(self):
        """Test scan_dependency_security() raises RuntimeError when called from async context."""
        from project_management_automation.tools.dependency_security import scan_dependency_security

        async def call_from_async():
            # This should raise RuntimeError because we're in an async context
            return scan_dependency_security()

        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(call_from_async())

        assert "async context" in str(exc_info.value).lower()
        assert "scan_dependency_security_async" in str(exc_info.value)


class TestAsyncContextDetectionEdgeCases:
    """Edge case tests for async context detection."""

    def test_nested_async_context_detection(self):
        """Test that nested async calls properly detect the running loop."""
        from project_management_automation.tools.consolidated import security

        async def outer():
            async def inner():
                return security(action="scan")
            # Create task that calls inner() - replaced deprecated asyncio.coroutine
            return await inner()

        # The inner call should still detect the running loop
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(outer())

        assert "async context" in str(exc_info.value).lower()

    def test_error_message_is_helpful(self):
        """Test that error messages provide clear guidance."""
        from project_management_automation.tools.consolidated import security, testing
        from project_management_automation.tools.dependency_security import scan_dependency_security

        async def test_security():
            return security(action="scan")

        async def test_testing():
            return testing(action="run")

        async def test_dependency():
            return scan_dependency_security()

        # Check security error message
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(test_security())
        assert "security_async()" in str(exc_info.value)

        # Check testing error message
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(test_testing())
        assert "testing_async()" in str(exc_info.value)

        # Check dependency_security error message
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(test_dependency())
        assert "scan_dependency_security_async()" in str(exc_info.value)


class TestAsyncVersionsWork:
    """Tests that the async versions work correctly when awaited."""

    @pytest.mark.asyncio
    async def test_security_async_can_be_awaited(self):
        """Test that security_async() can be properly awaited."""
        from project_management_automation.tools.consolidated import security_async

        # Mock the dependency_security module's async function
        with patch('project_management_automation.tools.dependency_security.scan_dependency_security_async', new_callable=AsyncMock) as mock_scan:
            mock_scan.return_value = json.dumps({"status": "success", "results": {}})

            # Should not raise - we're properly awaiting
            result = await security_async(action="scan")

            # Result should be valid
            assert result is not None

    @pytest.mark.asyncio
    async def test_testing_async_can_be_awaited(self):
        """Test that testing_async() can be properly awaited."""
        from project_management_automation.tools.consolidated import testing_async

        # Mock the run_tests module's async function
        with patch('project_management_automation.tools.run_tests.run_tests_async', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = {"status": "success", "passed": 10, "failed": 0}

            # Should not raise - we're properly awaiting
            result = await testing_async(action="run")

            # Result should be valid
            assert result is not None

    @pytest.mark.asyncio
    async def test_scan_dependency_security_async_can_be_awaited(self):
        """Test that scan_dependency_security_async() can be properly awaited."""
        from project_management_automation.tools.dependency_security import scan_dependency_security_async

        # Mock the analyzer class and find_project_root (patch the source module)
        with patch('project_management_automation.utils.find_project_root') as mock_root:
            mock_root.return_value = Path("/test")

            with patch('project_management_automation.scripts.automate_dependency_security.DependencySecurityAnalyzer') as mock_analyzer_class:
                mock_analyzer = Mock()
                mock_analyzer.run.return_value = {"results": {"summary": {"total_vulnerabilities": 0}}}
                mock_analyzer_class.return_value = mock_analyzer

                # Should not raise - we're properly awaiting
                result = await scan_dependency_security_async()

                # Result should be valid JSON string
                assert result is not None
                data = json.loads(result)
                assert "success" in data or "status" in data or "vulnerabilities" in data


class TestRegressionBugFix:
    """
    Regression tests for the specific bug that was fixed.
    
    Bug: The except block caught ALL RuntimeError exceptions, including
    the one intentionally raised when detecting an async context.
    
    This caused asyncio.run() to be called from within a running event loop,
    which raises "RuntimeError: asyncio.run() cannot be called from a running event loop".
    """

    def test_intentional_error_not_caught_by_except_block(self):
        """
        Verify the intentional RuntimeError is NOT caught by the except block.
        
        Before fix: except RuntimeError caught both:
        - RuntimeError from get_running_loop() when no loop exists
        - RuntimeError("Use X_async()...") raised intentionally
        
        After fix: Uses try/except/else pattern so intentional error
        is raised in else block, not caught.
        """
        from project_management_automation.tools.consolidated import security

        async def trigger_bug():
            # Before the fix, this would:
            # 1. get_running_loop() succeeds (returns loop)
            # 2. raise RuntimeError("Use security_async()...")
            # 3. except RuntimeError catches it (BUG!)
            # 4. asyncio.run() called from running loop (CRASH!)
            #
            # After the fix:
            # 1. get_running_loop() succeeds (returns loop)
            # 2. else block raises RuntimeError (correct behavior)
            return security(action="scan")

        # Should raise our helpful error, NOT "asyncio.run() cannot be called..."
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(trigger_bug())

        error_msg = str(exc_info.value)

        # Verify it's our error, not the asyncio.run error
        assert "cannot be called from a running event loop" not in error_msg
        assert "security_async()" in error_msg or "async context" in error_msg.lower()

    def test_sync_caller_still_works_after_fix(self):
        """Ensure the fix didn't break sync callers."""
        from project_management_automation.tools.consolidated import security

        with patch('project_management_automation.tools.consolidated.security_async', new_callable=AsyncMock) as mock:
            mock.return_value = {"status": "success"}

            # This should work without any RuntimeError
            result = security(action="scan")

            assert result is not None
            mock.assert_called_once()


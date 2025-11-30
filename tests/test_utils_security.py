"""
Unit Tests for Security Utilities

Tests for path validation, input sanitization, rate limiting, and access control.
"""


# Add project root to path
import sys
import tempfile
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from project_management_automation.utils.security import (
    AccessController,
    AccessLevel,
    # Input validation
    InputValidationError,
    # Path validation
    PathBoundaryError,
    PathValidator,
    # Rate limiting
    RateLimiter,
    get_access_controller,
    get_default_path_validator,
    sanitize_string,
    set_access_controller,
    set_default_path_validator,
    validate_enum,
    validate_identifier,
    validate_path,
    validate_range,
)


class TestPathValidator:
    """Tests for PathValidator class."""

    def test_init_default_root(self):
        """Test PathValidator initializes with cwd as default root."""
        validator = PathValidator()
        assert len(validator.allowed_roots) == 1
        assert validator.allowed_roots[0] == Path.cwd().resolve()

    def test_init_custom_roots(self):
        """Test PathValidator with custom allowed roots."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            assert Path(tmpdir).resolve() in validator.allowed_roots

    def test_is_within_boundary_valid(self):
        """Test is_within_boundary returns True for valid paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            test_file = Path(tmpdir) / "test.txt"
            test_file.touch()
            assert validator.is_within_boundary(test_file) is True

    def test_is_within_boundary_invalid(self):
        """Test is_within_boundary returns False for paths outside boundary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            # Parent directory is outside boundary
            assert validator.is_within_boundary(Path(tmpdir).parent) is False

    def test_is_blocked_git_directory(self):
        """Test is_blocked detects .git directories."""
        validator = PathValidator()
        assert validator.is_blocked(Path("/project/.git/config")) is True
        assert validator.is_blocked(Path("/project/.git")) is True

    def test_is_blocked_env_file(self):
        """Test is_blocked detects .env files."""
        validator = PathValidator()
        assert validator.is_blocked(Path("/project/.env")) is True
        assert validator.is_blocked(Path("/project/.env.local")) is True

    def test_is_blocked_ssh_keys(self):
        """Test is_blocked detects SSH key files."""
        validator = PathValidator()
        assert validator.is_blocked(Path("/home/user/.ssh/id_rsa")) is True
        assert validator.is_blocked(Path("/project/id_rsa")) is True

    def test_is_blocked_safe_file(self):
        """Test is_blocked returns False for safe files."""
        validator = PathValidator()
        assert validator.is_blocked(Path("/project/src/main.py")) is False
        assert validator.is_blocked(Path("/project/README.md")) is False

    def test_validate_valid_path(self):
        """Test validate returns resolved path for valid paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            test_file = Path(tmpdir) / "test.txt"
            test_file.touch()

            result = validator.validate(str(test_file))
            assert result == test_file.resolve()

    def test_validate_path_traversal_attack(self):
        """Test validate blocks path traversal attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])

            # Attempt path traversal
            with pytest.raises(PathBoundaryError) as exc_info:
                validator.validate(f"{tmpdir}/../../../etc/passwd")

            assert "outside allowed boundaries" in str(exc_info.value)

    def test_validate_blocked_pattern(self):
        """Test validate blocks paths matching blocked patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            git_dir = Path(tmpdir) / ".git"
            git_dir.mkdir()

            with pytest.raises(PathBoundaryError) as exc_info:
                validator.validate(str(git_dir))

            assert "blocked pattern" in str(exc_info.value)

    def test_validate_must_exist_missing(self):
        """Test validate raises when must_exist=True and path missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])

            with pytest.raises(PathBoundaryError) as exc_info:
                validator.validate(f"{tmpdir}/nonexistent.txt", must_exist=True)

            assert "does not exist" in str(exc_info.value)

    def test_validate_output_path_creates_parents(self):
        """Test validate_output_path creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            output_path = Path(tmpdir) / "subdir" / "nested" / "output.txt"

            result = validator.validate_output_path(str(output_path))

            assert result.parent.exists()


class TestGlobalPathValidator:
    """Tests for global path validator functions."""

    def test_set_and_get_default_validator(self):
        """Test setting and getting the default path validator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            set_default_path_validator(validator)

            retrieved = get_default_path_validator()
            assert retrieved is validator

    def test_validate_path_convenience(self):
        """Test validate_path convenience function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator(allowed_roots=[Path(tmpdir)])
            set_default_path_validator(validator)

            test_file = Path(tmpdir) / "test.txt"
            test_file.touch()

            result = validate_path(str(test_file))
            assert result == test_file.resolve()


class TestInputValidation:
    """Tests for input validation functions."""

    def test_sanitize_string_valid(self):
        """Test sanitize_string with valid input."""
        result = sanitize_string("Hello, World!")
        assert result == "Hello, World!"

    def test_sanitize_string_max_length(self):
        """Test sanitize_string enforces max length."""
        with pytest.raises(InputValidationError) as exc_info:
            sanitize_string("x" * 100, max_length=50)

        assert "maximum length" in str(exc_info.value)

    def test_sanitize_string_strips_control_chars(self):
        """Test sanitize_string removes control characters."""
        # Include a control character (bell)
        result = sanitize_string("Hello\x07World")
        assert result == "HelloWorld"

    def test_sanitize_string_preserves_newlines(self):
        """Test sanitize_string preserves newlines when allowed."""
        result = sanitize_string("Hello\nWorld", allow_newlines=True)
        assert result == "Hello\nWorld"

    def test_sanitize_string_removes_newlines(self):
        """Test sanitize_string removes newlines when not allowed."""
        result = sanitize_string("Hello\nWorld", allow_newlines=False)
        assert result == "HelloWorld"

    def test_sanitize_string_non_string_input(self):
        """Test sanitize_string rejects non-string input."""
        with pytest.raises(InputValidationError) as exc_info:
            sanitize_string(123)

        assert "Expected string" in str(exc_info.value)

    def test_validate_identifier_valid(self):
        """Test validate_identifier with valid identifiers."""
        assert validate_identifier("my_var") == "my_var"
        assert validate_identifier("MyClass") == "MyClass"
        assert validate_identifier("_private") == "_private"
        assert validate_identifier("with-dash") == "with-dash"

    def test_validate_identifier_invalid(self):
        """Test validate_identifier rejects invalid identifiers."""
        with pytest.raises(InputValidationError):
            validate_identifier("123invalid")  # Starts with number

        with pytest.raises(InputValidationError):
            validate_identifier("has space")  # Contains space

        with pytest.raises(InputValidationError):
            validate_identifier("has.dot")  # Contains dot

    def test_validate_enum_valid(self):
        """Test validate_enum with valid values."""
        allowed = {"red", "green", "blue"}
        assert validate_enum("red", allowed) == "red"
        assert validate_enum("green", allowed) == "green"

    def test_validate_enum_invalid(self):
        """Test validate_enum rejects invalid values."""
        allowed = {"red", "green", "blue"}

        with pytest.raises(InputValidationError) as exc_info:
            validate_enum("yellow", allowed, param_name="color")

        assert "Invalid color" in str(exc_info.value)
        assert "yellow" in str(exc_info.value)

    def test_validate_range_valid(self):
        """Test validate_range with valid values."""
        assert validate_range(5, min_val=0, max_val=10) == 5
        assert validate_range(0, min_val=0) == 0
        assert validate_range(100, max_val=100) == 100

    def test_validate_range_below_min(self):
        """Test validate_range rejects values below minimum."""
        with pytest.raises(InputValidationError) as exc_info:
            validate_range(-1, min_val=0, param_name="count")

        assert "must be >= 0" in str(exc_info.value)

    def test_validate_range_above_max(self):
        """Test validate_range rejects values above maximum."""
        with pytest.raises(InputValidationError) as exc_info:
            validate_range(101, max_val=100, param_name="percentage")

        assert "must be <= 100" in str(exc_info.value)


class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_allow_within_limit(self):
        """Test allow returns True within rate limit."""
        limiter = RateLimiter(calls_per_minute=60, burst_size=10)

        # First 10 calls should be allowed (burst)
        for _ in range(10):
            assert limiter.allow("test") is True

    def test_allow_exceeds_burst(self):
        """Test allow returns False when exceeding burst."""
        limiter = RateLimiter(calls_per_minute=60, burst_size=5)

        # Use up burst
        for _ in range(5):
            limiter.allow("test")

        # Next call should be rate limited
        assert limiter.allow("test") is False

    def test_tokens_refill_over_time(self):
        """Test tokens refill over time."""
        limiter = RateLimiter(calls_per_minute=600, burst_size=1)  # 10/sec

        # Use the token
        assert limiter.allow("test") is True
        assert limiter.allow("test") is False

        # Wait for refill (0.1 sec = 1 token at 10/sec)
        time.sleep(0.15)

        # Should have token again
        assert limiter.allow("test") is True

    def test_separate_keys(self):
        """Test different keys have separate rate limits."""
        limiter = RateLimiter(calls_per_minute=60, burst_size=2)

        # Use up key1
        limiter.allow("key1")
        limiter.allow("key1")
        assert limiter.allow("key1") is False

        # key2 should still have tokens
        assert limiter.allow("key2") is True

    def test_get_wait_time(self):
        """Test get_wait_time returns correct wait time."""
        limiter = RateLimiter(calls_per_minute=60, burst_size=1)

        # Initially no wait
        assert limiter.get_wait_time("test") == 0.0

        # Use token
        limiter.allow("test")

        # Should have wait time > 0
        wait = limiter.get_wait_time("test")
        assert wait > 0


class TestAccessController:
    """Tests for AccessController class."""

    def test_can_execute_default(self):
        """Test can_execute allows tools by default."""
        controller = AccessController()
        assert controller.can_execute("some_tool") is True

    def test_can_execute_denied_tool(self):
        """Test can_execute rejects denied tools."""
        controller = AccessController(denied_tools={"dangerous_tool"})
        assert controller.can_execute("dangerous_tool") is False
        assert controller.can_execute("safe_tool") is True

    def test_deny_and_allow_tool(self):
        """Test deny_tool and allow_tool methods."""
        controller = AccessController()

        # Deny a tool
        controller.deny_tool("my_tool")
        assert controller.can_execute("my_tool") is False

        # Allow it again
        controller.allow_tool("my_tool")
        assert controller.can_execute("my_tool") is True

    def test_read_only_mode(self):
        """Test read_only mode only allows read operations."""
        controller = AccessController(read_only=True)

        # Read operations allowed
        assert controller.can_execute("check_documentation_health") is True
        assert controller.can_execute("project_scorecard") is True

        # Write operations denied
        assert controller.can_execute("sync_todo_tasks") is False
        assert controller.can_execute("batch_approve_tasks") is False

    def test_check_access_raises(self):
        """Test check_access raises InputValidationError when denied."""
        controller = AccessController(denied_tools={"blocked_tool"})

        with pytest.raises(InputValidationError) as exc_info:
            controller.check_access("blocked_tool")

        assert "Access denied" in str(exc_info.value)

    def test_set_tool_level(self):
        """Test set_tool_level configures tool access level."""
        controller = AccessController(read_only=True)

        # Custom tool defaults to write level, so denied in read_only
        assert controller.can_execute("custom_tool") is False

        # Set to read level
        controller.set_tool_level("custom_tool", AccessLevel.READ)
        assert controller.can_execute("custom_tool") is True


class TestGlobalAccessController:
    """Tests for global access controller functions."""

    def test_set_and_get_controller(self):
        """Test setting and getting the global access controller."""
        controller = AccessController(read_only=True)
        set_access_controller(controller)

        retrieved = get_access_controller()
        assert retrieved is controller
        assert retrieved.read_only is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


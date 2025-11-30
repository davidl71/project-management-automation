"""
Tests for CLI mode detection and shell setup commands.
"""

import os
import subprocess
import sys
import unittest
from io import StringIO
from unittest.mock import patch


class TestMCPModeDetection(unittest.TestCase):
    """Test MCP mode auto-detection."""

    def test_mcp_mode_env_var(self):
        """Test detection via EXARP_MCP_MODE env var."""
        from project_management_automation.server import _is_mcp_mode

        with patch.dict(os.environ, {"EXARP_MCP_MODE": "1"}):
            self.assertTrue(_is_mcp_mode())

    def test_mcp_mode_cursor_trace_id(self):
        """Test detection via CURSOR_TRACE_ID env var."""
        from project_management_automation.server import _is_mcp_mode

        # Clear EXARP_MCP_MODE first
        env = os.environ.copy()
        env.pop("EXARP_MCP_MODE", None)
        env["CURSOR_TRACE_ID"] = "test-trace-123"

        with patch.dict(os.environ, env, clear=True):
            with patch('sys.stdin') as mock_stdin:
                mock_stdin.isatty.return_value = True
                # Need to reload to get fresh env
                self.assertTrue(_is_mcp_mode())

    def test_mcp_mode_stdin_not_tty(self):
        """Test detection when stdin is not a TTY (piped input)."""
        from project_management_automation.server import _is_mcp_mode

        # Clear env vars
        env = os.environ.copy()
        env.pop("EXARP_MCP_MODE", None)
        env.pop("CURSOR_TRACE_ID", None)

        with patch.dict(os.environ, env, clear=True):
            with patch('sys.stdin') as mock_stdin:
                mock_stdin.isatty.return_value = False
                self.assertTrue(_is_mcp_mode())

    def test_interactive_mode_tty(self):
        """Test interactive mode when stdin IS a TTY."""
        from project_management_automation.server import _is_mcp_mode

        # Clear env vars that would force MCP mode
        env = os.environ.copy()
        env.pop("EXARP_MCP_MODE", None)
        env.pop("CURSOR_TRACE_ID", None)

        with patch.dict(os.environ, env, clear=True):
            with patch('sys.stdin') as mock_stdin:
                mock_stdin.isatty.return_value = True
                self.assertFalse(_is_mcp_mode())


class TestShellSetup(unittest.TestCase):
    """Test shell setup output."""

    def test_shell_setup_output(self):
        """Test --shell-setup generates valid shell script."""
        from project_management_automation.server import _print_shell_setup

        # Capture stdout
        captured = StringIO()
        with patch('sys.stdout', captured):
            _print_shell_setup("zsh")

        output = captured.getvalue()

        # Check key components
        self.assertIn("alias exarp=", output)
        self.assertIn("xl()", output)  # xl is a function, not alias
        self.assertIn("_exarp_detect()", output)
        self.assertIn("_exarp_tasks()", output)
        self.assertIn("EXARP_CACHE_DIR", output)

    def test_completions_output(self):
        """Test --completions generates valid completions."""
        from project_management_automation.server import _print_completions

        captured = StringIO()
        with patch('sys.stdout', captured):
            _print_completions("zsh")

        output = captured.getvalue()

        self.assertIn("_exarp_commands()", output)
        self.assertIn("compdef", output)
        self.assertIn("--help", output)

    def test_aliases_output(self):
        """Test --aliases generates aliases."""
        from project_management_automation.server import _print_aliases

        captured = StringIO()
        with patch('sys.stdout', captured):
            _print_aliases()

        output = captured.getvalue()

        self.assertIn("alias exarp=", output)
        self.assertIn("alias xs=", output)

    def test_usage_output(self):
        """Test usage help output."""
        from project_management_automation.server import _print_usage

        captured = StringIO()
        with patch('sys.stdout', captured):
            _print_usage()

        output = captured.getvalue()

        self.assertIn("USAGE:", output)
        self.assertIn("--help", output)
        self.assertIn("--shell-setup", output)
        self.assertIn("--mcp", output)
        self.assertIn("uvx exarp", output)


class TestCLIFlags(unittest.TestCase):
    """Test CLI flag handling."""

    def test_help_flag(self):
        """Test --help shows usage."""
        result = subprocess.run(
            [sys.executable, "-m", "project_management_automation.server", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("USAGE:", result.stdout)

    def test_version_flag(self):
        """Test --version shows version."""
        result = subprocess.run(
            [sys.executable, "-m", "project_management_automation.server", "--version"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("exarp", result.stdout)

    def test_shell_setup_flag(self):
        """Test --shell-setup outputs shell config."""
        result = subprocess.run(
            [sys.executable, "-m", "project_management_automation.server", "--shell-setup"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("alias exarp=", result.stdout)

    def test_completions_flag(self):
        """Test --completions outputs completions."""
        result = subprocess.run(
            [sys.executable, "-m", "project_management_automation.server", "--completions"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("compdef", result.stdout)

    def test_aliases_flag(self):
        """Test --aliases outputs aliases."""
        result = subprocess.run(
            [sys.executable, "-m", "project_management_automation.server", "--aliases"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("alias", result.stdout)


class TestInteractiveMode(unittest.TestCase):
    """Test interactive mode behavior."""

    def test_no_args_shows_usage(self):
        """Test running without args in TTY mode shows usage."""
        # Simulate TTY by NOT piping input
        result = subprocess.run(
            [sys.executable, "-m", "project_management_automation.server"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent),
            input=""  # Empty input simulates non-TTY
        )
        # Should show usage (exit 0) since stdin is not TTY
        # Note: In subprocess, stdin is never a TTY
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()


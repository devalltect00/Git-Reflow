# tests/core/dry_run/test_dry_run.py

"""
Tests for dry_run module.

This module tests command execution helpers and Runner.
"""

from subprocess import CompletedProcess
from unittest.mock import Mock, patch

from app.core.dry_run.dry_run import (
    Runner,
    format_command,
)

# -----------------------------------------------------
# Format Command Tests
# -----------------------------------------------------


class TestFormatCommand:
    """
    Tests for format_command().
    """

    def test_format_command_from_list(self):
        """
        Should join list items with spaces.
        """
        result = format_command(["git", "status"])

        assert result == "git status"

    def test_format_command_from_string(self):
        """
        Should return string unchanged.
        """
        result = format_command("git status")

        assert result == "git status"


# -----------------------------------------------------
# Runner Constructor Tests
# -----------------------------------------------------


class TestRunner:
    """
    Tests for Runner.
    """

    def test_init_defaults(self):
        """
        Should initialize with defaults.
        """
        runner = Runner()

        assert runner.get_is_dry_run() is False
        assert runner.get_silent() is False

    def test_init_custom_values(self):
        """
        Should initialize with provided values.
        """
        runner = Runner(
            is_dry_run=True,
            is_silent=True,
        )

        assert runner.get_is_dry_run() is True
        assert runner.get_silent() is True

    # -----------------------------------------------------
    # Dry Run State
    # -----------------------------------------------------

    def test_set_is_dry_run(self):
        """
        Should update dry-run state.
        """
        runner = Runner()

        runner.set_is_dry_run(True)

        assert runner.get_is_dry_run() is True

    def test_set_silent(self):
        """
        Should update silent state.
        """
        runner = Runner()

        runner.set_silent(True)

        assert runner.get_silent() is True

    # -----------------------------------------------------
    # run()
    # -----------------------------------------------------
    # Success
    # -----------------------------------------------------

    @patch("app.core.dry_run.dry_run.subprocess.run")
    def test_run_success(
        self,
        mock_run,
    ):
        """
        Should execute subprocess.
        """
        mock_run.return_value = CompletedProcess(
            args=["git"],
            returncode=0,
        )

        runner = Runner()

        result = runner.run(["git", "status"])

        assert result.returncode == 0

        mock_run.assert_called_once()

    # -----------------------------------------------------
    # Dry Run
    # -----------------------------------------------------

    @patch("app.core.dry_run.dry_run.log_dry_run")
    def test_run_dry_run(
        self,
        mock_log,
    ):
        """
        Should simulate execution.
        """
        runner = Runner(
            is_dry_run=True,
        )

        result = runner.run(["git", "status"])

        assert result is None

        mock_log.assert_called_once()

    # -----------------------------------------------------
    # Error Callback
    # -----------------------------------------------------

    @patch("app.core.dry_run.dry_run.subprocess.run")
    def test_run_calls_on_error(
        self,
        mock_run,
    ):
        """
        Should invoke error callback.
        """
        callback = Mock()

        mock_run.side_effect = __import__("subprocess").CalledProcessError(
            1,
            "git",
        )

        runner = Runner()

        result = runner.run(
            ["git"],
            on_error=callback,
        )

        assert result.returncode == 1

        callback.assert_called_once()

    @patch("app.core.dry_run.dry_run.subprocess.run")
    def test_run_executes_read_only_command_during_dry_run(
        self,
        mock_run,
    ):
        """Dry-run must execute discovery commands needed to build a plan."""
        mock_run.return_value = CompletedProcess(
            args=["git", "tag"],
            returncode=0,
        )
        runner = Runner(is_dry_run=True)

        result = runner.run(
            ["git", "tag"],
            mutates=False,
        )

        assert result.returncode == 0
        mock_run.assert_called_once()

    # -----------------------------------------------------
    # check_output()
    # -----------------------------------------------------
    # Success
    # -----------------------------------------------------

    @patch("app.core.dry_run.dry_run.subprocess.check_output")
    def test_check_output_success(
        self,
        mock_check_output,
    ):
        """
        Should return decoded output.
        """
        mock_check_output.return_value = b"hello"

        runner = Runner()

        result = runner.check_output(
            ["git"],
        )

        assert result == "hello"

    # -----------------------------------------------------
    # Dry Run
    # -----------------------------------------------------

    @patch("app.core.dry_run.dry_run.log_dry_run")
    def test_check_output_dry_run(
        self,
        mock_log,
    ):
        """
        Should simulate output command.
        """
        runner = Runner(
            is_dry_run=True,
        )

        result = runner.check_output(
            ["git"],
        )

        assert result is None

        mock_log.assert_called_once()

    @patch("app.core.dry_run.dry_run.subprocess.check_output")
    def test_check_output_executes_read_only_command_during_dry_run(
        self,
        mock_check_output,
    ):
        """Dry-run must retain output from non-mutating discovery commands."""
        mock_check_output.return_value = b"v1.0.0"
        runner = Runner(is_dry_run=True)

        result = runner.check_output(
            ["git", "tag"],
            mutates=False,
        )

        assert result == "v1.0.0"
        mock_check_output.assert_called_once()

    # -----------------------------------------------------
    # Error Callback
    # -----------------------------------------------------

    @patch("app.core.dry_run.dry_run.subprocess.check_output")
    def test_check_output_calls_on_error(
        self,
        mock_check_output,
    ):
        """
        Should invoke error callback.
        """
        callback = Mock()

        mock_check_output.side_effect = __import__("subprocess").CalledProcessError(
            1,
            "git",
        )

        runner = Runner()

        result = runner.check_output(
            ["git"],
            on_error=callback,
        )

        assert result is None

        callback.assert_called_once()

# tests/core/shared/test_result.py

"""
Tests for CommandResult.

This module tests the shared command execution result model.
"""

from subprocess import CompletedProcess

from app.core.shared.result import CommandResult


class TestCommandResult:
    """
    Tests for CommandResult.
    """

    # =====================================================
    # success
    # =====================================================

    def test_success_returns_true_for_zero_returncode(self):
        """
        Should return True when returncode is 0.
        """
        result = CommandResult(
            returncode=0,
        )

        assert result.success is True

    def test_success_returns_false_for_non_zero_returncode(self):
        """
        Should return False when returncode is not 0.
        """
        result = CommandResult(
            returncode=1,
        )

        assert result.success is False

    # =====================================================
    # failed
    # =====================================================

    def test_failed_returns_false_for_zero_returncode(self):
        """
        Should return False when returncode is 0.
        """
        result = CommandResult(
            returncode=0,
        )

        assert result.failed is False

    def test_failed_returns_true_for_non_zero_returncode(self):
        """
        Should return True when returncode is not 0.
        """
        result = CommandResult(
            returncode=1,
        )

        assert result.failed is True

    # =====================================================
    # from_completed_process
    # =====================================================

    def test_from_completed_process(self):
        """
        Should create CommandResult from
        CompletedProcess.
        """
        process = CompletedProcess(
            args=["git"],
            returncode=0,
        )

        process.stdout = "hello"
        process.stderr = ""

        result = CommandResult.from_completed_process(process)

        assert result.returncode == 0
        assert result.stdout == "hello"
        assert result.stderr == ""

    def test_from_completed_process_handles_none_output(self):
        """
        Should convert None stdout/stderr
        to empty strings.
        """
        process = CompletedProcess(
            args=["git"],
            returncode=0,
        )

        process.stdout = None
        process.stderr = None

        result = CommandResult.from_completed_process(process)

        assert result.stdout == ""
        assert result.stderr == ""

    # =====================================================
    # dry_run
    # =====================================================

    def test_dry_run_returns_successful_result(self):
        """
        Should create a successful dry-run result.
        """
        result = CommandResult.dry_run()

        assert result.returncode == 0
        assert result.stdout == ""
        assert result.stderr == ""
        assert result.skipped is True
        assert result.success is True
        assert result.failed is False

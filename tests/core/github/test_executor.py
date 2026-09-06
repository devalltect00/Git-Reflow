# tests/core/github/test_executor.py

"""
Tests for GitHubExecutor.

This module tests GitHub command execution.
"""

from subprocess import CompletedProcess
from unittest.mock import Mock

import pytest

from app.core.github.executor import GitHubExecutor


class TestGitHubExecutor:
    """
    Tests for GitHubExecutor.
    """

    @pytest.fixture
    def executor(self):
        """
        Create GitHub executor.
        """
        return GitHubExecutor()

    # =====================================================
    # _run
    # =====================================================

    def test_run_returns_command_result(
        self,
        executor,
    ):
        """
        Should convert CompletedProcess into CommandResult.
        """
        executor.runner = Mock()

        executor.runner.run.return_value = CompletedProcess(
            args=["gh", "--version"],
            returncode=0,
            stdout="gh version",
            stderr="",
        )

        result = executor._run(["--version"])

        assert result.success is True
        assert result.stdout == "gh version"
        assert result.stderr == ""

    def test_run_uses_selected_repository(self, tmp_path):
        """Execute GitHub CLI commands from the explicit repository target."""
        executor = GitHubExecutor(repository=tmp_path)
        executor.runner = Mock()
        executor.runner.run.return_value = CompletedProcess(
            args=["gh", "release", "list"],
            returncode=0,
            stdout="",
            stderr="",
        )

        executor._run(["release", "list"], mutates=False)

        assert executor.runner.run.call_args.kwargs["cwd"] == tmp_path.resolve()

    def test_run_returns_dry_run_result(
        self,
        executor,
    ):
        """
        Should return dry-run result when Runner
        returns None.
        """
        executor.runner = Mock()

        executor.runner.run.return_value = None

        result = executor._run(["release"])

        assert result.success is True
        assert result.skipped is True

    # =====================================================
    # Releases
    # =====================================================

    def test_release_exists(
        self,
        executor,
    ):
        """
        Should execute release view command.
        """
        executor._run = Mock()

        executor.release_exists("v1.0.0")

        executor._run.assert_called_once_with(
            [
                "release",
                "view",
                "v1.0.0",
            ],
            check=False,
            mutates=False,
        )

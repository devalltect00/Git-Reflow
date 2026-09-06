# tests/core/repository/test_executor.py

"""Tests for remote repository clone command execution."""

from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import Mock

from app.core.repository import RepositoryExecutor


def test_clone_executes_non_mutating_full_history_clone(tmp_path: Path) -> None:
    """Clone all tags and branches into the managed checkout directory."""
    executor = RepositoryExecutor(dry_run=True)
    executor.runner = Mock()
    executor.runner.run.return_value = CompletedProcess(
        args=["git", "clone"],
        returncode=0,
        stdout="cloned",
        stderr="",
    )
    destination = tmp_path / "checkout"

    result = executor.clone(
        url="https://github.com/example/project.git",
        destination=destination,
    )

    assert result.success is True
    assert result.stdout == "cloned"
    executor.runner.run.assert_called_once_with(
        [
            "git",
            "clone",
            "--no-single-branch",
            "--",
            "https://github.com/example/project.git",
            str(destination),
        ],
        check=False,
        mutates=False,
        cwd=tmp_path,
        stdout=-1,
        stderr=-1,
        text=True,
        encoding="utf-8",
    )


def test_clone_normalizes_command_failure(tmp_path: Path) -> None:
    """Return failed clone output without leaking subprocess details upward."""
    executor = RepositoryExecutor()
    executor.runner = Mock()
    executor.runner.run.return_value = CompletedProcess(
        args=["git", "clone"],
        returncode=128,
        stdout="",
        stderr="authentication failed",
    )

    result = executor.clone(
        url="https://github.com/example/private.git",
        destination=tmp_path / "checkout",
    )

    assert result.failed is True
    assert result.stderr == "authentication failed"


def test_clone_normalizes_skipped_result(tmp_path: Path) -> None:
    """Keep the executor defensive if a custom runner skips the clone."""
    executor = RepositoryExecutor(dry_run=True)
    executor.runner = Mock()
    executor.runner.run.return_value = None

    result = executor.clone(
        url="https://github.com/example/project.git",
        destination=tmp_path / "checkout",
    )

    assert result.success is True
    assert result.skipped is True

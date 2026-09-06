# tests/core/repository/test_workspace.py

"""Tests for managed local and remote repository workspaces."""

from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.core.repository import RepositoryTarget, RepositoryWorkspace
from app.core.shared import CommandResult, RepositoryOperationError


def test_local_workspace_yields_selected_directory(tmp_path: Path) -> None:
    """Use a local target directly without invoking the clone executor."""
    executor = Mock()
    workspace = RepositoryWorkspace(
        RepositoryTarget.resolve(tmp_path),
        executor=executor,
    )

    with workspace.materialize() as repository:
        assert repository == tmp_path.resolve()

    executor.clone.assert_not_called()


def test_remote_workspace_clones_and_cleans_up() -> None:
    """Remove the temporary clone after a successful command invocation."""
    executor = Mock()

    def create_checkout(*, url: str, destination: Path) -> CommandResult:
        """Emulate Git creating the requested checkout directory."""
        assert url == "https://github.com/example/project.git"
        destination.mkdir()
        return CommandResult(returncode=0)

    executor.clone.side_effect = create_checkout
    target = RepositoryTarget.resolve(url="https://github.com/example/project.git")
    workspace = RepositoryWorkspace(target, executor=executor)

    with workspace.materialize() as repository:
        checkout = repository
        assert checkout.exists()
        assert checkout.name == "checkout"

    assert checkout.exists() is False


def test_remote_workspace_displays_configurable_clone_progress(
    monkeypatch,
) -> None:
    """Keep the user informed while a remote clone is running."""

    executor = Mock()
    events: list[object] = []

    def create_checkout(*, url: str, destination: Path) -> CommandResult:
        destination.mkdir()
        return CommandResult(returncode=0)

    @contextmanager
    def fake_progress(message: str, *, enabled: bool):
        events.extend((message, enabled, "started"))
        yield
        events.append("finished")

    executor.clone.side_effect = create_checkout
    monkeypatch.setattr(
        "app.core.repository.workspace.progress_spinner",
        fake_progress,
    )
    workspace = RepositoryWorkspace(
        RepositoryTarget.resolve(url="https://github.com/example/project.git"),
        progress_enabled=False,
        executor=executor,
    )

    with workspace.materialize():
        pass

    assert events == [
        "Cloning target repository",
        False,
        "started",
        "finished",
    ]


def test_remote_workspace_cleans_up_after_workflow_failure() -> None:
    """Remove the temporary clone when downstream command execution fails."""
    executor = Mock()

    def create_checkout(*, url: str, destination: Path) -> CommandResult:
        """Emulate a successful clone before the workflow raises."""
        destination.mkdir()
        return CommandResult(returncode=0)

    executor.clone.side_effect = create_checkout
    workspace = RepositoryWorkspace(
        RepositoryTarget.resolve(url="git@github.com:example/project.git"),
        executor=executor,
    )

    with pytest.raises(RuntimeError, match="workflow failed"):
        with workspace.materialize() as repository:
            checkout = repository
            raise RuntimeError("workflow failed")

    assert checkout.exists() is False


def test_remote_workspace_reports_clone_failure() -> None:
    """Provide actionable remediation when a remote clone fails."""
    executor = Mock()
    executor.clone.return_value = CommandResult(
        returncode=128,
        stderr="authentication failed",
    )
    workspace = RepositoryWorkspace(
        RepositoryTarget.resolve(url="https://github.com/example/private.git"),
        executor=executor,
    )

    with pytest.raises(RepositoryOperationError, match="Git authentication"):
        with workspace.materialize():
            pytest.fail("A failed clone must not yield a repository")


def test_remote_workspace_reports_missing_git() -> None:
    """Translate an unavailable Git executable into actionable remediation."""
    executor = Mock()
    executor.clone.side_effect = FileNotFoundError("git")
    workspace = RepositoryWorkspace(
        RepositoryTarget.resolve(url="https://github.com/example/project.git"),
        executor=executor,
    )

    with pytest.raises(RepositoryOperationError, match="available on PATH"):
        with workspace.materialize():
            pytest.fail("An unavailable Git executable must not yield a checkout")

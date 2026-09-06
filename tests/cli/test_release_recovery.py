# tests/cli/test_release_recovery.py

"""Tests for the release-recovery CLI and replay compatibility alias."""

from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock

from typer.testing import CliRunner

from app.cli.main import app

runner = CliRunner()


def test_releases_recover_help_describes_remote_effect() -> None:
    """Expose the canonical command and its remote-operation warning."""
    result = runner.invoke(
        app,
        ["--no-banner", "releases", "recover", "--help"],
    )

    assert result.exit_code == 0
    assert "Recover Missing Releases" in result.stdout
    assert "Remote effect" in result.stdout
    assert "Reads existing version tags" in result.stdout
    assert "does not directly create a release" in result.stdout


def test_tags_help_marks_replay_as_deprecated() -> None:
    """Expose alias deprecation before a user selects the command."""
    result = runner.invoke(
        app,
        ["--no-banner", "tags", "--help"],
    )

    assert result.exit_code == 0
    assert "replay" in result.stdout
    assert "DEPRECATED" in result.stdout


def test_legacy_replay_help_redirects_to_canonical_command() -> None:
    """Explain the migration path without executing release recovery."""
    result = runner.invoke(
        app,
        ["--no-banner", "tags", "replay", "--help"],
    )

    assert result.exit_code == 0
    assert "DEPRECATED COMMAND" in result.stdout
    assert "reflow releases recover" in result.stdout
    assert "Deletes and re-pushes" in result.stdout


def test_releases_recover_runs_against_explicit_repository(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Run the canonical command with the selected external repository."""
    recovery = Mock()
    recovery_class = Mock(return_value=recovery)
    monkeypatch.setattr(
        "app.cli.commands.reflow.releases.recover.command.ReleaseRecovery",
        recovery_class,
    )

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "--repository",
            str(tmp_path),
            "releases",
            "recover",
            "--only-stable",
            "--limit",
            "3",
        ],
    )

    assert result.exit_code == 0
    assert "Preview" in result.stdout
    assert "none (dry-run)" in result.stdout
    recovery_class.assert_called_once_with(
        dry_run=True,
        is_silent=False,
        delay=2,
        repository=tmp_path.resolve(),
        progress_enabled=True,
    )
    recovery.run.assert_called_once_with(
        only_stable=True,
        limit=3,
    )


def test_releases_recover_materializes_remote_repository(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Recover releases through the origin in a managed temporary clone."""
    captured: dict[str, object] = {}
    checkout = tmp_path / "checkout"
    checkout.mkdir()

    class FakeRepositoryWorkspace:
        """Record workspace input and yield the controlled checkout."""

        def __init__(self, target, **kwargs) -> None:
            captured["target"] = target
            captured["workspace_options"] = kwargs

        @contextmanager
        def materialize(self):
            """Yield a checkout without performing network access."""
            yield checkout

    recovery = Mock()
    recovery_class = Mock(return_value=recovery)
    monkeypatch.setattr(
        "app.cli.commands.reflow.releases.recover.command.RepositoryWorkspace",
        FakeRepositoryWorkspace,
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.releases.recover.command.ReleaseRecovery",
        recovery_class,
    )
    url = "https://github.com/example/project.git"

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "--repository-url",
            url,
            "releases",
            "recover",
        ],
    )

    assert result.exit_code == 0
    assert captured["target"].url == url
    recovery_class.assert_called_once_with(
        dry_run=True,
        is_silent=False,
        delay=2,
        repository=checkout,
        progress_enabled=True,
    )
    recovery.run.assert_called_once_with(only_stable=False, limit=None)


def test_releases_recover_prompts_before_live_operation(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Require confirmation before remote tag deletion and re-push."""
    recovery_class = Mock()
    monkeypatch.setattr(
        "app.cli.commands.reflow.releases.recover.command.ReleaseRecovery",
        recovery_class,
    )

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--no-dry-run",
            "--repository",
            str(tmp_path),
            "releases",
            "recover",
        ],
        input="n\n",
    )

    assert result.exit_code != 0
    recovery_class.assert_not_called()


def test_legacy_replay_warns_and_delegates(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Keep the former command as a clear compatibility alias."""
    recovery = Mock()
    recovery_class = Mock(return_value=recovery)
    monkeypatch.setattr(
        "app.cli.commands.reflow.releases.recover.command.ReleaseRecovery",
        recovery_class,
    )

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "-C",
            str(tmp_path),
            "tags",
            "replay",
        ],
    )

    assert result.exit_code == 0
    assert "DEPRECATED COMMAND" in result.stdout
    assert "reflow releases recover" in result.stdout
    recovery.run.assert_called_once()

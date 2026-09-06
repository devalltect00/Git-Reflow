# tests/cli/test_init_command.py

"""Tests for CLI `init` command argument handling and execution wiring."""

from pathlib import Path

from typer.testing import CliRunner

from app.cli.main import app

runner = CliRunner()


def test_init_command_executes_with_defaults(monkeypatch, tmp_path: Path) -> None:
    """
    Verify `init` executes with default resolved arguments.

    Args:
        monkeypatch: Pytest fixture used to replace InitMain.execute.

    Returns:
        None
    """
    captured = {}

    def fake_execute(self, args):
        captured["args"] = args

    monkeypatch.setattr(
        "app.cli.commands.init.command.InitMain.execute",
        fake_execute,
    )

    result = runner.invoke(
        app,
        ["--no-banner", "--repository", str(tmp_path), "init"],
    )

    assert result.exit_code == 0
    assert "args" in captured
    assert captured["args"].mode == "all"
    assert captured["args"].force_init is False
    assert captured["args"].ask is False


def test_init_command_accepts_flags(monkeypatch, tmp_path: Path) -> None:
    """
    Verify `init` accepts explicit mode/force/ask flags.

    Args:
        monkeypatch: Pytest fixture used to replace InitMain.execute.

    Returns:
        None
    """
    captured = {}

    def fake_execute(self, args):
        captured["args"] = args

    monkeypatch.setattr(
        "app.cli.commands.init.command.InitMain.execute",
        fake_execute,
    )

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--repository",
            str(tmp_path),
            "init",
            "--mode",
            "config",
            "--force",
            "--ask",
        ],
    )

    assert result.exit_code == 0
    assert "args" in captured
    assert captured["args"].mode == "config"
    assert captured["args"].force_init is True
    assert captured["args"].ask is True


def test_init_command_rejects_remote_repository_url() -> None:
    """Explain that initialization output requires a persistent local path."""
    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--repository-url",
            "https://github.com/example/project.git",
            "init",
        ],
    )

    assert result.exit_code != 0
    assert "Clone the repository first" in result.stdout
    assert "Traceback" not in result.stdout


def test_init_dry_run_previews_without_writing(tmp_path: Path) -> None:
    """Report planned initialization without changing the target directory."""
    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "--repository",
            str(tmp_path),
            "init",
            "--mode",
            "config",
        ],
    )

    assert result.exit_code == 0
    assert list(tmp_path.iterdir()) == []
    assert "Dry-run preview completed successfully" in result.stdout
    assert "No project files or directories were changed" in result.stdout
    assert "Configuration files created" not in result.stdout

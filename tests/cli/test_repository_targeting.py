# tests/cli/test_repository_targeting.py

"""Tests for global external-repository CLI targeting."""

from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock

from typer.testing import CliRunner

from app.cli.main import app

runner = CliRunner()


def _normalize_rich_layout(value: str) -> str:
    """Remove whitespace and box-drawing characters inserted by Rich wrapping."""
    return "".join(
        character
        for character in value
        if not character.isspace() and not "\u2500" <= character <= "\u257f"
    )


def _install_remote_workspace(
    monkeypatch,
    *,
    module: str,
    checkout: Path,
    captured: dict[str, object],
) -> None:
    """Replace command workspace materialization with a local test checkout."""

    class FakeRepositoryWorkspace:
        """Record the remote target and yield a controlled checkout."""

        def __init__(self, target, **kwargs) -> None:
            captured["target"] = target
            captured["workspace_options"] = kwargs

        @contextmanager
        def materialize(self):
            """Yield the test checkout without network access."""
            yield checkout

    monkeypatch.setattr(
        f"{module}.RepositoryWorkspace",
        FakeRepositoryWorkspace,
    )


def test_repository_option_reaches_init_workflow(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Pass an explicit repository target through the shared CLI context."""
    captured: dict[str, object] = {}

    def fake_execute(_self, args) -> None:
        """Capture resolved initialization arguments."""
        captured["repository"] = args.repository

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
        ],
    )

    assert result.exit_code == 0
    assert captured["repository"] == tmp_path.resolve()


def test_repository_short_alias_reaches_init_workflow(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Support the familiar ``-C`` short target option."""
    captured: dict[str, object] = {}

    def fake_execute(_self, args) -> None:
        """Capture resolved initialization arguments."""
        captured["repository"] = args.repository

    monkeypatch.setattr(
        "app.cli.commands.init.command.InitMain.execute",
        fake_execute,
    )

    result = runner.invoke(
        app,
        ["--no-banner", "-C", str(tmp_path), "init"],
    )

    assert result.exit_code == 0
    assert captured["repository"] == tmp_path.resolve()


def test_repository_option_rejects_missing_directory(tmp_path: Path) -> None:
    """Fail before running a workflow when its target directory is absent."""
    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--repository",
            str(tmp_path / "missing"),
            "init",
        ],
    )

    assert result.exit_code == 2
    assert "does not exist" in result.stdout
    assert "Solution" in result.stdout
    assert "Traceback" not in result.stdout


def test_repository_url_is_rejected_for_init() -> None:
    """Keep initialization local because temporary output would be discarded."""
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
    assert "requires a local repository path" in result.stdout
    assert "Clone the repository first" in result.stdout
    assert "Traceback" not in result.stdout


def test_repository_path_and_url_options_are_mutually_exclusive(
    tmp_path: Path,
) -> None:
    """Reject ambiguous target selection before command execution."""
    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--repository",
            str(tmp_path),
            "--repository-url",
            "https://github.com/example/project.git",
            "init",
        ],
    )

    assert result.exit_code == 2
    assert "mutually exclusive" in result.stdout
    assert "Pass exactly one repository target option" in result.stdout
    assert "Traceback" not in result.stdout


def test_configured_path_and_url_show_actionable_solution(monkeypatch) -> None:
    """Explain how to correct mutually exclusive configuration targets."""

    config = Mock()
    values = {
        ("repository", "path"): "D:/project/testing_lab/testing_reflow",
        (
            "repository",
            "url",
        ): "https://github.com/devalltect00/testing_reflow.git",
    }
    config.get.side_effect = lambda *keys, default=None: values.get(keys, default)
    monkeypatch.setattr(
        "app.cli.commands.main.command.get_config",
        Mock(return_value=config),
    )

    result = runner.invoke(
        app,
        ["--no-banner", "tags", "convert", "remote", "--yes"],
    )

    assert result.exit_code == 2
    assert "Repository 'path' and 'url' are mutually exclusive" in result.stdout
    assert ".config/reflow/config.toml" in result.stdout
    assert 'path = "D:/path/to/repository"' in result.stdout
    assert 'url = "https://github.com/owner/project.git"' in result.stdout
    assert "Traceback" not in result.stdout


def test_local_tag_conversion_uses_selected_checkout_only(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Route local conversion to the checkout without remote mutation."""
    git = Mock()
    git.is_git_repo.return_value = True
    git.get_all_tags.return_value = ["v1.0.0rc1"]
    create_git_service = Mock(return_value=git)
    replacement = Mock()
    replacement.prepare.return_value = [Mock()]
    replacement_class = Mock(return_value=replacement)
    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.command.create_git_service",
        create_git_service,
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.command.TagReplacementService",
        replacement_class,
    )

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "-C",
            str(tmp_path),
            "tags",
            "convert",
            "local",
        ],
    )

    assert result.exit_code == 0
    assert "Would replace 1 tag(s)" in result.stdout
    assert "No tag objects, local refs, or remote refs were changed" in result.stdout
    assert _normalize_rich_layout(str(tmp_path.resolve())) in _normalize_rich_layout(
        result.stdout
    )
    assert "v1.0.0rc1" in result.stdout
    assert "v1.0.0-rc.1" in result.stdout
    create_git_service.assert_called_once_with(
        dry_run=True,
        is_silent=False,
        repository=tmp_path.resolve(),
    )
    replacement.prepare.assert_called_once()
    assert replacement.prepare.call_args.kwargs["remote"] is False
    replacement.replace_local.assert_not_called()
    replacement.replace_remote.assert_not_called()


def test_remote_tag_conversion_materializes_remote_repository(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Convert tags in the managed checkout selected by a remote URL."""
    captured: dict[str, object] = {}
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    _install_remote_workspace(
        monkeypatch,
        module="app.cli.commands.reflow.tags.convert.command",
        checkout=checkout,
        captured=captured,
    )
    git = Mock()
    git.is_git_repo.return_value = True
    git.get_all_tags.return_value = ["v1.0.0rc1"]
    create_git_service = Mock(return_value=git)
    replacement = Mock()
    replacement.prepare.return_value = [Mock()]
    replacement_class = Mock(return_value=replacement)
    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.command.create_git_service",
        create_git_service,
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.command.TagReplacementService",
        replacement_class,
    )
    url = "https://github.com/example/project.git"

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "--repository-url",
            url,
            "tags",
            "convert",
            "remote",
        ],
    )

    assert result.exit_code == 0
    assert captured["target"].url == url
    assert captured["workspace_options"] == {
        "dry_run": True,
        "is_silent": False,
        "progress_enabled": True,
    }
    assert url in result.stdout
    assert "remote tag replacement" in result.stdout
    create_git_service.assert_called_once_with(
        dry_run=True,
        is_silent=False,
        repository=checkout,
    )
    replacement.prepare.assert_called_once()
    assert replacement.prepare.call_args.kwargs["remote"] is True
    replacement.replace_remote.assert_not_called()


def test_dockerize_uses_target_repository_for_all_services(
    monkeypatch,
    tmp_path: Path,
    mock_dockerize_config: Mock,
) -> None:
    """Route tag discovery and Docker publishing through the same target."""
    git = Mock()
    git.is_git_repo.return_value = True
    git.get_all_tags.return_value = ["v1.0.0"]
    docker = Mock()
    create_git_service = Mock(return_value=git)
    create_docker_service = Mock(return_value=docker)
    dockerizer = Mock()
    dockerizer_class = Mock(return_value=dockerizer)
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.create_git_service",
        create_git_service,
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.create_docker_service",
        create_docker_service,
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.Dockerizer",
        dockerizer_class,
    )
    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "--repo",
            str(tmp_path),
            "dockerize",
        ],
    )

    assert result.exit_code == 0
    assert "Would publish 1 tag(s)" in result.stdout
    assert "No Docker images were built, pushed, tagged, or removed" in result.stdout
    assert "Published 1 tag(s)" not in result.stdout
    expected_service_args = {
        "dry_run": True,
        "is_silent": False,
        "repository": tmp_path.resolve(),
    }
    create_git_service.assert_called_once_with(**expected_service_args)
    create_docker_service.assert_called_once_with(**expected_service_args)
    dockerizer_class.assert_called_once_with(git=git, docker=docker)
    dockerizer.publish_tag.assert_called_once_with(
        image="ghcr.io/devalltect00/testing_reflow",
        tag="v1.0.0",
        latest_tag="v1.0.0",
        keep_local_images=False,
    )


def test_dockerize_materializes_remote_repository(
    monkeypatch,
    tmp_path: Path,
    mock_dockerize_config: Mock,
) -> None:
    """Build images from a managed clone while retaining configured registry."""
    captured: dict[str, object] = {}
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    _install_remote_workspace(
        monkeypatch,
        module="app.cli.commands.reflow.dockerize.command",
        checkout=checkout,
        captured=captured,
    )
    git = Mock()
    git.is_git_repo.return_value = True
    git.get_all_tags.return_value = ["v1.0.0"]
    docker = Mock()
    create_git_service = Mock(return_value=git)
    create_docker_service = Mock(return_value=docker)
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.create_git_service",
        create_git_service,
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.create_docker_service",
        create_docker_service,
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.Dockerizer",
        Mock(return_value=Mock()),
    )
    url = "git@github.com:example/project.git"

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "--repository-url",
            url,
            "dockerize",
        ],
    )

    assert result.exit_code == 0
    assert captured["target"].url == url
    expected_service_args = {
        "dry_run": True,
        "is_silent": False,
        "repository": checkout,
    }
    create_git_service.assert_called_once_with(**expected_service_args)
    create_docker_service.assert_called_once_with(**expected_service_args)

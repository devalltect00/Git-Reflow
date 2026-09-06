# tests/cli/test_error_handling.py

"""Tests for concise, actionable command failure reporting."""

from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock

from typer.testing import CliRunner

from app.cli.main import app
from app.core.shared import DockerOperationError, RepositoryOperationError

runner = CliRunner()


def _mock_docker_workflow(monkeypatch, *, tags: list[str], side_effect) -> Mock:
    """Install Docker workflow doubles and return the Dockerizer mock."""
    git = Mock()
    git.is_git_repo.return_value = True
    git.get_all_tags.return_value = tags
    dockerizer = Mock()
    dockerizer.publish_tag.side_effect = side_effect
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.create_git_service",
        Mock(return_value=git),
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.create_docker_service",
        Mock(return_value=Mock()),
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.command.Dockerizer",
        Mock(return_value=dockerizer),
    )
    return dockerizer


def test_dockerize_total_failure_is_concise_and_unsuccessful(
    monkeypatch,
    tmp_path: Path,
    mock_dockerize_config: Mock,
) -> None:
    """Return status 1 and an actionable reason without a traceback."""
    _mock_docker_workflow(
        monkeypatch,
        tags=["v1.2.3-beta.1"],
        side_effect=DockerOperationError("Docker build failed."),
    )

    result = runner.invoke(
        app,
        ["--no-banner", "-C", str(tmp_path), "dockerize"],
    )

    assert result.exit_code == 1
    assert "Failed to publish 1 image tag(s)" in result.stdout
    assert "Docker build failed" in result.stdout
    assert "Published 0 tag(s)" not in result.stdout
    assert "Traceback" not in result.stdout
    assert "GitLab" not in result.stdout


def test_dockerize_partial_failure_reports_both_outcomes(
    monkeypatch,
    tmp_path: Path,
    mock_dockerize_config: Mock,
) -> None:
    """Keep successful work visible while returning a failed exit status."""
    _mock_docker_workflow(
        monkeypatch,
        tags=["v1.0.0", "v1.1.0"],
        side_effect=[None, DockerOperationError("Registry push failed.")],
    )

    result = runner.invoke(
        app,
        ["--no-banner", "-C", str(tmp_path), "dockerize"],
    )

    assert result.exit_code == 1
    assert "Published : 1" in result.stdout
    assert "Failed    : 1" in result.stdout
    assert "Registry push failed" in result.stdout
    assert "Traceback" not in result.stdout


def test_release_workspace_failure_has_remediation_without_traceback(
    monkeypatch,
) -> None:
    """Handle expected remote-workspace errors at the command boundary."""

    class FailingWorkspace:
        """Raise a controlled repository failure during materialization."""

        def __init__(self, *_args, **_kwargs) -> None:
            pass

        @contextmanager
        def materialize(self):
            """Fail before yielding a checkout."""
            raise RepositoryOperationError("Unable to clone repository.")
            yield  # pragma: no cover

    monkeypatch.setattr(
        "app.cli.commands.reflow.releases.recover.command.RepositoryWorkspace",
        FailingWorkspace,
    )

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "--repository-url",
            "https://github.com/example/project.git",
            "releases",
            "recover",
        ],
    )

    assert result.exit_code == 1
    assert "Release recovery failed" in result.stdout
    assert "Unable to clone repository" in result.stdout
    assert "Verify Git and GitHub CLI authentication" in result.stdout
    assert "Traceback" not in result.stdout


def test_init_unexpected_failure_hides_internal_details(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Reserve programming details for debug logs instead of normal output."""

    def fail(_self, _args) -> None:
        raise RuntimeError("private implementation detail")

    monkeypatch.setattr("app.cli.commands.init.command.InitMain.execute", fail)

    result = runner.invoke(
        app,
        ["--no-banner", "-C", str(tmp_path), "init"],
    )

    assert result.exit_code == 1
    assert "Initialization failed unexpectedly" in result.stdout
    assert "Re-run with --debug" in result.stdout
    assert "private implementation detail" not in result.stdout
    assert "Traceback" not in result.stdout

# tests/cli/test_main_resolver.py

"""Tests for global CLI repository-target resolution."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from app.cli.commands.main.resolver import resolve_main_args, resolve_repository_target
from app.cli.constants.args import CliArgs
from app.core.shared import ConfigurationError


def _config_with_repository(
    *,
    path: str | None = None,
    url: str | None = None,
) -> Mock:
    """Return a configuration double with repository target values."""
    config = Mock()
    values = {
        ("repository", "path"): path,
        ("repository", "url"): url,
    }
    config.get.side_effect = lambda *keys, default=None: values.get(keys, default)
    return config


def test_configured_remote_url_is_selected() -> None:
    """Resolve a remote URL when no target is supplied on the CLI."""
    url = "https://github.com/example/project.git"
    target = resolve_repository_target(
        _config_with_repository(url=url),
        CliArgs(repository=None, repository_url=None),
    )

    assert target.url == url
    assert target.is_remote is True


def test_cli_url_overrides_configured_local_path(tmp_path: Path) -> None:
    """Treat an explicit CLI target as a complete priority-level override."""
    url = "git@github.com:example/project.git"
    target = resolve_repository_target(
        _config_with_repository(path=str(tmp_path)),
        CliArgs(repository=None, repository_url=url),
    )

    assert target.url == url


def test_cli_path_overrides_configured_remote_url(tmp_path: Path) -> None:
    """Allow a local CLI path even when configuration selects URL mode."""
    target = resolve_repository_target(
        _config_with_repository(url="https://github.com/example/project.git"),
        CliArgs(repository=tmp_path, repository_url=None),
    )

    assert target.path == tmp_path.resolve()


def test_configured_path_and_url_are_rejected(tmp_path: Path) -> None:
    """Reject ambiguous configuration instead of guessing a target."""
    with pytest.raises(ConfigurationError, match="mutually exclusive"):
        resolve_repository_target(
            _config_with_repository(
                path=str(tmp_path),
                url="https://github.com/example/project.git",
            ),
            CliArgs(repository=None, repository_url=None),
        )


def test_cli_path_and_url_are_rejected(tmp_path: Path) -> None:
    """Reject mutually exclusive CLI target forms."""
    with pytest.raises(ConfigurationError, match="mutually exclusive"):
        resolve_repository_target(
            _config_with_repository(),
            CliArgs(
                repository=tmp_path,
                repository_url="https://github.com/example/project.git",
            ),
        )


def test_main_args_resolve_configured_progress_visibility(tmp_path: Path) -> None:
    """Propagate the shared progress setting into command execution state."""

    config = _config_with_repository(path=str(tmp_path))

    def resolve(cli_value, config_keys, default=None):
        if tuple(config_keys) == ("cli", "progress", "enabled"):
            return False
        return cli_value if cli_value is not None else default

    config.resolve.side_effect = resolve
    args = resolve_main_args(
        config,
        CliArgs(
            no_banner=None,
            help=None,
            version=None,
            dry_run=None,
            debug=None,
            log_level=None,
            repository=None,
            repository_url=None,
        ),
    )

    assert args.progress_enabled is False

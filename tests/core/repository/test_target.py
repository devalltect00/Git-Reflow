# tests/core/repository/test_target.py

"""Tests for validated repository target resolution."""

from pathlib import Path

import pytest

from app.core.repository import RepositoryTarget
from app.core.shared import ConfigurationError


def test_resolve_defaults_to_base_directory(tmp_path: Path) -> None:
    """Use the invocation directory when no target is supplied."""
    target = RepositoryTarget.resolve(None, base_directory=tmp_path)

    assert target.path == tmp_path.resolve()


def test_resolve_relative_path_from_base_directory(tmp_path: Path) -> None:
    """Resolve configured relative targets from the invocation directory."""
    repository = tmp_path / "external-repository"
    repository.mkdir()

    target = RepositoryTarget.resolve(
        "external-repository",
        base_directory=tmp_path,
    )

    assert target.path == repository.resolve()


def test_resolve_accepts_absolute_directory(tmp_path: Path) -> None:
    """Keep an absolute repository directory as the selected target."""
    target = RepositoryTarget.resolve(tmp_path)

    assert target.path == tmp_path.resolve()


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/example/project.git",
        "http://gitlab.example.com/group/project.git",
        "ssh://git@github.com/example/project.git",
        "git://github.com/example/project.git",
        "git@github.com:example/project.git",
    ],
)
def test_resolve_accepts_supported_remote_urls(url: str) -> None:
    """Keep supported credential-free Git URLs as remote targets."""
    target = RepositoryTarget.resolve(url=url)

    assert target.url == url
    assert target.path is None
    assert target.is_remote is True
    assert target.is_local is False
    assert target.display == url


def test_local_target_properties(tmp_path: Path) -> None:
    """Describe an existing directory as a local target."""
    target = RepositoryTarget.resolve(tmp_path)

    assert target.is_local is True
    assert target.is_remote is False
    assert target.display == str(tmp_path.resolve())
    assert target.require_local(command="reflow init") == tmp_path.resolve()


def test_require_local_rejects_remote_target() -> None:
    """Explain how to use a local-only command with a remote repository."""
    target = RepositoryTarget.resolve(url="https://github.com/example/project.git")

    with pytest.raises(ConfigurationError, match="requires a local repository"):
        target.require_local(command="reflow init")


def test_resolve_rejects_path_and_url_together(tmp_path: Path) -> None:
    """Require one target form at each configuration priority level."""
    with pytest.raises(ConfigurationError, match="mutually exclusive"):
        RepositoryTarget.resolve(
            tmp_path,
            url="https://github.com/example/project.git",
        )


@pytest.mark.parametrize(
    ("url", "message"),
    [
        ("", "empty"),
        ("github.com/example/project", "Unsupported"),
        ("ftp://github.com/example/project.git", "Unsupported"),
        ("https://github.com", "host and repository path"),
        ("https://token@github.com/example/project.git", "credentials"),
        ("https://user:token@github.com/example/project.git", "credentials"),
        ("https://github.com/example/project.git?token=secret", "query"),
        ("https://github.com/example/project.git#main", "fragments"),
    ],
)
def test_resolve_rejects_unsafe_or_invalid_remote_urls(
    url: str,
    message: str,
) -> None:
    """Reject malformed URLs and URLs that could expose credentials."""
    with pytest.raises(ConfigurationError, match=message):
        RepositoryTarget.resolve(url=url)


def test_target_requires_exactly_one_target_form(tmp_path: Path) -> None:
    """Protect the target model from empty and ambiguous construction."""
    with pytest.raises(ConfigurationError, match="exactly one"):
        RepositoryTarget()

    with pytest.raises(ConfigurationError, match="exactly one"):
        RepositoryTarget(
            path=tmp_path,
            url="https://github.com/example/project.git",
        )


def test_resolve_rejects_missing_path(tmp_path: Path) -> None:
    """Reject a target that does not exist."""
    missing = tmp_path / "missing"

    with pytest.raises(ConfigurationError, match="does not exist"):
        RepositoryTarget.resolve(missing)


def test_resolve_rejects_file(tmp_path: Path) -> None:
    """Reject a file because workflows require a directory target."""
    file_target = tmp_path / "not-a-directory.txt"
    file_target.write_text("content", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="not a directory"):
        RepositoryTarget.resolve(file_target)

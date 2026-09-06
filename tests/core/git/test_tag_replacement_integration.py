# tests/core/git/test_tag_replacement_integration.py

"""Git integration tests for local and remote atomic tag replacement."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from app.cli.main import app

runner = CliRunner()


def _git(
    repository: Path,
    *args: str,
    input_text: str | None = None,
    env: dict[str, str] | None = None,
) -> str:
    """Run Git in one disposable test repository and return stdout."""

    result = subprocess.run(
        ["git", *args],
        cwd=repository,
        check=True,
        text=True,
        encoding="utf-8",
        input=input_text,
        capture_output=True,
        env=env,
    )
    return result.stdout.strip()


def _repository(tmp_path: Path) -> Path:
    """Create a disposable repository with one commit."""

    repository = tmp_path / "work"
    repository.mkdir()
    _git(repository, "init")
    _git(repository, "config", "user.name", "Test User")
    _git(repository, "config", "user.email", "test@example.com")
    (repository / "README.md").write_text("test\n", encoding="utf-8")
    _git(repository, "add", "README.md")
    _git(repository, "commit", "-m", "initial")
    return repository


def _annotated_tag(repository: Path, tag: str) -> None:
    """Create one tag with stable identity, timestamp, timezone, and message."""

    env = os.environ.copy()
    env.update(
        {
            "GIT_COMMITTER_NAME": "Release Bot",
            "GIT_COMMITTER_EMAIL": "release@example.com",
            "GIT_COMMITTER_DATE": "1700000000 +0700",
        }
    )
    _git(repository, "tag", "-a", tag, "-m", "Release notes", env=env)


def test_local_replacement_preserves_complete_unsigned_annotated_metadata(
    tmp_path: Path,
) -> None:
    """Rename only the tag header while replacing refs transactionally."""

    repository = _repository(tmp_path)
    _annotated_tag(repository, "v1.2.3b1")
    original = _git(repository, "cat-file", "tag", "refs/tags/v1.2.3b1")

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "-C",
            str(repository),
            "tags",
            "convert",
            "local",
            "--yes",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert _git(repository, "tag") == "v1.2.3-beta.1"
    renamed = _git(repository, "cat-file", "tag", "refs/tags/v1.2.3-beta.1")
    assert renamed == original.replace("tag v1.2.3b1", "tag v1.2.3-beta.1")
    assert "Release Bot <release@example.com> 1700000000 +0700" in renamed


def test_local_replacement_preserves_lightweight_tag_type(tmp_path: Path) -> None:
    """Point a renamed lightweight tag at the same object without annotation."""

    repository = _repository(tmp_path)
    _git(repository, "tag", "v1.2.3b1")
    source_oid = _git(repository, "rev-parse", "refs/tags/v1.2.3b1")

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "-C",
            str(repository),
            "tags",
            "convert",
            "local",
            "-y",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert _git(repository, "cat-file", "-t", "refs/tags/v1.2.3-beta.1") == "commit"
    assert _git(repository, "rev-parse", "refs/tags/v1.2.3-beta.1") == source_oid


def test_local_dry_run_changes_neither_refs_nor_object_database(tmp_path: Path) -> None:
    """Prove simulation stops before mktag and update-ref."""

    repository = _repository(tmp_path)
    _annotated_tag(repository, "v1.2.3b1")
    before_objects = _git(repository, "count-objects", "-v")

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "-C",
            str(repository),
            "tags",
            "convert",
            "local",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert _git(repository, "tag") == "v1.2.3b1"
    assert _git(repository, "count-objects", "-v") == before_objects
    assert "No tag objects, local refs, or remote refs were changed" in result.stdout


def test_remote_replacement_deletes_source_and_preserves_local_refs(
    tmp_path: Path,
) -> None:
    """Use one atomic push for remote creation/deletion without local ref edits."""

    repository = _repository(tmp_path)
    remote = tmp_path / "remote.git"
    remote.mkdir()
    _git(remote, "init", "--bare")
    _git(repository, "remote", "add", "origin", str(remote))
    _annotated_tag(repository, "v1.2.3b1")
    _git(repository, "push", "origin", "refs/tags/v1.2.3b1")

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "-C",
            str(repository),
            "tags",
            "convert",
            "remote",
            "--yes",
        ],
    )

    assert result.exit_code == 0, result.stdout
    remote_tags = _git(remote, "tag").splitlines()
    assert remote_tags == ["v1.2.3-beta.1"]
    assert _git(repository, "tag") == "v1.2.3b1"
    assert _git(remote, "cat-file", "-t", "refs/tags/v1.2.3-beta.1") == "tag"


def test_remote_dry_run_changes_no_local_or_remote_git_state(tmp_path: Path) -> None:
    """Inspect a real bare remote without creating objects or changing refs."""

    repository = _repository(tmp_path)
    remote = tmp_path / "remote.git"
    remote.mkdir()
    _git(remote, "init", "--bare")
    _git(repository, "remote", "add", "origin", str(remote))
    _annotated_tag(repository, "v1.2.3b1")
    _git(repository, "push", "origin", "refs/tags/v1.2.3b1")
    local_objects = _git(repository, "count-objects", "-v")
    remote_objects = _git(remote, "count-objects", "-v")

    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--dry-run",
            "-C",
            str(repository),
            "tags",
            "convert",
            "remote",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert _git(repository, "tag") == "v1.2.3b1"
    assert _git(remote, "tag") == "v1.2.3b1"
    assert _git(repository, "count-objects", "-v") == local_objects
    assert _git(remote, "count-objects", "-v") == remote_objects
    assert "No tag objects, local refs, or remote refs were changed" in result.stdout

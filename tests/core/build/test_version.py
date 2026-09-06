"""Tests for Docker and distribution build-version resolution."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock

from app.core.build.version import (
    resolve_repository_version,
    version_from_git_description,
)


class TestVersionFromGitDescription:
    """Test conversion of supported Git tag forms to package versions."""

    def test_exact_semver_release(self) -> None:
        """An exact prefixed SemVer tag becomes its public package version."""

        assert version_from_git_description("v1.0.0-0-gabc1234") == "1.0.0"

    def test_semver_release_after_additional_commits(self) -> None:
        """Commit distance is represented as a post release."""

        assert version_from_git_description("1.0.0-4-gabc1234") == "1.0.0.post4"

    def test_semver_prerelease_is_normalized_for_python(self) -> None:
        """SemVer RC spelling converts to a valid PEP 440 package version."""

        assert version_from_git_description("v1.0.0-rc.1-0-gabc1234") == "1.0.0rc1"

    def test_untagged_description_uses_fallback(self) -> None:
        """A revision-only description cannot invent a release version."""

        assert version_from_git_description("abc1234", fallback="0.0.0") == "0.0.0"


class TestResolveRepositoryVersion:
    """Test the read-only Git command boundary."""

    def test_runs_git_without_a_shell(self, tmp_path: Path) -> None:
        """Repository discovery uses an argument list and ``shell=False``."""

        runner = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=["git", "describe"],
                returncode=0,
                stdout="v1.0.0-rc.1-3-gabc1234\n",
                stderr="",
            )
        )

        version = resolve_repository_version(tmp_path, runner=runner)

        assert version == "1.0.0rc1.post3"
        runner.assert_called_once_with(
            ["git", "describe", "--tags", "--long", "--always"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
            shell=False,
        )

    def test_git_failure_uses_fallback(self, tmp_path: Path) -> None:
        """Unavailable repository metadata returns the explicit fallback."""

        runner = MagicMock(side_effect=FileNotFoundError("git missing"))

        version = resolve_repository_version(
            tmp_path,
            fallback="0.0.0",
            runner=runner,
        )

        assert version == "0.0.0"

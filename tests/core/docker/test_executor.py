# tests/core/docker/test_executor.py

"""
Tests for DockerExecutor.

This module tests Docker command execution.
"""

from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import Mock

import pytest

from app.core.docker.executor import DockerExecutor


class TestDockerExecutor:
    """
    Tests for DockerExecutor.
    """

    @pytest.fixture
    def executor(self):
        """
        Create Docker executor.
        """
        return DockerExecutor()

    # =====================================================
    # _run
    # =====================================================

    def test_run_returns_command_result(
        self,
        executor,
    ):
        """
        Should convert CompletedProcess into CommandResult.
        """
        executor.runner = Mock()

        executor.runner.run.return_value = CompletedProcess(
            args=["docker", "--version"],
            returncode=0,
            stdout="docker version",
            stderr="",
        )

        result = executor._run(["--version"])

        assert result.success is True
        assert result.stdout == "docker version"

    def test_run_uses_selected_repository(self, tmp_path):
        """Execute Docker commands from the explicit repository target."""
        executor = DockerExecutor(repository=tmp_path)
        executor.runner = Mock()
        executor.runner.run.return_value = CompletedProcess(
            args=["docker", "version"],
            returncode=0,
            stdout="",
            stderr="",
        )

        executor._run(["version"])

        assert executor.runner.run.call_args.kwargs["cwd"] == tmp_path.resolve()

    def test_run_returns_dry_run_result(
        self,
        executor,
    ):
        """
        Should return dry-run result.
        """
        executor.runner = Mock()

        executor.runner.run.return_value = None

        result = executor._run(["build"])

        assert result.success is True
        assert result.skipped is True

    # =====================================================
    # Build
    # =====================================================

    def test_build_image(
        self,
        executor,
    ):
        """
        Should execute image build command.
        """
        executor._run = Mock()

        executor.build_image(
            "example",
            "latest",
        )

        executor._run.assert_called_once_with(
            [
                "build",
                "-t",
                "example:latest",
                str(Path.cwd()),
            ],
            check=True,
        )

    def test_build_image_uses_explicit_context(
        self,
        executor,
        tmp_path,
    ):
        """Build from the explicitly supplied repository worktree."""
        executor._run = Mock()

        executor.build_image(
            "example",
            "v1.0.0",
            context=tmp_path,
        )

        executor._run.assert_called_once_with(
            [
                "build",
                "-t",
                "example:v1.0.0",
                str(tmp_path),
            ],
            check=True,
        )

    # =====================================================
    # Tag
    # =====================================================

    def test_tag_image(
        self,
        executor,
    ):
        """
        Should execute image tag command.
        """
        executor._run = Mock()

        executor.tag_image(
            "example",
            "latest",
            "v1.0.0",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "example:latest",
                "example:v1.0.0",
            ],
            check=True,
        )

    # =====================================================
    # Push
    # =====================================================

    def test_push_image(
        self,
        executor,
    ):
        """
        Should execute image push command.
        """
        executor._run = Mock()

        executor.push_image(
            "example",
            "latest",
        )

        executor._run.assert_called_once_with(
            [
                "push",
                "example:latest",
            ],
            check=True,
        )

    # =====================================================
    # Cleanup
    # =====================================================

    def test_remove_local_image(
        self,
        executor,
    ):
        """
        Should execute image removal command.
        """
        executor._run = Mock()

        executor.remove_local_image(
            "example",
            "latest",
        )

        executor._run.assert_called_once_with(
            [
                # "image",
                # "rm",
                "rmi",
                "-f",
                "example:latest",
            ],
            check=False,
        )

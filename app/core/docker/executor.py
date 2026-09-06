# app/core/docker/executor.py

"""
Docker command executor.

This module contains the low-level Docker command execution layer.

Responsibilities:
- Execute Docker commands
- Return CommandResult objects
- Support dry-run mode
- Support silent mode

This module does NOT:
- Contain business logic
- Make workflow decisions
- Decide which images should be built
- Decide which tags should be pushed

Those responsibilities belong to DockerService.
"""

import subprocess
from pathlib import Path

from app.core.dry_run.dry_run_support import DryRunSupport
from app.core.shared.result import CommandResult


class DockerExecutor(DryRunSupport):
    """
    Low-level Docker command executor.

    This class is responsible only for executing Docker commands
    and returning normalized CommandResult objects.

    It should remain small, reusable, and free from
    business logic.
    """

    def __init__(
        self,
        dry_run: bool = False,
        is_silent: bool = False,
        repository: Path | None = None,
    ) -> None:
        """
        Initialize Docker executor.

        Args:
            dry_run (bool):
                Enable dry-run mode.

            is_silent (bool):
                Disable command logging.

            repository (Path | None):
                Working directory for Docker commands and default build
                context.
        """
        super().__init__(
            dry_run=dry_run,
            is_silent=is_silent,
        )
        self.repository = (repository or Path.cwd()).resolve()

    # =====================================================
    # Dry Run
    # =====================================================

    def get_is_dry_run(self) -> bool:
        """
        Get current dry-run state.

        Returns:
            bool:
                Current dry-run state.
        """
        return self.runner.get_is_dry_run()

    def set_is_dry_run(
        self,
        is_dry_run: bool,
    ) -> None:
        """
        Set dry-run mode.

        Args:
            is_dry_run (bool):
                New dry-run state.
        """
        self.runner.set_is_dry_run(is_dry_run)

    def get_silent(self) -> bool:
        """
        Get current silent mode.

        Returns:
            bool:
                Current silent state.
        """
        return self.runner.get_silent()

    def set_silent(
        self,
        is_silent: bool,
    ) -> None:
        """
        Set silent mode.

        Args:
            is_silent (bool):
                New silent state.
        """
        self.runner.set_silent(is_silent)

    # =====================================================
    # Internal
    # =====================================================

    def _run(
        self,
        args: list[str],
        *,
        check: bool = False,
    ) -> CommandResult:
        """
        Execute a Docker command.

        Args:
            args (list[str]):
                Docker arguments without the 'docker' prefix.

            check (bool):
                Raise on non-zero return code.

        Returns:
            CommandResult:
                Normalized command result.
        """
        result = self.runner.run(
            ["docker", *args],
            check=check,
            mutates=True,
            cwd=self.repository,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

        if result is None:
            return CommandResult.dry_run()

        return CommandResult.from_completed_process(result)

    # =====================================================
    # Images
    # =====================================================

    def build_image(
        self,
        image: str,
        tag: str,
        context: Path | None = None,
    ) -> CommandResult:
        """
        Build a Docker image.

        Command:
            docker build -t <image>:<tag> .

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.

            context (Path | None):
                Explicit Docker build context. Defaults to the selected
                repository.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "build",
                "-t",
                f"{image}:{tag}",
                str(context or self.repository),
            ],
            check=True,
        )

    def tag_image(
        self,
        image: str,
        source_tag: str,
        target_tag: str,
    ) -> CommandResult:
        """
        Create a new image tag.

        Command:
            docker tag <image>:<source_tag> <image>:<target_tag>

        Args:
            image (str):
                Image name.

            source_tag (str):
                Existing tag.

            target_tag (str):
                New tag.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "tag",
                f"{image}:{source_tag}",
                f"{image}:{target_tag}",
            ],
            check=True,
        )

    def push_image(
        self,
        image: str,
        tag: str,
    ) -> CommandResult:
        """
        Push an image to a registry.

        Command:
            docker push <image>:<tag>

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "push",
                f"{image}:{tag}",
            ],
            check=True,
        )

    def remove_local_image(
        self,
        image: str,
        tag: str,
    ) -> CommandResult:
        """
        Remove a local image.

        Command:
            docker rmi -f <image>:<tag>

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "rmi",
                "-f",
                f"{image}:{tag}",
            ],
            check=False,
        )

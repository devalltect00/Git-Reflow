# app/core/docker/protocol.py

"""
Docker executor protocol.

This module defines the contract used by DockerService.

The goal is to allow DockerService to depend on an abstraction
instead of a specific implementation.

Any executor that implements this protocol can be used by
DockerService.

Examples:
- DockerExecutor
- MockDockerExecutor
"""

from pathlib import Path
from typing import Protocol

from app.core.shared.result import CommandResult


class IDockerExecutor(Protocol):
    """
    Contract for Docker command execution.

    Implementations are responsible for executing Docker
    commands and returning normalized CommandResult objects.

    Business logic belongs in DockerService.
    """

    # =====================================================
    # Dry Run
    # =====================================================

    def get_is_dry_run(self) -> bool:
        """
        Get current dry-run status.

        Returns:
            bool:
                True if dry-run mode is enabled.
        """
        ...

    def set_is_dry_run(self, is_dry_run: bool) -> None:
        """
        Enable or disable dry-run mode.

        Args:
            is_dry_run (bool):
                New dry-run state.
        """
        ...

    def get_silent(self) -> bool:
        """
        Get current silent mode status.

        Returns:
            bool:
                True if silent mode is enabled.
        """
        ...

    def set_silent(self, is_silent: bool) -> None:
        """
        Enable or disable silent mode.

        Args:
            is_silent (bool):
                New silent state.
        """
        ...

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

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.

            context (Path | None):
                Docker build context.
        """
        ...

    def tag_image(
        self,
        image: str,
        source_tag: str,
        target_tag: str,
    ) -> CommandResult:
        """
        Create a new image tag.

        Args:
            image (str):
                Image name.

            source_tag (str):
                Existing tag.

            target_tag (str):
                New tag.
        """
        ...

    def push_image(
        self,
        image: str,
        tag: str,
    ) -> CommandResult:
        """
        Push an image to a registry.

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.
        """
        ...

    def remove_local_image(
        self,
        image: str,
        tag: str,
    ) -> CommandResult:
        """
        Remove a local image.

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.
        """
        ...

# app/core/docker/service.py

"""
Docker service layer.

This module contains high-level Docker operations used by Reflow.

Responsibilities:
- Image build operations
- Image tagging operations
- Image push operations
- Local image cleanup

This module does not execute Docker commands directly.

All command execution is delegated to a Docker executor.
"""

import logging
from pathlib import Path

from app.core.decorators.log_decorators import log_execution
from app.core.docker.protocol import IDockerExecutor
from app.core.shared.exceptions import DockerOperationError

logger = logging.getLogger(__name__)


class DockerService:
    """
    High-level Docker operations.

    This class contains Docker-related business logic used by
    Reflow.

    It depends on an executor abstraction instead of a specific
    implementation.
    """

    @log_execution
    def __init__(
        self,
        executor: IDockerExecutor,
    ) -> None:
        """
        Initialize Docker service.

        Args:
            executor (IDockerExecutor):
                Docker command executor.
        """
        self.executor = executor

    # =====================================================
    # Images
    # =====================================================

    @log_execution
    def build_image(
        self,
        image: str,
        tag: str,
        context: Path | None = None,
    ) -> None:
        """
        Build a Docker image.

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.

            context (Path | None):
                Source worktree used as the Docker build context.

        Raises:
            DockerOperationError:
                If build fails.
        """
        logger.debug(
            "Building image '%s:%s'",
            image,
            tag,
        )

        result = self.executor.build_image(
            image=image,
            tag=tag,
            context=context,
        )

        if not result.success:
            logger.debug(
                "Failed to build image '%s:%s'",
                image,
                tag,
            )

            raise DockerOperationError(f"Failed to build Docker image '{image}:{tag}'.")

    @log_execution
    def tag_image(
        self,
        image: str,
        source_tag: str,
        target_tag: str,
    ) -> None:
        """
        Create a new image tag.

        Args:
            image (str):
                Image name.

            source_tag (str):
                Existing image tag.

            target_tag (str):
                New image tag.

        Raises:
            DockerOperationError:
                If tagging fails.
        """
        logger.debug(
            "Tagging image '%s:%s' -> '%s:%s'",
            image,
            source_tag,
            image,
            target_tag,
        )

        result = self.executor.tag_image(
            image=image,
            source_tag=source_tag,
            target_tag=target_tag,
        )

        if not result.success:
            logger.debug(
                "Failed to tag image '%s:%s' -> '%s:%s'",
                image,
                source_tag,
                image,
                target_tag,
            )

            raise DockerOperationError(
                f"Failed to tag image '{image}:{source_tag}' as '{image}:{target_tag}'."
            )

    @log_execution
    def push_image(
        self,
        image: str,
        tag: str,
    ) -> None:
        """
        Push a Docker image.

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.

        Raises:
            DockerOperationError:
                If push fails.
        """
        logger.debug(
            "Pushing image '%s:%s'",
            image,
            tag,
        )

        result = self.executor.push_image(
            image=image,
            tag=tag,
        )

        if not result.success:
            logger.debug(
                "Failed to push image '%s:%s'",
                image,
                tag,
            )

            raise DockerOperationError(f"Failed to push Docker image '{image}:{tag}'.")

    @log_execution
    def remove_local_image(
        self,
        image: str,
        tag: str,
    ) -> None:
        """
        Remove a local Docker image.

        This operation is best-effort.
        Failure should not stop the workflow.

        Args:
            image (str):
                Image name.

            tag (str):
                Image tag.
        """
        logger.debug(
            "Removing local image '%s:%s'",
            image,
            tag,
        )

        self.executor.remove_local_image(
            image=image,
            tag=tag,
        )

    # =====================================================
    # Executor Access
    # =====================================================

    @log_execution
    def get_is_dry_run(self) -> bool:
        """
        Get current dry-run state.

        Returns:
            bool:
                Current dry-run state.
        """
        return self.executor.get_is_dry_run()

    @log_execution
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
        self.executor.set_is_dry_run(is_dry_run)

    @log_execution
    def get_silent(self) -> bool:
        """
        Get current silent mode.

        Returns:
            bool:
                Current silent state.
        """
        return self.executor.get_silent()

    @log_execution
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
        self.executor.set_silent(is_silent)

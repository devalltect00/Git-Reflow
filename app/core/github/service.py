# app/core/github/service.py

"""
GitHub service layer.

This module contains high-level GitHub operations used by Reflow.

Responsibilities:
- Release existence checks
- GitHub-related business logic
- Configuration-independent workflow operations

This module does not execute GitHub CLI commands directly.

All command execution is delegated to a GitHub executor.
"""

import logging

from app.core.decorators.log_decorators import log_execution
from app.core.github.protocol import IGitHubExecutor

logger = logging.getLogger(__name__)


class GitHubService:
    """
    High-level GitHub operations.

    This class contains GitHub-related business logic used by
    Reflow.

    It depends on an executor abstraction instead of a specific
    implementation.
    """

    @log_execution
    def __init__(
        self,
        executor: IGitHubExecutor,
    ) -> None:
        """
        Initialize GitHub service.

        Args:
            executor (IGitHubExecutor):
                GitHub command executor.
        """
        self.executor = executor

    # =====================================================
    # Releases
    # =====================================================

    @log_execution
    def release_exists(
        self,
        tag: str,
    ) -> bool:
        """
        Check whether a GitHub release already exists.

        Args:
            tag (str):
                Release tag.

        Returns:
            bool:
                True if the release exists.
        """
        if not tag:
            logger.warning("Empty release tag received")
            return False

        logger.debug(
            "Checking GitHub release '%s'",
            tag,
        )

        result = self.executor.release_exists(tag)

        return result.success

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

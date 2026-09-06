# app/core/github/protocol.py

"""
GitHub executor protocol.

This module defines the contract used by GitHubService.

The goal is to allow GitHubService to depend on an abstraction
instead of a specific implementation.

Any executor that implements this protocol can be used by
GitHubService.

Examples:
- GitHubExecutor
- MockGitHubExecutor
"""

from typing import Protocol

from app.core.shared.result import CommandResult


class IGitHubExecutor(Protocol):
    """
    Contract for GitHub command execution.

    Implementations are responsible for executing GitHub CLI
    commands and returning normalized CommandResult objects.

    Business logic belongs in GitHubService.
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
    # Releases
    # =====================================================

    def release_exists(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Check whether a GitHub release exists.

        Args:
            tag (str):
                Release tag.

        Returns:
            CommandResult
        """
        ...

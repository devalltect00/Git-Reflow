# app/core/git/protocol.py

"""
Git executor protocol.

This module defines the contract used by GitService.

The goal is to allow GitService to depend on an abstraction
instead of a specific implementation.

Any executor that implements this protocol can be used by
GitService.

Examples:
- GitExecutor
- MockGitExecutor (tests)
- Future Git providers
"""

from pathlib import Path
from typing import Protocol

from app.core.git.models import TagRefReplacement
from app.core.shared.result import CommandResult


class IGitExecutor(Protocol):
    """
    Contract for Git command execution.

    Implementations are responsible for running Git commands
    and returning normalized CommandResult objects.

    This protocol contains only low-level Git operations.

    Business logic belongs in GitService.
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
                True if command logging is disabled.
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
    # Repository
    # =====================================================

    def rev_parse_inside_work_tree(self) -> CommandResult:
        """
        Check whether current directory is inside a Git repository.
        """
        ...

    def get_all_tags(self) -> CommandResult:
        """
        Get all tags sorted by creation date.
        """
        ...

    def get_tag_commit_sha(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Get commit SHA referenced by a tag.

        Args:
            tag (str):
                Tag name.
        """
        ...

    def get_tag_message(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Get annotated tag message.

        Args:
            tag (str):
                Tag name.
        """
        ...

    def get_tag_ref_oid(self, tag: str) -> CommandResult:
        """Resolve the object ID stored directly in a tag reference."""
        ...

    def get_tag_object_type(self, tag: str) -> CommandResult:
        """Return the direct Git object type of a tag reference."""
        ...

    def get_raw_tag_object(self, tag: str) -> CommandResult:
        """Read the raw object for an annotated tag."""
        ...

    def create_tag_object(self, raw_object: str) -> CommandResult:
        """Create a validated annotated-tag object."""
        ...

    def replace_local_tags_atomically(
        self,
        replacements: list[TagRefReplacement],
    ) -> CommandResult:
        """Replace local tag refs in one transaction."""
        ...

    def replace_remote_tags_atomically(
        self,
        remote: str,
        replacements: list[TagRefReplacement],
    ) -> CommandResult:
        """Replace remote tag refs in one atomic push."""
        ...

    def get_remote_tag_oid(self, remote: str, tag: str) -> CommandResult:
        """Read one exact tag ref from a remote."""
        ...

    def create_annotated_tag(
        self,
        tag: str,
        sha: str,
        message_file: str,
    ) -> CommandResult:
        """
        Create annotated tag.

        Args:
            tag (str):
                New tag name.

            sha (str):
                Commit SHA.

            message_file (str):
                Path to message file.
        """
        ...

    # =====================================================
    # Tags
    # =====================================================

    def push_tag(
        self,
        remote: str,
        tag: str,
    ) -> CommandResult:
        """
        Push a tag to a remote.

        Args:
            remote (str):
                Remote name.

            tag (str):
                Tag name.
        """
        ...

    def delete_remote_tag(
        self,
        remote: str,
        tag: str,
    ) -> CommandResult:
        """
        Delete a tag from a remote.

        Args:
            remote (str):
                Remote name.

            tag (str):
                Tag name.
        """
        ...

    def delete_local_tag(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Delete local tag.

        Args:
            tag (str):
                Tag name.
        """
        ...

    # =====================================================
    # Remote
    # =====================================================

    def remote_get_url(
        self,
        remote: str = "origin",
    ) -> CommandResult:
        """
        Get remote URL.

        Args:
            remote (str):
                Remote name.
        """
        ...

    def add_detached_worktree(
        self,
        tag: str,
        path: Path,
    ) -> CommandResult:
        """Create a detached worktree for a Git tag."""
        ...

    def remove_worktree(
        self,
        path: Path,
    ) -> CommandResult:
        """Remove a detached Git worktree."""
        ...

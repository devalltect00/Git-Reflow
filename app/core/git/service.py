# app/core/git/service.py

"""
Git service layer.

This module contains high-level Git operations used by Reflow.

Responsibilities:
- Repository validation
- Remote resolution
- Tag retrieval
- Tag push operations

This module does not execute subprocess commands directly.

All command execution is delegated to a Git executor.
"""

import logging
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from app.config.config_loader import ConfigLoader, get_config
from app.core.decorators.log_decorators import log_execution
from app.core.git.models import TagRefReplacement, TagSnapshot
from app.core.git.protocol import IGitExecutor
from app.core.shared.exceptions import GitOperationError

logger = logging.getLogger(__name__)


class GitService:
    """
    High-level Git operations.

    This class contains Git-related business logic used by Reflow.

    It depends on an executor abstraction instead of a specific
    implementation.
    """

    def __init__(
        self,
        executor: IGitExecutor,
        config: ConfigLoader | None = None,
        repository: Path | None = None,
    ) -> None:
        """
        Initialize Git service.

        Args:
            executor (IGitExecutor):
                Git command executor.

            config (ConfigLoader | None):
                Configuration loader.

            repository (Path | None):
                Repository represented by this service.
        """
        self.executor = executor
        self.config = config or get_config()
        self.repository = (repository or Path.cwd()).resolve()

    # =====================================================
    # Configuration
    # =====================================================

    def resolve_default_remote(
        self,
        remote: str | None = None,
    ) -> str:
        """
        Resolve the default Git remote.

        Priority:
            1. Explicit argument
            2. Configuration
            3. "origin"

        Args:
            remote (str | None):
                Explicit remote name.

        Returns:
            str:
                Resolved remote name.
        """
        resolved_remote = self.config.resolve(
            cli_value=remote,
            config_keys=["git", "default_remote"],
            default="origin",
        )

        logger.debug(
            "Resolved remote '%s'",
            resolved_remote,
        )

        return resolved_remote

    # =====================================================
    # Repository
    # =====================================================

    @log_execution
    def is_git_repo(self) -> bool:
        """
        Check whether current directory is a Git repository.

        Logic:
            1. Check .git directory
            2. Fallback to git rev-parse

        Returns:
            bool:
                True if repository exists.
        """
        if (self.repository / ".git").exists():
            return True

        result = self.executor.rev_parse_inside_work_tree()

        return result.success

    # =====================================================
    # Remote
    # =====================================================

    @log_execution
    def get_remote_url(
        self,
        remote: str | None = None,
    ) -> str | None:
        """
        Get remote URL.

        Args:
            remote (str | None):
                Remote name.

        Returns:
            str | None:
                Remote URL if found.
        """
        resolved_remote = self.resolve_default_remote(remote)

        result = self.executor.remote_get_url(
            remote=resolved_remote,
        )

        if not result.success:
            logger.debug(
                "Remote '%s' does not exist",
                resolved_remote,
            )
            return None

        return result.stdout.strip()

    @log_execution
    def remote_exists(
        self,
        remote: str | None = None,
    ) -> bool:
        """
        Check whether a remote exists.

        Args:
            remote (str | None):
                Remote name.

        Returns:
            bool:
                True if remote exists.
        """
        resolved_remote = self.resolve_default_remote(remote)

        result = self.executor.remote_get_url(
            remote=resolved_remote,
        )

        return result.success

    # =====================================================
    # Tags
    # =====================================================

    @log_execution
    def get_all_tags(self) -> list[str]:
        """
        Get all tags sorted by creation date.

        Returns:
            list[str]:
                List of tags.

        Raises:
            GitOperationError:
                If Git cannot inspect the repository tags.
        """
        result = self.executor.get_all_tags()

        if not result.success:
            logger.debug("Failed to retrieve Git tags")
            raise GitOperationError(
                "Failed to retrieve Git tags. Verify repository access, Git "
                "configuration, and repository ownership."
            )

        if not result.stdout:
            return []

        return result.stdout.strip().splitlines()

    @log_execution
    def get_tag_commit_sha(
        self,
        tag: str,
    ) -> str | None:
        """
        Get commit SHA referenced by a tag.

        Args:
            tag (str):
                Tag name.

        Returns:
            str | None:
                Commit SHA if found.
        """
        result = self.executor.get_tag_commit_sha(tag)

        if not result.success:
            logger.debug(
                "Failed to retrieve SHA for tag '%s'",
                tag,
            )
            return None

        return result.stdout.strip()

    @log_execution
    def get_tag_message(
        self,
        tag: str,
    ) -> str:
        """
        Get annotated tag message.

        Args:
            tag (str):
                Tag name.

        Returns:
            str:
                Tag message.
        """
        result = self.executor.get_tag_message(tag)

        if not result.success:
            logger.debug(
                "Failed to retrieve message for tag '%s'",
                tag,
            )
            return ""

        return result.stdout

    @log_execution
    def create_annotated_tag(
        self,
        tag: str,
        sha: str,
        message_file: str,
    ) -> None:
        """
        Create annotated tag.

        Args:
            tag (str):
                New tag name.

            sha (str):
                Commit SHA.

            message_file (str):
                Path to tag message file.

        Raises:
            GitOperationError:
                If creation fails.
        """
        logger.debug(
            "Creating annotated tag '%s'",
            tag,
        )

        result = self.executor.create_annotated_tag(
            tag=tag,
            sha=sha,
            message_file=message_file,
        )

        if not result.success:
            logger.debug(
                "Failed to create annotated tag '%s'",
                tag,
            )

            raise GitOperationError(f"Failed to create annotated tag '{tag}'.")

    @log_execution
    def delete_local_tag(
        self,
        tag: str,
    ) -> None:
        """
        Delete local tag.

        Args:
            tag (str):
                Tag name.

        Raises:
            GitOperationError:
                If deletion fails.
        """
        logger.debug(
            "Deleting local tag '%s'",
            tag,
        )

        result = self.executor.delete_local_tag(
            tag=tag,
        )

        if not result.success:
            logger.debug(
                "Failed to delete local tag '%s'",
                tag,
            )

            raise GitOperationError(f"Failed to delete local tag '{tag}'.")

    @log_execution
    def push_tag(
        self,
        tag: str,
        remote: str | None = None,
    ) -> None:
        """
        Push a tag to a remote.

        Args:
            tag (str):
                Tag name.

            remote (str | None):
                Remote name.

        Raises:
            GitOperationError:
                If push fails.
        """
        resolved_remote = self.resolve_default_remote(remote)

        logger.debug(
            "Pushing tag '%s' to '%s'",
            tag,
            resolved_remote,
        )

        result = self.executor.push_tag(
            remote=resolved_remote,
            tag=tag,
        )

        if not result.success:
            logger.debug(
                "Failed to push tag '%s' to '%s'",
                tag,
                resolved_remote,
            )

            raise GitOperationError(
                f"Failed to push tag '{tag}' to remote '{resolved_remote}'."
            )

    @log_execution
    def delete_remote_tag(
        self,
        tag: str,
        remote: str | None = None,
    ) -> None:
        """
        Delete a tag from a remote.

        Args:
            tag (str):
                Tag name.

            remote (str | None):
                Remote name.

        Raises:
            GitOperationError:
                If delete fails.
        """
        resolved_remote = self.resolve_default_remote(remote)

        logger.debug(
            "Deleting remote tag '%s' from '%s'",
            tag,
            resolved_remote,
        )

        result = self.executor.delete_remote_tag(
            remote=resolved_remote,
            tag=tag,
        )

        if not result.success:
            logger.debug(
                "Failed to delete tag '%s' from '%s'",
                tag,
                resolved_remote,
            )

            raise GitOperationError(
                f"Failed to delete remote tag '{tag}' from '{resolved_remote}'."
            )

    @log_execution
    def get_tag_snapshot(self, tag: str) -> TagSnapshot:
        """Capture the direct ref and complete annotated metadata for one tag.

        Args:
            tag:
                Existing local tag name.

        Returns:
            TagSnapshot:
                Immutable tag state used for a guarded replacement.

        Raises:
            GitOperationError:
                If the tag cannot be inspected safely.
        """

        ref_result = self.executor.get_tag_ref_oid(tag)
        type_result = self.executor.get_tag_object_type(tag)
        if not ref_result.success or not ref_result.stdout.strip():
            raise GitOperationError(f"Unable to resolve tag reference '{tag}'.")
        if not type_result.success or not type_result.stdout.strip():
            raise GitOperationError(f"Unable to inspect tag type for '{tag}'.")

        object_type = type_result.stdout.strip()
        raw_object: str | None = None
        if object_type == "tag":
            raw_result = self.executor.get_raw_tag_object(tag)
            if not raw_result.success or not raw_result.stdout:
                raise GitOperationError(
                    f"Unable to read annotated metadata for tag '{tag}'."
                )
            raw_object = raw_result.stdout

        return TagSnapshot(
            name=tag,
            ref_oid=ref_result.stdout.strip(),
            object_type=object_type,
            raw_object=raw_object,
        )

    @log_execution
    def create_replacement_ref(
        self,
        *,
        snapshot: TagSnapshot,
        destination: str,
    ) -> TagRefReplacement:
        """Build the destination object while preserving supported metadata."""

        if snapshot.is_signed:
            snapshot.renamed_raw_object(destination)

        destination_oid = snapshot.ref_oid
        if snapshot.is_annotated:
            raw_object = snapshot.renamed_raw_object(destination)
            result = self.executor.create_tag_object(raw_object)
            if not result.success or not result.stdout.strip():
                detail = result.stderr.strip()
                raise GitOperationError(
                    f"Failed to construct destination tag object '{destination}'. "
                    f"{detail}".strip()
                )
            destination_oid = result.stdout.strip()

        return TagRefReplacement(
            source=snapshot.name,
            destination=destination,
            source_oid=snapshot.ref_oid,
            destination_oid=destination_oid,
        )

    @log_execution
    def replace_local_tags_atomically(
        self,
        replacements: list[TagRefReplacement],
    ) -> None:
        """Apply an all-or-nothing local tag-reference replacement plan."""

        result = self.executor.replace_local_tags_atomically(replacements)
        if not result.success:
            raise GitOperationError(
                "Failed to replace local tags atomically. No local tag "
                f"references were changed. {result.stderr.strip()}".strip()
            )

        for item in replacements:
            source = self.executor.get_tag_ref_oid(item.source)
            destination = self.executor.get_tag_ref_oid(item.destination)
            if source.success or destination.stdout.strip() != item.destination_oid:
                raise GitOperationError(
                    "Local tag verification failed after the atomic replacement."
                )

    @log_execution
    def replace_remote_tags_atomically(
        self,
        replacements: list[TagRefReplacement],
        remote: str | None = None,
    ) -> None:
        """Apply and verify an all-or-nothing remote tag replacement plan."""

        resolved_remote = self.resolve_default_remote(remote)
        result = self.executor.replace_remote_tags_atomically(
            resolved_remote,
            replacements,
        )
        if not result.success:
            detail = result.stderr.strip()
            raise GitOperationError(
                "Failed to replace remote tags atomically. The remote rejected "
                "the complete operation, so Reflow did not fall back to a "
                f"partial update. {detail}".strip()
            )

        for item in replacements:
            source_oid = self.get_remote_tag_oid(item.source, resolved_remote)
            destination_oid = self.get_remote_tag_oid(
                item.destination,
                resolved_remote,
            )
            if source_oid is not None or destination_oid != item.destination_oid:
                raise GitOperationError(
                    "Remote tag verification failed after the atomic replacement."
                )

    @log_execution
    def get_remote_tag_oid(
        self,
        tag: str,
        remote: str | None = None,
    ) -> str | None:
        """Return an exact remote tag ref object ID, or ``None`` if absent."""

        resolved_remote = self.resolve_default_remote(remote)
        result = self.executor.get_remote_tag_oid(resolved_remote, tag)
        if not result.success:
            raise GitOperationError(
                f"Unable to inspect remote tag '{tag}' on '{resolved_remote}'."
            )
        if not result.stdout.strip():
            return None
        return result.stdout.split()[0]

    @contextmanager
    def tag_worktree(
        self,
        tag: str,
    ) -> Iterator[Path]:
        """
        Materialize a tag in a temporary detached worktree.

        Args:
            tag:
                Tag whose source tree should be materialized.

        Yields:
            Path:
                Temporary Docker build context for the tag.

        Raises:
            GitOperationError:
                If the worktree cannot be created.
        """

        with tempfile.TemporaryDirectory(prefix="reflow-") as temporary_root:
            worktree = Path(temporary_root) / "checkout"
            result = self.executor.add_detached_worktree(
                tag=tag,
                path=worktree,
            )

            if not result.success:
                raise GitOperationError(
                    f"Failed to create temporary worktree for tag '{tag}'."
                )

            try:
                yield worktree
            finally:
                removal = self.executor.remove_worktree(worktree)

                if not removal.success:
                    logger.warning(
                        "Failed to remove temporary worktree '%s'",
                        worktree,
                    )

    # =====================================================
    # Executor Access
    # =====================================================

    def get_is_dry_run(self) -> bool:
        """
        Get current dry-run state.

        Returns:
            bool:
                Current dry-run state.
        """
        return self.executor.get_is_dry_run()

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

    def get_silent(self) -> bool:
        """
        Get current silent mode.

        Returns:
            bool:
                Current silent state.
        """
        return self.executor.get_silent()

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

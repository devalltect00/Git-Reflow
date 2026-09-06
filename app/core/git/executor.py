# app/core/git/executor.py

"""
Git command executor.

This module contains the low-level Git command execution layer.

Responsibilities:
- Execute Git commands
- Return CommandResult objects
- Support dry-run mode
- Support silent mode

This module does NOT:
- Contain business logic
- Make workflow decisions
- Perform tag filtering
- Perform release checks

Those responsibilities belong to GitService.
"""

import subprocess
from pathlib import Path

from app.core.dry_run.dry_run_support import DryRunSupport
from app.core.git.models import TagRefReplacement
from app.core.shared.result import CommandResult


class GitExecutor(DryRunSupport):
    """
    Low-level Git command executor.

    This class is responsible only for executing Git commands
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
        Initialize Git executor.

        Args:
            dry_run (bool):
                Enable dry-run mode.

            is_silent (bool):
                Disable command logging.

            repository (Path | None):
                Working directory for every Git command.
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
        Get current dry-run status.

        Returns:
            bool:
                Current dry-run state.
        """
        return self.runner.get_is_dry_run()

    def set_is_dry_run(self, is_dry_run: bool) -> None:
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

    def set_silent(self, is_silent: bool) -> None:
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
        mutates: bool = True,
    ) -> CommandResult:
        """
        Execute a Git command.

        Args:
            args (list[str]):
                Git arguments without the 'git' prefix.

            check (bool):
                Raise on non-zero return code.

            mutates (bool):
                Whether dry-run mode should skip the command.

        Returns:
            CommandResult:
                Normalized command result.
        """
        result = self.runner.run(
            ["git", *args],
            check=check,
            mutates=mutates,
            cwd=self.repository,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

        if result is None:
            return CommandResult.dry_run()

        return CommandResult.from_completed_process(result)

    def _run_with_exact_input(
        self,
        args: list[str],
        input_data: bytes,
        *,
        check: bool = False,
    ) -> CommandResult:
        """Execute Git with byte-exact standard input.

        Git tag objects and ``update-ref --stdin`` transactions are
        line-oriented protocols whose newlines must not be translated by the
        Windows text layer. Passing bytes preserves their canonical LF form.
        """

        result = self.runner.run(
            ["git", *args],
            check=check,
            mutates=True,
            cwd=self.repository,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=input_data,
        )

        if result is None:
            return CommandResult.dry_run()

        return CommandResult(
            returncode=result.returncode,
            stdout=(result.stdout or b"").decode("utf-8", errors="replace"),
            stderr=(result.stderr or b"").decode("utf-8", errors="replace"),
        )

    # =====================================================
    # Repository
    # =====================================================

    def rev_parse_inside_work_tree(self) -> CommandResult:
        """
        Check whether current directory is inside a Git repository.

        Command:
            git rev-parse --is-inside-work-tree

        Returns:
            CommandResult
        """
        return self._run(
            ["rev-parse", "--is-inside-work-tree"],
            check=False,
            mutates=False,
        )

    def get_all_tags(self) -> CommandResult:
        """
        Get all tags sorted by creation date.

        Command:
            git tag --sort=creatordate

        Returns:
            CommandResult
        """
        return self._run(
            ["tag", "--sort=creatordate"],
            check=True,
            mutates=False,
        )

    def get_tag_commit_sha(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Get commit SHA for a tag.

        Command:
            git rev-list -n 1 <tag>

        Args:
            tag (str):
                Tag name.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "rev-list",
                "-n",
                "1",
                tag,
            ],
            check=True,
            mutates=False,
        )

    def get_tag_message(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Get annotated tag message.

        Command:
            git tag -l --format=%(contents) <tag>

        Args:
            tag (str):
                Tag name.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "tag",
                "-l",
                "--format=%(contents)",
                tag,
            ],
            check=True,
            mutates=False,
        )

    def get_tag_ref_oid(self, tag: str) -> CommandResult:
        """Resolve the object ID stored directly in one tag reference."""

        return self._run(
            ["rev-parse", "--verify", f"refs/tags/{tag}"],
            check=False,
            mutates=False,
        )

    def get_tag_object_type(self, tag: str) -> CommandResult:
        """Return the Git object type stored directly in one tag reference."""

        return self._run(
            ["cat-file", "-t", f"refs/tags/{tag}"],
            check=False,
            mutates=False,
        )

    def get_raw_tag_object(self, tag: str) -> CommandResult:
        """Read the complete annotated-tag object for metadata reconstruction."""

        return self._run(
            ["cat-file", "tag", f"refs/tags/{tag}"],
            check=False,
            mutates=False,
        )

    def create_tag_object(self, raw_object: str) -> CommandResult:
        """Create one validated annotated-tag object with ``git mktag``."""

        return self._run_with_exact_input(
            ["mktag"],
            raw_object.encode("utf-8"),
            check=False,
        )

    def replace_local_tags_atomically(
        self,
        replacements: list[TagRefReplacement],
    ) -> CommandResult:
        """Create destination refs and delete source refs in one transaction."""

        commands: list[str] = []
        for item in replacements:
            commands.append(
                f"create refs/tags/{item.destination} {item.destination_oid}"
            )
            commands.append(f"delete refs/tags/{item.source} {item.source_oid}")
        commands.append("")
        return self._run_with_exact_input(
            ["update-ref", "--stdin"],
            "\n".join(commands).encode("utf-8"),
            check=False,
        )

    def replace_remote_tags_atomically(
        self,
        remote: str,
        replacements: list[TagRefReplacement],
    ) -> CommandResult:
        """Atomically push destination refs and source deletions with leases."""

        args = ["push", "--atomic"]
        for item in replacements:
            args.append(f"--force-with-lease=refs/tags/{item.destination}:")
            args.append(f"--force-with-lease=refs/tags/{item.source}:{item.source_oid}")
        args.append(remote)
        for item in replacements:
            args.append(f"{item.destination_oid}:refs/tags/{item.destination}")
            args.append(f":refs/tags/{item.source}")
        return self._run(args, check=False)

    def get_remote_tag_oid(self, remote: str, tag: str) -> CommandResult:
        """Read one exact remote tag reference without changing local state."""

        return self._run(
            ["ls-remote", "--refs", "--tags", remote, f"refs/tags/{tag}"],
            check=False,
            mutates=False,
        )

    def create_annotated_tag(
        self,
        tag: str,
        sha: str,
        message_file: str,
    ) -> CommandResult:
        """
        Create annotated tag.

        Command:
            git tag -a <tag> <sha> -F <file>

        Args:
            tag (str):
                Tag name.

            sha (str):
                Commit SHA.

            message_file (str):
                Tag message file.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "tag",
                "-a",
                tag,
                sha,
                "-F",
                message_file,
            ],
            check=True,
        )

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

        Command:
            git push <remote> <tag>

        Args:
            remote (str):
                Remote name.

            tag (str):
                Tag name.

        Returns:
            CommandResult
        """
        return self._run(
            ["push", remote, tag],
            check=True,
        )

    def delete_remote_tag(
        self,
        remote: str,
        tag: str,
    ) -> CommandResult:
        """
        Delete a tag from a remote.

        Command:
            git push <remote> --delete <tag>

        Args:
            remote (str):
                Remote name.

            tag (str):
                Tag name.

        Returns:
            CommandResult
        """
        return self._run(
            ["push", remote, "--delete", tag],
            check=False,
        )

    def delete_local_tag(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Delete local tag.

        Command:
            git tag -d <tag>

        Args:
            tag (str):
                Tag name.

        Returns:
            CommandResult
        """
        return self._run(
            [
                "tag",
                "-d",
                tag,
            ],
            check=True,
        )

    # =====================================================
    # Remote
    # =====================================================

    def remote_get_url(
        self,
        remote: str = "origin",
    ) -> CommandResult:
        """
        Get remote URL.

        Command:
            git remote get-url <remote>

        Args:
            remote (str):
                Remote name.

        Returns:
            CommandResult
        """
        return self._run(
            ["remote", "get-url", remote],
            check=False,
            mutates=False,
        )

    def add_detached_worktree(
        self,
        tag: str,
        path: Path,
    ) -> CommandResult:
        """
        Create a detached temporary worktree for a tag.

        Args:
            tag:
                Git tag to materialize.

            path:
                Destination path for the detached worktree.

        Returns:
            CommandResult:
                Worktree command result.
        """

        return self._run(
            ["worktree", "add", "--detach", str(path), tag],
            check=True,
        )

    def remove_worktree(
        self,
        path: Path,
    ) -> CommandResult:
        """
        Remove a temporary Git worktree.

        Args:
            path:
                Worktree path to remove.

        Returns:
            CommandResult:
                Worktree removal result.
        """

        return self._run(
            ["worktree", "remove", "--force", str(path)],
            check=False,
        )

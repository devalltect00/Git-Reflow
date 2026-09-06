# app/core/repository/executor.py

"""
Remote repository clone executor.

Responsibilities:
- Execute credential-safe Git clone commands
- Normalize subprocess results
- Preserve dry-run discovery behavior
"""

import subprocess
from pathlib import Path

from app.core.dry_run.dry_run_support import DryRunSupport
from app.core.shared import CommandResult


class RepositoryExecutor(DryRunSupport):
    """Low-level executor for materializing remote repository targets."""

    def __init__(
        self,
        *,
        dry_run: bool = False,
        is_silent: bool = False,
    ) -> None:
        """
        Initialize repository command execution.

        Args:
            dry_run:
                Shared dry-run state. Clone discovery still executes.

            is_silent:
                Suppress command logging.
        """

        super().__init__(dry_run=dry_run, is_silent=is_silent)

    def clone(
        self,
        *,
        url: str,
        destination: Path,
    ) -> CommandResult:
        """
        Clone a remote repository into a managed destination.

        The operation executes during dry-run because subsequent discovery
        requires real Git metadata. It does not mutate the remote repository.

        Args:
            url:
                Validated credential-free Git URL.

            destination:
                Empty destination path below a temporary directory.

        Returns:
            CommandResult:
                Normalized clone result.
        """

        result = self.runner.run(
            [
                "git",
                "clone",
                "--no-single-branch",
                "--",
                url,
                str(destination),
            ],
            check=False,
            mutates=False,
            cwd=destination.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

        if result is None:
            return CommandResult.dry_run()

        return CommandResult.from_completed_process(result)

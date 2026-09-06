# app/core/github/executor.py

"""
GitHub command executor.

This module contains the low-level GitHub command execution layer.

Responsibilities:
- Execute GitHub CLI commands
- Return CommandResult objects
- Support dry-run mode
- Support silent mode

This module does NOT:
- Contain business logic
- Make workflow decisions
- Decide whether releases should be created
- Perform release orchestration

Those responsibilities belong to GitHubService.
"""

import subprocess
from pathlib import Path

from app.core.dry_run.dry_run_support import DryRunSupport
from app.core.shared.result import CommandResult


class GitHubExecutor(DryRunSupport):
    """
    Low-level GitHub command executor.

    This class is responsible only for executing GitHub CLI
    commands and returning normalized CommandResult objects.

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
        Initialize GitHub executor.

        Args:
            dry_run (bool):
                Enable dry-run mode.

            is_silent (bool):
                Disable command logging.

            repository (Path | None):
                Working directory used for GitHub repository discovery.
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
        mutates: bool = True,
    ) -> CommandResult:
        """
        Execute a GitHub CLI command.

        Args:
            args (list[str]):
                Command arguments without the 'gh' prefix.

            check (bool):
                Raise on non-zero return code.

            mutates (bool):
                Whether dry-run mode should skip the command.

        Returns:
            CommandResult:
                Normalized command result.
        """
        result = self.runner.run(
            ["gh", *args],
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

    # =====================================================
    # Releases
    # =====================================================

    def release_exists(
        self,
        tag: str,
    ) -> CommandResult:
        """
        Check whether a GitHub release exists.

        Command:
            gh release view <tag>

        Args:
            tag (str):
                Release tag.

        Returns:
            CommandResult
        """
        return self._run(
            ["release", "view", tag],
            check=False,
            mutates=False,
        )

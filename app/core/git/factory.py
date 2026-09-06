# app/core/git/factory.py

"""
Git service factory.

This module creates fully configured GitService instances.

The factory is responsible for wiring together:
- GitExecutor
- ConfigLoader
- GitService

This keeps object creation centralized and makes
dependency management easier.
"""

from pathlib import Path

from app.config.config_loader import get_config
from app.core.git.executor import GitExecutor
from app.core.git.service import GitService


def create_git_service(
    dry_run: bool = False,
    is_silent: bool = False,
    repository: Path | None = None,
) -> GitService:
    """
    Create a configured Git service.

    Args:
        dry_run (bool):
            Enable dry-run mode.

        is_silent (bool):
            Disable command logging.

        repository (Path | None):
            Working directory for Git commands.

    Returns:
        GitService:
            Ready-to-use Git service.
    """
    executor = GitExecutor(
        dry_run=dry_run,
        is_silent=is_silent,
        repository=repository,
    )

    config = get_config()

    return GitService(
        executor=executor,
        config=config,
        repository=repository,
    )

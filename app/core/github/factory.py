# app/core/github/factory.py

"""
GitHub service factory.

This module creates fully configured GitHubService instances.

The factory is responsible for wiring together:
- GitHubExecutor
- GitHubService

This keeps object creation centralized and makes
dependency management easier.
"""

from pathlib import Path

from app.core.github.executor import GitHubExecutor
from app.core.github.service import GitHubService


def create_github_service(
    dry_run: bool = False,
    is_silent: bool = False,
    repository: Path | None = None,
) -> GitHubService:
    """
    Create a configured GitHub service.

    Args:
        dry_run (bool):
            Enable dry-run mode.

        is_silent (bool):
            Disable command logging.

        repository (Path | None):
            Working directory used by GitHub CLI repository discovery.

    Returns:
        GitHubService:
            Ready-to-use GitHub service.
    """
    executor = GitHubExecutor(
        dry_run=dry_run,
        is_silent=is_silent,
        repository=repository,
    )

    return GitHubService(
        executor=executor,
    )

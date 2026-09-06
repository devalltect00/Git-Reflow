# app/core/docker/factory.py

"""
Docker service factory.

This module creates fully configured DockerService instances.

The factory is responsible for wiring together:
- DockerExecutor
- DockerService

This keeps object creation centralized and makes
dependency management easier.
"""

from pathlib import Path

from app.core.docker.executor import DockerExecutor
from app.core.docker.service import DockerService


def create_docker_service(
    dry_run: bool = False,
    is_silent: bool = False,
    repository: Path | None = None,
) -> DockerService:
    """
    Create a configured Docker service.

    Args:
        dry_run (bool):
            Enable dry-run mode.

        is_silent (bool):
            Disable command logging.

        repository (Path | None):
            Working directory for Docker commands and default build context.

    Returns:
        DockerService:
            Ready-to-use Docker service.
    """
    executor = DockerExecutor(
        dry_run=dry_run,
        is_silent=is_silent,
        repository=repository,
    )

    return DockerService(
        executor=executor,
    )

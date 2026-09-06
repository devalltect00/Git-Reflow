# tests/core/docker/test_factory.py

"""
Tests for Docker service factory.

This module tests Docker service creation.
"""

from app.core.docker import DockerService
from app.core.docker.factory import create_docker_service


class TestDockerFactory:
    """
    Tests for Docker service factory.
    """

    def test_create_docker_service_returns_service(self):
        """
        Should return a DockerService instance.
        """
        service = create_docker_service()

        assert isinstance(
            service,
            DockerService,
        )

    def test_create_docker_service_sets_dry_run(self):
        """
        Should configure dry-run mode.
        """
        service = create_docker_service(
            dry_run=True,
        )

        assert service.get_is_dry_run() is True

    def test_create_docker_service_sets_silent(self):
        """
        Should configure silent mode.
        """
        service = create_docker_service(
            is_silent=True,
        )

        assert service.get_silent() is True

    def test_create_docker_service_defaults_to_non_dry_run(self):
        """
        Should default to dry-run disabled.
        """
        service = create_docker_service()

        assert service.get_is_dry_run() is False

    def test_create_docker_service_defaults_to_non_silent(self):
        """
        Should default to silent mode disabled.
        """
        service = create_docker_service()

        assert service.get_silent() is False

    def test_create_docker_service_uses_repository(self, tmp_path):
        """Use the selected repository as the default Docker context."""
        service = create_docker_service(repository=tmp_path)

        assert service.executor.repository == tmp_path.resolve()

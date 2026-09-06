# tests/core/git/test_factory.py

"""
Tests for Git service factory.

This module tests Git service creation.
"""

from app.core.git import GitService
from app.core.git.factory import create_git_service


class TestGitFactory:
    """
    Tests for Git service factory.
    """

    def test_create_git_service_returns_service(self):
        """
        Should return a GitService instance.
        """
        service = create_git_service()

        assert isinstance(
            service,
            GitService,
        )

    def test_create_git_service_sets_dry_run(self):
        """
        Should configure dry-run mode.
        """
        service = create_git_service(
            dry_run=True,
        )

        assert service.get_is_dry_run() is True

    def test_create_git_service_sets_silent(self):
        """
        Should configure silent mode.
        """
        service = create_git_service(
            is_silent=True,
        )

        assert service.get_silent() is True

    def test_create_git_service_defaults_to_non_dry_run(self):
        """
        Should default to dry-run disabled.
        """
        service = create_git_service()

        assert service.get_is_dry_run() is False

    def test_create_git_service_defaults_to_non_silent(self):
        """
        Should default to silent mode disabled.
        """
        service = create_git_service()

        assert service.get_silent() is False

    def test_create_git_service_uses_repository(self, tmp_path):
        """Configure both the service and executor for the target repository."""
        service = create_git_service(repository=tmp_path)

        assert service.repository == tmp_path.resolve()
        assert service.executor.repository == tmp_path.resolve()

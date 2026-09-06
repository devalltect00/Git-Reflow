# tests/core/github/test_factory.py

"""
Tests for GitHub service factory.

This module tests GitHub service creation.
"""

from app.core.github import GitHubService
from app.core.github.factory import create_github_service


class TestGitHubFactory:
    """
    Tests for GitHub service factory.
    """

    def test_create_github_service_returns_service(self):
        """
        Should return a GitHubService instance.
        """
        service = create_github_service()

        assert isinstance(
            service,
            GitHubService,
        )

    def test_create_github_service_sets_dry_run(self):
        """
        Should configure dry-run mode.
        """
        service = create_github_service(
            dry_run=True,
        )

        assert service.get_is_dry_run() is True

    def test_create_github_service_sets_silent(self):
        """
        Should configure silent mode.
        """
        service = create_github_service(
            is_silent=True,
        )

        assert service.get_silent() is True

    def test_create_github_service_defaults_to_non_dry_run(self):
        """
        Should default to dry-run disabled.
        """
        service = create_github_service()

        assert service.get_is_dry_run() is False

    def test_create_github_service_defaults_to_non_silent(self):
        """
        Should default to silent mode disabled.
        """
        service = create_github_service()

        assert service.get_silent() is False

    def test_create_github_service_uses_repository(self, tmp_path):
        """Run GitHub CLI commands from the selected repository."""
        service = create_github_service(repository=tmp_path)

        assert service.executor.repository == tmp_path.resolve()

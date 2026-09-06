# tests/core/github/test_service.py

"""
Tests for GitHubService.

This module tests GitHub business logic.
"""

from unittest.mock import Mock

import pytest

from app.core.github.service import GitHubService


class TestGitHubService:
    """
    Tests for GitHubService.
    """

    @pytest.fixture
    def executor(self):
        """
        Create a mock executor.
        """
        return Mock()

    @pytest.fixture
    def service(
        self,
        executor,
    ):
        """
        Create a GitHub service.
        """
        return GitHubService(
            executor=executor,
        )

    # =====================================================
    # release_exists
    # =====================================================

    def test_release_exists_returns_true(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should return True when release exists.
        """
        executor.release_exists.return_value = success_result

        assert service.release_exists("v1.0.0")

    def test_release_exists_returns_false(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should return False when release does not exist.
        """
        executor.release_exists.return_value = failed_result

        assert service.release_exists("v1.0.0") is False

    def test_release_exists_returns_false_for_empty_tag(
        self,
        service,
    ):
        """
        Should return False for an empty tag.
        """
        assert service.release_exists("") is False

    # =====================================================
    # Dry Run
    # =====================================================

    def test_get_is_dry_run(
        self,
        service,
        executor,
    ):
        """
        Should return executor dry-run state.
        """
        executor.get_is_dry_run.return_value = True

        assert service.get_is_dry_run() is True

    def test_set_is_dry_run(
        self,
        service,
        executor,
    ):
        """
        Should update executor dry-run state.
        """
        service.set_is_dry_run(True)

        executor.set_is_dry_run.assert_called_once_with(True)

    # =====================================================
    # Silent
    # =====================================================

    def test_get_silent(
        self,
        service,
        executor,
    ):
        """
        Should return executor silent state.
        """
        executor.get_silent.return_value = True

        assert service.get_silent() is True

    def test_set_silent(
        self,
        service,
        executor,
    ):
        """
        Should update executor silent state.
        """
        service.set_silent(True)

        executor.set_silent.assert_called_once_with(True)

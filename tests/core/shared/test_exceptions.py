# tests/core/shared/test_exceptions.py

"""
Tests for custom exceptions.

This module verifies the exception inheritance hierarchy.
"""

from app.core.shared.exceptions import (
    ConfigurationError,
    DockerOperationError,
    GitHubOperationError,
    GitOperationError,
    ReflowError,
    ValidationError,
)


class TestExceptions:
    """
    Tests for custom exception classes.
    """

    # =====================================================
    # ReflowError
    # =====================================================

    def test_reflow_error_is_exception(self):
        """
        ReflowError should inherit from Exception.
        """
        assert issubclass(
            ReflowError,
            Exception,
        )

    # =====================================================
    # GitOperationError
    # =====================================================

    def test_git_operation_error_inherits_reflow_error(self):
        """
        GitOperationError should inherit from ReflowError.
        """
        assert issubclass(
            GitOperationError,
            ReflowError,
        )

    def test_git_operation_error_can_be_raised(self):
        """
        GitOperationError should be raisable.
        """
        try:
            raise GitOperationError("Git operation failed")
        except GitOperationError as exc:
            assert str(exc) == "Git operation failed"

    # =====================================================
    # GitHubOperationError
    # =====================================================

    def test_github_operation_error_inherits_reflow_error(self):
        """
        GitHubOperationError should inherit from ReflowError.
        """
        assert issubclass(
            GitHubOperationError,
            ReflowError,
        )

    # =====================================================
    # DockerOperationError
    # =====================================================

    def test_docker_operation_error_inherits_reflow_error(self):
        """
        DockerOperationError should inherit from ReflowError.
        """
        assert issubclass(
            DockerOperationError,
            ReflowError,
        )

    # =====================================================
    # ConfigurationError
    # =====================================================

    def test_configuration_error_inherits_reflow_error(self):
        """
        ConfigurationError should inherit from ReflowError.
        """
        assert issubclass(
            ConfigurationError,
            ReflowError,
        )

    # =====================================================
    # ValidationError
    # =====================================================

    def test_validation_error_inherits_reflow_error(self):
        """
        ValidationError should inherit from ReflowError.
        """
        assert issubclass(
            ValidationError,
            ReflowError,
        )

    # =====================================================
    # Catching
    # =====================================================

    def test_git_operation_error_is_caught_by_reflow_error(self):
        """
        GitOperationError should be catchable as ReflowError.
        """
        try:
            raise GitOperationError("failure")
        except ReflowError:
            caught = True
        else:
            caught = False

        assert caught is True

    def test_docker_operation_error_is_caught_by_reflow_error(self):
        """
        DockerOperationError should be catchable as ReflowError.
        """
        try:
            raise DockerOperationError("failure")
        except ReflowError:
            caught = True
        else:
            caught = False

        assert caught is True

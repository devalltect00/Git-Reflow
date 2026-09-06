# app/core/shared/exceptions.py

"""
Shared exceptions used by Reflow.

This module contains application-specific exceptions used
throughout the project.

Using dedicated exception types makes error handling,
testing, and debugging easier.
"""


class ReflowError(Exception):
    """
    Base exception for Reflow.

    All custom Reflow exceptions should inherit from this
    exception.
    """


# =====================================================
# Git
# =====================================================


class GitOperationError(ReflowError):
    """
    Raised when a Git operation fails.
    """


class RepositoryOperationError(ReflowError):
    """Raised when a managed repository workspace cannot be materialized."""


# =====================================================
# GitHub
# =====================================================


class GitHubOperationError(ReflowError):
    """
    Raised when a GitHub operation fails.
    """


# =====================================================
# Docker
# =====================================================


class DockerOperationError(ReflowError):
    """
    Raised when a Docker operation fails.
    """


# =====================================================
# Configuration
# =====================================================


class ConfigurationError(ReflowError):
    """
    Raised when configuration is invalid.
    """


# =====================================================
# Validation
# =====================================================


class ValidationError(ReflowError):
    """
    Raised when validation fails.
    """

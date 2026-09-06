# tests/conftest.py

"""
Shared pytest fixtures.

This module contains reusable fixtures shared across the
entire test suite.
"""

from unittest.mock import Mock

import pytest

from app.core.shared.result import CommandResult

# =====================================================
# Generic Mocks
# =====================================================


@pytest.fixture
def mock_executor():
    """
    Create a generic mock executor.
    """
    return Mock()


@pytest.fixture
def mock_config():
    """
    Create a generic mock configuration.
    """
    config = Mock()

    config.resolve.return_value = "origin"

    return config


@pytest.fixture
def mock_git():
    """
    Create a mock Git service.
    """
    return Mock()


@pytest.fixture
def mock_github():
    """
    Create a mock GitHub service.
    """
    return Mock()


@pytest.fixture
def mock_docker():
    """
    Create a mock Docker service.
    """
    return Mock()


@pytest.fixture
def mock_dockerize_config(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """Install deterministic registry settings for Docker CLI workflow tests."""
    config = Mock()
    configured_values = {
        ("docker", "provider"): "github",
        ("github", "image"): "ghcr.io/devalltect00/testing_reflow",
        ("gitlab", "image"): "registry.gitlab.com/example/unused",
        ("docker", "keep_local_images"): False,
    }
    config.resolve.side_effect = lambda *, cli_value, config_keys, default=None: (
        cli_value
        if cli_value is not None
        else configured_values.get(tuple(config_keys), default)
    )
    monkeypatch.setattr(
        "app.cli.commands.reflow.dockerize.resolver.get_config",
        Mock(return_value=config),
    )
    return config


# =====================================================
# Command Results
# =====================================================


@pytest.fixture
def success_result():
    """
    Create a successful command result.
    """
    return CommandResult(
        returncode=0,
        stdout="",
        stderr="",
    )


@pytest.fixture
def failed_result():
    """
    Create a failed command result.
    """
    return CommandResult(
        returncode=1,
        stdout="",
        stderr="error",
    )


@pytest.fixture
def dry_run_result():
    """
    Create a successful dry-run result.
    """
    return CommandResult.dry_run()

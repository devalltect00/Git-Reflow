# app/cli/commands/reflow/dockerize/resolver.py

"""
Resolver utilities for:

    reflow dockerize

This module converts:

    CLI arguments
        +
    configuration values
        +
    defaults

into a strongly typed DockerizeArgs object.
"""

from app.cli.commands.reflow.dockerize.models import DockerizeArgs
from app.config.config_loader import get_config
from app.core.shared import ConfigurationError


def _validate_provider(
    provider: str,
) -> None:
    """
    Validate registry provider.

    Workflow:
        1. Check provider value.
        2. Verify supported provider.
        3. Raise configuration error if invalid.

    Args:
        provider (str):
            Provider name.

    Raises:
        ConfigurationError:
            If provider is invalid.
    """
    if provider not in (
        "github",
        "gitlab",
        "both",
    ):
        raise ConfigurationError(
            f"Invalid docker provider '{provider}'. Expected: github, gitlab, or both."
        )


def _validate_images(
    *,
    provider: str,
    github_image: str | None,
    gitlab_image: str | None,
) -> None:
    """
    Validate registry image configuration.

    Workflow:
        1. Check GitHub image if required.
        2. Check GitLab image if required.
        3. Raise configuration error if missing.

    Args:
        provider (str):
            Selected provider.

        github_image (str | None):
            GitHub image.

        gitlab_image (str | None):
            GitLab image.

    Raises:
        ConfigurationError:
            If required image is missing.
    """
    if (
        provider
        in (
            "github",
            "both",
        )
        and not github_image
    ):
        raise ConfigurationError("Missing GitHub image configuration.")

    if (
        provider
        in (
            "gitlab",
            "both",
        )
        and not gitlab_image
    ):
        raise ConfigurationError("Missing GitLab image configuration.")


def _validate_configuration(
    *,
    provider: str,
    github_image: str | None,
    gitlab_image: str | None,
) -> None:
    """
    Validate Docker configuration.

    Workflow:
        1. Validate provider.
        2. Validate image configuration.

    Args:
        provider (str):
            Registry provider.

        github_image (str | None):
            GitHub image.

        gitlab_image (str | None):
            GitLab image.
    """
    _validate_provider(
        provider,
    )

    _validate_images(
        provider=provider,
        github_image=github_image,
        gitlab_image=gitlab_image,
    )


def resolve_dockerize_args(
    *,
    execution_args,
) -> DockerizeArgs:
    """
    Resolve dockerize arguments.

    Priority:

        CLI
            ↓
        config.toml
            ↓
        defaults

    Workflow:
        1. Load configuration.
        2. Resolve provider.
        3. Resolve registry images.
        4. Resolve execution settings.
        5. Validate configuration.
        6. Return strongly typed arguments.

    Returns:
        DockerizeArgs
    """
    config = get_config()

    provider = config.resolve(
        cli_value=None,
        config_keys=[
            "docker",
            "provider",
        ],
        default="github",
    )

    github_image = config.resolve(
        cli_value=None,
        config_keys=[
            "github",
            "image",
        ],
        default=None,
    )

    gitlab_image = config.resolve(
        cli_value=None,
        config_keys=[
            "gitlab",
            "image",
        ],
        default=None,
    )

    keep_local_images = config.resolve(
        cli_value=None,
        config_keys=[
            "docker",
            "keep_local_images",
        ],
        default=False,
    )

    _validate_configuration(
        provider=provider,
        github_image=github_image,
        gitlab_image=gitlab_image,
    )

    if provider in ("github", "both"):
        assert github_image is not None

    if provider in ("gitlab", "both"):
        assert gitlab_image is not None

    return DockerizeArgs(
        **execution_args.model_dump(),
        provider=provider,
        github_image=github_image,
        gitlab_image=gitlab_image,
        keep_local_images=keep_local_images,
    )

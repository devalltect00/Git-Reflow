# app/cli/commands/reflow/tags/convert/resolver.py

"""
Resolver utilities for:

    reflow tags convert local|remote

This module converts:

    CLI arguments
        +
    configuration values
        +
    defaults

into a strongly typed ConvertTagsArgs object.
"""

from app.cli.commands.reflow.tags.convert.models import (
    ConvertTagsArgs,
    TagConversionScope,
)
from app.config.config_loader import (
    get_config,
)
from app.core.reflow import TagFormat
from app.core.shared import ConfigurationError


def resolve_convert_tags_args(
    *,
    execution_args,
    scope: TagConversionScope,
    target_format: TagFormat | str | None = None,
    yes: bool | None = None,
) -> ConvertTagsArgs:
    """
    Resolve convert-tags arguments.

    Workflow:
        1. Load configuration.
        2. Validate local/remote target compatibility.
        3. Resolve and validate the destination format.
        4. Resolve confirmation behavior.
        5. Merge execution arguments.
        6. Return strongly typed model.

    Priority:
        1. CLI argument
        2. Configuration file
        3. Internal default

    Args:
        execution_args:
            Shared execution arguments.

        scope:
            Explicit local or remote conversion scope.

        target_format:
            CLI supplied destination format.

        yes:
            CLI supplied non-interactive confirmation value.

    Returns:
        ConvertTagsArgs
    """
    config = get_config()

    if scope is TagConversionScope.LOCAL and execution_args.repository.is_remote:
        raise ConfigurationError(
            "'reflow tags convert local' requires a persistent local checkout. "
            "Clone the repository and use --repository/-C, or choose "
            "'reflow tags convert remote' for --repository-url."
        )
    raw_target_format = config.resolve(
        cli_value=target_format,
        config_keys=[
            "cli",
            "tags",
            "convert",
            "target_format",
        ],
        default=TagFormat.SEMVER,
    )
    resolved_yes = config.resolve(
        cli_value=yes,
        config_keys=[
            "cli",
            "tags",
            "convert",
            "yes",
        ],
        default=False,
    )

    try:
        resolved_target_format = TagFormat.from_value(raw_target_format)
    except ValueError as exc:
        raise ConfigurationError(str(exc)) from exc

    return ConvertTagsArgs(
        **execution_args.model_dump(),
        scope=scope,
        target_format=resolved_target_format,
        yes=resolved_yes,
    )

# app/cli/commands/reflow/tags/replay/resolver.py

"""
Resolver utilities for:

    reflow tags replay

This module converts:

    CLI arguments
        +
    configuration values
        +
    defaults

into a strongly typed ReplayTagsArgs object.
"""

from app.cli.commands.reflow.tags.replay.models import (
    ReplayTagsArgs,
)
from app.config.config_loader import get_config


def resolve_replay_tags_args(
    *,
    execution_args,
    delay,
    only_stable,
    limit,
) -> ReplayTagsArgs:
    """
    Resolve replay-tags arguments.

    Priority:

        CLI
            ↓
        config.toml
            ↓
        defaults

    Returns
    -------
    ReplayTagsArgs
    """

    config = get_config()

    return ReplayTagsArgs(
        **execution_args.model_dump(),
        delay=config.resolve(
            delay,
            ["cli", "tags", "replay", "delay"],
            2,
        ),
        only_stable=config.resolve(
            only_stable,
            ["cli", "tags", "replay", "only_stable"],
            False,
        ),
        limit=config.resolve(
            limit,
            ["cli", "tags", "replay", "limit"],
            None,
        ),
    )

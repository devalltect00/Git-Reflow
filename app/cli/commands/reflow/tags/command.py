# app/cli/commands/reflow/tags/command.py

"""
Parent command group for:

    reflow tags

Provides:

    reflow tags replay (deprecated compatibility alias)
    reflow tags convert local|remote
"""

import typer

from app.cli.commands.reflow.tags.convert.command import (
    app as convert_app,
)
from app.cli.commands.reflow.tags.replay.command import (
    app as replay_app,
)

app = typer.Typer(
    help="""
    Git tag related commands.

    Examples
    --------

        reflow tags replay  # deprecated; use releases recover

        reflow tags convert local
    """,
    rich_help_panel="Tags",
)

# =========================================================
# REPLAY
# =========================================================

app.add_typer(
    replay_app,
    name="replay",
)

# =========================================================
# CONVERT
# =========================================================

app.add_typer(
    convert_app,
    name="convert",
)

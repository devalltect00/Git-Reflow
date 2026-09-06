# app/cli/commands/reflow/command.py

"""
Parent command group for:

    reflow

Provides:

    reflow releases recover
    reflow tags convert local|remote
    reflow dockerize
"""

import typer

from app.cli.commands.reflow.dockerize.command import (
    app as dockerize_app,
)
from app.cli.commands.reflow.releases.command import app as releases_app
from app.cli.commands.reflow.tags.command import (
    app as tags_app,
)

app = typer.Typer(
    help="""
    Release workflow automation commands.

    Examples
    --------

        reflow releases recover

        reflow tags convert local

        reflow dockerize
    """,
    rich_help_panel="Release Flow",
)

# =========================================================
# TAGS
# =========================================================

app.add_typer(
    tags_app,
    name="tags",
)

app.add_typer(
    releases_app,
    name="releases",
)

# =========================================================
# DOCKER
# =========================================================

app.add_typer(
    dockerize_app,
    name="dockerize",
)

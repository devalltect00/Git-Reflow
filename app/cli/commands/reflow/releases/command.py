# app/cli/commands/reflow/releases/command.py

"""Parent command group for release-management workflows."""

import typer

from app.cli.commands.reflow.releases.recover.command import app as recover_app

app = typer.Typer(
    help="Manage and recover repository releases.",
    rich_help_panel="Releases",
)

app.add_typer(
    recover_app,
    name="recover",
)

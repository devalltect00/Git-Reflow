# app/cli/main.py

"""
Main CLI application.

Entrypoint for Reflow.
"""

import typer

from app.cli.commands import init_command, main_command, reflow_command
from app.ui.console import console

typer.rich_utils._console = console

app = typer.Typer(
    name="reflow",
    help="Release workflow automation toolkit.",
    no_args_is_help=True,
    add_help_option=False,
    add_completion=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)

# =========================================================
# GLOBAL BOOTSTRAP
# =========================================================

app.callback(
    invoke_without_command=True,
)(
    main_command.main,
)

# =========================================================
# STANDALONE COMMANDS
# =========================================================

app.command()(
    init_command.init,
)

# =========================================================
# COMMAND GROUPS
# =========================================================

app.add_typer(
    reflow_command.app,
    # name="reflow",
)

# Optional alias
# app.add_typer(
#     reflow_command.app,
#     name="workflow",
# )


def main() -> None:
    """
    CLI entrypoint.
    """
    app()

# app/cli/commands/main/options.py

from pathlib import Path
from typing import Annotated

import typer

from app.cli.constants.enums import LogLevelChoices
from app.cli.utils import version_callback

# ---------------------------
# 🧩 APPLICATION OPTIONS
# ---------------------------
NoBannerOption = Annotated[
    bool | None,
    typer.Option(
        "--no-banner",
        help="""
        Disable banner

        [dim blue]Default:[/dim blue] [red]False[/red]
        """,
    ),
]
HelpOption = Annotated[
    bool | None,
    typer.Option(
        "--help",
        "-h",
        help="Show help",
    ),
]
VersionOption = Annotated[
    bool | None,
    typer.Option(
        "--version",
        "-v",
        help="Get app version",
        callback=version_callback,
    ),
]

RepositoryOption = Annotated[
    Path | None,
    typer.Option(
        "--repository",
        "--repo",
        "-C",
        help="""
        Local repository directory operated on by Reflow.

        Relative paths are resolved from the invocation directory.
        The default is the current directory.
        """,
        rich_help_panel="Global • Target",
        file_okay=False,
        dir_okay=True,
        resolve_path=False,
    ),
]

RepositoryUrlOption = Annotated[
    str | None,
    typer.Option(
        "--repository-url",
        help="""
        Remote Git repository URL operated on through a temporary clone.

        Supports HTTPS, SSH, Git-protocol, and SCP-style Git URLs.
        Cannot be combined with --repository, --repo, or -C.
        """,
        rich_help_panel="Global • Target",
    ),
]


# ---------------------------
# ⚙️ EXECUTION OPTIONS
# ---------------------------
DryRunOption = Annotated[
    bool | None,
    typer.Option(
        "--dry-run/--no-dry-run",
        "-dr/-Dr",
        help="""
        [bold yellow]Dry run mode[/bold yellow]

        Preview the workflow without persistent local or remote changes.

        Read-only discovery may still run.
        Mutating operations are simulated.

        Useful for testing workflow safely.

        [dim yellow]HINT:[/dim yellow]: Useful for debugging
        """,
        rich_help_panel="Global • Execution",
    ),
]


# ---------------------------
# 📝 LOGGING OPTIONS
# ---------------------------
DebugOption = Annotated[
    bool | None,
    typer.Option(
        "--debug/--no-debug",
        "-dbg/-Dbg",
        help="""
        [bold yellow]Debugging mode[/bold yellow]

        [green]Show[/green]/[blue]Hide[/blue] debug message.
        """,
        rich_help_panel="Global • Debug",
    ),
]
LogLevelOption = Annotated[
    LogLevelChoices | None,
    typer.Option(
        "--log-level",
        "-ll",
        help="""
        [bold]Logging level[/bold]

        Control verbosity of logs

        [bold yellow]•[/bold yellow] [bold]critical[/bold] → only critical errors\n
        [bold yellow]•[/bold yellow] [bold]error[/bold]    → errors only\n
        [bold yellow]•[/bold yellow] [bold]warning[/bold]  → warnings + errors\n
        [bold yellow]•[/bold yellow] [bold]info[/bold]     → general info (default\n
        [bold yellow]•[/bold yellow] [bold]debug[/bold]    → detailed debugging\n

        [dim blue]Default:[/dim blue] info

        [dim yellow]HINT:[/dim yellow] better using config.toml configuration.
        [dim]Variable:[/dim] 'tool.reflow.logging.level'
        """,
        rich_help_panel="Global • Debug",
        case_sensitive=False,
    ),
]

# app/cli/commands/init/command.py

from dataclasses import asdict
from types import SimpleNamespace

import typer

from app.cli.commands.init.options import AskOption, ForceOption, ModeOption
from app.cli.commands.init.resolver import resolve_init_args
from app.cli.constants.args import CliArgs
from app.cli.errors import handle_cli_errors

# from app.services import InitService
from app.config.config_loader import get_config
from app.core.initialize.main import InitMain

app = typer.Typer()


@app.callback(
    rich_help_panel="Initialization",
)
@handle_cli_errors(
    "Initialization",
    solution=(
        "Use a writable local repository path, review --mode/--force/--ask, "
        "and run with --dry-run before retrying."
    ),
)

# @app.command("init")
def init(
    ctx: typer.Context,
    mode: ModeOption = None,
    force_init: ForceOption = None,
    ask: AskOption = None,
):
    """
    Initialize a Reflow Project

    Create configuration files and project scaffolding
    required to start using Reflow.

    [dim]Recommended for first-time setup, new repositories,
    or recovering missing project files.[/dim]

    ────────────────────────────────────────

    📦 [bold]What This Command Creates[/bold]

    • config.toml
    • **version**.py
    • Templates (optional)
    • Examples (optional)

    ────────────────────────────────────────

    🚀 [bold]Typical Workflow[/bold]

    ```
    Install Reflow
            ↓
        reflow init
            ↓
        Edit config.toml
            ↓
    reflow tags convert local
    reflow releases recover
    reflow dockerize
    ```

    ────────────────────────────────────────

    ⚙️ [bold]Modes[/bold]

    [cyan]config[/cyan]

    ```
    Create configuration files only.
    ```

    [cyan]templates[/cyan]

    ```
    Create template files only.
    ```

    [cyan]examples[/cyan]

    ```
    Create example files only.
    ```

    [cyan]all[/cyan]

    ```
    Create everything.
    ```

    ────────────────────────────────────────

    🧪 [bold]Examples[/bold]

    [yellow]reflow init[/yellow]

    ```
    Initialize everything.
    ```

    [yellow]reflow init --mode config[/yellow]

    ```
    Create configuration files only.
    ```

    [yellow]reflow init --force[/yellow]

    ```
    Overwrite existing files.
    ```

    [yellow]reflow init --ask[/yellow]

    ```
    Ask before creating or overwriting files.
    ```

    [yellow]reflow --dry-run init[/yellow]

    ```
    Preview changes without writing files.
    ```

    ────────────────────────────────────────

    💡 [bold]Tips[/bold]

    • Safe to run multiple times.
    • Start with [cyan]reflow init[/cyan] after installation.
    • Use [cyan]--mode[/cyan] when you only need a specific setup.
    • Initialization requires a local target; --repository-url is not supported.

    ────────────────────────────────────────

    📚 [bold]Documentation[/bold]

    docs/init/
    docs/user-guide/getting-started.md
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        mode=mode,
        force_init=force_init,
        ask=ask,
    )

    execution_args = ctx.obj.execution_args
    repository = execution_args.repository.require_local(command="reflow init")

    args = resolve_init_args(config=config, cli_args=cli_args)

    combined_args = SimpleNamespace(
        # **vars(args),
        **asdict(args),
        dry_run=execution_args.dry_run,
        debug=execution_args.debug,
        log_level=execution_args.log_level,
        silent=execution_args.silent,
        repository=repository,
        progress_enabled=execution_args.progress_enabled,
    )

    InitMain().execute(combined_args)

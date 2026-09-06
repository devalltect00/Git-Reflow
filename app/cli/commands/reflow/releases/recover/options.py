# app/cli/commands/reflow/releases/recover/options.py

"""CLI options for ``reflow releases recover``."""

from typing import Annotated

import typer

DelayOption = Annotated[
    int | None,
    typer.Option(
        "--delay",
        "-d",
        min=0,
        help="Delay in seconds between remote tag re-push operations.",
    ),
]

OnlyStableOption = Annotated[
    bool | None,
    typer.Option(
        "--only-stable",
        help="Recover stable releases only.",
    ),
]

LimitOption = Annotated[
    int | None,
    typer.Option(
        "--limit",
        "-l",
        min=1,
        help="Maximum number of selected tags to process.",
    ),
]

YesOption = Annotated[
    bool,
    typer.Option(
        "--yes",
        "-y",
        help="Confirm remote tag deletion and re-push without prompting.",
    ),
]

# app/cli/commands/reflow/tags/convert/options.py

"""
CLI options for:

    reflow tags convert local|remote

The options control destination format and confirmation behavior. Persistence
is selected explicitly by the ``local`` or ``remote`` subcommand.
"""

from typing import Annotated

import typer

from app.core.reflow import TagFormat

TargetFormatOption = Annotated[
    TagFormat | None,
    typer.Option(
        "--to",
        "--format",
        "--target-format",
        help="Destination format: semver (default) or pep440.",
    ),
]

YesOption = Annotated[
    bool | None,
    typer.Option(
        "--yes",
        "-y",
        help="Apply the displayed local or remote replacement plan without prompting.",
    ),
]

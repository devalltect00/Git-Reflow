# app/cli/commands/reflow/tags/replay/options.py

"""
CLI options for:

    reflow tags replay
"""

from typing import Annotated

import typer

# =========================================================
# DELAY
# =========================================================

DelayOption = Annotated[
    int | None,
    typer.Option(
        "--delay",
        "-d",
        help="""
        Delay between tag replay operations.

        Example:

            --delay 2
            --delay 5

        Value is expressed in seconds.
        """,
    ),
]

# =========================================================
# ONLY STABLE
# =========================================================

OnlyStableOption = Annotated[
    bool | None,
    typer.Option(
        "--only-stable",
        help="""
        Replay stable releases only.

        Excludes:

            alpha
            beta
            rc
            dev
        """,
    ),
]

# =========================================================
# LIMIT
# =========================================================

LimitOption = Annotated[
    int | None,
    typer.Option(
        "--limit",
        "-l",
        help="""
        Maximum number of tags to replay.

        Examples:

            --limit 10
            --limit 50
        """,
    ),
]

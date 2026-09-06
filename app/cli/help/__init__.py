# app/cli/help/__init__.py

"""
CLI help messages.

This package contains rich help text used by
Typer commands.

Keeping help text outside command modules
makes command implementations smaller and
easier to maintain.
"""

from .init.help import INIT_HELP
from .main.help import ROOT_HELP
from .reflow.dockerize.help import DOCKERIZE_HELP
from .reflow.releases.recover.help import RECOVER_RELEASES_HELP
from .reflow.tags.convert.help import CONVERT_HELP
from .reflow.tags.replay.help import REPLAY_HELP

__all__ = [
    "ROOT_HELP",
    "INIT_HELP",
    "REPLAY_HELP",
    "RECOVER_RELEASES_HELP",
    "CONVERT_HELP",
    "DOCKERIZE_HELP",
]

# app/cli/commands/init/models.py

from dataclasses import dataclass

from app.cli.constants.enums import InitMode


@dataclass(slots=True)
class InitArgs:
    mode: InitMode
    force_init: bool
    ask: bool

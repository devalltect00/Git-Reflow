# app/cli/commands/main/models.py

from dataclasses import dataclass

from app.cli.constants.enums import LogLevelChoices
from app.core.repository import RepositoryTarget


@dataclass
class MainArgs:
    no_banner: bool
    help: bool
    version: bool | None
    dry_run: bool
    debug: bool
    log_level: LogLevelChoices
    repository: RepositoryTarget
    progress_enabled: bool

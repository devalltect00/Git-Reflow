# app\utils\dry_run_support.py

from app.utils.dry_run import Runner


class DryRunSupport:
    """
    Base class providing dry-run support.
    """

    def __init__(self, dry_run: bool = False):
        self.runner = Runner(dry_run)
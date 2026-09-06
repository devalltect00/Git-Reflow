# app/core/reflow/release_recovery.py

"""
Release recovery workflow.

The public name describes the user outcome while the compatibility
``Orchestrator`` class retains the existing implementation and API.
"""

from app.core.reflow.orchestrator import Orchestrator


class ReleaseRecovery(Orchestrator):
    """
    Recover missing GitHub releases by re-pushing existing remote tags.

    This class intentionally inherits the established orchestration behavior so
    the former ``reflow tags replay`` entry point can remain a compatible alias.
    """

# tests/test_runtime_imports.py

"""Regression tests for working-directory-independent CLI startup."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cli_import_does_not_require_an_app_directory(tmp_path: Path) -> None:
    """Importing the installed entry point must not inspect the target checkout."""

    environment = os.environ.copy()
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = os.pathsep.join(
        value for value in (str(PROJECT_ROOT), existing_pythonpath) if value
    )

    result = subprocess.run(
        [sys.executable, "-c", "from app.cli.main import app"],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )

    assert result.returncode == 0, result.stderr

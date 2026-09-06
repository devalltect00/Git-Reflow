# app/__main__.py

"""
Application entrypoint.
Entrypoint for reflow CLI.

This module allows the project to be executed using:

    python -m app

It delegates execution to the CLI application.
"""

from app.cli.main import app

if __name__ == "__main__":
    app()

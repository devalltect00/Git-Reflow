# tests/cli/test_main_command.py

"""Tests for root CLI initialization and informational options."""

from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

from app.cli.main import app

runner = CliRunner()


def test_root_without_arguments_shows_banner_and_help(monkeypatch) -> None:
    """Bare invocation should run the callback before showing successful help."""

    show_banner = Mock()
    get_config = Mock(side_effect=AssertionError("configuration must not load"))
    monkeypatch.setattr("app.cli.commands.main.command.banner.show", show_banner)
    monkeypatch.setattr("app.cli.commands.main.command.get_config", get_config)

    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Release workflow automation toolkit" in result.stdout
    show_banner.assert_called_once_with()
    get_config.assert_not_called()


def test_root_without_arguments_honors_no_banner(monkeypatch) -> None:
    """The no-banner flag should suppress art during bare invocation."""

    show_banner = Mock()
    monkeypatch.setattr("app.cli.commands.main.command.banner.show", show_banner)

    result = runner.invoke(app, ["--no-banner"])

    assert result.exit_code == 0
    assert "Release workflow automation toolkit" in result.stdout
    show_banner.assert_not_called()


def test_explicit_root_help_shows_banner_by_default(monkeypatch) -> None:
    """Explicit help should retain the same banner contract as bare help."""

    show_banner = Mock()
    monkeypatch.setattr("app.cli.commands.main.command.banner.show", show_banner)

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    show_banner.assert_called_once_with()


def test_root_help_does_not_load_operational_configuration(monkeypatch) -> None:
    """Root help should work when configured repository paths are unavailable."""

    get_config = Mock(side_effect=AssertionError("configuration must not load"))
    monkeypatch.setattr("app.cli.commands.main.command.get_config", get_config)

    result = runner.invoke(app, ["--no-banner", "--help"])

    assert result.exit_code == 0
    assert "Release workflow automation toolkit" in result.stdout
    get_config.assert_not_called()


@pytest.mark.parametrize(
    "arguments",
    [
        ["releases", "recover", "--help"],
        ["tags", "--help"],
        ["tags", "replay", "--help"],
    ],
)
def test_nested_help_does_not_load_operational_configuration(
    monkeypatch,
    arguments: list[str],
) -> None:
    """Nested help should remain available while configuration is invalid."""

    get_config = Mock(side_effect=AssertionError("configuration must not load"))
    monkeypatch.setattr("app.cli.commands.main.command.get_config", get_config)

    result = runner.invoke(app, ["--no-banner", *arguments])

    assert result.exit_code == 0
    get_config.assert_not_called()

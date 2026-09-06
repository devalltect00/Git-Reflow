# tests/config/test_config_loader.py

"""
Tests for ConfigLoader.

This module tests configuration loading,
access helpers, and resolution logic.
"""

import pytest

from app.config.config_loader import (
    ConfigLoader,
    get_config,
)
from app.core.shared import ConfigurationError


class TestConfigLoader:
    """
    Tests for ConfigLoader.
    """

    # =====================================================
    # Loading
    # =====================================================

    def test_load_missing_file(
        self,
        tmp_path,
    ):
        """
        Should return empty config
        when file does not exist.
        """
        missing_file = tmp_path / "missing.toml"

        config = ConfigLoader(
            filename=str(missing_file),
        )

        assert config.config == {}

    def test_load_valid_config(
        self,
        tmp_path,
    ):
        """
        Should load TOML configuration.
        """
        config_file = tmp_path / "config.toml"

        config_file.write_text(
            """
[tool.reflow.git]
remote = "origin"
""",
            encoding="utf-8",
        )

        config = ConfigLoader(
            filename=str(config_file),
        )

        assert (
            config.get(
                "git",
                "remote",
            )
            == "origin"
        )

    def test_load_invalid_toml(
        self,
        tmp_path,
    ):
        """
        Should raise ConfigurationError
        for invalid TOML.
        """
        config_file = tmp_path / "config.toml"

        config_file.write_text(
            "[tool.reflow",
            encoding="utf-8",
        )

        with pytest.raises(
            ConfigurationError,
        ):
            ConfigLoader(
                filename=str(config_file),
            )

    # =====================================================
    # get
    # =====================================================

    def test_get_nested_value(
        self,
        tmp_path,
    ):
        """
        Should return nested value.
        """
        config_file = tmp_path / "config.toml"

        config_file.write_text(
            """
[tool.reflow.git]
remote = "origin"
""",
            encoding="utf-8",
        )

        config = ConfigLoader(
            filename=str(config_file),
        )

        assert (
            config.get(
                "git",
                "remote",
            )
            == "origin"
        )

    def test_get_returns_default(
        self,
        tmp_path,
    ):
        """
        Should return default value.
        """
        config = ConfigLoader(
            filename=str(tmp_path / "missing.toml"),
        )

        result = config.get(
            "missing",
            default="fallback",
        )

        assert result == "fallback"

    def test_get_returns_default_when_path_breaks(
        self,
        tmp_path,
    ):
        """
        Should return default when
        nested access reaches
        a non-dictionary value.
        """
        config_file = tmp_path / "config.toml"

        config_file.write_text(
            """
[tool.reflow.git]
remote = "origin"
""",
            encoding="utf-8",
        )

        config = ConfigLoader(
            filename=str(config_file),
        )

        result = config.get(
            "git",
            "remote",
            "invalid",
            default="fallback",
        )

        assert result == "fallback"

    # =====================================================
    # require
    # =====================================================

    def test_require_returns_value(
        self,
        tmp_path,
    ):
        """
        Should return required value.
        """
        config_file = tmp_path / "config.toml"

        config_file.write_text(
            """
[tool.reflow.git]
remote = "origin"
""",
            encoding="utf-8",
        )

        config = ConfigLoader(
            filename=str(config_file),
        )

        assert (
            config.require(
                "git",
                "remote",
            )
            == "origin"
        )

    def test_require_raises_for_missing_value(
        self,
        tmp_path,
    ):
        """
        Should raise ConfigurationError
        for missing value.
        """
        config = ConfigLoader(
            filename=str(tmp_path / "missing.toml"),
        )

        with pytest.raises(
            ConfigurationError,
        ):
            config.require(
                "git",
                "remote",
            )

    # =====================================================
    # get_section
    # =====================================================

    def test_get_section_returns_dict(
        self,
        tmp_path,
    ):
        """
        Should return section dictionary.
        """
        config_file = tmp_path / "config.toml"

        config_file.write_text(
            """
[tool.reflow.git]
remote = "origin"
branch = "main"
""",
            encoding="utf-8",
        )

        config = ConfigLoader(
            filename=str(config_file),
        )

        result = config.get_section(
            "git",
        )

        assert result == {
            "remote": "origin",
            "branch": "main",
        }

    def test_get_section_returns_empty_dict(
        self,
        tmp_path,
    ):
        """
        Should return empty dictionary
        for missing section.
        """
        config = ConfigLoader(
            filename=str(tmp_path / "missing.toml"),
        )

        assert (
            config.get_section(
                "missing",
            )
            == {}
        )

    # =====================================================
    # resolve
    # =====================================================

    def test_resolve_prefers_cli_value(
        self,
        tmp_path,
    ):
        """
        CLI value should win.
        """
        config = ConfigLoader(
            filename=str(tmp_path / "missing.toml"),
        )

        result = config.resolve(
            cli_value="cli",
            config_keys=["git", "remote"],
            default="default",
        )

        assert result == "cli"

    def test_resolve_uses_config_value(
        self,
        tmp_path,
    ):
        """
        Config value should be used
        when CLI value is missing.
        """
        config_file = tmp_path / "config.toml"

        config_file.write_text(
            """
[tool.reflow.git]
remote = "origin"
""",
            encoding="utf-8",
        )

        config = ConfigLoader(
            filename=str(config_file),
        )

        result = config.resolve(
            cli_value=None,
            config_keys=["git", "remote"],
            default="default",
        )

        assert result == "origin"

    def test_resolve_uses_default(
        self,
        tmp_path,
    ):
        """
        Default value should be used.
        """
        config = ConfigLoader(
            filename=str(tmp_path / "missing.toml"),
        )

        result = config.resolve(
            cli_value=None,
            config_keys=["git", "remote"],
            default="default",
        )

        assert result == "default"

    def test_resolve_treats_false_as_none(
        self,
        tmp_path,
    ):
        """
        False can be treated as missing.
        """
        config = ConfigLoader(
            filename=str(tmp_path / "missing.toml"),
        )

        result = config.resolve(
            cli_value=False,
            config_keys=["git", "remote"],
            default="default",
            treat_false_as_none=True,
        )

        assert result == "default"

    def test_resolve_required_raises(
        self,
        tmp_path,
    ):
        """
        Required values should raise
        when missing.
        """
        config = ConfigLoader(
            filename=str(tmp_path / "missing.toml"),
        )

        with pytest.raises(
            ConfigurationError,
        ):
            config.resolve(
                cli_value=None,
                config_keys=["git", "remote"],
                required=True,
            )


class TestSingleton:
    """
    Tests for shared ConfigLoader instance.
    """

    def test_get_config_returns_singleton(
        self,
        monkeypatch,
    ):
        """
        Should return same instance.
        """
        import app.config.config_loader as module

        monkeypatch.setattr(
            module,
            "_config_instance",
            None,
        )

        config1 = get_config()
        config2 = get_config()

        assert config1 is config2

# app/core/initialize/registry.py

from app.constants.path import (
    REFLOW_SETTINGS,
)
from app.core.initialize.loader import load_template
from app.core.initialize.models.template_file import TemplateFile


class DirRegistry:
    @staticmethod
    def get_config_directories() -> list[str]:
        return [".config/reflow"]

    def get_all_directories(self) -> list[str]:
        return [
            *self.get_config_directories(),
        ]


class FileRegistry:
    def __init__(self):
        # =========================
        # CONFIG
        # =========================
        self.config = TemplateFile(
            target_path=REFLOW_SETTINGS,
            content=lambda: load_template("config.toml"),
        )

    @staticmethod
    def get_config() -> list[TemplateFile]:
        # =========================
        # CONFIG
        # =========================
        return [
            TemplateFile(
                target_path=REFLOW_SETTINGS,
                content=lambda: load_template("config.toml"),
            )
        ]

    def get_all_files(self) -> list[TemplateFile]:
        return [
            *self.get_config(),
        ]

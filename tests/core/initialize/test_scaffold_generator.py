# tests/core/initialize/test_scaffold_generator.py

"""Tests for repository-aware project scaffold generation."""

from pathlib import Path

from app.core.initialize.models.template_file import TemplateFile
from app.core.initialize.services.scaffold_generator import ScaffoldGenerator


def test_run_writes_only_under_selected_repository(tmp_path: Path) -> None:
    """Create initialization directories and files below the target root."""
    generator = ScaffoldGenerator(root_directory=tmp_path)
    template = TemplateFile(
        target_path=".config/reflow/config.toml",
        content=lambda: "[tool.reflow]\n",
    )

    result = generator.run(
        mode="config",
        dirs=[".config/reflow"],
        templates=[template],
    )

    target = tmp_path / ".config" / "reflow" / "config.toml"
    assert target.read_text(encoding="utf-8") == "[tool.reflow]\n"
    assert result.created_directories == 1
    assert result.created_files == 1


def test_dry_run_previews_without_writing(tmp_path: Path) -> None:
    """Leave the selected repository unchanged during initialization preview."""
    generator = ScaffoldGenerator(
        root_directory=tmp_path,
        dry_run=True,
    )
    template = TemplateFile(
        target_path=".config/reflow/config.toml",
        content=lambda: "[tool.reflow]\n",
    )

    result = generator.run(
        mode="config",
        dirs=[".config/reflow"],
        templates=[template],
    )

    assert not (tmp_path / ".config").exists()
    assert result.created_directories == 0
    assert result.created_files == 0


def test_existing_file_is_skipped_without_force(tmp_path: Path) -> None:
    """Preserve existing target files unless overwrite is requested."""
    target = tmp_path / "config.toml"
    target.write_text("existing", encoding="utf-8")
    generator = ScaffoldGenerator(root_directory=tmp_path)

    result = generator.run(
        mode="config",
        templates=[
            TemplateFile(
                target_path="config.toml",
                content=lambda: "replacement",
            )
        ],
    )

    assert target.read_text(encoding="utf-8") == "existing"
    assert result.skipped_files == 1


def test_force_overwrites_existing_file(tmp_path: Path) -> None:
    """Replace an existing scaffold file when force is enabled."""
    target = tmp_path / "config.toml"
    target.write_text("existing", encoding="utf-8")
    generator = ScaffoldGenerator(root_directory=tmp_path, force=True)

    generator.run(
        mode="config",
        templates=[
            TemplateFile(
                target_path="config.toml",
                content=lambda: "replacement",
            )
        ],
    )

    assert target.read_text(encoding="utf-8") == "replacement"

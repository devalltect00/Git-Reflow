# app/core/initialize/services/scaffold_generator.py

"""
Project scaffold generation.

Responsibilities
----------------

- Create directories
- Generate template files
- Copy template directories
- Track execution statistics
- Return structured execution results

This module intentionally contains no presentation logic.
UI rendering is handled by presenters.
"""

from importlib.resources import files
from pathlib import Path

from app.constants.path import (
    THIS_PROJECT_SOURCE,
)
from app.core.initialize.models.initialization_result import (
    InitializationResult,
)
from app.ui.console import console


class ScaffoldGenerator:
    """
    Execute project initialization.

    Creates files and directories according to the
    initialization specification.
    """

    def __init__(
        self,
        *,
        force: bool = False,
        interactive: bool = False,
        dry_run: bool = False,
        root_directory: Path | None = None,
    ) -> None:
        """
        Initialize scaffold generation.

        Args:
            force:
                Overwrite existing files.

            interactive:
                Ask before overwriting existing files.

            dry_run:
                Preview file operations without writing.

            root_directory:
                Repository directory below which relative targets are created.
        """
        self.force = force
        self.interactive = interactive
        self.dry_run = dry_run
        self.root_directory = (root_directory or Path.cwd()).resolve()

        self.created_files = 0
        self.copied_files = 0
        self.skipped_files = 0
        self.created_directories = 0

    def resolve_target(self, value: str | Path) -> Path:
        """
        Resolve a scaffold path under the configured repository root.

        Args:
            value:
                Relative or absolute scaffold target.

        Returns:
            Path:
                Absolute scaffold target.
        """

        path = Path(value)
        return path if path.is_absolute() else self.root_directory / path

    def create_directories(
        self,
        directories: list[str],
    ) -> None:
        """
        Create directories.
        """

        for directory in directories:
            path = self.resolve_target(directory)

            if self.dry_run:
                console.print(f"[dry_run](dry-run)[/dry_run] Would create {path}")
                continue

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.created_directories += 1

    def should_write(
        self,
        path: Path,
    ) -> bool:
        """
        Determine whether a file should be written.
        """

        if not path.exists():
            return True

        if self.force:
            return True

        if self.interactive:
            answer = input(f"{path} exists. Overwrite? (y/N): ")

            return answer.lower() == "y"

        return False

    def write_file(
        self,
        template,
    ) -> None:
        """
        Generate a template file.
        """

        path = self.resolve_target(template.target_path)

        if not self.should_write(path):
            self.skipped_files += 1

            console.print(f"[yellow]Skipped[/yellow] {path}")

            return

        if self.dry_run:
            console.print(f"[dry_run](dry-run)[/dry_run] Would create {path}")
            return

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        content = template.render()

        path.write_text(
            content,
            encoding="utf-8",
        )

        self.created_files += 1

        console.print(f"[green]Created[/green] {path}")

    def copy_package_dir(
        self,
        package_path: str,
        target_path: str,
        *,
        force: bool = False,
    ) -> None:
        """
        Copy packaged template directory.
        """

        src_root = files(f"{THIS_PROJECT_SOURCE}.templates").joinpath(package_path)

        dst_root = self.resolve_target(target_path)

        if self.dry_run:
            console.print(
                f"[dry_run](dry-run)[/dry_run] Would copy {package_path} to {dst_root}"
            )
            return

        for item in src_root.rglob("*"):
            relative = item.relative_to(src_root)

            target = dst_root / relative

            if item.is_dir():
                target.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                continue

            if target.exists() and not force:
                self.skipped_files += 1

                continue

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            target.write_text(
                item.read_text(
                    encoding="utf-8",
                ),
                encoding="utf-8",
            )

            self.copied_files += 1

            console.print(f"[cyan]Copied[/cyan] {target}")

    def run(
        self,
        *,
        mode: str,
        templates=None,
        dirs=None,
        template_dirs=None,
    ) -> InitializationResult:
        """
        Execute initialization workflow.

        Returns
        -------
        InitializationResult
        """

        if dirs:
            self.create_directories(dirs)

        if templates:
            for template in templates:
                self.write_file(template)

        if template_dirs:
            for template_dir in template_dirs:
                self.copy_package_dir(
                    template_dir.source,
                    template_dir.target,
                    force=self.force,
                )

        return InitializationResult(
            mode=mode,
            created_files=self.created_files,
            copied_files=self.copied_files,
            skipped_files=self.skipped_files,
            created_directories=self.created_directories,
        )

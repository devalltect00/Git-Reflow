# app/core/initialize/main.py

"""
Initialization workflow entry point.

Responsibilities
----------------

- Build initialization configuration
- Build initialization plan
- Execute scaffold generation
- Display progress information
- Display execution summaries
- Handle runtime errors
"""

from time import perf_counter

from app.core.initialize.builder.init_builder import (
    InitBuilder,
)
from app.core.initialize.models.init_config import (
    InitConfig,
)
from app.core.initialize.presenters.initialization_presenter import (
    InitializationPresenter,
)
from app.core.initialize.services.scaffold_generator import (
    ScaffoldGenerator,
)
from app.ui.console import console
from app.ui.panels import success_summary_panel
from app.ui.progress import progress_spinner


class InitMain:
    """
    Initialization workflow coordinator.
    """

    def execute(
        self,
        args,
    ) -> None:
        """
        Execute initialization workflow.

        Parameters
        ----------
        args:
            Resolved initialization arguments.
        """

        start_time = perf_counter()

        try:
            # =====================================================
            # 1. Build configuration
            # =====================================================

            with progress_spinner(
                "Preparing configuration",
                enabled=args.progress_enabled,
            ):
                config = InitConfig(
                    mode=args.mode,
                    force_init=args.force_init,
                    ask=args.ask,
                    dry_run=args.dry_run,
                    no_debug=not args.debug,
                    log_level=args.log_level,
                    repository=args.repository,
                )

            # =====================================================
            # 2. Build execution plan
            # =====================================================
            with progress_spinner(
                "Building initialization plan",
                enabled=args.progress_enabled,
            ):
                spec = InitBuilder(
                    config,
                ).build()

            # =====================================================
            # 3. Execute initialization
            # =====================================================
            with progress_spinner(
                "Initializing project",
                enabled=args.progress_enabled,
            ):
                generator = ScaffoldGenerator(
                    force=config.force_init,
                    interactive=config.ask,
                    dry_run=config.dry_run,
                    root_directory=config.repository,
                )

                console.print("\n")

                result = generator.run(
                    mode=config.mode.value,
                    templates=spec.templates,
                    dirs=spec.dirs,
                    template_dirs=spec.template_dirs,
                )

            console.print()

            # =====================================================
            # 4. Summary Table
            # =====================================================
            console.print(InitializationPresenter().render(result))

            console.print()

            # =====================================================
            # 5. Messages
            # =====================================================
            if spec.messages and not config.dry_run:
                for message in spec.messages:
                    console.print(f"[green]{message}[/green]")

            # =====================================================
            # 6. Success
            # =====================================================
            elapsed_time = perf_counter() - start_time

            console.print()

            if config.dry_run:
                completion_message = (
                    "[bold green]Dry-run preview completed successfully."
                    "[/bold green]\n\n"
                    "No project files or directories were changed.\n"
                    f"[dim]Mode: {config.mode.value}[/dim]"
                )
            else:
                completion_message = (
                    "[bold green]✅ Initialization completed "
                    "successfully.[/bold green]\n\n"
                    f"[dim]Mode: {config.mode.value}[/dim]"
                )

            console.print(
                success_summary_panel(
                    message=completion_message,
                    elapsed_time=elapsed_time,
                )
            )

            console.print("\n[bold yellow]💡 Next Steps[/bold yellow]")

            console.print("  [cyan]reflow releases recover[/cyan]")

        except Exception:
            raise

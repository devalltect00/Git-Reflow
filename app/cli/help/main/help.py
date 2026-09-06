# app/cli/help/main/help.py

"""
Help text for:

    reflow
"""

ROOT_HELP = """
🚀 [bold cyan]Reflow[/bold cyan]

Release Recovery, Version Conversion,
and Docker Release Automation.

Reflow treats Git tags as the source of truth
for releases and automation.

────────────────────────────────────────

📦 [bold]What Reflow Can Do[/bold]

🛟 [bold]Recover Releases[/bold]

```
  Re-trigger release automation
  for existing tags.

  Command:

      reflow releases recover
```

🔀 [bold]Convert Tags[/bold]

```
  Convert PEP 440 tags into
  Semantic Version tags.

  Command:

      reflow tags convert local|remote
```

🐳 [bold]Dockerize Releases[/bold]

```
  Build and publish Docker images
  from Git tags.

  Command:

      reflow dockerize
```

────────────────────────────────────────

🚀 [bold]Getting Started[/bold]

1. Initialize your project

   reflow init

2. Configure Reflow

   Edit:

   ```
    config.toml
   ```

3. Run the commands you need

   reflow tags convert local
   reflow releases recover
   reflow dockerize

────────────────────────────────────────

📖 [bold]Recommended Workflow[/bold]

```
  Install Reflow
         ↓
     reflow init
         ↓
    Edit config.toml
         ↓
  reflow tags convert local
         ↓
  reflow releases recover
         ↓
   reflow dockerize
```

────────────────────────────────────────

📚 [bold]Available Commands[/bold]

[cyan]init[/cyan]

```
  Initialize a Reflow project.
```

[cyan]tags[/cyan]

```
  Version-tag management.

  Subcommands:

      convert
      replay (deprecated alias)
```

[cyan]releases[/cyan]

```
  Release management.

  Subcommands:

      recover
```

[cyan]dockerize[/cyan]

```
  Build and publish Docker images.
```

────────────────────────────────────────

⚙️ [bold]Global Options[/bold]

[cyan]--repository / --repo / -C[/cyan]

```
  Select the local repository operated on by Reflow.
```

[cyan]--repository-url[/cyan]

```
  Clone a GitHub or GitLab repository into a managed
  temporary checkout for this command.

  Cannot be combined with --repository.
```

[cyan]--dry-run[/cyan]

```
  Preview execution without changes.
```

[cyan]--debug[/cyan]

```
  Enable debug logging.
```

[cyan]--log-level[/cyan]

```
  Control logging verbosity.
```

[cyan]--no-banner[/cyan]

```
  Disable startup banner.
```

[cyan]--version[/cyan]

```
  Show application version.
```

────────────────────────────────────────

📚 [bold]Documentation[/bold]

User Guide

```
  docs/user-guide/
```

Commands

```
  docs/user-guide/commands.md
```

Lifecycle

```
  docs/user-guide/lifecycle.md
```

Configuration

```
  docs/configuration.md
```

Questions and Answers

```
  docs/qa/
```

Architecture

```
  docs/architecture/workflow.md
```

────────────────────────────────────────

💡 [bold]Tip[/bold]

New users should start with:

```
  reflow init
```

before running any other command.
"""

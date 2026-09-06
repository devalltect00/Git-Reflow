# app/cli/help/init/help.py

"""
Help text for:

    reflow init
"""

INIT_HELP = """
🚀 [bold cyan]Initialize a Reflow Project[/bold cyan]

Create configuration files and project scaffolding
required to start using Reflow.

[dim]Recommended for first-time setup, new repositories,
or recovering missing project files.[/dim]

────────────────────────────────────────

📦 [bold]What This Command Creates[/bold]

• config.toml
• **version**.py
• Templates (optional)
• Examples (optional)

────────────────────────────────────────

🚀 [bold]Typical Workflow[/bold]

```
  Install Reflow
         ↓
     reflow init
         ↓
    Edit config.toml
         ↓
  reflow tags convert local
  reflow releases recover
  reflow dockerize
```

────────────────────────────────────────

⚙️ [bold]Modes[/bold]

[cyan]config[/cyan]

```
  Create configuration files only.
```

[cyan]templates[/cyan]

```
  Create template files only.
```

[cyan]examples[/cyan]

```
  Create example files only.
```

[cyan]all[/cyan]

```
  Create everything.
```

────────────────────────────────────────

🧪 [bold]Examples[/bold]

[yellow]reflow init[/yellow]

```
  Initialize everything.
```

[yellow]reflow init --mode config[/yellow]

```
  Create configuration files only.
```

[yellow]reflow init --force[/yellow]

```
  Overwrite existing files.
```

[yellow]reflow init --ask[/yellow]

```
  Ask before creating or overwriting files.
```

[yellow]reflow --dry-run init[/yellow]

```
  Preview changes without writing files.
```

────────────────────────────────────────

💡 [bold]Tips[/bold]

• Safe to run multiple times.
• Start with [cyan]reflow init[/cyan] after installation.
• Use [cyan]--mode[/cyan] when you only need a specific setup.

────────────────────────────────────────

📚 [bold]Documentation[/bold]

docs/init/
docs/user-guide/getting-started.md
"""

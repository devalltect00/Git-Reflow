# app/cli/help/reflow/releases/recover/help.py

"""Rich help text for ``reflow releases recover``."""

RECOVER_RELEASES_HELP = """
[bold]Recover Missing Releases[/bold]

Recover missing GitHub releases by deleting and re-pushing their existing
version tags so tag-triggered release automation runs again.

[bold]What this command does[/bold]

1. Reads existing version tags.
2. Checks which tags do not have corresponding GitHub releases.
3. Deletes and re-pushes those selected remote tags.
4. Retriggers tag-based CI/CD release automation.

It does not directly create a release through the GitHub website. It
retriggers your repository's release workflow.

[bold red]Remote effect:[/bold red] selected remote tags are deleted and pushed
again. Use [cyan]--dry-run[/cyan] to preview and [cyan]--yes[/cyan] only after
reviewing the resolved repository.

[bold]Examples[/bold]

    reflow --repository ../testing_reflow --dry-run releases recover
    reflow --repository ../testing_reflow releases recover --only-stable --yes
    reflow --repository-url https://github.com/acme/project.git --dry-run releases recover
"""

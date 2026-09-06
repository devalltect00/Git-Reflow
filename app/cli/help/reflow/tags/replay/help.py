# app/cli/help/reflow/tags/replay/help.py

"""
Help text for:

    reflow tags replay
"""

REPLAY_HELP = """
[bold yellow]⚠ DEPRECATED COMMAND[/bold yellow]

`reflow tags replay` is retained only as a compatibility alias.
Use `reflow releases recover` for all new workflows and scripts.

────────────────────────────────────────

🧩 Delegated behavior

• Reads repository tags
• Checks which tags do not have corresponding GitHub releases
• Deletes and re-pushes those selected remote tags
• Retriggers tag-based CI/CD release automation
• Does not directly create a release through the GitHub website

────────────────────────────────────────

📋 Workflow

1. Print the deprecation warning
2. Delegate to `reflow releases recover`
3. Run the canonical release-recovery workflow

────────────────────────────────────────

⚙️ Requirements

• Git installed
• GitHub CLI installed
• Git repository with tags

────────────────────────────────────────

🧪 Examples

reflow --dry-run releases recover

reflow releases recover --only-stable

reflow releases recover --limit 10

────────────────────────────────────────

💡 Tips

• Do not use this alias in new automation
• Migrate existing scripts to `reflow releases recover`
• Use the global --dry-run option before a live recovery

────────────────────────────────────────

📚 Related Commands

reflow tags convert local
reflow dockerize
"""

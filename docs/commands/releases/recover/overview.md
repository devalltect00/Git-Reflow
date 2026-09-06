# Recover Missing Releases

`reflow releases recover` repairs release automation for tags that already
exist. The name describes the outcome: Reflow finds version tags without a
GitHub release, deletes those tags from the configured remote, and pushes them
again so tag-driven CI/CD can recreate the missing releases.

This is the replacement for the ambiguous `reflow tags replay` name. The old
command remains available as a deprecated compatibility alias.

## What Release Recovery Does

`reflow releases recover`:

1. Reads existing version tags.
2. Checks which tags do not have corresponding GitHub releases.
3. Deletes and re-pushes those selected remote tags.
4. Retriggers tag-based CI/CD release automation.

It does not directly create a release through the GitHub website. It retriggers
your repository's release workflow, which must already be configured to create
the release in response to a tag push.

Tags that already have a GitHub release are skipped.

## Preview First

Release recovery changes remote tags. Start with a dry run:

```bash
reflow --repository ../testing_reflow --dry-run releases recover
```

No local checkout is required when a remote URL is available:

```bash
reflow --repository-url https://github.com/acme/project.git --dry-run releases recover
```

Reflow temporarily clones the URL, uses its `origin` remote, and removes the
checkout afterward. Release discovery and recovery are currently GitHub-only.

Dry-run mode still reads the selected repository's tags and GitHub release
state, but it does not delete or push tags and does not wait between tags.

## Run Recovery

Interactive confirmation is required for a live run:

```bash
reflow --repository ../testing_reflow releases recover
```

For automation, use `--yes` only after reviewing a dry run:

```bash
reflow --repository ../testing_reflow releases recover --only-stable --yes
```

## Options

| Option | Meaning |
| --- | --- |
| `--delay`, `-d` | Seconds between live remote tag re-push operations; minimum `0` |
| `--only-stable` | Select stable version tags only |
| `--limit`, `-l` | Process at most this many selected tags; minimum `1` |
| `--yes`, `-y` | Skip the live-operation confirmation prompt |

Global options such as `--repository` and `--dry-run` must be written before
the command group.

## Configuration

```toml
[tool.reflow.repository]
path = "../testing_reflow"

[tool.reflow.git]
default_remote = "origin"

[tool.reflow.cli.releases.recover]
delay = 2
only_stable = false
# limit = 25
```

To use URL mode, replace `path` with `url`; do not configure both:

```toml
[tool.reflow.repository]
url = "https://github.com/acme/project.git"
```

The CLI target takes precedence over the configured path. If neither is set,
Reflow operates on the current directory.

## Safety Model

- Existing releases are skipped.
- A live run requires confirmation unless `--yes` is supplied.
- Dry-run discovery commands execute so the preview reflects real tags and
  release state; mutating commands are only displayed.
- Failures are collected per tag so remaining selected tags can continue.

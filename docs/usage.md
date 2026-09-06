# Usage

## Overview

This page provides a quick reference for Reflow commands.

For detailed guides, see:

```text id="j3wqpr"
docs/how-to-use.md
docs/user-guide/commands.md
```

---

# Command Structure

Root command:

```bash id="h2kbm1"
reflow
```

Display help:

```bash id="u0vnkg"
reflow --help
```

Display version:

```bash id="pxyvr0"
reflow --version
```

---

# Initialize Project

Initialize a project:

```bash id="vz50kq"
reflow init
```

Configuration only:

```bash id="l9o7zy"
reflow init --mode config
```

Preview changes:

```bash id="km4f6n"
reflow --dry-run init
```

Force overwrite:

```bash id="x8yl0n"
reflow init --force
```

Ask before changes:

```bash id="vch4tx"
reflow init --ask
```

Documentation:

```text id="zw43wy"
docs/init/
```

---

# Tag Commands

Display help:

```bash id="bg79al"
reflow tags --help
```

Available subcommands:

```text id="ps7nuv"
convert
replay
```

---

# Convert Tags

Convert existing tags:

```bash id="w8i73h"
reflow tags convert local
reflow tags convert remote
```

Dry run:

```bash id="tz9v4l"
reflow --dry-run tags convert local
```

Purpose:

```text id="x2j5gd"
PEP440 → SemVer (default)
SemVer → PEP440 (--to pep440)
```

Example:

```text id="by5u9q"
v1.0.0rc1
      ↓
v1.0.0-rc.1
```

Every live conversion displays the selected repository, destination format,
planned mappings, and skipped tags before prompting for `y`/`n`. Use `--yes`
only when that plan has already been reviewed. Dry-run displays the same plan
without prompting or modifying tags.

Documentation:

```text id="wn5a7g"
docs/tags/convert/
```

---

# Recover Releases

Replay releases:

```bash id="w43q7s"
reflow releases recover
```

Dry run:

```bash id="u1x78q"
reflow --dry-run releases recover
```

Purpose:

```text id="y3e4zj"
Recreate GitHub releases
Recover release automation
```

Documentation:

```text id="o5h78w"
docs/commands/releases/recover/
```

---

# Dockerize Images

Build and publish images:

```bash id="r2l0f7"
reflow dockerize
```

Dry run:

```bash id="m6q7tj"
reflow --dry-run dockerize
```

Purpose:

```text id="s7e8af"
Build Docker images
Publish container images
```

Documentation:

```text id="k4x6ws"
docs/dockerize/
```

---

# Global Options

Most commands support:

```text id="j9t2ea"
--repository PATH / --repo PATH / -C PATH
--repository-url URL
--dry-run
--debug
--log-level
```

Example:

```bash id="d7m2pf"
reflow -C ../testing_reflow --dry-run dockerize
```

The target options are global, so write them before `tags`, `releases`, or
`dockerize`. `--repository` and `--repository-url` are mutually exclusive.

## Dry-run behavior

`--dry-run` previews a workflow without persistent changes to the selected
checkout, Git remotes, GitHub or GitLab, or a container registry. Reflow still
runs read-only discovery so the preview can use real tags, commits, releases,
and configuration. A URL target is also cloned into a temporary directory and
removed afterward.

Dry-run summaries use phrases such as `Would replace`, `Would publish`, and
`Preview completed`. The global option must appear before the command:

```bash
reflow --dry-run init
reflow -C ../testing_reflow --dry-run tags convert remote
reflow --repository-url https://github.com/acme/project.git --dry-run releases recover
reflow --repository-url https://gitlab.com/acme/project.git --dry-run dockerize
```

Enable preview mode in configuration when it should be the default:

```toml
[tool.reflow.cli.execution]
dry_run = true
```

An explicit `--no-dry-run` overrides that configured value and enables a live
run. Review the target and planned operations before doing so.

## Progress behavior

Reflow displays activity while cloning URL targets and uses determinate bars
for stage-based or per-tag workflows. The current description identifies work
such as repository discovery, conversion planning, release recovery, or Docker
publishing so a long-running command does not appear frozen.

Progress is also displayed during dry-run because discovery and simulation are
still real work. It does not indicate that a persistent mutation occurred.
Disable only the UI, without changing execution behavior, when output is being
redirected or consumed by automation:

```toml
[tool.reflow.cli.progress]
enabled = false
```

---

# Common Workflows

## Initialize Project

```bash id="c3r7wa"
reflow init
```

---

## Convert Versions

```bash id="s1j4nr"
reflow tags convert local
```

---

## Recover Releases

```bash id="f8v6yk"
reflow releases recover
```

---

## Publish Containers

```bash id="w9g5jt"
reflow dockerize
```

---

## Complete Workflow

```text id="q4n2zb"
Initialize
      ↓
Configure
      ↓
Convert
      ↓
Replay
      ↓
Dockerize
```

Commands:

```bash id="n5w3pa"
reflow init

reflow tags convert local

reflow releases recover

reflow dockerize
```

---

# Requirements

| Command   | Requirements    |
| --------- | --------------- |
| init      | Reflow          |
| convert   | Git             |
| replay    | Git, GitHub CLI |
| dockerize | Git, Docker     |

---

# Configuration

Configuration file:

```text id="r7m5dk"
config.toml
```

Select an existing checkout independently from the Reflow source checkout:

```toml
[tool.reflow.repository]
path = "../testing_reflow"

[tool.reflow.git]
default_remote = "origin"
```

If you do not have a local checkout, select a remote repository instead:

```toml
[tool.reflow.repository]
url = "https://github.com/devalltect00/testing_reflow.git"
```

Choose exactly one of `path` or `url`. Reflow creates a temporary clone for a
URL target and deletes it after the command. The clone preserves `origin`, so
explicit remote operations use the selected repository.

CLI target options override configuration:

```bash
reflow --repository ../testing_reflow --dry-run releases recover
reflow --repo ../testing_reflow tags convert remote
reflow -C ../testing_reflow dockerize

reflow --repository-url https://github.com/devalltect00/testing_reflow.git --dry-run tags convert remote
reflow --repository-url git@github.com:devalltect00/testing_reflow.git dockerize
```

The target priority is an explicit CLI target, a configured repository target,
then the current directory. `tags convert local` atomically replaces only
checkout-local tag refs and rejects URL targets. `tags convert remote`
atomically replaces remote tag refs and accepts a URL or a local checkout with
a remote. URL mode is not available for `reflow init`; clone first or select a
local directory.

Example:

```toml id="g2p8ca"
[tool.reflow.docker]

provider = "github"
```

Documentation:

```text id="k8v4ew"
docs/configuration.md
```

---

# Help Commands

Root help:

```bash id="j4p9un"
reflow --help
```

Init help:

```bash id="p3w7ft"
reflow init --help
```

Tags help:

```bash id="e2m8yc"
reflow tags --help
```

Convert help:

```bash id="s6t4qx"
reflow tags convert local --help
reflow tags convert remote --help
reflow tags convert local --help
reflow tags convert remote --help
```

Replay help:

```bash id="u9r1ak"
reflow releases recover --help
```

Dockerize help:

```bash id="v4k2nz"
reflow dockerize --help
```

---

# Related Documentation

Quick Start:

```text id="h8z4jm"
docs/user-guide/quickstart.md
```

How To Use:

```text id="m3v6pe"
docs/how-to-use.md
```

Commands:

```text id="n7w2xa"
docs/user-guide/commands.md
```

Lifecycle:

```text id="b5r9co"
docs/user-guide/lifecycle.md
```

---

# Summary

The most common commands are:

```bash id="z6y4lu"
reflow init

reflow tags convert local

reflow releases recover

reflow dockerize
```

Use only the commands required by your workflow.

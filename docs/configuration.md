# Release Lifecycle

## Overview

This document explains the complete release lifecycle supported by Reflow.

While each command can be used independently, Reflow is designed around a common workflow:

```text id="n7vj8r"
Git Tags
     ↓
Release Automation
     ↓
Version Standardization
     ↓
Container Publishing
```

Understanding this lifecycle helps determine when each command should be used.

---

# Big Picture

```text id="n7c5h4"
Developer
    │
    ▼
Create Release Tag
    │
    ▼
Replay (Optional)
    │
    ▼
Convert (Optional)
    │
    ▼
Dockerize
    │
    ▼
Container Registry
    │
    ▼
Deployment
```

Not every repository requires every step.

---

# Stage 1 — Create Tags

Every workflow begins with Git tags.

Example:

```text id="vbk06j"
v1.0.0
v1.1.0
v2.0.0
```

or:

```text id="h4y6zq"
v2.0.0rc1
v2.0.0b1
v2.0.0a1
```

Tags represent release versions.

Reflow treats tags as the source of truth.

---

# Stage 2 — Recover Releases (Optional)

Command:

```bash id="e1r4z6"
reflow releases recover
```

Purpose:

```text id="9b6du6"
Recover release automation.
```

Typical scenarios:

```text id="svy0ii"
Missing GitHub releases
Failed release workflows
Repository migration
CI/CD migration
```

Workflow:

```text id="jzuvrx"
Tag Exists
      ↓
Release Missing
      ↓
Replay Tag
      ↓
Release Recreated
```

---

# Stage 3 — Convert Tags (Optional)

Command:

```bash id="j3ymwm"
reflow tags convert local
```

Purpose:

```text id="3uxuzh"
Convert PEP 440 tags into SemVer tags.
```

Example:

Before:

```text id="q1h8w7"
v1.0.0rc1
v1.0.0b1
v1.0.0a1
```

After:

```text id="m0jj4m"
v1.0.0-rc.1
v1.0.0-beta.1
v1.0.0-alpha.1
```

This step is optional.

Repositories already using SemVer may skip conversion entirely.

---

# Stage 4 — Build Container Images

Command:

```bash id="p63j80"
reflow dockerize
```

Purpose:

```text id="36bvy8"
Turn release tags into Docker images.
```

Example:

Tag:

```text id="5w8v3s"
v2.0.0
```

Produces:

```text id="g1znq9"
ghcr.io/acme/my-app:v2.0.0
```

---

# Stage 5 — Publish Container Images

Dockerize pushes images into:

```text id="a0wb0l"
GitHub Container Registry
GitLab Container Registry
```

Example:

```text id="2c1l92"
ghcr.io/acme/my-app:v2.0.0
```

The image becomes available for deployment.

---

# Stage 6 — Deploy

Deployment occurs outside Reflow.

Examples:

```text id="jlwm2s"
Docker Compose
Kubernetes
Nomad
Azure
AWS
Google Cloud
```

Reflow stops after publishing images.

---

# Common Workflows

## Release Recovery Workflow

Problem:

```text id="8k4ej0"
Tags exist.
Releases missing.
```

Workflow:

```bash id="0z4iqz"
reflow releases recover
```

Result:

```text id="t5a3uz"
Release automation re-triggered.
```

---

## Version Migration Workflow

Problem:

```text id="qltmbz"
PEP 440 tags.
```

Need:

```text id="7hch2h"
Semantic Versioning.
```

Workflow:

```bash id="9rj4b4"
reflow tags convert local
```

Result:

```text id="p4n75l"
SemVer tags created.
```

---

## Container Publishing Workflow

Problem:

```text id="p2eh1j"
Tags exist.
Images missing.
```

Workflow:

```bash id="mjlwm8"
reflow dockerize
```

Result:

```text id="hmh34j"
Images published.
```

---

## Full Migration Workflow

Typical workflow:

```bash id="iqaz2s"
reflow tags convert local
```

```bash id="q8j7ey"
reflow releases recover
```

```bash id="cb3t1o"
reflow dockerize
```

Workflow:

```text id="e7z72l"
PEP 440
      ↓
SemVer
      ↓
Release Recovery
      ↓
Docker Images
```

---

# When To Use Each Command

## Replay

Use when:

```text id="njh8v2"
Release automation failed.
```

---

## Convert

Use when:

```text id="h6cr35"
Tag format migration is needed.
```

---

## Dockerize

Use when:

```text id="mjqh1k"
Deployable container images are needed.
```

---

# When NOT To Use Each Command

## Replay

Do not use when:

```text id="sxqrv5"
You need new versions.
```

Replay does not create versions.

---

## Convert

Do not use when:

```text id="e1u0l8"
Tags already follow SemVer.
```

---

## Dockerize

Do not use when:

```text id="9a0j2n"
No Dockerfile exists.
```

or:

```text id="o56l6j"
Container images are not required.
```

---

# Current Supported Lifecycle

Current support:

```text id="dlzvxt"
Git Tags
    ↓
Replay
    ↓
Convert
    ↓
Dockerize
    ↓
GHCR / GitLab Registry
```

---

# Future Lifecycle Possibilities

Potential future enhancements:

```text id="s5r5j0"
Docker Hub
AWS ECR
Azure ACR
Google Artifact Registry

Single Tag Processing
Tag Range Processing

Release Report Generation
```

---

# Repository Targeting

Image configuration and repository targeting are separate concerns. For
example, `[tool.reflow.github].image` controls the published image name; it
does not tell Git commands which repository to read or modify.

Configure an existing checkout explicitly:

```toml
[tool.reflow.repository]
path = "../testing_reflow"

[tool.reflow.git]
default_remote = "origin"
```

Or, when no local checkout exists, configure a remote Git URL instead:

```toml
[tool.reflow.repository]
url = "https://github.com/devalltect00/testing_reflow.git"

[tool.reflow.git]
default_remote = "origin"
```

`path` and `url` are mutually exclusive. Never place a password, personal
access token, or other credential in the URL. Use the Git credential helper,
SSH agent, GitHub CLI authentication, Docker login, or equivalent provider
credential mechanism.

Keep exactly one target active. For a local checkout, comment out `url`:

```toml
[tool.reflow.repository]
path = "../testing_reflow"
# url = "https://github.com/acme/project.git"
```

For URL mode, comment out `path`:

```toml
[tool.reflow.repository]
# path = "../testing_reflow"
url = "https://github.com/acme/project.git"
```

If both are active, Reflow exits with code 2 and prints these corrective
examples without an internal Python traceback.

Every workflow receives this resolved path. A global CLI option has higher
priority:

```bash
reflow -C ../testing_reflow tags convert local
reflow --repository ../testing_reflow --dry-run releases recover
reflow --repo ../testing_reflow dockerize
```

URL targets use the separate global option:

```bash
reflow --repository-url https://github.com/devalltect00/testing_reflow.git --dry-run tags convert remote
reflow --repository-url git@github.com:devalltect00/testing_reflow.git tags convert remote --yes
reflow --repository-url https://gitlab.com/acme/project.git dockerize
```

Reflow clones a URL target with all branches and tags into a managed temporary
directory, operates on that checkout, and removes it after success or failure.
The clone also occurs during dry-run so Reflow can discover real tags, but
dry-run still suppresses remote tag changes and registry publishing.

To make preview mode the default for every command:

```toml
[tool.reflow.cli.execution]
dry_run = true
```

Dry-run suppresses persistent local and remote mutations, but read-only
discovery still runs. For URL targets this includes the managed temporary clone.
Use the global `--no-dry-run` option only when you intentionally want to override
the configured value and perform a live workflow.

## Progress Display Configuration

Progress indicators are enabled by default for every operational command:

```toml
[tool.reflow.cli.progress]
enabled = true
```

This setting controls remote-clone spinners, tag-conversion stages,
release-recovery tag progress, Docker publishing progress, and initialization
spinners. It is used by `reflow init`, `reflow tags convert local|remote`,
`reflow releases recover`, the deprecated `reflow tags replay` alias, and
`reflow dockerize`.

Set `enabled = false` when progress animation is undesirable in redirected
output or CI logs. Disabling the display does not skip any work and does not
change dry-run or live mutation behavior.

An explicit CLI target overrides the configured target. If neither CLI nor
configuration selects a target, Reflow uses the current directory. The
`reflow init` command requires a local path because files created in a
temporary checkout would otherwise be discarded.

Tag-conversion scope is explicit. Use `local` only for the persistent checkout,
or `remote` for one guarded atomic replacement on its Git remote:

```bash
reflow -C ../testing_reflow tags convert local
reflow -C ../testing_reflow tags convert remote
```

## Tag Conversion Configuration

Configure the default direction and confirmation behavior under the dedicated
command section:

```toml
[tool.reflow.cli.tags.convert]
target_format = "semver" # "semver" or "pep440"
yes = false              # skip the live prompt for local or remote conversion
```

CLI values override these settings:

```bash
reflow --dry-run tags convert local --to pep440
reflow tags convert remote --to pep440 --yes
```

`yes = true` only skips confirmation. Scope remains an explicit command name;
configuration cannot silently turn a local operation into a remote one. Keep
it `false` for normal interactive use. Dry-run ignores confirmation because no
persistent tag mutation occurs.

---

# Summary

Reflow treats Git tags as the central release artifact.

Everything else flows from those tags:

```text id="jzlp9v"
Git Tags
    ↓
Release Recovery
    ↓
Version Standardization
    ↓
Container Publishing
```

This philosophy keeps release automation predictable, repeatable, and easy to understand.

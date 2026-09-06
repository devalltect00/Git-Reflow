# Reflow Commands Guide

## Overview

Reflow provides tools for managing repository release tags and publishing Docker images.

The available commands are:

```bash
reflow init
reflow releases recover
reflow tags convert local
reflow dockerize
```

Each command solves a different problem.

This guide helps you determine which command you need and how they work together.

Operational commands accept a local checkout with `--repository` / `-C` or a
remote Git repository with `--repository-url`. A URL target is cloned into a
managed temporary checkout for the duration of the command. `reflow init` is
local-only.

---

# Command Overview

| Command               | Purpose                                         |
| --------------------- | ----------------------------------------------- |
| `reflow init`         | Initialize a project for use with Reflow        |
| `reflow releases recover`  | Re-trigger release automation for existing tags |
| `reflow tags convert local` | Safely convert tags between PEP 440 and SemVer |
| `reflow dockerize`    | Build and publish Docker images from tags       |

---

## Initialize Project

Command:

```bash
reflow init
```

Purpose:

```text
Bootstrap a project for use with Reflow.
```

Creates:

```text
config.toml
__version__.py
templates
examples
```

Documentation:

```text
docs/init/
```

Recommended for:

```text
New users
New repositories
First-time setup
```

---

# New To Reflow?

Start with:

```bash
reflow init
```

Workflow:

```text
Install Reflow
      ↓
reflow init
      ↓
Edit config.toml
      ↓
Run the commands you need
```

Documentation:

```text
docs/init/
docs/user-guide/getting-started.md
```

---

# Which Command Should I Use?

## My Releases Are Missing

Example:

```text
Tags exist.
GitHub releases do not.
```

Use:

```bash
reflow releases recover
```

Documentation:

```text
docs/commands/releases/recover/
```

---

## My Tags Use PEP 440

Example:

```text
v1.0.0rc1
v1.0.0b1
v1.0.0a1
```

Need:

```text
v1.0.0-rc.1
v1.0.0-beta.1
v1.0.0-alpha.1
```

Use:

```bash
reflow tags convert local
```

Documentation:

```text
docs/tags/convert/
```

---

## I Need Docker Images

Example:

```text
Repository tags exist.
No container images exist.
```

Use:

```bash
reflow dockerize
```

Documentation:

```text
docs/dockerize/
```

---

# Command Relationship

The commands are independent.

You may run only the command you need.

Example:

```text
Only missing releases
        ↓
Replay
```

---

```text
Only tag migration
        ↓
Convert
```

---

```text
Only Docker publishing
        ↓
Dockerize
```

---

# Recommended Workflow

For repositories migrating from PEP 440 to SemVer and publishing Docker images:

```text
Initialize Project
       ↓
Configure Project
       ↓
Convert Tags (optional)
       ↓
Recover Releases (optional)
       ↓
Dockerize Images (optional)
```

Commands:

```bash
reflow tags convert local
```

```bash
reflow releases recover
```

```bash
reflow dockerize
```

---

# Workflow Examples

## Existing Releases Missing

Problem:

```text
Tags exist.
Releases missing.
```

Solution:

```bash
reflow releases recover
```

---

## PEP 440 Migration

Problem:

```text
v1.0.0rc1
v1.0.0b1
```

Need:

```text
v1.0.0-rc.1
v1.0.0-beta.1
```

Solution:

```bash
reflow tags convert local
```

---

## Docker Registry Publishing

Problem:

```text
Tags exist.
Images missing.
```

Solution:

```bash
reflow dockerize
```

---

# Command Comparison

## Replay

Purpose:

```text
Recover release automation.
```

Input:

```text
Git tags.
```

Output:

```text
Re-triggered release workflows.
```

Changes tags:

```text
No.
```

Creates Docker images:

```text
No.
```

---

## Convert

Purpose:

```text
Convert version formats.
```

Input:

```text
PEP 440 tags.
```

Output:

```text
Semantic Version tags.
```

Changes tags:

```text
Yes.
```

Creates Docker images:

```text
No.
```

---

## Dockerize

Purpose:

```text
Publish Docker images.
```

Input:

```text
Git tags.
```

Output:

```text
Container images.
```

Changes tags:

```text
No.
```

Creates Docker images:

```text
Yes.
```

---

# Requirements Summary

## Init

Requirements:

```text
✓ Reflow installed
✓ Write access to project directory
```

Optional:

```text
Git
Docker
GitHub CLI
```

are not required for initialization.

## Replay

Requirements:

```text
✓ Git
✓ GitHub CLI
✓ GitHub authentication
```

---

## Convert

Requirements:

```text
✓ Git
```

---

## Dockerize

Requirements:

```text
✓ Git
✓ Docker
✓ Dockerfile
✓ Registry authentication
```

---

# Documentation Structure

## Init

```text
docs/init/

overview.md
workflow.md
examples.md
faq.md
```

## Replay

```text
docs/commands/releases/recover/

overview.md
workflow.md
requirements.md
examples.md
faq.md
```

---

## Convert

```text
docs/tags/convert/

overview.md
workflow.md
requirements.md
examples.md
faq.md
```

---

## Dockerize

```text
docs/dockerize/

overview.md
workflow.md
requirements.md
examples.md
faq.md
```

---

# Quick Start

Initialize project:

```bash
reflow init
```

Convert tags:

```bash
reflow tags convert local
```

Replay releases:

```bash
reflow releases recover
```

Build images:

```bash
reflow dockerize
```

---

# Next Reading

Choose the command that matches your goal:

- Replay → `docs/commands/releases/recover/`
- Convert → `docs/tags/convert/`
- Dockerize → `docs/dockerize/`

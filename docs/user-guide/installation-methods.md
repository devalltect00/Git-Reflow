# Installation Methods

## Overview

Reflow supports multiple installation methods.

This guide helps you choose the most appropriate installation method for your use case.

If you only want installation instructions, see:

```text
docs/installation.md
```

---

# Available Installation Methods

Reflow currently supports:

| Method                   | Recommended | Typical Use Case        |
| ------------------------ | ----------- | ----------------------- |
| GitHub Clone             | ✅          | Most users              |
| GitLab Clone             | ✅          | GitLab users            |
| Private GitLab PyPI      | ✅          | Authorized deployments  |
| Wheel (.whl)             | ✅          | Stable releases         |
| Source Archive (.tar.gz) | ✅          | Offline installation    |
| Editable Installation    | ✅          | Contributors            |
| Public PyPI              | ❌          | Not currently available |

---

# Method 1 — GitHub Repository

Clone:

```bash
git clone https://github.com/your-org/reflow.git
```

Install:

```bash
pip install -e .
```

Advantages:

```text
Latest version
Easy updates
Simple workflow
```

Disadvantages:

```text
Requires Git
Requires internet connection
```

Recommended for:

```text
Most users
Open-source users
Developers
```

---

# Method 2 — GitLab Repository

Clone:

```bash
git clone https://gitlab.com/your-org/reflow.git
```

Install:

```bash
pip install -e .
```

Advantages:

```text
Latest version
GitLab-native workflow
Simple updates
```

Disadvantages:

```text
Requires Git
Requires internet connection
```

Recommended for:

```text
GitLab users
GitLab-hosted projects
```

---

# Method 3 — Private GitLab PyPI Registry

Reflow releases are published as the `git-reflow` distribution in the
project's private GitLab package registry. Use a deploy token with
`read_package_registry` access and keep credentials out of committed files:

```bash
python -m pip install \
  --index-url "https://<deploy-token-user>:<deploy-token>@gitlab.com/api/v4/projects/<project-id>/packages/pypi/simple" \
  "git-reflow==1.0.2"
```

Install a release candidate explicitly with its PEP 440 version:

```bash
python -m pip install \
  --index-url "https://<deploy-token-user>:<deploy-token>@gitlab.com/api/v4/projects/<project-id>/packages/pypi/simple" \
  "git-reflow==1.0.0rc1"
```

The corresponding repository tag may be `v1.0.0-rc.1`; the package registry
stores its normalized version as `1.0.0rc1`.

For strictly private resolution, disable package forwarding in the GitLab group
settings. Avoid `--extra-index-url` for private packages because consulting
multiple indexes can expose a dependency-confusion path.

---

# Method 4 — Wheel File (.whl)

Example:

```text
git_reflow-1.0.2-py3-none-any.whl
```

Install:

```bash
pip install git_reflow-1.0.2-py3-none-any.whl
```

Advantages:

```text
Fast installation
Stable release
No repository required
```

Disadvantages:

```text
Must download new wheel for updates
```

Recommended for:

```text
Production systems
Stable environments
CI/CD runners
```

---

# Method 5 — Source Archive (.tar.gz)

Example:

```text
git_reflow-1.0.2.tar.gz
```

Install:

```bash
pip install git_reflow-1.0.2.tar.gz
```

Advantages:

```text
Simple distribution
Works offline after download
```

Disadvantages:

```text
Slower installation
Less convenient updates
```

Recommended for:

```text
Offline environments
Archived releases
Long-term storage
```

---

# Method 6 — Editable Installation

Clone:

```bash
git clone <repository-url>
```

Install:

```bash
pip install -e .
```

Advantages:

```text
Instant code changes
Contributor friendly
Ideal for development
```

Disadvantages:

```text
Not intended for production
```

Recommended for:

```text
Contributors
Maintainers
Feature development
Testing
```

---

# GitHub vs GitLab

## GitHub

Advantages:

```text
Largest community
GitHub Releases
GitHub Container Registry
```

Typical workflow:

```text
GitHub
    ↓
GitHub Releases
    ↓
GitHub Container Registry
```

---

## GitLab

Advantages:

```text
Integrated DevOps platform
GitLab Container Registry
GitLab CI/CD
```

Typical workflow:

```text
GitLab
    ↓
GitLab Releases
    ↓
GitLab Container Registry
```

---

# Wheel vs Source Archive

## Wheel

```text
.whl
```

Advantages:

```text
Fast install
Prebuilt package
Preferred option
```

Recommended when available.

---

## Source Archive

```text
.tar.gz
```

Advantages:

```text
Universal format
Source distribution
```

Useful when wheel files are unavailable.

---

# Development vs Production

## Development

Recommended:

```bash
git clone <repository-url>

pip install -e .
```

Benefits:

```text
Editable installation
Easy debugging
Immediate updates
```

---

## Production

Recommended:

```bash
pip install git_reflow-1.0.2-py3-none-any.whl
```

Benefits:

```text
Stable version
Predictable deployment
Reproducible environment
```

---

# Release Assets

Release pages may contain:

```text
.whl
.tar.gz
```

These files are typically generated using:

```bash
python -m build
```

and published through:

```text
GitHub Releases
GitLab Releases
```

---

# Which Method Should I Choose?

## New User

Recommended:

```text
GitHub Clone
```

---

## GitLab User

Recommended:

```text
GitLab Clone
```

---

## Contributor

Recommended:

```text
Editable Installation
```

---

## CI/CD Environment

Recommended:

```text
Wheel File
```

---

## Offline Environment

Recommended:

```text
Source Archive
```

---

# Recommendation Summary

| Scenario    | Recommended Method    |
| ----------- | --------------------- |
| New User    | GitHub Clone          |
| GitLab User | GitLab Clone          |
| Contributor | Editable Installation |
| Production  | Private GitLab PyPI or wheel |
| CI/CD       | Private GitLab PyPI or wheel |
| Offline     | Source Archive        |

---

# Related Documentation

Installation:

```text
docs/installation.md
```

Quick Start:

```text
docs/user-guide/quickstart.md
```

Getting Started:

```text
docs/user-guide/getting-started.md
```

Commands:

```text
docs/user-guide/commands.md
```

---

# Summary

For most users:

```bash
git clone <repository-url>

pip install -e .
```

is the recommended installation method.

For production and CI/CD environments:

```text
Wheel (.whl)
```

is usually the preferred choice.

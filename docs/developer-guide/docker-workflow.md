# Docker Development Workflow

## Overview

This guide explains how Docker is used during Reflow development.

It focuses on:

- Developing Docker-related features
- Testing Docker integrations
- Testing registry publishing workflows
- Troubleshooting Docker issues

This document is intended for contributors and maintainers.

---

# Purpose

Reflow includes:

```bash id="z4t7vn"
reflow dockerize
```

which automates:

```text id="q6m2pk"
Docker image builds
Image tagging
Registry publishing
```

Contributors should understand the Docker workflow before modifying Docker-related code.

---

# Docker Architecture

High-level flow:

```text id="v3q8tk"
Git Tag
      ↓
DockerService
      ↓
Docker Executor
      ↓
Docker CLI
      ↓
Container Registry
```

The Docker CLI remains the source of truth.

Reflow acts as an orchestration layer.

---

# Development Requirements

Required:

```text id="u9r4vp"
Python
Git
Docker
```

Verify:

```bash id="n2m8tk"
docker --version
```

Example output:

```text id="d5v3rp"
Docker version 28.x
```

---

# Verify Docker Access

Check daemon availability:

```bash id="k7q4tn"
docker info
```

If this command fails:

```text id="w4m8pk"
Docker daemon may not be running.
```

Start Docker Desktop or Docker Engine before continuing.

---

# Local Development Workflow

Typical workflow:

```text id="r8v2tm"
Create Feature
       ↓
Run Tests
       ↓
Build Image
       ↓
Validate Result
       ↓
Open Pull Request
```

---

# Build A Test Image

Example:

```bash id="j4m7vk"
docker build -t reflow-test .
```

Reflow derives distribution metadata from Git through `setuptools-scm`, while
`.git` is intentionally excluded from the Docker build context. For a local
image that must carry the exact package version, resolve the version before the
build and pass it explicitly:

```bash
python -m pip install "packaging>=24"
REFLOW_BUILD_VERSION="$(python -m app.core.build.version)"
docker build \
  --build-arg "REFLOW_BUILD_VERSION=${REFLOW_BUILD_VERSION}" \
  --target production \
  -t reflow-test .
```

The GitHub and GitLab development and production workflows perform this version
resolution automatically. When the build argument is omitted, the existing
`setuptools-scm` fallback remains in effect. See [`docs/ci-cd.md`](../ci-cd.md)
for the annotated-tag, registry-name, prerelease, and stable alias contracts.

Stable releases publish four coordinated references to the same image:

| Tag | Example | Intended use |
| --- | --- | --- |
| Exact | `v1.0.1` | Immutable, reproducible automation pin |
| Minor | `v1.0` | Newest stable patch in the 1.0 line |
| Major | `v1` | Newest stable release in the 1.x line |
| Latest | `latest` | Newest stable Reflow release |

Prereleases such as `v1.0.0-rc.1` publish only their exact tag and never move
the stable aliases. GitHub and GitLab apply the same alias policy; the release
package gate continues to reject build-metadata tags rather than guessing.

The source checkout's `.config/reflow/config.toml` is intentionally excluded
from built images because it may contain host-specific repository paths or
registry destinations. Mount the target workspace when running operational
commands; informational commands such as `reflow --help` do not require a
configured repository target.

Verify:

```bash id="t9q3rp"
docker images
```

Expected:

```text id="g6v8tn"
reflow-test
```

appears in the image list.

The development Compose configuration builds `reflow-dev:latest` through the
`app` service. Test, lint, format, shell, QA, and package-build services reuse
that image instead of defining independent builds. The corresponding Make
targets prepare the app image before invoking those helper services.

Build all local Compose images with a current GNU Make 4.x release:

```bash
make c-build-all
```

Old MinGW GNU Make 3.82 builds may terminate on current Windows systems with an
internal `readdir` error before reading Reflow's Makefile. Upgrade GNU Make, or
run the equivalent Compose commands directly:

```bash
docker compose -f docker-compose.yml build base
docker compose -f docker-compose.yml -f docker-compose.dev.yml build app
docker compose -f docker-compose.yml -f docker-compose.prod.yml build app
```

---

# Test Dockerize Workflow

Typical workflow:

```text id="m5r2pk"
Git Tag
      ↓
Dockerize
      ↓
Build Image
      ↓
Tag Image
```

Run:

```bash id="y8q4tm"
reflow --dry-run dockerize
```

before performing a real build.

---

# Recommended Development Mode

Use:

```bash id="v2m8tn"
reflow --dry-run dockerize
```

whenever possible.

Benefits:

```text id="r4q7pk"
Safer testing
Faster iteration
No registry pushes
```

---

# Registry Providers

Currently supported:

```text id="d8v3tm"
GitHub Container Registry
GitLab Container Registry
```

Configuration:

```toml id="g3m9rp"
[tool.reflow.docker]

provider = "github"
```

or:

```toml id="z7q4tn"
[tool.reflow.docker]

provider = "gitlab"
```

---

# Testing GitHub Container Registry

Example:

```toml id="s2v8pk"
[tool.reflow.github]

image = "ghcr.io/your-org/your-image"
```

Login:

```bash id="w5m3tn"
docker login ghcr.io
```

Verify:

```bash id="c8q4rp"
docker pull ghcr.io/your-org/your-image
```

if applicable.

---

# Testing GitLab Container Registry

Example:

```toml id="j4v7pk"
[tool.reflow.gitlab]

image = "registry.gitlab.com/your-org/your-image"
```

Login:

```bash id="r9m2tn"
docker login registry.gitlab.com
```

Verify:

```bash id="u3q8rp"
docker pull registry.gitlab.com/your-org/your-image
```

if applicable.

---

# Testing Strategy

Preferred testing order:

```text id="x5v4tm"
Unit Tests
      ↓
Dry Run
      ↓
Local Build
      ↓
Registry Testing
```

Avoid pushing images during routine development unless necessary.

---

# Unit Tests

Run Docker-related tests:

```bash id="m8q2pk"
pytest tests/core/docker/
```

Run coverage:

```bash id="z4v7tn"
pytest --cov=app
```

Expected:

```text id="g2m9rp"
All tests pass
Coverage remains stable
```

---

# Manual Verification

Before submitting Docker-related changes:

Verify:

```text id="d6q4tn"
Image naming
Image tagging
Provider selection
Registry URL generation
```

---

# Troubleshooting

## Docker Not Found

Example:

```text id="r3v8pk"
docker: command not found
```

Solution:

```text id="m7q2tn"
Install Docker
Restart terminal
Verify PATH
```

---

## Docker Daemon Not Running

Example:

```text id="v4m8rp"
Cannot connect to the Docker daemon
```

Solution:

```text id="z9q3tn"
Start Docker Desktop
Start Docker Engine
```

---

## Registry Authentication Failed

Example:

```text id="k2v7pk"
unauthorized
authentication required
```

Solution:

GitHub:

```bash id="w8m4tn"
docker login ghcr.io
```

GitLab:

```bash id="f3q9rp"
docker login registry.gitlab.com
```

---

## Image Push Failed

Verify:

```text id="y6v2tm"
Registry URL
Image Name
Authentication
Network Access
```

---

# Development Guidelines

When modifying Docker features:

Prefer:

```text id="u4m8pk"
DockerService
Resolvers
Models
Tests
```

Avoid:

```text id="x7q3tn"
Embedding Docker logic directly inside CLI commands
```

The CLI should remain thin.

---

# Future Possibilities

Potential future enhancements:

```text id="j9v4rp"
Multi-architecture builds
Buildx support
Additional registries
Image signing
SBOM generation
```

See:

```text id="n5q8tm"
docs/project/roadmap.md
TODO.md
```

for tracking.

---

# Related Documentation

Docker User Guide:

```text id="m3v7pk"
docs/dockerize/
```

Infrastructure:

```text id="p8q2tn"
docs/infrastructure.md
```

Architecture:

```text id="d4v9rp"
docs/architecture/
```

Testing:

```text id="g7q3tm"
docs/testing/testing-guide.md
```

---

# Summary

The recommended Docker development workflow is:

```text id="z2v8pk"
Develop
    ↓
Test
    ↓
Dry Run
    ↓
Local Build
    ↓
Registry Validation
```

This approach minimizes risk while ensuring Docker-related features remain reliable and maintainable.

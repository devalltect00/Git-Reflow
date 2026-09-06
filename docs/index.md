# Reflow Documentation

Welcome to the official documentation for **Reflow**.

Reflow is a command-line tool for:

- Project initialization
- Git tag conversion
- Release replay and recovery
- Docker image publishing

This documentation is organized for multiple audiences:

- **Users** — install, configure, and use Reflow
- **Developers** — understand architecture and implementation details
- **Maintainers** — review workflows, layers, and project direction
- **Contributors** — understand project structure and future plans

---

# Documentation Entry Points

## User Documentation

Start here if you are new to Reflow.

- [Getting Started](user-guide/getting-started.md)
- [Commands](user-guide/commands.md)
- [Command Examples](examples.md)
- [Lifecycle](user-guide/lifecycle.md)

Recommended reading order:

```text
Getting Started
      ↓
Commands
      ↓
Lifecycle
```

---

## Initialization Documentation

Everything related to:

```bash
reflow init
```

- [Overview](commands/init/overview.md)
- [Workflow](commands/init/workflow.md)
- [Examples](commands/init/examples.md)
- [FAQ](commands/init/faq.md)

Recommended for:

```text
First-time setup
New repositories
Team onboarding
```

---

## Tag Documentation

Everything related to:

```bash
reflow tags
```

### Convert

```bash
reflow tags convert local
```

- Overview
- Workflow
- Examples
- FAQ

### Replay

```bash
reflow releases recover
```

- Overview
- Workflow
- Examples
- FAQ

Recommended for:

```text
Version migration
Release recovery
GitHub release management
```

---

## Docker Documentation

Everything related to:

```bash
reflow dockerize
```

- Overview
- Workflow
- Examples
- FAQ

Recommended for:

```text
Container publishing
GHCR workflows
GitLab Registry workflows
```

---

## Architecture Documentation

Architecture and implementation details.

- Architecture Workflow
- Design Patterns
- Architecture Diagrams

Recommended for:

```text
Developers
Contributors
Maintainers
```

---

## Diagram Documentation

Visual documentation for Reflow.

- Reflow Overview
- Init Workflow
- Convert Workflow
- Release Recovery Workflow
- Dockerize Workflow
- Release Lifecycle
- Architecture Layers

Documentation:

```text
docs/diagrams/
```

---

## Reference Documentation

Project reference material.

- Configuration
- Badges

Files:

```text
docs/configuration.md
docs/badges.md
```

---

## Project Documentation

Project planning and future direction.

- Roadmap
- TODO

Files:

```text
docs/project/roadmap.md
TODO.md
```

---

# Recommended Reading Paths

## New Users

```text
Getting Started
       ↓
Initialization
       ↓
Commands
       ↓
Lifecycle
```

---

## Release Maintainers

```text
Convert
      ↓
Replay
      ↓
Dockerize
```

---

## Contributors

```text
Architecture
      ↓
Diagrams
      ↓
Roadmap
```

---

# Reflow Workflow Summary

```text
Install Reflow
       ↓
Initialize Project
       ↓
Configure Project
       ↓
Convert Tags (Optional)
       ↓
Recover Releases (Optional)
       ↓
Dockerize Images (Optional)
```

Run only the commands required for your workflow.

---

# Quick Links

Project Initialization:

```bash
reflow init
```

Convert Tags:

```bash
reflow tags convert local
```

Recover Releases:

```bash
reflow releases recover
```

Docker Publishing:

```bash
reflow dockerize
```

---

# Documentation Philosophy

Reflow documentation follows a layered approach:

```text
Overview
      ↓
Workflow
      ↓
Examples
      ↓
FAQ
```

This structure helps users learn concepts before diving into implementation details.

---

# Project Scope

Reflow focuses on:

```text
Project Initialization
Version Management
Release Recovery
Container Publishing
```

Reflow does not currently focus on:

```text
Kubernetes Deployment
Infrastructure Provisioning
CI/CD Pipeline Generation
Dockerfile Generation
```

See:

```text
docs/project/roadmap.md
TODO.md
```

for future plans and project direction.

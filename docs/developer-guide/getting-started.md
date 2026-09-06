# Developer Getting Started

## Overview

This guide helps developers set up a local Reflow development environment.

By the end of this guide, you will be able to:

- Clone the repository
- Install Reflow locally
- Run tests
- Run linting and formatting tools
- Understand the project structure

---

# Who Is This Guide For?

This guide is intended for:

```text id="4r2x6j"
Contributors
Maintainers
Developers
Students
Open Source Participants
```

If you only want to use Reflow, see:

```text id="v9q4nk"
docs/user-guide/
```

instead.

---

# Requirements

Minimum:

```text id="w6t3fp"
Python 3.14+
Git
```

Recommended:

```text id="x2p8vd"
Docker
GitHub CLI
```

depending on which features you are developing.

---

# Clone Repository

GitHub:

```bash id="h7p4sk"
git clone https://github.com/your-org/reflow.git
```

GitLab:

```bash id="y1m7tr"
git clone https://gitlab.com/your-org/reflow.git
```

Enter project:

```bash id="j9k3qx"
cd reflow
```

---

# Create Virtual Environment

Using the project Make workflow:

```bash
make venv
```

Then display the platform-specific activation command:

```bash
make activate
```

Manual activation uses the default `venv` directory.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

# Install Dependencies

Install Reflow and all developer/documentation dependencies:

```bash
make install-all
```

For a complete first-time setup, including pre-commit hooks:

```bash
make setup
```

---

# Verify Installation

Display help:

```bash id="r3v8tn"
reflow --help
```

Display version:

```bash id="m7q1kb"
reflow --version
```

---

# Run Tests

Run all tests:

```bash
make test
```

Run coverage:

```bash
make test-cov
```

Run specific test folder:

```bash id="u4t9km"
pytest tests/core/git/
```

Run specific file:

```bash id="y2r6qx"
pytest tests/core/git/test_service.py
```

---

# Run Ruff

Lint:

```bash id="n8w3fp"
ruff check .
```

Format:

```bash id="j1x5tv"
ruff format .
```

Check formatting:

```bash id="q7m2rd"
ruff format . --check
```

---

# Recommended Development Workflow

Before opening a pull request:

```bash
make check
```

All commands should pass successfully.

See [Make Workflows](make-workflows.md) for local, Docker, Compose, published
container, repository-targeting, and dry-run examples.

---

# Project Structure

High-level structure:

```text id="c5n4zp"
app/
├── cli/
├── core/
├── config/
├── ui/

tests/
docs/
```

---

# Architecture Overview

Reflow follows a layered architecture:

```text id="w7t9mf"
CLI
 ↓
Resolver
 ↓
Core
 ↓
Service
 ↓
Executor
 ↓
External Tool
```

Benefits:

```text id="p2x6vd"
Separation of concerns
Testability
Maintainability
Extensibility
```

Documentation:

```text id="m9q3rk"
docs/architecture/
```

---

# Important Directories

## CLI

```text id="t6v4hp"
app/cli/
```

Responsibilities:

```text id="k3n7dx"
Command definitions
Options
Help messages
Presentation
```

---

## Core

```text id="e8m5tr"
app/core/
```

Responsibilities:

```text id="r4q9vk"
Business logic
Services
Workflows
```

---

## Config

```text id="y7w1mp"
app/config/
```

Responsibilities:

```text id="g2x8rn"
Configuration loading
Configuration models
```

---

## UI

```text id="f5m3vd"
app/ui/
```

Responsibilities:

```text id="u1t8pk"
Rich tables
Panels
Progress bars
User-facing presentation
```

---

## Tests

```text id="n6q4sr"
tests/
```

Responsibilities:

```text id="v8p2mx"
Unit tests
Integration tests
Coverage
```

---

# First Contribution

Good first tasks:

```text id="k4x7tp"
Documentation improvements
Additional tests
CLI UX improvements
Error handling improvements
```

---

# Before Making Changes

Read:

```text id="r2m9vd"
docs/architecture/workflow.md
```

Then:

```text id="g6p4tn"
docs/architecture/design-patterns.md
```

Then:

```text id="q8v1rm"
docs/project/roadmap.md
```

Understanding the architecture first usually saves a lot of time.

---

# Related Documentation

Developer Guide:

```text id="m3q7vk"
docs/developer-guide/developer-guide.md
```

Testing:

```text id="z9t2pn"
docs/testing/testing-guide.md
```

Architecture:

```text id="c7x4rd"
docs/architecture/
```

Roadmap:

```text id="j5n8tm"
docs/project/roadmap.md
```

---

# Summary

The recommended setup process is:

```text id="d8v3pk"
Clone
   ↓
Install
   ↓
Run Tests
   ↓
Read Architecture
   ↓
Start Contributing
```

Once tests and linting pass, you are ready to contribute to Reflow.

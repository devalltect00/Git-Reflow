# Reflow

Release Recovery, Version Conversion, and Docker Release Automation.

Reflow helps automate release workflows by treating Git tags as the source of truth for releases, versioning, and container publishing.

---

## Badges

![Python](https://img.shields.io/badge/python-3.14+-blue.svg)
![Versioning](https://img.shields.io/badge/versioning-SemVer-3F4551.svg)
![Tag](https://img.shields.io/github/v/tag/devalltect00/Git-Reflow)
![License](https://img.shields.io/github/license/devalltect00/Git-Reflow)
![Build](https://img.shields.io/badge/CI-GitHub%20Actions-success)
![Coverage](https://img.shields.io/badge/coverage-tracked-success)
![Ruff](https://img.shields.io/badge/lint-ruff-purple.svg)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)
![Documentation](https://img.shields.io/badge/docs-online-success.svg)
![MkDocs](https://img.shields.io/badge/docs-MkDocs-success.svg)
![Docker](https://img.shields.io/badge/docker-supported-2496ED?logo=docker&logoColor=white)
![Docker Release](https://img.shields.io/badge/docker-release%20images-2496ED?logo=docker&logoColor=white)
![Docker Commit](https://img.shields.io/badge/docker-commit%2Fsha%20images-1D63ED?logo=docker&logoColor=white)
![Release](https://img.shields.io/github/v/release/devalltect00/Path-Header-Scanner)
![Developer Tool](https://img.shields.io/badge/category-developer--tool-orange.svg)

See: [`docs/badges.md`](docs/badges.md)

for the complete badge reference.

---

## What Is Reflow?

Reflow is a command-line tool designed to simplify release management workflows.

It provides tools for:

- Project initialization
- Version conversion
- Missing-release recovery
- Docker image publishing

Workflow:

```text
Initialize Project
       ↓
Configure Project
       ↓
Convert Tags
       ↓
Recover Releases
       ↓
Publish Containers
```

---

## ✨ Features

- 🏷️ Replaying Git tags to trigger CI/CD
- 🐳 Building Docker images per tag
- 🦊 Supporting GitHub (GHCR) and GitLab Registry
- ⚙️ Config-driven via `.config/reflow/config.toml`
- 📊 Observable clone, conversion, recovery, initialization, and publish progress

### 🚀 Project Initialization

Bootstrap a project for use with Reflow.

Command:

```bash
reflow init
```

Documentation: [`docs/commands/init/`](docs/commands/init/)

---

### 🔀 Version Conversion

Convert PEP 440 tags into Semantic Version tags.

Command:

```bash
reflow tags convert local
reflow tags convert remote
```

Documentation: [`docs/commands/tags/convert/`](docs/commands/tags/convert/)

---

### 🛟 Release Recovery

Recover release automation from existing tags.

Command:

```bash
reflow releases recover
```

Documentation: [`docs/commands/releases/recover/`](docs/commands/releases/recover/)

---

### 🐳 Docker Publishing

Build and publish Docker images from Git tags.

Command:

```bash
reflow dockerize
```

Documentation: [`docs/commands/dockerize/`](docs/commands/dockerize/)

---

## 📦 Installation

Clone the repository:

```bash
git clone <repository-url>
```

Enter the project:

```bash
cd reflow
```

For a contributor installation with development, documentation, and
pre-commit tooling:

```bash
make setup
```

The Make workflow uses `venv` by default. Display the activation command with:

```bash
make activate
```

For a manual runtime-only installation, create and activate the environment.

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install:

```bash
pip install -e .
```

See [`docs/developer-guide/make-workflows.md`](docs/developer-guide/make-workflows.md)
for local, Docker, Compose, published-image, and dry-run Make targets.

---

## 🚀 Quick Start

Initialize a project:

```bash
reflow init
```

Review:

```text
config.toml
```

Run the commands you need:

Convert tags:

```bash
reflow tags convert local
```

Recover missing releases:

```bash
reflow releases recover
```

Publish images:

```bash
reflow dockerize
```

---

## 📖 Commands

| Command                      | Description                                 |
| ---------------------------- | ------------------------------------------- |
| `reflow init`                | Initialize a project                        |
| `reflow tags convert local`  | Replace converted names in a local checkout |
| `reflow tags convert remote` | Replace converted names on the Git remote   |
| `reflow releases recover`    | Recover missing releases                    |
| `reflow dockerize`           | Build and publish Docker images             |

The former `reflow tags replay` spelling remains as a deprecated compatibility
alias.

### Target Another Repository

Operational workflows can use either an existing local checkout or a remote
GitHub/GitLab URL. For a local checkout:

```bash
reflow --repository ../testing_reflow --dry-run releases recover
reflow -C ../testing_reflow tags convert local
reflow -C ../testing_reflow tags convert remote
reflow --repo ../testing_reflow dockerize
```

Or configure the target once:

```toml
[tool.reflow.repository]
path = "../testing_reflow"
```

If no checkout exists, use a remote URL directly:

```bash
reflow --repository-url https://github.com/devalltect00/testing_reflow.git --dry-run tags convert remote
reflow --repository-url https://github.com/devalltect00/testing_reflow.git tags convert remote --yes
reflow --repository-url https://github.com/devalltect00/testing_reflow.git dockerize
```

Or configure `url` instead of `path`:

```toml
[tool.reflow.repository]
url = "https://github.com/devalltect00/testing_reflow.git"
```

Reflow clones URL targets into a temporary checkout and removes it when the
command finishes. Configure exactly one of `path` or `url`; an explicit CLI
target overrides configuration. `reflow init` and `tags convert local` require
a persistent checkout. `tags convert remote` accepts a URL and performs one
guarded atomic remote tag replacement.

Progress indicators are enabled by default. For CI logs or redirected output,
disable only the presentation layer without changing execution or dry-run
behavior:

```toml
[tool.reflow.cli.progress]
enabled = false
```

For detailed usage:

[`docs/user-guide/commands.md`](docs/user-guide/commands.md)

---

## 📖 Documentation

### 📘 User Guide [`docs/user-guide/`](docs/user-guide/)

Contains:

```text
getting-started.md
commands.md
lifecycle.md
```

---

### 📘 Initialization [`docs/commands/init/`](docs/commands/init/)

Contains:

```text
overview.md
workflow.md
examples.md
faq.md
```

---

### 📘 Architecture [`docs/architecture/`](docs/architecture/)

Contains:

```text
workflow.md
design-patterns.md
diagrams.md
```

---

### 📘 Configuration [`docs/configuration.md`](docs/configuration.md)

---

### ❓ Questions and Answers [`docs/qa/`](docs/qa/)

Answers common questions about local paths, repository URLs, remote effects,
authentication, and troubleshooting.

---

### 📘 Roadmap [`docs/project/roadmap.md`](docs/project/roadmap.md)

---

### 📘 Future Work

```text
TODO.md
```

---

## 🧱 Architecture

High-level architecture:

```text
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

Documentation:

[`docs/architecture/workflow.md`](docs/architecture/workflow.md)

---

## ♻️ Recommended Workflow

```text
Install Reflow
      ↓
reflow init
      ↓
Edit config.toml
      ↓
reflow tags convert local
      ↓
reflow releases recover
      ↓
reflow dockerize
```

Run only the commands required for your workflow.

---

## 📍 Roadmap

Current project roadmap: [`docs/project/roadmap.md`](docs/project/roadmap.md)

Future ideas and enhancements:

```text
TODO.md
```

---

## 📁 Project Structure

For the details, see full structure in [`project_structure.md`](docs/project_structure.md).

---

## 🤝 Contributing

Contributions, issues, and suggestions are welcome.

Before contributing, review: [`docs/developer-guide/`](docs/developer-guide/)

and: [`docs/architecture/`](docs/architecture/)

For the details, see [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

## 🔐 Security

See [`SECURITY.md`](SECURITY.md)

---

## 📃 Changelog

See [`CHANGELOG.md`](CHANGELOG.md)

---

## 📜 License

MIT License

Copyright © 2026
This software is **not open source**.
You may not copy, distribute, or modify without permission.

📧 Contact: `rizkypffdev37@gmail.com`

---

_Handcrafted with ❤️ by Devalltect / Rizky Fernandes_

# Installation

## Overview

This guide explains the supported methods for installing Reflow.

Reflow is currently **not published to the public PyPI index**. Authorized
users can install it from the project's private GitLab PyPI registry; source,
repository, and release-artifact installations remain available.

This means:

```bash id="w2y6g7"
pip install reflow
```

without a private index is **not currently supported**.

Instead, Reflow can be installed using:

- Source code
- GitHub repository
- GitLab repository
- Private GitLab PyPI registry
- Release artifacts (`.whl`)
- Release artifacts (`.tar.gz`)

---

# Supported Installation Methods

| Method                    | Recommended | Use Case                |
| ------------------------- | ----------- | ----------------------- |
| Source Installation       | ✅          | Development             |
| GitHub Repository         | ✅          | Most users              |
| GitLab Repository         | ✅          | GitLab users            |
| Private GitLab PyPI       | ✅          | Authorized deployments  |
| Wheel File (.whl)         | ✅          | Stable releases         |
| Source Archive (.tar.gz)  | ✅          | Offline installation    |
| Public PyPI               | ❌          | Not currently supported |

---

# Requirements

Minimum requirements:

```text id="a3y1cl"
Python 3.14+
Git
```

Recommended:

```text id="0crpqk"
Docker
GitHub CLI
```

depending on which commands you intend to use.

---

# Install From the Private GitLab PyPI Registry

Use a GitLab deploy token with `read_package_registry` access. Replace the
placeholders with the project ID and deploy-token credentials:

```bash
python -m pip install \
  --index-url "https://<deploy-token-user>:<deploy-token>@gitlab.com/api/v4/projects/<project-id>/packages/pypi/simple" \
  "git-reflow==1.0.2"
```

Release-candidate tags are normalized to PEP 440 package versions. For
example, tag `v1.0.0-rc.1` is installed as `git-reflow==1.0.0rc1`.

Keep tokens out of committed files and shell history. For strictly private
dependency resolution, disable GitLab package forwarding and avoid using a
private registry through `--extra-index-url`.

---

# Install From GitHub

Clone the repository:

```bash id="tw3nx5"
git clone https://github.com/your-org/reflow.git
```

Enter the project:

```bash id="9a4e1t"
cd reflow
```

Create a virtual environment:

```bash id="q3wz4s"
python -m venv .venv
```

Activate the environment.

Windows:

```bash id="8vcqke"
.venv\Scripts\activate
```

Linux/macOS:

```bash id="o1m3l7"
source .venv/bin/activate
```

Install:

```bash id="i6uk9r"
pip install -e .
```

Verify:

```bash id="j59qdx"
reflow --help
```

---

# Install From GitLab

Clone the repository:

```bash id="svv3gr"
git clone https://gitlab.com/your-org/reflow.git
```

Enter the project:

```bash id="5k7gj4"
cd reflow
```

Install:

```bash id="1u8pj6"
pip install -e .
```

Verify:

```bash id="2r98ud"
reflow --help
```

---

# Install From Release Assets

Reflow release pages may contain:

```text id="uvv0rn"
.whl
.tar.gz
```

files generated using:

```bash id="2u6xt5"
python -m build
```

---

## Install From Wheel

Example:

```text id="gyd2o4"
git_reflow-1.0.2-py3-none-any.whl
```

Install:

```bash id="8n1k9h"
pip install git_reflow-1.0.2-py3-none-any.whl
```

Verify:

```bash id="lqq3ol"
reflow --help
```

---

## Install From Source Archive

Example:

```text id="lf9xv5"
git_reflow-1.0.2.tar.gz
```

Install:

```bash id="ifh0fk"
pip install git_reflow-1.0.2.tar.gz
```

Verify:

```bash id="kgf9w1"
reflow --help
```

---

# Development Installation

Recommended for contributors.

Clone repository:

```bash id="7u7t8h"
git clone <repository-url>
```

Install in editable mode:

```bash id="st0g38"
pip install -e .
```

Benefits:

```text id="2vkq3g"
Immediate code changes
Local development
Testing new features
```

---

# Verify Installation

Display help:

```bash id="1d70xk"
reflow --help
```

Display version:

```bash id="zbix7u"
reflow --version
```

Display initialization help:

```bash id="t7h33m"
reflow init --help
```

Expected result:

```text id="5cx5g2"
Reflow help screen displayed successfully.
```

---

# Optional Dependencies

Some commands require additional tools.

---

## Git

Required for:

```bash id="bgj0q7"
reflow tags convert local
reflow releases recover
reflow dockerize
```

Verify:

```bash id="84sdjq"
git --version
```

---

## GitHub CLI

Required for:

```bash id="4l2hkp"
reflow releases recover
```

Verify:

```bash id="b5fxtu"
gh --version
```

Authentication:

```bash id="r6s8c9"
gh auth login
```

---

## Docker

Required for:

```bash id="ud56kk"
reflow dockerize
```

Verify:

```bash id="9lnvxt"
docker --version
```

---

# First Command

After installation:

```bash id="jbm5q5"
reflow init
```

Recommended workflow:

```text id="m0fd9v"
Install
     ↓
Initialize
     ↓
Configure
     ↓
Run Commands
```

---

# Troubleshooting

## Command Not Found

Verify installation:

```bash id="12v2r0"
pip show reflow
```

or:

```bash id="mnuk7m"
pip list
```

---

## Virtual Environment Not Active

Windows:

```bash id="wmh9o0"
.venv\Scripts\activate
```

Linux/macOS:

```bash id="v79f5z"
source .venv/bin/activate
```

---

## Git Missing

Install Git and verify:

```bash id="zrfq5r"
git --version
```

---

## Docker Missing

Install Docker Desktop or Docker Engine and verify:

```bash id="9xwx6p"
docker --version
```

---

# Related Documentation

Quick Start:

```text id="p9z84r"
docs/user-guide/quickstart.md
```

Installation Methods:

```text id="8zhlsp"
docs/user-guide/installation-methods.md
```

Getting Started:

```text id="4xmnru"
docs/user-guide/getting-started.md
```

Commands:

```text id="u3hks0"
docs/user-guide/commands.md
```

---

# Summary

The recommended installation method for most users is:

```bash id="4zlz4v"
git clone <repository-url>

pip install -e .
```

After installation:

```bash id="p93bju"
reflow init
```

is the recommended first command.

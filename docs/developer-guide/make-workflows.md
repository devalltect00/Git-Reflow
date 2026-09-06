# Make Workflows

## Overview

Reflow uses a small root `Makefile` and focused modules under `make/core/`.
The layout follows the same modular pattern used by the Custy development
tooling. Local, Docker, and Compose commands remain Reflow-specific, while the
remote group exposes the shared Devalltect utility-image catalog.

Run all Make commands from the Reflow repository root:

```bash
make help
```

Use a focused help view when the complete list is too long:

```bash
make help-local
make help-docker
make help-compose
make help-remote
```

`make --help` is GNU Make's own executable help and is not controlled by this
repository. Use `make` or `make help` for the formatted project command list.

## Directory Layout

```text
Makefile
make/
└── core/
    ├── variables/          # Shared runtime and argument variables
    ├── helpers/            # Validation and command registration macros
    ├── setup_install/      # Python environment and installation
    ├── local/              # Reflow through the local virtual environment
    ├── testing/            # Pytest
    ├── lint_format/        # Ruff and Black
    ├── qa/                 # Aggregate quality workflows
    ├── ci/                 # CI-compatible checks
    ├── documentation/      # MkDocs
    ├── build_publish/      # Python package build and publication
    ├── docker/             # Direct Docker workflows
    ├── compose/            # Docker Compose workflows
    ├── remote/             # Published Devalltect utility-image workflows
    ├── git/                # Read-only Git helpers
    ├── cleanup/            # Project and Docker cleanup
    ├── examples/           # Help examples
    └── help/               # Help aggregation
```

The root loader defines the include order. Command implementations and their
help text live in the matching module directories.

## Command Prefixes

| Prefix | Execution environment | Typical prerequisite |
|---|---|---|
| `l-` | Reflow's local `venv` | `make setup` or `make install-dev` |
| `d-` | A locally built Reflow Docker image | `make d-build-prod` |
| `c-` | Reflow's Docker Compose services | Docker and Compose |
| `r-` | Published Devalltect utility images, normally from GHCR | Docker and registry access |

Commands without a runtime prefix cover developer tooling such as `test`,
`lint`, `docs-build`, `build`, and `clean`.

## Current Reflow Commands

The Make targets map to the current CLI names:

| CLI workflow | Local Make target | Dry-run target |
|---|---|---|
| `reflow init` | `l-init` | `l-init-dryrun` |
| `reflow releases recover` | `l-reflow-releases-recover` | `l-reflow-releases-recover-dryrun` |
| `reflow tags convert local` | `l-reflow-tags-convert-local` | `l-reflow-tags-convert-local-dryrun` |
| `reflow tags convert remote` | `l-reflow-tags-convert-remote` | `l-reflow-tags-convert-remote-dryrun` |
| `reflow dockerize` | `l-reflow-dockerize` | `l-reflow-dockerize-dryrun` |

Replace `l-` with `d-` or `c-` for local Docker and Compose workflows. The
published-image targets use `r-reflow-...`, including `r-reflow-init`.

The `*-reflow-tags-replay` targets remain compatibility aliases. They print a
deprecation warning and delegate to the matching `releases recover` target.
They do not invoke the old CLI spelling.

## Passing Reflow Arguments

Shared variables work across all runtimes:

```text
REFLOW_GLOBAL_ARGS
REFLOW_INIT_ARGS
REFLOW_RELEASES_RECOVER_ARGS
REFLOW_TAGS_CONVERT_ARGS
REFLOW_DOCKERIZE_ARGS
REFLOW_EXTRA_ARGS
```

Global options must be placed in `REFLOW_GLOBAL_ARGS` because they appear
before the Reflow command. Examples include:

```text
--repository PATH
--repository-url URL
--dry-run
--debug
--log-level LEVEL
--no-banner
```

Command-specific options belong in their matching variable. For example:

```bash
make l-reflow-tags-convert-local \
  REFLOW_GLOBAL_ARGS="--repository D:/project/testing_lab/testing_reflow" \
  REFLOW_TAGS_CONVERT_ARGS="--to semver --yes"
```

Runtime-specific overrides are also available. For example,
`LOCAL_REFLOW_GLOBAL_ARGS` affects only local execution and
`REMOTE_REFLOW_TAGS_CONVERT_ARGS` affects only the published-image workflow.

## Repository Targets

### Local directory

Preview a conversion in a local target repository:

```bash
make l-reflow-tags-convert-local-dryrun \
  REFLOW_GLOBAL_ARGS="--repository D:/project/testing_lab/testing_reflow"
```

Apply a SemVer replacement in the local checkout:

```bash
make l-reflow-tags-convert-local \
  REFLOW_GLOBAL_ARGS="--repository D:/project/testing_lab/testing_reflow" \
  REFLOW_TAGS_CONVERT_ARGS="--to semver --yes"
```

The local target never mutates a remote. Use the separate remote Make target
when remote refs should be replaced.

### GitHub or GitLab URL

Preview release recovery against a URL through Reflow's temporary-clone mode:

```bash
make l-reflow-releases-recover-dryrun \
  REFLOW_GLOBAL_ARGS="--repository-url https://github.com/owner/repository.git"
```

For `tags convert remote`, a URL target is cloned temporarily and the reviewed
mapping is applied through one guarded atomic push.

```bash
make l-reflow-tags-convert-remote \
  REFLOW_GLOBAL_ARGS="--repository-url https://github.com/owner/repository.git" \
  REFLOW_TAGS_CONVERT_ARGS="--to semver --yes"
```

`reflow init` requires a local directory and does not support
`--repository-url`.

## Container Repository Mounts

Direct Docker commands mount `DOCKER_WORKSPACE_HOST` at `/workspace`. To run a
locally built image against another local repository:

```bash
make d-reflow-tags-convert-dryrun \
  DOCKER_WORKSPACE_HOST="D:/project/testing_lab/testing_reflow"
```

Published-image commands use `REMOTE_WORKSPACE` in the same way:

```bash
make r-reflow-tags-convert-dryrun \
  REMOTE_WORKSPACE="D:/project/testing_lab/testing_reflow"
```

Compose mounts the Reflow checkout defined by the Compose files. For another
repository, use `--repository-url` or use the direct Docker/published-image
workflow with an explicit host workspace.

Docker and Compose developer utilities prepare their required images before
execution. `d-test` builds the development image, while Compose test, lint,
format, shell, and package-build targets build the shared development app image
and then reuse it through their service-specific commands. Compose build targets
build the `app` service explicitly rather than rebuilding every helper service.

Commands that push Git tags, releases, packages, or container images still
need the corresponding Git, GitHub/GitLab, package-index, and registry
credentials inside their execution environment.

## Remote Utility Catalog

The remote group follows Custy's shared utility-image pattern rather than
containing Reflow alone:

| Project | Image variable | Registry targets | Runtime prefix |
|---|---|---|---|
| Path Header Scanner | `REMOTE_IMAGE_PHS` | `r-phs-info`, `r-phs-pull`, `r-phs-push`, `r-phs-remove` | `r-phs-` |
| Doc Gen | `REMOTE_IMAGE_DOC_GEN` | `r-doc-gen-info`, `r-doc-gen-pull`, `r-doc-gen-push`, `r-doc-gen-remove` | `r-doc-` |
| Custy | `REMOTE_IMAGE_CUSTY` | `r-custy-info`, `r-custy-pull`, `r-custy-push`, `r-custy-remove` | `r-custy-` |
| Reflow | `REMOTE_IMAGE_REFLOW` | `r-reflow-info`, `r-reflow-pull`, `r-reflow-push`, `r-reflow-remove` | `r-reflow-` |

All images resolve through:

```text
GHCR_REGISTRY/GHCR_OWNER/REMOTE_IMAGE:REMOTE_TAG
```

The defaults are lowercase GHCR-compatible repository names and can be
overridden from the Make command line. For example:

```bash
make r-custy-pull REMOTE_TAG=v2.0.0
make r-doc-gen-info GHCR_OWNER=another-owner
```

Runtime commands mount `REMOTE_WORKSPACE` at `/workspace`. Common examples are:

```bash
make r-phs-scan TARGET=app REMOTE_WORKSPACE="D:/project/target"
make r-doc-generate-smart REMOTE_WORKSPACE="D:/project/target"
make r-custy-run-validate REMOTE_WORKSPACE="D:/project/target"
make r-reflow-tags-convert-dryrun REMOTE_WORKSPACE="D:/project/target"
```

The shared Custy runtime follows Custy's current command tree. Its dedicated
targets invoke `validate`, `version update`, `changelog generate`, `backup ...`,
`cleanup ...`, and `workflow branch` directly. The
`r-custy-init-all-no-examples` target initializes Custy configuration and
templates without example resources. These Custy-only initialization modes are
not copied into Reflow's own `l-`, `d-`, or `c-` initialization targets.

### Custy credential helpers

Published Custy-image workflows can use an external credential directory
without copying tokens into the Reflow repository or the image:

```bash
make r-custy-credentials-set-github
make r-custy-credentials-set-gitlab
make r-custy-credentials-status
make r-custy-credentials-test CUSTY_CREDENTIALS_REMOTE=origin
```

The provider `set` targets mount the directory read-write. The `status` and
`test` targets mount it read-only, and `test` performs a read-only access check
against the selected Git remote. Credential values are not passed as Make
variables or printed by these targets.

`CUSTY_CREDENTIALS_HOST_DIR` defaults to
`%LOCALAPPDATA%/Custy/credentials` on Windows and
`$XDG_DATA_HOME/custy/credentials` or
`$HOME/.local/share/custy/credentials` on Unix. Its container destination is
controlled by `CUSTY_CREDENTIALS_CONTAINER_DIR` and defaults to
`/run/secrets/custy`.

The credential directory is not mounted into ordinary `r-custy-run*` or
`r-custy-workflow` execution unless explicitly enabled. Use the read-only
runtime mount when a Custy workflow needs the configured fallback:

```bash
make r-custy-run-push CUSTY_CREDENTIALS_MOUNT=true
```

Use `make help-remote` for the complete registry and runtime list. Registry
`push`/`remove` targets and non-dry-run utility commands can change local or
remote state; displaying them in help does not execute them.

## Dry Run

Every Reflow Make workflow has a `-dryrun` variant. It adds Reflow's global
`--dry-run` option without discarding other global arguments.

```bash
make l-reflow-dockerize-dryrun \
  REFLOW_GLOBAL_ARGS="--repository D:/project/testing_lab/testing_reflow"
```

Dry-run targets simulate Reflow mutations. Make targets that directly manage
infrastructure, such as `d-build-all`, `r-reflow-push`, or `d-prune-all`, are
not Reflow CLI workflows and therefore do not use Reflow's dry-run option.

## Development Validation

Common local checks are:

```bash
make test
make lint
make format-check
make check
make docs-build
```

`make qa` modifies formatting before running validation. `make publish`,
`r-reflow-push`, cleanup targets, and non-dry-run release workflows can change
local or external state; review their help and resolved arguments first.

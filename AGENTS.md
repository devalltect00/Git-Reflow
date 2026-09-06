# AGENTS.md

## Project overview

Reflow is a repository-aware Python CLI for release-maintenance workflows. It
converts Git tags between PEP 440 and Semantic Versioning, recovers missing
GitHub releases by re-pushing selected tags, and builds or publishes tagged
Docker images to GitHub Container Registry (GHCR) or GitLab Container Registry.

Reflow can operate on the current checkout, an explicitly selected local Git
repository, or a supported Git URL cloned into a temporary workspace. Preserve
predictable target selection, safe mutation defaults, clear terminal previews,
and configuration compatibility.

## Supported user-facing commands

Primary commands are:

```text
reflow init
reflow tags convert local
reflow tags convert remote
reflow releases recover
reflow dockerize
```

`reflow tags replay` is a deprecated compatibility alias for
`reflow releases recover`. Keep its deprecation warning clear and direct users,
documentation, and new automation to the canonical command.

Important global target and safety options include:

```text
--repository, --repo, -C
--repository-url
--dry-run
```

`reflow tags convert local` replaces tag names only in a persistent checkout;
it rejects repository URLs. `reflow tags convert remote` replaces remote tag
names through one guarded atomic push. Both convert to SemVer by default,
support PEP 440 through `--to pep440`, and require confirmation unless
`--yes`/`-y` is supplied. Signed tags and existing destination refs must stop
the operation before mutation.

`reflow releases recover` does not create releases through a provider API. It
finds version tags without corresponding GitHub releases, deletes and re-pushes
selected remote tags, and thereby retriggers tag-based CI/CD release automation.

## Technology and packaging

- Python 3.14+
- Typer and Rich
- setuptools and setuptools-scm
- Ruff and Black
- Pytest and pytest-cov
- MkDocs Material
- Docker, Docker Compose, and Make helpers

The console entry point is defined in `pyproject.toml`. Reflow configuration
templates under `app/templates/` must remain included in distributions.

## Project structure

```text
app/
├── cli/          CLI commands, options, argument resolution, and help
├── config/       Configuration loading and models
├── core/         Git, repository, release, conversion, and Docker workflows
├── services/     Application-level service composition
├── templates/    Configuration copied by reflow init
├── theme/        Rich styles and theme definitions
├── ui/           Shared terminal presentation
└── utils/        Focused shared utilities

tests/
├── cli/
├── config/
├── core/
├── services/
├── theme/
└── unit/

docs/             User, command, architecture, QA, and developer documentation
make/             Modular local, Docker, Compose, and remote Make commands
```

The CLI entry point is `app/cli/main.py`. Keep parsing, prompting, and
presentation in `app/cli/`; keep reusable behavior in `app/core/` or the
appropriate service layer. Shared terminal rendering belongs in `app/ui/`.
See `docs/project_structure.md` for the fuller inventory.

## Repository targeting contract

Resolve the target repository in this order:

1. An explicit CLI target: `--repository-url` or `--repository`/`--repo`/`-C`
2. A configured target: `[tool.reflow.repository].url` or `.path`
3. The current working directory

Path and URL forms are mutually exclusive at each priority level.

Local paths select an existing checkout. Repository URLs use a temporary clone;
the original remote repository is changed only when the selected operation
explicitly performs a remote mutation. Registry image settings select image
destinations and must never be treated as repository targets.

Do not let Reflow's own source checkout become the implicit target when another
repository was selected. Target identity should remain visible in command
previews and summaries.

## Configuration and templates

Reflow uses `.config/reflow/config.toml`. The source template shipped by the
package is `app/templates/config.toml`; a generated target-project configuration
is user-owned after `reflow init`.

When adding or changing a configuration field:

1. Update the source template and loading/resolution logic.
2. Preserve compatible defaults where practical.
3. Add tests for CLI/config/default precedence and validation.
4. Update the relevant command, configuration, architecture, and QA docs.

Never silently overwrite user-managed `.config/reflow/` content.

## Dry-run and confirmation contracts

When `--dry-run` is enabled:

- Read-only discovery, validation, and temporary-clone setup may execute.
- Persistent local, registry, and remote mutations must be simulated.
- Commands must explain the target and what would change.
- Interactive mutation confirmation must not be required.
- Diagnostic logging may still write to the configured log destination.

Without `--dry-run`, mutating commands must display a meaningful plan and obey
their normal confirmation rules. Automation may bypass supported prompts only
through explicit options such as `--yes`/`-y`. New commands must test both dry-run
and live-mode boundaries.

## External mutation safeguards

Git pushes, tag deletion/re-push, release recovery, registry publishing, and
other external mutations require explicit user authorization. Prefer dry-run or
local test repositories during validation. Never use a production repository,
provider API, or container registry as a test target unless the user explicitly
approves that target and mutation.

Do not run Git commits, tags, pushes, rebases, history rewrites, release
operations, package publication, or registry publication unless explicitly
requested and approved.

## Coding standards

- Follow PEP 8 and existing project conventions.
- Use type hints whenever practical.
- Prefer `pathlib` over `os.path`.
- Keep functions focused and responsibilities separated.
- Prefer composition and straightforward code over unnecessary abstraction.
- Use dataclasses when they clarify data ownership.
- Do not change public CLI behavior without discussing compatibility and impact.
- Preserve unrelated work in a dirty worktree.

Every new public file, class, function, and method should have useful
documentation. Use this section order when applicable:

1. Description
2. Logic
3. Args
4. Returns
5. Raises
6. Notes
7. Examples

Avoid placeholder implementations, hardcoded repository paths, duplicated
business logic, and debugging `print()` calls.

## Logging standards

Use logging when it improves troubleshooting or observability:

- `CRITICAL`: the application cannot continue safely.
- `ERROR`: an operation failed.
- `WARNING`: a recoverable issue, fallback, or deprecation occurred.
- `INFO`: an important workflow state changed.
- `DEBUG`: detailed execution flow or resolved values.

When useful, include timing, target identity, operation names, and structured
counts such as `processed_tags`, `success_count`, `error_count`, or
`retry_count`. Never expose credentials, access tokens, or secret-bearing URLs.

## Testing and validation

All behavior changes require proportionate tests. Follow the existing test
layout rather than creating a parallel taxonomy without a clear need.

Prefer the project virtual environment:

```powershell
.\venv\Scripts\python.exe -m pytest
```

Use targeted tests first, then the full suite. On Windows, use a repository-local
`--basetemp` if the system temporary directory has inherited ACL problems.
Relevant packaging or runtime changes should also be checked through applicable
Docker Compose and Make targets after approval.

For external-facing workflows, use mocks or the dedicated testing repository
unless live mutation was explicitly authorized. Dry-run validation must assert
that no persistent local or remote mutation occurred.

## Documentation

Keep implementation and documentation synchronized. Update the relevant files
under `docs/` when changing commands, options, targeting, configuration,
dry-run behavior, confirmation prompts, installation, output, troubleshooting,
architecture, Docker workflows, or Make targets.

Important entry points include:

```text
docs/Installation.md
docs/usage.md
docs/configuration.md
docs/project_structure.md
docs/qa/
docs/architecture/
docs/developer-guide/
```

Significant architecture changes require an explanation of responsibilities,
dependencies, data flow, and trade-offs. Add or update Mermaid diagrams when a
diagram materially clarifies the change.

## Development workflow

Work in clear phases:

1. Analyze the current implementation, configuration, and target behavior.
2. Describe the design, affected files, compatibility, and risks.
3. Implement focused changes with logging where useful.
4. Add or update tests and documentation.
5. Validate the smallest relevant scope, followed by broader checks.

Before editing or executing mutating commands, explain the intended action and
obtain user confirmation. At each meaningful phase, report completed work,
remaining work, required context, and recommended documentation updates.

## Git workflow

Primary branches:

```text
main
develop
```

Suggested working branches:

```text
feature/<name>
bugfix/<name>
release/<version>
```

## Do not

- Do not remove tests or documentation without justification.
- Do not modify `CHANGELOG.md` or bump the project version unless explicitly requested.
- Do not silently weaken dry-run guarantees or confirmation safeguards.
- Do not revive `reflow tags replay` as the preferred public terminology.
- Do not invent missing code, files, configuration, provider behavior, or URLs.
- Do not confuse a configured Docker image with the target Git repository.
- Do not overwrite user-managed `.config/reflow/` content unexpectedly.
- Do not introduce architectural changes without explaining their impact.

## Completion report

Before completing implementation work, verify and report:

1. What changed and why
2. Files added, modified, or removed
3. Tests and commands run, including results
4. Documentation changes or remaining documentation work
5. Known limitations, missing context, and the next recommended step

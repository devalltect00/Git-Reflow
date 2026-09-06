---
name: follow-reflow-guidelines
description: Apply Reflow-specific authorization boundaries, project references, source layout, release safeguards, environment rules, validation workflow, and documentation requirements. Use for tasks that inspect, run, test, debug, or change files in the git-reflow repository.
---

# Follow Reflow Guidelines

## Purpose

Work safely and consistently in the Reflow repository. Apply this skill together
with the user's latest instruction and the repository's governing files.

## Respect Authorization

1. Treat the user's latest explicit instruction as the authority for the current
   task and its write scope.
2. Before changing files or running commands, describe the intended action and
   obtain confirmation unless the user has already clearly authorized that action
   and scope with wording such as "go ahead", "implement", or "run the tests".
3. Read-only repository inspection is allowed once the user has authorized review
   of the repository.
4. Do not infer permission to modify adjacent or unrelated files. Ask again before
   expanding scope or performing a materially different action.
5. Ask before destructive, externally visible, release-affecting, or credentialed
   operations even when related read-only work is authorized.
6. Keep an authorization active only for its stated paths, operations, and task.

Apply rules in this order:

1. System security, sandbox, and tool restrictions
2. The user's latest explicit instruction
3. File-specific policy
4. Directory-specific policy
5. This skill and repository guidance

If equally ranked rules conflict or the scope is unclear, stop and ask.

## Read the Governing Project Files

Before source analysis, implementation, debugging, testing, or command execution:

1. Read the repository-root `AGENTS.md` as the primary project guide.
2. Read `ENGINEERING_EXECUTION_POLICY.md` when architecture, implementation,
   logging, CLI integration, or release readiness is relevant.
3. Use `pyproject.toml`, `Makefile`, and the active source as executable project
   truth for tool configuration and available commands.
4. Do not silently resolve contradictions by editing project files. In particular,
   `AGENTS.md` currently specifies Python 3.14+ while `pyproject.toml` declares
   Python 3.9+ and configures older tool targets. Report the conflict when Python
   compatibility matters and ask which policy should govern a compatibility change.

## Apply the Repository Path Policy

All paths are repository-relative, and directory rules apply recursively.

| Path | Default policy | Guidance |
| --- | --- | --- |
| `app/**` | Read only until the task authorizes writes | Active application code. Keep CLI, core, configuration, services, and UI responsibilities separated. |
| `.config/reflow/**` and `app/templates/config.toml` | Read only until the task authorizes writes | Reflow configuration and packaged defaults. Keep the two synchronized when approved behavior requires it. |
| `tests/**` | Task-approved writes; explicit removal | Add or update tests for approved behavior changes. Never remove or weaken tests merely to pass validation. |
| `docs/**` and `mkdocs.yml` | Task-approved writes; explicit removal | Documentation is maintained project content, not protected unfinished material. Update relevant guides for approved user-facing, configuration, workflow, or architecture changes. |
| `.agents/skills/**` | Read only until specifically authorized | Repository-local Codex skills. Do not change them as a side effect of ordinary application work. |
| `scripts/**`, `tools/**`, `Makefile`, `Dockerfile`, and `docker-compose*.yml` | Read only until the task authorizes writes | Developer, documentation, build, and container tooling. Check downstream workflow effects before edits. |
| `CHANGELOG.md`, version-bearing files, Git tags, and release metadata | Explicit authorization required | Do not bump versions, edit the changelog, create or replay tags, or alter release metadata automatically. |
| Backup or temporary source files | Protected | Preserve personal or historical copies and exclude them from implementation and formatting. |
| All other paths | Ask before changing | Make no unrelated changes. |

Treat filenames such as `* copy.py`, `*_copy.py`, `*_temp.py`,
`*_temp_before.py`, and similarly obvious backups as inactive. Do not edit,
delete, rename, format, import, or use them as the source of current behavior.

## Understand the Reflow Workflow

Keep discovery proportional to the task, but trace the complete affected workflow:

- Start at `app/cli/main.py` for CLI registration and entry behavior.
- Treat `app/cli/**` as the command, option, resolver, model, and help layer.
- Treat `app/core/**` as orchestration and Git, Docker, GitHub, initialization,
  dry-run, execution, and shared domain behavior.
- Inspect `app/config/**`, `app/services/**`, `app/ui/**`, `app/theme/**`,
  `app/constants/**`, and `app/utils/**` when the workflow crosses them.
- Follow the matching tests under `tests/**` before changing behavior.
- For configuration behavior, preserve the documented precedence of CLI arguments,
  `.config/reflow/config.toml`, and internal defaults.
- Use the active implementation and tests to verify behavior; do not invent missing
  modules or rely on historical notes as current truth.

## Protect Release and External Operations

Reflow can mutate Git history and tags, publish container images, and interact with
remote registries. For commands that can have those effects:

1. Prefer an available `--dry-run` path for initial validation.
2. Resolve and show the target repository, tags, registry, image, and operation
   before a live run.
3. Require explicit approval before creating, deleting, converting, replaying, or
   pushing tags; pushing images; changing remote state; or using credentials.
4. Never print or log tokens, passwords, registry credentials, or sensitive
   configuration values.
5. Stop after the requested target is complete; do not continue into publishing or
   release steps merely because local validation passed.

## Use the Project Environment

Use an existing project virtual environment for Python work. Prefer the checked-in
workspace convention `venv/`, then look for `env/`, `.venv/`, or a versioned
environment. Do not create, replace, upgrade, or install into an environment unless
the user authorizes it.

On Windows, typical approved commands are:

```powershell
venv\Scripts\python.exe -m pytest
venv\Scripts\python.exe -m ruff check app tests
venv\Scripts\python.exe -m black app tests --check
venv\Scripts\reflow.exe --help
```

Use these as examples, not as standing permission. Prefer the project Python over a
global executable, and account for the existing editable installation.

## Implement and Document Approved Changes

For approved implementation work:

1. Define the affected responsibilities, files, and validation before editing.
2. Keep changes focused, complete, typed, and consistent with nearby code.
3. Follow `AGENTS.md` documentation requirements for new files, classes,
   functions, and public methods.
4. Use the project's logging approach where it adds operational value. Do not use
   `print()` for debugging or log secrets.
5. Add or update focused tests for changed behavior.
6. Update relevant documentation for approved user-facing behavior, commands,
   configuration, workflows, developer processes, and architectural changes.
7. For significant architecture changes, explain responsibilities, dependencies,
   and trade-offs, and add or update Mermaid documentation under
   `docs/architecture/` only within the approved scope.
8. Do not change public CLI behavior without discussion, and do not change
   versions or `CHANGELOG.md` unless explicitly requested.

## Validate Proportionally

Run the smallest meaningful checks first, then broader checks justified by the
change and authorization:

1. Focused Pytest targets for affected behavior
2. Relevant Ruff and Black checks
3. The broader test suite or `make test`
4. Documentation link/build checks when documentation changes
5. CLI help or a dry-run workflow when user-facing execution changes

Formatting and autofix commands can rewrite files, so keep them within the approved
path scope. Do not run cleanup, prune, release, push, or live replay targets as
ordinary validation.

## Report Completion

At the end of each applicable phase and in the final result, state:

- What was completed and why
- What remains, if anything
- Which files were added, changed, or removed
- Which commands ran and their outcomes
- Which documentation was updated or why no update was needed
- Any conflicts, skipped checks, missing files, or required user action
- Whether anything outside the approved scope was touched

State explicitly when nothing was removed.

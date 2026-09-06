# TODO

> Current status: see the [2026-09-06 checkpoint update](#checkpoint-4-2026-09-06).
> Older checkboxes, test counts, plans, and decisions are preserved as recorded;
> they are historical context, not proof that every current release gate passed.

Tracks short-term development tasks, improvements, tasks and ideas .

---

## Features

### ✅ Completed

- _(Nothing yet)_

---

### 🧩 In Progress

#### General

- [x] add .github workflow file
  - [x] add ci.yml file
  - [x] add docker-dev.yml file
  - [x] add docker-prod.yml file
  - [x] add release.yml file
- [x] add gitlab-ci.yml
- [x] add ignore files
  - [x] add .gitignore
  - [x] add .dockerignore
  - [x] add .prettierignore
- [x] use logs for external logs
- [x] add .vscode/
  - [x] add .vscode/launch.json // wait if any updates to the app commands if changed
  - [x] add .vscode/settings.json
- [ ] add config or meta data
  - [x] add .pre-commit-config.yaml
  - [x] add .prettierrc.json
  - [x] add AGENTS.md
  - [x] add CONTRIBUTING.md
  - [x] add LICENSE
  - [x] add pyproject.toml
  - [x] add requirements.txt
  - [x] add SECURITY.md
  - [x] add TODO.md
  - [x] add README.md
  - [ ] Add CHANGELOG.md.
- [x] add docker compose files
  - [x] add docker-compose.dev.yml files
  - [x] add docker-compose.prod.yml files
  - [x] add docker-compose.yml files
  - [x] add Dockerfile
- [ ] add example_command.txt
- [x] add Makefile
- [x] add Testing
- [x] add mkdocs.yml
- [x] add documentations
  - [x] Add the docs/badges.md
  - [x] Add the docs/configuration.md
  - [x] Add the docs/how-to-use.md
  - [x] Add the docs/index.md
  - [x] Add the docs/infrastructure.md
  - [x] Add the docs/installation.md
  - [x] Add the docs/usage.md
  - [x] Add the docs/project_structure.md
  - [x] Add the diagrams to docs/diagrams/
- [x] Using .config/ path instead from tools/ path
- [x] add banner
- [x] Fix init
- [ ] General project cleanup and consistency pass.
- [-] Update pyproject.toml description
- [-] Update CONTRIBUTING.md description
- [x] Refactor GitHelper
- [ ] Make sure app run well
- [ ] Update Makefile
- [ ] error exception on CLI when command is missing

==================

refactor Makefile help message
gitlab pipeline
fix why app error when run the command

---

### 🧠 Planned

#### 🚀 v1.0.0 release preparation

- [x] Consolidate the post-v0.1.0 command, repository-targeting, tag-conversion, release-recovery, Docker, configuration, architecture, test, Make, CI/CD, and documentation work into the `v1.0.0-rc.1` release scope.
- [x] Prepare distinct internal commit messages and public tag/release messages for `v1.0.0-rc.1` and stable `v1.0.0`.
- [x] Replace ambiguous release replay terminology with `reflow releases recover` while keeping `reflow tags replay` as a deprecated compatibility alias.
- [x] Add local-path and repository-URL targeting with managed temporary clones and explicit target presentation.
- [x] Add bidirectional PEP 440 and SemVer conversion, safe additive defaults, collision handling, confirmation, and explicit push/delete controls.
- [x] Align modular Make, Docker, Compose, packaging, metadata, `AGENTS.md`, dry-run behavior, tests, and documentation with the current Reflow architecture.
- [ ] Validate `v1.0.0-rc.1` against disposable local and URL-targeted repositories and supported registry workflows.
- [ ] Complete final cleanup and incorporate release-blocking corrections or migration clarifications discovered during RC validation.
- [ ] Run final approved test, documentation, packaging, Make, Docker, Compose, and dry-run release checks.
- [ ] Commit, tag, publish, and verify `v1.0.0` only after explicit release approval.

#### 🧰 Future maintenance

- [ ] Review and update `.pre-commit-config.yaml` so hook versions, Python targets, and validation commands align with the current Reflow project. This is planning only; do not update the configuration as part of the release-message work.

---

### 🔭 Future

- [x] Add supported conversion between PEP 440 and SemVer.
- [ ] Extend conversion to explicitly configured custom tag formats without weakening collision or dry-run safeguards.
- [ ] Validate configured GitHub and GitLab container image URLs and image names before publication.

---

### 🗑️ Cancelled / Dropped

- _(Nothing yet)_

---

## ⚖️ Considerations

- _(Nothing yet)_

---

## 💡 Ideas

- _(Nothing yet)_

---

## 🧾 Notes

### TODO.md

Keep this file concise, status-driven, and updated during each milestone.

---

<a id="checkpoint-3-2026-09-02"></a>

## 2026-09-02 status update — untagged checkpoint 3

Version scope: **v1.0.0-rc.1**.
The [checkpoint commit message](../.config/custy/templates/commit-message-v1.0.0-development-checkpoint-3.txt)
has **no associated tag or tag message**. Earlier checkpoint files remain unchanged.

### ✅ Current application and developer workflow

- [x] Retain the v0.1.0 baseline: a simple tag-replay, version-conversion, and Docker-release utility.
- [x] Use `tags convert local` for persistent checkouts and `tags convert remote` for guarded atomic remote replacement; keep SemVer as the default and PEP 440 as an explicit destination.
- [x] Preserve supported tag metadata, visible target previews, confirmation, signed-tag/conflict guards, and non-mutating dry-run boundaries.
- [x] Keep URL/path selection separate from registry image destinations and show actionable CLI errors and configurable progress.
- [x] Keep `releases recover` as GitHub workflow retriggering, not direct API release creation; retain `tags replay` only as a deprecated alias.

Earlier notes about additive conversion, `--push`, or `--delete-old` describe
the previous design. The explicit local/remote replacement workflow supersedes
that design; the original notes remain as history.

### ✅ Delivery work carried forward

- [x] Align local, Docker/Compose, Make, pre-commit, and hosted CI validation with the active project rather than the old standalone layout.
- [x] Validate annotated release-tag metadata and package versions; publish exact prerelease/stable image tags and update `latest` only for stable releases.
- [x] Add private GitLab Python package build, artifact checks, clean-install verification, and protected-tag publication using `CI_JOB_TOKEN`.
- [x] Normalize supported release tags to PEP 440 package versions; reject unsupported or ambiguous versions rather than guessing.
- [x] Keep unprotected GitLab tag pipelines validation-only, skipping production-image, package-upload, and provider-release jobs.
- [x] Document installation of an available package version from the selected project registry, independently of cloning source or pulling a container.
- [x] Record the maintainer's report that hosted pipelines passed and the GitLab package registry was populated. This is historical reported validation, not a new pipeline run for this documentation checkpoint.

### ✅ Optional repository metadata helper

- [x] Add `scripts/repository/src/sync_metadata.py` outside the core application and installed CLI.
- [x] Read `[project].description` and independent GitHub/GitLab topics from `pyproject.toml`; do not reinterpret package keywords as repository topics.
- [x] Resolve one repository per provider from ordered remote candidates; the current defaults are GitHub `origin` and GitLab `backup`, using fetch URLs.
- [x] Provide a `--dry-run` path with read-only Git discovery and no provider API calls.
- [x] Document authenticated `gh`/`glab` for live updates, topic replacement and empty-list clearing, no confirmation prompt, and possible partial updates on failure.
- [x] Refresh the README against active commands, configuration, runtime requirements, installation methods, and the helper's actual `src/` path.
- [x] Keep helper details in checkpoint/release commit messages; leave user-facing tag-message templates unchanged for this maintainer-only addition.

### ⏳ Follow-up and release gates

- [ ] Correct the helper docstring examples that omit `src/` and reconcile its GitHub topic-limit constant (currently 50) with the provider maximum of 20.
- [ ] Add isolated mocked coverage for metadata validation, remote selection, dry-run API suppression, topic clearing, and provider failures before treating the helper as fully validated.
- [ ] Review actual targets, credentials, topic lists, and provider permissions before a separately authorized live metadata synchronization; no live synchronization was performed for this checkpoint.
- [ ] Re-run the relevant checks against the exact candidate commit before creating the v1.0.0-rc.1 tag. A passing temporary-tag pipeline is not a formal release.
- [ ] Complete the RC review and approved stable cleanup, then validate the final v1.0.0 commit before its release tag.
- [ ] Review and update pre-commit configuration in a future maintenance task. Existing pre-commit setup is complete; this pending item means a later refresh, not that hooks were never configured.

### Notes and evidence

- [README](../README.md) and [metadata helper](../scripts/repository/src/sync_metadata.py) describe the current setup.
- [GitLab package pipeline](../.gitlab/python-package.yml) defines the validation/publication boundary.
- Earlier test/coverage figures and release-checklist statuses remain attached to their original milestones.
- No existing history, ideas, alternatives, cancelled work, backup snapshots, or earlier checkpoint messages were removed.

---

<a id="checkpoint-4-2026-09-06"></a>

## 2026-09-06 status update — untagged checkpoint 4

Version scope: **v1.0.0-rc.1**.
The [checkpoint commit message](../.config/custy/templates/commit-message-v1.0.0-development-checkpoint-4.txt)
has **no associated tag or tag message**. It becomes part of the cumulative
RC.1 and stable release history.

### ✅ GitHub release-note rendering

- [x] Replace fragile shell-interpreted Markdown output with explicit `printf` generation so backticks remain literal release content.
- [x] Preserve the complete reviewed annotated tag message as the main GitHub Release description.
- [x] Populate version, release type, repository, commit, and workflow metadata instead of leaving empty placeholders.
- [x] Present concise literal Docker pull and CLI verification commands instead of transient image-download or runner output.
- [x] Preserve exact prerelease image tags and stable-only `latest` behavior.
- [x] Add regression coverage for release-note construction and keep the GitLab release workflow unchanged.

### ✅ Validation recorded

- [x] Complete Reflow test suite: 365 passed with 92% overall coverage.
- [x] Targeted release-workflow regression checks passed.
- [x] Pre-commit validation passed for the checkpoint and cumulative release-message templates.
- [x] Diff whitespace and mirrored-template consistency checks passed.

### Notes and evidence

- [GitHub release workflow](../.github/workflows/release.yml) contains the corrected release-note generation.
- [Checkpoint 4 commit message](../.config/custy/templates/commit-message-v1.0.0-development-checkpoint-4.txt) records the internal implementation details.
- The cumulative RC.1 and v1.0.0 commit and tag messages include checkpoint 4; this checkpoint itself remains untagged.
- No existing history, plans, ideas, cancelled work, or earlier checkpoint evidence was removed.

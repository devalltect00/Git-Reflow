# TODO

> Cumulative snapshot for **v1.0.0**. Earlier tasks, unfinished work,
> considerations, ideas, cancelled items, and notes are intentionally retained.

# Reflow TODO Tracking History — v1.0.0

> Current status: see the [2026-09-08 post-RC stabilization update](#stabilization-checkpoint-2026-09-08).
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

## Since v0.1.0

- [x] Create a simple Reflow CLI for replaying Git tags to retrigger tag-based CI/CD workflows.
- [x] Add basic one-way conversion from PEP 440 tag names to Semantic Versioning tag names.
- [x] Build and publish one Docker image per Git tag to GHCR, GitLab Container Registry, or both, using `.reflow.toml` configuration.

---

## Since v1.0.0-rc.1

### Version context

| Field            | Value                                                                                                                |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| Version          | `v1.0.0-rc.1`                                                                                                        |
| Previous version | `v0.1.0`                                                                                                             |
| Release type     | Major release candidate                                                                                              |
| Version strategy | Semantic Versioning                                                                                                  |
| Runtime policy   | Python 3.14+                                                                                                         |
| Purpose          | Validate repository targeting, tag replacement, release recovery, Docker publishing, and the redesigned architecture |

### Completed release-candidate scope

#### Commands and targeting

- [x] Establish `reflow init`, `reflow tags convert local`, `reflow tags convert remote`, `reflow releases recover`, and `reflow dockerize` as the supported command set.
- [x] Keep `reflow tags replay` as a clearly deprecated compatibility alias.
- [x] Add explicit local targets through `--repository`, `--repo`, and `-C`.
- [x] Add direct HTTPS, SSH, Git-protocol, and SCP-style URL targeting through `--repository-url`.
- [x] Add mutually exclusive configured `path` and `url` targets with actionable conflict errors.
- [x] Materialize URL targets in managed temporary clones and clean them after success or failure.
- [x] Keep `reflow init` local-only.

#### Tag conversion

- [x] Add explicit local and remote conversion scopes.
- [x] Convert PEP 440 to SemVer by default and support SemVer to PEP 440 with `--to pep440`.
- [x] Preview every planned mapping, skipped tag, target repository, and mutation scope.
- [x] Require confirmation for live conversion, with `--yes`/`-y` for reviewed automation.
- [x] Use all-or-nothing local reference transactions and guarded atomic remote replacement.
- [x] Preserve lightweight targets and supported annotated-tag metadata.
- [x] Reject signed tags, collisions, invalid plans, and incompatible remote state before mutation.
- [x] Verify post-operation results and report converted, skipped, failed, and no-op outcomes accurately.

#### Release recovery and Docker

- [x] Discover GitHub tags that do not have corresponding GitHub Releases.
- [x] Re-push selected tags to retrigger existing tag-based CI/CD rather than creating releases directly.
- [x] Add stable-only filtering, limits, delays, previews, confirmation, and summaries.
- [x] Build and publish Docker images from the selected repository and its tags.
- [x] Support GHCR, GitLab Container Registry, or both providers.
- [x] Show repository, build context, provider, and image destinations before execution.
- [x] Add per-image failure details, partial-publication accounting, and reliable nonzero failure exits.

#### Safety, UI, and architecture

- [x] Apply dry-run simulation to initialization, conversion, recovery, Docker build/tag/push/cleanup, and temporary-clone workflows.
- [x] Keep persistent local, remote, and registry mutations behind explicit live execution.
- [x] Add Rich banners, panels, tables, confirmations, summaries, spinners, and determinate progress.
- [x] Add configurable progress output and Windows-safe completion rendering.
- [x] Centralize expected and unexpected CLI error handling without duplicate normal-mode tracebacks.
- [x] Separate CLI, repository, Git, GitHub, Docker, initialization, dry-run, task execution, services, executors, UI, and configuration responsibilities.

#### Tooling, tests, and documentation

- [x] Add modular Make, Docker, Compose, CI/CD, packaging, Ruff, Black, Pytest, pre-commit, and MkDocs workflows.
- [x] Add repository-target, clone-lifecycle, conversion, transaction, recovery, Docker, initialization, dry-run, progress, help, and error-boundary regression tests.
- [x] Ensure tests do not require a user-generated `.config/reflow/config.toml`.
- [x] Document all commands, repository selection, dry-run, confirmation, progress, conversion, recovery, Docker, Q&A, troubleshooting, and architecture.
- [x] Prepare separate internal commit and public release messages for RC.1 and stable 1.0.0.

### Breaking-change checklist

- [x] Document migration from `.reflow.toml` to `.config/reflow/config.toml`.
- [x] Document replacement of `convert-tags` with explicit local and remote conversion commands.
- [x] Document replacement of `replay-tags` with `releases recover`.
- [x] Remove additive conversion semantics based on `--push` and `--delete-old` from the supported workflow.
- [x] Document the new console entry point, target model, and internal extension boundaries.

### RC validation checklist

- [ ] Validate initialization in a disposable local repository.
- [ ] Validate both conversion directions against disposable lightweight and annotated tags.
- [ ] Verify collision, signed-tag, and remote-preflight failures leave refs unchanged.
- [ ] Verify local, URL-targeted, recovery, and Docker dry-runs create no persistent mutations.
- [ ] Validate guarded remote replacement against a dedicated non-production repository.
- [ ] Validate GHCR and GitLab image plans without publishing unless separately approved.
- [ ] Run final tests, coverage, lint, format, docs, package, Make, Docker, and Compose checks.
- [ ] Commit, tag, publish, and verify `v1.0.0-rc.1` only with explicit release approval.

### Deferred beyond RC.1

- [ ] Add GitLab release discovery and recovery.
- [ ] Support explicitly configured custom tag formats without weakening collision or dry-run safeguards.
- [ ] Validate configured registry image names and destinations before publication.
- [ ] Complete stable-release cleanup and incorporate only release-blocking RC corrections.

### Notes

- Release recovery retriggers an existing workflow; it does not directly create
  a GitHub Release page.
- This snapshot does not claim that any Git tag, release, package, or image was
  published.

---

## Since v1.0.0

### Version context

| Field                   | Value                                         |
| ----------------------- | --------------------------------------------- |
| Version                 | `v1.0.0`                                      |
| Previous version        | `v1.0.0-rc.1`                                 |
| Previous stable version | `v0.1.0`                                      |
| Release type            | Stable major release                          |
| Version strategy        | Semantic Versioning                           |
| Promotion rule          | Preserve the RC.1 safety and command contract |

### Stable feature baseline

#### CI/CD baseline promoted from RC.1

- [x] Carry forward dynamic GitHub and GitLab registry destinations.
- [x] Carry forward annotated-tag, non-empty-message, and package-version validation.
- [x] Carry forward exact prerelease image tags and stable-only `latest` publication.
- [x] Carry forward full tag-message release notes, package artifacts, and root multi-stage Docker builds.
- [ ] Re-run the hosted-workflow-equivalent checks after final stable cleanup and before creating `v1.0.0`.

- [x] Carry forward the focused initialization, local conversion, remote conversion, release recovery, and Docker commands.
- [x] Carry forward local-path and direct repository-URL targeting with managed clone cleanup.
- [x] Carry forward bidirectional PEP 440 and SemVer conversion with SemVer as the default.
- [x] Carry forward collision-aware atomic replacement and metadata preservation.
- [x] Carry forward GitHub release recovery by guarded tag re-push and CI/CD retriggering.
- [x] Carry forward GHCR and GitLab registry workflows based on the selected repository.
- [x] Carry forward visible targets, previews, confirmations, `--yes`, dry-run, progress, summaries, and actionable errors.
- [x] Carry forward layered services, executors, protocols, factories, typed targets, results, exceptions, UI, and configuration.
- [x] Preserve `reflow tags replay` only as a deprecated alias.

### Stable-release finalization

- [ ] Incorporate only release-blocking corrections and migration clarifications found during RC validation.
- [ ] Remove temporary development artifacts that are not part of the supported product.
- [ ] Review package metadata, generated configuration, command help, documentation, CI/CD, and container destinations.
- [ ] Confirm no source-repository fallback can override an explicitly selected target.
- [ ] Confirm failed and partially failed Docker publication returns a nonzero exit and a useful summary.
- [ ] Preserve completed development history and future plans in versioned and rolling tracking documents.

### Stable validation checklist

- [ ] Run the approved full test and coverage suite in a clean checkout without generated Reflow configuration.
- [ ] Run Ruff, Black, packaging, and documentation validation.
- [ ] Validate root and nested help while repository configuration is invalid.
- [ ] Validate every mutating workflow through dry-run.
- [ ] Validate representative Make, Docker, and Compose workflows.
- [ ] Re-check local and remote atomic tag replacement in disposable repositories.
- [ ] Verify release-recovery wording and deprecated-alias guidance in CLI help and documentation.
- [ ] Commit and create the `v1.0.0` tag only with explicit release approval.
- [ ] Verify releases, packages, images, and documentation after publication.

### Known 1.0 boundaries

- [x] GitHub release discovery is supported; GitLab release discovery is not included.
- [x] PEP 440 and SemVer conversion are supported; arbitrary custom formats are not inferred.
- [x] Signed tags stop conversion because renaming would invalidate their signatures.
- [x] Repository targets and Docker image destinations remain separate configuration concepts.
- [x] URL targets are temporary workspaces unless the user maintains a separate persistent clone.

### Future work

- [ ] Add GitLab release discovery and recovery when provider behavior and tests are defined.
- [ ] Add explicitly configured custom tag formats with collision-safe planning.
- [ ] Strengthen registry image URL and image-name validation.
- [ ] Review and intentionally refresh pre-commit hooks and Python targets.

### Notes

- Stable 1.0 should promote the validated RC.1 behavior without weakening its
  dry-run, confirmation, targeting, or atomicity guarantees.
- Unchecked publication tasks are intentionally not presented as completed.

---

## Additional status and roadmap carried from repository TODO files

### Target-project source configuration

- [x] Add `[tool.reflow.project].project_source` resolution for the selected target project's source directory.
- [x] Support explicit source directories such as `app` and `src` together with automatic resolution.
- [x] Keep the resolved target-project source separate from repository targeting and Docker image configuration.

### High-priority tag controls

- [ ] Add tag-pattern filtering, such as `--match "v2.*"`, to conversion, release recovery, and Docker publishing.
- [ ] Add single-tag selection through a reviewed `--tag` option.
- [ ] Add inclusive tag-range selection for controlled migrations and image recovery.
- [ ] Expand summaries with processed, successful, skipped, and failed counts.
- [ ] Add optional Markdown or JSON summary exports.
- [ ] Continue improving dry-run mapping output without changing its non-mutating contract.

### Versioning and configuration extensions

- [ ] Add explicit custom version mappings without weakening collision checks.
- [ ] Define conversion-provider or plugin boundaries for custom formats.
- [ ] Introduce typed configuration models where they improve validation and maintainability.
- [ ] Consider structured JSON logging in addition to console and file logging.

### Registry and Docker roadmap

- [ ] Evaluate Docker Hub, AWS ECR, Azure ACR, Google Artifact Registry, and Harbor support.
- [ ] Support reviewed multi-registry publication from one operation.
- [ ] Evaluate multi-architecture builds through Docker Buildx.
- [ ] Define safe `latest`-tag behavior.
- [ ] Evaluate SPDX or CycloneDX SBOM generation.

### Developer and reporting roadmap

- [ ] Consider provider, registry, and version plugin interfaces.
- [ ] Evaluate asynchronous executors for independent build or push work while preserving deterministic summaries.
- [ ] Generate optional Markdown, JSON, and CI-artifact reports.
- [ ] Add end-to-end examples for conversion, release recovery, and Docker publishing.
- [ ] Add CLI screenshots only when they remain maintainable and useful.
- [ ] Consider an interactive wizard, a web dashboard, release audit reports, and changelog generation as non-priority ideas.

### Explicitly out of scope

- Kubernetes and Helm deployment.
- Infrastructure provisioning.
- Dockerfile, CI/CD pipeline, or general source-code generation.

> Historical roadmap notes used “replay” for release recovery. New work and
> documentation should use the canonical `reflow releases recover` terminology.

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

### Reflow TODO Tracking History — v1.0.0.md

Keep this file concise, status-driven, and updated during each milestone.

---

<a id="checkpoint-3-2026-09-02"></a>

## 2026-09-02 status update — untagged checkpoint 3

Version scope: **v1.0.0, carrying forward v1.0.0-rc.1 preparation**.
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

Version scope: **v1.0.0, carrying forward v1.0.0-rc.1 preparation**.
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

<a id="stabilization-checkpoint-2026-09-08"></a>

## 2026-09-08 status update — post-RC stabilization checkpoint

Version scope: **between published v1.0.0-rc.1 and planned stable v1.0.0**.
The [stabilization commit message](../.config/custy/templates/commit-message-v1.0.0-stabilization-checkpoint.txt)
has **no associated tag or tag message**. It is separate from pre-RC
development checkpoints 1–4.

### ✅ Stable container aliases

- [x] Publish stable images under the exact, minor, major, and `latest` tags.
- [x] Keep prerelease images exact-only so they cannot move stable aliases.
- [x] Keep GitHub and GitLab alias behavior aligned with the package gate's build-metadata rejection.
- [x] Add structural regression coverage for alias creation and prerelease isolation.
- [x] Update repository and public Docker guidance with immutable and moving-tag semantics.

### ✅ Local validation recorded

- [x] Complete Reflow suite: 366 tests passed with 92% overall coverage.
- [x] Targeted Ruff and Black checks passed for the modified regression test.
- [x] GitHub and GitLab production workflow YAML parsed successfully.

### ⏳ Remaining stable-release validation

- [ ] Validate the hosted workflows with the reviewed `v1.0.0` tag only after explicit release approval.
- [ ] Confirm `v1.0.0`, `v1.0`, `v1`, and `latest` resolve to the same image digest on each enabled registry.
- [ ] Complete final cleanup and the broader stable-release checklist before publication.

### Notes

- The exact `v1.0.0` image tag is the recommended reproducible automation pin.
- `v1.0`, `v1`, and `latest` are intentionally moving aliases advanced only by stable releases.
- The published RC.1 records and pre-RC checkpoint history remain unchanged.

---

<a id="v101-patch-release"></a>

## Since v1.0.1

Version scope: **v1.0.1 patch release**, following published v1.0.0.

### ✅ Root CLI consistency

- [x] Show the Reflow banner and root help for bare `reflow` invocation.
- [x] Exit successfully for bare help, explicit `--help`, and `--version`.
- [x] Preserve `--no-banner` suppression for both bare and explicit help.

### ✅ Container portability

- [x] Remove import-time project-source validation and the unused initialization-registry dependency on the resolved source constant.
- [x] Keep project-source configuration resolution lazy for the code paths that explicitly request it.
- [x] Change the production Docker smoke check to run Reflow from `/tmp`, proving startup does not require `/workspace/app`.
- [x] Add regression coverage for imports from an unrelated working directory.
- [x] Verify the v1.0.1 production image starts from a mounted documentation repository with no `/workspace/app` directory.

### ✅ Release documentation

- [x] Synchronize the source fallback version with v1.0.1.
- [x] Prepare separate internal commit and public annotated-tag messages for v1.0.1.
- [x] Update canonical installation, Docker, reference, and documentation-status pages for the patch release.

### ⏳ Final release actions

- [ ] Re-run the complete test, formatting, lint, pre-commit, documentation, package, and container checks against the exact release commit.
- [ ] Confirm the production image starts with `--help` from both an empty directory and a mounted repository without an `app/` folder.
- [ ] Review the v1.0.1 commit message, annotated tag message, generated changelog, and registry destinations.
- [ ] Commit, create the `v1.0.1` tag, publish, and verify provider releases only with explicit release approval.

### Notes

- The patch does not change repository-target precedence, tag-conversion safeguards, release recovery, Docker publication, confirmation, or dry-run behavior.
- No Git commit, tag, push, package publication, image publication, or provider release was performed while preparing this entry.

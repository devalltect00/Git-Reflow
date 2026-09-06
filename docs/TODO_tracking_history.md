# TODO

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

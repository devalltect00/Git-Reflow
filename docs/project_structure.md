# Project Structure

# Repository Overview

This repository follows a modular structure commonly used in modern projects.

Common directories include:

- `app/` — Main application source code.
- `.config/` — Project configuration files.
- `.github/` — GitHub-related configuration.
- `.vscode/` — Visual Studio Code workspace settings.
- `docs/` — Project documentation and technical references.
- `tests/` — Automated tests.
- `data/` — Input datasets or static data.
- `output/` — Generated outputs from the application.
- `scripts/` — Utility scripts for development or automation.
- `tools/` — Development tools and automation utilities.
- `templates/` — Reusable templates used by the project.

---

# Repository Structure

(project type: ProjectType.PYTHON)

```text
.
├── .agents
│   └── skills
│       └── follow-reflow-guidelines
│           ├── agents
│           │   └── openai.yaml
│           └── SKILL.md
├── .config
│   ├── custy
│   │   ├── templates
│   │   │   ├── backups
│   │   │   │   ├── commit
│   │   │   │   └── tag
│   │   │   ├── changelog
│   │   │   │   └── changelog.j2
│   │   │   ├── examples
│   │   │   │   ├── commit_message
│   │   │   │   └── tag_message
│   │   │   ├── commit-message.txt
│   │   │   └── tag-message.txt
│   │   └── config.toml
│   ├── doc_gen
│   │   └── config.toml
│   ├── path_header_scanner
│   │   └── config.toml
│   └── reflow
│       └── config.toml
├── .gitlab
│   ├── ci.yml
│   ├── docker-dev.yml
│   ├── docker-prod.yml
│   ├── python-package.yml
│   └── release.yml
├── .ruff_cache/ ... (collapsed)
├── app
│   ├── cli
│   │   ├── commands
│   │   │   ├── init
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── main
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── reflow
│   │   │   │   ├── common
│   │   │   │   ├── dockerize
│   │   │   │   ├── releases
│   │   │   │   ├── tags
│   │   │   │   ├── __init__.py
│   │   │   │   └── command.py
│   │   │   └── __init__.py
│   │   ├── constants
│   │   │   ├── args.py
│   │   │   ├── completions.py
│   │   │   └── enums.py
│   │   ├── help
│   │   │   ├── init
│   │   │   │   └── help.py
│   │   │   ├── main
│   │   │   │   └── help.py
│   │   │   ├── reflow
│   │   │   │   ├── dockerize
│   │   │   │   ├── releases
│   │   │   │   └── tags
│   │   │   └── __init__.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   └── versions.py
│   │   ├── errors.py
│   │   └── main.py
│   ├── config
│   │   ├── __init__.py
│   │   └── config_loader.py
│   ├── constants
│   │   ├── docker.py
│   │   ├── path.py
│   │   └── resolver.py
│   ├── core
│   │   ├── build/ ... (collapsed)
│   │   ├── decorators
│   │   │   └── log_decorators.py
│   │   ├── docker
│   │   │   ├── __init__.py
│   │   │   ├── executor.py
│   │   │   ├── factory.py
│   │   │   ├── protocol.py
│   │   │   └── service.py
│   │   ├── dry_run
│   │   │   ├── dry_run.py
│   │   │   └── dry_run_support.py
│   │   ├── execution
│   │   │   ├── __init__.py
│   │   │   └── task_executor.py
│   │   ├── git
│   │   │   ├── __init__.py
│   │   │   ├── executor.py
│   │   │   ├── factory.py
│   │   │   ├── models.py
│   │   │   ├── protocol.py
│   │   │   └── service.py
│   │   ├── github
│   │   │   ├── __init__.py
│   │   │   ├── executor.py
│   │   │   ├── factory.py
│   │   │   ├── protocol.py
│   │   │   └── service.py
│   │   ├── initialize
│   │   │   ├── builder
│   │   │   │   └── init_builder.py
│   │   │   ├── models
│   │   │   │   ├── init_config.py
│   │   │   │   ├── init_spec.py
│   │   │   │   ├── initialization_result.py
│   │   │   │   ├── template_dir.py
│   │   │   │   └── template_file.py
│   │   │   ├── presenters
│   │   │   │   └── initialization_presenter.py
│   │   │   ├── services
│   │   │   │   └── scaffold_generator.py
│   │   │   ├── loader.py
│   │   │   ├── main.py
│   │   │   └── registry.py
│   │   ├── reflow
│   │   │   ├── __init__.py
│   │   │   ├── dockerizer.py
│   │   │   ├── orchestrator.py
│   │   │   ├── release_recovery.py
│   │   │   ├── tag_converter.py
│   │   │   ├── tag_processor.py
│   │   │   └── tag_replacement.py
│   │   ├── repository
│   │   │   ├── __init__.py
│   │   │   ├── executor.py
│   │   │   ├── target.py
│   │   │   └── workspace.py
│   │   └── shared
│   │       ├── __init__.py
│   │       ├── exceptions.py
│   │       └── result.py
│   ├── services
│   │   ├── banner.py
│   │   └── banner_service.py
│   ├── templates
│   │   ├── __init__.py
│   │   ├── __version__.py
│   │   └── config.toml
│   ├── theme
│   │   ├── __init__.py
│   │   └── theme.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── banner.py
│   │   ├── console.py
│   │   ├── exceptions.py
│   │   ├── panels.py
│   │   ├── progress.py
│   │   └── tables.py
│   ├── utils
│   │   ├── logging.py
│   │   └── parsing.py
│   ├── __init__.py
│   ├── __main__.py
│   └── __version__.py
├── build/ ... (collapsed)
├── docs
│   ├── architecture
│   │   ├── design-pattern.md
│   │   ├── diagrams.md
│   │   ├── repository-targeting.md
│   │   └── workflow.md
│   ├── commands
│   │   ├── dockerize
│   │   │   ├── examples.md
│   │   │   ├── faq.md
│   │   │   ├── overview.md
│   │   │   ├── requirements.md
│   │   │   └── workflow.md
│   │   ├── init
│   │   │   ├── examples.md
│   │   │   ├── faq.md
│   │   │   ├── overview.md
│   │   │   └── workflow.md
│   │   ├── releases
│   │   │   └── recover
│   │   │       ├── overview.md
│   │   │       └── workflow.md
│   │   └── tags
│   │       ├── convert
│   │       │   ├── examples.md
│   │       │   ├── faq.md
│   │       │   ├── overview.md
│   │       │   ├── requirements.md
│   │       │   └── workflow.md
│   │       └── replay
│   │           ├── examples.md
│   │           ├── faq.md
│   │           ├── overview.md
│   │           ├── requirements.md
│   │           └── workflow.md
│   ├── developer-guide
│   │   ├── blackbox
│   │   │   └── ai-development-workflow.md
│   │   ├── tooling
│   │   │   └── ruff
│   │   │       ├── ruff-ignore.md
│   │   │       └── ruff-select.md
│   │   ├── developer-guide.md
│   │   ├── docker-workflow.md
│   │   ├── getting-started.md
│   │   └── make-workflows.md
│   ├── diagrams
│   │   ├── generated
│   │   │   ├── architecture-layers.png
│   │   │   ├── convert-workflow.png
│   │   │   ├── dockerize-workflow.png
│   │   │   ├── init-workflow.png
│   │   │   ├── reflow-overview.png
│   │   │   ├── release-lifecycle.png
│   │   │   └── replay-workflow.png
│   │   ├── architecture-layers.mmd
│   │   ├── convert-workflow.mmd
│   │   ├── dockerize-workflow.mmd
│   │   ├── init-workflow.mmd
│   │   ├── README.md
│   │   ├── reflow-overview.mmd
│   │   ├── release-lifecycle.mmd
│   │   ├── replay-workflow.mmd
│   │   └── repository-targeting.mmd
│   ├── future
│   │   └── scripts
│   │       └── validate_github_gitlab_image.py
│   ├── project
│   │   ├── roadmap.md
│   │   └── TODO_future.md
│   ├── qa
│   │   ├── index.md
│   │   ├── repository-targeting.md
│   │   └── troubleshooting.md
│   ├── reads
│   │   ├── notes
│   │   │   └── old
│   │   │       └── reflow
│   │   ├── documentation-audit-report.md
│   │   ├── linting-vs-formatting.md
│   │   └── ruff.md
│   ├── testing
│   │   └── testing-guide.md
│   ├── user-guide
│   │   ├── commands.md
│   │   ├── getting-started.md
│   │   ├── installation-methods.md
│   │   ├── lifecycle.md
│   │   ├── overview.md
│   │   └── quickstart.md
│   ├── badges.md
│   ├── ci-cd.md
│   ├── configuration.md
│   ├── example-command.txt
│   ├── examples.md
│   ├── how-to-use.md
│   ├── index.md
│   ├── infrastructure.md
│   ├── Installation.md
│   ├── project_structure.md
│   ├── TODO_tracking_history.md
│   └── usage.md
├── htmlcov/ ... (collapsed)
├── logs/ ... (collapsed)
├── make
│   ├── backups
│   │   └── Full_Makefile - 22082026
│   └── core
│       ├── build_publish
│       │   ├── command.mk
│       │   └── help.mk
│       ├── ci
│       │   ├── command.mk
│       │   └── help.mk
│       ├── cleanup
│       │   ├── command.mk
│       │   └── help.mk
│       ├── compose
│       │   ├── command
│       │   │   ├── common.mk
│       │   │   └── core.mk
│       │   └── help.mk
│       ├── docker
│       │   ├── command
│       │   │   ├── common.mk
│       │   │   └── core.mk
│       │   └── help.mk
│       ├── documentation
│       │   ├── command.mk
│       │   └── help.mk
│       ├── examples
│       │   └── help.mk
│       ├── git
│       │   ├── command.mk
│       │   └── help.mk
│       ├── help
│       │   ├── command.mk
│       │   ├── helper.mk
│       │   └── variable.mk
│       ├── helpers
│       │   ├── common.mk
│       │   └── registry.mk
│       ├── lint_format
│       │   ├── command.mk
│       │   └── help.mk
│       ├── local
│       │   ├── command.mk
│       │   └── help.mk
│       ├── qa
│       │   ├── command.mk
│       │   └── help.mk
│       ├── remote
│       │   ├── command
│       │   │   ├── registry.mk
│       │   │   └── runtime.mk
│       │   └── help.mk
│       ├── setup_install
│       │   ├── command.mk
│       │   └── help.mk
│       ├── testing
│       │   ├── command.mk
│       │   └── help.mk
│       └── variables
│           ├── help.mk
│           └── variable.mk
├── scripts
│   ├── ci
│   │   ├── __init__.py
│   │   └── package_version.py
│   ├── docs
│   │   ├── docs
│   │   │   └── render_mermaid_examples.md
│   │   ├── venv/ ... (collapsed)
│   │   ├── check_docs_links.py
│   │   └── render_mermaid.py
│   ├── repository
│   │   └── src
│   │       └── sync_metadata.py
│   └── __init__.py
├── templates
│   ├── commit-msg.txt
│   └── tag-msg.txt
├── tests
│   ├── cli
│   │   ├── test_error_handling.py
│   │   ├── test_init_command.py
│   │   ├── test_main_command.py
│   │   ├── test_main_resolver.py
│   │   ├── test_release_recovery.py
│   │   ├── test_repository_targeting.py
│   │   ├── test_tag_conversion.py
│   │   └── test_versions.py
│   ├── config
│   │   └── test_config_loader.py
│   ├── core
│   │   ├── build/ ... (collapsed)
│   │   ├── docker
│   │   │   ├── test_executor.py
│   │   │   ├── test_factory.py
│   │   │   └── test_service.py
│   │   ├── dry_run
│   │   │   ├── test_dry_run.py
│   │   │   └── test_dry_run_support.py
│   │   ├── git
│   │   │   ├── test_executor.py
│   │   │   ├── test_factory.py
│   │   │   ├── test_service.py
│   │   │   ├── test_tag_models.py
│   │   │   └── test_tag_replacement_integration.py
│   │   ├── github
│   │   │   ├── test_executor.py
│   │   │   ├── test_factory.py
│   │   │   └── test_service.py
│   │   ├── initialize
│   │   │   └── test_scaffold_generator.py
│   │   ├── reflow
│   │   │   ├── test_dockerizer.py
│   │   │   ├── test_orchestrator.py
│   │   │   ├── test_tag_converter.py
│   │   │   ├── test_tag_processor.py
│   │   │   └── test_tag_replacement.py
│   │   ├── repository
│   │   │   ├── test_executor.py
│   │   │   ├── test_target.py
│   │   │   └── test_workspace.py
│   │   └── shared
│   │       ├── test_exceptions.py
│   │       └── test_result.py
│   ├── services
│   │   └── test_banner_service.py
│   ├── theme
│   │   └── test_theme.py
│   ├── ui
│   │   └── test_progress.py
│   ├── unit
│   │   └── config
│   │       ├── test_precommit_config.py
│   │       └── test_pyproject_toml.py
│   ├── conftest.py
│   ├── test_container_workflows.py
│   ├── test_make_workflows.py
│   └── test_runtime_imports.py
├── tools
│   ├── clean-test-tags.bat
│   └── docker-build-push.bat
├── venv/ ... (collapsed)
├── .dockerignore
├── .gitignore
├── .gitlab-ci.yml
├── .pre-commit-config.yaml
├── .prettierignore
├── .prettierrc.json
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── docker-compose.yml
├── Dockerfile
├── ENGINEERING_EXECUTION_POLICY.md
├── LICENSE
├── Makefile
├── mkdocs.yml
├── pyproject.toml
├── README.md
├── requirements.txt
├── SECURITY.md
└── TODO.md
```

---

## Root Files

| File | Description |
|------|-------------|
| `README.md` | Project overview and introduction. |
| `CHANGELOG.md` | History of notable changes between releases. |
| `LICENSE` | Project license information. |
| `CONTRIBUTING.md` | Guidelines for contributing to the project. |
| `SECURITY.md` | Security policy and vulnerability reporting instructions. |
| `TODO.md` | Pending tasks and future improvements. |
| `AGENTS.md` | Instructions and guidance for AI agents and automation tools. |
| `ENGINEERING_EXECUTION_POLICY.md` | Engineering execution standards and policies. |
| `pyproject.toml` | Main Python project configuration file. |
| `requirements.txt` | Python package dependencies. |
| `mkdocs.yml` | MkDocs documentation site configuration. |
| `Makefile` | Defines common development, testing, and build commands. |
| `Dockerfile` | Container image build instructions. |
| `docker-compose.yml` | Default multi-container Docker configuration. |
| `docker-compose.dev.yml` | Development Docker Compose configuration. |
| `docker-compose.prod.yml` | Production Docker Compose configuration. |
| `.gitignore` | Specifies files and directories ignored by Git. |
| `.dockerignore` | Specifies files excluded from Docker build context. |
| `.prettierrc.json` | Prettier code formatting configuration. |
| `.prettierignore` | Files ignored by Prettier. |
| `.pre-commit-config.yaml` | Pre-commit hooks configuration. |
| `.gitlab-ci.yml` | GitLab CI/CD pipeline configuration. |

---

## Directory Details

### `.config/`
Project configuration files.

Stores reusable configuration files used by the project.
Helps keep the repository root clean and organized.

Common examples:
- .config/tool-config/
- .config/templates/
- .config/settings/

### `app/`
Main application source code.

Contains the core implementation of the project.
May include business logic, services, modules, and utilities.

### `docs/`
Project documentation and technical references.

The documentation folder usually contains structured knowledge about the project.

Common documentation sections:
- docs/architecture        → system design and architecture diagrams
- docs/development         → development guides and workflows
- docs/system              → detailed technical documentation
- docs/reference           → command references and APIs
- docs/user-guide          → instructions for end users
- docs/diagrams            → visual architecture diagrams
- docs/phases              → project phases and planning
- docs/Q&A                 → common questions and explanations

Common files:
- PROJECT_STRUCTURE.md
- DEVELOPMENT_GUIDE.md
- HOW_TO_USE.md
- TODO.md
- CLI_COMMAND.md
- references.md
- badges.md

### `scripts/`
Utility scripts for development or automation.

May include deployment scripts, maintenance tools, or helpers.

### `templates/`
Reusable templates used by the project.

Often includes templates for git commit messages or configuration files.

Example structure:
- templates/git/example/commit-msg
- templates/git/example/tag-msg
- templates/git/example/gitignore

Templates allow consistent commit messages and tagging workflows.

### `tests/`
Automated tests.

Contains unit tests and integration tests.
Ensures code reliability and correctness.

### `tools/`
Development tools and automation utilities.

Contains scripts used during development and maintenance.

Common examples:
- tools/generate_ignore     → generate .gitignore, .dockerignore
- tools/project_structure   → generate PROJECT_STRUCTURE.md
- tools/git_commit          → commit and tagging automation tools


---

## Notes

- Temporary files, caches, and environment directories are excluded.
- Structure is generated automatically using DocGen.

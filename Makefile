# =========================
# CONFIG
# =========================
APP = reflow

# =========================
# INSTALL
# =========================
install:
	pip install -e .

install-dev:
	pip install -e .[dev]

# =========================
# COMMANDS (CLI)
# =========================
help:
	$(APP) --help

init:
	$(APP) init

dockerize:
	$(APP) dockerize

dockerize-dry:
	$(APP) dockerize --dry-run

replay:
	$(APP) replay-tags

replay-dry:
	$(APP) replay-tags --dry-run

convert:
	$(APP) convert-tags

# =========================
# TEST
# =========================
test:
	pytest -v

# =========================
# CLEAN
# =========================
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# =========================
# DOCKER (CLI TOOL)
# =========================
build-image:
	docker build -t reflow:latest .

run-image:
	docker run --rm reflow:latest --help
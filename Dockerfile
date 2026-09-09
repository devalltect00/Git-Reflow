# Dockerfile

# =========================================================
# ➤ BASE STAGE
# =========================================================

# =========================
# 💿 Base image
# =========================

# Use official Python image
FROM python:3.14-slim AS base

# =========================
# 🔡 Environment
# =========================

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# 📁 Working directory (WORKSPACE)
# =========================

# Set working directory
WORKDIR /workspace

# =========================
# 📦 SYSTEM DEPENDENCIES
# =========================

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        | dd of=/etc/apt/keyrings/githubcli.gpg status=none \
    && chmod a+r /etc/apt/keyrings/githubcli.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        docker-ce-cli \
        gh \
        git \
        make \
    && rm -rf /var/lib/apt/lists/*

# Alternatives:
# docker.io \
# docker-cli \
#
# gh \

# NOTE:
# Don't use like these below when install
#   make \
#   git \
#   # docker.io \
#   # docker-cli \
#   docker-ce-cli \
# Comments inside a \ continuation can produce unexpected parsing behavior.

# =========================
# 📄 Copy application
# =========================

COPY . .

# =========================
# 🚀 PYTHON SETUP
# =========================

RUN pip install --no-cache-dir --upgrade pip

# Optional PEP 440 version supplied by CI or a reviewed local build. Git metadata
# remains outside the Docker context, so setuptools-scm otherwise uses its
# configured fallback version.
ARG REFLOW_BUILD_VERSION


# =========================================================
# ➤ DEVELOPMENT STAGE
# =========================================================

# =========================
# 💿 DEVELOPMENT IMAGE
# =========================

FROM base AS development

# =========================
# 📦 Install DEV dependencies
# =========================

RUN if [ -n "$REFLOW_BUILD_VERSION" ]; then \
        SETUPTOOLS_SCM_PRETEND_VERSION="$REFLOW_BUILD_VERSION" \
            pip install --no-cache-dir -e ".[dev]"; \
    else \
        pip install --no-cache-dir -e ".[dev]"; \
    fi

# =========================
# 🚀 Default command
# =========================

ENTRYPOINT ["reflow"]

CMD ["--help"]


# =========================================================
# ➤ PRODUCTION STAGE
# =========================================================

# =========================
# 💿 PRODUCTION IMAGE
# =========================

FROM base AS production

# =========================
# 📦 INSTALL RUNTIME DEPENDENCIES
# =========================

RUN if [ -n "$REFLOW_BUILD_VERSION" ]; then \
        SETUPTOOLS_SCM_PRETEND_VERSION="$REFLOW_BUILD_VERSION" \
            pip install --no-cache-dir .; \
    else \
        pip install --no-cache-dir .; \
    fi

# Fail the image build when a runtime dependency is missing or CLI startup
# incorrectly assumes that the current directory has a Python ``app`` folder.
RUN cd /tmp && reflow --no-banner --help

# =========================
# 🚀 Default command
# =========================

ENTRYPOINT ["reflow"]

CMD ["--help"]

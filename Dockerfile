FROM python:3.14-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# LABEL org.opencontainers.image.source=https://github.com/devalltect00/git_reflow
# LABEL org.opencontainers.image.description="Git Reflow CLI tool"
# LABEL org.opencontainers.image.licenses=MIT

# Install system deps (optional but safe)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only necessary files first (better caching)
COPY pyproject.toml README.md ./

# Install project
RUN pip install --no-cache-dir .

# Copy source
COPY app ./app

# CLI entry
ENTRYPOINT ["reflow"]
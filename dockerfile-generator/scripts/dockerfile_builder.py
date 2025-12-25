#!/usr/bin/env python3
"""
Dockerfile Generator - Creates optimized multi-stage Dockerfiles.
"""

import json
import sys
from typing import Optional


TEMPLATES = {
    "node": {
        "base_image": "node:20-alpine",
        "build_deps": ["python3", "make", "g++"],
        "port": 3000
    },
    "python": {
        "base_image": "python:3.12-slim",
        "build_deps": ["gcc", "libpq-dev"],
        "port": 8000
    },
    "go": {
        "base_image": "golang:1.22-alpine",
        "runtime_image": "alpine:3.19",
        "port": 8080
    },
    "rust": {
        "base_image": "rust:1.75-alpine",
        "runtime_image": "alpine:3.19",
        "port": 8080
    }
}


def generate_node_dockerfile(
    app_name: str = "app",
    port: int = 3000,
    use_pnpm: bool = False,
    include_healthcheck: bool = True
) -> str:
    """Generate optimized Node.js Dockerfile."""
    pkg_manager = "pnpm" if use_pnpm else "npm"
    install_cmd = "pnpm install --frozen-lockfile" if use_pnpm else "npm ci --only=production"
    dev_install = "pnpm install --frozen-lockfile" if use_pnpm else "npm ci"

    healthcheck = ""
    if include_healthcheck:
        healthcheck = f"""
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD wget --no-verbose --tries=1 --spider http://localhost:{port}/health || exit 1
"""

    return f"""# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json {"pnpm-lock.yaml" if use_pnpm else ""} ./
{"RUN corepack enable && corepack prepare pnpm@latest --activate" if use_pnpm else ""}

# Install all dependencies (including dev)
RUN {dev_install}

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Security: run as non-root
RUN addgroup -g 1001 -S nodejs && \\
    adduser -S nodejs -u 1001

# Copy package files
COPY package*.json {"pnpm-lock.yaml" if use_pnpm else ""} ./
{"RUN corepack enable && corepack prepare pnpm@latest --activate" if use_pnpm else ""}

# Install production dependencies only
RUN {install_cmd} && \\
    npm cache clean --force

# Copy built assets
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

USER nodejs

EXPOSE {port}

ENV NODE_ENV=production
{healthcheck}
CMD ["node", "dist/index.js"]
"""


def generate_python_dockerfile(
    app_name: str = "app",
    port: int = 8000,
    use_poetry: bool = False,
    framework: str = "fastapi"
) -> str:
    """Generate optimized Python Dockerfile."""

    install_section = ""
    if use_poetry:
        install_section = """# Install poetry
RUN pip install poetry && \\
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi"""
    else:
        install_section = """COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt"""

    cmd = '["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]' if framework == "fastapi" else '["python", "main.py"]'

    return f"""# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

{install_section}

# Production stage
FROM python:3.12-slim AS production

WORKDIR /app

# Security: run as non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE {port}

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:{port}/health')" || exit 1

CMD {cmd}
"""


def generate_go_dockerfile(
    app_name: str = "app",
    port: int = 8080,
    use_cgo: bool = False
) -> str:
    """Generate optimized Go Dockerfile."""
    cgo_env = "CGO_ENABLED=1" if use_cgo else "CGO_ENABLED=0"

    return f"""# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache git {"gcc musl-dev" if use_cgo else ""}

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build
COPY . .
RUN {cgo_env} GOOS=linux go build -ldflags="-w -s" -o /{app_name} .

# Production stage
FROM alpine:3.19 AS production

WORKDIR /app

# Security: run as non-root
RUN addgroup -g 1001 -S appgroup && \\
    adduser -S appuser -u 1001 -G appgroup

# Install runtime dependencies
RUN apk add --no-cache ca-certificates tzdata

# Copy binary
COPY --from=builder /{app_name} .

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE {port}

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD wget --no-verbose --tries=1 --spider http://localhost:{port}/health || exit 1

ENTRYPOINT ["./{app_name}"]
"""


def generate_nextjs_dockerfile(
    port: int = 3000,
    standalone: bool = True
) -> str:
    """Generate optimized Next.js Dockerfile."""
    return f"""# Dependencies stage
FROM node:20-alpine AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# Builder stage
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs && \\
    adduser --system --uid 1001 nextjs

{"COPY --from=builder /app/.next/standalone ./" if standalone else "COPY --from=builder /app/.next ./.next"}
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

USER nextjs

EXPOSE {port}

ENV PORT {port}

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD wget --no-verbose --tries=1 --spider http://localhost:{port}/api/health || exit 1

CMD ["node", "server.js"]
"""


def generate_dockerignore() -> str:
    """Generate .dockerignore file."""
    return """# Dependencies
node_modules
.pnpm-store
__pycache__
*.pyc
.venv
venv

# Build outputs
.next
dist
build
*.egg-info

# Development
.git
.gitignore
.env*
.DS_Store
*.log

# IDE
.vscode
.idea
*.swp

# Testing
coverage
.pytest_cache
.nyc_output

# Docker
Dockerfile*
docker-compose*
.docker

# Documentation
README.md
docs
*.md
"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        lang = sys.argv[1].lower()

        if lang == "node":
            print(generate_node_dockerfile())
        elif lang == "python":
            print(generate_python_dockerfile())
        elif lang == "go":
            print(generate_go_dockerfile())
        elif lang == "nextjs":
            print(generate_nextjs_dockerfile())
        elif lang == "dockerignore":
            print(generate_dockerignore())
        else:
            print(f"Unknown language: {lang}")
    else:
        print("Dockerfile Generator")
        print("Usage: python dockerfile_builder.py <language>")
        print("Languages: node, python, go, nextjs")
        print("Also: dockerignore")

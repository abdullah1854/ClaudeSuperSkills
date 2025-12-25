#!/usr/bin/env python3
"""
GitHub Actions Workflow Generator - Creates CI/CD workflow templates.
"""

import json
import sys
from typing import Optional


def generate_node_ci(
    node_versions: list[str] = None,
    package_manager: str = "npm",
    test_command: str = "test",
    build_command: str = "build",
    branches: list[str] = None
) -> str:
    """Generate Node.js CI workflow."""

    if node_versions is None:
        node_versions = ["18", "20"]
    if branches is None:
        branches = ["main"]

    matrix = f"node-version: [{', '.join(node_versions)}]"
    cache = "pnpm" if package_manager == "pnpm" else package_manager

    pnpm_setup = ""
    if package_manager == "pnpm":
        pnpm_setup = """
      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8
"""

    install_cmd = {
        "npm": "npm ci",
        "pnpm": "pnpm install --frozen-lockfile",
        "yarn": "yarn --frozen-lockfile"
    }.get(package_manager, "npm ci")

    return f"""name: Node.js CI

on:
  push:
    branches: [{', '.join(branches)}]
  pull_request:
    branches: [{', '.join(branches)}]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        {matrix}

    steps:
      - uses: actions/checkout@v4
{pnpm_setup}
      - name: Use Node.js ${{{{ matrix.node-version }}}}
        uses: actions/setup-node@v4
        with:
          node-version: ${{{{ matrix.node-version }}}}
          cache: '{cache}'

      - name: Install dependencies
        run: {install_cmd}

      - name: Run tests
        run: {package_manager} run {test_command}

      - name: Build
        run: {package_manager} run {build_command}
"""


def generate_python_ci(
    python_versions: list[str] = None,
    test_framework: str = "pytest",
    lint: bool = True
) -> str:
    """Generate Python CI workflow."""

    if python_versions is None:
        python_versions = ["3.11", "3.12"]

    matrix = f"python-version: [{', '.join(f'\"{v}\"' for v in python_versions)}]"

    lint_step = ""
    if lint:
        lint_step = """
      - name: Lint with ruff
        run: |
          pip install ruff
          ruff check .
"""

    return f"""name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        {matrix}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{{{ matrix.python-version }}}}
        uses: actions/setup-python@v5
        with:
          python-version: ${{{{ matrix.python-version }}}}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install {test_framework}
{lint_step}
      - name: Test with {test_framework}
        run: {test_framework}
"""


def generate_docker_build(
    registry: str = "ghcr.io",
    push_on_main: bool = True
) -> str:
    """Generate Docker build and push workflow."""
    return f"""name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: {registry}
  IMAGE_NAME: ${{{{ github.repository }}}}

jobs:
  build:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{{{ env.REGISTRY }}}}
          username: ${{{{ github.actor }}}}
          password: ${{{{ secrets.GITHUB_TOKEN }}}}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{{{version}}}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{{{ github.event_name != 'pull_request' }}}}
          tags: ${{{{ steps.meta.outputs.tags }}}}
          labels: ${{{{ steps.meta.outputs.labels }}}}
          cache-from: type=gha
          cache-to: type=gha,mode=max
"""


def generate_release_workflow() -> str:
    """Generate release automation workflow."""
    return """name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: orhun/git-cliff-action@v3
        with:
          args: --latest --strip header

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.changelog.outputs.content }}
          draft: false
          prerelease: ${{ contains(github.ref, '-') }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""


def generate_deploy_workflow(
    platform: str = "vercel",
    production_branch: str = "main"
) -> str:
    """Generate deployment workflow."""

    if platform == "vercel":
        return f"""name: Deploy to Vercel

on:
  push:
    branches: [{production_branch}]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{{{ secrets.VERCEL_TOKEN }}}}
          vercel-org-id: ${{{{ secrets.VERCEL_ORG_ID }}}}
          vercel-project-id: ${{{{ secrets.VERCEL_PROJECT_ID }}}}
          vercel-args: '--prod'
"""

    elif platform == "cloudflare":
        return f"""name: Deploy to Cloudflare Pages

on:
  push:
    branches: [{production_branch}]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: npm ci && npm run build

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{{{ secrets.CLOUDFLARE_API_TOKEN }}}}
          accountId: ${{{{ secrets.CLOUDFLARE_ACCOUNT_ID }}}}
          projectName: your-project-name
          directory: dist
"""

    return ""


def generate_dependabot_config() -> str:
    """Generate Dependabot configuration."""
    return """version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      dev-dependencies:
        patterns:
          - "@types/*"
          - "eslint*"
          - "prettier*"
          - "typescript"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--node":
            print(generate_node_ci())
        elif cmd == "--python":
            print(generate_python_ci())
        elif cmd == "--docker":
            print(generate_docker_build())
        elif cmd == "--release":
            print(generate_release_workflow())
        elif cmd == "--deploy":
            platform = sys.argv[2] if len(sys.argv) > 2 else "vercel"
            print(generate_deploy_workflow(platform))
        elif cmd == "--dependabot":
            print(generate_dependabot_config())
    else:
        print("GitHub Actions Workflow Generator")
        print("Usage:")
        print("  --node           Node.js CI workflow")
        print("  --python         Python CI workflow")
        print("  --docker         Docker build workflow")
        print("  --release        Release automation")
        print("  --deploy [plat]  Deploy workflow (vercel/cloudflare)")
        print("  --dependabot     Dependabot config")

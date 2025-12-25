# github-actions

Generates GitHub Actions CI/CD workflow templates for Node.js, Python, and Docker.

## Metadata
- **Version**: 1.0.0
- **Category**: devops
- **Source**: workspace


## Tags
`github`, `ci-cd`, `actions`, `automation`

## MCP Dependencies
None specified

## Inputs
- `type` (string) (required): Workflow type: node, python, docker, release
- `branches` (array) (optional): Trigger branches



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "github-actions", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/github-actions/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { type, branches = ['main'] } = inputs;
const branchList = branches.join(', ');

const workflows = {
  node: `name: Node.js CI

on:
  push:
    branches: [${branchList}]
  pull_request:
    branches: [${branchList}]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: \${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run build`,

  docker: `name: Docker Build

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: \${{ github.actor }}
          password: \${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/\${{ github.repository }}:\${{ github.ref_name }}`
};

console.log(workflows[type] || workflows.node);

```

---
Created: Mon Dec 22 2025 10:36:14 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:36:14 GMT+0800 (Singapore Standard Time)

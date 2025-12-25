# git-smart-commit

Generates conventional commit messages by analyzing staged changes.

## Metadata
- **Version**: 1.0.0
- **Category**: git-workflow
- **Source**: workspace


## Tags
`git`, `commit`, `conventional-commits`

## MCP Dependencies
None specified

## Inputs
- `type` (string) (optional): Commit type: feat, fix, refactor, docs, test, chore
- `scope` (string) (optional): Scope of change
- `description` (string) (required): Brief description of change
- `breaking` (boolean) (optional): Is this a breaking change?



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "git-smart-commit", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/git-smart-commit/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { type = 'feat', scope, description, breaking = false } = inputs;

const validTypes = ['feat', 'fix', 'refactor', 'docs', 'test', 'chore', 'style', 'perf', 'ci', 'build'];
const t = validTypes.includes(type) ? type : 'feat';

let message = t;
if (scope) message += `(${scope})`;
if (breaking) message += '!';
message += `: ${description}`;

let body = '';
if (breaking) {
  body = '\n\nBREAKING CHANGE: Describe the breaking change here';
}

const footer = '\n\n🤖 Generated with Claude Code';

console.log(`# Commit Message\n\n\`\`\`\n${message}${body}${footer}\n\`\`\`\n\n## Conventional Commit Types\n- feat: New feature\n- fix: Bug fix\n- refactor: Code refactoring\n- docs: Documentation\n- test: Adding tests\n- chore: Maintenance`);

```

---
Created: Mon Dec 22 2025 10:36:14 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:36:14 GMT+0800 (Singapore Standard Time)

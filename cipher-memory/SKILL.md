# cipher-memory

Formats messages for Cipher cross-IDE memory persistence with proper projectPath.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`memory`, `cipher`, `persistence`

## MCP Dependencies
None specified

## Inputs
- `action` (string) (required): Action: recall, decision, learning, milestone, blocker
- `content` (string) (required): Content to store/recall
- `projectPath` (string) (required): Full project path



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "cipher-memory", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/cipher-memory/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { action, content, projectPath } = inputs;

const templates = {
  recall: { message: `Recall context for this project. What do you remember? Topic: ${content}` },
  decision: { message: `STORE DECISION for ${projectPath}: ${content}` },
  learning: { message: `STORE LEARNING for ${projectPath}: ${content}` },
  milestone: { message: `STORE MILESTONE for ${projectPath}: ${content}` },
  blocker: { message: `STORE BLOCKER for ${projectPath}: ${content}` }
};

const t = templates[action] || templates.recall;

console.log(`// Cipher MCP Call
{
  "tool": "cipher_ask_cipher",
  "arguments": {
    "message": "${t.message}",
    "projectPath": "${projectPath}"
  }
}`);

```

---
Created: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)

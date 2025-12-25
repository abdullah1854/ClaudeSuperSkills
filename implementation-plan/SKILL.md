# implementation-plan

Generates structured implementation plans with requirements, phases, tasks, and definitions of done.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`planning`, `implementation`, `tasks`

## MCP Dependencies
None specified

## Inputs
- `feature` (string) (required): Feature name
- `requirements` (array) (required): List of requirements
- `phases` (array) (optional): Implementation phases



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "implementation-plan", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/implementation-plan/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { feature, requirements, phases = ['Setup', 'Core', 'Integration', 'Test'] } = inputs;
const date = new Date().toISOString().split('T')[0];

let plan = `# Implementation Plan: ${feature}\n\n**Created**: ${date}\n\n## Requirements\n`;
requirements.forEach((r, i) => plan += `- REQ-${String(i+1).padStart(3,'0')}: ${r}\n`);

plan += '\n';
phases.forEach((phase, pi) => {
  plan += `## Phase ${pi+1}: ${phase}\n`;
  plan += `- TASK-${pi+1}.1: [Task description]\n`;
  plan += `  - Files: \`src/...\`\n`;
  plan += `  - DoD: [Definition of done]\n\n`;
});

plan += `## Definition of Done\n- [ ] All tests passing\n- [ ] Code reviewed\n- [ ] Documentation updated`;

console.log(plan);

```

---
Created: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)

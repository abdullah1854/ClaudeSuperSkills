# adr-generator

Generates Architectural Decision Records with context, decision, consequences, and alternatives.

## Metadata
- **Version**: 1.0.0
- **Category**: documentation
- **Source**: workspace


## Tags
`adr`, `architecture`, `documentation`

## MCP Dependencies
None specified

## Inputs
- `title` (string) (required): Decision title
- `context` (string) (required): Problem context
- `decision` (string) (required): The decision made
- `status` (string) (optional): Status: PROPOSED, ACCEPTED, DEPRECATED



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "adr-generator", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/adr-generator/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { title, context, decision, status = 'PROPOSED' } = inputs;
const date = new Date().toISOString().split('T')[0];

console.log(`# ADR: ${title}

## Status
${status}

## Context
${context}

## Decision
${decision}

## Consequences
**Positive:**
- [List benefits]

**Negative:**
- [List trade-offs]

## Alternatives Considered
- [Alternative 1]: [Why not chosen]
- [Alternative 2]: [Why not chosen]

---
*Date: ${date}*`);

```

---
Created: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)


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

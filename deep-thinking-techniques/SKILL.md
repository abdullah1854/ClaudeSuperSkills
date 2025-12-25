# deep-thinking-techniques

Extended reasoning activation with trigger phrases. Enables deeper analysis without model switching. Use when: complex problems, architecture decisions, debugging difficult issues, thorough analysis needed.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`thinking`, `reasoning`, `analysis`, `ultrathink`, `planning`

## MCP Dependencies
None specified

## Inputs
- `level` (string) (optional): Level: think, think-hard, ultrathink
- `task` (string) (required): Task requiring deep thinking
- `critique` (boolean) (optional): Enable self-critique loop

## Chain of Thought
1. Identify complexity level. 2. Select appropriate thinking trigger. 3. Structure problem clearly. 4. Apply extended reasoning. 5. Self-critique if enabled. 6. Synthesize conclusions.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "deep-thinking-techniques", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/deep-thinking-techniques/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Deep Thinking Techniques Skill
const level = inputs.level || 'think-hard';
const task = inputs.task;
const critique = inputs.critique || false;

console.log(\`## Deep Thinking Techniques

### Task: \${task}

---

## Thinking Trigger Phrases

These are natural language cues that activate extended reasoning:

| Phrase | Effect | Use For |
|--------|--------|---------|
| "think step by step" | Structured reasoning | Multi-step problems |
| "think harder" | Extended analysis | Complex decisions |
| "ultrathink" | Maximum reasoning | Architecture, debugging |

---

## Three-Level Performance Stack

### Level 1: Enhanced Thinking
\`\`\`
"think step by step: \${task}"
\`\`\`
- Activates structured reasoning
- Good for: algorithms, logic problems

### Level 2: Deep Analysis  
\`\`\`
"think harder: \${task}"
\`\`\`
- Extended reasoning mode
- Good for: design decisions, trade-offs

### Level 3: Maximum Reasoning
\`\`\`
"ultrathink: \${task}"
\`\`\`
- Comprehensive analysis
- Good for: architecture, complex debugging

---

## Combining with Plan Mode

\`\`\`
"think harder + plan mode: \${task}"
\`\`\`

This combines:
1. Extended reasoning (deeper analysis)
2. Structured planning (actionable steps)

---

## Self-Critique Loop

\${critique ? \`
**Enabled**: After initial analysis, critique for:
- Edge cases missed
- Alternative approaches
- Potential failures
- Scalability concerns

Pattern:
"ultrathink: \${task}. Then critique your solution for edge cases."
\` : \`
**Disabled**: Single-pass analysis only.

To enable, add critique loop:
"...Then critique it for edge cases and improve."
\`}

---

## Application Patterns

### Debugging
\`\`\`
"ultrathink: Debug this error. Consider all possible causes, 
check each systematically, and propose solutions."
\`\`\`

### Architecture
\`\`\`
"think harder + plan mode: Design a caching strategy for this API.
Consider trade-offs between consistency and performance."
\`\`\`

### Code Review
\`\`\`
"think step by step: Review this code for security issues.
Check each OWASP top 10 vulnerability."
\`\`\`

---

## Key Insight

These phrases cost nothing extra - they're test-time compute 
optimization. You get ~80% of Opus performance at fraction of cost
by simply asking Claude to think more carefully.
\`);
```

---
Created: Tue Dec 23 2025 00:34:29 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:34:29 GMT+0800 (Singapore Standard Time)

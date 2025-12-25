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
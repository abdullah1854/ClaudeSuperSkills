// Context Engineering - Six Pillars Framework
const pillar = inputs.pillar || 'all';
const issue = inputs.issue;

console.log(\`## Context Engineering: Six Pillars Framework

### Focus: \${pillar === 'all' ? 'Complete Framework' : pillar.toUpperCase()}
\${issue ? \`### Addressing Issue: \${issue}\` : ''}

---

## THE SIX PILLARS

### 1. AGENTS
Distribute context across specialized AI agents.

- **Why**: Single context window gets overloaded
- **How**: Central coordinator delegates to focused subagents
- **Pattern**: Main AI plans, specialists execute

\`\`\`
Main Context: Planning, coordination
Subagent 1: Code implementation (isolated)
Subagent 2: Research (isolated)
Subagent 3: Testing (isolated)
\`\`\`

---

### 2. QUERY AUGMENTATION
Refine messy queries before execution.

- **Why**: Vague queries → vague results
- **How**: Analyze → Scope → Generate targeted prompt
- **Pattern**: Position Claude as "development manager"

\`\`\`typescript
// Before: "fix the bug"
// After: "In src/auth/login.ts, the validateToken 
//         function returns undefined when token expires.
//         Fix by adding proper expiry checking."
\`\`\`

---

### 3. RETRIEVAL
Strategic chunking and on-demand loading.

- **Why**: Don't load everything upfront
- **How**: CLAUDE.md + Skills for structured retrieval
- **Pattern**: Load at high-attention zones (start/end of context)

\`\`\`
High Attention: [Start of context]
Low Attention:  [Middle - "lost in the middle"]
High Attention: [End of context - where skills load]
\`\`\`

---

### 4. PROMPTING TECHNIQUES
Leverage context window positioning.

- **Why**: Beginning and end get more attention than middle
- **How**: Load expertise when needed, not upfront
- **Pattern**: Skills activate at conversation end = peak attention

---

### 5. MEMORY
Persistent knowledge across sessions.

- **CLAUDE.md**: Loads at session start (authoritative)
- **Skills**: Load on-demand (persistent when loaded)
- **Session files**: Track progress across interactions
- **Cipher**: Cross-IDE memory persistence

---

### 6. TOOLS
Executable capabilities without context exposure.

- **Why**: Don't read implementation, invoke interface
- **How**: Skills wrap complexity in simple invocations
- **Pattern**: MCP tools = context-efficient execution

---

## FOUR FAILURE MODES

| Mode | Problem | Solution |
|------|---------|----------|
| **Poisoning** | Errors compound in reused context | Fresh sessions, /clear |
| **Distraction** | Over-reliance on prior patterns | Strategic chunking |
| **Confusion** | Irrelevant tools misdirect | Skills organization |
| **Clash** | Contradictory information | Single source (CLAUDE.md) |

---

## QUICK WINS

1. **Immediate**: Audit CLAUDE.md structure
2. **This Week**: Create skills for repeated workflows
3. **Ongoing**: Monitor failures, fresh sessions when needed

---

## Core Principle

> "Context is a scarce resource."

Structure determines whether Claude delivers precisely or misses intent.
\`);
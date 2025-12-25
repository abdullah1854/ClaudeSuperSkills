# context-fundamentals

Understand context components, mechanics, and constraints in agent systems. Guides on system prompts, tool definitions, message history, retrieval, and attention mechanics.

## Metadata
- **Version**: 1.0.0
- **Category**: documentation
- **Source**: workspace


## Tags
`context`, `engineering`, `fundamentals`, `agents`

## MCP Dependencies
None specified

## Inputs
- `topic` (string) (optional): Topic: anatomy, attention, quality, disclosure, budgeting



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "context-fundamentals", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/context-fundamentals/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { topic = 'overview' } = inputs;

const topics = {
  overview: `# Context Engineering Fundamentals

Context is the complete state available to a language model at inference time:
- System prompts (identity, constraints)
- Tool definitions (actions available)
- Message history (conversation state)
- Retrieved documents (knowledge)
- Tool outputs (observations)

Key Principles:
1. Context is a FINITE resource with diminishing returns
2. Quality > Quantity - smallest high-signal token set
3. Progressive disclosure - load only when needed
4. Attention budget depletes as context grows`,

  anatomy: `# Anatomy of Context

**System Prompts**: Core identity loaded once at start
- Use clear, direct language
- Balance specificity vs flexibility
- Structure with XML/Markdown sections

**Tool Definitions**: Actions agent can take
- Names + descriptions + parameters
- Descriptions steer behavior
- Poor descriptions force guessing

**Message History**: Scratchpad memory
- Tracks progress and state
- Can dominate context in long tasks

**Tool Outputs**: 80%+ of tokens in typical agents
- Compress/mask after use`,

  attention: `# Attention Mechanics

**Attention Budget**: n tokens = n² relationships
- Budget depletes as context grows
- Models trained on shorter sequences

**Position Effects**:
- Beginning/end get reliable attention
- Middle suffers "lost-in-middle" effect
- Place critical info at edges

**Context Extension**:
- Position interpolation introduces degradation
- Longer contexts = less precision`,

  quality: `# Context Quality vs Quantity

Larger windows DON'T solve memory problems:
- Cost grows exponentially with length
- Performance degrades beyond thresholds
- Long inputs expensive even with caching

Principle: INFORMATIVITY over EXHAUSTIVENESS
- Include what matters for current decision
- Exclude what doesn't
- Design systems to access more on demand`,

  disclosure: `# Progressive Disclosure

Load information ONLY as needed:
1. At startup: skill names/descriptions only
2. On activation: full skill content

**File-System Pattern**:
- Store reference materials externally
- Load files when needed
- File metadata hints at relevance

**Hybrid Strategy**:
- Pre-load stable context (CLAUDE.md)
- Enable autonomous exploration
- Dynamic vs static content tradeoff`,

  budgeting: `# Context Budgeting

Design with explicit budgets:
1. Know effective limit for model/task
2. Monitor usage during development
3. Trigger compaction at 70-80%
4. Design assuming degradation

Budget Allocation:
- System prompt: 5-10%
- Tool definitions: 10-20%
- Retrieved docs: variable
- Message history: growing
- Buffer: 20% reserved`
};

console.log(topics[topic] || topics.overview);

```

---
Created: Mon Dec 22 2025 10:43:11 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:43:11 GMT+0800 (Singapore Standard Time)

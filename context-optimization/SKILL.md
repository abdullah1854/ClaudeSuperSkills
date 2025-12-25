# context-optimization

Techniques to extend effective context capacity: compaction, observation masking, KV-cache optimization, and partitioning strategies.

## Metadata
- **Version**: 1.0.0
- **Category**: documentation
- **Source**: workspace


## Tags
`context`, `optimization`, `performance`, `tokens`

## MCP Dependencies
None specified

## Inputs
- `technique` (string) (optional): Technique: compaction, masking, caching, partitioning, budget



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "context-optimization", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/context-optimization/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { technique = 'overview' } = inputs;

const techniques = {
  overview: `# Context Optimization Techniques

Goal: Better use of available capacity, NOT magic increases

Primary Strategies:
1. **Compaction**: Summarize near limits (50-70% reduction)
2. **Observation Masking**: Replace verbose outputs (60-80%)
3. **KV-Cache**: Reuse cached computations (70%+ hit rate)
4. **Partitioning**: Split across sub-agents

When to Optimize:
- Context utilization >70%
- Quality degrades as conversations extend
- Costs increase with length
- Latency increases with conversation`,

  compaction: `# Compaction Strategies

Summarize context when approaching limits:
1. Identify compressible sections
2. Generate fidelity-preserving summaries
3. Replace full content with summaries

Priority (what to compress):
1. Tool outputs → summaries of key findings
2. Old turns → key decisions/commitments
3. Retrieved docs → key facts/claims
4. NEVER compress system prompt

Summary Targets:
- Tool outputs: Preserve metrics, conclusions. Remove raw output
- Conversations: Preserve decisions, context shifts. Remove filler
- Documents: Preserve key facts. Remove elaboration

Target: 50-70% reduction with <5% quality loss`,

  masking: `# Observation Masking

Tool outputs = 80%+ of tokens in agents
Replace verbose outputs with compact references:

**Never Mask**:
- Critical to current task
- From most recent turn
- Used in active reasoning

**Consider Masking**:
- From 3+ turns ago
- Verbose with extractable key points
- Purpose already served

**Always Mask**:
- Repeated outputs
- Boilerplate headers/footers
- Already summarized in conversation

Example:
\`[Obs:ref_123 elided. Key: Found 5 matching records, top result: X]\`

Target: 60-80% reduction in masked observations`,

  caching: `# KV-Cache Optimization

KV-cache stores Key/Value tensors during inference:
- Grows linearly with sequence
- Caching identical prefixes avoids recomputation
- Dramatically reduces cost/latency

Optimization Patterns:
1. Place stable content FIRST (system prompt, tools)
2. Then frequently reused content
3. Unique/dynamic content LAST

Design for Cache Stability:
- Avoid dynamic content (timestamps)
- Use consistent formatting
- Keep structure stable across sessions

Example Order:
\`[system_prompt, tool_defs, reused_templates, unique_content]\`

Target: 70%+ cache hit rate for stable workloads`,

  partitioning: `# Context Partitioning

Most aggressive optimization: split across sub-agents

Each sub-agent operates in:
- Clean context
- Focused on its subtask
- Without accumulated context from others

Result Aggregation:
1. Validate all partitions completed
2. Merge compatible results
3. Summarize if still too large

Use When:
- Tasks decompose into parallel subtasks
- Different subtasks need different tools/prompts
- Single context would degrade`,

  budget: `# Budget Management

Explicit Context Budgets:
1. Allocate tokens by category
2. Monitor usage vs budget
3. Trigger optimization at thresholds

Typical Allocation:
- System prompt: 5-10%
- Tool definitions: 10-20%
- Retrieved docs: 20-30%
- Message history: 20-30%
- Buffer: 20%

Trigger-Based Optimization:
- >70%: Consider optimization
- >80%: Apply optimization
- Performance drop: Investigate degradation`
};

console.log(techniques[technique] || techniques.overview);

```

---
Created: Mon Dec 22 2025 10:43:12 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:43:12 GMT+0800 (Singapore Standard Time)

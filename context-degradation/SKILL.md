# context-degradation

Recognize and mitigate context degradation patterns: lost-in-middle, poisoning, distraction, confusion, and clash. Includes model-specific thresholds.

## Metadata
- **Version**: 1.0.0
- **Category**: documentation
- **Source**: workspace


## Tags
`context`, `degradation`, `debugging`, `agents`

## MCP Dependencies
None specified

## Inputs
- `pattern` (string) (optional): Pattern: lost-in-middle, poisoning, distraction, confusion, clash, thresholds, mitigation



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "context-degradation", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/context-degradation/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { pattern = 'overview' } = inputs;

const patterns = {
  overview: `# Context Degradation Patterns

Context degrades predictably as length increases:

1. **Lost-in-Middle**: Middle content gets 10-40% less attention
2. **Poisoning**: Errors compound through repeated reference
3. **Distraction**: Irrelevant info overwhelms relevant
4. **Confusion**: Wrong context influences responses
5. **Clash**: Accumulated info directly conflicts

Mitigation Strategies:
- Write (save outside window)
- Select (pull relevant only)
- Compress (summarize)
- Isolate (sub-agents)`,

  'lost-in-middle': `# Lost-in-Middle Phenomenon

Information in the middle of context receives dramatically less attention:
- 10-40% lower recall accuracy vs beginning/end
- Caused by attention mechanics + training distributions
- "Attention sink" on first tokens soaks up budget

Mitigations:
- Place critical info at beginning or end
- Use explicit section headers
- Surface key points in summaries at edges
- Consider whether info supports reasoning (placement matters less)`,

  poisoning: `# Context Poisoning

Errors enter context and compound through repeated reference:

Entry Pathways:
1. Tool outputs with errors/unexpected formats
2. Retrieved docs with incorrect info
3. Model-generated hallucinations that persist

Symptoms:
- Degraded output quality on previously working tasks
- Tool misalignment (wrong tools/parameters)
- Persistent hallucinations despite correction

Recovery:
- Truncate to before poisoning point
- Explicitly note poisoning, ask re-evaluation
- Restart with clean context, preserve only verified info`,

  distraction: `# Context Distraction

Long context causes over-focus on provided info at expense of training knowledge:

The Distractor Effect:
- Single irrelevant document reduces performance
- Multiple distractors compound degradation
- Model must attend to EVERYTHING provided
- No mechanism to "skip" irrelevant content

Mitigations:
- Apply relevance filtering before loading
- Use namespacing to isolate irrelevant sections
- Consider tool calls vs context loading
- Curate what enters context carefully`,

  confusion: `# Context Confusion

Irrelevant information influences responses inappropriately:

Signs:
- Responses address wrong aspects
- Tool calls appropriate for different tasks
- Outputs mix requirements from multiple sources

Causes:
- Multiple task types in single context
- Switching tasks within session
- Unclear task segmentation

Solutions:
- Explicit task segmentation (different tasks = different windows)
- Clear transitions between contexts
- State management isolating different objectives`,

  clash: `# Context Clash

Accumulated information directly conflicts:

Sources:
- Multi-source retrieval with contradictions
- Version conflicts (outdated + current)
- Perspective conflicts (valid but incompatible)

Resolution:
- Explicit conflict marking + clarification request
- Priority rules (which source takes precedence)
- Version filtering (exclude outdated)
- Temporal validity periods on facts`,

  thresholds: `# Model Degradation Thresholds

| Model | Degradation Onset | Severe | Notes |
|-------|------------------|--------|-------|
| GPT-5.2 | ~64K | ~200K | Best with thinking mode |
| Claude Opus 4.5 | ~100K | ~180K | Strong attention mgmt |
| Claude Sonnet 4.5 | ~80K | ~150K | Optimized for agents |
| Gemini 3 Pro | ~500K | ~800K | 1M window |

Model Behaviors:
- Claude 4.5: Refuses/asks clarification vs fabricate
- GPT-5.2: Thinking mode reduces hallucination
- Gemini 3: Strong multimodal reasoning`,

  mitigation: `# The Four-Bucket Approach

**Write**: Save outside window
- Scratchpads, file systems, external storage
- Keep active context lean

**Select**: Pull relevant only
- Retrieval, filtering, prioritization
- Exclude irrelevant

**Compress**: Reduce tokens
- Summarization, abstraction
- Observation masking

**Isolate**: Split across sub-agents
- Each operates in clean context
- Most aggressive but often most effective`
};

console.log(patterns[pattern] || patterns.overview);

```

---
Created: Mon Dec 22 2025 10:43:11 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:43:11 GMT+0800 (Singapore Standard Time)

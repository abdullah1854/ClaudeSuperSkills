# agent-evaluation

Build evaluation frameworks for agent systems. Multi-dimensional rubrics, LLM-as-judge patterns, test set design, and continuous evaluation.

## Metadata
- **Version**: 1.0.0
- **Category**: testing
- **Source**: workspace


## Tags
`evaluation`, `testing`, `agents`, `quality`

## MCP Dependencies
None specified

## Inputs
- `aspect` (string) (optional): Aspect: rubrics, methodology, testset, continuous, pitfalls



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "agent-evaluation", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/agent-evaluation/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { aspect = 'overview' } = inputs;

const aspects = {
  overview: `# Agent Evaluation Methods

Agents require different evaluation than traditional software:
- Non-deterministic between runs
- Multiple valid paths to goals
- No single correct answer

The 95% Finding (BrowseComp):
| Factor | Variance | Implication |
|--------|----------|-------------|
| Token usage | 80% | More tokens = better |
| Tool calls | ~10% | More exploration helps |
| Model choice | ~5% | Better models multiply efficiency |

Key Insight: Model upgrades beat token increases`,

  rubrics: `# Multi-Dimensional Rubrics

Dimensions to Evaluate:
1. **Factual Accuracy**: Claims match ground truth
2. **Completeness**: Covers requested aspects
3. **Citation Accuracy**: Citations match sources
4. **Source Quality**: Uses appropriate primaries
5. **Tool Efficiency**: Right tools, reasonable count

Scoring:
- Convert assessments to 0.0-1.0
- Apply dimension weights
- Calculate weighted overall
- Set pass threshold by use case

DON'T use single metrics - quality is multidimensional`,

  methodology: `# Evaluation Methodologies

**LLM-as-Judge**:
- Scales to large test sets
- Consistent judgments
- Provide: task description, output, ground truth, scale, request structure

**Human Evaluation**:
- Catches what automation misses
- Notices hallucinations on unusual queries
- Detects subtle biases
- Cover edge cases, sample systematically

**End-State Evaluation**:
- For agents that mutate persistent state
- Focus: does final state match expectations?
- Not HOW agent got there

Combine: LLM for scale, human for edge cases`,

  testset: `# Test Set Design

**Sample Selection**:
- Start small during development
- Sample from real usage patterns
- Add known edge cases
- Ensure complexity coverage

**Complexity Stratification**:
| Level | Description |
|-------|-------------|
| Simple | Single tool call |
| Medium | Multiple tool calls |
| Complex | Many calls, ambiguity |
| Very Complex | Extended interaction, deep reasoning |

**Context Testing**:
- Run at different context sizes
- Identify performance cliffs
- Establish safe operating limits`,

  continuous: `# Continuous Evaluation

**Evaluation Pipeline**:
1. Run automatically on agent changes
2. Track results over time
3. Compare versions for regressions

**Production Monitoring**:
- Sample and evaluate randomly
- Set alerts for quality drops
- Maintain trend dashboards

**Feedback Loop**:
1. Collect failure modes
2. Add to test set
3. Fix and validate
4. Deploy with confidence`,

  pitfalls: `# Evaluation Pitfalls to Avoid

1. **Overfitting to Paths**: Evaluate outcomes, not specific steps
2. **Ignoring Edge Cases**: Include diverse scenarios
3. **Single-Metric Obsession**: Use multi-dimensional rubrics
4. **Neglecting Context**: Test with realistic context sizes
5. **Skipping Human Review**: Automated misses subtle issues
6. **No Baseline**: Establish metrics before changes
7. **Release-Only Testing**: Run continuously, not just before deploy`
};

console.log(aspects[aspect] || aspects.overview);

```

---
Created: Mon Dec 22 2025 10:43:12 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:43:12 GMT+0800 (Singapore Standard Time)

const { topic = 'overview' } = inputs;

const topics = {
  overview: `# Agent Evaluation Framework

Agents require different evaluation than traditional software:
- Non-deterministic between runs
- Multiple valid paths to goals
- No single correct answer

**The 95% Finding** (BrowseComp research):
| Factor | Variance Explained | Implication |
|--------|-------------------|-------------|
| Token usage | 80% | More tokens = better performance |
| Tool calls | ~10% | More exploration helps |
| Model choice | ~5% | Better models multiply efficiency |

**Key Insight**: Model upgrades beat token increases. Upgrading to a better model provides larger gains than doubling token budgets.

## Quick Reference

| Topic | Command |
|-------|---------|
| Rubric design | topic: "rubrics" |
| Methodologies | topic: "methodology" |
| Test set design | topic: "testset" |
| Continuous eval | topic: "continuous" |
| Common pitfalls | topic: "pitfalls" |
| 95% finding | topic: "95-finding" |
| Degradation testing | topic: "degradation" |`,

  rubrics: `# Multi-Dimensional Evaluation Rubrics

Single metrics fail for agents. Use multi-dimensional rubrics:

## Core Dimensions

| Dimension | Weight | What it Measures |
|-----------|--------|------------------|
| Factual Accuracy | 30% | Claims match ground truth |
| Completeness | 25% | Covers requested aspects |
| Tool Efficiency | 20% | Right tools, reasonable count |
| Citation Accuracy | 15% | Citations match sources |
| Source Quality | 10% | Uses appropriate primaries |

## Scoring Levels

Each dimension uses a 5-point scale:
- **Excellent** (1.0): All criteria met perfectly
- **Good** (0.8): Minor issues, main goal achieved
- **Acceptable** (0.6): Key aspects correct, some gaps
- **Poor** (0.3): Significant issues
- **Failed** (0.0): Fundamental problems

## Calculating Overall Score

\`\`\`
overall = sum(dimension_score * dimension_weight)
passed = overall >= threshold (typically 0.7)
\`\`\`

## Customization

Adjust weights based on use case:
- Research agents: Increase citation/source weights
- Task automation: Increase tool efficiency weight
- Customer support: Increase completeness weight`,

  methodology: `# Evaluation Methodologies

## LLM-as-Judge

Best for: Scale, consistency, automated pipelines

Prompt structure:
1. Clear task description
2. Agent output to evaluate
3. Ground truth (if available)
4. Evaluation scale with level descriptions
5. Request structured judgment

Advantages:
- Scales to large test sets
- Consistent judgments
- Can evaluate complex reasoning

Limitations:
- May miss subtle hallucinations
- Struggles with domain-specific accuracy

## Human Evaluation

Best for: Edge cases, quality assurance, calibration

Focus areas:
- Hallucinations on unusual queries
- System failures and error handling
- Subtle biases and unsafe outputs
- Context-dependent failures

Process:
- Sample systematically (stratified by complexity)
- Track patterns across evaluations
- Use for calibrating automated systems

## End-State Evaluation

Best for: Agents that mutate persistent state

Focus: Does final state match expectations?
- Database changes
- File system modifications
- External API calls

Ignores: How the agent got there (different valid paths allowed)

## Recommended Approach

Combine all three:
- LLM-as-judge for continuous automated evaluation
- Human review for edge cases and calibration
- End-state checks for state-mutating agents`,

  testset: `# Test Set Design

## Sample Selection Principles

**Start Small**: During development, changes have dramatic impacts. Small test sets (20-50 cases) reveal large effects.

**Sample from Real Usage**: Mining production logs for representative queries. Add known edge cases systematically.

## Complexity Stratification

Every test set should span complexity levels:

| Level | Characteristics | Example |
|-------|-----------------|---------|
| Simple | Single tool call | "What is the capital of France?" |
| Medium | Multiple tool calls | "Compare revenue of Apple vs Microsoft" |
| Complex | Many calls, ambiguity | "Analyze Q1-Q4 sales, create trend report" |
| Very Complex | Extended interaction | "Research AI technologies, recommend strategy" |

## Test Case Structure

\`\`\`json
{
  "name": "descriptive_test_name",
  "input": "The user query or task",
  "expected": { "type": "fact", "answer": "expected output" },
  "complexity": "simple|medium|complex|very_complex",
  "tags": ["category", "feature"],
  "requires_citations": false,
  "requirements": ["must mention X", "must include Y"]
}
\`\`\`

## Coverage Checklist

- [ ] All complexity levels represented
- [ ] Edge cases included
- [ ] Real usage patterns sampled
- [ ] Different tool combinations tested
- [ ] Context size variations covered`,

  continuous: `# Continuous Evaluation

## Evaluation Pipeline

Build automated pipelines that run on every agent change:

\`\`\`
1. Agent change committed
2. CI triggers evaluation run
3. Run against standard test set
4. Compare to baseline metrics
5. Block deployment if regression detected
6. Update baseline on successful deploy
\`\`\`

## Production Monitoring

Sample and evaluate live interactions:

**Sampling Strategy**:
- 1-5% of production traffic
- Stratified by query type
- Higher sampling for new features

**Metrics to Track**:
- Overall pass rate
- Per-dimension scores
- Latency and token usage
- Tool call patterns

**Alerting Thresholds**:
- Warning: pass_rate < 85%
- Critical: pass_rate < 70%
- Quality: avg_score < 0.6

## Trend Analysis

Track metrics over time to detect:
- Gradual degradation
- Sudden regressions
- Improvement from changes
- Seasonal patterns

## Feedback Loop

\`\`\`
1. Collect failure modes from production
2. Add representative cases to test set
3. Fix the underlying issues
4. Validate fix with test set
5. Deploy with confidence
6. Monitor for recurrence
\`\`\``,

  pitfalls: `# Common Evaluation Pitfalls

## 1. Overfitting to Specific Paths

**Problem**: Checking if agent took exact expected steps
**Why it fails**: Multiple valid paths to same goal
**Fix**: Evaluate outcomes, not execution paths

## 2. Single-Metric Obsession

**Problem**: Optimizing for one number (e.g., accuracy)
**Why it fails**: Gaming the metric, ignoring other dimensions
**Fix**: Multi-dimensional rubrics with balanced weights

## 3. Ignoring Edge Cases

**Problem**: Only testing happy paths
**Why it fails**: Agents fail unpredictably on unusual inputs
**Fix**: Include diverse scenarios, stratify by complexity

## 4. Neglecting Context Effects

**Problem**: Testing with ideal context sizes
**Why it fails**: Production context varies, degradation occurs
**Fix**: Test with realistic context sizes and histories

## 5. Skipping Human Review

**Problem**: Relying solely on automated evaluation
**Why it fails**: Automation misses subtle issues
**Fix**: Human evaluation for edge cases and calibration

## 6. No Baseline

**Problem**: Making changes without knowing starting point
**Why it fails**: Can't measure improvement or detect regression
**Fix**: Establish baseline metrics before any changes

## 7. Release-Only Testing

**Problem**: Only evaluating before major releases
**Why it fails**: Slow feedback, accumulated regressions
**Fix**: Continuous evaluation on every change`,

  '95-finding': `# The 95% Performance Finding

Research on BrowseComp (browsing agents finding hard-to-locate information) revealed that **three factors explain 95% of performance variance**:

## Factor Breakdown

| Factor | Variance Explained | What it Means |
|--------|-------------------|---------------|
| **Token Usage** | 80% | More tokens = better performance |
| **Tool Calls** | ~10% | More exploration helps |
| **Model Choice** | ~5% | Better models multiply efficiency |

## Key Implications

### 1. Token Budgets Matter
- Evaluate agents with realistic token budgets
- Don't test with unlimited resources
- Understand the performance/cost tradeoff

### 2. Model Upgrades Beat Token Increases
- Upgrading to a better model (Sonnet 4.5, GPT-5) provides larger gains than doubling tokens
- Better models use tokens more efficiently
- Consider model choice as a lever for improvement

### 3. Multi-Agent Validation
- Supports architectures that distribute work across agents
- Each agent gets a fresh context window
- Explains why multi-agent beats single-agent for complex tasks

## Practical Application

When evaluating agents:
1. Test at multiple token budget levels
2. Compare model choices for same token budget
3. Track tool call efficiency
4. Consider multi-agent for token-intensive tasks`,

  degradation: `# Context Degradation Testing

## Why Test Degradation?

Agent performance can degrade as context grows:
- Critical information gets lost in the middle
- Earlier context may be forgotten
- Competing information causes confusion

## Testing Approach

### 1. Baseline at Fresh Context
Establish performance with minimal context:
- Run test set with clean slate
- Record baseline scores per dimension
- This is your "best case" performance

### 2. Progressive Context Loading
Add context incrementally and measure:
- 25% context capacity
- 50% context capacity
- 75% context capacity
- 90%+ context capacity

### 3. Identify Performance Cliffs
Look for sudden drops:
- Where does accuracy start declining?
- Which dimensions degrade first?
- What's the safe operating limit?

### 4. Stress Testing
Push beyond limits to understand failure modes:
- What happens at context overflow?
- How graceful is degradation?
- Are there recovery mechanisms?

## Metrics to Track

| Metric | What it Indicates |
|--------|-------------------|
| Accuracy vs context size | Information retention |
| First-mention recall | Beginning bias |
| Last-mention recall | Recency bias |
| Middle-content recall | Lost-in-middle effect |
| Tool efficiency vs context | Decision quality under load |

## Setting Safe Limits

Based on testing, establish:
- **Green zone**: Safe operating range
- **Yellow zone**: Monitoring required
- **Red zone**: Active intervention needed`
};

console.log(topics[topic] || topics.overview);

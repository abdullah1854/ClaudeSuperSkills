
const { pattern = 'overview' } = inputs;

const patterns = {
  overview: `# Multi-Agent Architecture Patterns

Sub-agents exist primarily to ISOLATE CONTEXT, not role-play.

Token Economics:
| Architecture | Multiplier | Use Case |
|--------------|-----------|----------|
| Single chat | 1× | Simple queries |
| With tools | ~4× | Tool tasks |
| Multi-agent | ~15× | Complex research |

Key Patterns:
1. **Supervisor**: Central control, delegating to specialists
2. **Swarm/P2P**: Flexible handoffs, no central control
3. **Hierarchical**: Strategy → Planning → Execution layers

Design Principle: Context isolation is the primary benefit`,

  supervisor: `# Supervisor/Orchestrator Pattern

User → Supervisor → [Specialists] → Aggregation → Output

**When to Use**:
- Complex tasks with clear decomposition
- Tasks requiring cross-domain coordination
- When human oversight is important

**Advantages**:
- Strict workflow control
- Easier human-in-the-loop
- Ensures adherence to plans

**Disadvantages**:
- Supervisor context becomes bottleneck
- "Telephone game" - paraphrasing loses fidelity

**The Fix**: forward_message tool
- Sub-agents pass responses directly to users
- Bypasses supervisor synthesis when appropriate
- 50% improvement in benchmarks`,

  swarm: `# Peer-to-Peer/Swarm Pattern

Any agent can transfer to any other via handoff:

\`\`\`
def transfer_to_agent_b():
    return agent_b  # Handoff via function
\`\`\`

**When to Use**:
- Flexible exploration needed
- Rigid planning counterproductive
- Emergent requirements

**Advantages**:
- No single point of failure
- Scales for breadth-first exploration
- Emergent problem-solving

**Disadvantages**:
- Coordination complexity grows with agents
- Risk of divergence without central keeper
- Needs convergence constraints`,

  hierarchical: `# Hierarchical Pattern

Strategy → Planning → Execution

**Strategy Layer**: Goals and constraints
**Planning Layer**: Break into actionable plans
**Execution Layer**: Atomic tasks

**When to Use**:
- Large-scale projects with clear hierarchy
- Enterprise workflows with management layers
- Tasks needing both high-level + detailed execution

**Advantages**:
- Mirrors org structures
- Clear separation of concerns
- Different context at different levels

**Disadvantages**:
- Coordination overhead between layers
- Strategy/execution misalignment
- Complex error propagation`,

  isolation: `# Context Isolation (Primary Purpose)

Each sub-agent operates in CLEAN context:
- Focused on its subtask
- Without accumulated context from others

**Isolation Mechanisms**:

1. **Full Context Delegation**
   - Share entire context for complex tasks
   - Defeats purpose somewhat

2. **Instruction Passing**
   - Planner creates instructions via function
   - Sub-agent receives only what's needed
   - Maintains isolation

3. **File System Memory**
   - Agents read/write to persistent storage
   - Avoids context bloat from state passing
   - Introduces latency

Choose based on: task complexity, coordination needs, latency tolerance`,

  consensus: `# Consensus and Coordination

**The Voting Problem**:
- Simple majority treats hallucinations = strong reasoning
- Multi-agent discussions devolve into false consensus

**Solutions**:

**Weighted Voting**:
- Weight by confidence or expertise
- Higher confidence = more weight

**Debate Protocols**:
- Agents critique each other over rounds
- Adversarial critique > collaborative consensus

**Trigger-Based Intervention**:
- Stall triggers: no progress
- Sycophancy triggers: mimicking without unique reasoning`,

  failures: `# Failure Modes and Mitigations

**Supervisor Bottleneck**:
- Context accumulates from all workers
- FIX: Output schema constraints, checkpointing

**Coordination Overhead**:
- Communication consumes tokens + latency
- FIX: Clear handoff protocols, batch results, async

**Divergence**:
- Agents drift from objectives
- FIX: Objective boundaries, convergence checks, TTL limits

**Error Propagation**:
- Errors in one agent cascade downstream
- FIX: Validate outputs, retry with circuit breakers, idempotent ops`
};

console.log(patterns[pattern] || patterns.overview);

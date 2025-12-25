
const { topic = 'overview' } = inputs;

const topics = {
  overview: `# Memory System Design

Memory provides persistence across sessions and accumulated knowledge:

Memory Evolution:
1. Vector stores (semantic, loses relationships)
2. Knowledge graphs (preserves relationships)
3. Temporal knowledge graphs (adds validity periods)

Benchmark Performance (DMR):
| System | Accuracy | Notes |
|--------|----------|-------|
| Zep (TKG) | 94.8% | Best, fast retrieval |
| MemGPT | 93.4% | Good general |
| GraphRAG | 75-85% | 20-35% over baseline |
| Vector RAG | 60-70% | Loses relationships |
| Recursive Summary | 35.3% | Severe info loss |`,

  architecture: `# Memory Architecture

**The Context-Memory Spectrum**:
- Working memory (context window): Zero latency, volatile
- Short-term: Session-persistent, searchable
- Long-term: Cross-session, structured
- Permanent: Archival, queryable

**Why Vector Stores Fall Short**:
- Lose relationship information
- Can't answer "what else did customers who bought X buy?"
- No temporal validity (current vs outdated facts)

**Graph-Based Memory**:
- Preserves Entity → Relationship → Entity
- Enables traversal queries
- Temporal KG adds validity periods`,

  layers: `# Memory Layer Architecture

**Layer 1: Working Memory** (Context)
- Scratchpad calculations
- Conversation history
- Current task state
- Active retrieved docs

**Layer 2: Short-Term** (Session)
- Persists until session end
- Searchable
- Tracks state across turns
- Caches for re-use

**Layer 3: Long-Term** (Persistent)
- Learns from past interactions
- Builds knowledge over time
- Key-value to graph databases

**Layer 4: Entity Memory**
- Tracks entities across interactions
- Maintains identity consistency
- Stores properties and relationships

**Layer 5: Temporal Knowledge Graph**
- Facts with validity periods
- Time-travel queries
- Prevents context clash`,

  patterns: `# Memory Implementation Patterns

**Pattern 1: File-System-as-Memory**
- Use file hierarchy for organization
- Naming conventions convey meaning
- Timestamps for temporal tracking
- Simple, portable, no infrastructure
- Disadvantage: No semantic search

**Pattern 2: Vector RAG + Metadata**
- Embed facts/docs
- Rich metadata: entity tags, validity, source, confidence
- Query = semantic + metadata filters

**Pattern 3: Knowledge Graph**
- Explicit entity types and relationships
- Graph database or property graph
- Indexes for common patterns

**Pattern 4: Temporal KG**
- Validity periods on all facts
- Time-travel queries
- Prevents outdated info conflicts`,

  retrieval: `# Memory Retrieval Patterns

**Semantic Retrieval**:
- Embedding similarity search
- Good for "find similar"

**Entity-Based Retrieval**:
- Traverse graph relationships
- "Get all related to X"

**Temporal Retrieval**:
- Filter by validity periods
- "What was true at time T?"

**Integration with Context**:
- Just-in-time loading
- Strategic injection at attention-favored positions
- Progressive disclosure`,

  consolidation: `# Memory Consolidation

Memories accumulate - must consolidate:

**Triggers**:
- Significant accumulation
- Too many outdated results
- Periodic schedule
- Explicit request

**Process**:
1. Identify outdated facts
2. Merge related facts
3. Update validity periods
4. Archive/delete obsolete
5. Rebuild indexes

**Guidelines**:
- Consider privacy implications
- Implement backup/recovery
- Monitor growth and performance
- Design for retrieval failures`
};

console.log(topics[topic] || topics.overview);

// Archon - Kanban + RAG Skill
const action = inputs.action || 'create-board';

console.log(\`## Archon: Visual Kanban + RAG

### Action: \${action}

---

## Kanban Board Structure

\`\`\`typescript
interface Board {
  id: string;
  name: string;
  columns: Column[];
  knowledge: KnowledgeBase;
}

interface Column {
  id: string;
  name: string; // "Backlog" | "In Progress" | "Review" | "Done"
  tasks: Task[];
}

interface Task {
  id: string;
  title: string;
  description: string;
  priority: "low" | "medium" | "high";
  labels: string[];
  context: string[]; // RAG-retrieved context
}
\`\`\`

---

## RAG Integration

### Knowledge Base Setup
\`\`\`typescript
// Using vector store for context
const kb = {
  // Store project documentation
  addDocument: async (doc) => {
    const embedding = await embed(doc.content);
    await vectorStore.upsert({
      id: doc.id,
      values: embedding,
      metadata: { source: doc.source, type: doc.type }
    });
  },
  
  // Query relevant context
  query: async (question) => {
    const embedding = await embed(question);
    const results = await vectorStore.query({
      vector: embedding,
      topK: 5
    });
    return results.matches;
  }
};
\`\`\`

### Smart Task Suggestions
\`\`\`typescript
// When creating a task, auto-retrieve relevant context
async function createTask(title, description) {
  // Query knowledge base for relevant docs
  const context = await kb.query(description);
  
  // Suggest related tasks
  const similar = await findSimilarTasks(description);
  
  return {
    title,
    description,
    context: context.map(c => c.metadata.source),
    relatedTasks: similar
  };
}
\`\`\`

---

## Board Operations

### Create Board
\`\`\`bash
# Using TodoWrite for simple Kanban
TodoWrite([
  { content: "Task 1", status: "pending" },    // Backlog
  { content: "Task 2", status: "in_progress" }, // In Progress
  { content: "Task 3", status: "completed" }    // Done
])
\`\`\`

### Sync with External Tools
- Linear: \`linear_*\` MCP tools
- GitHub Projects: \`gh project\` CLI
- Notion: \`notion_*\` MCP tools

---

## RAG Workflow

1. **Index** - Store project docs in vector DB
2. **Query** - Retrieve relevant context for tasks
3. **Augment** - Enhance task descriptions with context
4. **Generate** - AI-powered task breakdown
\`);
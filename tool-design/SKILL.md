# tool-design

Design tools for agent systems. Description engineering, consolidation principle, response formats, error handling, and MCP naming conventions.

## Metadata
- **Version**: 1.0.0
- **Category**: documentation
- **Source**: workspace


## Tags
`tools`, `design`, `agents`, `mcp`

## MCP Dependencies
None specified

## Inputs
- `topic` (string) (optional): Topic: descriptions, consolidation, responses, errors, naming, collection



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "tool-design", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/tool-design/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { topic = 'overview' } = inputs;

const topics = {
  overview: `# Tool Design for Agents

Tools are contracts between deterministic systems and non-deterministic agents.

The Consolidation Principle:
"If a human cannot say which tool to use, an agent cannot either."

Key Principles:
1. Descriptions answer: What, When, What Returns
2. Consolidate overlapping tools
3. Design error messages for agent recovery
4. Use consistent naming conventions
5. Limit to 10-20 tools, use namespacing if more

MCP Naming: Always use \`ServerName:tool_name\` format`,

  descriptions: `# Tool Description Engineering

Descriptions are PROMPT ENGINEERING that shapes behavior.

**Must Answer**:
1. **What** does it do? (Specific, not "helps with")
2. **When** to use? (Direct + indirect triggers)
3. **What inputs**? (Types, constraints, defaults)
4. **What returns**? (Format, examples, errors)

**Bad**: "Search the database"
**Good**: 
\`\`\`
Retrieve customer by ID.

Use when:
- User asks about specific customer
- Need customer context for decisions

Args:
  customer_id: Format "CUST-######"
  format: "concise" | "detailed"

Returns: Customer object
Errors: NOT_FOUND, INVALID_FORMAT
\`\`\``,

  consolidation: `# The Consolidation Principle

Prefer SINGLE comprehensive tools over multiple narrow tools.

**Instead of**:
- list_users
- list_events
- create_event

**Use**:
- schedule_event (finds availability AND schedules)

**Why It Works**:
- Less tool selection complexity
- Fewer tokens (no redundant descriptions)
- No ambiguity about which tool
- Handles full workflow internally

**When NOT to Consolidate**:
- Fundamentally different behaviors
- Different contexts benefit from separation
- Tools called independently`,

  responses: `# Response Format Optimization

Tool responses significantly impact context usage.

**Offer Format Options**:
- \`concise\`: Essential fields only
- \`detailed\`: Complete objects

**Include Guidance**:
- When to use each format
- Agents learn to select appropriately

**Token Efficiency**:
- Concise for confirmations
- Detailed when full context needed for decisions

**Example**:
\`\`\`
Args:
  format: "concise" for key fields, 
          "detailed" for complete record
\`\`\``,

  errors: `# Error Message Design

Errors serve TWO audiences:
1. Developers debugging
2. Agents recovering

**For Agents - Must Be Actionable**:
- What went wrong
- How to correct it

**Design for Recovery**:
- Retryable errors: Include retry guidance
- Input errors: Include corrected format
- Missing data: Specify what's needed

**Example**:
\`\`\`
Error: INVALID_FORMAT
Message: customer_id must match CUST-######
Received: "12345"
Expected: "CUST-000001"
\`\`\``,

  naming: `# MCP Tool Naming

Always use fully qualified names:
\`ServerName:tool_name\`

**Correct**:
- "BigQuery:bigquery_schema"
- "GitHub:create_issue"

**Incorrect**:
- "bigquery_schema" (may fail with multiple servers)

**Conventions**:
- verb-noun pattern: get_customer, create_order
- Consistent parameter names across tools
- Consistent return field names`,

  collection: `# Tool Collection Design

Research: Tool overlap causes model confusion.

**Guidelines**:
- 10-20 tools for most applications
- If more needed, use namespacing
- Each tool = clear, unambiguous purpose

**Selection Mechanisms**:
- Tool grouping by domain
- Example-based selection
- Hierarchy with umbrella tools

**Using Agents to Optimize**:
1. Agent attempts to use tools
2. Collect failure modes
3. Agent analyzes + proposes improvements
4. Test improved descriptions

Result: 40% reduction in task completion time`
};

console.log(topics[topic] || topics.overview);

```

---
Created: Mon Dec 22 2025 10:44:28 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:44:28 GMT+0800 (Singapore Standard Time)

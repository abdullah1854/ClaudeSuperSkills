# sub-agent-invocation

Constitutional delegation protocol for invoking specialized sub-agents. Routes tasks to appropriate specialists (code, research, design, testing) with proper context isolation. Use when: complex tasks need parallel work, specialized expertise required, context isolation needed.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`agents`, `delegation`, `routing`, `parallel`, `specialists`

## MCP Dependencies
None specified

## Inputs
- `task` (string) (required): Task to delegate to sub-agent
- `agentType` (string) (required): Agent type: code, research, design, test, explore, plan
- `context` (string) (optional): Context to pass to sub-agent
- `isolated` (boolean) (optional): Run in isolated context to prevent pollution

## Chain of Thought
1. Analyze task requirements. 2. Select appropriate agent type. 3. Prepare context package (minimal but sufficient). 4. Define success criteria. 5. Invoke with isolation if needed. 6. Collect and validate results.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "sub-agent-invocation", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/sub-agent-invocation/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Sub-Agent Invocation Skill
const agentConfigs = {
  code: {
    name: 'Code Agent',
    focus: 'Implementation, debugging, refactoring',
    tools: ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
    prompt: 'You are a senior developer. Focus on clean, maintainable code.'
  },
  research: {
    name: 'Research Agent', 
    focus: 'Documentation, investigation, analysis',
    tools: ['Read', 'Grep', 'Glob', 'WebFetch', 'WebSearch'],
    prompt: 'You are a research specialist. Gather comprehensive information.'
  },
  design: {
    name: 'Design Agent',
    focus: 'Architecture, UI/UX, system design',
    tools: ['Read', 'Write', 'Glob'],
    prompt: 'You are a system architect. Focus on scalable, maintainable designs.'
  },
  test: {
    name: 'Test Agent',
    focus: 'Testing, validation, quality assurance',
    tools: ['Read', 'Write', 'Bash', 'Grep'],
    prompt: 'You are a QA engineer. Ensure comprehensive test coverage.'
  },
  explore: {
    name: 'Explore Agent',
    focus: 'Codebase navigation, understanding, mapping',
    tools: ['Read', 'Grep', 'Glob', 'LSP'],
    prompt: 'You are a codebase analyst. Map structure and patterns.'
  },
  plan: {
    name: 'Plan Agent',
    focus: 'Planning, architecture, strategy',
    tools: ['Read', 'Grep', 'Glob', 'TodoWrite'],
    prompt: 'You are a technical lead. Create actionable implementation plans.'
  }
};

const agent = agentConfigs[inputs.agentType] || agentConfigs.code;

console.log(`## ${agent.name} Delegation

**Task:** ${inputs.task}

**Focus:** ${agent.focus}

**Available Tools:** ${agent.tools.join(', ')}

**System Context:** ${agent.prompt}

**User Context:** ${inputs.context || 'No additional context provided'}

**Isolation Mode:** ${inputs.isolated ? 'Enabled (separate context window)' : 'Disabled (shared context)'}

### Invocation Pattern:
Use the Task tool with subagent_type="${inputs.agentType === 'explore' ? 'Explore' : inputs.agentType === 'plan' ? 'Plan' : 'general-purpose'}"
`);
```

---
Created: Tue Dec 23 2025 00:30:24 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:30:24 GMT+0800 (Singapore Standard Time)

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
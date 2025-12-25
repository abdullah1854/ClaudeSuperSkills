# skill-creation-guide

Complete guide for creating new Claude Code skills. Templates, best practices, and activation patterns. Use when: creating new skills, documenting workflows, packaging expertise.

## Metadata
- **Version**: 1.0.0
- **Category**: documentation
- **Source**: workspace


## Tags
`skills`, `templates`, `creation`, `guide`, `best-practices`

## MCP Dependencies
None specified

## Inputs
- `skillName` (string) (required): Name for the new skill
- `purpose` (string) (required): What the skill should do
- `category` (string) (optional): Category: code-quality, git-workflow, database, api, documentation, testing, devops, productivity, analysis

## Chain of Thought
1. Define skill purpose clearly. 2. Identify trigger conditions. 3. Write concise description. 4. Create input parameters. 5. Implement code logic. 6. Test activation.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "skill-creation-guide", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/skill-creation-guide/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Skill Creation Guide
const skillName = inputs.skillName;
const purpose = inputs.purpose;
const category = inputs.category || 'productivity';

console.log(\`## Skill Creation Guide: \${skillName}

### Purpose
\${purpose}

---

## Skill Anatomy

### 1. SKILL.md Structure (Claude Code Native)
\`\`\`markdown
---
name: \${skillName}
description: [Concise, trigger-focused description]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# \${skillName}

## When to Use
[Specific trigger conditions]

## Instructions
[Step-by-step procedure]

## Examples
[Concrete examples]
\`\`\`

### 2. MCP Gateway Skill (JSON + Code)
\`\`\`json
{
  "name": "\${skillName}",
  "description": "[Description that triggers activation]",
  "category": "\${category}",
  "inputs": [
    {
      "name": "param1",
      "type": "string",
      "description": "What this parameter does",
      "required": true
    }
  ],
  "tags": ["tag1", "tag2"],
  "code": "// Implementation here"
}
\`\`\`

---

## Best Practices

### Description Writing (CRITICAL)
The description determines when skill activates:

❌ Bad: "Helps with code"
✅ Good: "Reviews TypeScript code for security vulnerabilities, 
   performance issues, and maintainability. Use when: code review 
   requested, PR review, security audit."

### Trigger Phrases
Include in description:
- "Use when: [specific situations]"
- "Activates for: [task types]"
- Keywords users will naturally use

### Input Parameters
- Required: Core inputs needed for skill
- Optional: Customization options with defaults
- Types: string, number, boolean, object, array

---

## Skill Categories

| Category | Use For |
|----------|---------|
| code-quality | Reviews, refactoring, linting |
| git-workflow | Commits, PRs, branching |
| database | Queries, migrations, schemas |
| api | Integrations, endpoints, webhooks |
| documentation | Docs, ADRs, READMEs |
| testing | Test generation, coverage |
| devops | CI/CD, deployment, infra |
| productivity | Workflows, automation |
| analysis | Research, exploration |

---

## Create Skill Command

\`\`\`typescript
gateway_create_skill({
  name: "\${skillName}",
  description: "\${purpose}. Use when: [triggers]",
  category: "\${category}",
  tags: ["relevant", "tags"],
  inputs: [/* parameters */],
  chainOfThought: "1. Step one. 2. Step two...",
  code: \\\`// Your implementation\\\`
});
\`\`\`

---

## Testing Activation

After creating, test with:
1. Direct invocation: \`gateway_execute_skill("\${skillName}", inputs)\`
2. Natural language: Ask Claude something matching description
3. Check if skill loads in context
\`);
```

---
Created: Tue Dec 23 2025 00:34:29 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:34:29 GMT+0800 (Singapore Standard Time)

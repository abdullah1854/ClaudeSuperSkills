# hooks-guide

Claude Code hooks implementation guide. Auto-formatting, permission handling, session context, and skill activation patterns. Use when: setting up automation, configuring permissions, implementing hooks.

## Metadata
- **Version**: 1.0.0
- **Category**: devops
- **Source**: workspace


## Tags
`hooks`, `automation`, `permissions`, `formatting`, `claude-code`

## MCP Dependencies
None specified

## Inputs
- `hookType` (string) (required): Hook type: PreToolUse, PostToolUse, PermissionRequest, SessionStart, Stop, UserPromptSubmit
- `purpose` (string) (optional): What the hook should accomplish

## Chain of Thought
1. Identify hook trigger point. 2. Define matcher pattern. 3. Implement hook command. 4. Configure in settings.json. 5. Test hook behavior.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "hooks-guide", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/hooks-guide/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Hooks Guide Skill
const hookType = inputs.hookType || 'PostToolUse';

console.log(\`## Claude Code Hooks Guide

### Hook Type: \${hookType}

---

## Available Hook Events

| Hook | Trigger | Use Case |
|------|---------|----------|
| PreToolUse | Before tool runs | Block dangerous ops |
| PostToolUse | After tool completes | Auto-format, lint |
| PermissionRequest | Permission dialog | Auto-approve safe commands |
| SessionStart | Session begins | Inject context |
| Stop | Claude finishes | Run tests, validate |
| UserPromptSubmit | User hits enter | Inject instructions |
| SubagentStop | Subagent completes | Validate agent output |

---

## Configuration Location

\`\`\`
~/.claude/settings.json          # Global (personal)
.claude/settings.json            # Project (shared)
.claude/settings.local.json      # Project (personal)
\`\`\`

---

## Hook Templates

### 1. Auto-Format on Save (PostToolUse)
\`\`\`json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \\"$CLAUDE_TOOL_INPUT_FILE_PATH\\""
      }]
    }]
  }
}
\`\`\`

### 2. Auto-Approve Safe Commands (PermissionRequest)
\`\`\`json
{
  "hooks": {
    "PermissionRequest": [{
      "matcher": "Bash(npm test*)|Bash(npm run*)|Read|Grep|Glob",
      "hooks": [{
        "type": "command",
        "command": "echo '{\\"decision\\": \\"approve\\"}'"
      }]
    }]
  }
}
\`\`\`

### 3. Session Context Injection (SessionStart)
\`\`\`json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo '## Session Context' && git status --short && echo '## TODOs' && grep -r 'TODO:' src/ 2>/dev/null | head -10"
      }]
    }]
  }
}
\`\`\`

### 4. Skill Activation Hook (UserPromptSubmit)
\`\`\`json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "node .claude/hooks/skill-activation.mjs"
      }]
    }]
  }
}
\`\`\`

### 5. Test After Stop (Stop)
\`\`\`json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "npm test --passWithNoTests 2>&1 | tail -20"
      }]
    }]
  }
}
\`\`\`

---

## Matcher Syntax

- \`Write|Edit\` - Match Write OR Edit tools
- \`Bash(npm*)\` - Match Bash with npm commands
- \`*\` - Match everything
- NO SPACES around | (will fail)

---

## Hook Responses

### PermissionRequest Response
\`\`\`json
{"decision": "approve"}  // Allow
{"decision": "deny"}     // Block
\`\`\`

### Context Injection
Stdout from hook command is added to Claude's context.

---

## Best Practices

1. **Don't block mid-plan** - Use Stop hook, not PreToolUse
2. **Add logging** - \`2>&1 | tee ~/.claude/hook.log\`
3. **Timeout awareness** - 60 second limit
4. **Security** - Hooks run with your credentials
\`);
```

---
Created: Tue Dec 23 2025 00:34:29 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:34:29 GMT+0800 (Singapore Standard Time)

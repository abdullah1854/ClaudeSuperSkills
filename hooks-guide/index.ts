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
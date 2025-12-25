
const { action, content, projectPath } = inputs;

const templates = {
  recall: { message: `Recall context for this project. What do you remember? Topic: ${content}` },
  decision: { message: `STORE DECISION for ${projectPath}: ${content}` },
  learning: { message: `STORE LEARNING for ${projectPath}: ${content}` },
  milestone: { message: `STORE MILESTONE for ${projectPath}: ${content}` },
  blocker: { message: `STORE BLOCKER for ${projectPath}: ${content}` }
};

const t = templates[action] || templates.recall;

console.log(`// Cipher MCP Call
{
  "tool": "cipher_ask_cipher",
  "arguments": {
    "message": "${t.message}",
    "projectPath": "${projectPath}"
  }
}`);

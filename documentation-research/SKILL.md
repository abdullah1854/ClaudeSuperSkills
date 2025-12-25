# documentation-research

Live library documentation lookup via Context7 API and web research. Fetches current docs for any library/framework. Use when: need current API docs, checking library usage, researching implementation patterns.

## Metadata
- **Version**: 1.0.0
- **Category**: api
- **Source**: workspace


## Tags
`documentation`, `research`, `context7`, `api-docs`, `libraries`

## MCP Dependencies
None specified

## Inputs
- `library` (string) (required): Library/framework name (e.g., react, nextjs, stripe)
- `topic` (string) (optional): Specific topic or API to research
- `version` (string) (optional): Specific version

## Chain of Thought
1. Identify library and version. 2. Query Context7 or official docs. 3. Extract relevant sections. 4. Summarize key patterns. 5. Provide code examples.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "documentation-research", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/documentation-research/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Documentation Research Skill
const library = inputs.library;
const topic = inputs.topic || 'getting started';

console.log(\`## Documentation Research: \${library}

### Research Strategy

1. **Context7 API** (if available):
   Use MCP tool: \`context7_get_library_docs\`
   Query: "\${library} \${topic}"

2. **Official Documentation**:
   - Search: "\${library} documentation \${topic}"
   - Check: npmjs.com, pypi.org for package docs
   
3. **GitHub Repository**:
   - README.md for quick start
   - /docs or /examples folders
   - Issues for common problems

### Quick Research Commands

\`\`\`bash
# NPM package info
npm info \${library}

# Check installed version
npm list \${library}

# Open docs in browser
npx open-cli https://www.npmjs.com/package/\${library}
\`\`\`

### Research Prompt Template

"Research the \${library} library, specifically:
- Current stable version
- \${topic} implementation
- Common patterns and best practices
- Known issues or gotchas
- Code examples"

### MCP Tools to Use
- \`context7_resolve_library_id\` - Get library ID
- \`context7_get_library_docs\` - Fetch documentation
- \`WebSearch\` - Search for tutorials
- \`WebFetch\` - Fetch specific doc pages
\`);
```

---
Created: Tue Dec 23 2025 00:31:32 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:31:32 GMT+0800 (Singapore Standard Time)

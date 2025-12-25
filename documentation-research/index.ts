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
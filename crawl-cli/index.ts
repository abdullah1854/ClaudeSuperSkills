// Crawl CLI Skill
const url = inputs.url;
const depth = inputs.depth || 1;
const output = inputs.output || 'markdown';

console.log(\`## Web Crawling: \${url}

### Available Tools

1. **WebFetch** (Built-in)
   - Simple page fetch with markdown conversion
   - Best for single pages
   
2. **Firecrawl MCP** (if available)
   - \`firecrawl_scrape\` - Single page
   - \`firecrawl_crawl\` - Multi-page with depth
   - \`firecrawl_map\` - Site mapping

3. **Puppeteer MCP** (for JS-heavy sites)
   - Full browser rendering
   - Handle dynamic content

### Crawl Patterns

#### Single Page Extraction
\`\`\`typescript
// Using WebFetch
const content = await WebFetch({
  url: "\${url}",
  prompt: "Extract the main content as clean markdown"
});
\`\`\`

#### Multi-Page Crawl
\`\`\`typescript
// Using Firecrawl
const result = await firecrawl_crawl({
  url: "\${url}",
  maxDepth: \${depth},
  includePaths: ["/docs/*", "/blog/*"],
  excludePaths: ["/api/*"]
});
\`\`\`

### Output Formatting (\${output})

\`\`\`markdown
# Page Title

## Source
URL: \${url}
Crawled: [timestamp]

## Content
[extracted content here]

## Links Found
- [Link 1](url1)
- [Link 2](url2)
\`\`\`

### Best Practices

1. **Respect rate limits** - Add delays between requests
2. **Check robots.txt** - Honor crawl rules
3. **Cache results** - Don't re-crawl unchanged pages
4. **Handle errors** - Retry with exponential backoff
5. **Clean output** - Remove nav, footer, ads

### CLI Examples

\`\`\`bash
# Using curl + html-to-markdown
curl -s "\${url}" | npx html-to-markdown

# Using Firecrawl CLI
npx firecrawl scrape "\${url}" --format markdown
\`\`\`
\`);
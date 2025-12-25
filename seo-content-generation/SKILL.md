# seo-content-generation

SERP analysis to publication-ready articles. SEO-optimized content with proper structure, meta tags, and keyword placement. Use when: writing blog posts, creating landing page copy, optimizing content for search.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`seo`, `content`, `writing`, `marketing`, `serp`, `keywords`

## MCP Dependencies
None specified

## Inputs
- `topic` (string) (required): Main topic or keyword
- `type` (string) (optional): Content type: blog, landing, product, comparison
- `length` (string) (optional): Length: short (500), medium (1000), long (2000+)

## Chain of Thought
1. Research SERP for target keyword. 2. Analyze competitor content structure. 3. Identify content gaps. 4. Create outline with H2/H3 structure. 5. Write with keyword density 1-2%. 6. Add meta description and title tag.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "seo-content-generation", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/seo-content-generation/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// SEO Content Generation Skill
const topic = inputs.topic;
const type = inputs.type || 'blog';
const length = inputs.length || 'medium';

console.log(\`## SEO Content Generation: \${topic}

### SERP Analysis Process

1. **Search Intent Analysis**
   - Informational: "how to", "what is"
   - Commercial: "best", "vs", "review"
   - Transactional: "buy", "pricing"

2. **Competitor Analysis**
   - Top 5 ranking articles
   - Word count
   - Heading structure
   - Featured snippets

### Content Structure Template (\${type})

\`\`\`markdown
# [Primary Keyword] - [Benefit/Hook]
<!-- Title: 50-60 characters -->

## Introduction (100-150 words)
- Hook with problem/question
- Establish credibility
- Preview what reader will learn

## [H2: Primary Subtopic]
### [H3: Supporting Point]
- Include primary keyword naturally
- Add internal links
- Use short paragraphs (2-3 sentences)

## [H2: Secondary Subtopic]
- Include related keywords
- Add examples/data
- Use bullet points

## Conclusion
- Summarize key points
- Clear CTA
- FAQ section for snippets
\`\`\`

### Meta Tags Template

\`\`\`html
<title>\${topic} - [Benefit] | [Brand] (50-60 chars)</title>
<meta name="description" content="[Action verb] \${topic}. 
  [Benefit]. [CTA]. (150-160 chars)" />
\`\`\`

### Keyword Placement

- Title tag: Primary keyword
- H1: Primary keyword (variation)
- First 100 words: Primary keyword
- H2s: Secondary keywords
- Image alt text: Descriptive with keyword
- URL slug: primary-keyword-here

### Content Length Guide

- Short (500w): Quick answers, definitions
- Medium (1000w): How-to guides, lists
- Long (2000w+): Comprehensive guides, pillar content

### Quality Checklist

- [ ] Unique angle (not rehashed content)
- [ ] Data/statistics included
- [ ] Internal links (2-3)
- [ ] External links to authority sources
- [ ] Images with alt text
- [ ] Mobile-readable paragraphs
- [ ] Clear CTAs
\`);
```

---
Created: Tue Dec 23 2025 00:32:50 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:32:50 GMT+0800 (Singapore Standard Time)

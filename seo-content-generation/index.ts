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
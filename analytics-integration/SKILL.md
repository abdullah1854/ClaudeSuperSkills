# analytics-integration

DataFast and Umami analytics integration. Event tracking, custom metrics, dashboards, and privacy-focused analytics. Use when: adding analytics, tracking events, setting up dashboards.

## Metadata
- **Version**: 1.0.0
- **Category**: api
- **Source**: workspace


## Tags
`analytics`, `tracking`, `umami`, `datafast`, `metrics`, `privacy`

## MCP Dependencies
None specified

## Inputs
- `provider` (string) (required): Provider: umami, datafast, plausible
- `feature` (string) (optional): Feature: setup, events, custom

## Chain of Thought
1. Select analytics provider. 2. Generate setup code. 3. Add event tracking patterns. 4. Configure custom metrics. 5. Ensure privacy compliance.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "analytics-integration", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/analytics-integration/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Analytics Integration Skill
const provider = inputs.provider || 'umami';

const analytics = {
  umami: `## Umami Analytics (Privacy-Focused)

### Setup (Next.js)
\`\`\`typescript
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script
          src="https://analytics.yoursite.com/script.js"
          data-website-id="your-website-id"
          strategy="afterInteractive"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
\`\`\`

### Event Tracking
\`\`\`typescript
// Track custom events
declare global {
  interface Window { umami: any; }
}

// Track button click
const trackPurchase = () => {
  window.umami?.track('purchase', { 
    product: 'pro-plan',
    value: 99 
  });
};
\`\`\`

### Self-Hosted Setup
\`\`\`bash
# Docker Compose
docker run -d \\
  -p 3000:3000 \\
  -e DATABASE_URL=postgresql://... \\
  ghcr.io/umami-software/umami:latest
\`\`\``,

  datafast: `## DataFast Analytics

### Setup
\`\`\`typescript
import { DataFast } from 'datafast';

const df = new DataFast({
  projectId: process.env.DATAFAST_PROJECT_ID,
});

// Track page view
df.track('pageview', { path: window.location.pathname });

// Track custom event
df.track('signup', { plan: 'pro', source: 'landing' });
\`\`\``,

  plausible: `## Plausible Analytics

### Setup
\`\`\`html
<script defer data-domain="yoursite.com" 
  src="https://plausible.io/js/script.js"></script>
\`\`\`

### Custom Events
\`\`\`typescript
// Track goal
plausible('Signup', { props: { plan: 'pro' } });
\`\`\``
};

console.log(analytics[provider] || analytics.umami);
```

---
Created: Tue Dec 23 2025 00:31:32 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:31:32 GMT+0800 (Singapore Standard Time)

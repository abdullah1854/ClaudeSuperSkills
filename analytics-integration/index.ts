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
# idea-to-product

SaaS validation, go-to-market strategy, and product development framework. Takes ideas from concept to launch. Use when: validating startup ideas, planning product launches, creating MVPs.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`saas`, `startup`, `validation`, `gtm`, `mvp`, `product`, `strategy`

## MCP Dependencies
None specified

## Inputs
- `idea` (string) (required): Product idea description
- `stage` (string) (optional): Stage: validate, build, launch, grow
- `market` (string) (optional): Target market/niche

## Chain of Thought
1. Validate problem exists. 2. Identify target customer. 3. Define MVP scope. 4. Plan go-to-market. 5. Set success metrics. 6. Create launch timeline.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "idea-to-product", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/idea-to-product/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Idea to Product Skill
const idea = inputs.idea;
const stage = inputs.stage || 'validate';

console.log(\`## Idea to Product: \${idea}

### Stage: \${stage.toUpperCase()}

---

## 1. VALIDATION PHASE

### Problem Validation
- [ ] Can you describe the problem in one sentence?
- [ ] Who experiences this problem daily?
- [ ] What's the current solution (even if manual)?
- [ ] Why is now the right time?

### Customer Discovery
\`\`\`
Target Customer Profile:
- Role: [Job title/role]
- Pain: [Specific pain point]
- Budget: [Willingness to pay]
- Access: [Where to find them]
\`\`\`

### Competitive Analysis
| Competitor | Strength | Weakness | Price |
|------------|----------|----------|-------|
| [Name] | | | |

---

## 2. BUILD PHASE

### MVP Definition
**Must Have (Week 1-2):**
- Core feature that solves main problem
- User authentication
- Basic UI

**Should Have (Week 3-4):**
- Secondary features
- Polish and UX improvements

**Won't Have (Future):**
- Nice-to-haves for v2

### Tech Stack Recommendation
\`\`\`
Frontend: Next.js + Tailwind + shadcn/ui
Backend: Next.js API routes or FastAPI
Database: Supabase or PlanetScale
Auth: Clerk or NextAuth
Payments: Stripe
Hosting: Vercel
\`\`\`

---

## 3. LAUNCH PHASE

### Pre-Launch (2 weeks before)
- [ ] Landing page with waitlist
- [ ] Social proof (testimonials/beta users)
- [ ] Launch copy and assets

### Launch Channels
1. **Product Hunt** - Prepare 2 weeks ahead
2. **Hacker News** - Show HN post
3. **Twitter/X** - Build in public thread
4. **Reddit** - Relevant subreddits
5. **Indie Hackers** - Launch post

### Launch Day Checklist
- [ ] Monitoring alerts set up
- [ ] Support channels ready
- [ ] Metrics dashboard live
- [ ] Team available for issues

---

## 4. GROW PHASE

### Key Metrics (North Star)
- Activation: First value moment
- Retention: Weekly active users
- Revenue: MRR growth

### Growth Levers
1. SEO content
2. Referral program
3. Integrations
4. Partnerships
\`);
```

---
Created: Tue Dec 23 2025 00:32:50 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:32:50 GMT+0800 (Singapore Standard Time)

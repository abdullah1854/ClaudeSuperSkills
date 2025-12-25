# payment-processing

Integration patterns for Stripe, Polar, and Dodo payment systems. Handles checkout flows, webhooks, subscriptions, and billing. Use when: implementing payments, setting up subscriptions, handling webhooks.

## Metadata
- **Version**: 1.0.0
- **Category**: api
- **Source**: workspace


## Tags
`payments`, `stripe`, `subscriptions`, `webhooks`, `billing`, `polar`, `dodo`

## MCP Dependencies
None specified

## Inputs
- `provider` (string) (required): Provider: stripe, polar, dodo
- `feature` (string) (required): Feature: checkout, webhook, subscription, portal
- `framework` (string) (optional): Framework: nextjs, express, fastapi

## Chain of Thought
1. Identify payment provider. 2. Select integration pattern. 3. Generate secure implementation. 4. Add webhook verification. 5. Include error handling. 6. Add testing guidance.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "payment-processing", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/payment-processing/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Payment Processing Skill
const provider = inputs.provider || 'stripe';
const feature = inputs.feature || 'checkout';

const integrations = {
  stripe: {
    checkout: `## Stripe Checkout (Next.js)

\`\`\`typescript
// app/api/checkout/route.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const { priceId } = await req.json();
  
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: \`\${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}\`,
    cancel_url: \`\${process.env.NEXT_PUBLIC_URL}/canceled\`,
  });
  
  return Response.json({ url: session.url });
}
\`\`\``,
    webhook: `## Stripe Webhook Handler

\`\`\`typescript
// app/api/webhook/route.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get('stripe-signature')!;
  
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body, sig, process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return new Response('Webhook Error', { status: 400 });
  }
  
  switch (event.type) {
    case 'checkout.session.completed':
      // Handle successful checkout
      break;
    case 'customer.subscription.updated':
      // Handle subscription changes
      break;
  }
  
  return new Response('OK');
}
\`\`\``
  },
  polar: {
    checkout: `## Polar.sh Integration

\`\`\`typescript
// Polar SDK setup
import { Polar } from '@polar-sh/sdk';

const polar = new Polar({ accessToken: process.env.POLAR_ACCESS_TOKEN });

// Create checkout
const checkout = await polar.checkouts.create({
  productId: 'prod_xxx',
  successUrl: 'https://yoursite.com/success',
});
\`\`\``,
    webhook: `## Polar Webhook

\`\`\`typescript
// Verify webhook signature
import { validateWebhookSignature } from '@polar-sh/sdk';

const isValid = validateWebhookSignature(
  payload, signature, process.env.POLAR_WEBHOOK_SECRET
);
\`\`\``
  }
};

const result = integrations[provider]?.[feature] || 'Provider/feature not found';
console.log(result);
```

---
Created: Tue Dec 23 2025 00:31:32 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:31:32 GMT+0800 (Singapore Standard Time)

# project-scaffold

Generates project structure templates for Next.js, Express, and FastAPI applications.

## Metadata
- **Version**: 1.0.0
- **Category**: devops
- **Source**: workspace


## Tags
`scaffold`, `project`, `template`

## MCP Dependencies
None specified

## Inputs
- `framework` (string) (required): Framework: nextjs, express, fastapi



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "project-scaffold", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/project-scaffold/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { framework } = inputs;

const structures = {
  nextjs: `nextjs-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   └── lib/
├── public/
├── package.json
├── tsconfig.json
├── next.config.js
└── .gitignore`,

  express: `express-api/
├── src/
│   ├── routes/
│   ├── middleware/
│   ├── services/
│   ├── types/
│   └── index.ts
├── package.json
├── tsconfig.json
├── .env.example
└── .gitignore`,

  fastapi: `fastapi-app/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── __init__.py
│   └── main.py
├── tests/
├── requirements.txt
├── pyproject.toml
└── .gitignore`
};

console.log(`# ${framework} Project Structure\n\n\`\`\`\n${structures[framework] || structures.nextjs}\n\`\`\``);

```

---
Created: Mon Dec 22 2025 10:37:26 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:26 GMT+0800 (Singapore Standard Time)

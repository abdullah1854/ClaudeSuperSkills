# refactor-suggest

Identifies code smells and suggests refactoring patterns like extract method, decompose conditional.

## Metadata
- **Version**: 1.0.0
- **Category**: code-quality
- **Source**: workspace


## Tags
`refactoring`, `code-quality`, `patterns`

## MCP Dependencies
None specified

## Inputs
- `smell` (string) (required): Code smell: long_function, deep_nesting, long_params, duplicate_code



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "refactor-suggest", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/refactor-suggest/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { smell } = inputs;

const patterns = {
  long_function: {
    name: 'Extract Method',
    description: 'Extract code block into separate method',
    example: `// Before
function process(data) {
  // 50+ lines of mixed logic
}

// After
function validate(data) { /* validation */ }
function transform(data) { /* transform */ }
function save(data) { /* save */ }

function process(data) {
  validate(data);
  const result = transform(data);
  save(result);
}`
  },
  deep_nesting: {
    name: 'Guard Clauses',
    description: 'Replace nested conditions with early returns',
    example: `// Before
if (user) {
  if (user.active) {
    if (user.hasPermission) {
      doSomething();
    }
  }
}

// After
if (!user) return;
if (!user.active) return;
if (!user.hasPermission) return;
doSomething();`
  },
  long_params: {
    name: 'Parameter Object',
    description: 'Group related parameters into object',
    example: `// Before
function createUser(name, email, phone, address, city, zip) {}

// After
function createUser(userInfo: UserInfo) {}`
  }
};

const p = patterns[smell] || patterns.long_function;
console.log(`# Refactoring: ${p.name}\n\n${p.description}\n\n\`\`\`javascript\n${p.example}\n\`\`\``);

```

---
Created: Mon Dec 22 2025 10:37:26 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:26 GMT+0800 (Singapore Standard Time)

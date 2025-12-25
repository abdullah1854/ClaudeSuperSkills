# chrome-data-extract

Generates JavaScript snippets for browser automation data extraction from tables, forms, lists.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`browser`, `automation`, `extraction`

## MCP Dependencies
None specified

## Inputs
- `type` (string) (required): Extraction type: table, form, list
- `selector` (string) (optional): CSS selector



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "chrome-data-extract", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/chrome-data-extract/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { type, selector = 'table' } = inputs;

const scripts = {
  table: `// Extract table data
const table = document.querySelector('${selector}');
const rows = Array.from(table.querySelectorAll('tr'));
const headers = Array.from(rows[0].querySelectorAll('th,td')).map(c => c.textContent.trim());

const data = rows.slice(1).map(row => {
  const cells = Array.from(row.querySelectorAll('td'));
  return Object.fromEntries(headers.map((h, i) => [h, cells[i]?.textContent?.trim()]));
});
console.log(JSON.stringify(data, null, 2));`,

  form: `// Extract form data
const form = document.querySelector('${selector}');
const formData = {};
form.querySelectorAll('input, select, textarea').forEach(el => {
  if (el.name) formData[el.name] = el.value;
});
console.log(JSON.stringify(formData, null, 2));`,

  list: `// Extract list items
const items = document.querySelectorAll('${selector}');
const data = Array.from(items).map(el => el.textContent.trim());
console.log(JSON.stringify(data, null, 2));`
};

console.log(scripts[type] || scripts.table);

```

---
Created: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)

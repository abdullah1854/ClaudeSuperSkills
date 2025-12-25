# maximo-helper

Generates Maximo database queries with mandatory GBE site filtering for work orders, assets, inventory.

## Metadata
- **Version**: 1.0.0
- **Category**: database
- **Source**: workspace


## Tags
`maximo`, `database`, `work-orders`, `assets`

## MCP Dependencies
None specified

## Inputs
- `table` (string) (required): Table: WORKORDER, ASSET, INVENTORY, LABOR, LABTRANS
- `filter` (string) (optional): Additional WHERE conditions



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "maximo-helper", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/maximo-helper/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { table, filter } = inputs;
const GBE = "SITEID = 'GBE'";

const schemas = {
  WORKORDER: ['WONUM', 'DESCRIPTION', 'STATUS', 'WORKTYPE', 'REPORTDATE', 'LOCATION', 'ASSETNUM'],
  ASSET: ['ASSETNUM', 'DESCRIPTION', 'STATUS', 'LOCATION', 'PARENT', 'SERIALNUM'],
  INVENTORY: ['ITEMNUM', 'STORELOC', 'CURBAL', 'AVGCOST', 'MINLEVEL'],
  LABOR: ['LABORCODE', 'DISPLAYNAME', 'STATUS', 'WORKSITE'],
  LABTRANS: ['LABTRANSID', 'LABORCODE', 'REFWO', 'STARTDATE', 'REGULARHRS']
};

const t = table.toUpperCase();
const cols = schemas[t] || ['*'];

let query = `SELECT TOP 100\n    ${cols.join(',\n    ')}\nFROM ${t}\nWHERE ${GBE}`;

if (filter) {
  query += `\n  AND ${filter}`;
}

query += ';';

console.log(`-- Maximo Query for ${t}\n-- ⚠️ ALWAYS filter by ${GBE}\n\n${query}`);

```

---
Created: Mon Dec 22 2025 10:35:19 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:35:19 GMT+0800 (Singapore Standard Time)

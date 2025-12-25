# database-query-guide

Routes queries to correct MSSQL servers and provides connection guidance.

## Metadata
- **Version**: 1.0.0
- **Category**: database
- **Source**: workspace


## Tags
`database`, `mssql`, `routing`

## MCP Dependencies
None specified

## Inputs
- `database` (string) (required): Database: maximo, ax, fabric, other
- `query` (string) (optional): Query to execute



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "database-query-guide", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/database-query-guide/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { database, query } = inputs;

const servers = {
  maximo: { server: 'MAXIMO-PROD', db: 'MAXIMO_DB', note: 'Always filter by SITEID = YOUR_SITE_ID' },
  ax: { server: 'AX-PROD', db: 'AX_LIVE_DB', note: 'Always filter by DATAAREAID' },
  fabric: { server: 'Fabric Lakehouse', db: 'Analytics', note: 'Use Spark SQL or Delta' }
};

const s = servers[database.toLowerCase()] || { server: 'UNKNOWN', db: database, note: 'Verify connection' };

let output = `# Database: ${database.toUpperCase()}\n\n`;
output += `**Server**: ${s.server}\n`;
output += `**Database**: ${s.db}\n`;
output += `**Note**: ⚠️ ${s.note}\n`;

if (query) {
  output += `\n## Query\n\`\`\`sql\n${query}\n\`\`\``;
}

console.log(output);

```

---
Created: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)

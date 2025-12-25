# ax-dynamics-helper

Generates Dynamics AX queries with DATAAREAID filtering for sales, purchasing, inventory.

## Metadata
- **Version**: 1.0.0
- **Category**: database
- **Source**: workspace


## Tags
`dynamics`, `ax`, `erp`, `database`

## MCP Dependencies
None specified

## Inputs
- `table` (string) (required): Table: SALESTABLE, SALESLINE, PURCHTABLE, INVENTTABLE, CUSTTABLE
- `dataareaid` (string) (optional): Company code (default: YOUR_COMPANY)



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "ax-dynamics-helper", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/ax-dynamics-helper/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { table, dataareaid = 'YOUR_COMPANY' } = inputs;

const schemas = {
  SALESTABLE: ['SALESID', 'CUSTACCOUNT', 'SALESSTATUS', 'CREATEDDATE', 'CURRENCYCODE'],
  SALESLINE: ['SALESID', 'LINENUM', 'ITEMID', 'SALESQTY', 'LINEAMOUNT'],
  PURCHTABLE: ['PURCHID', 'VENDACCOUNT', 'PURCHSTATUS', 'CREATEDDATE'],
  PURCHLINE: ['PURCHID', 'LINENUM', 'ITEMID', 'PURCHQTY', 'LINEAMOUNT'],
  INVENTTABLE: ['ITEMID', 'ITEMNAME', 'ITEMGROUPID', 'ITEMTYPE'],
  CUSTTABLE: ['ACCOUNTNUM', 'NAME', 'CURRENCY', 'CUSTGROUP'],
  VENDTABLE: ['ACCOUNTNUM', 'NAME', 'CURRENCY', 'VENDGROUP']
};

const t = table.toUpperCase();
const cols = schemas[t] || ['*'];

const query = `SELECT TOP 100
    ${cols.join(',\n    ')},
    DATAAREAID
FROM ${t}
WHERE DATAAREAID = '${dataareaid}';`;

console.log(`-- AX Dynamics Query for ${t}\n\n${query}`);

```

---
Created: Mon Dec 22 2025 10:35:19 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:35:19 GMT+0800 (Singapore Standard Time)

# fabric-helper

Generates Microsoft Fabric Lakehouse and Warehouse queries with Delta Lake and Spark SQL.

## Metadata
- **Version**: 1.0.0
- **Category**: database
- **Source**: workspace


## Tags
`fabric`, `delta`, `spark`, `lakehouse`

## MCP Dependencies
None specified

## Inputs
- `operation` (string) (required): Operation: read, write, merge, optimize
- `table` (string) (required): Table name



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "fabric-helper", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/fabric-helper/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { operation, table } = inputs;

const templates = {
  read: `# Read from Delta table
df = spark.read.format("delta").table("${table}")
df.show()`,

  write: `# Write to Delta table
(df
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("${table}")
)`,

  merge: `MERGE INTO ${table} AS target
USING source_table AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET target.value = source.value
WHEN NOT MATCHED THEN
    INSERT (id, value) VALUES (source.id, source.value);`,

  optimize: `-- Optimize table (compact small files)
OPTIMIZE ${table};

-- Z-ORDER for query performance
OPTIMIZE ${table} ZORDER BY (column1);

-- Vacuum old files
VACUUM ${table};`
};

console.log(templates[operation] || templates.read);

```

---
Created: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:37:27 GMT+0800 (Singapore Standard Time)

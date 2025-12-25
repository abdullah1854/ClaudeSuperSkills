
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

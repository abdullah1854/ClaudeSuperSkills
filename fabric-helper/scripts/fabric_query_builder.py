#!/usr/bin/env python3
"""
Fabric Helper - Microsoft Fabric Lakehouse and Warehouse query builder.
"""

import json
import sys
from typing import Optional


# Common Fabric table patterns
FABRIC_PATTERNS = {
    "lakehouse": {
        "prefix": "lakehouse_",
        "format": "delta",
        "path_pattern": "Tables/{schema}/{table}"
    },
    "warehouse": {
        "prefix": "dw_",
        "format": "sql",
        "path_pattern": "dbo.{table}"
    }
}


def generate_delta_read(
    table_name: str,
    schema: str = "default",
    columns: Optional[list[str]] = None,
    filter_condition: Optional[str] = None,
    limit: Optional[int] = None
) -> str:
    """Generate PySpark code to read from Delta table."""

    cols = "*" if not columns else ", ".join(f'"{c}"' for c in columns)

    code = f'''# Read from Delta table
df = spark.read.format("delta").table("{schema}.{table_name}")
'''

    if columns:
        code += f'\ndf = df.select({", ".join(f\'"{c}\'' for c in columns)})'

    if filter_condition:
        code += f'\ndf = df.filter("{filter_condition}")'

    if limit:
        code += f'\ndf = df.limit({limit})'

    code += '\ndf.show()'

    return code


def generate_delta_write(
    df_name: str,
    table_name: str,
    schema: str = "default",
    mode: str = "overwrite",
    partition_by: Optional[list[str]] = None
) -> str:
    """Generate PySpark code to write to Delta table."""

    partition = ""
    if partition_by:
        partition = f'.partitionBy({", ".join(f\'"{p}\'' for p in partition_by)})'

    return f'''# Write to Delta table
({df_name}
    .write
    .format("delta")
    .mode("{mode}"){partition}
    .saveAsTable("{schema}.{table_name}")
)
'''


def generate_spark_sql(
    query: str,
    result_var: str = "result_df"
) -> str:
    """Generate Spark SQL execution code."""
    # Escape quotes in query
    escaped_query = query.replace('"', '\\"')

    return f'''{result_var} = spark.sql("""
{query}
""")
{result_var}.show()
'''


def generate_merge_statement(
    target_table: str,
    source_table: str,
    merge_keys: list[str],
    update_columns: list[str],
    insert_columns: Optional[list[str]] = None
) -> str:
    """Generate Delta MERGE statement."""

    join_condition = " AND ".join([f"target.{k} = source.{k}" for k in merge_keys])
    update_set = ", ".join([f"target.{c} = source.{c}" for c in update_columns])

    if insert_columns is None:
        insert_columns = merge_keys + update_columns

    insert_cols = ", ".join(insert_columns)
    insert_vals = ", ".join([f"source.{c}" for c in insert_columns])

    return f"""MERGE INTO {target_table} AS target
USING {source_table} AS source
ON {join_condition}
WHEN MATCHED THEN
    UPDATE SET {update_set}
WHEN NOT MATCHED THEN
    INSERT ({insert_cols})
    VALUES ({insert_vals});
"""


def generate_time_travel_query(
    table_name: str,
    version: Optional[int] = None,
    timestamp: Optional[str] = None
) -> str:
    """Generate Delta time travel query."""

    if version is not None:
        return f"""-- Query table at specific version
SELECT * FROM {table_name} VERSION AS OF {version};

-- Or using PySpark:
df = spark.read.format("delta").option("versionAsOf", {version}).table("{table_name}")
"""
    elif timestamp:
        return f"""-- Query table at specific timestamp
SELECT * FROM {table_name} TIMESTAMP AS OF '{timestamp}';

-- Or using PySpark:
df = spark.read.format("delta").option("timestampAsOf", "{timestamp}").table("{table_name}")
"""

    return f"""-- Get table history
DESCRIBE HISTORY {table_name};
"""


def generate_optimize_commands(table_name: str) -> str:
    """Generate Delta OPTIMIZE and VACUUM commands."""
    return f"""-- Optimize table (compact small files)
OPTIMIZE {table_name};

-- Optimize with Z-ORDER on frequently filtered columns
OPTIMIZE {table_name} ZORDER BY (column1, column2);

-- Vacuum old files (default 7 days retention)
VACUUM {table_name};

-- Vacuum with custom retention (use with caution)
-- SET spark.databricks.delta.retentionDurationCheck.enabled = false;
-- VACUUM {table_name} RETAIN 0 HOURS;
"""


def generate_warehouse_query(
    table_name: str,
    columns: Optional[list[str]] = None,
    where_clause: Optional[str] = None,
    order_by: Optional[str] = None,
    top: Optional[int] = None
) -> str:
    """Generate Fabric Warehouse SQL query."""

    cols = "*" if not columns else ", ".join(columns)
    top_clause = f"TOP {top} " if top else ""

    query = f"""SELECT {top_clause}{cols}
FROM dbo.{table_name}"""

    if where_clause:
        query += f"\nWHERE {where_clause}"

    if order_by:
        query += f"\nORDER BY {order_by}"

    return query + ";"


def generate_create_table(
    table_name: str,
    columns: dict[str, str],
    table_type: str = "delta"
) -> str:
    """Generate CREATE TABLE statement."""

    col_defs = ",\n    ".join([f"{name} {dtype}" for name, dtype in columns.items()])

    if table_type == "delta":
        return f"""CREATE TABLE IF NOT EXISTS {table_name} (
    {col_defs}
)
USING DELTA;
"""
    else:
        return f"""CREATE TABLE dbo.{table_name} (
    {col_defs}
);
"""


def generate_shortcut_creation(
    shortcut_name: str,
    source_path: str,
    source_type: str = "adls"
) -> str:
    """Generate shortcut creation guidance."""
    return f"""-- Create shortcut in Fabric Lakehouse
-- Shortcut Name: {shortcut_name}
-- Source Type: {source_type.upper()}
-- Source Path: {source_path}

-- Shortcuts are created via Fabric UI:
-- 1. Open Lakehouse
-- 2. Right-click Tables or Files
-- 3. Select "New shortcut"
-- 4. Choose {source_type.upper()} as source
-- 5. Enter path: {source_path}
-- 6. Name: {shortcut_name}

-- After creation, access via:
SELECT * FROM {shortcut_name} LIMIT 10;
"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--read":
            table = sys.argv[2] if len(sys.argv) > 2 else "my_table"
            print(generate_delta_read(table))

        elif cmd == "--write":
            print(generate_delta_write("df", "output_table"))

        elif cmd == "--merge":
            print(generate_merge_statement(
                "target_table",
                "source_table",
                ["id"],
                ["name", "value", "updated_at"]
            ))

        elif cmd == "--history":
            table = sys.argv[2] if len(sys.argv) > 2 else "my_table"
            print(generate_time_travel_query(table))

        elif cmd == "--optimize":
            table = sys.argv[2] if len(sys.argv) > 2 else "my_table"
            print(generate_optimize_commands(table))

        elif cmd == "--warehouse":
            table = sys.argv[2] if len(sys.argv) > 2 else "my_table"
            print(generate_warehouse_query(table, top=100))
    else:
        print("Fabric Helper - Query Builder")
        print("Usage:")
        print("  --read [table]      Generate Delta read")
        print("  --write             Generate Delta write")
        print("  --merge             Generate MERGE statement")
        print("  --history [table]   Generate time travel query")
        print("  --optimize [table]  Generate OPTIMIZE commands")
        print("  --warehouse [table] Generate Warehouse query")

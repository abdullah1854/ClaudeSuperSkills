#!/usr/bin/env python3
"""
Maximo Query Builder - Generates SQL queries for IBM Maximo tables.
"""

import json
import sys
from typing import Optional


# Maximo table schemas
MAXIMO_TABLES = {
    "WORKORDER": {
        "description": "Work orders",
        "key_columns": ["WONUM", "SITEID"],
        "common_columns": ["DESCRIPTION", "STATUS", "WORKTYPE", "REPORTDATE", "SCHEDSTART", "TARGCOMPDATE", "ACTFINISH", "LOCATION", "ASSETNUM"],
        "status_field": "STATUS"
    },
    "ASSET": {
        "description": "Assets/Equipment",
        "key_columns": ["ASSETNUM", "SITEID"],
        "common_columns": ["DESCRIPTION", "STATUS", "LOCATION", "PARENT", "ASSETTYPE", "SERIALNUM", "MANUFACTURER"],
        "status_field": "STATUS"
    },
    "LOCATIONS": {
        "description": "Locations",
        "key_columns": ["LOCATION", "SITEID"],
        "common_columns": ["DESCRIPTION", "STATUS", "TYPE", "PARENT"],
        "status_field": "STATUS"
    },
    "INVENTORY": {
        "description": "Inventory items",
        "key_columns": ["ITEMNUM", "ITEMSETID", "SITEID", "STORELOC"],
        "common_columns": ["CURBAL", "AVGCOST", "LASTISSUEDATE", "MINLEVEL", "ORDERQTY"],
        "status_field": None
    },
    "ITEM": {
        "description": "Item master",
        "key_columns": ["ITEMNUM", "ITEMSETID"],
        "common_columns": ["DESCRIPTION", "ROTATING", "ITEMTYPE", "ORDERUNIT", "ISSUEUNIT"],
        "status_field": None
    },
    "LABOR": {
        "description": "Labor records",
        "key_columns": ["LABORCODE", "ORGID"],
        "common_columns": ["DISPLAYNAME", "STATUS", "LABORCRAFTRATE", "WORKSITE"],
        "status_field": "STATUS"
    },
    "LABTRANS": {
        "description": "Labor transactions",
        "key_columns": ["LABTRANSID", "SITEID"],
        "common_columns": ["LABORCODE", "REFWO", "TRANSTYPE", "STARTDATE", "FINISHDATE", "REGULARHRS"],
        "status_field": None
    },
    "MATUSETRANS": {
        "description": "Material usage transactions",
        "key_columns": ["MATUSETRANSID", "SITEID"],
        "common_columns": ["REFWO", "ITEMNUM", "QUANTITY", "TRANSDATE", "STORELOC"],
        "status_field": None
    },
    "PERSON": {
        "description": "Person records",
        "key_columns": ["PERSONID"],
        "common_columns": ["DISPLAYNAME", "STATUS", "PRIMARYEMAIL", "PRIMARYPHONE"],
        "status_field": "STATUS"
    },
    "WOSTATUS": {
        "description": "Work order status history",
        "key_columns": ["WOSTATUSID"],
        "common_columns": ["WONUM", "SITEID", "STATUS", "CHANGEDATE", "CHANGEBY"],
        "status_field": None
    }
}


# GBE site filter - ALWAYS required
GBE_FILTER = "SITEID = 'GBE'"


def build_select_query(
    table: str,
    columns: Optional[list[str]] = None,
    site_filter: bool = True,
    where_clause: Optional[str] = None,
    order_by: Optional[str] = None,
    top: Optional[int] = None
) -> str:
    """Build a SELECT query for a Maximo table."""

    table_upper = table.upper()
    if table_upper not in MAXIMO_TABLES:
        return f"-- Warning: Unknown table {table}. Verify table exists in Maximo."

    schema = MAXIMO_TABLES[table_upper]

    # Default to key + common columns
    if columns is None:
        columns = schema["key_columns"] + schema["common_columns"]

    columns_str = ",\n    ".join(columns)
    top_clause = f"TOP {top} " if top else ""

    query = f"""SELECT {top_clause}
    {columns_str}
FROM {table_upper}"""

    where_parts = []
    if site_filter and "SITEID" in schema["key_columns"]:
        where_parts.append(GBE_FILTER)

    if where_clause:
        where_parts.append(where_clause)

    if where_parts:
        query += "\nWHERE " + "\n  AND ".join(where_parts)

    if order_by:
        query += f"\nORDER BY {order_by}"

    return query + ";"


def get_work_orders(
    status: Optional[str] = None,
    worktype: Optional[str] = None,
    location: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    top: int = 100
) -> str:
    """Get work orders with common filters."""

    where_parts = []

    if status:
        where_parts.append(f"STATUS = '{status}'")
    if worktype:
        where_parts.append(f"WORKTYPE = '{worktype}'")
    if location:
        where_parts.append(f"LOCATION = '{location}'")
    if date_from:
        where_parts.append(f"REPORTDATE >= '{date_from}'")
    if date_to:
        where_parts.append(f"REPORTDATE <= '{date_to}'")

    where_clause = " AND ".join(where_parts) if where_parts else None

    return build_select_query(
        "WORKORDER",
        where_clause=where_clause,
        order_by="REPORTDATE DESC",
        top=top
    )


def get_asset_hierarchy(asset_num: str) -> str:
    """Get asset with parent hierarchy."""
    return f"""-- Asset Hierarchy for {asset_num}
WITH AssetHierarchy AS (
    SELECT
        ASSETNUM,
        DESCRIPTION,
        PARENT,
        LOCATION,
        0 as Level
    FROM ASSET
    WHERE ASSETNUM = '{asset_num}'
        AND {GBE_FILTER}

    UNION ALL

    SELECT
        a.ASSETNUM,
        a.DESCRIPTION,
        a.PARENT,
        a.LOCATION,
        h.Level + 1
    FROM ASSET a
    INNER JOIN AssetHierarchy h ON a.ASSETNUM = h.PARENT
    WHERE a.{GBE_FILTER}
)
SELECT * FROM AssetHierarchy
ORDER BY Level;
"""


def get_labor_hours_by_workorder(wonum: str) -> str:
    """Get labor hours for a work order."""
    return f"""-- Labor Hours for Work Order {wonum}
SELECT
    lt.LABORCODE,
    l.DISPLAYNAME,
    SUM(lt.REGULARHRS) as TOTAL_REGULAR_HRS,
    SUM(lt.PREMIUMPAYHOURS) as TOTAL_PREMIUM_HRS,
    COUNT(*) as TRANSACTION_COUNT
FROM LABTRANS lt
INNER JOIN LABOR l ON lt.LABORCODE = l.LABORCODE
WHERE lt.REFWO = '{wonum}'
    AND lt.{GBE_FILTER}
GROUP BY lt.LABORCODE, l.DISPLAYNAME
ORDER BY TOTAL_REGULAR_HRS DESC;
"""


def get_material_usage_by_workorder(wonum: str) -> str:
    """Get material usage for a work order."""
    return f"""-- Material Usage for Work Order {wonum}
SELECT
    mt.ITEMNUM,
    i.DESCRIPTION,
    SUM(mt.QUANTITY) as TOTAL_QTY,
    mt.STORELOC,
    SUM(mt.LINECOST) as TOTAL_COST
FROM MATUSETRANS mt
INNER JOIN ITEM i ON mt.ITEMNUM = i.ITEMNUM
WHERE mt.REFWO = '{wonum}'
    AND mt.{GBE_FILTER}
GROUP BY mt.ITEMNUM, i.DESCRIPTION, mt.STORELOC
ORDER BY TOTAL_COST DESC;
"""


def get_inventory_levels(
    storeloc: Optional[str] = None,
    below_min: bool = False
) -> str:
    """Get inventory levels."""

    where_parts = [GBE_FILTER]
    if storeloc:
        where_parts.append(f"STORELOC = '{storeloc}'")
    if below_min:
        where_parts.append("CURBAL < MINLEVEL")

    return f"""-- Inventory Levels
SELECT
    inv.ITEMNUM,
    i.DESCRIPTION,
    inv.STORELOC,
    inv.CURBAL,
    inv.MINLEVEL,
    inv.ORDERQTY,
    inv.AVGCOST,
    inv.CURBAL * inv.AVGCOST as INVENTORY_VALUE
FROM INVENTORY inv
INNER JOIN ITEM i ON inv.ITEMNUM = i.ITEMNUM
WHERE {' AND '.join(where_parts)}
ORDER BY inv.STORELOC, inv.ITEMNUM;
"""


def get_work_order_status_history(wonum: str) -> str:
    """Get work order status change history."""
    return f"""-- Status History for Work Order {wonum}
SELECT
    ws.STATUS,
    ws.CHANGEDATE,
    ws.CHANGEBY,
    p.DISPLAYNAME as CHANGED_BY_NAME
FROM WOSTATUS ws
LEFT JOIN PERSON p ON ws.CHANGEBY = p.PERSONID
WHERE ws.WONUM = '{wonum}'
    AND ws.{GBE_FILTER}
ORDER BY ws.CHANGEDATE DESC;
"""


def list_tables() -> str:
    """List all known Maximo tables."""
    output = "Available Maximo Tables:\n" + "=" * 50 + "\n"
    output += f"\n⚠️  IMPORTANT: Always filter by {GBE_FILTER}\n\n"

    for table, info in MAXIMO_TABLES.items():
        output += f"\n{table}\n  {info['description']}\n"
        output += f"  Keys: {', '.join(info['key_columns'])}\n"

    return output


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--tables":
            print(list_tables())

        elif cmd == "--workorders":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            print(get_work_orders(status=status))

        elif cmd == "--asset" and len(sys.argv) > 2:
            print(get_asset_hierarchy(sys.argv[2]))

        elif cmd == "--labor" and len(sys.argv) > 2:
            print(get_labor_hours_by_workorder(sys.argv[2]))

        elif cmd == "--materials" and len(sys.argv) > 2:
            print(get_material_usage_by_workorder(sys.argv[2]))

        elif cmd == "--inventory":
            storeloc = sys.argv[2] if len(sys.argv) > 2 else None
            print(get_inventory_levels(storeloc=storeloc))

        elif cmd == "--status" and len(sys.argv) > 2:
            print(get_work_order_status_history(sys.argv[2]))

        elif cmd == "--select" and len(sys.argv) > 2:
            print(build_select_query(sys.argv[2], top=100))

    else:
        print("Maximo Query Builder")
        print("Usage:")
        print("  --tables                 List all known tables")
        print("  --workorders [status]    Get work orders")
        print("  --asset <assetnum>       Get asset hierarchy")
        print("  --labor <wonum>          Get labor hours")
        print("  --materials <wonum>      Get material usage")
        print("  --inventory [storeloc]   Get inventory levels")
        print("  --status <wonum>         Get status history")
        print("  --select <table>         Generate SELECT for table")

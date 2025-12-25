#!/usr/bin/env python3
"""
AX Dynamics Query Builder - Generates SQL queries for Dynamics AX tables.
"""

import json
import sys
from typing import Optional


# AX table schemas
AX_TABLES = {
    "CUSTTABLE": {
        "description": "Customer master data",
        "key_columns": ["ACCOUNTNUM", "DATAAREAID"],
        "common_columns": ["NAME", "CURRENCY", "CUSTGROUP", "PAYMTERMID", "BLOCKED"]
    },
    "VENDTABLE": {
        "description": "Vendor master data",
        "key_columns": ["ACCOUNTNUM", "DATAAREAID"],
        "common_columns": ["NAME", "CURRENCY", "VENDGROUP", "PAYMTERMID", "BLOCKED"]
    },
    "INVENTTABLE": {
        "description": "Item master data",
        "key_columns": ["ITEMID", "DATAAREAID"],
        "common_columns": ["ITEMNAME", "ITEMGROUPID", "ITEMTYPE", "UNITID"]
    },
    "INVENTTRANS": {
        "description": "Inventory transactions",
        "key_columns": ["RECID", "DATAAREAID"],
        "common_columns": ["ITEMID", "QTY", "DATEPHYSICAL", "STATUSRECEIPT", "STATUSISSUE"]
    },
    "SALESTABLE": {
        "description": "Sales order headers",
        "key_columns": ["SALESID", "DATAAREAID"],
        "common_columns": ["CUSTACCOUNT", "SALESSTATUS", "CREATEDDATE", "CURRENCYCODE"]
    },
    "SALESLINE": {
        "description": "Sales order lines",
        "key_columns": ["RECID", "DATAAREAID"],
        "common_columns": ["SALESID", "ITEMID", "SALESQTY", "SALESUNIT", "LINEAMOUNT"]
    },
    "PURCHTABLE": {
        "description": "Purchase order headers",
        "key_columns": ["PURCHID", "DATAAREAID"],
        "common_columns": ["VENDACCOUNT", "PURCHSTATUS", "CREATEDDATE", "CURRENCYCODE"]
    },
    "PURCHLINE": {
        "description": "Purchase order lines",
        "key_columns": ["RECID", "DATAAREAID"],
        "common_columns": ["PURCHID", "ITEMID", "PURCHQTY", "PURCHUNIT", "LINEAMOUNT"]
    },
    "LEDGERJOURNALTABLE": {
        "description": "General ledger journal headers",
        "key_columns": ["JOURNALNUM", "DATAAREAID"],
        "common_columns": ["JOURNALNAME", "POSTED", "JOURNALTYPE"]
    },
    "LEDGERJOURNALTRANS": {
        "description": "General ledger journal lines",
        "key_columns": ["RECID", "DATAAREAID"],
        "common_columns": ["JOURNALNUM", "ACCOUNTNUM", "AMOUNTCURDEBIT", "AMOUNTCURCREDIT"]
    }
}


def build_select_query(
    table: str,
    columns: Optional[list[str]] = None,
    dataareaid: str = "YOUR_COMPANY",
    where_clause: Optional[str] = None,
    order_by: Optional[str] = None,
    top: Optional[int] = None
) -> str:
    """Build a SELECT query for an AX table."""

    table_upper = table.upper()
    if table_upper not in AX_TABLES:
        return f"-- Warning: Unknown table {table}. Verify table exists in AX."

    # Default to all common columns plus keys
    if columns is None:
        schema = AX_TABLES[table_upper]
        columns = schema["key_columns"] + schema["common_columns"]

    columns_str = ",\n    ".join(columns)
    top_clause = f"TOP {top} " if top else ""

    query = f"""SELECT {top_clause}
    {columns_str}
FROM {table_upper}
WHERE DATAAREAID = '{dataareaid}'"""

    if where_clause:
        query += f"\n  AND {where_clause}"

    if order_by:
        query += f"\nORDER BY {order_by}"

    return query


def build_join_query(
    main_table: str,
    join_table: str,
    join_columns: list[tuple[str, str]],
    select_columns: Optional[dict[str, list[str]]] = None,
    dataareaid: str = "YOUR_COMPANY",
    where_clause: Optional[str] = None
) -> str:
    """Build a JOIN query between two AX tables."""

    main_alias = main_table[0].lower()
    join_alias = join_table[0].lower() + "2" if main_table[0].lower() == join_table[0].lower() else join_table[0].lower()

    # Build column list
    if select_columns:
        cols = []
        for alias, columns in select_columns.items():
            for col in columns:
                cols.append(f"{alias}.{col}")
        columns_str = ",\n    ".join(cols)
    else:
        columns_str = f"{main_alias}.*"

    # Build join condition
    join_conditions = [f"{main_alias}.{c1} = {join_alias}.{c2}" for c1, c2 in join_columns]
    join_str = " AND ".join(join_conditions)

    query = f"""SELECT
    {columns_str}
FROM {main_table.upper()} {main_alias}
INNER JOIN {join_table.upper()} {join_alias}
    ON {join_str}
    AND {join_alias}.DATAAREAID = '{dataareaid}'
WHERE {main_alias}.DATAAREAID = '{dataareaid}'"""

    if where_clause:
        query += f"\n  AND {where_clause}"

    return query


def get_sales_order_details(salesid: str, dataareaid: str = "YOUR_COMPANY") -> str:
    """Get sales order with line items."""
    return f"""-- Sales Order Details
SELECT
    h.SALESID,
    h.CUSTACCOUNT,
    h.SALESSTATUS,
    h.CREATEDDATE,
    l.LINENUM,
    l.ITEMID,
    l.SALESQTY,
    l.SALESUNIT,
    l.SALESPRICE,
    l.LINEAMOUNT
FROM SALESTABLE h
INNER JOIN SALESLINE l
    ON h.SALESID = l.SALESID
    AND l.DATAAREAID = '{dataareaid}'
WHERE h.DATAAREAID = '{dataareaid}'
    AND h.SALESID = '{salesid}'
ORDER BY l.LINENUM;"""


def get_purchase_order_details(purchid: str, dataareaid: str = "YOUR_COMPANY") -> str:
    """Get purchase order with line items."""
    return f"""-- Purchase Order Details
SELECT
    h.PURCHID,
    h.VENDACCOUNT,
    h.PURCHSTATUS,
    h.CREATEDDATE,
    l.LINENUM,
    l.ITEMID,
    l.PURCHQTY,
    l.PURCHUNIT,
    l.PURCHPRICE,
    l.LINEAMOUNT
FROM PURCHTABLE h
INNER JOIN PURCHLINE l
    ON h.PURCHID = l.PURCHID
    AND l.DATAAREAID = '{dataareaid}'
WHERE h.DATAAREAID = '{dataareaid}'
    AND h.PURCHID = '{purchid}'
ORDER BY l.LINENUM;"""


def get_inventory_on_hand(itemid: Optional[str] = None, dataareaid: str = "YOUR_COMPANY") -> str:
    """Get inventory on-hand query."""
    item_filter = f"AND i.ITEMID = '{itemid}'" if itemid else ""
    return f"""-- Inventory On-Hand
SELECT
    i.ITEMID,
    i.ITEMNAME,
    SUM(CASE WHEN t.STATUSRECEIPT = 1 THEN t.QTY ELSE 0 END) as QTY_RECEIVED,
    SUM(CASE WHEN t.STATUSISSUE = 1 THEN t.QTY ELSE 0 END) as QTY_ISSUED,
    SUM(t.QTY) as QTY_ONHAND
FROM INVENTTABLE i
LEFT JOIN INVENTTRANS t
    ON i.ITEMID = t.ITEMID
    AND t.DATAAREAID = '{dataareaid}'
WHERE i.DATAAREAID = '{dataareaid}'
    {item_filter}
GROUP BY i.ITEMID, i.ITEMNAME
HAVING SUM(t.QTY) <> 0
ORDER BY i.ITEMID;"""


def list_tables() -> str:
    """List all known AX tables."""
    output = "Available AX Tables:\n" + "=" * 50 + "\n"
    for table, info in AX_TABLES.items():
        output += f"\n{table}\n  {info['description']}\n"
        output += f"  Keys: {', '.join(info['key_columns'])}\n"
    return output


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "--tables":
            print(list_tables())
        elif cmd == "--sales" and len(sys.argv) > 2:
            print(get_sales_order_details(sys.argv[2]))
        elif cmd == "--purchase" and len(sys.argv) > 2:
            print(get_purchase_order_details(sys.argv[2]))
        elif cmd == "--inventory":
            itemid = sys.argv[2] if len(sys.argv) > 2 else None
            print(get_inventory_on_hand(itemid))
        elif cmd == "--select" and len(sys.argv) > 2:
            print(build_select_query(sys.argv[2], top=100))
    else:
        print("AX Dynamics Query Builder")
        print("Usage:")
        print("  --tables              List all known tables")
        print("  --sales <salesid>     Get sales order details")
        print("  --purchase <purchid>  Get purchase order details")
        print("  --inventory [itemid]  Get inventory on-hand")
        print("  --select <table>      Generate SELECT for table")

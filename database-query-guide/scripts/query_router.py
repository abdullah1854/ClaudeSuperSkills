"""
Database Query Router

Routes queries to appropriate server and formats with required statements.

Usage:
    python query_router.py --domain maximo --query "SELECT * FROM WORKORDER"
"""

from typing import Dict, Optional, Tuple
import argparse
import re


# Server routing configuration
SERVER_CONFIG = {
    "maximo": {
        "server": "mssql-prod",
        "tool": "mssql_prod_execute_query",
        "use_statement": "USE MAXDB76;",
        "required_filter": "siteid = 'GBE'",
    },
    "ax": {
        "server": "mssql-prod",
        "tool": "mssql_prod_execute_query",
        "use_statement": "USE AX_GB_LIVE_60;",
        "required_filter": "DATAAREAID = 'GBE'",
    },
    "commission": {
        "server": "mssql-prod",
        "tool": "mssql_prod_execute_query",
        "use_statement": "USE COMMISSION;",
        "required_filter": None,
    },
    "crm_dev": {
        "server": "mssql-crm-dev",
        "tool": "mssql_crm_dev_execute_query",
        "use_statement": None,
        "required_filter": None,
    },
    "crm_prod": {
        "server": "mssql-crm-prod",
        "tool": "mssql_crm_prod_execute_query",
        "use_statement": None,
        "required_filter": None,
        "read_only": True,
    },
    "corpforms": {
        "server": "mssql-corpforms",
        "tool": "mssql_corpforms_execute_query",
        "use_statement": None,
        "required_filter": None,
    },
}


def detect_domain(query: str) -> Optional[str]:
    """
    Detect the data domain from query content.

    Returns domain name or None if unable to detect.
    """
    query_upper = query.upper()

    # Maximo tables
    maximo_tables = ["WORKORDER", "ASSET", "LABOR", "INVENTORY", "MATUSETRANS"]
    if any(t in query_upper for t in maximo_tables):
        return "maximo"

    # AX tables
    ax_tables = ["LEDGERJOURNALTABLE", "INVENTTABLE", "SALESTABLE", "CUSTTABLE", "VENDTABLE"]
    if any(t in query_upper for t in ax_tables):
        return "ax"

    # Commission indicators
    if "COMMISSION" in query_upper:
        return "commission"

    return None


def validate_query(query: str, config: Dict) -> Tuple[bool, str]:
    """
    Validate query against domain requirements.

    Returns (is_valid, message).
    """
    query_upper = query.upper()

    # Check for write operations on read-only server
    if config.get("read_only"):
        write_ops = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER"]
        for op in write_ops:
            if op in query_upper:
                return False, f"Server is READ-ONLY. {op} operations not permitted."

    # Check for required filter
    required_filter = config.get("required_filter")
    if required_filter:
        filter_column = required_filter.split("=")[0].strip()
        if filter_column.upper() not in query_upper:
            return False, f"Missing required filter: {required_filter}"

    return True, "Query validated successfully"


def format_query(query: str, domain: str) -> str:
    """
    Format query with USE statement and validate filters.

    Args:
        query: Original SQL query
        domain: Data domain (maximo, ax, etc.)

    Returns:
        Formatted query with USE statement
    """
    config = SERVER_CONFIG.get(domain)
    if not config:
        raise ValueError(f"Unknown domain: {domain}")

    # Validate query
    is_valid, message = validate_query(query, config)
    if not is_valid:
        raise ValueError(message)

    # Add USE statement if required
    use_stmt = config.get("use_statement")
    if use_stmt:
        # Check if USE already present
        if not query.strip().upper().startswith("USE"):
            query = f"{use_stmt}\n{query}"

    return query


def get_routing_info(domain: str) -> Dict:
    """Get routing information for a domain."""
    config = SERVER_CONFIG.get(domain)
    if not config:
        raise ValueError(f"Unknown domain: {domain}")

    return {
        "server": config["server"],
        "tool": config["tool"],
        "use_statement": config.get("use_statement"),
        "required_filter": config.get("required_filter"),
        "read_only": config.get("read_only", False),
    }


def route_query(query: str, domain: Optional[str] = None) -> Dict:
    """
    Route a query to the appropriate server.

    Args:
        query: SQL query to execute
        domain: Optional domain override (auto-detected if not provided)

    Returns:
        Dictionary with server, tool, and formatted query
    """
    # Auto-detect domain if not provided
    if not domain:
        domain = detect_domain(query)
        if not domain:
            raise ValueError("Could not detect domain. Specify domain explicitly.")

    config = SERVER_CONFIG.get(domain)
    if not config:
        raise ValueError(f"Unknown domain: {domain}")

    formatted_query = format_query(query, domain)

    return {
        "domain": domain,
        "server": config["server"],
        "tool": config["tool"],
        "query": formatted_query,
        "read_only": config.get("read_only", False),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Route database queries")
    parser.add_argument("--domain", choices=list(SERVER_CONFIG.keys()),
                        help="Data domain")
    parser.add_argument("--query", required=True, help="SQL query")

    args = parser.parse_args()

    try:
        result = route_query(args.query, args.domain)
        print(f"Server: {result['server']}")
        print(f"Tool: {result['tool']}")
        print(f"Read-Only: {result['read_only']}")
        print(f"\nFormatted Query:\n{result['query']}")
    except ValueError as e:
        print(f"Error: {e}")

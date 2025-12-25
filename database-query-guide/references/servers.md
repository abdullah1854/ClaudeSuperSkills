# Database Server Reference

## Server Overview

### db-prod (Production Multi-Database Server)

**Purpose**: Primary production server hosting Maximo, AX, and Commission databases

**Databases**:
- `MAXIMO_DB` - Maximo Asset Management
- `AX_LIVE_DB` - Microsoft Dynamics AX ERP
- `COMMISSION_DB` - Commission processing

**Access Pattern**:
```sql
USE MAXIMO_DB;
-- Query here
```

**Key Considerations**:
- Always start with USE statement
- Apply site/entity filters
- Use TOP N for large tables

### db-crm-dev (CRM Development)

**Purpose**: CRM development and testing environment

**Access Pattern**: Direct query, no USE statement required

**Key Considerations**:
- Safe for testing queries
- Data may differ from production
- Full read/write access

### db-crm-prod (CRM Production)

**Purpose**: Production CRM data

**Access Pattern**: Direct query, no USE statement required

**Key Considerations**:
- READ-ONLY access
- No INSERT/UPDATE/DELETE operations
- Production data - handle with care

### db-corpforms (Corporate Forms)

**Purpose**: Corporate forms and document management

**Access Pattern**: Direct query, no USE statement required

## Common Query Patterns

### Cross-Database Query (db-prod)
```sql
-- Query across databases on same server
SELECT m.wonum, a.ITEMID
FROM MAXIMO_DB.dbo.WORKORDER m
JOIN AX_LIVE_DB.dbo.INVENTTABLE a
ON m.itemnum = a.ITEMID
WHERE m.siteid = 'YOUR_SITE_ID' AND a.DATAAREAID = 'YOUR_COMPANY';
```

### Schema Discovery
```sql
USE MAXIMO_DB;
-- List all tables
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';

-- List columns for a table
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'WORKORDER';
```

### Performance Optimization
```sql
-- Add WITH (NOLOCK) for read-only queries on busy tables
SELECT TOP 100 *
FROM WORKORDER WITH (NOLOCK)
WHERE siteid = 'YOUR_SITE_ID' AND status = 'COMP';
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid object name | Missing USE statement | Add USE [database]; |
| Invalid column name | Column doesn't exist | Verify with INFORMATION_SCHEMA |
| Login failed | Permission issue | Check credentials and access |
| Timeout | Query too expensive | Add WHERE clauses, use TOP N |

# Maximo Database Schema Reference

## WORKORDER Table

Primary table for maintenance work orders and tasks.

| Column | Type | Description |
|--------|------|-------------|
| wonum | VARCHAR | Work order number (primary key) |
| siteid | VARCHAR | Site identifier (use 'GBE') |
| description | VARCHAR | Work order description |
| status | VARCHAR | Current status (WAPPR, APPR, INPRG, COMP, CLOSE, CAN) |
| worktype | VARCHAR | Type of work |
| assetnum | VARCHAR | Related asset number |
| location | VARCHAR | Work location |
| reportdate | DATETIME | Date reported |
| schedstart | DATETIME | Scheduled start |
| actstart | DATETIME | Actual start |
| actfinish | DATETIME | Actual finish |
| owner | VARCHAR | Owner/supervisor |
| lead | VARCHAR | Lead technician |

## ASSET Table

Equipment and vehicle master data.

| Column | Type | Description |
|--------|------|-------------|
| assetnum | VARCHAR | Asset number (primary key) |
| siteid | VARCHAR | Site identifier (use 'GBE') |
| description | VARCHAR | Asset description |
| status | VARCHAR | Asset status |
| assettype | VARCHAR | Type classification |
| location | VARCHAR | Current location |
| serialnum | VARCHAR | Serial number |
| manufacturer | VARCHAR | Manufacturer name |
| vendor | VARCHAR | Vendor name |
| purchaseprice | DECIMAL | Purchase price |
| installdate | DATETIME | Installation date |
| gb_assetregistrationno | VARCHAR | Vehicle plate number |
| gb_branch | VARCHAR | Branch location |
| gb_department | VARCHAR | Department |

## INVENTORY Table

Spare parts and inventory items.

| Column | Type | Description |
|--------|------|-------------|
| itemnum | VARCHAR | Item number (primary key) |
| siteid | VARCHAR | Site identifier |
| storeloc | VARCHAR | Storage location |
| binnum | VARCHAR | Bin number |
| curbal | DECIMAL | Current balance |
| minlevel | DECIMAL | Minimum stock level |
| maxlevel | DECIMAL | Maximum stock level |
| orderqty | DECIMAL | Order quantity |
| issueunit | VARCHAR | Issue unit of measure |
| avgcost | DECIMAL | Average cost |
| lastissuedate | DATETIME | Last issue date |

## LABOR Table

Technician and labor resource data.

| Column | Type | Description |
|--------|------|-------------|
| laborcode | VARCHAR | Labor code (primary key) |
| personid | VARCHAR | Person identifier |
| displayname | VARCHAR | Display name |
| orgid | VARCHAR | Organization |
| status | VARCHAR | Labor status |
| craft | VARCHAR | Craft/skill |
| skilllevel | VARCHAR | Skill level |
| laborhrs | DECIMAL | Labor hours available |
| regularhr | DECIMAL | Regular hourly rate |

## MATUSETRANS Table

Material usage transactions.

| Column | Type | Description |
|--------|------|-------------|
| matusetransid | BIGINT | Transaction ID (primary key) |
| siteid | VARCHAR | Site identifier |
| itemnum | VARCHAR | Item number |
| storeloc | VARCHAR | Store location |
| refwo | VARCHAR | Reference work order |
| quantity | DECIMAL | Quantity used |
| unitcost | DECIMAL | Unit cost |
| linecost | DECIMAL | Line total cost |
| transdate | DATETIME | Transaction date |
| description | VARCHAR | Item description |

## Common Joins

### Work Order with Asset
```sql
WORKORDER w
JOIN ASSET a ON w.assetnum = a.assetnum AND w.siteid = a.siteid
```

### Work Order with Material Costs
```sql
WORKORDER w
JOIN MATUSETRANS m ON w.wonum = m.refwo AND w.siteid = m.siteid
```

### Asset with Inventory
```sql
ASSET a
JOIN INVENTORY i ON a.siteid = i.siteid
```

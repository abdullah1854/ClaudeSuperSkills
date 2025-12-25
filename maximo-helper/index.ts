
const { table, filter } = inputs;
const SITE_FILTER = "SITEID = 'YOUR_SITE_ID'";

const schemas = {
  WORKORDER: ['WONUM', 'DESCRIPTION', 'STATUS', 'WORKTYPE', 'REPORTDATE', 'LOCATION', 'ASSETNUM'],
  ASSET: ['ASSETNUM', 'DESCRIPTION', 'STATUS', 'LOCATION', 'PARENT', 'SERIALNUM'],
  INVENTORY: ['ITEMNUM', 'STORELOC', 'CURBAL', 'AVGCOST', 'MINLEVEL'],
  LABOR: ['LABORCODE', 'DISPLAYNAME', 'STATUS', 'WORKSITE'],
  LABTRANS: ['LABTRANSID', 'LABORCODE', 'REFWO', 'STARTDATE', 'REGULARHRS']
};

const t = table.toUpperCase();
const cols = schemas[t] || ['*'];

let query = `SELECT TOP 100\n    ${cols.join(',\n    ')}\nFROM ${t}\nWHERE ${SITE_FILTER}`;

if (filter) {
  query += `\n  AND ${filter}`;
}

query += ';';

console.log(`-- Maximo Query for ${t}\n-- ⚠️ ALWAYS filter by ${SITE_FILTER}\n\n${query}`);

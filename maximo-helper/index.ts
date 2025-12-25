
const { table, filter } = inputs;
const GBE = "SITEID = 'GBE'";

const schemas = {
  WORKORDER: ['WONUM', 'DESCRIPTION', 'STATUS', 'WORKTYPE', 'REPORTDATE', 'LOCATION', 'ASSETNUM'],
  ASSET: ['ASSETNUM', 'DESCRIPTION', 'STATUS', 'LOCATION', 'PARENT', 'SERIALNUM'],
  INVENTORY: ['ITEMNUM', 'STORELOC', 'CURBAL', 'AVGCOST', 'MINLEVEL'],
  LABOR: ['LABORCODE', 'DISPLAYNAME', 'STATUS', 'WORKSITE'],
  LABTRANS: ['LABTRANSID', 'LABORCODE', 'REFWO', 'STARTDATE', 'REGULARHRS']
};

const t = table.toUpperCase();
const cols = schemas[t] || ['*'];

let query = `SELECT TOP 100\n    ${cols.join(',\n    ')}\nFROM ${t}\nWHERE ${GBE}`;

if (filter) {
  query += `\n  AND ${filter}`;
}

query += ';';

console.log(`-- Maximo Query for ${t}\n-- ⚠️ ALWAYS filter by ${GBE}\n\n${query}`);

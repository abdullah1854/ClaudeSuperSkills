
const { table, dataareaid = 'GBE' } = inputs;

const schemas = {
  SALESTABLE: ['SALESID', 'CUSTACCOUNT', 'SALESSTATUS', 'CREATEDDATE', 'CURRENCYCODE'],
  SALESLINE: ['SALESID', 'LINENUM', 'ITEMID', 'SALESQTY', 'LINEAMOUNT'],
  PURCHTABLE: ['PURCHID', 'VENDACCOUNT', 'PURCHSTATUS', 'CREATEDDATE'],
  PURCHLINE: ['PURCHID', 'LINENUM', 'ITEMID', 'PURCHQTY', 'LINEAMOUNT'],
  INVENTTABLE: ['ITEMID', 'ITEMNAME', 'ITEMGROUPID', 'ITEMTYPE'],
  CUSTTABLE: ['ACCOUNTNUM', 'NAME', 'CURRENCY', 'CUSTGROUP'],
  VENDTABLE: ['ACCOUNTNUM', 'NAME', 'CURRENCY', 'VENDGROUP']
};

const t = table.toUpperCase();
const cols = schemas[t] || ['*'];

const query = `SELECT TOP 100
    ${cols.join(',\n    ')},
    DATAAREAID
FROM ${t}
WHERE DATAAREAID = '${dataareaid}';`;

console.log(`-- AX Dynamics Query for ${t}\n\n${query}`);

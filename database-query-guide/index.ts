
const { database, query } = inputs;

const servers = {
  maximo: { server: 'MAXIMO-PROD', db: 'MAXIMO', note: 'Always filter by SITEID = GBE' },
  ax: { server: 'AX-PROD', db: 'AX2012', note: 'Always filter by DATAAREAID' },
  fabric: { server: 'Fabric Lakehouse', db: 'Analytics', note: 'Use Spark SQL or Delta' }
};

const s = servers[database.toLowerCase()] || { server: 'UNKNOWN', db: database, note: 'Verify connection' };

let output = `# Database: ${database.toUpperCase()}\n\n`;
output += `**Server**: ${s.server}\n`;
output += `**Database**: ${s.db}\n`;
output += `**Note**: ⚠️ ${s.note}\n`;

if (query) {
  output += `\n## Query\n\`\`\`sql\n${query}\n\`\`\``;
}

console.log(output);

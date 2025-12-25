
const { type, selector = 'table' } = inputs;

const scripts = {
  table: `// Extract table data
const table = document.querySelector('${selector}');
const rows = Array.from(table.querySelectorAll('tr'));
const headers = Array.from(rows[0].querySelectorAll('th,td')).map(c => c.textContent.trim());

const data = rows.slice(1).map(row => {
  const cells = Array.from(row.querySelectorAll('td'));
  return Object.fromEntries(headers.map((h, i) => [h, cells[i]?.textContent?.trim()]));
});
console.log(JSON.stringify(data, null, 2));`,

  form: `// Extract form data
const form = document.querySelector('${selector}');
const formData = {};
form.querySelectorAll('input, select, textarea').forEach(el => {
  if (el.name) formData[el.name] = el.value;
});
console.log(JSON.stringify(formData, null, 2));`,

  list: `// Extract list items
const items = document.querySelectorAll('${selector}');
const data = Array.from(items).map(el => el.textContent.trim());
console.log(JSON.stringify(data, null, 2));`
};

console.log(scripts[type] || scripts.table);

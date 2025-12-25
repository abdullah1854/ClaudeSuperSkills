/**
 * D365 Finance & Operations Debugging Framework
 * Version: 6.0.0
 *
 * This skill is a Claude Code managed skill - the full implementation
 * is in SKILL.md which contains the complete debugging playbooks for:
 * - Finance (GL, AP, AR)
 * - Supply Chain (Order-to-Cash, Procure-to-Pay, Inventory)
 * - Warehouse (WMS)
 * - Batch & Operations
 * - Security
 * - Integration (DMF/OData)
 * - Reporting (SSRS)
 * - Performance
 *
 * Core Rules:
 * - SCHEMA FIRST: Never guess columns
 * - PLATINUM RULE: Always find a working example to diff
 * - DIAMOND RULE: Check full stack (UI -> Logic -> Config)
 * - LINE CONTAMINATION: One bad line can override header classification
 */

const { businessKey, symptom, legalEntity } = $input;

// Route to appropriate playbook based on symptom
const symptomRouter = {
  'missing from report': 'REPORTING',
  'not posted': 'POSTING',
  'can\'t post': 'POSTING',
  'wrong amount': 'FINANCE-CALC',
  'can\'t see': 'SECURITY',
  'can\'t access': 'SECURITY',
  'integration success': 'INTEGRATION',
  'batch didn\'t run': 'BATCH',
  'stuck': 'BATCH',
  'slow': 'PERFORMANCE',
  'timeout': 'PERFORMANCE',
  'invoice missing': 'SCM-ORDER',
  'work stuck': 'WMS',
  'voucher wrong': 'FINANCE-GL',
  'voucher missing': 'FINANCE-GL'
};

// Find matching playbook
let playbook = 'GENERAL';
if (symptom) {
  const lowerSymptom = symptom.toLowerCase();
  for (const [pattern, route] of Object.entries(symptomRouter)) {
    if (lowerSymptom.includes(pattern)) {
      playbook = route;
      break;
    }
  }
}

console.log(`## D365 Debug Session Started`);
console.log(`- Business Key: ${businessKey || 'Not specified'}`);
console.log(`- Symptom: ${symptom || 'Not specified'}`);
console.log(`- Legal Entity: ${legalEntity || 'Will validate'}`);
console.log(`- Routing to: ${playbook} playbook`);
console.log(`\nSee SKILL.md for complete debugging instructions and SQL templates.`);


const { feature, requirements, phases = ['Setup', 'Core', 'Integration', 'Test'] } = inputs;
const date = new Date().toISOString().split('T')[0];

let plan = `# Implementation Plan: ${feature}\n\n**Created**: ${date}\n\n## Requirements\n`;
requirements.forEach((r, i) => plan += `- REQ-${String(i+1).padStart(3,'0')}: ${r}\n`);

plan += '\n';
phases.forEach((phase, pi) => {
  plan += `## Phase ${pi+1}: ${phase}\n`;
  plan += `- TASK-${pi+1}.1: [Task description]\n`;
  plan += `  - Files: \`src/...\`\n`;
  plan += `  - DoD: [Definition of done]\n\n`;
});

plan += `## Definition of Done\n- [ ] All tests passing\n- [ ] Code reviewed\n- [ ] Documentation updated`;

console.log(plan);

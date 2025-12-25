// Codebase Navigation Skill
const scope = inputs.scope || 'full';
const focus = inputs.focus || 'all';

const explorationSteps = {
  structure: [
    '1. List root directory structure',
    '2. Identify src/lib/app directories',
    '3. Map module organization',
    '4. Find entry points',
    '5. Locate configuration files'
  ],
  dependencies: [
    '1. Read package.json/requirements.txt',
    '2. Map internal imports',
    '3. Identify shared modules',
    '4. Trace dependency chains',
    '5. Find circular dependencies'
  ],
  patterns: [
    '1. Identify architectural patterns (MVC, Clean, etc.)',
    '2. Find design patterns in use',
    '3. Map naming conventions',
    '4. Identify testing patterns',
    '5. Document code style'
  ]
};

console.log(`## Codebase Navigation - ${scope}

### Focus: ${focus}

### Exploration Steps:
${focus === 'all' ? 
  Object.entries(explorationSteps).map(([k, v]) => `#### ${k}\\n${v.join('\\n')}`).join('\\n\\n') :
  explorationSteps[focus]?.join('\\n') || 'Invalid focus area'}

### Quick Commands:
- \`tree -L 3 -I node_modules\` - Directory structure
- \`grep -r "import" --include="*.ts" | head -50\` - Import analysis
- \`find . -name "*.config.*"\` - Configuration files
- \`cat package.json | jq '.dependencies'\` - Dependencies

### Key Files to Check:
- README.md - Project overview
- package.json / requirements.txt - Dependencies
- tsconfig.json / pyproject.toml - Build config
- .env.example - Environment variables
- CLAUDE.md - AI instructions
`);
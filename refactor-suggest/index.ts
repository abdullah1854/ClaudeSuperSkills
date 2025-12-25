
const { smell } = inputs;

const patterns = {
  long_function: {
    name: 'Extract Method',
    description: 'Extract code block into separate method',
    example: `// Before
function process(data) {
  // 50+ lines of mixed logic
}

// After
function validate(data) { /* validation */ }
function transform(data) { /* transform */ }
function save(data) { /* save */ }

function process(data) {
  validate(data);
  const result = transform(data);
  save(result);
}`
  },
  deep_nesting: {
    name: 'Guard Clauses',
    description: 'Replace nested conditions with early returns',
    example: `// Before
if (user) {
  if (user.active) {
    if (user.hasPermission) {
      doSomething();
    }
  }
}

// After
if (!user) return;
if (!user.active) return;
if (!user.hasPermission) return;
doSomething();`
  },
  long_params: {
    name: 'Parameter Object',
    description: 'Group related parameters into object',
    example: `// Before
function createUser(name, email, phone, address, city, zip) {}

// After
function createUser(userInfo: UserInfo) {}`
  }
};

const p = patterns[smell] || patterns.long_function;
console.log(`# Refactoring: ${p.name}\n\n${p.description}\n\n\`\`\`javascript\n${p.example}\n\`\`\``);

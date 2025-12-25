
const { framework } = inputs;

const structures = {
  nextjs: `nextjs-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   └── lib/
├── public/
├── package.json
├── tsconfig.json
├── next.config.js
└── .gitignore`,

  express: `express-api/
├── src/
│   ├── routes/
│   ├── middleware/
│   ├── services/
│   ├── types/
│   └── index.ts
├── package.json
├── tsconfig.json
├── .env.example
└── .gitignore`,

  fastapi: `fastapi-app/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── __init__.py
│   └── main.py
├── tests/
├── requirements.txt
├── pyproject.toml
└── .gitignore`
};

console.log(`# ${framework} Project Structure\n\n\`\`\`\n${structures[framework] || structures.nextjs}\n\`\`\``);

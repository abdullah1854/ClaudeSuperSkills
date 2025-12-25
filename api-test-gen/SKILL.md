# api-test-gen

Generates API test templates for Jest/Supertest or Pytest with authentication handling.

## Metadata
- **Version**: 1.0.0
- **Category**: testing
- **Source**: workspace


## Tags
`api`, `testing`, `jest`, `pytest`

## MCP Dependencies
None specified

## Inputs
- `endpoint` (string) (required): API endpoint path
- `method` (string) (optional): HTTP method: GET, POST, PUT, DELETE
- `framework` (string) (optional): Test framework: jest or pytest



## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "api-test-gen", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/api-test-gen/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript

const { endpoint, method = 'GET', framework = 'jest' } = inputs;
const m = method.toLowerCase();

if (framework === 'jest') {
  console.log(`describe('${method} ${endpoint}', () => {
  it('should return success response', async () => {
    const response = await request(app)
      .${m}('${endpoint}')
      .set('Authorization', \`Bearer \${authToken}\`)
      .expect(200);
    
    expect(response.body).toBeDefined();
  });

  it('should return 401 without auth', async () => {
    await request(app)
      .${m}('${endpoint}')
      .expect(401);
  });
});`);
} else {
  console.log(`def test_${m}_${endpoint.replace(/\//g, '_').replace(/^_/, '')}(client):
    """Test ${method} ${endpoint}"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.${m}("${endpoint}", headers=headers)
    assert response.status_code == 200

def test_${m}_${endpoint.replace(/\//g, '_').replace(/^_/, '')}_unauthorized(client):
    """Test ${method} ${endpoint} without auth"""
    response = client.${m}("${endpoint}")
    assert response.status_code == 401`);
}

```

---
Created: Mon Dec 22 2025 10:36:14 GMT+0800 (Singapore Standard Time)
Updated: Mon Dec 22 2025 10:36:14 GMT+0800 (Singapore Standard Time)

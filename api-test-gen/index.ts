
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

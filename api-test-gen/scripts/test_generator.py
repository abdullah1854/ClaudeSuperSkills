#!/usr/bin/env python3
"""
API Test Generator - Creates test templates for REST APIs.
"""

import json
import sys
from typing import Optional


def generate_jest_test(
    endpoint: str,
    method: str,
    description: str,
    request_body: Optional[dict] = None,
    expected_status: int = 200,
    expected_response: Optional[dict] = None,
    auth_required: bool = False
) -> str:
    """Generate Jest/Supertest test for an API endpoint."""

    auth_header = ""
    if auth_required:
        auth_header = "\n      .set('Authorization', `Bearer ${authToken}`)"

    body_line = ""
    if request_body and method.upper() in ["POST", "PUT", "PATCH"]:
        body_json = json.dumps(request_body, indent=6)
        body_line = f"\n      .send({body_json})"

    response_checks = ""
    if expected_response:
        for key, value in expected_response.items():
            if isinstance(value, str):
                response_checks += f"\n    expect(response.body.{key}).toBe('{value}');"
            else:
                response_checks += f"\n    expect(response.body.{key}).toBe({json.dumps(value)});"

    test = f"""describe('{method.upper()} {endpoint}', () => {{
  it('{description}', async () => {{
    const response = await request(app)
      .{method.lower()}('{endpoint}'){auth_header}{body_line}
      .expect({expected_status});
{response_checks}
  }});
}});
"""
    return test


def generate_pytest_test(
    endpoint: str,
    method: str,
    description: str,
    request_body: Optional[dict] = None,
    expected_status: int = 200,
    expected_response: Optional[dict] = None,
    auth_required: bool = False
) -> str:
    """Generate Pytest test for an API endpoint."""

    func_name = description.lower().replace(" ", "_").replace("-", "_")
    func_name = "test_" + "".join(c for c in func_name if c.isalnum() or c == "_")

    headers = "headers = {}"
    if auth_required:
        headers = 'headers = {"Authorization": f"Bearer {auth_token}"}'

    body_param = ""
    if request_body and method.upper() in ["POST", "PUT", "PATCH"]:
        body_json = json.dumps(request_body, indent=4)
        body_param = f", json={body_json}"

    response_checks = ""
    if expected_response:
        for key, value in expected_response.items():
            response_checks += f'\n    assert response.json()["{key}"] == {json.dumps(value)}'

    test = f'''def {func_name}(client):
    """{description}"""
    {headers}
    response = client.{method.lower()}("{endpoint}"{body_param}, headers=headers)
    assert response.status_code == {expected_status}{response_checks}
'''
    return test


def generate_test_suite(
    base_url: str,
    endpoints: list[dict],
    framework: str = "jest"
) -> str:
    """Generate a complete test suite for multiple endpoints."""

    if framework == "jest":
        suite = f"""import request from 'supertest';
import app from '../src/app';

const authToken = process.env.TEST_AUTH_TOKEN || 'test-token';

"""
        for ep in endpoints:
            suite += generate_jest_test(**ep) + "\n"

    elif framework == "pytest":
        suite = f"""import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

auth_token = "test-token"

"""
        for ep in endpoints:
            suite += generate_pytest_test(**ep) + "\n"

    return suite


def generate_crud_tests(
    resource: str,
    base_path: str,
    framework: str = "jest"
) -> str:
    """Generate standard CRUD tests for a resource."""

    endpoints = [
        {
            "endpoint": base_path,
            "method": "GET",
            "description": f"should list all {resource}s",
            "expected_status": 200
        },
        {
            "endpoint": f"{base_path}/1",
            "method": "GET",
            "description": f"should get {resource} by id",
            "expected_status": 200
        },
        {
            "endpoint": base_path,
            "method": "POST",
            "description": f"should create new {resource}",
            "request_body": {"name": f"Test {resource}"},
            "expected_status": 201,
            "auth_required": True
        },
        {
            "endpoint": f"{base_path}/1",
            "method": "PUT",
            "description": f"should update {resource}",
            "request_body": {"name": f"Updated {resource}"},
            "expected_status": 200,
            "auth_required": True
        },
        {
            "endpoint": f"{base_path}/1",
            "method": "DELETE",
            "description": f"should delete {resource}",
            "expected_status": 204,
            "auth_required": True
        }
    ]

    return generate_test_suite(base_path, endpoints, framework)


def generate_error_tests(
    endpoint: str,
    method: str,
    framework: str = "jest"
) -> str:
    """Generate error handling tests."""

    if framework == "jest":
        return f"""describe('{method.upper()} {endpoint} - Error Cases', () => {{
  it('should return 401 without auth token', async () => {{
    const response = await request(app)
      .{method.lower()}('{endpoint}')
      .expect(401);
    expect(response.body.error).toBeDefined();
  }});

  it('should return 400 with invalid input', async () => {{
    const response = await request(app)
      .{method.lower()}('{endpoint}')
      .set('Authorization', `Bearer ${{authToken}}`)
      .send({{ invalid: 'data' }})
      .expect(400);
    expect(response.body.error).toBeDefined();
  }});

  it('should return 404 for non-existent resource', async () => {{
    const response = await request(app)
      .get('{endpoint}/99999')
      .set('Authorization', `Bearer ${{authToken}}`)
      .expect(404);
  }});
}});
"""
    return ""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--crud":
            resource = sys.argv[2] if len(sys.argv) > 2 else "user"
            path = sys.argv[3] if len(sys.argv) > 3 else f"/api/{resource}s"
            framework = sys.argv[4] if len(sys.argv) > 4 else "jest"
            print(generate_crud_tests(resource, path, framework))
        elif sys.argv[1] == "--example":
            print(generate_jest_test(
                endpoint="/api/users",
                method="POST",
                description="should create a new user",
                request_body={"email": "test@example.com", "name": "Test User"},
                expected_status=201,
                expected_response={"email": "test@example.com"},
                auth_required=True
            ))
    else:
        print("API Test Generator")
        print("Usage: --crud <resource> [path] [framework]")
        print("       --example")

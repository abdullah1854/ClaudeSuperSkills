#!/usr/bin/env python3
"""
Implementation Plan Generator - Creates structured development plans.
"""

import json
import sys
from datetime import datetime
from typing import Optional


def generate_plan(
    feature_name: str,
    requirements: list[dict],
    phases: list[dict],
    risks: Optional[list[dict]] = None
) -> str:
    """
    Generate an implementation plan.

    Args:
        feature_name: Name of the feature
        requirements: List of {id, description, type} dicts
        phases: List of {name, tasks: [{id, description, files, dod, test}]} dicts
        risks: Optional list of {id, description, mitigation} dicts
    """
    plan = f"""# Implementation Plan: {feature_name}

**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Draft

## Requirements
"""

    for req in requirements:
        req_type = f" ({req.get('type', 'functional')})" if req.get('type') else ""
        plan += f"- {req['id']}: {req['description']}{req_type}\n"

    for phase in phases:
        plan += f"\n## {phase['name']}\n"

        for task in phase.get('tasks', []):
            plan += f"\n### {task['id']}: {task['description']}\n"

            if task.get('files'):
                plan += f"- **Files**: `{', '.join(task['files'])}`\n"

            if task.get('depends'):
                plan += f"- **Depends**: {task['depends']}\n"

            if task.get('dod'):
                plan += f"- **DoD**: {task['dod']}\n"

            if task.get('test'):
                plan += f"- **Test**: {task['test']}\n"

    if risks:
        plan += "\n## Risks\n"
        for risk in risks:
            plan += f"- {risk['id']}: {risk['description']}\n"
            plan += f"  - **Mitigation**: {risk['mitigation']}\n"

    plan += """
## Definition of Done
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No new linting errors
"""

    return plan


def create_task(
    task_id: str,
    description: str,
    files: Optional[list[str]] = None,
    dod: Optional[str] = None,
    test: Optional[str] = None,
    depends: Optional[str] = None,
    size: str = "M"
) -> dict:
    """Create a task dictionary."""
    return {
        "id": task_id,
        "description": description,
        "files": files or [],
        "dod": dod,
        "test": test,
        "depends": depends,
        "size": size
    }


def create_requirement(
    req_id: str,
    description: str,
    req_type: str = "functional"
) -> dict:
    """Create a requirement dictionary."""
    return {
        "id": req_id,
        "description": description,
        "type": req_type
    }


def create_risk(
    risk_id: str,
    description: str,
    mitigation: str
) -> dict:
    """Create a risk dictionary."""
    return {
        "id": risk_id,
        "description": description,
        "mitigation": mitigation
    }


def generate_crud_plan(
    resource_name: str,
    fields: list[str]
) -> str:
    """Generate a plan for CRUD operations on a resource."""

    requirements = [
        create_requirement("REQ-001", f"Users can create new {resource_name}s"),
        create_requirement("REQ-002", f"Users can view {resource_name} details"),
        create_requirement("REQ-003", f"Users can list all {resource_name}s"),
        create_requirement("REQ-004", f"Users can update {resource_name}s"),
        create_requirement("REQ-005", f"Users can delete {resource_name}s"),
        create_requirement("REQ-006", "All operations require authentication", "non-functional")
    ]

    phases = [
        {
            "name": "Phase 1: Data Layer",
            "tasks": [
                create_task(
                    "TASK-1.1",
                    f"Create {resource_name} model/schema",
                    files=[f"src/models/{resource_name.lower()}.ts"],
                    dod=f"Model with fields: {', '.join(fields)}",
                    test="Unit tests for model validation"
                ),
                create_task(
                    "TASK-1.2",
                    "Create database migration",
                    files=["migrations/"],
                    dod="Migration creates table with all fields",
                    test="Migration runs successfully"
                )
            ]
        },
        {
            "name": "Phase 2: API Layer",
            "tasks": [
                create_task(
                    "TASK-2.1",
                    f"Implement GET /{resource_name.lower()}s endpoint",
                    files=[f"src/routes/{resource_name.lower()}.ts"],
                    dod="Returns paginated list",
                    test="Integration test for list endpoint",
                    depends="TASK-1.1"
                ),
                create_task(
                    "TASK-2.2",
                    f"Implement GET /{resource_name.lower()}s/:id endpoint",
                    files=[f"src/routes/{resource_name.lower()}.ts"],
                    dod="Returns single item or 404",
                    test="Integration test for get by ID"
                ),
                create_task(
                    "TASK-2.3",
                    f"Implement POST /{resource_name.lower()}s endpoint",
                    files=[f"src/routes/{resource_name.lower()}.ts"],
                    dod="Creates item and returns 201",
                    test="Integration test for create"
                ),
                create_task(
                    "TASK-2.4",
                    f"Implement PUT /{resource_name.lower()}s/:id endpoint",
                    files=[f"src/routes/{resource_name.lower()}.ts"],
                    dod="Updates item and returns 200",
                    test="Integration test for update"
                ),
                create_task(
                    "TASK-2.5",
                    f"Implement DELETE /{resource_name.lower()}s/:id endpoint",
                    files=[f"src/routes/{resource_name.lower()}.ts"],
                    dod="Deletes item and returns 204",
                    test="Integration test for delete"
                )
            ]
        },
        {
            "name": "Phase 3: Authentication",
            "tasks": [
                create_task(
                    "TASK-3.1",
                    "Add auth middleware to routes",
                    files=["src/middleware/auth.ts", f"src/routes/{resource_name.lower()}.ts"],
                    dod="All endpoints require valid token",
                    test="Unauthenticated requests return 401",
                    depends="TASK-2.5"
                )
            ]
        }
    ]

    risks = [
        create_risk("RISK-001", "Schema changes during development", "Use migrations for all changes"),
        create_risk("RISK-002", "Performance with large datasets", "Add pagination from start")
    ]

    return generate_plan(f"{resource_name} CRUD API", requirements, phases, risks)


def generate_feature_plan(
    feature_name: str,
    description: str,
    components: list[str]
) -> str:
    """Generate a generic feature implementation plan."""

    requirements = [
        create_requirement("REQ-001", description),
        create_requirement("REQ-002", "Feature should be tested", "non-functional"),
        create_requirement("REQ-003", "Feature should be documented", "non-functional")
    ]

    tasks = [
        create_task(
            f"TASK-1.{i+1}",
            f"Implement {component}",
            files=[f"src/{component.lower().replace(' ', '_')}.ts"],
            dod=f"{component} is functional",
            test=f"Tests for {component}"
        )
        for i, component in enumerate(components)
    ]

    phases = [
        {"name": "Phase 1: Implementation", "tasks": tasks}
    ]

    return generate_plan(feature_name, requirements, phases)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--crud":
            resource = sys.argv[2] if len(sys.argv) > 2 else "Item"
            fields = sys.argv[3].split(",") if len(sys.argv) > 3 else ["id", "name", "description"]
            print(generate_crud_plan(resource, fields))

        elif cmd == "--feature":
            name = sys.argv[2] if len(sys.argv) > 2 else "New Feature"
            components = sys.argv[3].split(",") if len(sys.argv) > 3 else ["Component A", "Component B"]
            print(generate_feature_plan(name, f"Implement {name}", components))

        elif cmd == "--example":
            plan = generate_plan(
                "User Authentication",
                [
                    create_requirement("REQ-001", "Users can register"),
                    create_requirement("REQ-002", "Users can login")
                ],
                [
                    {
                        "name": "Phase 1: Setup",
                        "tasks": [
                            create_task("TASK-1.1", "Create User model", ["src/models/user.ts"])
                        ]
                    }
                ]
            )
            print(plan)
    else:
        print("Implementation Plan Generator")
        print("Usage:")
        print("  --crud <resource> [fields]    Generate CRUD plan")
        print("  --feature <name> [components] Generate feature plan")
        print("  --example                     Show example plan")

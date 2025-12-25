#!/usr/bin/env python3
"""
Chrome Data Extractor - Patterns for browser automation data extraction.
"""

import json
import re
from typing import Optional


def generate_table_extraction_script(
    table_selector: str,
    include_headers: bool = True
) -> str:
    """Generate JavaScript to extract data from HTML table."""
    return f"""// Extract data from table
const table = document.querySelector('{table_selector}');
if (!table) throw new Error('Table not found: {table_selector}');

const rows = Array.from(table.querySelectorAll('tr'));
const data = [];

{'const headers = Array.from(rows[0].querySelectorAll("th, td")).map(cell => cell.textContent.trim());' if include_headers else ''}
const startRow = {1 if include_headers else 0};

for (let i = startRow; i < rows.length; i++) {{
    const cells = Array.from(rows[i].querySelectorAll('td'));
    const rowData = cells.map(cell => cell.textContent.trim());
    {'data.push(Object.fromEntries(headers.map((h, idx) => [h, rowData[idx]])));' if include_headers else 'data.push(rowData);'}
}}

console.log(JSON.stringify(data, null, 2));
"""


def generate_list_extraction_script(
    container_selector: str,
    item_selector: str,
    fields: dict[str, str]
) -> str:
    """Generate JavaScript to extract data from list items."""
    field_extractions = []
    for name, selector in fields.items():
        field_extractions.append(f'"{name}": item.querySelector(\'{selector}\')?.textContent?.trim() || null')

    fields_str = ",\n            ".join(field_extractions)

    return f"""// Extract data from list
const container = document.querySelector('{container_selector}');
if (!container) throw new Error('Container not found: {container_selector}');

const items = container.querySelectorAll('{item_selector}');
const data = Array.from(items).map(item => ({{
    {fields_str}
}}));

console.log(JSON.stringify(data, null, 2));
"""


def generate_form_extraction_script(form_selector: str) -> str:
    """Generate JavaScript to extract form field values."""
    return f"""// Extract form data
const form = document.querySelector('{form_selector}');
if (!form) throw new Error('Form not found: {form_selector}');

const formData = {{}};
const inputs = form.querySelectorAll('input, select, textarea');

inputs.forEach(input => {{
    const name = input.name || input.id;
    if (!name) return;

    if (input.type === 'checkbox') {{
        formData[name] = input.checked;
    }} else if (input.type === 'radio') {{
        if (input.checked) formData[name] = input.value;
    }} else {{
        formData[name] = input.value;
    }}
}});

console.log(JSON.stringify(formData, null, 2));
"""


def generate_pagination_script(
    item_selector: str,
    next_button_selector: str,
    max_pages: int = 10
) -> str:
    """Generate JavaScript for paginated data extraction."""
    return f"""// Paginated data extraction
async function extractAllPages() {{
    const allData = [];
    let page = 1;

    while (page <= {max_pages}) {{
        // Extract current page items
        const items = document.querySelectorAll('{item_selector}');
        items.forEach(item => {{
            allData.push(item.textContent.trim());
        }});

        // Try to go to next page
        const nextBtn = document.querySelector('{next_button_selector}');
        if (!nextBtn || nextBtn.disabled) break;

        nextBtn.click();
        await new Promise(r => setTimeout(r, 1000)); // Wait for page load
        page++;
    }}

    return allData;
}}

extractAllPages().then(data => console.log(JSON.stringify(data, null, 2)));
"""


def generate_wait_and_extract_script(
    wait_selector: str,
    extract_selector: str,
    timeout_ms: int = 10000
) -> str:
    """Generate script that waits for element before extracting."""
    return f"""// Wait for element and extract
async function waitAndExtract() {{
    const startTime = Date.now();

    while (Date.now() - startTime < {timeout_ms}) {{
        const element = document.querySelector('{wait_selector}');
        if (element) {{
            const target = document.querySelector('{extract_selector}');
            return target ? target.textContent.trim() : null;
        }}
        await new Promise(r => setTimeout(r, 100));
    }}

    throw new Error('Timeout waiting for: {wait_selector}');
}}

waitAndExtract().then(data => console.log(data));
"""


def generate_accessibility_tree_query(
    role: Optional[str] = None,
    name: Optional[str] = None
) -> dict:
    """Generate accessibility tree query pattern."""
    query = {
        "description": "Query accessibility tree for elements",
        "tool": "read_page",
        "parameters": {
            "filter": "interactive" if role else "all"
        }
    }

    if role or name:
        query["post_filter"] = {
            "role": role,
            "name_contains": name
        }

    return query


def generate_extraction_workflow(
    url: str,
    selectors: dict[str, str],
    auth_required: bool = False
) -> list[dict]:
    """Generate a complete extraction workflow."""
    workflow = []

    # Step 1: Navigate
    workflow.append({
        "step": 1,
        "action": "navigate",
        "tool": "navigate",
        "parameters": {"url": url}
    })

    # Step 2: Wait for page load
    workflow.append({
        "step": 2,
        "action": "wait_for_load",
        "tool": "computer",
        "parameters": {"action": "wait", "duration": 2}
    })

    # Step 3: Take screenshot
    workflow.append({
        "step": 3,
        "action": "screenshot",
        "tool": "computer",
        "parameters": {"action": "screenshot"}
    })

    # Step 4: Extract data
    for name, selector in selectors.items():
        workflow.append({
            "step": len(workflow) + 1,
            "action": f"extract_{name}",
            "tool": "javascript_tool",
            "parameters": {
                "text": f"document.querySelector('{selector}')?.textContent?.trim()"
            }
        })

    return workflow


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--table":
            selector = sys.argv[2] if len(sys.argv) > 2 else "table"
            print(generate_table_extraction_script(selector))

        elif cmd == "--form":
            selector = sys.argv[2] if len(sys.argv) > 2 else "form"
            print(generate_form_extraction_script(selector))

        elif cmd == "--list":
            print(generate_list_extraction_script(
                container_selector=".results",
                item_selector=".item",
                fields={
                    "title": ".title",
                    "price": ".price",
                    "link": "a"
                }
            ))

        elif cmd == "--workflow":
            workflow = generate_extraction_workflow(
                url="https://example.com",
                selectors={"title": "h1", "content": ".main-content"}
            )
            print(json.dumps(workflow, indent=2))
    else:
        print("Chrome Data Extractor")
        print("Usage:")
        print("  --table [selector]  Generate table extraction script")
        print("  --form [selector]   Generate form extraction script")
        print("  --list              Generate list extraction script")
        print("  --workflow          Generate extraction workflow")

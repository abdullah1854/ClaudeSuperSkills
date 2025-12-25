#!/usr/bin/env python3
"""
ADR Generator - Creates Architectural Decision Records from structured input.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def generate_adr(
    title: str,
    context: str,
    decision: str,
    consequences: dict,
    alternatives: list[dict],
    status: str = "PROPOSED",
    adr_number: Optional[int] = None,
    output_dir: str = "docs/adr"
) -> str:
    """
    Generate an ADR document.

    Args:
        title: Decision title
        context: Problem context and motivation
        decision: The change being proposed/made
        consequences: Dict with 'positive', 'negative', 'neutral' lists
        alternatives: List of dicts with 'name' and 'reason' keys
        status: PROPOSED|ACCEPTED|DEPRECATED|SUPERSEDED
        adr_number: ADR sequence number (auto-generated if None)
        output_dir: Output directory for ADR files
    """
    # Auto-generate ADR number
    if adr_number is None:
        adr_dir = Path(output_dir)
        if adr_dir.exists():
            existing = list(adr_dir.glob("*.md"))
            adr_number = len(existing) + 1
        else:
            adr_number = 1

    # Build consequences section
    consequences_text = ""
    if consequences.get("positive"):
        consequences_text += "**Positive:**\n"
        for item in consequences["positive"]:
            consequences_text += f"- {item}\n"
        consequences_text += "\n"

    if consequences.get("negative"):
        consequences_text += "**Negative:**\n"
        for item in consequences["negative"]:
            consequences_text += f"- {item}\n"
        consequences_text += "\n"

    if consequences.get("neutral"):
        consequences_text += "**Neutral:**\n"
        for item in consequences["neutral"]:
            consequences_text += f"- {item}\n"

    # Build alternatives section
    alternatives_text = ""
    for alt in alternatives:
        alternatives_text += f"- **{alt['name']}**: {alt['reason']}\n"

    # Generate ADR
    adr = f"""# ADR-{adr_number:03d}: {title}

## Status
{status}

## Context
{context}

## Decision
{decision}

## Consequences
{consequences_text.strip()}

## Alternatives Considered
{alternatives_text.strip()}

## References
- Related ADRs: [List related ADRs]
- Documentation: [Link to relevant docs]

---
*Date: {datetime.now().strftime('%Y-%m-%d')}*
"""

    return adr


def get_next_adr_number(adr_dir: str = "docs/adr") -> int:
    """Get the next available ADR number."""
    path = Path(adr_dir)
    if not path.exists():
        return 1
    existing = list(path.glob("*.md"))
    return len(existing) + 1


def validate_status(status: str) -> bool:
    """Validate ADR status."""
    valid = ["PROPOSED", "ACCEPTED", "DEPRECATED", "SUPERSEDED"]
    return status.upper() in valid


def create_adr_index(adr_dir: str = "docs/adr") -> str:
    """Create an index of all ADRs."""
    path = Path(adr_dir)
    if not path.exists():
        return "No ADRs found."

    adrs = sorted(path.glob("*.md"))
    if not adrs:
        return "No ADRs found."

    index = "# ADR Index\n\n| ADR | Title | Status |\n|-----|-------|--------|\n"

    for adr_file in adrs:
        content = adr_file.read_text()
        # Extract title and status
        lines = content.split("\n")
        title = lines[0].replace("# ", "") if lines else adr_file.stem
        status = "Unknown"
        for i, line in enumerate(lines):
            if line.strip() == "## Status":
                if i + 1 < len(lines):
                    status = lines[i + 1].strip()
                break
        index += f"| [{adr_file.stem}]({adr_file.name}) | {title} | {status} |\n"

    return index


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        example = generate_adr(
            title="Use PostgreSQL for Primary Database",
            context="We need a database that supports complex queries with joins, ACID transactions, and full-text search. Current team has experience with both PostgreSQL and MongoDB.",
            decision="We will use PostgreSQL as our primary database.",
            consequences={
                "positive": [
                    "Strong ACID compliance for financial data",
                    "Mature ecosystem and tooling",
                    "Team familiarity reduces ramp-up time"
                ],
                "negative": [
                    "Horizontal scaling requires additional complexity",
                    "Schema migrations need careful planning"
                ]
            },
            alternatives=[
                {"name": "MongoDB", "reason": "Flexible schema but lacks strong transactions"},
                {"name": "MySQL", "reason": "Similar to PostgreSQL but less feature-rich"}
            ],
            status="ACCEPTED"
        )
        print(example)
    else:
        print("ADR Generator - Use --example to see sample output")
        print(f"Next ADR number: {get_next_adr_number()}")

#!/usr/bin/env python3
"""
Cipher Memory Client - Interface for cross-IDE memory persistence.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class CipherMemoryClient:
    """Client for interacting with Cipher memory system."""

    def __init__(self, project_path: Optional[str] = None):
        self.project_path = project_path or os.getcwd()

    def format_store_message(
        self,
        category: str,
        content: str,
        context: Optional[str] = None
    ) -> dict:
        """Format a message for storing in Cipher."""
        message_parts = [f"STORE {category.upper()} for {self.project_path}:", content]
        if context:
            message_parts.append(f"Context: {context}")

        return {
            "message": " ".join(message_parts),
            "projectPath": self.project_path
        }

    def format_recall_message(self, topic: Optional[str] = None) -> dict:
        """Format a message for recalling from Cipher."""
        if topic:
            message = f"Search memory for: {topic}. What patterns, decisions, or learnings are relevant?"
        else:
            message = "Recall context for this project. What do you remember?"

        return {
            "message": message,
            "projectPath": self.project_path
        }

    def format_decision(
        self,
        description: str,
        reasoning: str,
        alternatives: Optional[list[str]] = None
    ) -> dict:
        """Format an architectural decision for storage."""
        content = f"{description}. Reasoning: {reasoning}"
        if alternatives:
            content += f". Alternatives considered: {', '.join(alternatives)}"

        return self.format_store_message("DECISION", content)

    def format_learning(
        self,
        bug_description: str,
        root_cause: str,
        solution: str
    ) -> dict:
        """Format a bug fix learning for storage."""
        content = f"Fixed {bug_description}. Root cause: {root_cause}. Solution: {solution}"
        return self.format_store_message("LEARNING", content)

    def format_milestone(
        self,
        feature: str,
        key_files: list[str]
    ) -> dict:
        """Format a feature milestone for storage."""
        content = f"Completed {feature}. Key files: {', '.join(key_files)}"
        return self.format_store_message("MILESTONE", content)

    def format_pattern(
        self,
        pattern_name: str,
        usage: str
    ) -> dict:
        """Format a discovered pattern for storage."""
        content = f"{pattern_name}. Usage: {usage}"
        return self.format_store_message("PATTERN", content)

    def format_blocker(
        self,
        description: str,
        attempts: list[str]
    ) -> dict:
        """Format a blocker for storage."""
        content = f"{description}. Attempted: {', '.join(attempts)}"
        return self.format_store_message("BLOCKER", content)

    def format_session_summary(
        self,
        accomplishments: list[str],
        open_items: list[str]
    ) -> dict:
        """Format end-of-session summary."""
        message = f"Summarize and consolidate today's session for {self.project_path}. "
        message += f"Key accomplishments: {', '.join(accomplishments)}. "
        message += f"Open items: {', '.join(open_items)}"

        return {
            "message": message,
            "projectPath": self.project_path
        }


def generate_mcp_call(action: str, **kwargs) -> dict:
    """Generate MCP tool call for cipher_ask_cipher."""
    client = CipherMemoryClient(kwargs.get("project_path"))

    if action == "recall":
        return {
            "tool": "cipher_ask_cipher",
            "arguments": client.format_recall_message(kwargs.get("topic"))
        }

    elif action == "decision":
        return {
            "tool": "cipher_ask_cipher",
            "arguments": client.format_decision(
                kwargs["description"],
                kwargs["reasoning"],
                kwargs.get("alternatives")
            )
        }

    elif action == "learning":
        return {
            "tool": "cipher_ask_cipher",
            "arguments": client.format_learning(
                kwargs["bug"],
                kwargs["cause"],
                kwargs["solution"]
            )
        }

    elif action == "milestone":
        return {
            "tool": "cipher_ask_cipher",
            "arguments": client.format_milestone(
                kwargs["feature"],
                kwargs["files"]
            )
        }

    elif action == "pattern":
        return {
            "tool": "cipher_ask_cipher",
            "arguments": client.format_pattern(
                kwargs["name"],
                kwargs["usage"]
            )
        }

    elif action == "blocker":
        return {
            "tool": "cipher_ask_cipher",
            "arguments": client.format_blocker(
                kwargs["description"],
                kwargs["attempts"]
            )
        }

    elif action == "summary":
        return {
            "tool": "cipher_ask_cipher",
            "arguments": client.format_session_summary(
                kwargs["accomplishments"],
                kwargs["open_items"]
            )
        }

    return {"error": f"Unknown action: {action}"}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        action = sys.argv[1]
        project = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

        if action == "--recall":
            topic = sys.argv[3] if len(sys.argv) > 3 else None
            result = generate_mcp_call("recall", project_path=project, topic=topic)
            print(json.dumps(result, indent=2))

        elif action == "--decision":
            result = generate_mcp_call(
                "decision",
                project_path=project,
                description="Example decision",
                reasoning="Example reasoning"
            )
            print(json.dumps(result, indent=2))

        elif action == "--help":
            print("Cipher Memory Client")
            print("Actions: --recall, --decision, --learning, --milestone, --pattern, --blocker, --summary")
    else:
        # Show example usage
        client = CipherMemoryClient("/Users/abdullah/MCP Gateway")
        print("Example Cipher calls:")
        print()
        print("Recall:")
        print(json.dumps(client.format_recall_message(), indent=2))
        print()
        print("Store Decision:")
        print(json.dumps(client.format_decision(
            "Use PostgreSQL for database",
            "Strong ACID compliance needed",
            ["MongoDB", "MySQL"]
        ), indent=2))

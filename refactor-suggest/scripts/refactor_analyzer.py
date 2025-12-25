#!/usr/bin/env python3
"""
Refactor Analyzer - Identifies code smells and suggests refactoring patterns.
"""

import json
import re
import sys
from typing import Optional


# Code smell patterns
CODE_SMELLS = {
    "long_function": {
        "description": "Function exceeds recommended length",
        "threshold": 50,  # lines
        "severity": "medium",
        "suggestion": "Extract logical sections into smaller, focused functions"
    },
    "deep_nesting": {
        "description": "Excessive nesting depth",
        "threshold": 4,  # levels
        "severity": "medium",
        "suggestion": "Use guard clauses, extract methods, or invert conditions"
    },
    "magic_numbers": {
        "description": "Unexplained numeric literals in code",
        "severity": "low",
        "suggestion": "Replace with named constants"
    },
    "god_class": {
        "description": "Class has too many responsibilities",
        "threshold": 300,  # lines
        "severity": "high",
        "suggestion": "Split into smaller, focused classes following SRP"
    },
    "long_parameter_list": {
        "description": "Function has too many parameters",
        "threshold": 5,
        "severity": "medium",
        "suggestion": "Use parameter object or builder pattern"
    },
    "duplicate_code": {
        "description": "Similar code blocks repeated",
        "severity": "medium",
        "suggestion": "Extract common logic into shared function"
    },
    "feature_envy": {
        "description": "Method uses another class's data more than its own",
        "severity": "medium",
        "suggestion": "Move method to the class it envies"
    },
    "primitive_obsession": {
        "description": "Overuse of primitives instead of small objects",
        "severity": "low",
        "suggestion": "Create value objects for related primitives"
    }
}


# Refactoring patterns
REFACTORING_PATTERNS = {
    "extract_method": {
        "description": "Extract a code block into a separate method",
        "when_to_use": [
            "Code block can be grouped together",
            "Code is duplicated elsewhere",
            "Method is too long",
            "Code needs a comment to explain it"
        ],
        "example": """
# Before
def process_order(order):
    # Calculate total
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    total *= 1.1  # Tax

    # Send notification
    send_email(order.customer, f"Order total: {total}")

# After
def calculate_total(items):
    subtotal = sum(item.price * item.quantity for item in items)
    return subtotal * 1.1

def process_order(order):
    total = calculate_total(order.items)
    send_email(order.customer, f"Order total: {total}")
"""
    },
    "replace_conditional_with_polymorphism": {
        "description": "Replace type-checking conditionals with polymorphic behavior",
        "when_to_use": [
            "Switch/if statements based on type",
            "Same conditional structure repeated",
            "Adding new types requires modifying existing code"
        ],
        "example": """
# Before
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height

# After
class Circle:
    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle:
    def area(self):
        return self.width * self.height
"""
    },
    "introduce_parameter_object": {
        "description": "Replace a group of parameters with an object",
        "when_to_use": [
            "Multiple functions take same group of parameters",
            "Parameters are naturally related",
            "Function has too many parameters"
        ],
        "example": """
# Before
def create_invoice(customer_name, customer_email, customer_address,
                   customer_phone, items, discount):
    ...

# After
@dataclass
class Customer:
    name: str
    email: str
    address: str
    phone: str

def create_invoice(customer: Customer, items, discount):
    ...
"""
    },
    "replace_temp_with_query": {
        "description": "Replace a temporary variable with a method call",
        "when_to_use": [
            "Temporary variable holds result of expression",
            "Expression is used multiple times",
            "Expression logic could be reused"
        ],
        "example": """
# Before
def get_discount(order):
    base_price = order.quantity * order.price
    if base_price > 1000:
        return base_price * 0.1
    return 0

# After
def get_discount(order):
    if base_price(order) > 1000:
        return base_price(order) * 0.1
    return 0

def base_price(order):
    return order.quantity * order.price
"""
    },
    "decompose_conditional": {
        "description": "Extract condition and branches into separate methods",
        "when_to_use": [
            "Complex conditional logic",
            "Condition is hard to understand",
            "Same condition used elsewhere"
        ],
        "example": """
# Before
if date.before(SUMMER_START) or date.after(SUMMER_END):
    charge = quantity * winter_rate + winter_service_charge
else:
    charge = quantity * summer_rate

# After
if is_winter(date):
    charge = winter_charge(quantity)
else:
    charge = summer_charge(quantity)
"""
    }
}


def analyze_function_length(code: str) -> list[dict]:
    """Analyze functions for length issues."""
    issues = []

    # Simple pattern matching for function definitions
    function_pattern = r'(def|function|async function)\s+(\w+)'

    lines = code.split('\n')
    current_func = None
    func_start = 0
    indent_level = 0

    for i, line in enumerate(lines):
        match = re.match(function_pattern, line.strip())
        if match:
            if current_func and (i - func_start) > CODE_SMELLS["long_function"]["threshold"]:
                issues.append({
                    "smell": "long_function",
                    "location": f"Line {func_start + 1}",
                    "function": current_func,
                    "lines": i - func_start,
                    "suggestion": CODE_SMELLS["long_function"]["suggestion"]
                })
            current_func = match.group(2)
            func_start = i

    return issues


def analyze_nesting_depth(code: str) -> list[dict]:
    """Analyze code for deep nesting."""
    issues = []
    max_depth = 0
    current_depth = 0

    for i, line in enumerate(code.split('\n')):
        # Count indent changes (simplified)
        stripped = line.lstrip()
        if stripped.startswith(('if ', 'for ', 'while ', 'try:', 'with ')):
            current_depth += 1
            if current_depth > max_depth:
                max_depth = current_depth
            if current_depth > CODE_SMELLS["deep_nesting"]["threshold"]:
                issues.append({
                    "smell": "deep_nesting",
                    "location": f"Line {i + 1}",
                    "depth": current_depth,
                    "suggestion": CODE_SMELLS["deep_nesting"]["suggestion"]
                })
        elif stripped in ('', '}') or stripped.startswith(('return', 'break', 'continue')):
            current_depth = max(0, current_depth - 1)

    return issues


def analyze_parameters(code: str) -> list[dict]:
    """Analyze functions for too many parameters."""
    issues = []

    # Match function definitions with parameters
    pattern = r'(def|function)\s+(\w+)\s*\(([^)]*)\)'

    for match in re.finditer(pattern, code):
        func_name = match.group(2)
        params_str = match.group(3)

        if params_str.strip():
            params = [p.strip() for p in params_str.split(',') if p.strip()]
            # Filter out self/this
            params = [p for p in params if p not in ('self', 'this', 'cls')]

            if len(params) > CODE_SMELLS["long_parameter_list"]["threshold"]:
                issues.append({
                    "smell": "long_parameter_list",
                    "function": func_name,
                    "count": len(params),
                    "suggestion": CODE_SMELLS["long_parameter_list"]["suggestion"]
                })

    return issues


def suggest_refactoring(smell_type: str) -> dict:
    """Get refactoring suggestion for a smell type."""
    mapping = {
        "long_function": "extract_method",
        "deep_nesting": "decompose_conditional",
        "long_parameter_list": "introduce_parameter_object",
        "duplicate_code": "extract_method",
        "magic_numbers": "replace_temp_with_query"
    }

    pattern_name = mapping.get(smell_type)
    if pattern_name and pattern_name in REFACTORING_PATTERNS:
        return REFACTORING_PATTERNS[pattern_name]

    return {"description": "Review code for potential improvements"}


def generate_refactoring_report(code: str) -> str:
    """Generate a comprehensive refactoring report."""
    issues = []
    issues.extend(analyze_function_length(code))
    issues.extend(analyze_nesting_depth(code))
    issues.extend(analyze_parameters(code))

    if not issues:
        return "No significant code smells detected."

    report = "# Refactoring Analysis Report\n\n"
    report += f"Found {len(issues)} potential issue(s):\n\n"

    for i, issue in enumerate(issues, 1):
        smell = CODE_SMELLS.get(issue["smell"], {})
        report += f"## Issue {i}: {smell.get('description', issue['smell'])}\n"
        report += f"- **Location**: {issue.get('location', 'Unknown')}\n"
        report += f"- **Severity**: {smell.get('severity', 'medium')}\n"
        report += f"- **Suggestion**: {issue.get('suggestion', 'Review this code')}\n\n"

        pattern = suggest_refactoring(issue["smell"])
        if pattern.get("example"):
            report += f"### Refactoring Pattern: {pattern['description']}\n"
            report += f"```python{pattern['example']}```\n\n"

    return report


def list_patterns() -> str:
    """List all refactoring patterns."""
    output = "Available Refactoring Patterns:\n" + "=" * 40 + "\n\n"

    for name, pattern in REFACTORING_PATTERNS.items():
        output += f"**{name}**\n"
        output += f"  {pattern['description']}\n"
        output += "  When to use:\n"
        for use in pattern["when_to_use"]:
            output += f"    - {use}\n"
        output += "\n"

    return output


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--patterns":
            print(list_patterns())

        elif cmd == "--smells":
            print("Code Smells:\n" + "=" * 40)
            for name, smell in CODE_SMELLS.items():
                print(f"\n{name}")
                print(f"  {smell['description']}")
                print(f"  Severity: {smell['severity']}")

        elif cmd == "--analyze":
            if len(sys.argv) > 2:
                with open(sys.argv[2], 'r') as f:
                    code = f.read()
                print(generate_refactoring_report(code))
            else:
                print("Usage: --analyze <file>")

        elif cmd == "--pattern":
            pattern_name = sys.argv[2] if len(sys.argv) > 2 else None
            if pattern_name and pattern_name in REFACTORING_PATTERNS:
                pattern = REFACTORING_PATTERNS[pattern_name]
                print(f"# {pattern_name}\n")
                print(pattern["description"])
                print("\nWhen to use:")
                for use in pattern["when_to_use"]:
                    print(f"  - {use}")
                if pattern.get("example"):
                    print(f"\nExample:{pattern['example']}")
            else:
                print(f"Unknown pattern. Available: {', '.join(REFACTORING_PATTERNS.keys())}")
    else:
        print("Refactor Analyzer")
        print("Usage:")
        print("  --patterns           List refactoring patterns")
        print("  --smells             List code smells")
        print("  --analyze <file>     Analyze a file")
        print("  --pattern <name>     Show pattern details")

import ast
import re


def analyze_python_code(code: str) -> dict:
    lines = code.split("\n")
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))

    result = {
        "total_lines": total_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "functions": [],
        "classes": [],
        "imports": [],
        "has_docstrings": False,
        "has_type_hints": False,
        "has_try_except": False,
        "has_main_guard": False,
        "nested_loops": 0,
        "variable_names": [],
    }

    # Check for if __name__ == "__main__" guard
    result["has_main_guard"] = bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', code))

    try:
        tree = ast.parse(code)
    except SyntaxError:
        result["parse_error"] = True
        return result

    for node in ast.walk(tree):
        # Functions
        if isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)
            # Check for docstrings
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
                result["has_docstrings"] = True
            # Check for type hints
            if node.returns or any(arg.annotation for arg in node.args.args):
                result["has_type_hints"] = True

        # Classes
        elif isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)

        # Imports
        elif isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            result["imports"].append(node.module or "")

        # Try/except
        elif isinstance(node, ast.Try):
            result["has_try_except"] = True

        # Variable assignments (top-level names)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result["variable_names"].append(target.id)

        # Nested loops
        elif isinstance(node, (ast.For, ast.While)):
            for child in ast.walk(node):
                if child is not node and isinstance(child, (ast.For, ast.While)):
                    result["nested_loops"] += 1
                    break  # count once per outer loop

    return result


def format_analysis_for_prompt(analysis: dict) -> str:
    if analysis.get("parse_error"):
        return "Static analysis failed: code has syntax errors."

    parts = [
        f"Lines of code: {analysis['total_lines']} ({analysis['comment_lines']} comments, {analysis['blank_lines']} blank)",
        f"Functions: {', '.join(analysis['functions']) or 'none'}",
        f"Classes: {', '.join(analysis['classes']) or 'none'}",
        f"Imports: {', '.join(analysis['imports']) or 'none'}",
        f"Docstrings: {'yes' if analysis['has_docstrings'] else 'no'}",
        f"Type hints: {'yes' if analysis['has_type_hints'] else 'no'}",
        f"Try/except: {'yes' if analysis['has_try_except'] else 'no'}",
        f"Main guard: {'yes' if analysis['has_main_guard'] else 'no'}",
        f"Nested loops: {analysis['nested_loops']}",
    ]

    if analysis["variable_names"]:
        parts.append(f"Variable names: {', '.join(analysis['variable_names'][:15])}")

    return "\n".join(parts)

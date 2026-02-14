import ast
import re


def _max_nesting_depth(node, current=0):
    """Recursively compute the maximum nesting depth of loops/conditionals."""
    max_depth = current
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While, ast.If, ast.With)):
            max_depth = max(max_depth, _max_nesting_depth(child, current + 1))
        else:
            max_depth = max(max_depth, _max_nesting_depth(child, current))
    return max_depth


def _function_line_count(node):
    """Return the number of lines a function spans."""
    if hasattr(node, "end_lineno") and node.end_lineno and node.lineno:
        return node.end_lineno - node.lineno + 1
    return len(ast.dump(node).split("\n"))


def assess_naming(variable_names: list[str]) -> str:
    """Heuristic assessment of variable naming quality."""
    if not variable_names:
        return "N/A"
    single_char = [v for v in variable_names if len(v) == 1 and v not in ("i", "j", "k", "x", "y", "_")]
    total = len(variable_names)
    single_char_count = len(single_char)
    if single_char_count == 0:
        return "good"
    if single_char_count / total < 0.3:
        return "mixed"
    return "poor"


def analyze_python_code(code: str) -> dict:
    lines = code.split("\n")
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
    code_lines = total_lines - blank_lines - comment_lines

    result = {
        "total_lines": total_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "comment_ratio": round(comment_lines / max(code_lines, 1), 2),
        "functions": [],
        "classes": [],
        "imports": [],
        "has_docstrings": False,
        "has_type_hints": False,
        "has_error_handling": False,
        "has_main_guard": False,
        "has_tests": False,
        "nested_loops": 0,
        "max_nesting_depth": 0,
        "longest_function_lines": 0,
        "variable_names": [],
        "single_char_vars": [],
        "naming_quality": "N/A",
        "is_valid_syntax": True,
        "syntax_error": None,
    }

    result["has_main_guard"] = bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', code))

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result["is_valid_syntax"] = False
        result["syntax_error"] = str(e)
        return result

    result["max_nesting_depth"] = _max_nesting_depth(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)
            # Check for docstrings
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
                result["has_docstrings"] = True
            # Check for type hints
            if node.returns or any(arg.annotation for arg in node.args.args):
                result["has_type_hints"] = True
            # Track longest function
            func_lines = _function_line_count(node)
            if func_lines > result["longest_function_lines"]:
                result["longest_function_lines"] = func_lines
            # Check for test functions
            if node.name.startswith("test_"):
                result["has_tests"] = True

        elif isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            result["imports"].append(node.module or "")

        elif isinstance(node, ast.Try):
            result["has_error_handling"] = True

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result["variable_names"].append(target.id)

        elif isinstance(node, (ast.For, ast.While)):
            for child in ast.walk(node):
                if child is not node and isinstance(child, (ast.For, ast.While)):
                    result["nested_loops"] += 1
                    break

        # Check for assert statements (test patterns)
        elif isinstance(node, ast.Assert):
            result["has_tests"] = True

    # Naming analysis
    result["single_char_vars"] = [v for v in result["variable_names"] if len(v) == 1]
    result["naming_quality"] = assess_naming(result["variable_names"])

    return result


def format_analysis_for_prompt(analysis: dict) -> str:
    if not analysis.get("is_valid_syntax", True):
        return f"Static analysis failed: code has syntax errors. ({analysis.get('syntax_error', '')})"

    parts = [
        f"Lines of code: {analysis['total_lines']} ({analysis['comment_lines']} comments, {analysis['blank_lines']} blank)",
        f"Comment ratio: {analysis['comment_ratio']}",
        f"Functions: {', '.join(analysis['functions']) or 'none'} (count: {len(analysis['functions'])})",
        f"Longest function: {analysis['longest_function_lines']} lines",
        f"Classes: {', '.join(analysis['classes']) or 'none'}",
        f"Imports: {', '.join(analysis['imports']) or 'none'}",
        f"Docstrings: {'yes' if analysis['has_docstrings'] else 'no'}",
        f"Type hints: {'yes' if analysis['has_type_hints'] else 'no'}",
        f"Error handling (try/except): {'yes' if analysis['has_error_handling'] else 'no'}",
        f"Main guard: {'yes' if analysis['has_main_guard'] else 'no'}",
        f"Has tests: {'yes' if analysis['has_tests'] else 'no'}",
        f"Nested loops: {analysis['nested_loops']}",
        f"Max nesting depth: {analysis['max_nesting_depth']}",
        f"Naming quality: {analysis['naming_quality']}",
    ]

    if analysis["single_char_vars"]:
        parts.append(f"Single-char variables: {', '.join(analysis['single_char_vars'])}")

    if analysis["variable_names"]:
        parts.append(f"Variable names: {', '.join(analysis['variable_names'][:15])}")

    return "\n".join(parts)

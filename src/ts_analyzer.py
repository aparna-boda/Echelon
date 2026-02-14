"""Tree-sitter-based static analysis for non-Python languages."""

import re
from src.analyzer import assess_naming

# Maps Echelon language names to tree-sitter parser names
LANGUAGE_TO_PARSER = {
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "Java": "java",
    "C": "c",
    "C++": "cpp",
    "Go": "go",
    "Ruby": "ruby",
    "Rust": "rust",
}

# Per-language node type configuration
_LANGUAGE_CONFIG = {
    "javascript": {
        "function_nodes": {"function_declaration", "arrow_function", "method_definition"},
        "class_nodes": {"class_declaration"},
        "import_nodes": {"import_statement"},
        "comment_nodes": {"comment"},
        "error_handling_nodes": {"try_statement"},
        "loop_nodes": {"for_statement", "for_in_statement", "while_statement", "do_statement"},
        "conditional_nodes": {"if_statement", "switch_statement"},
        "assignment_nodes": {"variable_declarator"},
        "has_static_types": False,
        "main_guard_check": None,
        "docstring_pattern": "/**",
        "require_import": True,
    },
    "typescript": {
        "function_nodes": {"function_declaration", "arrow_function", "method_definition"},
        "class_nodes": {"class_declaration"},
        "import_nodes": {"import_statement"},
        "comment_nodes": {"comment"},
        "error_handling_nodes": {"try_statement"},
        "loop_nodes": {"for_statement", "for_in_statement", "while_statement", "do_statement"},
        "conditional_nodes": {"if_statement", "switch_statement"},
        "assignment_nodes": {"variable_declarator"},
        "has_static_types": True,
        "main_guard_check": None,
        "docstring_pattern": "/**",
        "require_import": True,
    },
    "java": {
        "function_nodes": {"method_declaration", "constructor_declaration"},
        "class_nodes": {"class_declaration", "interface_declaration"},
        "import_nodes": {"import_declaration"},
        "comment_nodes": {"line_comment", "block_comment"},
        "error_handling_nodes": {"try_statement"},
        "loop_nodes": {"for_statement", "enhanced_for_statement", "while_statement", "do_statement"},
        "conditional_nodes": {"if_statement", "switch_expression"},
        "assignment_nodes": {"variable_declarator"},
        "has_static_types": True,
        "main_guard_check": "public static void main",
        "docstring_pattern": "/**",
        "require_import": False,
    },
    "c": {
        "function_nodes": {"function_definition"},
        "class_nodes": {"struct_specifier"},
        "import_nodes": {"preproc_include"},
        "comment_nodes": {"comment"},
        "error_handling_nodes": set(),
        "loop_nodes": {"for_statement", "while_statement", "do_statement"},
        "conditional_nodes": {"if_statement", "switch_statement"},
        "assignment_nodes": {"init_declarator"},
        "has_static_types": True,
        "main_guard_check": "int main",
        "docstring_pattern": "/**",
        "require_import": False,
    },
    "cpp": {
        "function_nodes": {"function_definition"},
        "class_nodes": {"class_specifier", "struct_specifier"},
        "import_nodes": {"preproc_include"},
        "comment_nodes": {"comment"},
        "error_handling_nodes": {"try_statement"},
        "loop_nodes": {"for_statement", "for_range_loop", "while_statement", "do_statement"},
        "conditional_nodes": {"if_statement", "switch_statement"},
        "assignment_nodes": {"init_declarator"},
        "has_static_types": True,
        "main_guard_check": "int main",
        "docstring_pattern": "/**",
        "require_import": False,
    },
    "go": {
        "function_nodes": {"function_declaration", "method_declaration"},
        "class_nodes": {"type_declaration"},
        "import_nodes": {"import_declaration"},
        "comment_nodes": {"comment"},
        "error_handling_nodes": set(),  # Go uses `if err != nil` — handled via heuristic
        "loop_nodes": {"for_statement"},
        "conditional_nodes": {"if_statement", "expression_switch_statement", "type_switch_statement"},
        "assignment_nodes": {"short_var_declaration", "var_declaration"},
        "has_static_types": True,
        "main_guard_check": "func main()",
        "docstring_pattern": "//",
        "require_import": False,
        "error_heuristic": "if err != nil",
    },
    "ruby": {
        "function_nodes": {"method", "singleton_method"},
        "class_nodes": {"class", "module"},
        "import_nodes": set(),  # Ruby uses require() calls — handled via heuristic
        "comment_nodes": {"comment"},
        "error_handling_nodes": {"begin"},
        "loop_nodes": {"for", "while", "until"},
        "conditional_nodes": {"if", "unless", "case"},
        "assignment_nodes": {"assignment"},
        "has_static_types": False,
        "main_guard_check": 'if __FILE__ == $0',
        "docstring_pattern": "##",
        "require_import": True,
    },
    "rust": {
        "function_nodes": {"function_item"},
        "class_nodes": {"struct_item", "enum_item", "trait_item"},
        "import_nodes": {"use_declaration"},
        "comment_nodes": {"line_comment", "block_comment"},
        "error_handling_nodes": set(),  # Rust uses ? operator — handled via heuristic
        "loop_nodes": {"for_expression", "while_expression", "loop_expression"},
        "conditional_nodes": {"if_expression", "match_expression"},
        "assignment_nodes": {"let_declaration"},
        "has_static_types": True,
        "main_guard_check": "fn main()",
        "docstring_pattern": "///",
        "require_import": False,
        "error_heuristic": "?",
    },
}


def _get_parser(language: str):
    """Return (parser, config) for a given Echelon language name."""
    parser_name = LANGUAGE_TO_PARSER.get(language)
    if parser_name is None:
        return None, None

    config = _LANGUAGE_CONFIG.get(parser_name)
    if config is None:
        return None, None

    from tree_sitter_language_pack import get_parser
    parser = get_parser(parser_name)
    return parser, config


def _walk_tree(node):
    """Depth-first generator yielding all nodes in the tree."""
    yield node
    for child in node.children:
        yield from _walk_tree(child)


def _get_node_text(node, code_bytes: bytes) -> str:
    """Extract source text for a node."""
    return code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _extract_function_name(node, code_bytes: bytes, config: dict) -> str | None:
    """Get the name of a function/method node."""
    # Most languages have a 'name' field child
    for child in node.children:
        if child.type in ("identifier", "property_identifier"):
            return _get_node_text(child, code_bytes)

    # Arrow functions: check if parent is a variable_declarator
    if node.type == "arrow_function" and node.parent and node.parent.type == "variable_declarator":
        for child in node.parent.children:
            if child.type == "identifier":
                return _get_node_text(child, code_bytes)

    return None


def _extract_class_name(node, code_bytes: bytes) -> str | None:
    """Get the name of a class/struct/enum/trait node."""
    for child in node.children:
        if child.type in ("identifier", "type_identifier"):
            return _get_node_text(child, code_bytes)
    return None


def _max_nesting_depth(node, config: dict, current: int = 0) -> int:
    """Recursively compute the maximum nesting depth of loops/conditionals."""
    nesting_nodes = config["loop_nodes"] | config["conditional_nodes"]
    max_depth = current
    for child in node.children:
        if child.type in nesting_nodes:
            max_depth = max(max_depth, _max_nesting_depth(child, config, current + 1))
        else:
            max_depth = max(max_depth, _max_nesting_depth(child, config, current))
    return max_depth


def _count_nested_loops(node, config: dict) -> int:
    """Count loop nodes that contain other loop nodes."""
    count = 0
    loop_types = config["loop_nodes"]

    for child in _walk_tree(node):
        if child.type in loop_types:
            # Check if this loop contains another loop
            for descendant in _walk_tree(child):
                if descendant is not child and descendant.type in loop_types:
                    count += 1
                    break
    return count


def _function_line_count(node) -> int:
    """Return the number of lines a function spans."""
    return node.end_point[0] - node.start_point[0] + 1


def _extract_variable_name(node, code_bytes: bytes, config: dict) -> str | None:
    """Extract the variable name from an assignment/declaration node."""
    for child in node.children:
        if child.type in ("identifier", "name"):
            return _get_node_text(child, code_bytes)
    return None


def analyze_code_treesitter(code: str, language: str) -> dict:
    """
    Analyze code using tree-sitter and return the same dict shape as analyze_python_code().

    Args:
        code: Source code string
        language: Echelon language name (e.g. "JavaScript", "Java")

    Returns:
        dict with the same keys as analyze_python_code()
    """
    parser, config = _get_parser(language)
    if parser is None:
        return None

    lines = code.split("\n")
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())

    code_bytes = code.encode("utf-8")
    tree = parser.parse(code_bytes)

    # Syntax validity
    is_valid_syntax = not tree.root_node.has_error
    syntax_error = None
    if not is_valid_syntax:
        for node in _walk_tree(tree.root_node):
            if node.type == "ERROR":
                row, col = node.start_point
                syntax_error = f"Syntax error at line {row + 1}, column {col}"
                break
        if syntax_error is None:
            syntax_error = "Syntax error detected"

    # Walk the tree and collect data
    functions = []
    classes = []
    imports = []
    comment_lines_count = 0
    has_docstrings = False
    has_error_handling = False
    has_tests = False
    longest_function_lines = 0
    variable_names = []
    comment_texts = []

    for node in _walk_tree(tree.root_node):
        node_type = node.type

        # Functions
        if node_type in config["function_nodes"]:
            name = _extract_function_name(node, code_bytes, config)
            if name:
                functions.append(name)
                # Check for test functions
                if name.startswith("test") or name.startswith("Test"):
                    has_tests = True

            # Track longest function
            fl = _function_line_count(node)
            if fl > longest_function_lines:
                longest_function_lines = fl

        # Classes
        elif node_type in config["class_nodes"]:
            name = _extract_class_name(node, code_bytes)
            if name:
                classes.append(name)

        # Imports
        elif node_type in config["import_nodes"]:
            imports.append(_get_node_text(node, code_bytes).strip())

        # Comments
        elif node_type in config["comment_nodes"]:
            text = _get_node_text(node, code_bytes)
            comment_texts.append(text)
            # Count comment lines (multi-line comments span multiple lines)
            comment_lines_count += text.count("\n") + 1
            # Check for docstring patterns
            if config["docstring_pattern"] and text.startswith(config["docstring_pattern"]):
                has_docstrings = True

        # Error handling
        elif config["error_handling_nodes"] and node_type in config["error_handling_nodes"]:
            has_error_handling = True

        # Assignments / variable declarations
        elif node_type in config["assignment_nodes"]:
            var_name = _extract_variable_name(node, code_bytes, config)
            if var_name:
                variable_names.append(var_name)

    # Ruby: detect require() calls as imports
    if config.get("require_import") and language == "Ruby":
        for match in re.finditer(r'require\s*[\(]?\s*["\']([^"\']+)["\']', code):
            imports.append(match.group(1))

    # JS/TS: detect require() calls as additional imports
    if config.get("require_import") and language in ("JavaScript", "TypeScript"):
        for match in re.finditer(r'require\s*\(\s*["\']([^"\']+)["\']', code):
            imports.append(match.group(1))

    # Go error handling heuristic: if err != nil
    if config.get("error_heuristic") and not has_error_handling:
        if config["error_heuristic"] in code:
            has_error_handling = True

    # Rust error handling heuristic: ? operator
    if language == "Rust" and not has_error_handling:
        # Look for ? operator usage (not in comments)
        if re.search(r'[a-zA-Z_]\w*\?\s*[;,)]', code):
            has_error_handling = True

    # Main guard detection
    has_main_guard = False
    if config["main_guard_check"]:
        has_main_guard = config["main_guard_check"] in code

    # Test detection via assert patterns
    if not has_tests:
        if re.search(r'\b(assert|expect|describe|it|test)\s*[\(.]', code):
            has_tests = True

    # Type hints: statically typed languages always have type hints
    has_type_hints = config["has_static_types"]
    # For JS/TS: check for JSDoc @type or TypeScript type annotations
    if language == "TypeScript":
        has_type_hints = True
    elif language == "JavaScript":
        # Check for JSDoc type annotations
        has_type_hints = any("@type" in c or "@param" in c or "@returns" in c for c in comment_texts)

    # Compute derived metrics
    code_lines = total_lines - blank_lines - comment_lines_count
    comment_ratio = round(comment_lines_count / max(code_lines, 1), 2)
    single_char_vars = [v for v in variable_names if len(v) == 1]
    naming_quality = assess_naming(variable_names)

    return {
        "total_lines": total_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines_count,
        "comment_ratio": comment_ratio,
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "has_docstrings": has_docstrings,
        "has_type_hints": has_type_hints,
        "has_error_handling": has_error_handling,
        "has_main_guard": has_main_guard,
        "has_tests": has_tests,
        "nested_loops": _count_nested_loops(tree.root_node, config),
        "max_nesting_depth": _max_nesting_depth(tree.root_node, config),
        "longest_function_lines": longest_function_lines,
        "variable_names": variable_names,
        "single_char_vars": single_char_vars,
        "naming_quality": naming_quality,
        "is_valid_syntax": is_valid_syntax,
        "syntax_error": syntax_error,
    }

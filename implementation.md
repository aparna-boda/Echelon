 Plan to implement                                                                                                                                                            │
│                                                                                                                                                                              │
│ Multi-Language Static Analysis via tree-sitter                                                                                                                               │
│                                                                                                                                                                              │
│ Context                                                                                                                                                                      │
│                                                                                                                                                                              │
│ Echelon's static analysis currently only works for Python (via ast module). For all other languages (JS, Java, C, C++, Go, Ruby, Rust), the evaluator sends "Not available   │
│ (static analysis only supports Python)" to the LLM and skips the Static Analysis UI section entirely. This means non-Python submissions get weaker evaluations — the LLM has │
│  no structural metrics to anchor its scoring.                                                                                                                                │
│                                                                                                                                                                              │
│ Goal: Extend static analysis to JavaScript, TypeScript, Java, C, C++, Go, Ruby, and Rust using tree-sitter-language-pack — a maintained package with pre-compiled grammars   │
│ for 165+ languages. The Python analyzer stays untouched.                                                                                                                     │
│                                                                                                                                                                              │
│ File to Create                                                                                                                                                               │
│                                                                                                                                                                              │
│ - src/ts_analyzer.py — tree-sitter-based analysis engine (~350 lines)                                                                                                        │
│                                                                                                                                                                              │
│ Files to Modify                                                                                                                                                              │
│                                                                                                                                                                              │
│ - src/analyzer.py — Add analyze_code() dispatcher (keep existing code untouched)                                                                                             │
│ - src/evaluator.py — Use dispatcher instead of Python-only conditional                                                                                                       │
│ - app.py — Update "Python AST inspection results" subtitle to be language-aware                                                                                              │
│ - src/report_generator.py — Update "Static Analysis (Python AST)" PDF heading                                                                                                │
│ - requirements.txt — Add tree-sitter-language-pack                                                                                                                           │
│                                                                                                                                                                              │
│ Design: src/ts_analyzer.py                                                                                                                                                   │
│                                                                                                                                                                              │
│ Language registry                                                                                                                                                            │
│                                                                                                                                                                              │
│ Map Echelon language names to tree-sitter parser names and per-language node type config:                                                                                    │
│                                                                                                                                                                              │
│ LANGUAGE_TO_PARSER = {                                                                                                                                                       │
│     "JavaScript": "javascript", "TypeScript": "typescript",                                                                                                                  │
│     "Java": "java", "C": "c", "C++": "cpp",                                                                                                                                  │
│     "Go": "go", "Ruby": "ruby", "Rust": "rust",                                                                                                                              │
│ }                                                                                                                                                                            │
│                                                                                                                                                                              │
│ Each language gets a config dict specifying:                                                                                                                                 │
│ - function_nodes — node types for function/method declarations                                                                                                               │
│ - class_nodes — node types for class/struct/interface                                                                                                                        │
│ - import_nodes — node types for imports/includes                                                                                                                             │
│ - comment_nodes — node types for comments                                                                                                                                    │
│ - error_handling_nodes — try/catch equivalents (empty for C, Go, Rust)                                                                                                       │
│ - loop_nodes / conditional_nodes — for nesting depth calculation                                                                                                             │
│ - assignment_nodes — for variable name extraction                                                                                                                            │
│ - has_static_types — True for Java/C/C++/Go/Rust (always report has_type_hints=True)                                                                                         │
│ - main_guard_check — string pattern to search for (e.g. "public static void main" for Java, "int main" for C/C++)                                                            │
│ - docstring_pattern — "/**" for JSDoc/Javadoc, "///" for Rust, etc.                                                                                                          │
│                                                                                                                                                                              │
│ Node types per language                                                                                                                                                      │
│ ┌──────────┬─────────────────────────────────────────────────────┬───────────────────────────────────────┬────────────────────────────┬───────────────────────────────────── │
│ ┐                                                                                                                                                                            │
│ │ Language │                      Functions                      │                Classes                │          Imports           │           Error Handling             │
│ │                                                                                                                                                                            │
│ ├──────────┼─────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────┼───────────────────────────────────── │
│ ┤                                                                                                                                                                            │
│ │ JS/TS    │ function_declaration, arrow_function,               │ class_declaration                     │ import_statement +         │ try_statement                        │
│ │                                                                                                                                                                            │
│ │          │ method_definition                                   │                                       │ require()                  │                                      │
│ │                                                                                                                                                                            │
│ ├──────────┼─────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────┼───────────────────────────────────── │
│ ┤                                                                                                                                                                            │
│ │ Java     │ method_declaration, constructor_declaration         │ class_declaration,                    │ import_declaration         │ try_statement                        │
│ │                                                                                                                                                                            │
│ │          │                                                     │ interface_declaration                 │                            │                                      │
│ │                                                                                                                                                                            │
│ ├──────────┼─────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────┼───────────────────────────────────── │
│ ┤                                                                                                                                                                            │
│ │ C        │ function_definition                                 │ struct_specifier                      │ preproc_include            │ (none)                               │
│ │                                                                                                                                                                            │
│ ├──────────┼─────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────┼───────────────────────────────────── │
│ ┤                                                                                                                                                                            │
│ │ C++      │ function_definition                                 │ class_specifier, struct_specifier     │ preproc_include            │ try_statement                        │
│ │                                                                                                                                                                            │
│ ├──────────┼─────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────┼───────────────────────────────────── │
│ ┤                                                                                                                                                                            │
│ │ Go       │ function_declaration, method_declaration            │ type_declaration                      │ import_declaration         │ heuristic: if err != nil             │
│ │                                                                                                                                                                            │
│ ├──────────┼─────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────┼───────────────────────────────────── │
│ ┤                                                                                                                                                                            │
│ │ Ruby     │ method, singleton_method                            │ class, module                         │ require() calls            │ begin (rescue)                       │
│ │                                                                                                                                                                            │
│ ├──────────┼─────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────┼───────────────────────────────────── │
│ ┤                                                                                                                                                                            │
│ │ Rust     │ function_item                                       │ struct_item, enum_item, trait_item    │ use_declaration            │ heuristic: ? operator /              │
│ │                                                                                                                                                                            │
│ │          │                                                     │                                       │                            │ try_expression                       │
│ │                                                                                                                                                                            │
│ └──────────┴─────────────────────────────────────────────────────┴───────────────────────────────────────┴────────────────────────────┴───────────────────────────────────── │
│ ┘                                                                                                                                                                            │
│ Main function                                                                                                                                                                │
│                                                                                                                                                                              │
│ def analyze_code_treesitter(code: str, language: str) -> dict:                                                                                                               │
│                                                                                                                                                                              │
│ Returns the exact same dict shape as analyze_python_code():                                                                                                                  │
│ {                                                                                                                                                                            │
│     "total_lines", "blank_lines", "comment_lines", "comment_ratio",                                                                                                          │
│     "functions", "classes", "imports",                                                                                                                                       │
│     "has_docstrings", "has_type_hints", "has_error_handling",                                                                                                                │
│     "has_main_guard", "has_tests",                                                                                                                                           │
│     "nested_loops", "max_nesting_depth", "longest_function_lines",                                                                                                           │
│     "variable_names", "single_char_vars", "naming_quality",                                                                                                                  │
│     "is_valid_syntax", "syntax_error",                                                                                                                                       │
│ }                                                                                                                                                                            │
│                                                                                                                                                                              │
│ Internal helpers                                                                                                                                                             │
│                                                                                                                                                                              │
│ - _get_parser(language) — returns (parser, config) from tree_sitter_language_pack.get_parser()                                                                               │
│ - _walk_tree(node) — depth-first generator yielding all nodes                                                                                                                │
│ - _get_node_text(node, code_bytes) — extract source text for a node                                                                                                          │
│ - _extract_function_name(node, code_bytes, config) — get name from a function node's "name" field child; for arrow functions, check parent variable_declarator               │
│ - _extract_class_name(node, code_bytes) — get name from identifier/type_identifier child                                                                                     │
│ - _max_nesting_depth(node, config) — recursive depth for loop+conditional nodes                                                                                              │
│ - _count_nested_loops(node, config) — count loops containing other loops                                                                                                     │
│ - _function_line_count(node) — node.end_point[0] - node.start_point[0] + 1                                                                                                   │
│                                                                                                                                                                              │
│ Syntax validity: check tree.root_node.has_error; walk for ERROR nodes to get position.                                                                                       │
│                                                                                                                                                                              │
│ Naming quality: reuse existing assess_naming() from src/analyzer.py.                                                                                                         │
│                                                                                                                                                                              │
│ Changes to Existing Files                                                                                                                                                    │
│                                                                                                                                                                              │
│ src/analyzer.py — Add dispatcher (append, don't modify existing code)                                                                                                        │
│                                                                                                                                                                              │
│ def analyze_code(code: str, language: str) -> dict | None:                                                                                                                   │
│     if language.lower() == "python":                                                                                                                                         │
│         return analyze_python_code(code)                                                                                                                                     │
│     try:                                                                                                                                                                     │
│         from src.ts_analyzer import analyze_code_treesitter, LANGUAGE_TO_PARSER                                                                                              │
│         if language in LANGUAGE_TO_PARSER:                                                                                                                                   │
│             return analyze_code_treesitter(code, language)                                                                                                                   │
│     except ImportError:                                                                                                                                                      │
│         pass  # graceful degradation if tree-sitter not installed                                                                                                            │
│     return None                                                                                                                                                              │
│                                                                                                                                                                              │
│ src/evaluator.py — Replace Python-only block (lines 18-23)                                                                                                                   │
│                                                                                                                                                                              │
│ Before:                                                                                                                                                                      │
│ static_analysis_result = None                                                                                                                                                │
│ static_analysis_text = "Not available (static analysis only supports Python)"                                                                                                │
│ if language.lower() == "python":                                                                                                                                             │
│     static_analysis_result = analyze_python_code(code)                                                                                                                       │
│     static_analysis_text = format_analysis_for_prompt(static_analysis_result)                                                                                                │
│ After:                                                                                                                                                                       │
│ static_analysis_result = analyze_code(code, language)                                                                                                                        │
│ if static_analysis_result is not None:                                                                                                                                       │
│     static_analysis_text = format_analysis_for_prompt(static_analysis_result)                                                                                                │
│ else:                                                                                                                                                                        │
│     static_analysis_text = f"Not available (static analysis not supported for {language})"                                                                                   │
│ Also update the import from analyze_python_code to analyze_code.                                                                                                             │
│                                                                                                                                                                              │
│ app.py line 995 — Update subtitle                                                                                                                                            │
│                                                                                                                                                                              │
│ "Python AST inspection results"  →  dynamic based on language                                                                                                                │
│                                                                                                                                                                              │
│ src/report_generator.py line 178 — Update heading                                                                                                                            │
│                                                                                                                                                                              │
│ "Static Analysis (Python AST)"  →  dynamic based on result["language"]                                                                                                       │
│                                                                                                                                                                              │
│ requirements.txt — Add line                                                                                                                                                  │
│                                                                                                                                                                              │
│ tree-sitter-language-pack                                                                                                                                                    │
│                                                                                                                                                                              │
│ What stays unchanged                                                                                                                                                         │
│                                                                                                                                                                              │
│ - analyze_python_code() — untouched, continues using Python ast                                                                                                              │
│ - format_analysis_for_prompt() — works on the dict shape, no changes needed                                                                                                  │
│ - src/scoring.py, src/prompts.py, src/llm_client.py, src/utils.py — no changes                                                                                               │
│ - UI metric pills and PDF table — already read from the dict generically                                                                                                     │
│                                                                                                                                                                              │
│ Implementation Steps                                                                                                                                                         │
│                                                                                                                                                                              │
│ 1. pip install tree-sitter-language-pack and add to requirements.txt                                                                                                         │
│ 2. Create src/ts_analyzer.py with language config registry and analyze_code_treesitter()                                                                                     │
│ 3. Add analyze_code() dispatcher to src/analyzer.py                                                                                                                          │
│ 4. Update src/evaluator.py to use the dispatcher                                                                                                                             │
│ 5. Update app.py subtitle (line 995) to be language-aware                                                                                                                    │
│ 6. Update src/report_generator.py heading (line 178) to be language-aware                                                                                                    │
│                                                                                                                                                                              │
│ Verification                                                                                                                                                                 │
│                                                                                                                                                                              │
│ 1. Run python3 test_setup.py to verify tree-sitter imports work                                                                                                              │
│ 2. Test with Python file — confirm existing behavior unchanged                                                                                                               │
│ 3. Paste/upload JavaScript code — verify Static Analysis section appears with metrics                                                                                        │
│ 4. Paste/upload Java code — verify same                                                                                                                                      │
│ 5. Paste/upload C code — verify has_error_handling is False (C has no try/catch)                                                                                             │
│ 6. Verify PDF report shows correct language label in static analysis heading                                                                                                 │
│ 7. Verify graceful degradation: if tree-sitter-language-pack is uninstalled, non-Python analysis returns None and the app works as before                

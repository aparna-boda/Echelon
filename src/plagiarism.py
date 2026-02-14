"""Plagiarism / similarity detection engine.

Pure algorithmic — no LLM calls. Combines three layers:
  1. Text similarity (difflib SequenceMatcher)
  2. Token n-gram Jaccard similarity
  3. AST structural cosine similarity (Python only)
"""

import ast
import difflib
import io
import math
import re
import tokenize
from collections import Counter
from itertools import combinations


# ── Layer 1: Text similarity ──

def normalize_code(code: str) -> str:
    """Strip comments, blank lines, normalize whitespace."""
    lines = code.splitlines()
    cleaned = []
    for line in lines:
        # Remove inline comments (simple heuristic — works for Python/#-style)
        stripped = line.split("#")[0].rstrip()
        # Remove C-style single-line comments
        stripped = re.sub(r"//.*$", "", stripped).rstrip()
        if stripped.strip():
            cleaned.append(stripped)
    return "\n".join(cleaned)


def text_similarity(code_a: str, code_b: str) -> float:
    """SequenceMatcher ratio on normalized code. Returns 0.0-1.0."""
    norm_a = normalize_code(code_a)
    norm_b = normalize_code(code_b)
    if not norm_a and not norm_b:
        return 1.0
    if not norm_a or not norm_b:
        return 0.0
    return difflib.SequenceMatcher(None, norm_a, norm_b).ratio()


# ── Layer 2: Token n-gram similarity ──

def tokenize_code(code: str, language: str) -> list[str]:
    """Tokenize code into normalized tokens.

    For Python: uses the stdlib tokenizer (strips comments & strings).
    For other languages: regex-based word splitter.
    """
    if language.lower() == "python":
        return _tokenize_python(code)
    return _tokenize_generic(code)


def _tokenize_python(code: str) -> list[str]:
    """Tokenize Python source using the stdlib tokenizer."""
    tokens = []
    try:
        readline = io.BytesIO(code.encode("utf-8")).readline
        for tok in tokenize.tokenize(readline):
            if tok.type in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
                            tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING,
                            tokenize.ENDMARKER):
                continue
            if tok.type == tokenize.STRING:
                tokens.append("__STR__")
            elif tok.type == tokenize.NUMBER:
                tokens.append("__NUM__")
            elif tok.type == tokenize.NAME:
                tokens.append(tok.string.lower())
            else:
                tokens.append(tok.string)
    except tokenize.TokenizeError:
        return _tokenize_generic(code)
    return tokens


def _tokenize_generic(code: str) -> list[str]:
    """Fallback regex word splitter for non-Python code."""
    # Remove string literals
    code = re.sub(r'"(?:[^"\\]|\\.)*"', "__STR__", code)
    code = re.sub(r"'(?:[^'\\]|\\.)*'", "__STR__", code)
    # Remove single-line comments
    code = re.sub(r"//.*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"#.*$", "", code, flags=re.MULTILINE)
    # Remove multi-line comments
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    # Split into word and operator tokens
    return [t.lower() for t in re.findall(r"[a-zA-Z_]\w*|[^\s]", code) if t.strip()]


def _ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    """Generate a set of n-grams from a token list."""
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def ngram_similarity(code_a: str, code_b: str, language: str, n: int = 3) -> float:
    """Jaccard similarity on token n-grams. Returns 0.0-1.0."""
    toks_a = tokenize_code(code_a, language)
    toks_b = tokenize_code(code_b, language)
    grams_a = _ngrams(toks_a, n)
    grams_b = _ngrams(toks_b, n)
    if not grams_a and not grams_b:
        return 1.0
    if not grams_a or not grams_b:
        return 0.0
    intersection = len(grams_a & grams_b)
    union = len(grams_a | grams_b)
    return intersection / union if union else 0.0


# ── Layer 3: AST structural similarity (Python only) ──

def ast_node_histogram(code: str) -> dict[str, int]:
    """Count each AST node type. Returns {node_type: count}."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {}
    counter: dict[str, int] = {}
    for node in ast.walk(tree):
        name = type(node).__name__
        counter[name] = counter.get(name, 0) + 1
    return counter


def structural_similarity(code_a: str, code_b: str) -> float:
    """Cosine similarity of AST node histograms. Returns 0.0-1.0."""
    hist_a = ast_node_histogram(code_a)
    hist_b = ast_node_histogram(code_b)
    if not hist_a or not hist_b:
        return 0.0
    all_keys = set(hist_a) | set(hist_b)
    vec_a = [hist_a.get(k, 0) for k in all_keys]
    vec_b = [hist_b.get(k, 0) for k in all_keys]
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ── Combined similarity ──

_FLAG_HIGH = 80.0
_FLAG_MEDIUM = 60.0


def _flag_label(score: float) -> str:
    if score >= _FLAG_HIGH:
        return "high"
    if score >= _FLAG_MEDIUM:
        return "medium"
    return "low"


def compute_pair_similarity(code_a: str, code_b: str, language: str) -> dict:
    """Combine all layers into an overall similarity score.

    Returns dict with keys:
        overall   — float 0-100
        text_sim  — float 0-100
        token_sim — float 0-100
        structural_sim — float 0-100, or None if not Python
        flag      — 'high' | 'medium' | 'low'
    """
    txt = text_similarity(code_a, code_b)
    tok = ngram_similarity(code_a, code_b, language)

    is_python = language.lower() == "python"
    if is_python:
        struct = structural_similarity(code_a, code_b)
        # Weights: text 40%, token 30%, structural 30%
        overall = txt * 0.40 + tok * 0.30 + struct * 0.30
        struct_pct = round(struct * 100, 1)
    else:
        # Redistribute structural weight: text 57%, token 43%
        overall = txt * 0.57 + tok * 0.43
        struct_pct = None

    overall_pct = round(overall * 100, 1)

    return {
        "overall": overall_pct,
        "text_sim": round(txt * 100, 1),
        "token_sim": round(tok * 100, 1),
        "structural_sim": struct_pct,
        "flag": _flag_label(overall_pct),
    }


def detect_plagiarism(submissions: list[dict], threshold: float = 60.0) -> dict:
    """Run pairwise comparison on all submissions.

    Args:
        submissions: list of {'name': str, 'code': str, 'language': str}
        threshold: minimum overall % to flag a pair

    Returns dict with keys:
        pairs         — list of pair result dicts (sorted by similarity desc)
        matrix        — NxN similarity matrix (list of lists)
        names         — ordered file names
        flagged_count — number of pairs >= threshold
        threshold     — the threshold used
    """
    n = len(submissions)
    names = [s["name"] for s in submissions]
    matrix = [[100.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    pairs = []

    for i, j in combinations(range(n), 2):
        lang = submissions[i]["language"]
        # If languages differ, use the first one (or generic)
        if submissions[j]["language"] != lang:
            lang = "Other"
        result = compute_pair_similarity(
            submissions[i]["code"], submissions[j]["code"], lang
        )
        matrix[i][j] = result["overall"]
        matrix[j][i] = result["overall"]
        pairs.append({
            "sub_a": names[i],
            "sub_b": names[j],
            **result,
        })

    pairs.sort(key=lambda p: p["overall"], reverse=True)
    flagged_count = sum(1 for p in pairs if p["overall"] >= threshold)

    return {
        "pairs": pairs,
        "matrix": matrix,
        "names": names,
        "flagged_count": flagged_count,
        "threshold": threshold,
    }

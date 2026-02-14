# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Echelon** is an AI-powered code evaluation engine that scores coding submissions across 6 dimensions (Correctness, Time Efficiency, Space Efficiency, Readability, Modularity, Best Practices) on a 0-100 scale. It combines static code analysis (Python AST) with LLM evaluation (Groq/Gemini) to produce weighted scores and actionable feedback.

## Development Commands

### Initial Setup
```bash
cd Echelon
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Configure API Keys
Create a `.env` file in the `Echelon/` directory:
```
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
```
- Groq is the primary LLM provider (llama-3.3-70b-versatile)
- Google Gemini (gemini-2.0-flash) is the automatic fallback

### Run the Application
```bash
streamlit run app.py
```
Opens at http://localhost:8501

### Test Dependencies & API Setup
```bash
python test_setup.py
```
Verifies imports, Groq API connectivity, and AST parsing.

## Architecture

### Evaluation Pipeline
```
Code Input (GitHub URL / Upload / Paste)
    ↓
Static Analysis (analyzer.py — Python AST only)
    ↓
LLM Evaluation (llm_client.py — Groq primary, Gemini fallback)
    ↓
Score Computation (scoring.py — weighted 0-100 from LLM dimensions)
    ↓
Interactive Dashboard (app.py — Streamlit UI with radar charts)
```

### Core Modules

| Module | Responsibility |
|--------|---------------|
| `app.py` | Streamlit UI entry point — handles 3 input methods (GitHub URL, file upload, paste), displays results with radar charts and progress bars |
| `src/evaluator.py` | Orchestration layer — calls static analyzer → LLM → scoring, handles errors, returns final evaluation dict |
| `src/analyzer.py` | Python-specific static analysis via `ast` module — extracts metrics like function count, nesting depth, comment ratio, naming quality |
| `src/llm_client.py` | LLM wrapper with automatic fallback — tries Groq twice (with retry on timeout/rate-limit), then falls back to Gemini |
| `src/prompts.py` | Evaluation rubric and prompt templates — defines the 0-100 scoring bands and dimension-specific criteria sent to the LLM |
| `src/scoring.py` | Weighted score calculation — applies fixed weights (Correctness 30%, Readability 20%, etc.) to compute overall score and verdict |
| `src/utils.py` | JSON parsing and language detection — handles LLM response parsing and file extension mapping |
| `src/github_fetcher.py` | GitHub raw file fetcher — converts `github.com/user/repo/blob/...` URLs to raw content |

### Key Design Decisions

**Scoring is Python-controlled, not LLM-controlled**: The LLM provides 6 dimension scores (0-100). The `scoring.py` module computes the weighted overall score using fixed weights. This prevents LLM hallucination of the final score.

**Static analysis only supports Python**: `analyzer.py` uses Python's `ast` module. For other languages, static analysis returns "Not available" and the LLM evaluates purely from source code.

**LLM fallback mechanism**: `llm_client.py` tries Groq up to 2 times (retrying once on timeout/rate-limit), then automatically switches to Gemini. This ensures high availability despite API rate limits.

**API key flexibility**: Keys are read from Streamlit secrets (cloud deployment) or `.env` file (local development) via `get_api_key()` in `llm_client.py`.

**Test submissions**: `test_submissions/` contains 3 sample two-sum solutions (good/ok/bad) for manual testing.

## Scoring System

### Weights (Hardcoded in `scoring.py`)
```
Correctness:      30%
Time Efficiency:  15%
Space Efficiency: 10%
Readability:      20%
Modularity:       15%
Best Practices:   10%
```

### Verdict Bands
| Score | Verdict | Emoji |
|-------|---------|-------|
| 85-100 | Excellent | 🟢 |
| 70-84 | Strong | 🔵 |
| 50-69 | Acceptable | 🟡 |
| 30-49 | Weak | 🟠 |
| 0-29 | Poor | 🔴 |

### LLM Calibration Rules (from `prompts.py`)
- **Use the full 0-100 range** — Do not cluster scores around 70
- **Reserve 90-100 for production-ready code** — genuinely excellent implementations
- **Trivial brute-force solutions cap at ~40-55** — not 70
- **Single-function solutions without error handling cap at ~60 for modularity/best_practices**

## Common Workflows

### Adding a new evaluation dimension
1. Add to `WEIGHTS` in `src/scoring.py`
2. Add to `EXPECTED_DIMENSIONS` in `src/evaluator.py`
3. Update the rubric in `src/prompts.py` (both system prompt and JSON schema)
4. Update UI labels in `DIMENSION_LABELS` in `src/scoring.py`

### Debugging LLM response parsing failures
1. Check `evaluation["error"]` and `evaluation["raw_response"]` in the returned dict
2. The `parse_llm_response()` function in `src/utils.py` handles JSON extraction from markdown-wrapped responses
3. If the LLM returns non-JSON, the error is surfaced in the UI with the raw response

### Testing with new sample code
Place files in `test_submissions/` and use the "File Upload" tab in the Streamlit UI. Ensure the file extension matches a supported language (py, js, ts, java, c, cpp, go, rb, rs).

## Important Notes

- **Working directory**: Commands should be run from `Echelon/` subdirectory, not the repository root
- **Static analysis limitations**: AST-based analysis only works for Python. Other languages rely purely on LLM evaluation
- **LLM prompt engineering**: The calibration rules in `prompts.py` are critical for score distribution — avoid generic "does it work" prompts
- **No automated tests**: `test_setup.py` only verifies dependencies, not evaluation correctness
- **Streamlit deployment**: For cloud deployment, use `.streamlit/secrets.toml` instead of `.env` (format: `KEY = "value"`)

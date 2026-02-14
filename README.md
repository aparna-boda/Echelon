# Echelon

AI-powered code evaluation engine that scores submissions the way senior engineers do — beyond test cases, across 6 dimensions of engineering quality.

## The Problem

Companies receive hundreds of coding submissions from job applicants. Manual review is slow (15-30 min per submission), inconsistent (different reviewers score differently), and shallow (most only check "does it pass tests?").

**Echelon** evaluates code the way a senior engineer would — combining LLM intelligence with static code analysis to produce actionable verdicts on a 0-100 scale.

## Features

- **6-Dimension Scoring (0-100)** — Correctness, Time Efficiency, Space Efficiency, Readability, Modularity, Best Practices
- **Weighted Overall Score** — Computed programmatically with configurable weights
- **Verdict Bands** — Excellent (85+) / Strong (70+) / Acceptable (50+) / Weak (30+) / Poor (<30)
- **4 Input Methods** — GitHub URL (auto-fetch), File Upload, Paste Code, or Batch Upload
- **Batch Evaluation** — Process multiple submissions at once with summary statistics and export
- **Auto Language Detection** — From file extension or GitHub URL
- **Radar Chart** — Visual overview of strengths and weaknesses (0-100 scale)
- **Progress Bars** — Per-dimension score visualization
- **Static Analysis (AST)** — Python-specific metrics: functions, nesting depth, naming quality, comment ratio, and more
- **LLM Fallback** — Groq (primary) with automatic Gemini fallback
- **Better Approach Suggestions** — AI-generated alternative solutions
- **Strengths & Improvements** — Side-by-side actionable feedback
- **Export Results** — Download results as CSV, JSON, or PDF reports
- **Shareable Reports** — Generate shareable links for evaluation results

## Architecture

```
Code Input (GitHub URL / Upload / Paste)
              |
              v
      Static Analysis (Python AST)
              |
              v
      LLM Evaluation (Groq / Gemini fallback)
              |
              v
      Score Computation (Weighted Python logic)
              |
              v
      Interactive Dashboard (Streamlit)
```

| Layer | Role |
|-------|------|
| **Input** | GitHub URL fetch, file upload, or direct paste with auto language detection |
| **Static Analysis** (AST) | Objective facts — line count, functions, nesting depth, naming quality, comment ratio |
| **LLM Evaluation** (Groq + Gemini) | Subjective judgment — correctness, efficiency, readability, modularity |
| **Scoring Logic** (Python) | Final decision — weighted 0-100 score, verdict, feedback aggregation |
| **Streamlit UI** | Presentation — hero score, radar chart, progress bars, expandable details |

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend/UI | Streamlit |
| LLM API (primary) | Groq (Llama 3.3 70B) |
| LLM API (fallback) | Google Gemini 2.0 Flash |
| Static Analysis | Python `ast` module |
| Visualization | Plotly (radar charts) |
| Language | Python 3.12 |

## Project Structure

```
Echelon/
├── app.py                    # Streamlit app (entry point)
├── src/
│   ├── __init__.py
│   ├── prompts.py            # LLM prompt templates & rubric
│   ├── evaluator.py          # Orchestration: analysis → LLM → scoring
│   ├── analyzer.py           # AST-based static analysis (Python)
│   ├── scoring.py            # Weighted score calculation & verdicts
│   ├── llm_client.py         # LLM calls with Groq/Gemini fallback
│   ├── github_fetcher.py     # GitHub URL → raw code fetcher
│   └── utils.py              # JSON parsing, language detection
├── test_submissions/
│   ├── good_solution.py      # Excellent two-sum (expected: 80+)
│   ├── ok_solution.py        # Acceptable two-sum (expected: 50-70)
│   └── bad_solution.py       # Poor two-sum (expected: <40)
├── .streamlit/
│   └── config.toml           # Custom theme
├── .env                      # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/aparna-boda/Echelon.git
cd Echelon
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
```

- Groq key: https://console.groq.com
- Google key: https://aistudio.google.com

### 5. Run the app
```bash
streamlit run app.py
```

## Scoring Formula

```
Overall = Correctness      x 0.30
        + Time Efficiency   x 0.15
        + Space Efficiency  x 0.10
        + Readability       x 0.20
        + Modularity        x 0.15
        + Best Practices    x 0.10
```

| Verdict | Score Range |
|---------|------------|
| Excellent | 85 - 100 |
| Strong | 70 - 84 |
| Acceptable | 50 - 69 |
| Weak | 30 - 49 |
| Poor | 0 - 29 |

## Batch Evaluation

Echelon supports batch processing for evaluating multiple code submissions at once. This is ideal for:

- **Classrooms** — Grade all student submissions in one go
- **Coding Competitions** — Evaluate all participants' solutions
- **Recruiter Pipelines** — Screen multiple candidates simultaneously

### How to Use Batch Evaluation

1. Navigate to the **"Batch Evaluation"** tab
2. Upload multiple code files (supports all languages)
3. Optionally provide problem context (applies to all submissions)
4. Click **"Evaluate Batch"**
5. View summary statistics and detailed results table
6. Export results as CSV or JSON

### Batch Results Include

- **Summary Statistics** — Total, successful, failed, average/min/max/median scores
- **Results Table** — All submissions with scores, verdicts, and dimension breakdowns
- **Export Options** — Download as CSV (for Excel/spreadsheets), JSON (for programmatic use), or PDF (professional reports)
- **Error Handling** — Failed submissions are tracked separately with error messages

## Export & Share Features

Echelon provides multiple ways to export and share evaluation results:

### Single Evaluation Export

- **PDF Report** — Professional PDF document with:
  - Overall score and verdict
  - Dimension breakdown with scores and suggestions
  - Strengths and areas for improvement
  - Better approach suggestions
  - Static analysis metrics (for Python)
  
- **Shareable Data** — Copy encoded evaluation data to share with others
  - Recipients can paste the data to view results
  - Includes scores, verdict, and dimension breakdowns

### Batch Evaluation Export

- **CSV Export** — Spreadsheet-compatible format with all submission data
- **JSON Export** — Machine-readable format for programmatic use
- **PDF Report** — Comprehensive batch report with:
  - Summary statistics (average, min, max, median scores)
  - Verdict distribution
  - Individual results table
  - All evaluation metrics

### How to Use Export Features

1. **After evaluation**, scroll to the "Export & Share" section
2. **For PDF**: Click "Download PDF Report" — opens in your PDF viewer
3. **For CSV/JSON**: Click respective download buttons
4. **To Share**: Copy the shareable data and send to recipients

## Future Enhancements

- Multi-language static analysis (JavaScript, Java, C/C++)
- Plagiarism / similarity detection across submissions
- GitHub PR integration for inline review comments

## License

MIT License — see [LICENSE](LICENSE) for details.

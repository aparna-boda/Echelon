# Echelon

AI-powered code evaluation engine that scores submissions the way senior engineers do — beyond test cases, across 6 dimensions of engineering quality.

## The Problem

Companies receive hundreds of coding submissions from job applicants. Manual review is slow (15-30 min per submission), inconsistent (different reviewers score differently), and shallow (most only check "does it pass tests?").

**Echelon** evaluates code the way a senior engineer would — combining LLM intelligence with static code analysis to produce recruiter-ready verdicts.

## Features

- **6-Dimension Scoring** — Correctness, Code Quality, Efficiency, Error Handling, Problem Understanding, Engineering Maturity
- **Weighted Overall Score** — Computed programmatically with configurable weights
- **Verdict Bands** — Excellent / Strong / Acceptable / Weak / Poor with color-coded banners
- **Radar Chart** — Visual overview of strengths and weaknesses across all dimensions
- **Static Analysis (AST)** — Objective code metrics for Python submissions (functions, docstrings, type hints, nested loops, etc.)
- **Recruiter Summary** — Plain-English feedback a non-technical recruiter can understand
- **Interview Questions** — AI-generated follow-up questions based on the submission
- **Strengths & Red Flags** — Quick-scan lists for decision-making

## Architecture

```
Code Input → Static Analysis (Python AST)
                      ↓
              LLM Evaluation (Groq / Llama 3.3 70B)
                      ↓
              Score Computation (Weighted Python logic)
                      ↓
              Recruiter Feedback Report (Streamlit UI)
```

| Layer | Role |
|-------|------|
| **Static Analysis** (AST) | Objective facts — line count, functions, docstrings, type hints, nested loops |
| **LLM Evaluation** (Groq) | Subjective judgment — code quality, problem understanding, engineering maturity |
| **Scoring Logic** (Python) | Final decision — weighted score, verdict, feedback aggregation |
| **Streamlit UI** | Presentation — interactive dashboard with charts and expandable details |

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend/UI | Streamlit |
| LLM API (primary) | Groq (Llama 3.3 70B) |
| LLM API (backup) | Google Gemini |
| Static Analysis | Python `ast` module |
| Visualization | Plotly (radar charts) |
| Language | Python 3.12 |

## Project Structure

```
Echelon/
├── app.py                 # Streamlit app (entry point)
├── src/
│   ├── __init__.py
│   ├── prompts.py         # LLM prompt templates & rubric
│   ├── evaluator.py       # LLM call, JSON parsing, orchestration
│   ├── analyzer.py        # AST-based static analysis
│   └── scoring.py         # Weighted score calculation & verdicts
├── test_submissions/
│   ├── good_solution.py
│   ├── ok_solution.py
│   └── bad_solution.py
├── .env                   # API keys (not committed)
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
Overall = Correctness × 0.35
        + Code Quality × 0.20
        + Efficiency × 0.15
        + Error Handling × 0.10
        + Problem Understanding × 0.15
        + Engineering Maturity × 0.05
```

| Verdict | Score Range |
|---------|------------|
| Excellent | 4.5 – 5.0 |
| Strong | 3.5 – 4.4 |
| Acceptable | 2.5 – 3.4 |
| Weak | 1.5 – 2.4 |
| Poor | 0.0 – 1.4 |

## Future Enhancements

- Multi-language static analysis support
- Plagiarism detection across submissions
- Batch evaluation for recruiting teams
- GitHub PR workflow integration
- Export evaluation reports to PDF

## License

MIT License — see [LICENSE](LICENSE) for details.

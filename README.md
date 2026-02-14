# Echelon
AI-powered code evaluation engine that scores submissions the way senior engineers do — beyond test cases, across 6 dimensions of engineering quality.

---

# Your Complete Hackathon Roadmap
## AI Coding Assignment Evaluator — First-Timer's Sequential Guide

---

# SECTION 1: CONTEXT REFRESHER — What Is This Hackathon?

## The Organizer
**UnsaidTalks Education** — they've run 12+ hackathon editions with 2,800+ registrations. This is a well-known community hackathon, not a corporate one.

## The Problem You're Solving
Every day, companies receive hundreds of coding submissions from job applicants. Right now, evaluation is:
- **Slow** — a senior engineer spends 15-30 minutes per submission
- **Inconsistent** — different reviewers score the same code differently
- **Shallow** — many companies only check "does it pass the tests?" and ignore code quality

**Your job**: Build an AI-powered tool that evaluates code submissions the way a real senior engineer would — looking at correctness, code quality, efficiency, error handling, problem understanding, and engineering maturity.

## The Format
| Detail | Info |
|--------|------|
| **Date** | Friday, February 14, 2026 |
| **Kickoff** | 12:00 PM IST — full problem statement revealed |
| **Build Window** | 12:30 PM – 6:30 PM IST (6 hours) |
| **What you submit** | A working prototype + presentation/demo |
| **Team size** | Solo (based on registration) |

## What Judges Care About (4 Criteria)
1. **Evaluation Logic Code** — How smart is your scoring system? Is it just calling an API, or is there real engineering?
2. **Quality & Signal Clarity** — Does your output clearly show WHY code scored high or low?
3. **Recruiter-Style Feedback** — Is the feedback actionable? Could a non-technical recruiter understand it?
4. **Engineering Quality & Reliability** — Is YOUR code well-built? Does it handle edge cases?

## The Prizes
- Winner: 60% Scholarship on Build4Hire program + mentorship session
- Runner-up: 50% Scholarship
- Second Runner-up: 40% Scholarship
- All valid submissions get a certificate

## What You DON'T Know Yet
The detailed problem statement (specific requirements, constraints, input/output format) will only be revealed at the 12:00 PM kickoff. Your prep work builds the foundation so you can adapt quickly once you see it.

---

# SECTION 2: THE COMPLETE PATH — What To Do and In What Order

## Overview: Your Journey in 3 Phases

```
PHASE 1: BEFORE THE HACKATHON (Feb 12-13)
   → Understand the domain
   → Choose your tools
   → Set up everything
   → Build your foundation
   → Test that everything works

PHASE 2: DURING THE HACKATHON (Feb 14, 12:00-6:30 PM)
   → Read the problem statement
   → Adapt your foundation
   → Build core features
   → Test and polish
   → Submit

PHASE 3: PRESENTATION
   → Demo your working product
   → Explain your architecture
   → Show differentiation
```

---

## PHASE 1: BEFORE THE HACKATHON

### Step 1: Understand How Code Evaluation Works (1-2 hours)
**When**: Today (Feb 12)
**Why**: You can't build a code evaluator if you don't understand what good evaluation looks like

**What to learn:**
- Companies evaluate code across multiple dimensions, not just "does it pass tests?"
- The 6 key dimensions (you already have these in your rubric):
  1. Correctness & Edge Cases (35% weight) — Does it work?
  2. Code Quality & Readability (20%) — Is it clean?
  3. Efficiency & Performance (15%) — Is it fast?
  4. Error Handling & Robustness (10%) — Does it handle failures?
  5. Problem Understanding & Logic Depth (15%) — Is the approach thoughtful?
  6. Engineering Maturity (5%) — Does it reflect professional practices?
- The weighted scoring formula you'll implement:
  ```
  Overall = Correctness×0.35 + Quality×0.20 + Efficiency×0.15 +
            ErrorHandling×0.10 + Understanding×0.15 + Maturity×0.05
  ```
- The verdict bands: Excellent (4.5-5.0) → Strong (3.5-4.4) → Acceptable (2.5-3.4) → Weak (1.5-2.4) → Poor (0-1.4)

**You already have this** — Your rubric and dimensions documents cover this well.

---

### Step 2: Choose Your Tech Stack (30 minutes)
**When**: Today (Feb 12)
**Why**: You need to commit to tools NOW so you can set them up and practice

**Recommended stack for a 6-hour hackathon:**

| Layer | Tool | Why |
|-------|------|-----|
| **Frontend/UI** | Streamlit | Fastest to prototype. Zero CSS. Built-in widgets for file upload, text areas, charts. |
| **Backend** | Python | Your strongest language. Everything stays in one codebase. |
| **LLM API** | Groq (primary) | Free tier, fast inference, supports Llama 3.3 70B |
| **LLM API** | Google Gemini (backup) | Free tier, in case Groq goes down |
| **Static Analysis** | Python `ast` module | Built-in, no install needed, shows engineering depth |
| **Charts** | Plotly (via Streamlit) | Radar charts for dimension visualization |
| **Version Control** | Git + GitHub | Required for submission, good practice |

**Decision**: Commit to this stack. Don't second-guess during the hackathon.

---

### Step 3: Set Up Your Development Environment (1 hour)
**When**: Today (Feb 12)
**Why**: Zero setup time on hackathon day = more build time

**Do these in order:**

#### 3a. Create the project folder
```bash
mkdir ai-code-evaluator
cd ai-code-evaluator
```

#### 3b. Set up Python virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
```

#### 3c. Install all dependencies
```bash
pip install streamlit groq google-generativeai python-dotenv plotly
```

#### 3d. Save dependencies
```bash
pip freeze > requirements.txt
```

#### 3e. Create project structure
```
ai-code-evaluator/
├── app.py                 # Main Streamlit app (entry point)
├── src/
│   ├── __init__.py        # Makes src a Python package
│   ├── evaluator.py       # LLM evaluation pipeline
│   ├── prompts.py         # All LLM prompts stored here
│   ├── analyzer.py        # Static analysis (AST-based)
│   └── scoring.py         # Weighted score calculation
├── test_submissions/
│   ├── good_solution.py   # Test case: excellent code
│   ├── ok_solution.py     # Test case: mediocre code
│   └── bad_solution.py    # Test case: poor code
├── .env                   # API keys (NEVER commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

#### 3f. Create .gitignore
```
venv/
.env
__pycache__/
*.pyc
.streamlit/
```

#### 3g. Set up API keys
```bash
# .env file
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
```

Get your Groq key: https://console.groq.com (sign up with GitHub, it's free)
Get your Google key: https://aistudio.google.com (free tier)

#### 3h. Initialize Git
```bash
git init
git add .
git commit -m "Initial project setup"
```

#### 3i. Verify everything works
Create a quick test file and run it:
```python
# test_setup.py
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import ast
import plotly.graph_objects as go

load_dotenv()
print("All imports work")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say 'API works'"}],
    max_tokens=10
)
print(f"Groq API works: {response.choices[0].message.content}")

tree = ast.parse("x = 1 + 2")
print(f"AST parsing works: {ast.dump(tree)[:50]}...")

print("\nAll systems go! You're ready for the hackathon.")
```
Run: `python test_setup.py`

**If everything prints successfully, your setup is done. Commit this checkpoint.**

---

### Step 4: Build the Skeleton App (1.5 hours)
**When**: Today (Feb 12) or Tomorrow (Feb 13)
**Why**: On hackathon day, you open your laptop and already have a working UI

**What to build:**
- A Streamlit app with two columns: input on the left, results on the right
- Input side: problem statement text area, language dropdown, code text area, evaluate button
- Results side: placeholder text that says "Results will appear here"
- NO LLM integration yet — just the shell

**What this gives you:**
When the problem statement is revealed at the kickoff, you paste it in and start testing immediately. No fumbling with UI layout under time pressure.

**Test it**: Run `streamlit run app.py` and make sure it loads in your browser.

---

### Step 5: Build the Evaluation Prompt (2 hours) — MOST IMPORTANT STEP
**When**: Tonight (Feb 12) or Tomorrow morning (Feb 13)
**Why**: The prompt IS your product. Everything else is plumbing.

**What makes a good evaluation prompt:**

Your prompt needs to do 5 things:
1. **Set a persona**: "You are a senior software engineer reviewing code for a hiring decision"
2. **Provide context**: The problem statement and language
3. **Give a rubric**: What each dimension means and what each score level looks like
4. **Define output format**: Exact JSON structure you expect back
5. **Set calibration rules**: "Use the full 0-5 range. Don't cluster scores around 3."

**Key decisions for the prompt:**

**Decision 1: What goes in the prompt vs what stays in your code?**
- IN THE PROMPT: Dimension definitions, score band descriptions, output format
- IN YOUR CODE: Weighted score calculation, verdict mapping, UI formatting
- Rule of thumb: Let the LLM judge quality. Let your code do math.

**Decision 2: How much rubric detail?**
- Too much → LLM gets confused, output is inconsistent
- Too little → LLM guesses, scores are vague
- Sweet spot → Give 1-2 sentence descriptions per score level (5, 3, 1) for each dimension

**Decision 3: JSON output**
- Tell the LLM to respond with ONLY valid JSON
- Include "respond with JSON only, no markdown backticks, no explanation before or after"
- Still write defensive parsing in your code (LLMs sometimes ignore this)

**How to test your prompt:**
1. Copy your prompt template
2. Fill in a test code submission (use your poor solution example)
3. Paste into the Groq Playground (https://console.groq.com/playground)
4. Check: Are scores reasonable? Is feedback specific? Is JSON valid?
5. Repeat with your excellent solution
6. Compare: Are the scores meaningfully different? (Poor should be <2.5, Excellent should be >4.0)
7. If not, tweak the prompt and try again

**Do this at least 3-4 times until you're happy with the output quality.**

---

### Step 6: Build the Evaluation Pipeline (1.5 hours)
**When**: Tomorrow (Feb 13)
**Why**: This is the backend that connects your UI to your LLM

**The pipeline is 4 functions:**

```
Function 1: format_prompt(code, language, problem_statement)
   → Takes inputs, fills them into your prompt template
   → Returns the complete prompt string

Function 2: call_llm(prompt)
   → Sends prompt to Groq API
   → Returns raw response text
   → Has error handling: what if API is down? what if response is empty?

Function 3: parse_response(response_text)
   → Strips markdown backticks if present
   → Parses JSON
   → Validates that all expected fields exist
   → Returns structured dictionary
   → Has fallback: if JSON parsing fails, returns error message

Function 4: evaluate_code(code, language, problem_statement)
   → Orchestrates the above 3 functions
   → Calls static analysis if language is Python
   → Computes weighted overall score (YOUR code, not the LLM)
   → Returns final evaluation result
```

**Why 4 separate functions instead of 1 big one?**
- Easier to debug (you can test each piece independently)
- Easier to swap (change LLM provider by only changing `call_llm`)
- Shows engineering maturity in YOUR code (judges notice this)

---

### Step 7: Build the Static Analysis Module (1 hour)
**When**: Tomorrow (Feb 13)
**Why**: This is your differentiator — most teams won't have this

**What it does:**
Uses Python's built-in `ast` module to extract objective code metrics WITHOUT calling an LLM.

**Metrics to extract:**
- Lines of code, blank lines, comment lines
- Number of functions and their names
- Number of classes
- Variable names used (to assess naming quality)
- Whether docstrings exist
- Whether type hints exist
- Whether try/except blocks exist
- Whether `if __name__ == "__main__"` guard exists
- Nested loop detection (complexity signal)
- Import list

**How it fits into the system:**
Two ways to use these metrics (do at least one):

Option A — Feed metrics INTO the LLM prompt as context:
"This code has 3 functions, no docstrings, variable names: a, t, i, j"
The LLM uses this evidence to make better judgments.

Option B — Display metrics ALONGSIDE the LLM evaluation:
Show a separate "Static Analysis" panel in your UI with objective facts.
This proves your evaluation has two independent signals.

**Limitation**: AST only works for Python. That's okay for the hackathon.
Mention multi-language support as a "future enhancement."

---

### Step 8: Wire the UI Together (1 hour)
**When**: Tomorrow (Feb 13)
**Why**: Connect your skeleton app to the real evaluation pipeline

**What to connect:**
1. Evaluate button → calls `evaluate_code()`
2. Results panel shows:
   - Verdict banner (color-coded: green/yellow/orange/red)
   - Overall score as a big number
   - 2-3 sentence recruiter summary
   - Radar chart showing 6 dimension scores (use Plotly)
   - Expandable sections for each dimension (score + feedback + suggestion)
   - Strengths and red flags side-by-side
   - Suggested interview follow-up questions

**Information hierarchy** (top to bottom):
1. Verdict + Score (the headline — recruiter sees this first)
2. Summary (2-3 sentences — enough to make a pass/fail decision)
3. Radar chart (visual overview — where are they strong/weak?)
4. Dimension details (expandable — only opened if recruiter wants depth)
5. Strengths & red flags (quick scan for decision-making)
6. Next steps for the candidate (actionable feedback)

---

### Step 9: Prepare Test Submissions (30 minutes)
**When**: Tomorrow (Feb 13)
**Why**: Your demo is only as good as your test data

**You need 3 submissions for the same problem:**

| # | Quality | Target Score | What It Demonstrates |
|---|---------|-------------|---------------------|
| 1 | Poor | ~1.5-2.0 | Bad naming, O(n^2), no error handling, no docs |
| 2 | Acceptable | ~3.0-3.5 | Clean naming, still O(n^2), basic structure |
| 3 | Excellent | ~4.5-5.0 | Optimal algorithm, docstrings, tests, edge cases |

**Testing checklist:**
- Run all 3 through your evaluator
- Scores are meaningfully different (not all clustering around 3)
- Feedback is specific to each submission (not generic boilerplate)
- JSON parsing doesn't break on any of them
- The poor solution doesn't crash your app

---

### Step 10: Prepare Your Presentation Story (1 hour)
**When**: Tomorrow evening (Feb 13)
**Why**: 30% of your hackathon impact comes from how you present

**Your story arc (3-5 minutes):**

**Slide/Section 1: The Problem (30 seconds)**
"Companies receive hundreds of code submissions. Manual review is slow, inconsistent, and expensive. Current automated tools only check 'does it pass tests?' — they miss code quality, engineering maturity, and problem-solving depth."

**Slide/Section 2: Our Solution (30 seconds)**
"We built an AI evaluator that thinks like a senior engineer. It scores code across 6 dimensions, produces recruiter-ready verdicts, and combines LLM intelligence with static code analysis."

**Slide/Section 3: Live Demo (2 minutes)**
Run the 3 test submissions through your tool. Show the scores side by side. Point out how the feedback changes between poor/acceptable/excellent.

**Slide/Section 4: How It Works (1 minute)**
Simple architecture diagram:
```
Code Input → Language Detection → Static Analysis (AST)
                                          |
                                  LLM Evaluation (Groq)
                                          |
                                  Score Computation (Python)
                                          |
                                  Recruiter Feedback Report
```
Key talking point: "We combine deterministic analysis with AI reasoning — like combining a blood test with a doctor's diagnosis."

**Slide/Section 5: What's Next (30 seconds)**
"Multi-language support, plagiarism detection across submissions, batch evaluation for recruiting teams, integration with GitHub PR workflows."

---

### Step 11: Pre-Hackathon Final Checklist
**When**: Tomorrow night (Feb 13) before bed

- [ ] `streamlit run app.py` works without errors
- [ ] Groq API key is valid (tested within last 24 hours)
- [ ] Backup API key (Google Gemini) is ready
- [ ] All 3 test submissions run successfully through the evaluator
- [ ] Git repo is committed and pushed to GitHub
- [ ] Laptop is fully charged
- [ ] Charger is packed
- [ ] You know the WhatsApp group link and submission process
- [ ] You have water and snacks ready
- [ ] You've slept enough (seriously — a tired brain writes bad code)

---

## PHASE 2: DURING THE HACKATHON (Feb 14)

### 12:00 PM — Kickoff Session
- [ ] Join the session on time
- [ ] **Read the full problem statement TWICE**
- [ ] Write down any specific requirements, constraints, or formats they mention
- [ ] Note anything that differs from your assumptions
- [ ] Ask questions if anything is unclear

### 12:30 – 1:00 PM — Adapt (30 min)
- Compare revealed requirements vs your prep
- What matches? Keep it.
- What's new? What needs to change?
- Modify your prompt template if the problem format is different
- **Goal**: Have a clear plan for the next 5 hours

### 1:00 – 2:30 PM — Core Build (90 min)
- Get the full pipeline working end-to-end
- Code input → LLM evaluation → display results
- Don't worry about pretty UI — focus on WORKING
- **Goal**: "Ugly but functional" prototype

### 2:30 – 3:00 PM — Test & Fix (30 min)
- Run all 3 test submissions
- Fix any JSON parsing errors
- Fix any UI display issues
- **Goal**: Reliable, crash-free demo

### 3:00 – 4:00 PM — Polish & Features (60 min)
- Add radar chart visualization
- Integrate static analysis display
- Improve UI layout and labels
- Add any bonus features IF time permits
- **Goal**: Professional-looking output

### 4:00 – 4:30 PM — Bonus Features (30 min, ONLY if core is solid)
- Side-by-side comparison of two submissions
- Code syntax highlighting
- Export evaluation to PDF
- **Goal**: Stand out from other submissions

### 4:30 – 5:00 PM — STOP CODING
- Freeze all features
- Focus on README and documentation
- Write clear setup instructions
- Add screenshots of your tool in action
- **Goal**: Professional README on GitHub

### 5:00 – 5:30 PM — Presentation Prep
- Finalize your demo flow
- Practice your 3-5 minute presentation
- Time yourself
- Prepare backup screenshots in case of API failure

### 5:30 – 6:00 PM — Final Testing
- Full end-to-end test one more time
- Make sure nothing broke during polish phase
- Commit everything to Git
- Push to GitHub

### 6:00 – 6:30 PM — Submit
- Follow the submission process exactly
- Double-check all links work
- Submit early if possible (don't wait until 6:29)
- Take a deep breath. You did it.

---

## PHASE 3: EMERGENCY PROTOCOLS

| What Goes Wrong | What You Do |
|----------------|------------|
| LLM API is down | Switch to backup provider (Gemini). If both down, use pre-saved JSON outputs for demo. |
| JSON parsing keeps failing | Add a fallback: display raw LLM text with basic formatting instead of structured cards. |
| Streamlit crashes | Have your core `evaluator.py` runnable from command line: `python src/evaluator.py` |
| A feature doesn't work | Cut it. Show what works. Mention the broken feature as "planned enhancement." |
| Running out of time | Stop adding features at the 4-hour mark. Polish and present what you have. |
| Problem statement is very different from what you expected | Don't panic. Your evaluation framework (6 dimensions + weighted scoring) applies to ANY code evaluation problem. Adapt the prompt, keep the architecture. |

---

## QUICK REFERENCE: The 5 Files You'll Build

| File | Purpose | Build When |
|------|---------|-----------|
| `app.py` | Streamlit UI — the face of your product | Step 4 (skeleton) → Step 8 (wired) |
| `src/prompts.py` | LLM prompt templates | Step 5 |
| `src/evaluator.py` | LLM call + response parsing | Step 6 |
| `src/analyzer.py` | AST-based static analysis | Step 7 |
| `src/scoring.py` | Weighted score calculation + verdict mapping | Step 6 |

---

## THE MENTAL MODEL

Think of your system as a **hiring panel**:

```
Static Analysis (AST)  =  The automated screening tool
                           → Objective facts: "This code has 0 tests,
                             no docstrings, and variables named 'a' and 't'"

LLM Evaluation (Groq)  =  The senior engineer reviewer
                           → Subjective judgment: "This approach shows limited
                             understanding of optimal data structures"

Scoring Logic (Python)  =  The hiring committee rubric
                           → Final decision: Weighted score + verdict + feedback

Streamlit UI            =  The recruiter dashboard
                           → Presentation: Clear, actionable, professional
```

Each layer has a specific job. Together, they produce something no single layer could do alone. That's the story you tell the judges.

---

*You have 2 days. That's more than enough to build something impressive. The key is following this path in order — each step builds on the last. Don't skip ahead. Don't over-engineer. Trust the process.*

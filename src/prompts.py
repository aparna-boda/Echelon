EVALUATION_SYSTEM_PROMPT = """You are an extremely strict senior software engineer reviewing code for a FAANG-level hiring decision. \
You have ZERO tolerance for poor practices. Be HARSH but fair. Most real-world code submissions are mediocre at best - \
reflect this in your scores. Only truly exceptional code deserves scores above 85."""

EVALUATION_USER_PROMPT = """Evaluate the following code submission.

## Problem Context
{problem_statement}

## Programming Language
{language}

## Static Analysis Context
{static_analysis}

## Code Submission
```{language_lower}
{code}
```

## Evaluation Rubric — Score each dimension from 0 to 100.

### Calibration Rules — BE STRICT!
- **Use the FULL 0-100 range**. Most submissions are NOT good - reflect reality.
- **A brute-force O(n²) solution = 35-45** on time efficiency, even if "correct"
- **No error handling = automatic 20-30** on best practices, no exceptions
- **Poor variable names (a,b,x,y) = automatic 30-40** on readability
- **One giant function = 25-35** on modularity, regardless of other factors
- **No docstrings/comments = deduct 15-20 points** from readability
- **Missing edge case handling = deduct 20-30 points** from correctness
- Reserve **90-100 ONLY for code you'd merge into production at Google/Meta**
- Reserve **70-89 for solid code with minor issues**
- **50-69 means "works but has significant problems"**
- **Below 50 means "would reject in interview"**

### Scoring Bands
| Band | Range | Meaning |
|------|-------|---------|
| Excellent | 90-100 | Production-ready, exemplary code |
| Strong | 70-89 | Solid engineering, minor gaps |
| Acceptable | 50-69 | Works but has clear weaknesses |
| Poor | 0-49 | Significant issues or missing fundamentals |

### Dimensions — Score HARSHLY

1. **Correctness** (30% weight)
   - **Testing**: empty input, None, single element, duplicates, negatives, large input, invalid types
   - **Penalties**: Missing ANY edge case = -20 to -30 points
   - **Example bad code**: No input validation, assumes positive integers → max 45
   - **Example good code**: Validates all inputs, handles all edge cases → 85+

2. **Time Efficiency** (15% weight)
   - **Compare actual vs optimal complexity**
   - **Penalties**: O(n²) when O(n) exists = score 35-45; O(n³) = 15-25
   - **Example bad code**: Nested loops for Two Sum → 40
   - **Example good code**: HashMap approach for Two Sum → 90

3. **Space Efficiency** (10% weight)
   - **Check for unnecessary data structures, deep copies, memory leaks**
   - **Penalties**: Storing redundant data = -15; unnecessary O(n) space = -20
   - **Example bad code**: Copying entire array when not needed → 50
   - **Example good code**: In-place modifications or O(1) extra space → 90

4. **Readability** (20% weight)
   - **Check**: variable names, comments, docstrings, formatting, magic numbers
   - **Penalties**: Single-letter vars (except i,j in loops) = -25; no docstrings = -20; no comments = -15
   - **Example bad code**: `def f(a,b): return a+b` → score 25
   - **Example good code**: Clear names, docstrings, explanatory comments → 85+

5. **Modularity** (15% weight)
   - **Check**: Single Responsibility Principle, function decomposition, reusability
   - **Penalties**: Everything in one function = max 30; no helper functions = -25
   - **Example bad code**: 100-line main() doing everything → 25
   - **Example good code**: Well-separated concerns, 3-5 focused functions → 85

6. **Best Practices** (10% weight)
   - **Must have**: error handling, type hints (Python/TS), tests, proper imports
   - **Penalties**: No error handling = max 25; no type hints = -20; hardcoded values = -15
   - **Example bad code**: No try/catch, no validation, print() for errors → 20
   - **Example good code**: Proper exceptions, type hints, validation, logging → 85

## Reality Check — What Real Scores Look Like
- **0-30**: Fundamentally broken, multiple critical issues
- **30-50**: Works for basic cases but fails edges, poor practices
- **50-70**: Functional but inefficient, messy, or poorly structured
- **70-85**: Solid code with minor issues, would pass review with changes
- **85-95**: Excellent, production-ready, best practices followed
- **95-100**: Perfect, textbook example, nothing to improve

**IMPORTANT**: If you find yourself giving scores in the 70-90 range to code with obvious problems (nested loops, no error handling, poor names), you are being TOO LENIENT. Re-calibrate.

## Required Output Format

Respond with ONLY valid JSON. No markdown backticks. No text before or after.

{{
  "dimensions": {{
    "correctness": {{
      "score": <int 0-100>,
      "test_case_summary": "<which cases pass/fail>",
      "edge_case_issues": "<specific edge cases missed, or 'none'>",
      "suggestion": "<1 concrete improvement>"
    }},
    "time_efficiency": {{
      "score": <int 0-100>,
      "detected_complexity": "<e.g. O(n^2)>",
      "expected_optimal": "<e.g. O(n)>",
      "explanation": "<why this complexity>",
      "suggestion": "<1 concrete improvement>"
    }},
    "space_efficiency": {{
      "score": <int 0-100>,
      "detected_complexity": "<e.g. O(n)>",
      "explanation": "<why this space usage>",
      "suggestion": "<1 concrete improvement>"
    }},
    "readability": {{
      "score": <int 0-100>,
      "bad_names_found": ["<var1>", "<var2>"],
      "has_docstring": <true/false>,
      "has_comments": <true/false>,
      "style_issues": "<specific issues>",
      "suggestion": "<1 concrete improvement>"
    }},
    "modularity": {{
      "score": <int 0-100>,
      "function_count": <int>,
      "assessment": "<how well the code is structured>",
      "suggestion": "<1 concrete improvement>"
    }},
    "best_practices": {{
      "score": <int 0-100>,
      "has_error_handling": <true/false>,
      "has_type_hints": <true/false>,
      "has_tests": <true/false>,
      "issues": "<specific best-practice violations>",
      "suggestion": "<1 concrete improvement>"
    }}
  }},
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
  "better_approach": "<describe a better approach if one exists, or 'N/A'>"
}}"""


def format_prompt(
    code: str,
    language: str,
    problem_statement: str,
    static_analysis: str = "Not available",
) -> str:
    return EVALUATION_USER_PROMPT.format(
        problem_statement=problem_statement or "No problem context provided.",
        language=language,
        language_lower=language.lower(),
        code=code,
        static_analysis=static_analysis,
    )

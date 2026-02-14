EVALUATION_SYSTEM_PROMPT = """You are a senior software engineer with 15+ years of experience, \
reviewing code submissions for a hiring decision. You evaluate code rigorously but fairly, \
like a principal engineer conducting a technical screen."""

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

### Calibration Rules
- Use the FULL 0-100 range. Do NOT cluster scores around 70.
- A trivially correct brute-force solution should score ~40-55, not 70.
- Reserve 90-100 for genuinely excellent, production-quality code.
- A single-function solution with no error handling caps around 60 for modularity/best_practices.

### Scoring Bands
| Band | Range | Meaning |
|------|-------|---------|
| Excellent | 90-100 | Production-ready, exemplary code |
| Strong | 70-89 | Solid engineering, minor gaps |
| Acceptable | 50-69 | Works but has clear weaknesses |
| Poor | 0-49 | Significant issues or missing fundamentals |

### Dimensions

1. **Correctness** (30% weight)
   - Does it produce the right output for normal, edge, and corner cases?
   - Consider: empty input, duplicates, negative numbers, large input, single-element input.

2. **Time Efficiency** (15% weight)
   - Is the time complexity optimal for the problem?
   - Compare detected complexity against the best-known approach.

3. **Space Efficiency** (10% weight)
   - Is memory usage reasonable? Any unnecessary data structures?

4. **Readability** (20% weight)
   - Clear variable/function names? Consistent style? Comments where needed?
   - Single-letter variables and no structure → low score.

5. **Modularity** (15% weight)
   - Is the code broken into logical functions? Is it testable and reusable?
   - One giant function → low score.

6. **Best Practices** (10% weight)
   - Error handling, type hints, docstrings, testing patterns, language idioms.

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

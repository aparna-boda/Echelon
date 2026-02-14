EVALUATION_SYSTEM_PROMPT = """You are a senior software engineer with 15+ years of experience, \
reviewing code submissions for a hiring decision. You evaluate code rigorously but fairly, \
like a principal engineer conducting a technical screen."""

EVALUATION_USER_PROMPT = """Evaluate the following code submission against the problem statement.

## Problem Statement
{problem_statement}

## Programming Language
{language}

## Static Analysis Context
{static_analysis}

## Code Submission
```{language_lower}
{code}
```

## Evaluation Rubric

Score each dimension from 0.0 to 5.0 (use decimals, e.g. 3.7). Use the FULL range — do NOT cluster scores around 3.

### Dimensions:

1. **Correctness & Edge Cases** (35% weight)
   - 5: Handles all cases including edge cases (empty input, duplicates, large input, negative numbers)
   - 3: Core logic works but misses some edge cases
   - 1: Fundamental logic errors, fails on basic inputs

2. **Code Quality & Readability** (20% weight)
   - 5: Clean naming, consistent style, well-structured, easy to follow
   - 3: Readable but some unclear names or inconsistent formatting
   - 1: Single-letter variables, no structure, hard to understand

3. **Efficiency & Performance** (15% weight)
   - 5: Optimal time/space complexity for the problem
   - 3: Acceptable but suboptimal (e.g., O(n²) when O(n) exists)
   - 1: Brute force, unnecessary nested loops, wasteful memory use

4. **Error Handling & Robustness** (10% weight)
   - 5: Validates inputs, handles exceptions, fails gracefully
   - 3: Some basic checks but not comprehensive
   - 1: No validation, crashes on bad input

5. **Problem Understanding & Logic Depth** (15% weight)
   - 5: Demonstrates deep understanding, considers trade-offs, elegant approach
   - 3: Understands the problem, straightforward solution
   - 1: Misunderstands requirements, overcomplicated or naive approach

6. **Engineering Maturity** (5% weight)
   - 5: Docstrings, type hints, modular design, testable code
   - 3: Some documentation or structure
   - 1: No documentation, monolithic, untestable

## Required Output Format

Respond with ONLY valid JSON. No markdown backticks. No text before or after the JSON.

{{
  "dimensions": {{
    "correctness": {{
      "score": <float 0-5>,
      "feedback": "<2-3 sentences explaining the score with specific code references>",
      "suggestion": "<1 concrete improvement suggestion>"
    }},
    "code_quality": {{
      "score": <float 0-5>,
      "feedback": "<2-3 sentences>",
      "suggestion": "<1 concrete suggestion>"
    }},
    "efficiency": {{
      "score": <float 0-5>,
      "feedback": "<2-3 sentences>",
      "suggestion": "<1 concrete suggestion>"
    }},
    "error_handling": {{
      "score": <float 0-5>,
      "feedback": "<2-3 sentences>",
      "suggestion": "<1 concrete suggestion>"
    }},
    "problem_understanding": {{
      "score": <float 0-5>,
      "feedback": "<2-3 sentences>",
      "suggestion": "<1 concrete suggestion>"
    }},
    "engineering_maturity": {{
      "score": <float 0-5>,
      "feedback": "<2-3 sentences>",
      "suggestion": "<1 concrete suggestion>"
    }}
  }},
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "red_flags": ["<red flag 1>", "<red flag 2>"],
  "recruiter_summary": "<2-3 sentence summary a non-technical recruiter can understand>",
  "interview_questions": ["<follow-up question 1>", "<follow-up question 2>", "<follow-up question 3>"]
}}"""


def format_prompt(code: str, language: str, problem_statement: str, static_analysis: str = "Not available") -> str:
    return EVALUATION_USER_PROMPT.format(
        problem_statement=problem_statement,
        language=language,
        language_lower=language.lower(),
        code=code,
        static_analysis=static_analysis,
    )

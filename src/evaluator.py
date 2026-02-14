import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

from src.prompts import EVALUATION_SYSTEM_PROMPT, format_prompt
from src.analyzer import analyze_python_code, format_analysis_for_prompt
from src.scoring import compute_overall_score, get_verdict

load_dotenv()

EXPECTED_DIMENSIONS = [
    "correctness", "code_quality", "efficiency",
    "error_handling", "problem_understanding", "engineering_maturity",
]


def call_llm(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set in .env")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    return response.choices[0].message.content


def parse_response(response_text: str) -> dict:
    # Strip markdown code fences if the LLM wrapped the JSON
    cleaned = response_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    data = json.loads(cleaned)

    # Validate expected structure
    dims = data.get("dimensions", {})
    for key in EXPECTED_DIMENSIONS:
        if key not in dims:
            raise ValueError(f"Missing dimension: {key}")
        if "score" not in dims[key]:
            raise ValueError(f"Missing score for dimension: {key}")
        dims[key]["score"] = float(dims[key]["score"])

    return data


def evaluate_code(code: str, language: str, problem_statement: str) -> dict:
    # Run static analysis for Python submissions
    static_analysis_result = None
    static_analysis_text = "Not available (static analysis only supports Python)"
    if language.lower() == "python":
        static_analysis_result = analyze_python_code(code)
        static_analysis_text = format_analysis_for_prompt(static_analysis_result)

    # Build prompt and call LLM
    prompt = format_prompt(code, language, problem_statement, static_analysis_text)
    raw_response = call_llm(prompt)
    evaluation = parse_response(raw_response)

    # Compute weighted overall score (our code, not the LLM)
    overall_score = compute_overall_score(evaluation["dimensions"])
    verdict, verdict_color = get_verdict(overall_score)

    evaluation["overall_score"] = overall_score
    evaluation["verdict"] = verdict
    evaluation["verdict_color"] = verdict_color
    evaluation["static_analysis"] = static_analysis_result

    return evaluation

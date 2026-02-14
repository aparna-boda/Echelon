import time

from src.llm_client import call_llm
from src.utils import parse_llm_response
from src.prompts import EVALUATION_SYSTEM_PROMPT, format_prompt
from src.analyzer import analyze_python_code, format_analysis_for_prompt
from src.scoring import compute_overall_score, get_verdict

EXPECTED_DIMENSIONS = [
    "correctness", "time_efficiency", "space_efficiency",
    "readability", "modularity", "best_practices",
]


def evaluate_code(code: str, language: str, problem_statement: str) -> dict:
    start_time = time.time()

    # Run static analysis for Python submissions
    static_analysis_result = None
    static_analysis_text = "Not available (static analysis only supports Python)"
    if language.lower() == "python":
        static_analysis_result = analyze_python_code(code)
        static_analysis_text = format_analysis_for_prompt(static_analysis_result)

    # Build prompt and call LLM
    prompt = format_prompt(code, language, problem_statement, static_analysis_text)
    raw_response = call_llm(prompt, EVALUATION_SYSTEM_PROMPT)

    # Parse response
    evaluation = parse_llm_response(raw_response)

    if evaluation.get("error"):
        elapsed = round(time.time() - start_time, 1)
        return {
            "overall_score": 0,
            "verdict": "Error",
            "verdict_emoji": "\u274c",
            "language": language,
            "dimensions": {},
            "strengths": [],
            "improvements": [],
            "better_approach": None,
            "static_analysis": static_analysis_result,
            "evaluation_time_seconds": elapsed,
            "error": evaluation.get("message", "Failed to parse LLM response"),
            "raw_response": evaluation.get("raw_response", ""),
        }

    # Validate and fill missing dimensions
    dims = evaluation.get("dimensions", {})
    for key in EXPECTED_DIMENSIONS:
        if key not in dims:
            dims[key] = {"score": 0, "suggestion": "Dimension not evaluated"}
        if "score" not in dims[key]:
            dims[key]["score"] = 0
        dims[key]["score"] = int(float(dims[key]["score"]))

    # Compute weighted overall score (our code, not the LLM's)
    overall_score = compute_overall_score(dims)
    verdict, verdict_emoji = get_verdict(overall_score)
    elapsed = round(time.time() - start_time, 1)

    return {
        "overall_score": overall_score,
        "verdict": verdict,
        "verdict_emoji": verdict_emoji,
        "language": language,
        "dimensions": dims,
        "strengths": evaluation.get("strengths", []),
        "improvements": evaluation.get("improvements", []),
        "better_approach": evaluation.get("better_approach"),
        "static_analysis": static_analysis_result,
        "evaluation_time_seconds": elapsed,
        "error": None,
    }


def evaluate_batch(
    submissions: list[dict],
    problem_statement: str = "",
    progress_callback=None,
) -> dict:
    """
    Evaluate multiple code submissions in batch.
    
    Args:
        submissions: List of dicts with keys: 'code', 'language', 'name' (optional)
        problem_statement: Optional problem context for all submissions
        progress_callback: Optional function(submission_index, total, result) for progress updates
    
    Returns:
        dict with keys:
            - results: List of evaluation results (one per submission)
            - summary: Aggregate statistics
            - total_time: Total evaluation time
            - errors: List of errors encountered
    """
    start_time = time.time()
    results = []
    errors = []
    
    total = len(submissions)
    
    for idx, submission in enumerate(submissions, 1):
        code = submission.get("code", "")
        language = submission.get("language", "Python")
        name = submission.get("name", f"Submission {idx}")
        
        if not code.strip():
            error_msg = f"{name}: Empty code submission"
            errors.append({"submission": name, "error": error_msg})
            results.append({
                "name": name,
                "error": error_msg,
                "overall_score": 0,
                "verdict": "Error",
            })
            continue
        
        try:
            result = evaluate_code(code, language, problem_statement)
            result["name"] = name
            results.append(result)
            
            if progress_callback:
                progress_callback(idx, total, result)
                
        except Exception as e:
            error_msg = f"{name}: {str(e)}"
            errors.append({"submission": name, "error": error_msg})
            results.append({
                "name": name,
                "error": error_msg,
                "overall_score": 0,
                "verdict": "Error",
            })
    
    # Compute summary statistics
    successful_results = [r for r in results if not r.get("error")]
    
    if successful_results:
        scores = [r["overall_score"] for r in successful_results]
        summary = {
            "total_submissions": total,
            "successful": len(successful_results),
            "failed": len(errors),
            "average_score": round(sum(scores) / len(scores), 1),
            "min_score": min(scores),
            "max_score": max(scores),
            "median_score": sorted(scores)[len(scores) // 2] if scores else 0,
        }
        
        # Count by verdict
        verdict_counts = {}
        for r in successful_results:
            verdict = r.get("verdict", "Unknown")
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
        summary["verdict_distribution"] = verdict_counts
    else:
        summary = {
            "total_submissions": total,
            "successful": 0,
            "failed": len(errors),
            "average_score": 0,
            "min_score": 0,
            "max_score": 0,
            "median_score": 0,
            "verdict_distribution": {},
        }
    
    total_time = round(time.time() - start_time, 1)
    
    return {
        "results": results,
        "summary": summary,
        "total_time": total_time,
        "errors": errors,
    }

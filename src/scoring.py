WEIGHTS = {
    "correctness": 0.35,
    "code_quality": 0.20,
    "efficiency": 0.15,
    "error_handling": 0.10,
    "problem_understanding": 0.15,
    "engineering_maturity": 0.05,
}

VERDICT_BANDS = [
    (4.5, "Excellent", "#2ecc71"),
    (3.5, "Strong", "#27ae60"),
    (2.5, "Acceptable", "#f39c12"),
    (1.5, "Weak", "#e67e22"),
    (0.0, "Poor", "#e74c3c"),
]

DIMENSION_LABELS = {
    "correctness": "Correctness & Edge Cases",
    "code_quality": "Code Quality & Readability",
    "efficiency": "Efficiency & Performance",
    "error_handling": "Error Handling & Robustness",
    "problem_understanding": "Problem Understanding & Logic Depth",
    "engineering_maturity": "Engineering Maturity",
}


def compute_overall_score(dimensions: dict) -> float:
    total = 0.0
    for key, weight in WEIGHTS.items():
        score = dimensions.get(key, {}).get("score", 0.0)
        total += float(score) * weight
    return round(total, 2)


def get_verdict(overall_score: float) -> tuple[str, str]:
    for threshold, label, color in VERDICT_BANDS:
        if overall_score >= threshold:
            return label, color
    return "Poor", "#e74c3c"

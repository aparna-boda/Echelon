WEIGHTS = {
    "correctness": 0.30,
    "time_efficiency": 0.15,
    "space_efficiency": 0.10,
    "readability": 0.20,
    "modularity": 0.15,
    "best_practices": 0.10,
}

VERDICT_BANDS = [
    (85, "Excellent", "\U0001f7e2"),   # green circle
    (70, "Strong", "\U0001f535"),       # blue circle
    (50, "Acceptable", "\U0001f7e1"),   # yellow circle
    (30, "Weak", "\U0001f7e0"),         # orange circle
    (0,  "Poor", "\U0001f534"),         # red circle
]

DIMENSION_LABELS = {
    "correctness": "Correctness & Edge Cases",
    "time_efficiency": "Time Efficiency",
    "space_efficiency": "Space Efficiency",
    "readability": "Readability & Style",
    "modularity": "Modularity & Structure",
    "best_practices": "Best Practices",
}


def compute_overall_score(dimensions: dict) -> int:
    """Compute weighted overall score on the 0-100 scale. Returns an int."""
    total = 0.0
    for key, weight in WEIGHTS.items():
        score = dimensions.get(key, {}).get("score", 0)
        total += float(score) * weight
    return round(total)


def get_verdict(overall_score: int) -> tuple[str, str]:
    """Return (label, emoji) for the given overall score."""
    for threshold, label, emoji in VERDICT_BANDS:
        if overall_score >= threshold:
            return label, emoji
    return "Poor", "\U0001f534"

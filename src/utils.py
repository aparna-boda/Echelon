import json
import re

EXTENSION_TO_LANGUAGE = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "JavaScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".go": "Go",
    ".rb": "Ruby",
    ".rs": "Rust",
}


def detect_language(filename: str) -> str:
    """Detect programming language from a filename's extension."""
    for ext, lang in EXTENSION_TO_LANGUAGE.items():
        if filename.endswith(ext):
            return lang
    return "Unknown"


def parse_llm_response(text: str) -> dict:
    """Parse LLM response text into a dict.

    Strips markdown fences, extracts JSON between first { and last },
    and validates required fields. Returns a fallback dict on failure
    so the app never crashes on bad LLM output.
    """
    try:
        cleaned = text.strip()
        # Strip markdown code fences
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?\s*```\s*$", "", cleaned)
        cleaned = cleaned.strip()

        # Extract JSON between first { and last }
        first_brace = cleaned.index("{")
        last_brace = cleaned.rindex("}")
        json_str = cleaned[first_brace : last_brace + 1]

        data = json.loads(json_str)

        # Validate that dimensions exist
        if "dimensions" not in data or not isinstance(data["dimensions"], dict):
            return {
                "error": True,
                "raw_response": text,
                "message": "Missing 'dimensions' in LLM response",
            }

        # Ensure all dimension scores are numeric
        for dim_name, dim_data in data["dimensions"].items():
            if isinstance(dim_data, dict) and "score" in dim_data:
                dim_data["score"] = int(float(dim_data["score"]))

        return data

    except (json.JSONDecodeError, ValueError) as e:
        return {
            "error": True,
            "raw_response": text,
            "message": f"Failed to parse LLM response: {e}",
        }

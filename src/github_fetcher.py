import re
import requests

EXTENSION_TO_LANGUAGE = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".go": "Go",
    ".rb": "Ruby",
    ".rs": "Rust",
}


def github_url_to_raw(url: str) -> str:
    """Convert a GitHub file URL to its raw.githubusercontent.com equivalent."""
    # Match: https://github.com/{owner}/{repo}/blob/{branch}/{path}
    match = re.match(
        r"https?://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)", url.strip()
    )
    if not match:
        raise ValueError(
            "Invalid GitHub URL. Expected format: "
            "https://github.com/{owner}/{repo}/blob/{branch}/{path}"
        )
    owner, repo, branch, path = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"


def detect_language_from_url(url: str) -> str:
    """Detect programming language from a file URL's extension."""
    # Extract filename from the URL path
    path = url.rstrip("/").split("/")[-1]
    for ext, lang in EXTENSION_TO_LANGUAGE.items():
        if path.endswith(ext):
            return lang
    return "Unknown"


def fetch_github_code(url: str) -> tuple[str, str]:
    """Fetch code from a GitHub file URL.

    Returns (code_string, detected_language).
    Raises on invalid URL, 404, or 403.
    """
    raw_url = github_url_to_raw(url)
    language = detect_language_from_url(url)

    resp = requests.get(raw_url, timeout=15)

    if resp.status_code == 404:
        raise ValueError("File not found (404). Check the URL and branch name.")
    if resp.status_code == 403:
        raise ValueError(
            "Access denied (403). This may be a private repository."
        )
    if resp.status_code != 200:
        raise ValueError(f"GitHub returned HTTP {resp.status_code}.")

    return resp.text, language

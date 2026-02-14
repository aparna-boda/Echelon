import os
import time

from dotenv import load_dotenv

load_dotenv()


def get_api_key(key_name: str) -> str | None:
    """Get API key from Streamlit secrets (cloud) or environment variables (local)."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    return os.getenv(key_name)


def _call_groq(prompt: str, system_prompt: str) -> str:
    """Call Groq API with llama-3.3-70b-versatile."""
    from groq import Groq

    api_key = get_api_key("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not configured")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=3000,
    )
    return response.choices[0].message.content


def _call_gemini(prompt: str, system_prompt: str) -> str:
    """Call Google Gemini API as fallback."""
    import google.generativeai as genai

    api_key = get_api_key("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not configured")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-2.0-flash",
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=3000,
        ),
        system_instruction=system_prompt,
    )
    response = model.generate_content(prompt)
    return response.text


def call_llm(prompt: str, system_prompt: str) -> str:
    """Call LLM with Groq as primary and Gemini as fallback.

    Retries once on timeout/rate-limit before falling back.
    Returns raw response text or raises with a clear error message.
    """
    # Try Groq (primary)
    for attempt in range(2):
        try:
            return _call_groq(prompt, system_prompt)
        except RuntimeError:
            # Missing API key — skip straight to fallback
            break
        except Exception as e:
            error_msg = str(e).lower()
            is_retryable = any(
                kw in error_msg
                for kw in ("timeout", "rate_limit", "rate limit", "429", "503")
            )
            if is_retryable and attempt == 0:
                time.sleep(2)
                continue
            break

    # Fall back to Gemini
    try:
        return _call_gemini(prompt, system_prompt)
    except Exception as e:
        raise RuntimeError(
            f"Both Groq and Gemini failed. Last error: {e}"
        ) from e

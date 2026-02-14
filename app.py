import streamlit as st
import plotly.graph_objects as go

from src.evaluator import evaluate_code
from src.scoring import DIMENSION_LABELS, WEIGHTS
from src.github_fetcher import fetch_github_code
from src.utils import detect_language

# ── Page Configuration ──
st.set_page_config(
    page_title="Echelon - AI Code Evaluator",
    page_icon="🔬",
    layout="wide",
)

st.title("Echelon")
st.caption("AI-powered code evaluation engine — scores submissions across 6 dimensions of engineering quality")
st.divider()

# ── Input Section ──
st.header("Submit Code")

tab_github, tab_upload, tab_paste = st.tabs(["GitHub URL", "File Upload", "Paste Code"])

code = ""
language = "Python"
auto_detected = False

with tab_github:
    github_url = st.text_input(
        "GitHub File URL",
        placeholder="https://github.com/user/repo/blob/main/solution.py",
    )
    if github_url:
        try:
            code, detected_lang = fetch_github_code(github_url)
            language = detected_lang
            auto_detected = True
            st.success(f"Fetched! Language detected: **{language}** ({len(code.splitlines())} lines)")
            with st.expander("Preview fetched code", expanded=False):
                st.code(code, language=language.lower())
        except Exception as e:
            st.error(f"Failed to fetch: {e}")

with tab_upload:
    uploaded_file = st.file_uploader(
        "Upload a source code file",
        type=["py", "js", "ts", "java", "c", "cpp", "cc", "go", "rb", "rs"],
    )
    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8", errors="replace")
        language = detect_language(uploaded_file.name)
        auto_detected = True
        st.success(f"Loaded **{uploaded_file.name}** — Language: **{language}** ({len(code.splitlines())} lines)")
        with st.expander("Preview uploaded code", expanded=False):
            st.code(code, language=language.lower())

with tab_paste:
    language_select = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go", "Rust", "Ruby", "Other"],
    )
    pasted_code = st.text_area(
        "Code Submission",
        placeholder="Paste your code here...",
        height=300,
    )
    if pasted_code:
        code = pasted_code
        language = language_select

# ── Optional problem context ──
problem_statement = st.text_area(
    "Problem Context (optional)",
    placeholder="Describe the problem being solved — helps the AI evaluate correctness and approach...",
    height=100,
)

evaluate_btn = st.button("Evaluate", type="primary", use_container_width=True)

st.divider()

# ── Results Section ──
if evaluate_btn:
    if not code.strip():
        st.warning("Please provide code to evaluate — use one of the input tabs above.")
        st.stop()

    # Progress steps
    progress_placeholder = st.empty()
    with progress_placeholder.container():
        step1 = st.status("Analyzing code...", expanded=False)
        step1.update(label="Analyzing code...", state="running")

    result = None
    try:
        with progress_placeholder.container():
            step1 = st.status("Step 1: Running static analysis...", expanded=False)
            step1.update(label="Step 1: Static analysis complete", state="complete")
            step2 = st.status("Step 2: Calling AI evaluator...", expanded=False)
            step2.update(label="Step 2: Calling AI evaluator...", state="running")

        result = evaluate_code(code, language, problem_statement)

        with progress_placeholder.container():
            step1 = st.status("Step 1: Static analysis complete", expanded=False)
            step1.update(label="Step 1: Static analysis complete", state="complete")
            step2 = st.status("Step 2: AI evaluation complete", expanded=False)
            step2.update(label="Step 2: AI evaluation complete", state="complete")
            step3 = st.status("Step 3: Computing scores...", expanded=False)
            step3.update(label="Step 3: Scores computed!", state="complete")

    except Exception as e:
        st.error(f"Evaluation failed: {e}")
        st.stop()

    progress_placeholder.empty()

    if result.get("error"):
        st.error(f"Evaluation error: {result['error']}")
        if result.get("raw_response"):
            with st.expander("Raw LLM response"):
                st.text(result["raw_response"])
        st.stop()

    # ═══════════════════════════════════════
    # RESULTS DISPLAY
    # ═══════════════════════════════════════

    overall_score = result["overall_score"]
    verdict = result["verdict"]
    verdict_emoji = result["verdict_emoji"]
    eval_time = result["evaluation_time_seconds"]
    dims = result["dimensions"]

    # ── Hero Score Banner ──
    score_color = "#2ecc71" if overall_score >= 85 else "#3498db" if overall_score >= 70 else "#f39c12" if overall_score >= 50 else "#e67e22" if overall_score >= 30 else "#e74c3c"

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {score_color}22, {score_color}44);
                    border: 2px solid {score_color}; border-radius: 16px;
                    padding: 30px; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 64px; font-weight: bold; color: {score_color};">{overall_score}</div>
            <div style="font-size: 14px; color: #888;">out of 100</div>
            <div style="font-size: 28px; margin-top: 8px;">{verdict_emoji} {verdict}</div>
            <div style="font-size: 13px; color: #aaa; margin-top: 8px;">
                {language} &bull; evaluated in {eval_time}s
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Radar Chart ──
    labels = [DIMENSION_LABELS[k] for k in DIMENSION_LABELS]
    scores = [dims.get(k, {}).get("score", 0) for k in DIMENSION_LABELS]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=labels + [labels[0]],
        fill="toself",
        name="Score",
        line_color=score_color,
        fillcolor=f"rgba({int(score_color[1:3], 16)},{int(score_color[3:5], 16)},{int(score_color[5:7], 16)},0.15)",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=40),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Dimension Cards ──
    st.markdown("### Dimension Breakdown")

    for key, label in DIMENSION_LABELS.items():
        dim = dims.get(key, {})
        dim_score = dim.get("score", 0)
        weight_pct = int(WEIGHTS[key] * 100)

        col_bar, col_score = st.columns([4, 1])
        with col_bar:
            st.markdown(f"**{label}** ({weight_pct}% weight)")
            st.progress(dim_score / 100)
        with col_score:
            st.markdown(f"<div style='text-align:center; font-size:24px; font-weight:bold; padding-top:10px;'>{dim_score}</div>", unsafe_allow_html=True)

        with st.expander(f"Details: {label}"):
            # Show all available fields for this dimension
            for field_key, field_val in dim.items():
                if field_key == "score":
                    continue
                if field_key == "suggestion":
                    st.markdown(f"**Suggestion:** {field_val}")
                elif isinstance(field_val, list):
                    st.markdown(f"**{field_key.replace('_', ' ').title()}:** {', '.join(str(v) for v in field_val)}")
                elif isinstance(field_val, bool):
                    st.markdown(f"**{field_key.replace('_', ' ').title()}:** {'Yes' if field_val else 'No'}")
                else:
                    st.markdown(f"**{field_key.replace('_', ' ').title()}:** {field_val}")

    # ── Strengths & Improvements (side by side) ──
    col_s, col_i = st.columns(2)
    with col_s:
        st.markdown("### Strengths")
        for s in result.get("strengths", []):
            st.markdown(f"- {s}")
        if not result.get("strengths"):
            st.caption("No strengths identified.")
    with col_i:
        st.markdown("### Areas for Improvement")
        for imp in result.get("improvements", []):
            st.markdown(f"- {imp}")
        if not result.get("improvements"):
            st.caption("No improvements identified.")

    # ── Better Approach ──
    better = result.get("better_approach")
    if better and better.strip() and better.strip().lower() != "n/a":
        st.info(f"**Better Approach:** {better}")

    # ── Static Analysis Panel (Python only) ──
    sa = result.get("static_analysis")
    if sa:
        with st.expander("Static Analysis (Python AST)", expanded=False):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Lines of Code", sa["total_lines"])
                st.metric("Functions", len(sa["functions"]))
                st.metric("Classes", len(sa["classes"]))
            with col_b:
                st.metric("Nested Loops", sa["nested_loops"])
                st.metric("Max Nesting Depth", sa["max_nesting_depth"])
                st.metric("Longest Function", f"{sa['longest_function_lines']} lines")
            with col_c:
                st.metric("Docstrings", "Yes" if sa["has_docstrings"] else "No")
                st.metric("Type Hints", "Yes" if sa["has_type_hints"] else "No")
                st.metric("Error Handling", "Yes" if sa["has_error_handling"] else "No")

            col_d, col_e = st.columns(2)
            with col_d:
                st.metric("Has Tests", "Yes" if sa["has_tests"] else "No")
                st.metric("Main Guard", "Yes" if sa["has_main_guard"] else "No")
            with col_e:
                st.metric("Comment Ratio", sa["comment_ratio"])
                st.metric("Naming Quality", sa["naming_quality"])

            if sa.get("single_char_vars"):
                st.warning(f"Single-char variables: {', '.join(sa['single_char_vars'])}")

            if not sa.get("is_valid_syntax", True):
                st.error(f"Syntax error detected: {sa.get('syntax_error', 'unknown')}")

# ── Footer ──
st.divider()
st.caption("Built for UnsaidTalks Hackathon 2026 | Powered by Groq + Gemini")

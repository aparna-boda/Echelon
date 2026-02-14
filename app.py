import streamlit as st
import plotly.graph_objects as go

from src.evaluator import evaluate_code
from src.scoring import DIMENSION_LABELS, WEIGHTS

# Page configuration
st.set_page_config(
    page_title="Echelon — AI Code Evaluator",
    page_icon="🔬",
    layout="wide",
)

st.title("Echelon")
st.caption("AI-powered code evaluation engine — scores submissions across 6 dimensions of engineering quality")

st.divider()

# Two-column layout: input (left) | results (right)
left_col, right_col = st.columns([1, 1], gap="large")

# ── INPUT PANEL ──
with left_col:
    st.header("Submit Code")

    problem_statement = st.text_area(
        "Problem Statement",
        placeholder="Paste the coding problem / assignment description here...",
        height=150,
    )

    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "C++", "C", "Go", "Rust", "Other"],
    )

    code = st.text_area(
        "Code Submission",
        placeholder="Paste the candidate's code here...",
        height=300,
    )

    evaluate_btn = st.button("Evaluate", type="primary", use_container_width=True)

# ── RESULTS PANEL ──
with right_col:
    st.header("Evaluation Results")

    if evaluate_btn:
        if not code.strip():
            st.warning("Please paste a code submission before evaluating.")
        elif not problem_statement.strip():
            st.warning("Please provide a problem statement.")
        else:
            with st.spinner("Evaluating code..."):
                try:
                    result = evaluate_code(code, language, problem_statement)
                except Exception as e:
                    st.error(f"Evaluation failed: {e}")
                    st.stop()

            # ── Verdict Banner ──
            verdict = result["verdict"]
            score = result["overall_score"]
            color = result["verdict_color"]
            st.markdown(
                f"<div style='background-color:{color}; padding:20px; border-radius:10px; text-align:center;'>"
                f"<h1 style='color:white; margin:0;'>{verdict}</h1>"
                f"<h2 style='color:white; margin:0;'>{score} / 5.0</h2>"
                f"</div>",
                unsafe_allow_html=True,
            )

            # ── Recruiter Summary ──
            st.markdown("### Recruiter Summary")
            st.info(result.get("recruiter_summary", "N/A"))

            # ── Radar Chart ──
            dims = result["dimensions"]
            labels = [DIMENSION_LABELS[k] for k in DIMENSION_LABELS]
            scores = [dims[k]["score"] for k in DIMENSION_LABELS]
            weights_pct = [f"{int(WEIGHTS[k]*100)}%" for k in DIMENSION_LABELS]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],
                theta=labels + [labels[0]],
                fill="toself",
                name="Score",
                line_color=color,
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=False,
                margin=dict(l=40, r=40, t=40, b=40),
                height=350,
            )
            st.plotly_chart(fig, use_container_width=True)

            # ── Dimension Details ──
            st.markdown("### Dimension Breakdown")
            for key, label in DIMENSION_LABELS.items():
                dim = dims[key]
                weight_pct = int(WEIGHTS[key] * 100)
                with st.expander(f"{label}  —  {dim['score']}/5.0  ({weight_pct}% weight)"):
                    st.write(dim.get("feedback", ""))
                    suggestion = dim.get("suggestion", "")
                    if suggestion:
                        st.markdown(f"**Suggestion:** {suggestion}")

            # ── Strengths & Red Flags ──
            col_s, col_r = st.columns(2)
            with col_s:
                st.markdown("### Strengths")
                for s in result.get("strengths", []):
                    st.markdown(f"- {s}")
            with col_r:
                st.markdown("### Red Flags")
                for r in result.get("red_flags", []):
                    st.markdown(f"- {r}")

            # ── Interview Questions ──
            questions = result.get("interview_questions", [])
            if questions:
                st.markdown("### Suggested Interview Questions")
                for i, q in enumerate(questions, 1):
                    st.markdown(f"{i}. {q}")

            # ── Static Analysis (Python only) ──
            sa = result.get("static_analysis")
            if sa:
                with st.expander("Static Analysis (AST)"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Lines of Code", sa["total_lines"])
                        st.metric("Functions", len(sa["functions"]))
                        st.metric("Classes", len(sa["classes"]))
                        st.metric("Nested Loops", sa["nested_loops"])
                    with col_b:
                        st.metric("Docstrings", "Yes" if sa["has_docstrings"] else "No")
                        st.metric("Type Hints", "Yes" if sa["has_type_hints"] else "No")
                        st.metric("Try/Except", "Yes" if sa["has_try_except"] else "No")
                        st.metric("Main Guard", "Yes" if sa["has_main_guard"] else "No")
    else:
        st.markdown(
            "<div style='text-align:center; color:gray; padding-top:100px;'>"
            "Results will appear here after you click <b>Evaluate</b>."
            "</div>",
            unsafe_allow_html=True,
        )

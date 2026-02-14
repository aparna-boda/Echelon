import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import io

from src.evaluator import evaluate_code
from src.scoring import DIMENSION_LABELS, WEIGHTS
from src.github_fetcher import fetch_github_code
from src.utils import detect_language
from src.report_generator import generate_single_report
from src.plagiarism import detect_plagiarism


# ── Helper Functions ──
def get_score_color(score: int) -> str:
    """Get color hex code for a score based on verdict bands."""
    if score >= 85:
        return "#00D26A"  # Excellent - Green
    elif score >= 70:
        return "#4A9EFF"  # Strong - Blue
    elif score >= 50:
        return "#FFB800"  # Acceptable - Yellow
    elif score >= 30:
        return "#FF6B35"  # Weak - Orange
    else:
        return "#FF3B5C"  # Poor - Red


# ── Page Configuration ──
st.set_page_config(
    page_title="Echelon - AI Code Evaluator",
    page_icon="🔬",
    layout="wide",
)

# ══════════════════════════════════════════
# GLOBAL CSS — Dark & Sleek Theme
# ══════════════════════════════════════════
st.markdown("""
<style>
/* ── CSS Variables ── */
:root {
    /* Score Colors */
    --color-excellent: #00D26A;
    --color-strong: #4A9EFF;
    --color-acceptable: #FFB800;
    --color-weak: #FF6B35;
    --color-poor: #FF3B5C;

    /* Brand Colors */
    --color-primary: #6C63FF;
    --color-primary-dark: #5A52D5;

    /* UI Colors */
    --color-background: #0a0a0f;
    --color-background-lighter: #0d0d14;
    --color-text-primary: #F0F0F5;
    --color-text-secondary: #8888A0;
    --color-border: rgba(255,255,255,0.08);

    /* Spacing Scale */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;

    /* Border Radius */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
}

/* ── Base overrides ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #0a0a0f;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
section[data-testid="stSidebar"] {
    background: #0d0d14;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    overflow: hidden;
    position: relative;
}
.glass-card:hover {
    border-color: rgba(108,99,255,0.25);
    box-shadow: 0 0 20px rgba(108,99,255,0.08);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px 10px 0 0;
    border: 1px solid rgba(255,255,255,0.06);
    border-bottom: none;
    color: #8888A0;
    padding: 10px 24px;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(108,99,255,0.08);
    color: #F0F0F5;
}
.stTabs [aria-selected="true"] {
    background: rgba(108,99,255,0.12) !important;
    color: #F0F0F5 !important;
    border-color: rgba(108,99,255,0.3) !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: #6C63FF !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF 0%, #5A52D5 100%);
    color: #F0F0F5;
    border: none;
    border-radius: 12px;
    padding: 12px 32px;
    font-weight: 600;
    font-size: 16px;
    letter-spacing: 0.3px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(108,99,255,0.25);
}
.stButton > button:hover {
    box-shadow: 0 6px 25px rgba(108,99,255,0.45);
    transform: translateY(-1px);
    background: linear-gradient(135deg, #7B73FF 0%, #6C63FF 100%);
}
.stButton > button:active {
    transform: translateY(0px);
}

/* ── Text inputs, text areas, selectboxes ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #F0F0F5 !important;
    transition: border-color 0.2s ease;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(108,99,255,0.5) !important;
    box-shadow: 0 0 10px rgba(108,99,255,0.15) !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02);
    border: 1px dashed rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 16px;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: #F0F0F5 !important;
    font-weight: 500;
    margin-top: 8px !important;
    padding: 10px 12px !important;
}
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    margin-top: 8px;
    margin-bottom: 16px;
}
[data-testid="stExpander"] > div {
    width: 100%;
}
.streamlit-expanderHeader {
    width: 100% !important;
    max-width: 100% !important;
}
.streamlit-expanderHeader > p {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    width: 100% !important;
}

/* ── Status elements ── */
[data-testid="stStatusWidget"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
}

/* ── Score ring ── */
.score-ring-outer {
    width: 190px;
    height: 190px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    position: relative;
}
.score-ring-inner {
    width: 156px;
    height: 156px;
    border-radius: 50%;
    background: #0a0a0f;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* ── Custom progress bar ── */
.dim-bar-track {
    width: 100%;
    height: 10px;
    background: rgba(255,255,255,0.08);
    border-radius: 5px;
    overflow: hidden;
    position: relative;
}
.dim-bar-fill {
    height: 100%;
    border-radius: 5px;
    transition: width 0.6s ease;
    position: relative;
}

/* ── Metric pill ── */
.metric-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    transition: border-color 0.2s ease;
}
.metric-pill:hover {
    border-color: rgba(108,99,255,0.2);
}
.metric-pill .pill-value {
    font-size: 22px;
    font-weight: 700;
    color: #F0F0F5;
    margin-bottom: 2px;
}
.metric-pill .pill-label {
    font-size: 11px;
    color: #8888A0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeInUp 0.5s ease forwards;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb {
    background: rgba(108,99,255,0.3);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(108,99,255,0.5);
}

/* ══════════════════════════════════════════
   RESPONSIVE DESIGN — Mobile & Tablet
   ══════════════════════════════════════════ */

/* Tablet and below (< 1024px) */
@media (max-width: 1024px) {
    .score-ring-outer {
        width: 160px !important;
        height: 160px !important;
    }
    .score-ring-inner {
        width: 130px !important;
        height: 130px !important;
    }
    .glass-card {
        padding: 18px !important;
    }
}

/* Mobile and below (< 768px) */
@media (max-width: 768px) {
    /* Reduce score ring size */
    .score-ring-outer {
        width: 140px !important;
        height: 140px !important;
    }
    .score-ring-inner {
        width: 110px !important;
        height: 110px !important;
    }

    /* Reduce dimension card padding and heights */
    .glass-card {
        padding: 14px !important;
        min-height: auto !important;
    }

    /* Reduce dimension score font size */
    .glass-card div[style*="font-size: 36px"] {
        font-size: 28px !important;
    }

    /* Reduce progress bar height */
    .dim-bar-track {
        height: 8px !important;
    }

    /* Smaller metric pills */
    .metric-pill {
        padding: 10px 14px !important;
    }
    .pill-value {
        font-size: 20px !important;
    }
    .pill-label {
        font-size: 10px !important;
    }

    /* Reduce header sizes */
    h1 {
        font-size: 32px !important;
    }
    h2 {
        font-size: 24px !important;
    }
    h3 {
        font-size: 18px !important;
    }

    /* Scale down main title on mobile */
    div[style*="font-size: 140px"] {
        font-size: 70px !important;
        letter-spacing: 4px !important;
    }
}

/* Small mobile (< 480px) */
@media (max-width: 480px) {
    .score-ring-outer {
        width: 120px !important;
        height: 120px !important;
    }
    .score-ring-inner {
        width: 94px !important;
        height: 94px !important;
    }

    /* Even smaller dimension scores */
    .glass-card div[style*="font-size: 36px"],
    .glass-card div[style*="font-size: 28px"] {
        font-size: 24px !important;
    }

    /* Tighter spacing */
    .glass-card {
        padding: 12px !important;
        margin-bottom: 12px !important;
    }

    /* Stack metric pills more tightly */
    .metric-pill {
        padding: 8px 12px !important;
    }

    /* Even smaller main title on very small screens */
    div[style*="font-size: 140px"] {
        font-size: 50px !important;
        letter-spacing: 2px !important;
    }
}

/* ── Hide default Streamlit elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
button[title="Deploy"] {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# HEADER - MASSIVE GLOWING TITLE
# ══════════════════════════════════════════
st.markdown(
    '<div style="text-align:center; padding: 50px 0 40px 0; background: rgba(108,99,255,0.03); border-radius: 24px; margin-bottom: 0px;">'
    '<div style="font-size: 140px; font-weight: 900; line-height: 1; font-family: Inter, sans-serif; '
    'background: linear-gradient(135deg, #FFFFFF 0%, #8B7DFF 50%, #6C63FF 100%); '
    '-webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; '
    'margin-bottom: 20px; letter-spacing: 10px; text-transform: uppercase; '
    'filter: drop-shadow(0 0 50px rgba(108,99,255,0.8)) drop-shadow(0 0 80px rgba(108,99,255,0.5)); '
    'text-shadow: 0 0 60px rgba(108,99,255,0.6);">ECHELON</div>'
    '<div style="width: 350px; height: 5px; margin: 0 auto 18px auto; border-radius: 10px; '
    'background: linear-gradient(90deg, transparent, #6C63FF, transparent); '
    'box-shadow: 0 0 25px rgba(108,99,255,0.8), 0 0 50px rgba(108,99,255,0.4);"></div>'
    '<p style="color: #E0E0FF; font-size: 22px; font-weight: 600; margin: 0; '
    'letter-spacing: 2.5px; text-transform: uppercase; '
    'text-shadow: 0 0 30px rgba(108,99,255,0.5);">AI-Powered Code Evaluation Engine</p>'
    '</div>',
    unsafe_allow_html=True
)

# ══════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════
tab_github, tab_upload, tab_paste, tab_similarity = st.tabs(
    ["GitHub URL", "File Upload", "Paste Code", "Similarity Check"]
)

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
            st.success(
                f"Fetched! Language detected: **{language}** ({len(code.splitlines())} lines)"
            )
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
        st.success(
            f"Loaded **{uploaded_file.name}** — Language: **{language}** ({len(code.splitlines())} lines)"
        )
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

with tab_similarity:
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <p style="color: #8888A0; font-size: 14px; margin: 0;">
            Upload multiple code files to check for similarity and potential plagiarism.
            Uses text, token, and structural analysis — no AI calls required.
        </p>
    </div>
    """, unsafe_allow_html=True)

    sim_files = st.file_uploader(
        "Upload code files to compare",
        type=["py", "js", "ts", "java", "c", "cpp", "cc", "go", "rb", "rs"],
        accept_multiple_files=True,
        key="sim_uploader",
    )

    sim_threshold = st.slider(
        "Flagging threshold (%)", min_value=30, max_value=95, value=60, step=5,
        help="Pairs with similarity above this threshold are flagged.",
    )

    sim_btn = st.button(
        "Check Similarity",
        type="primary",
        use_container_width=True,
        disabled=len(sim_files) < 2 if sim_files else True,
        key="sim_btn",
    )

    if sim_files and len(sim_files) < 2:
        st.info("Upload at least 2 files to compare.")

    if sim_btn and sim_files and len(sim_files) >= 2:
        submissions = []
        for f in sim_files:
            file_code = f.read().decode("utf-8", errors="replace")
            file_lang = detect_language(f.name)
            submissions.append({"name": f.name, "code": file_code, "language": file_lang})

        with st.spinner("Analyzing similarity..."):
            sim_result = detect_plagiarism(submissions, threshold=float(sim_threshold))

        # ── Summary stats ──
        max_sim = max((p["overall"] for p in sim_result["pairs"]), default=0)
        n_files = len(sim_result["names"])
        n_flagged = sim_result["flagged_count"]
        flag_color = "#FF3B5C" if n_flagged > 0 else "#00D26A"

        st.markdown(f"""
        <div class="glass-card fade-in">
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px;">
                <div class="metric-pill">
                    <div class="pill-value">{n_files}</div>
                    <div class="pill-label">FILES</div>
                </div>
                <div class="metric-pill">
                    <div class="pill-value" style="color: {flag_color};">{n_flagged}</div>
                    <div class="pill-label">FLAGGED PAIRS</div>
                </div>
                <div class="metric-pill">
                    <div class="pill-value">{max_sim:.1f}%</div>
                    <div class="pill-label">MAX SIMILARITY</div>
                </div>
                <div class="metric-pill">
                    <div class="pill-value">{sim_threshold}%</div>
                    <div class="pill-label">THRESHOLD</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Heatmap ──
        st.markdown("""
        <div style="margin-top: 10px; margin-bottom: 12px;">
            <h3 style="color: #F0F0F5; font-weight: 700; font-size: 20px; margin-bottom: 4px;">Similarity Matrix</h3>
            <p style="color: #8888A0; font-size: 13px; margin-top: 0;">Pairwise similarity between all uploaded files</p>
        </div>
        """, unsafe_allow_html=True)

        heatmap_fig = go.Figure(data=go.Heatmap(
            z=sim_result["matrix"],
            x=sim_result["names"],
            y=sim_result["names"],
            colorscale=[
                [0.0, "#0d1b2a"],
                [0.3, "#1b2838"],
                [0.5, "#6C63FF"],
                [0.7, "#9b59b6"],
                [1.0, "#FF3B5C"],
            ],
            zmin=0,
            zmax=100,
            text=[[f"{v:.1f}%" for v in row] for row in sim_result["matrix"]],
            texttemplate="%{text}",
            textfont=dict(size=12, color="#F0F0F5"),
            hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Similarity: %{z:.1f}%<extra></extra>",
            colorbar=dict(
                title="Similarity %",
                titlefont=dict(color="#8888A0"),
                tickfont=dict(color="#8888A0"),
            ),
        ))
        heatmap_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            height=max(350, 60 * n_files + 100),
            xaxis=dict(tickfont=dict(color="#F0F0F5", size=11), side="bottom"),
            yaxis=dict(tickfont=dict(color="#F0F0F5", size=11), autorange="reversed"),
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

        # ── Flagged pairs ──
        flagged = [p for p in sim_result["pairs"] if p["overall"] >= sim_threshold]
        if flagged:
            st.markdown("""
            <div style="margin-top: 10px; margin-bottom: 12px;">
                <h3 style="color: #F0F0F5; font-weight: 700; font-size: 20px; margin-bottom: 4px;">Flagged Pairs</h3>
                <p style="color: #8888A0; font-size: 13px; margin-top: 0;">Pairs exceeding the similarity threshold</p>
            </div>
            """, unsafe_allow_html=True)

            for pair in flagged:
                is_high = pair["flag"] == "high"
                border_color = "#FF3B5C" if is_high else "#FFB800"
                flag_label = "HIGH" if is_high else "MEDIUM"
                flag_bg = "rgba(255,59,92,0.15)" if is_high else "rgba(255,184,0,0.15)"
                bar_gradient = f"linear-gradient(90deg, #6C63FF, {border_color})"
                overall_val = pair["overall"]

                struct_html = ""
                if pair["structural_sim"] is not None:
                    struct_html = f"""
                    <div style="flex: 1; min-width: 100px;">
                        <div style="font-size: 11px; color: #8888A0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Structural</div>
                        <div style="font-size: 16px; font-weight: 600; color: #F0F0F5;">{pair['structural_sim']:.1f}%</div>
                    </div>"""

                st.markdown(f"""
                <div class="glass-card fade-in" style="border-left: 3px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span style="color: #F0F0F5; font-weight: 600; font-size: 15px;">{pair['sub_a']}</span>
                            <span style="color: #8888A0; margin: 0 8px;">vs</span>
                            <span style="color: #F0F0F5; font-weight: 600; font-size: 15px;">{pair['sub_b']}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="
                                background: {flag_bg};
                                color: {border_color};
                                font-size: 10px;
                                font-weight: 700;
                                padding: 4px 10px;
                                border-radius: 12px;
                                letter-spacing: 0.5px;
                            ">{flag_label}</span>
                            <span style="font-size: 24px; font-weight: 800; color: {border_color};">{overall_val:.1f}%</span>
                        </div>
                    </div>
                    <div style="margin-bottom: 14px;">
                        <div class="dim-bar-track">
                            <div class="dim-bar-fill" style="width: {overall_val}%; background: {bar_gradient};"></div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 100px;">
                            <div style="font-size: 11px; color: #8888A0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Text</div>
                            <div style="font-size: 16px; font-weight: 600; color: #F0F0F5;">{pair['text_sim']:.1f}%</div>
                        </div>
                        <div style="flex: 1; min-width: 100px;">
                            <div style="font-size: 11px; color: #8888A0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Token</div>
                            <div style="font-size: 16px; font-weight: 600; color: #F0F0F5;">{pair['token_sim']:.1f}%</div>
                        </div>
                        {struct_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card fade-in" style="border-left: 3px solid #00D26A; text-align: center;">
                <p style="color: #00D26A; font-size: 16px; font-weight: 600; margin: 0;">
                    No pairs exceed the similarity threshold — all submissions appear independent.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ── All pairs table (collapsed) ──
        with st.expander("View all pair scores", expanded=False):
            for pair in sim_result["pairs"]:
                struct_str = f"{pair['structural_sim']:.1f}%" if pair["structural_sim"] is not None else "N/A"
                st.markdown(
                    f"**{pair['sub_a']}** vs **{pair['sub_b']}** — "
                    f"Overall: **{pair['overall']:.1f}%** "
                    f"(Text: {pair['text_sim']:.1f}%, Token: {pair['token_sim']:.1f}%, Structural: {struct_str})"
                )

# ── Optional problem context ──
problem_statement = st.text_area(
    "Problem Context (optional)",
    placeholder="Describe the problem being solved — helps the AI evaluate correctness and approach...",
    height=100,
)

# ── Evaluation button ──
evaluate_btn = st.button("Evaluate", type="primary", use_container_width=True)

# ══════════════════════════════════════════
# EVALUATION
# ══════════════════════════════════════════
if evaluate_btn:
    if not code.strip():
        st.warning("Please provide code to evaluate — use one of the input tabs above.")
        st.stop()

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

    # ══════════════════════════════════════════
    # RESULTS DISPLAY
    # ══════════════════════════════════════════

    overall_score = result["overall_score"]
    verdict = result["verdict"]
    verdict_emoji = result["verdict_emoji"]
    eval_time = result["evaluation_time_seconds"]
    dims = result["dimensions"]

    # Score color mapping
    score_color = get_score_color(overall_score)

    # ── Hero Score Ring ──
    score_deg = int((overall_score / 100) * 360)
    st.markdown(
        f"""
    <div class="fade-in" style="text-align: center; padding: 30px 0 20px 0;">
        <div class="score-ring-outer" style="
            background: conic-gradient({score_color} {score_deg}deg, #1a1a2e {score_deg}deg);
            box-shadow: 0 0 40px rgba({int(score_color[1:3],16)},{int(score_color[3:5],16)},{int(score_color[5:7],16)},0.25);
        ">
            <div class="score-ring-inner">
                <div style="font-size: 48px; font-weight: 800; color: {score_color}; line-height: 1;">{overall_score}</div>
                <div style="font-size: 12px; color: #8888A0; margin-top: 2px;">out of 100</div>
            </div>
        </div>
        <div style="font-size: 24px; margin-top: 16px; font-weight: 600; color: #F0F0F5;">
            {verdict_emoji} {verdict}
        </div>
        <div style="font-size: 13px; color: #8888A0; margin-top: 6px;">
            {language} &bull; evaluated in {eval_time}s
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Radar Chart ──
    labels = [DIMENSION_LABELS[k] for k in DIMENSION_LABELS]
    scores = [dims.get(k, {}).get("score", 0) for k in DIMENSION_LABELS]

    r_color = (
        f"{int(score_color[1:3],16)},{int(score_color[3:5],16)},{int(score_color[5:7],16)}"
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=scores + [scores[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name="Score",
            line=dict(color=score_color, width=2),
            fillcolor=f"rgba({r_color},0.15)",
            marker=dict(size=6, color=score_color),
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(108,99,255,0.15)",
                linecolor="rgba(108,99,255,0.1)",
                tickfont=dict(color="#8888A0", size=10),
            ),
            angularaxis=dict(
                gridcolor="rgba(108,99,255,0.12)",
                linecolor="rgba(108,99,255,0.1)",
                tickfont=dict(color="#F0F0F5", size=11),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=80, r=80, t=40, b=40),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Dimension Breakdown ──
    st.markdown("""
    <div style="margin-top: 10px; margin-bottom: 20px;">
        <h3 style="color: #F0F0F5; font-weight: 700; font-size: 20px; margin-bottom: 4px;">Dimension Breakdown</h3>
        <p style="color: #8888A0; font-size: 13px; margin-top: 0;">Score across each evaluation dimension</p>
    </div>
    """, unsafe_allow_html=True)

    dim_keys = list(DIMENSION_LABELS.keys())
    for row_start in range(0, len(dim_keys), 2):
        cols = st.columns(2, gap="medium")
        for col_idx, key in enumerate(dim_keys[row_start : row_start + 2]):
            label = DIMENSION_LABELS[key]
            dim = dims.get(key, {})
            dim_score = dim.get("score", 0)
            weight_pct = int(WEIGHTS[key] * 100)

            # Per-dimension color
            dim_color = get_score_color(dim_score)

            with cols[col_idx]:
                # Card
                st.markdown(
                    f"""
                <div style="margin-bottom: 20px; overflow: hidden; position: relative;">
                    <div class="glass-card fade-in" style="min-height: 130px; padding: 18px; overflow: hidden; position: relative;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; position: relative;">
                            <div style="flex: 1; min-width: 0; padding-right: 12px; overflow: hidden;">
                                <div style="font-size: 14px; font-weight: 600; color: #F0F0F5; line-height: 1.3; margin-bottom: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{label}">
                                    {label}
                                </div>
                                <div style="
                                    display: inline-block;
                                    background: rgba(108,99,255,0.15);
                                    color: #6C63FF;
                                    font-size: 10px;
                                    font-weight: 600;
                                    padding: 4px 10px;
                                    border-radius: 12px;
                                    white-space: nowrap;
                                    margin-top: 4px;
                                ">{weight_pct}% weight</div>
                            </div>
                            <div style="font-size: 36px; font-weight: 800; color: {dim_color}; flex-shrink: 0; line-height: 1; position: relative;">{dim_score}</div>
                        </div>
                        <div style="margin-top: 14px; clear: both; position: relative; overflow: hidden;">
                            <div class="dim-bar-track">
                                <div class="dim-bar-fill" style="
                                    width: {dim_score}%;
                                    background: linear-gradient(90deg, #6C63FF, {dim_color});
                                "></div>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Details expander
                with st.expander("View Details", expanded=False):
                    st.markdown(f"### {label}")
                    st.divider()
                    for field_key, field_val in dim.items():
                        if field_key == "score":
                            continue
                        title = field_key.replace("_", " ").title()
                        if field_key == "suggestion":
                            st.markdown(f"**Suggestion:** {field_val}")
                        elif isinstance(field_val, list):
                            st.markdown(
                                f"**{title}:** {', '.join(str(v) for v in field_val)}"
                            )
                        elif isinstance(field_val, bool):
                            icon = "Yes" if field_val else "No"
                            color = "#00D26A" if field_val else "#FF3B5C"
                            st.markdown(
                                f"**{title}:** <span style='color:{color}; font-weight:600;'>{icon}</span>",
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(f"**{title}:** {field_val}")

    # ── Strengths & Improvements ──
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    col_s, col_i = st.columns(2)

    with col_s:
        strengths = result.get("strengths", [])
        strengths_html = (
            "".join(
                f'<div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:10px;">'
                f'<span style="color:#00D26A; font-size:18px; line-height:1.4;">&#9679;</span>'
                f'<span style="color:#F0F0F5; font-size:14px; line-height:1.5;">{s}</span></div>'
                for s in strengths
            )
            if strengths
            else '<p style="color:#8888A0; font-size:13px;">No strengths identified.</p>'
        )
        st.markdown(
            f"""
        <div class="glass-card fade-in" style="border-left: 3px solid #00D26A;">
            <h4 style="color: #00D26A; font-weight: 700; font-size: 16px; margin-bottom: 16px; margin-top: 0;">Strengths</h4>
            {strengths_html}
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_i:
        improvements = result.get("improvements", [])
        improvements_html = (
            "".join(
                f'<div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:10px;">'
                f'<span style="color:#FFB800; font-size:18px; line-height:1.4;">&#9679;</span>'
                f'<span style="color:#F0F0F5; font-size:14px; line-height:1.5;">{s}</span></div>'
                for s in improvements
            )
            if improvements
            else '<p style="color:#8888A0; font-size:13px;">No improvements identified.</p>'
        )
        st.markdown(
            f"""
        <div class="glass-card fade-in" style="border-left: 3px solid #FFB800;">
            <h4 style="color: #FFB800; font-weight: 700; font-size: 16px; margin-bottom: 16px; margin-top: 0;">Areas for Improvement</h4>
            {improvements_html}
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── Better Approach ──
    better = result.get("better_approach")
    if better and better.strip() and better.strip().lower() != "n/a":
        st.markdown(
            f"""
        <div class="glass-card fade-in" style="border-left: 3px solid #6C63FF;">
            <h4 style="color: #6C63FF; font-weight: 700; font-size: 16px; margin-bottom: 10px; margin-top: 0;">Better Approach</h4>
            <p style="color: #F0F0F5; font-size: 14px; line-height: 1.6; margin: 0;">{better}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── Static Analysis (Python only) ──
    sa = result.get("static_analysis")
    if sa:
        st.markdown("""
        <div style="margin-top: 20px; margin-bottom: 12px;">
            <h3 style="color: #F0F0F5; font-weight: 700; font-size: 20px; margin-bottom: 4px;">Static Analysis</h3>
            <p style="color: #8888A0; font-size: 13px; margin-top: 0;">Python AST inspection results</p>
        </div>
        """, unsafe_allow_html=True)

        metrics = [
            ("Lines of Code", sa["total_lines"]),
            ("Functions", len(sa["functions"])),
            ("Classes", len(sa["classes"])),
            ("Nested Loops", sa["nested_loops"]),
            ("Max Nesting", sa["max_nesting_depth"]),
            ("Longest Fn", f"{sa['longest_function_lines']}L"),
            ("Docstrings", "Yes" if sa["has_docstrings"] else "No"),
            ("Type Hints", "Yes" if sa["has_type_hints"] else "No"),
            ("Error Handling", "Yes" if sa["has_error_handling"] else "No"),
            ("Has Tests", "Yes" if sa["has_tests"] else "No"),
            ("Main Guard", "Yes" if sa["has_main_guard"] else "No"),
            ("Comment Ratio", sa["comment_ratio"]),
            ("Naming Quality", sa["naming_quality"]),
        ]

        pills_html = "".join(
            f'<div class="metric-pill">'
            f'<div class="pill-value">{val}</div>'
            f'<div class="pill-label">{label}</div>'
            f"</div>"
            for label, val in metrics
        )

        st.markdown(
            f"""
        <div class="glass-card fade-in">
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px;">
                {pills_html}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if sa.get("single_char_vars"):
            st.warning(f"Single-char variables: {', '.join(sa['single_char_vars'])}")

        if not sa.get("is_valid_syntax", True):
            st.error(f"Syntax error detected: {sa.get('syntax_error', 'unknown')}")

    # ── Export Options ──
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 12px;">
        <h3 style="color: #F0F0F5; font-weight: 700; font-size: 20px; margin-bottom: 4px;">Export Report</h3>
    </div>
    """, unsafe_allow_html=True)

    try:
        pdf_buffer = generate_single_report(result, problem_statement)
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name=f"echelon_report_{overall_score}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"PDF generation failed: {e}")


# ── Footer ──
st.markdown("""
<div style="
    text-align: center;
    padding: 30px 0 20px 0;
    margin-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.06);
">
    <p style="color: #8888A0; font-size: 12px; margin: 0;">
        Built for UnsaidTalks Hackathon 2026 &nbsp;|&nbsp; Powered by Groq + Gemini
    </p>
</div>
""", unsafe_allow_html=True)

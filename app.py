"""
Streamlit UI for the Research-Forge multi-agent pipeline.
Run with:  streamlit run app.py
(place this file in the same folder as pipeline.py, agents.py, tools.py)
"""

import streamlit as st
from pipeline import run_research_pipeline

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Research Forge",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------
# Dark / black + cream theme
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --bg: #0d0d0d;
            --panel: #161616;
            --panel-border: #2a2a2a;
            --cream: #f2e9d8;
            --cream-dim: #cfc6b3;
            --accent: #d8b26a;
        }

        html, body, [class*="css"] {
            font-family: 'Georgia', 'Times New Roman', serif;
        }

        .stApp {
            background-color: var(--bg);
            color: var(--cream);
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--cream) !important;
            letter-spacing: 0.5px;
        }

        p, span, li, label, div {
            color: var(--cream-dim);
        }

        /* Title banner */
        .rf-title {
            text-align: center;
            padding: 1.2rem 0 0.4rem 0;
        }
        .rf-title h1 {
            font-size: 2.6rem;
            margin-bottom: 0.1rem;
            color: var(--cream) !important;
        }
        .rf-title p {
            color: var(--accent);
            font-size: 1rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* Input box */
        .stTextInput input {
            background-color: var(--panel) !important;
            color: var(--cream) !important;
            border: 1px solid var(--panel-border) !important;
            border-radius: 6px;
            padding: 0.7rem;
        }
        .stTextInput input:focus {
            border: 1px solid var(--accent) !important;
            box-shadow: none !important;
        }

        /* Buttons */
        .stButton button {
            background-color: var(--accent);
            color: #0d0d0d;
            font-weight: 700;
            border: none;
            border-radius: 6px;
            padding: 0.6rem 1.6rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .stButton button:hover {
            background-color: #eccf94;
            color: #0d0d0d;
        }

        /* Cards / panels for each stage */
        .rf-card {
            background-color: var(--panel);
            border: 1px solid var(--panel-border);
            border-left: 3px solid var(--accent);
            border-radius: 8px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1.2rem;
        }
        .rf-card h3 {
            margin-top: 0;
            color: var(--accent) !important;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .rf-card-content {
            color: var(--cream-dim);
            white-space: pre-wrap;
            line-height: 1.55;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: var(--panel);
            color: var(--cream-dim);
            border-radius: 6px 6px 0 0;
            border: 1px solid var(--panel-border);
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--accent) !important;
            color: #0d0d0d !important;
            font-weight: 700;
        }

        /* Divider */
        hr {
            border-color: var(--panel-border);
        }

        /* Download button */
        .stDownloadButton button {
            background-color: transparent;
            color: var(--accent);
            border: 1px solid var(--accent);
            border-radius: 6px;
        }
        .stDownloadButton button:hover {
            background-color: var(--accent);
            color: #0d0d0d;
        }

        /* Status widget */
        [data-testid="stStatusWidget"] {
            background-color: var(--panel);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="rf-title">
        <h1>Research Forge</h1>
        <p>Multi-Agent Research Pipeline</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "topic" not in st.session_state:
    st.session_state.topic = ""

# ----------------------------------------------------------------------
# Input row
# ----------------------------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of quantum computing on cryptography",
        label_visibility="collapsed",
    )
with col2:
    run_clicked = st.button("Run Pipeline", use_container_width=True)

# ----------------------------------------------------------------------
# Run the pipeline
# ----------------------------------------------------------------------
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.topic = topic
        steps = [
            "Search agent gathering sources...",
            "Reader agent scraping top result...",
            "Writer drafting the report...",
            "Critic reviewing the draft...",
        ]
        with st.status("Running multi-agent pipeline...", expanded=True) as status:
            for step_label in steps:
                st.write(step_label)
            try:
                result = run_research_pipeline(topic)
                st.session_state.result = result
                status.update(label="Pipeline complete", state="complete", expanded=False)
            except Exception as e:
                st.session_state.result = None
                status.update(label="Pipeline failed", state="error", expanded=True)
                st.error(f"Error while running pipeline: {e}")

# ----------------------------------------------------------------------
# Display results
# ----------------------------------------------------------------------
result = st.session_state.result
if result:
    st.markdown(f"### Results for: *{st.session_state.topic}*")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Report", "🧐 Critic Feedback", "🔎 Search Results", "📚 Scraped Content"]
    )

    with tab_report:
        st.markdown(
            f'<div class="rf-card"><h3>Final Report</h3>'
            f'<div class="rf-card-content">{result.get("report", "")}</div></div>',
            unsafe_allow_html=True,
        )
        st.download_button(
            "Download report (.txt)",
            data=str(result.get("report", "")),
            file_name=f"{st.session_state.topic.strip().replace(' ', '_')}_report.txt",
            mime="text/plain",
        )

    with tab_feedback:
        st.markdown(
            f'<div class="rf-card"><h3>Critic Feedback</h3>'
            f'<div class="rf-card-content">{result.get("feedback", "")}</div></div>',
            unsafe_allow_html=True,
        )

    with tab_search:
        st.markdown(
            f'<div class="rf-card"><h3>Search Results</h3>'
            f'<div class="rf-card-content">{result.get("search_results", "")}</div></div>',
            unsafe_allow_html=True,
        )

    with tab_scraped:
        st.markdown(
            f'<div class="rf-card"><h3>Scraped Content</h3>'
            f'<div class="rf-card-content">{result.get("scraped_content", "")}</div></div>',
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
        <div class="rf-card">
            <h3>How it works</h3>
            <div class="rf-card-content">
Enter a topic above and click "Run Pipeline". Four agents run in sequence:
1. Search agent finds recent, reliable sources
2. Reader agent scrapes the most relevant page
3. Writer agent drafts a report from the research
4. Critic agent reviews the report and gives feedback
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
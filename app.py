
import streamlit as st
from datetime import datetime

# Import your existing research pipeline
from src.pipelines.pipeline import run_research_pipeline


# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="ResearchAI | Multi-Agent Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #10182c 55%, #111827 100%);
        color: #f1f5f9;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #0a0f1d;
        border-right: 1px solid #253047;
    }

    .hero {
        padding: 32px 0 24px 0;
    }

    .eyebrow {
        color: #a5b4fc;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero h1 {
        font-size: clamp(32px, 4vw, 46px);
        font-weight: 800;
        line-height: 1.15;
        margin: 12px 0;
        color: #f8fafc;
    }

    .hero p {
        font-size: 16px;
        line-height: 1.7;
        color: #9caec7;
        max-width: 750px;
    }

    .panel {
        background: rgba(20, 30, 50, 0.85);
        border: 1px solid #2b3852;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .panel-title {
        font-size: 17px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }

    .muted {
        color: #94a3b8;
        font-size: 13px;
    }

    .agent-card {
        background: #131d30;
        border: 1px solid #2b3852;
        border-radius: 12px;
        padding: 16px;
        min-height: 112px;
    }

    .agent-icon {
        font-size: 22px;
        margin-bottom: 8px;
    }

    .agent-name {
        font-size: 14px;
        font-weight: 700;
        color: #e2e8f0;
    }

    .agent-desc {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 5px;
        line-height: 1.5;
    }

    .stTextInput input {
        background: #101a2b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 10px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 20px;
        font-weight: 700;
        min-height: 46px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border: none;
        filter: brightness(1.12);
        transform: translateY(-1px);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid #29364c;
    }

    .stTabs [data-baseweb="tab"] {
        color: #a8b5ca;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: #131d30;
        border: 1px solid #2b3852;
        border-radius: 12px;
        padding: 16px;
    }

    .footer {
        color: #64748b;
        text-align: center;
        font-size: 12px;
        padding: 28px 0 12px;
    }

    div[data-testid="stExpander"] {
        background: #111b2e;
        border: 1px solid #29364c;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# SESSION STATE
# =========================
if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""

if "research_history" not in st.session_state:
    st.session_state.research_history = []


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🔬 ResearchAI")
    st.caption("Multi-agent research workspace")

    st.divider()

    st.markdown("### Your AI research team")

    st.markdown("""
    **🔎 Search Agent**  
    <small>Finds recent and reliable sources.</small>

    **📖 Reader Agent**  
    <small>Extracts detailed information from a relevant URL.</small>

    **✍️ Writer Agent**  
    <small>Creates a structured research report.</small>

    **🛡️ Critic Agent**  
    <small>Reviews the generated report.</small>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Pipeline")
    st.caption("Search → Read → Write → Review")

    st.markdown(
        '<div class="muted">Built with Streamlit and your Python agent pipeline.</div>',
        unsafe_allow_html=True,
    )


# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero">
    <div class="eyebrow">AI-powered research workspace</div>
    <h1>Turn complex topics into<br>structured research.</h1>
    <p>
        Your multi-agent research assistant discovers relevant information,
        reads source material, writes a report, and reviews the result —
        all in one workflow.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# AGENT OVERVIEW
# =========================
cols = st.columns(4)

agents = [
    ("🔎", "Search Agent", "Discovers relevant sources"),
    ("📖", "Reader Agent", "Reads and extracts details"),
    ("✍️", "Writer Agent", "Drafts the research report"),
    ("🛡️", "Critic Agent", "Reviews the report"),
]

for col, (icon, name, description) in zip(cols, agents):
    with col:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-icon">{icon}</div>
            <div class="agent-name">{name}</div>
            <div class="agent-desc">{description}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")


# =========================
# RESEARCH INPUT
# =========================
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Start a new research task</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="muted">Enter a topic or question. Be specific for more useful results.</div>',
    unsafe_allow_html=True,
)

with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Latest developments in AI agents and multi-agent systems",
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(
        "🚀 Run Research Pipeline",
        use_container_width=True,
    )

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# EXECUTE PIPELINE
# =========================
if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic before continuing.")

    else:
        st.session_state.research_result = None
        st.session_state.research_topic = topic.strip()

        progress_bar = st.progress(0)
        status_box = st.status(
            "Initializing research pipeline...",
            expanded=True,
        )

        stage_placeholder = status_box.empty()

        def on_progress(step, message):
            progress_bar.progress(step / 4)
            stage_placeholder.write(f"**Step {step}/4:** {message}")
            status_box.update(
                label=f"Pipeline running — Step {step}/4",
                state="running",
                expanded=True,
            )

        try:
            with st.spinner("Your agents are working..."):
                # The pipeline must accept progress_callback.
                result = run_research_pipeline(
                    topic.strip(),
                    progress_callback=on_progress,
                )

            st.session_state.research_result = result

            st.session_state.research_history.insert(
                0,
                {
                    "topic": topic.strip(),
                    "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                },
            )

            progress_bar.progress(1.0)
            status_box.update(
                label="Research completed successfully",
                state="complete",
                expanded=False,
            )

            st.success("Your research report is ready!")

        except Exception as e:
            status_box.update(
                label="Research pipeline failed",
                state="error",
                expanded=True,
            )
            st.error(f"An error occurred: {e}")
            st.info(
                "Check your API keys, installed dependencies, "
                "agent configuration, and network connection."
            )


# =========================
# RESULTS DASHBOARD
# =========================
result = st.session_state.research_result

if result:
    st.write("")

    st.markdown("## Research results")
    st.caption(f"Topic: {st.session_state.research_topic}")

    report = result.get("report", "")
    feedback = result.get("feedback", "")
    search_result = result.get("search_result", "")
    scraped_content = result.get("scraped_content", "")

    # Support plain strings and LangChain message-like outputs.
    if hasattr(report, "content"):
        report = report.content
    if hasattr(feedback, "content"):
        feedback = feedback.content

    report = str(report)
    feedback = str(feedback)
    search_result = str(search_result)
    scraped_content = str(scraped_content)

    metric_cols = st.columns(3)

    with metric_cols[0]:
        st.metric("Pipeline stages", "4/4")

    with metric_cols[1]:
        st.metric("Search output", f"{len(search_result):,} chars")

    with metric_cols[2]:
        st.metric("Report length", f"{len(report.split()):,} words")

    tab_report, tab_sources, tab_reader, tab_critic = st.tabs([
        "📄 Final Report",
        "🔎 Search Results",
        "📖 Scraped Content",
        "🛡️ Critic Feedback",
    ])

    with tab_report:
        st.markdown("### Generated research report")

        if report.strip():
            st.markdown(report)

            st.download_button(
                label="⬇️ Download report (.md)",
                data=f"# Research Report\n\nTopic: {st.session_state.research_topic}\n\n{report}",
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=False,
            )
        else:
            st.info("The writer agent returned an empty report.")

    with tab_sources:
        st.markdown("### Search agent output")

        if search_result.strip():
            st.text_area(
                "Search results",
                value=search_result,
                height=450,
                label_visibility="collapsed",
            )
            st.download_button(
                "⬇️ Download search results",
                data=search_result,
                file_name="search_results.txt",
                mime="text/plain",
            )
        else:
            st.info("No search results were returned.")

    with tab_reader:
        st.markdown("### Reader agent output")

        if scraped_content.strip():
            st.text_area(
                "Scraped content",
                value=scraped_content,
                height=500,
                label_visibility="collapsed",
            )
            st.download_button(
                "⬇️ Download scraped content",
                data=scraped_content,
                file_name="scraped_content.txt",
                mime="text/plain",
            )
        else:
            st.info("No scraped content was returned.")

    with tab_critic:
        st.markdown("### Critic's review")

        if feedback.strip():
            st.markdown(feedback)
            st.download_button(
                "⬇️ Download critic feedback",
                data=feedback,
                file_name="critic_feedback.md",
                mime="text/markdown",
            )
        else:
            st.info("The critic agent returned no feedback.")


# =========================
# HISTORY
# =========================
with st.expander("🕘 Recent research tasks"):
    if st.session_state.research_history:
        for item in st.session_state.research_history[:10]:
            st.markdown(
                f"**{item['topic']}**  \n"
                f"<span class='muted'>{item['time']}</span>",
                unsafe_allow_html=True,
            )
            st.divider()
    else:
        st.caption("Your research tasks will appear here during this session.")


st.markdown("""
<div class="footer">
    ResearchAI · Multi-Agent Research System · Powered by your AI agents
</div>
""", unsafe_allow_html=True)

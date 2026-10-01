import streamlit as st
import os
import sys
import time
import re
from datetime import datetime
from dotenv import load_dotenv

# Ensure root workspace is in sys.path
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

# Load environment variables
load_dotenv(os.path.join(WORKSPACE_DIR, ".env"))

from src.agents.agent import get_llm
from src.pipelines.pipeline import run_research_pipeline

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AURA | Multi-Agent Research System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CUSTOM LUXURY AMBER / OBSIDIAN STYLING (NO AI BLUE/PURPLE)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Base typography & color tokens */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #0c0d11;
    --bg-surface: #14161d;
    --bg-card: #191c25;
    --bg-card-hover: #202430;
    --border-subtle: rgba(245, 158, 11, 0.15);
    --border-accent: rgba(245, 158, 11, 0.45);
    --amber-primary: #d97706;
    --amber-glow: #f59e0b;
    --amber-soft: rgba(245, 158, 11, 0.08);
    --amber-light: #fef3c7;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-emerald: #10b981;
    --accent-terracotta: #e07a5f;
}

html, body, [class*="st-"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* App Background */
.stApp {
    background-color: var(--bg-main);
    background-image: 
        radial-gradient(circle at 15% 10%, rgba(217, 119, 6, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(224, 122, 95, 0.04) 0%, transparent 45%);
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: var(--bg-surface);
    border-right: 1px solid var(--border-subtle);
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(245, 158, 11, 0.12);
}

/* Main Container spacing */
.main .block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3.5rem;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(245, 158, 11, 0.5) !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.25s ease-in-out !important;
    box-shadow: 0 4px 14px rgba(217, 119, 6, 0.25) !important;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.38) !important;
    transform: translateY(-1px);
}

div.stButton > button:active {
    transform: translateY(1px);
}

/* Secondary / Download Buttons */
div.stDownloadButton > button {
    background: var(--bg-card) !important;
    color: var(--amber-glow) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

div.stDownloadButton > button:hover {
    background: var(--bg-card-hover) !important;
    border-color: var(--amber-glow) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 10px rgba(245, 158, 11, 0.2) !important;
}

/* Text Inputs */
div[data-baseweb="input"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease;
}

div[data-baseweb="input"]:focus-within {
    border-color: var(--amber-glow) !important;
    box-shadow: 0 0 0 1px var(--amber-glow) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 4px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    border-radius: 6px !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--amber-glow) !important;
    background-color: var(--amber-soft) !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--amber-soft) !important;
    color: var(--amber-glow) !important;
    border: 1px solid var(--border-accent) !important;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

div[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

div[data-testid="stMetricValue"] {
    color: var(--amber-glow) !important;
    font-weight: 700 !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    margin-bottom: 0.75rem !important;
}

/* Markdown Custom Containers */
.aura-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border-subtle);
}

.aura-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: rgba(217, 119, 6, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.35);
    margin-bottom: 0.75rem;
}

.aura-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #f8fafc;
    margin: 0;
    line-height: 1.2;
}

.aura-title-highlight {
    background: linear-gradient(120deg, #f59e0b 0%, #e07a5f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.aura-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    line-height: 1.5;
}

/* Step Pipeline Cards */
.pipeline-step-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.15rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.25s ease;
}

.pipeline-step-card.active {
    border-color: var(--amber-glow);
    background-color: rgba(217, 119, 6, 0.08);
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.15);
}

.pipeline-step-card.completed {
    border-color: rgba(16, 185, 129, 0.4);
    background-color: rgba(16, 185, 129, 0.04);
}

.step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    background: #232733;
    color: var(--text-secondary);
}

.pipeline-step-card.active .step-number {
    background: var(--amber-primary);
    color: #ffffff;
    box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
}

.pipeline-step-card.completed .step-number {
    background: #10b981;
    color: #ffffff;
}

.step-info {
    flex: 1;
}

.step-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
}

.step-desc {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.step-status-badge {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.status-waiting {
    background: rgba(100, 116, 139, 0.2);
    color: var(--text-muted);
}

.status-running {
    background: rgba(245, 158, 11, 0.2);
    color: var(--amber-glow);
    animation: pulse 1.5s infinite;
}

.status-done {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
}

@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

/* Scorecard container */
.critic-card {
    background: var(--bg-card);
    border: 1px solid var(--border-accent);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.score-display {
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--amber-glow);
    line-height: 1;
}

.verdict-quote {
    background: var(--amber-soft);
    border-left: 4px solid var(--amber-glow);
    padding: 0.85rem 1.2rem;
    border-radius: 0 8px 8px 0;
    font-style: italic;
    color: #fef3c7;
    margin-top: 1rem;
    font-size: 0.95rem;
}

/* Source link pill */
.source-pill {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
}

.source-pill:hover {
    border-color: var(--amber-glow);
    background-color: var(--bg-card-hover);
    transform: translateX(4px);
}

.source-pill a {
    color: #f59e0b !important;
    text-decoration: none !important;
    font-weight: 600;
    font-size: 0.9rem;
    word-break: break-all;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""

if "is_running" not in st.session_state:
    st.session_state.is_running = False

if "selected_model" not in st.session_state:
    st.session_state.selected_model = os.getenv("GEMINI_MODEL", "models/gemini-3.5-flash-lite")

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def parse_critic_output(critic_text: str) -> dict:
    """Parses score, strengths, improvements and verdict from critic markdown."""
    data = {
        "score": "N/A",
        "score_val": 0,
        "strengths": [],
        "improvements": [],
        "verdict": "",
        "raw": critic_text
    }
    if not critic_text:
        return data

    # Extract score
    score_match = re.search(r"Score:\s*([0-9.]+)\s*/\s*10", critic_text, re.IGNORECASE)
    if score_match:
        data["score"] = f"{score_match.group(1)}/10"
        try:
            data["score_val"] = float(score_match.group(1))
        except ValueError:
            data["score_val"] = 7.0

    # Extract Strengths
    strengths_match = re.search(r"Strengths:(.*?)(?:Areas to improve:|One Line Verdict:|$)", critic_text, re.DOTALL | re.IGNORECASE)
    if strengths_match:
        lines = [line.strip("- *•").strip() for line in strengths_match.group(1).strip().splitlines() if line.strip("- *•").strip()]
        data["strengths"] = lines

    # Extract Areas to improve
    improve_match = re.search(r"Areas to improve:(.*?)(?:One Line Verdict:|$)", critic_text, re.DOTALL | re.IGNORECASE)
    if improve_match:
        lines = [line.strip("- *•").strip() for line in improve_match.group(1).strip().splitlines() if line.strip("- *•").strip()]
        data["improvements"] = lines

    # Extract One Line Verdict
    verdict_match = re.search(r"One Line Verdict:\s*(.*?)$", critic_text, re.DOTALL | re.IGNORECASE)
    if verdict_match:
        data["verdict"] = verdict_match.group(1).strip()
    
    return data

def extract_urls(text: str) -> list:
    """Extracts unique URLs from text."""
    if not text:
        return []
    url_pattern = r'https?://[^\s<>"\')]+'
    found = re.findall(url_pattern, text)
    # Remove trailing punctuation
    cleaned = []
    for u in found:
        u_clean = u.rstrip(".,;)>]")
        if u_clean not in cleaned:
            cleaned.append(u_clean)
    return cleaned

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;">
            <div style="background: linear-gradient(135deg, #d97706, #b45309); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                ⚡
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #f8fafc; letter-spacing: -0.01em;">AURA</div>
                <div style="font-size: 0.72rem; color: #f59e0b; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em;">Multi-Agent Intelligence</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("Autonomous Research System Powered by LangChain, LangGraph & Google Gemini.")
    st.divider()

    # 1. System Health & Keys
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #e2e8f0; margin-bottom: 8px;'>API CONNECTIVITY</div>", unsafe_allow_html=True)
    
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    tavily_key = os.getenv("TAVILY_API_KEY", "")

    col_k1, col_k2 = st.columns(2)
    with col_k1:
        if gemini_key:
            st.markdown("<div style='color: #10b981; font-size: 0.8rem;'>● Gemini API</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: #ef4444; font-size: 0.8rem;'>○ Gemini API Missing</div>", unsafe_allow_html=True)
            
    with col_k2:
        if tavily_key:
            st.markdown("<div style='color: #10b981; font-size: 0.8rem;'>● Tavily Search</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: #ef4444; font-size: 0.8rem;'>○ Tavily Missing</div>", unsafe_allow_html=True)

    with st.expander("🔑 Override API Keys", expanded=False):
        new_gemini = st.text_input("Gemini API Key", value=gemini_key, type="password", key="input_gemini_key")
        new_tavily = st.text_input("Tavily API Key", value=tavily_key, type="password", key="input_tavily_key")
        if st.button("Apply Key Changes"):
            if new_gemini:
                os.environ["GEMINI_API_KEY"] = new_gemini
            if new_tavily:
                os.environ["TAVILY_API_KEY"] = new_tavily
            st.success("API keys updated for this session!")

    st.divider()

    # 2. Model & Inference Engine
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #e2e8f0; margin-bottom: 8px;'>MODEL CONFIGURATION</div>", unsafe_allow_html=True)
    
    model_options = [
        "models/gemini-3.5-flash-lite",
        "models/gemini-3.1-flash-lite",
        "models/gemini-3.8-flash",
        "models/gemini-3.5-flash",
    ]
    
    current_default_index = 0
    if st.session_state.selected_model in model_options:
        current_default_index = model_options.index(st.session_state.selected_model)

    chosen_model = st.selectbox(
        "Active Gemini Model",
        options=model_options,
        index=current_default_index,
        help="gemini-3.5-flash-lite offers high speed, modern capabilities, and generous free quotas."
    )
    st.session_state.selected_model = chosen_model

    st.divider()

    # 3. Multi-Agent Fleet Status
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #e2e8f0; margin-bottom: 8px;'>ACTIVE AGENT FLEET</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="font-size: 0.8rem; line-height: 1.8; color: #94a3b8;">
            <div>🔍 <b>Agent 1:</b> Web Scout <span style="color: #64748b;">(Tavily API)</span></div>
            <div>📖 <b>Agent 2:</b> Deep Reader <span style="color: #64748b;">(Trafilatura + LXML)</span></div>
            <div>✍️ <b>Agent 3:</b> Synthesis Writer <span style="color: #64748b;">(Executive Report)</span></div>
            <div>⚖️ <b>Agent 4:</b> Strict Critic <span style="color: #64748b;">(Scorecard Audit)</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 4. History / Saved Sessions
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #e2e8f0; margin-bottom: 8px;'>SESSION ARCHIVE</div>", unsafe_allow_html=True)
    if st.session_state.research_history:
        for idx, item in enumerate(reversed(st.session_state.research_history)):
            topic_label = item["topic"]
            if len(topic_label) > 30:
                topic_label = topic_label[:27] + "..."
            if st.button(f"📌 {topic_label}", key=f"hist_{idx}", use_container_width=True):
                st.session_state.current_result = item["result"]
                st.session_state.current_topic = item["topic"]
                st.rerun()
        if st.button("🗑️ Clear Archive", use_container_width=True):
            st.session_state.research_history = []
            st.session_state.current_result = None
            st.rerun()
    else:
        st.caption("No previous research runs in this session.")

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="aura-header">
        <div class="aura-badge">Autonomous Multi-Agent System</div>
        <h1 class="aura-title">Next-Generation <span class="aura-title-highlight">Research Intelligence</span></h1>
        <p class="aura-subtitle">
            Deploy four specialized autonomous AI agents to explore the live web, extract deep primary source articles, synthesize executive reports, and perform critical rigorous evaluations.
        </p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RESEARCH QUERY BAR & QUICK PROMPTS
# -----------------------------------------------------------------------------
with st.container():
    col_input, col_btn = st.columns([5, 1.3])
    
    with col_input:
        user_topic = st.text_input(
            "Research Topic or Hypothesis",
            value=st.session_state.current_topic,
            placeholder="e.g. Next-Generation Solid-State Battery Commercialization and Materials Science",
            label_visibility="collapsed"
        )
    
    with col_btn:
        launch_clicked = st.button("⚡ Research", use_container_width=True, disabled=st.session_state.is_running)

    # Quick topic chips
    st.markdown("<div style='font-size: 0.8rem; color: #94a3b8; margin: 6px 0 10px 0;'>⚡ Quick Topics:</div>", unsafe_allow_html=True)
    chips = [
        "Quantum Error Correction Breakthroughs in 2026",
        "Perovskite Silicon Tandem Solar Cells Commercialization",
        "The Future of Solid-State EV Batteries",
        "Generative AI in Oncology & Precision Medicine",
    ]
    chip_cols = st.columns(len(chips))
    for i, chip in enumerate(chips):
        with chip_cols[i]:
            if st.button(chip, key=f"chip_{i}", use_container_width=True):
                st.session_state.current_topic = chip
                st.rerun()

# -----------------------------------------------------------------------------
# EXECUTION CONTROLLER
# -----------------------------------------------------------------------------
if launch_clicked:
    if not user_topic.strip():
        st.warning("Please enter a research topic or select one of the suggested topics above.")
    elif not gemini_key:
        st.error("Missing Gemini API Key! Please ensure GEMINI_API_KEY is configured in .env or the sidebar.")
    elif not tavily_key:
        st.error("Missing Tavily API Key! Please ensure TAVILY_API_KEY is configured in .env or the sidebar.")
    else:
        st.session_state.is_running = True
        st.session_state.current_topic = user_topic.strip()
        
        # UI Stepper Containers
        progress_bar = st.progress(0, text="Initializing autonomous multi-agent pipeline...")
        status_box = st.empty()

        # Step tracking
        steps = {
            "search": {"name": "Agent 1: Web Scout (Tavily Search)", "status": "running", "desc": "Scouting the live web for authoritative sources and fresh intelligence"},
            "reader": {"name": "Agent 2: Deep Reader (Article Scraper)", "status": "waiting", "desc": "Selecting highest-relevance URL and performing deep DOM & text extraction"},
            "writer": {"name": "Agent 3: Synthesis Writer", "status": "waiting", "desc": "Aggregating findings into structured executive findings and citations"},
            "critic": {"name": "Agent 4: Strict Critic", "status": "waiting", "desc": "Auditing factual rigor, methodology, weaknesses, and delivering scorecard"},
        }

        def render_stepper():
            html = "<div style='margin: 1.5rem 0;'>"
            step_keys = ["search", "reader", "writer", "critic"]
            for idx, key in enumerate(step_keys):
                s = steps[key]
                st_class = s["status"]
                badge_text = "Pending"
                if st_class == "running":
                    badge_text = "Working..."
                elif st_class == "done":
                    badge_text = "Completed"
                
                html += f"""
                <div class="pipeline-step-card {st_class}">
                    <div class="step-number">{idx + 1}</div>
                    <div class="step-info">
                        <div class="step-title">{s['name']}</div>
                        <div class="step-desc">{s['desc']}</div>
                    </div>
                    <div class="step-status-badge status-{st_class}">{badge_text}</div>
                </div>
                """
            html += "</div>"
            status_box.markdown(html, unsafe_allow_html=True)

        render_stepper()

        start_time = time.time()
        
        # Callback to update UI in real-time
        def pipeline_callback(step_id, status_type, payload):
            if step_id == "search":
                if status_type == "started":
                    steps["search"]["status"] = "running"
                    progress_bar.progress(15, text="Agent 1: Searching live web via Tavily...")
                elif status_type == "completed":
                    steps["search"]["status"] = "done"
                    steps["reader"]["status"] = "running"
                    progress_bar.progress(35, text="Agent 2: Selecting top URL & scraping full article...")
            elif step_id == "reader":
                if status_type == "started":
                    steps["reader"]["status"] = "running"
                    progress_bar.progress(40, text="Agent 2: Extracting article content via Trafilatura...")
                elif status_type == "completed":
                    steps["reader"]["status"] = "done"
                    steps["writer"]["status"] = "running"
                    progress_bar.progress(65, text="Agent 3: Drafting research report & synthesizing findings...")
            elif step_id == "writer":
                if status_type == "started":
                    steps["writer"]["status"] = "running"
                    progress_bar.progress(70, text="Agent 3: Composing structured executive report...")
                elif status_type == "completed":
                    steps["writer"]["status"] = "done"
                    steps["critic"]["status"] = "running"
                    progress_bar.progress(85, text="Agent 4: Critiquing report & generating scorecard...")
            elif step_id == "critic":
                if status_type == "started":
                    steps["critic"]["status"] = "running"
                    progress_bar.progress(90, text="Agent 4: Strict review underway...")
                elif status_type == "completed":
                    steps["critic"]["status"] = "done"
                    progress_bar.progress(100, text="All agents completed successfully!")
            render_stepper()

        try:
            # Instantiate model
            active_llm = get_llm(model_name=st.session_state.selected_model)
            
            # Execute Pipeline
            result = run_research_pipeline(
                topic=user_topic.strip(),
                step_callback=pipeline_callback,
                model=active_llm,
            )
            
            elapsed = round(time.time() - start_time, 2)
            result["elapsed_time"] = elapsed
            result["model"] = st.session_state.selected_model

            # Save to state
            st.session_state.current_result = result
            st.session_state.research_history.append({
                "topic": user_topic.strip(),
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            progress_bar.empty()
            status_box.empty()
            st.session_state.is_running = False
            st.success(f"⚡ Multi-Agent Research finished successfully in {elapsed}s!")
            st.rerun()

        except Exception as e:
            st.session_state.is_running = False
            progress_bar.empty()
            st.error(f"Pipeline execution encountered an error: {str(e)}")
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                st.info("💡 Tip: The selected model has hit a free-tier quota limit. You can switch to **gemini-3.5-flash-lite** or **gemini-3.1-flash-lite** in the sidebar for higher available quotas.")

# -----------------------------------------------------------------------------
# RESULTS DASHBOARD
# -----------------------------------------------------------------------------
if st.session_state.current_result:
    res = st.session_state.current_result
    report_text = res.get("report", "")
    critic_text = res.get("feedback", "")
    search_text = res.get("search_result", "")
    scraped_text = res.get("scraped_content", "")
    elapsed = res.get("elapsed_time", 0.0)
    used_model = res.get("model", st.session_state.selected_model)

    critic_data = parse_critic_output(critic_text)
    word_count = len(report_text.split())
    reading_time = max(1, round(word_count / 200))
    all_urls = extract_urls(search_text + "\n" + scraped_text + "\n" + report_text)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Metric Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Critic Quality Score", critic_data["score"], help="Evaluated strictly by Agent 4")
    with m_col2:
        st.metric("Total Word Count", f"{word_count:,} words")
    with m_col3:
        st.metric("Estimated Read Time", f"~{reading_time} min")
    with m_col4:
        st.metric("Pipeline Duration", f"{elapsed}s")

    # Tabbed Interface
    tab_report, tab_critic, tab_trace, tab_sources = st.tabs([
        "📄 Executive Report",
        "⚖️ Critical Review & Scorecard",
        "🔬 Agent Intelligence Trace",
        f"🔗 Sources & Citations ({len(all_urls)})"
    ])

    # TAB 1: EXECUTIVE REPORT
    with tab_report:
        col_down1, col_down2, _ = st.columns([1.5, 1.5, 5])
        with col_down1:
            st.download_button(
                label="📥 Download Markdown (.md)",
                data=report_text,
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_down2:
            st.download_button(
                label="📋 Download Plain Text (.txt)",
                data=report_text,
                file_name=f"research_report_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.markdown("""
            <div style="background-color: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 2rem; margin-top: 1rem;">
        """, unsafe_allow_html=True)
        st.markdown(report_text)
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: CRITICAL REVIEW
    with tab_critic:
        st.markdown("""
            <div class="critic-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; font-weight: 700;">
                            Independent Critic Assessment
                        </div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-top: 4px;">
                            Rigorous Peer-Review & Factual Audit
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div class="score-display">{score}</div>
                        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Overall Rigor Score</div>
                    </div>
                </div>
                {verdict_html}
            </div>
        """.format(
            score=critic_data["score"],
            verdict_html=f'<div class="verdict-quote"><b>Verdict:</b> {critic_data["verdict"]}</div>' if critic_data["verdict"] else ""
        ), unsafe_allow_html=True)

        crit_col1, crit_col2 = st.columns(2)
        with crit_col1:
            st.markdown("""
                <div style="background-color: var(--bg-card); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 1.25rem; height: 100%;">
                    <div style="color: #10b981; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 6px;">
                        <span>✓</span> Identified Strengths
                    </div>
            """, unsafe_allow_html=True)
            if critic_data["strengths"]:
                for s in critic_data["strengths"]:
                    st.markdown(f"<div style='margin-bottom: 8px; font-size: 0.88rem; color: #e2e8f0;'>• {s}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #94a3b8; font-size: 0.88rem;'>Comprehensive overview and structured points.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with crit_col2:
            st.markdown("""
                <div style="background-color: var(--bg-card); border: 1px solid rgba(224, 122, 95, 0.35); border-radius: 10px; padding: 1.25rem; height: 100%;">
                    <div style="color: #e07a5f; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 6px;">
                        <span>⚠</span> Areas to Improve & Blind Spots
                    </div>
            """, unsafe_allow_html=True)
            if critic_data["improvements"]:
                for imp in critic_data["improvements"]:
                    st.markdown(f"<div style='margin-bottom: 8px; font-size: 0.88rem; color: #e2e8f0;'>• {imp}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #94a3b8; font-size: 0.88rem;'>Expand deeper into specific citations and edge cases.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("🔍 View Raw Unparsed Critic Feedback"):
            st.text(critic_text)

    # TAB 3: AGENT INTELLIGENCE TRACE
    with tab_trace:
        st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Inspect the exact intermediary telemetry, tool outputs, and payloads exchanged between agents in this pipeline run.</p>", unsafe_allow_html=True)
        
        with st.expander("🔍 Agent 1: Search Specialist Telemetry (Tavily Output)", expanded=False):
            st.caption(f"Raw characters: {len(search_text):,}")
            st.code(search_text, language="markdown")

        with st.expander("📖 Agent 2: Document Reader Telemetry (Deep Article Scraping)", expanded=False):
            st.caption(f"Scraped characters: {len(scraped_text):,}")
            st.code(scraped_text, language="markdown")

        with st.expander("✍️ Agent 3: Synthesis Input Context (Combined Research Payload)", expanded=False):
            combined_preview = f"SEARCH RESULTS:\n{search_text}\n\nDETAILED SCRAPED CONTENT:\n{scraped_text}"
            st.caption(f"Total payload size: {len(combined_preview):,} characters")
            st.code(combined_preview[:4000] + ("..." if len(combined_preview) > 4000 else ""), language="markdown")

    # TAB 4: SOURCES & CITATIONS
    with tab_sources:
        if all_urls:
            st.markdown(f"<p style='color: #94a3b8; font-size: 0.9rem;'>Discovered <b>{len(all_urls)}</b> unique primary sources and referenced URLs during autonomous web scouting.</p>", unsafe_allow_html=True)
            for idx, url in enumerate(all_urls):
                domain = re.sub(r'^https?://(www\.)?', '', url).split('/')[0]
                st.markdown(f"""
                    <div class="source-pill">
                        <div>
                            <span style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; margin-right: 8px;">
                                {domain}
                            </span>
                            <a href="{url}" target="_blank">{url}</a>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.8rem;">↗ Open</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No external URLs were detected in the source payload.")

# Footer
st.markdown("<div style='margin-top: 4rem; text-align: center; color: #64748b; font-size: 0.8rem;'>AURA Autonomous Multi-Agent Research System &bull; LangChain &bull; Google Gemini &bull; Tavily</div>", unsafe_allow_html=True)

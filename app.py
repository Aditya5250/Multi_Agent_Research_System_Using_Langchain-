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
    page_title="Research Intelligence | Multi-Agent System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# HIGH-END OBSIDIAN & AMBER STYLING
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #0c0d11;
    --bg-surface: #13151b;
    --bg-card: #161820;
    --bg-card-hover: #1e212b;
    --border-subtle: rgba(245, 158, 11, 0.15);
    --border-accent: rgba(245, 158, 11, 0.45);
    --amber-primary: #d97706;
    --amber-glow: #f59e0b;
    --amber-soft: rgba(245, 158, 11, 0.08);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-emerald: #10b981;
    --accent-terracotta: #e07a5f;
}

/* Global typography & Executive Report Markdown */
html, body, p, h1, h2, h3, h4, h5, h6, input, textarea, li, ul, ol {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* Comprehensive Markdown Typography (Fix Issue 1: Darkened headings & bullets) */
[data-testid="stMarkdownContainer"],
.stMarkdown {
    color: #f1f5f9 !important;
}

[data-testid="stMarkdownContainer"] p,
.stMarkdown p {
    color: #f8fafc !important;
    font-size: 0.96rem !important;
    line-height: 1.75 !important;
    margin-bottom: 1.1rem !important;
}

[data-testid="stMarkdownContainer"] h1,
.stMarkdown h1 {
    color: #ffffff !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    border-bottom: 2px solid rgba(245, 158, 11, 0.45) !important;
    padding-bottom: 0.6rem !important;
    margin-top: 1.25rem !important;
    margin-bottom: 1.25rem !important;
}

[data-testid="stMarkdownContainer"] h2,
.stMarkdown h2 {
    color: #f59e0b !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    border-bottom: 1px solid rgba(245, 158, 11, 0.2) !important;
    padding-bottom: 0.45rem !important;
    margin-top: 1.6rem !important;
    margin-bottom: 0.9rem !important;
}

[data-testid="stMarkdownContainer"] h3,
.stMarkdown h3 {
    color: #fef08a !important;
    font-size: 1.18rem !important;
    font-weight: 700 !important;
    margin-top: 1.3rem !important;
    margin-bottom: 0.65rem !important;
}

[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6,
.stMarkdown h4,
.stMarkdown h5,
.stMarkdown h6 {
    color: #fde68a !important;
    font-weight: 600 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol,
.stMarkdown ul,
.stMarkdown ol {
    color: #f1f5f9 !important;
    padding-left: 1.6rem !important;
    margin-bottom: 1.2rem !important;
}

[data-testid="stMarkdownContainer"] li,
.stMarkdown li {
    color: #f1f5f9 !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    margin-bottom: 0.55rem !important;
}

[data-testid="stMarkdownContainer"] li::marker,
.stMarkdown li::marker {
    color: #f59e0b !important;
    font-weight: 700 !important;
}

[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b,
.stMarkdown strong,
.stMarkdown b {
    color: #fbbf24 !important;
    font-weight: 700 !important;
}

[data-testid="stMarkdownContainer"] em,
[data-testid="stMarkdownContainer"] i,
.stMarkdown em,
.stMarkdown i {
    color: #cbd5e1 !important;
}

[data-testid="stMarkdownContainer"] blockquote,
.stMarkdown blockquote {
    border-left: 4px solid #f59e0b !important;
    background: rgba(245, 158, 11, 0.08) !important;
    padding: 0.75rem 1.25rem !important;
    border-radius: 0 8px 8px 0 !important;
    color: #cbd5e1 !important;
    margin: 1.2rem 0 !important;
}

[data-testid="stMarkdownContainer"] a,
.stMarkdown a {
    color: #f59e0b !important;
    text-decoration: underline !important;
}

/* Executive Report dossier container box */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #141722 !important;
    background: #141722 !important;
    border: 1px solid rgba(245, 158, 11, 0.22) !important;
    border-radius: 12px !important;
    padding: 1.75rem 2rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45) !important;
    margin-top: 1rem !important;
}

/* Prevent Streamlit icon ligatures from rendering as overlapping plain text */
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-icons,
summary span {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

/* FIX: Eliminate Streamlit's white top bar completely */
header[data-testid="stHeader"],
.stAppHeader,
[data-testid="stHeader"],
header,
.stApp > header {
    background-color: var(--bg-main) !important;
    background: var(--bg-main) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

[data-testid="stToolbar"] button,
[data-testid="stToolbar"] span,
[data-testid="stToolbar"] svg {
    color: var(--text-secondary) !important;
    fill: var(--text-secondary) !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

/* App Background */
.stApp {
    background-color: var(--bg-main);
    background-image: 
        radial-gradient(circle at 15% 10%, rgba(217, 119, 6, 0.04) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(224, 122, 95, 0.03) 0%, transparent 45%);
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(245, 158, 11, 0.12) !important;
}

/* Main Container */
.main .block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 3.5rem;
}

/* SEARCH INPUT: ALWAYS DARK WITH CRISP WHITE TEXT */
div[data-testid="stTextInput"],
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] > div > div,
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="base-input"],
.stTextInput > div,
.stTextInput div[data-baseweb="input"] {
    background-color: #161820 !important;
    background: #161820 !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    box-shadow: none !important;
}

div[data-testid="stTextInput"] input,
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
.stTextInput input,
input[type="text"] {
    background-color: transparent !important;
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    caret-color: #f59e0b !important;
}

/* Hover and Focus within input */
div[data-testid="stTextInput"]:hover > div,
div[data-testid="stTextInput"] > div:hover,
div[data-baseweb="input"]:hover {
    border-color: rgba(245, 158, 11, 0.5) !important;
    background-color: #1a1d27 !important;
    background: #1a1d27 !important;
}

div[data-testid="stTextInput"]:focus-within > div,
div[data-testid="stTextInput"] > div:focus-within,
div[data-baseweb="input"]:focus-within {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 1px #f59e0b, 0 0 14px rgba(245, 158, 11, 0.25) !important;
    background-color: #1a1d27 !important;
    background: #1a1d27 !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-baseweb="input"] input::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    opacity: 1 !important;
}

div[data-testid="stTextInput"] [data-testid="InputInstructions"] {
    display: none !important;
}

/* Code Blocks Styling */
div[data-testid="stCodeBlock"],
div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code,
pre,
code {
    background-color: #13151c !important;
    background: #13151c !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(245, 158, 11, 0.15) !important;
    border-radius: 8px !important;
}

div[data-testid="stCodeBlock"] button {
    background-color: #1a1d26 !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    color: #94a3b8 !important;
}

div[data-testid="stCodeBlock"] button:hover {
    color: #f59e0b !important;
    border-color: #f59e0b !important;
}

/* AGENT INTELLIGENCE TRACE & TEXTAREA LUXURY TERMINAL STYLING (Fix Issue 2) */
div[data-testid="stTextArea"],
div[data-testid="stTextArea"] > div,
div[data-baseweb="textarea"],
div[data-baseweb="base-input"],
div[data-testid="stTextArea"] div[data-baseweb="textarea"],
div[data-testid="stTextArea"] div[data-baseweb="base-input"] {
    background-color: #0c0e14 !important;
    background: #0c0e14 !important;
    border: 1px solid rgba(245, 158, 11, 0.28) !important;
    border-radius: 10px !important;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.75), 0 2px 8px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stTextArea"]:hover > div,
div[data-testid="stTextArea"] div[data-baseweb="textarea"]:hover {
    border-color: rgba(245, 158, 11, 0.5) !important;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.75), 0 0 14px rgba(245, 158, 11, 0.15) !important;
}

div[data-testid="stTextArea"] textarea,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="base-input"] textarea,
textarea[disabled],
textarea:disabled,
textarea {
    background-color: #0c0e14 !important;
    background: #0c0e14 !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 0.86rem !important;
    line-height: 1.65 !important;
    letter-spacing: 0.015em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6) !important;
    opacity: 1 !important;
    cursor: text !important;
}

div[data-testid="stTextArea"] label,
div[data-testid="stTextArea"] label p {
    color: #f59e0b !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 6px !important;
}

div[data-testid="stTextArea"] textarea::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
div[data-testid="stTextArea"] textarea::-webkit-scrollbar-track {
    background: #0c0e14;
}
div[data-testid="stTextArea"] textarea::-webkit-scrollbar-thumb {
    background: rgba(245, 158, 11, 0.3);
    border-radius: 4px;
}
div[data-testid="stTextArea"] textarea::-webkit-scrollbar-thumb:hover {
    background: rgba(245, 158, 11, 0.6);
}

/* Amber Progress Bar */
div[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient(90deg, #d97706, #f59e0b) !important;
}
div[data-testid="stProgress"] > div > div {
    background-color: #161820 !important;
    border-radius: 6px !important;
}

/* Buttons */
button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(245, 158, 11, 0.6) !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(217, 119, 6, 0.28) !important;
    transition: all 0.2s ease-in-out !important;
}

button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.42) !important;
    transform: translateY(-1px);
}

button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background: #161820 !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.85rem !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    background: var(--amber-soft) !important;
    border-color: var(--amber-glow) !important;
    color: var(--amber-glow) !important;
    transform: translateY(-1px);
}

/* Download Buttons */
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
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

div[data-testid="stMetricValue"] {
    color: var(--amber-glow) !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
    white-space: normal !important;
    word-break: normal !important;
}

/* Header Component */
.header-container {
    margin-bottom: 1.5rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border-subtle);
}

.system-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: rgba(217, 119, 6, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.35);
    margin-bottom: 0.6rem;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #f8fafc;
    margin: 0;
    line-height: 1.2;
}

.main-title-highlight {
    background: linear-gradient(120deg, #f59e0b 0%, #e07a5f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    line-height: 1.5;
}

/* Step Pipeline Cards */
.pipeline-step-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 0.9rem 1.15rem;
    margin-bottom: 0.65rem;
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
    border-color: rgba(16, 185, 129, 0.35);
    background-color: rgba(16, 185, 129, 0.04);
}

.step-number {
    width: 30px;
    height: 30px;
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
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--text-primary);
}

.step-desc {
    font-size: 0.78rem;
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
}

.status-done {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
}

/* Critic scorecard */
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

/* Source links */
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
    transform: translateX(3px);
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

# Fixed model to eliminate sidebar clutter and ensure rock-solid quota stability
MODEL_NAME = os.getenv("GEMINI_MODEL", "models/gemini-3.5-flash-lite")

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

    score_match = re.search(r"Score:\s*([0-9.]+)\s*/\s*10", critic_text, re.IGNORECASE)
    if score_match:
        data["score"] = f"{score_match.group(1)}/10"
        try:
            data["score_val"] = float(score_match.group(1))
        except ValueError:
            data["score_val"] = 7.0

    strengths_match = re.search(r"Strengths:(.*?)(?:Areas to improve:|One Line Verdict:|$)", critic_text, re.DOTALL | re.IGNORECASE)
    if strengths_match:
        lines = [line.strip("- *•").strip() for line in strengths_match.group(1).strip().splitlines() if line.strip("- *•").strip()]
        data["strengths"] = lines

    improve_match = re.search(r"Areas to improve:(.*?)(?:One Line Verdict:|$)", critic_text, re.DOTALL | re.IGNORECASE)
    if improve_match:
        lines = [line.strip("- *•").strip() for line in improve_match.group(1).strip().splitlines() if line.strip("- *•").strip()]
        data["improvements"] = lines

    verdict_match = re.search(r"One Line Verdict:\s*(.*?)$", critic_text, re.DOTALL | re.IGNORECASE)
    if verdict_match:
        data["verdict"] = verdict_match.group(1).strip()
    
    return data

def extract_urls(text: str) -> list:
    """Extracts unique, valid HTTP/HTTPS URLs from text."""
    if not text:
        return []
    url_pattern = r'https?://[^\s<>"\'\)\]\}]+'
    found = re.findall(url_pattern, text)
    cleaned = []
    for u in found:
        u_clean = u.rstrip(".,;)>]\"'")
        # Ensure valid domain structure and min length
        if "." in u_clean and len(u_clean) > 12 and u_clean not in cleaned:
            cleaned.append(u_clean)
    return cleaned

# -----------------------------------------------------------------------------
# SIDEBAR: CLEAN & MINIMALIST (NO "AURA" BRANDING)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.75rem;">
            <div style="background: linear-gradient(135deg, #d97706, #b45309); width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px;">
                ⚡
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.05rem; color: #f8fafc; letter-spacing: -0.01em;">RESEARCH INTELLIGENCE</div>
                <div style="font-size: 0.68rem; color: #f59e0b; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em;">Multi-Agent System</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("Autonomous Multi-Agent System powered by LangChain & Tavily.")
    st.divider()

    # 1. System Health Status Card (Clean, no expanders)
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    tavily_key = os.getenv("TAVILY_API_KEY", "")

    st.markdown("""
        <div style="background-color: #161820; border: 1px solid rgba(245, 158, 11, 0.15); border-radius: 8px; padding: 0.85rem; margin-bottom: 1rem;">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.06em; margin-bottom: 8px;">
                System Health
            </div>
            <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.82rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #cbd5e1;">Google Gemini Core</span>
                    <span style="color: {gemini_color}; font-weight: 600;">{gemini_status}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #cbd5e1;">Tavily Web Search</span>
                    <span style="color: {tavily_color}; font-weight: 600;">{tavily_status}</span>
                </div>
            </div>
        </div>
    """.format(
        gemini_color="#10b981" if gemini_key else "#ef4444",
        gemini_status="Connected" if gemini_key else "Missing Key",
        tavily_color="#10b981" if tavily_key else "#ef4444",
        tavily_status="Connected" if tavily_key else "Missing Key",
    ), unsafe_allow_html=True)

    st.divider()

    # 2. Agent Fleet Architecture
    st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;'>PIPELINE AGENTS</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="font-size: 0.82rem; line-height: 2; color: #cbd5e1;">
            <div>🔍 <b>Agent 1:</b> Web Scout</div>
            <div>📖 <b>Agent 2:</b> Deep Reader</div>
            <div>✍️ <b>Agent 3:</b> Synthesis Writer</div>
            <div>⚖️ <b>Agent 4:</b> Strict Critic</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 3. Session Archive
    st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;'>RECENT RESEARCH</div>", unsafe_allow_html=True)
    if st.session_state.research_history:
        for idx, item in enumerate(reversed(st.session_state.research_history)):
            topic_label = item["topic"]
            if len(topic_label) > 28:
                topic_label = topic_label[:25] + "..."
            if st.button(f"📄 {topic_label}", key=f"hist_{idx}", use_container_width=True, type="secondary"):
                st.session_state.current_result = item["result"]
                st.session_state.current_topic = item["topic"]
                st.rerun()
        if st.button("Clear History", use_container_width=True, type="secondary"):
            st.session_state.research_history = []
            st.session_state.current_result = None
            st.rerun()
    else:
        st.caption("No reports in current session.")

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="header-container">
        <div class="system-badge">Autonomous Multi-Agent System</div>
        <h1 class="main-title">Research <span class="main-title-highlight">Intelligence</span></h1>
        <p class="main-subtitle">
            Deploy four specialized autonomous AI agents to explore the live web, extract deep primary source articles, synthesize executive reports, and perform critical rigorous evaluations.
        </p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TOPIC INPUT & MINIMALIST QUICK CHIPS
# -----------------------------------------------------------------------------
col_input, col_btn = st.columns([5, 1.2])

with col_input:
    user_topic = st.text_input(
        "Research Topic or Hypothesis",
        value=st.session_state.current_topic,
        placeholder="e.g. Next-Generation Solid-State Battery Commercialization and Materials Science",
        label_visibility="collapsed"
    )

with col_btn:
    launch_clicked = st.button("⚡ Research", type="primary", use_container_width=True, disabled=st.session_state.is_running)

# Sleek quick topic chips
st.markdown("<div style='font-size: 0.78rem; color: #64748b; margin: 6px 0 8px 0; font-weight: 600;'>Suggested Topics:</div>", unsafe_allow_html=True)
chips = [
    "Quantum Error Correction in 2026",
    "Perovskite Silicon Tandem Solar Cells",
    "Solid-State EV Battery Advancements",
    "Generative AI in Oncology & Medicine",
]
chip_cols = st.columns(len(chips))
for i, chip in enumerate(chips):
    with chip_cols[i]:
        if st.button(chip, key=f"chip_{i}", type="secondary", use_container_width=True):
            st.session_state.current_topic = chip
            st.rerun()

# -----------------------------------------------------------------------------
# PIPELINE EXECUTION
# -----------------------------------------------------------------------------
if launch_clicked:
    if not user_topic.strip():
        st.warning("Please enter a research topic or click one of the suggested topics above.")
    elif not gemini_key:
        st.error("Missing Gemini API Key! Please ensure GEMINI_API_KEY is configured in your .env file.")
    elif not tavily_key:
        st.error("Missing Tavily API Key! Please ensure TAVILY_API_KEY is configured in your .env file.")
    else:
        st.session_state.is_running = True
        st.session_state.current_topic = user_topic.strip()
        # Clear old results immediately so old dashboard/code blocks do not display underneath
        st.session_state.current_result = None
        
        progress_bar = st.progress(0, text="Initializing autonomous multi-agent pipeline...")
        status_box = st.empty()

        steps = {
            "search": {"name": "Agent 1: Web Scout", "status": "running", "desc": "Searching the live web for authoritative sources and fresh intelligence"},
            "reader": {"name": "Agent 2: Deep Reader", "status": "waiting", "desc": "Selecting highest-relevance URL and performing deep article extraction"},
            "writer": {"name": "Agent 3: Synthesis Writer", "status": "waiting", "desc": "Aggregating findings into structured executive report"},
            "critic": {"name": "Agent 4: Strict Critic", "status": "waiting", "desc": "Auditing factual rigor and delivering peer-review scorecard"},
        }

        # FIX ISSUE 2: Construct clean HTML with ZERO leading whitespace so Markdown never treats it as an indented code block
        def render_stepper():
            step_keys = ["search", "reader", "writer", "critic"]
            cards = []
            for idx, key in enumerate(step_keys):
                s = steps[key]
                st_class = s["status"]
                badge_text = "Pending"
                if st_class == "running":
                    badge_text = "Working..."
                elif st_class == "done":
                    badge_text = "Completed"
                
                # Single-line string without indentation ensures NO raw code block formatting
                card_html = (
                    f'<div class="pipeline-step-card {st_class}">'
                    f'<div class="step-number">{idx + 1}</div>'
                    f'<div class="step-info">'
                    f'<div class="step-title">{s["name"]}</div>'
                    f'<div class="step-desc">{s["desc"]}</div>'
                    f'</div>'
                    f'<div class="step-status-badge status-{st_class}">{badge_text}</div>'
                    f'</div>'
                )
                cards.append(card_html)
            
            wrapper = f'<div style="margin: 1.25rem 0;">{"".join(cards)}</div>'
            status_box.markdown(wrapper, unsafe_allow_html=True)

        render_stepper()
        start_time = time.time()
        
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
                    progress_bar.progress(100, text="Research pipeline completed!")
            render_stepper()

        try:
            active_llm = get_llm(model_name=MODEL_NAME)
            
            result = run_research_pipeline(
                topic=user_topic.strip(),
                step_callback=pipeline_callback,
                model=active_llm,
            )
            
            elapsed = round(time.time() - start_time, 2)
            result["elapsed_time"] = elapsed

            st.session_state.current_result = result
            st.session_state.research_history.append({
                "topic": user_topic.strip(),
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            progress_bar.empty()
            status_box.empty()
            st.session_state.is_running = False
            st.rerun()

        except Exception as e:
            st.session_state.is_running = False
            progress_bar.empty()
            st.error(f"Pipeline error: {str(e)}")

# -----------------------------------------------------------------------------
# RESULTS DASHBOARD
# -----------------------------------------------------------------------------
if st.session_state.current_result and not st.session_state.is_running:
    res = st.session_state.current_result
    report_text = res.get("report", "")
    critic_text = res.get("feedback", "")
    search_text = res.get("search_result", "")
    scraped_text = res.get("scraped_content", "")
    elapsed = res.get("elapsed_time", 0.0)

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

        with st.container(border=True):
            st.markdown(report_text)

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

        # Clean checkbox toggle instead of expander to completely prevent any icon/text overlap
        if st.checkbox("Show Raw Unparsed Critic Feedback", key="toggle_raw_critic"):
            st.text_area("Raw Review Output", critic_text, height=220, disabled=True)

    # TAB 3: AGENT INTELLIGENCE TRACE (Sub-tabs to eliminate all expanders and word overlapping)
    with tab_trace:
        st.markdown("<p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;'>Inspect the exact intermediary telemetry, tool outputs, and payloads exchanged between agents in this pipeline run.</p>", unsafe_allow_html=True)
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "🔍 Agent 1: Search Specialist",
            "📖 Agent 2: Document Reader",
            "✍️ Agent 3: Synthesis Input Payload"
        ])
        
        with sub_tab1:
            st.caption(f"Raw Search Characters: {len(search_text):,}")
            st.text_area("Tavily Search Telemetry", search_text, height=320, disabled=True)

        with sub_tab2:
            st.caption(f"Scraped Article Characters: {len(scraped_text):,}")
            st.text_area("Extracted Article Content", scraped_text, height=320, disabled=True)

        with sub_tab3:
            combined_preview = f"SEARCH RESULTS:\n{search_text}\n\nDETAILED SCRAPED CONTENT:\n{scraped_text}"
            st.caption(f"Total Combined Payload Size: {len(combined_preview):,} characters")
            st.text_area("Writer Input Payload", combined_preview, height=320, disabled=True)

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

# FIX ISSUE 4: Completely removed the word "AURA" from the footer
st.markdown("<div style='margin-top: 4rem; text-align: center; color: #64748b; font-size: 0.8rem;'>Research Intelligence &bull; Multi-Agent System &bull; LangChain &bull; Tavily</div>", unsafe_allow_html=True)

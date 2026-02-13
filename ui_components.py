"""
UI Components Module — Premium styled components.
"""

import streamlit as st


def inject_custom_css():
    """Inject premium CSS."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp { font-family: 'Inter', sans-serif; }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,75,75,0.15);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    .hero h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF4B4B, #FF8C42, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.5rem;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 300;
        margin: 0;
    }
    .hero .badge {
        display: inline-block;
        background: rgba(255,75,75,0.12);
        color: #FF6B6B;
        padding: 5px 14px;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.8rem;
        border: 1px solid rgba(255,75,75,0.2);
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        border: 1px solid rgba(255,255,255,0.06);
        text-align: center;
    }
    .metric-card .icon { font-size: 1.6rem; }
    .metric-card .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 4px 0 2px;
    }
    .metric-card .label {
        font-size: 0.72rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Chapter Card */
    .ch-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #FF4B4B;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .ch-card .ch-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }
    .ch-card .ch-meta {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 8px;
    }
    .ch-card .ch-summary {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.55;
    }

    /* Keyword Badges */
    .kw-badge {
        display: inline-block;
        background: rgba(59,130,246,0.12);
        color: #60a5fa;
        padding: 3px 10px;
        border-radius: 50px;
        font-size: 0.72rem;
        font-weight: 500;
        margin: 2px;
        border: 1px solid rgba(59,130,246,0.2);
    }

    /* Section Header */
    .sec-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 1.5rem 0 0.8rem;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(255,75,75,0.25);
    }

    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,75,75,0.25), transparent);
        margin: 1.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero():
    st.markdown("""
    <div class="hero">
        <h1>📘 PDF Intelligence Platform</h1>
        <p>AI-Powered Document Analysis • Smart Splitting • Reading Analytics</p>
        <span class="badge">✨ Powered by NLP & AI</span>
    </div>
    """, unsafe_allow_html=True)


def render_metric(icon, value, label):
    st.markdown(f"""
    <div class="metric-card">
        <div class="icon">{icon}</div>
        <div class="value">{value}</div>
        <div class="label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_chapter_card(name, pages, reading_time, summary, keywords):
    kw_html = ' '.join(f'<span class="kw-badge">{k}</span>' for k in keywords[:8])
    st.markdown(f"""
    <div class="ch-card">
        <div class="ch-name">📖 {name}</div>
        <div class="ch-meta">📄 {pages} &nbsp;•&nbsp; ⏱️ {reading_time}</div>
        <div class="ch-summary">{summary[:400]}</div>
        <div style="margin-top:8px">{kw_html}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section(text):
    st.markdown(f'<div class="sec-header">{text}</div>', unsafe_allow_html=True)


def render_divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

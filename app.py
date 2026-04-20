"""
PulseBoard — Main Entry Point
Predictive Business Intelligence Dashboard for SMBs.
"""
import streamlit as st
from core.session import init_session_state
from core.auth import init_auth, login_gate
from core.config import Config
from ui.styles import inject_custom_css

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PulseBoard — Predictive Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "PulseBoard v1.0 — Predictive Business Intelligence for SMBs"
    }
)

# ─── Initialize ──────────────────────────────────────────────────────────────
init_session_state()
init_auth()
inject_custom_css()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
        <h1 style="background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;font-weight:800;font-size:1.8rem;margin:0;">
        PulseBoard</h1>
        <p style="color:#94a3b8;font-size:0.8rem;margin:0.2rem 0 0;">Predictive Business Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # User info
    user_email = st.session_state.get('user_email', 'demo@pulseboard.app')
    biz_name = st.session_state.get('business_name', 'My Business')
    st.markdown(f"""
    <div style="padding:0.5rem 0;">
        <p style="color:#e2e8f0;font-size:0.95rem;font-weight:600;margin:0;">🏪 {biz_name}</p>
        <p style="color:#64748b;font-size:0.75rem;margin:0.2rem 0 0;">{user_email}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Status indicators
    status = Config.get_status()
    st.markdown(f"""
    <div style="padding:0.25rem 0;">
        <p style="color:#94a3b8;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">System Status</p>
        <p style="color:#e2e8f0;font-size:0.8rem;margin:0.3rem 0;">
            {'🟢' if status['gemini_enabled'] else '🔴'} Gemini AI</p>
        <p style="color:#e2e8f0;font-size:0.8rem;margin:0.3rem 0;">
            {'🟢' if status['firebase_enabled'] else '🟡'} Firebase {'Connected' if status['firebase_enabled'] else 'Demo Mode'}</p>
        <p style="color:#e2e8f0;font-size:0.8rem;margin:0.3rem 0;">
            {'🟢' if st.session_state.get('raw_data') is not None else '🔴'} Data {'Loaded' if st.session_state.get('raw_data') is not None else 'Not loaded'}</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Auth Gate ────────────────────────────────────────────────────────────────
if not login_gate():
    st.stop()

# ─── Landing Page Content ────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 1rem 1rem;">
    <h1 style="background:linear-gradient(135deg,#6366f1,#8b5cf6,#a78bfa);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;font-weight:800;font-size:3rem;margin-bottom:0.5rem;">
    Welcome to PulseBoard</h1>
    <p style="color:#94a3b8;font-size:1.15rem;max-width:600px;margin:0 auto;">
    AI-powered business intelligence that speaks your language.
    Forecasts, anomaly alerts, and actionable insights — all in plain English.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# Feature cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="pulse-card" style="text-align:center;min-height:200px;">
        <div style="font-size:2.5rem;margin-bottom:0.75rem;">📤</div>
        <h3 style="color:#e2e8f0;font-size:1rem;margin-bottom:0.5rem;">Upload Data</h3>
        <p style="color:#94a3b8;font-size:0.85rem;">CSV, Excel, or demo data. Auto-detects your columns.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pulse-card" style="text-align:center;min-height:200px;">
        <div style="font-size:2.5rem;margin-bottom:0.75rem;">📊</div>
        <h3 style="color:#e2e8f0;font-size:1rem;margin-bottom:0.5rem;">Live Dashboard</h3>
        <p style="color:#94a3b8;font-size:0.85rem;">Real-time KPIs, anomaly alerts, and daily insights.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="pulse-card" style="text-align:center;min-height:200px;">
        <div style="font-size:2.5rem;margin-bottom:0.75rem;">🔮</div>
        <h3 style="color:#e2e8f0;font-size:1rem;margin-bottom:0.5rem;">AI Forecasts</h3>
        <p style="color:#94a3b8;font-size:0.85rem;">4-week revenue predictions with confidence intervals.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="pulse-card" style="text-align:center;min-height:200px;">
        <div style="font-size:2.5rem;margin-bottom:0.75rem;">🎯</div>
        <h3 style="color:#e2e8f0;font-size:1rem;margin-bottom:0.5rem;">Smart Actions</h3>
        <p style="color:#94a3b8;font-size:0.85rem;">One daily action card. Plain English, no jargon.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# Quick start
st.markdown("""
<div style="text-align:center;">
    <h2 style="color:#e2e8f0;font-size:1.3rem;font-weight:600;margin-bottom:1rem;">🚀 Get Started</h2>
</div>
""", unsafe_allow_html=True)

qcol1, qcol2 = st.columns(2)
with qcol1:
    if st.button("📤 Upload Your Data", use_container_width=True, type="primary"):
        st.switch_page("pages/1_📤_Data_Upload.py")

with qcol2:
    if st.session_state.get('raw_data') is not None:
        if st.button("📊 Go to Dashboard", use_container_width=True):
            st.switch_page("pages/2_📊_Dashboard.py")
    else:
        if st.button("📊 Dashboard (load data first)", use_container_width=True, disabled=True):
            pass

# Target users
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.divider()

st.markdown("""
<div style="text-align:center;padding:1rem 0;">
    <p style="color:#64748b;font-size:0.85rem;">
    Built for <strong style="color:#94a3b8;">Retail Stores</strong> •
    <strong style="color:#94a3b8;">F&B Businesses</strong> •
    <strong style="color:#94a3b8;">Salons & Spas</strong> •
    <strong style="color:#94a3b8;">E-commerce SMBs</strong></p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align:center;padding:1rem 0;color:#475569;font-size:0.75rem;">
    PulseBoard v{Config.APP_VERSION} • Powered by Prophet + Gemini AI + Firebase
</div>
""", unsafe_allow_html=True)

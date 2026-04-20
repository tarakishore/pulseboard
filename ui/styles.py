"""
PulseBoard Custom CSS Styles
Premium glassmorphism UI with animations and responsive design.
"""
import streamlit as st


def inject_custom_css():
    """Inject all custom CSS into the Streamlit app."""
    st.markdown(get_css(), unsafe_allow_html=True)


def get_css() -> str:
    return """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === Global === */
html, body { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }

/* Apply Inter font only to relevant Streamlit elements, avoiding icons */
.stMarkdown, .stButton, .stTextInput, .stSelectbox, .stToggle, .stTab, .stMetric, [data-testid="stSidebar"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp { background: linear-gradient(180deg, #0f1725 0%, #0d1623 50%, #0f1725 100%); }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0f1725; }
::-webkit-scrollbar-thumb { background: #6366f1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #818cf8; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #131b2d 0%, #151f36 100%) !important; border-right: 2px solid rgba(99,102,241,0.15) !important; }
[data-testid="stSidebar"] .stMarkdown h1 { background: linear-gradient(135deg, #6366f1, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.8rem; }
header[data-testid="stHeader"] { background: rgba(15,23,37,0.9) !important; backdrop-filter: blur(16px); border-bottom: 1px solid rgba(99,102,241,0.1) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 12px; background: transparent; }
.stTabs [data-baseweb="tab"] { background: rgba(25,35,55,0.6); border-radius: 12px; border: 1.5px solid rgba(99,102,241,0.15); color: #a0aec0; padding: 10px 24px; font-weight: 600; transition: all 0.3s ease; }
.stTabs [data-baseweb="tab"]:hover { border-color: rgba(99,102,241,0.4); background: rgba(25,35,55,0.8); }
.stTabs [aria-selected="true"] { background: rgba(99,102,241,0.2) !important; border-color: #6366f1 !important; color: #f0f4f8 !important; }

/* === Cards === */
.pulse-card { background: rgba(25,35,55,0.75); backdrop-filter: blur(16px); border: 1.5px solid rgba(99,102,241,0.15); border-radius: 18px; padding: 1.75rem; margin-bottom: 1.25rem; transition: all 0.3s cubic-bezier(0.4,0,0.2,1); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.pulse-card:hover { border-color: rgba(99,102,241,0.35); box-shadow: 0 12px 48px rgba(99,102,241,0.12); transform: translateY(-3px); }

/* === Hero Insight Card === */
.insight-hero { background: linear-gradient(145deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.1) 100%); backdrop-filter: blur(20px); border: 2px solid rgba(99,102,241,0.3); border-radius: 22px; padding: 2.5rem; margin-bottom: 2rem; position: relative; overflow: hidden; animation: pulseGlow 3s ease-in-out infinite; box-shadow: 0 8px 32px rgba(99,102,241,0.15); }
.insight-hero::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%); animation: rotateBg 8s linear infinite; }
@keyframes pulseGlow { 0%, 100% { box-shadow: 0 8px 32px rgba(99,102,241,0.12); } 50% { box-shadow: 0 12px 48px rgba(99,102,241,0.18); } }
@keyframes rotateBg { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.insight-hero h2 { font-size: 1.75rem; font-weight: 750; color: #f8fafc; margin-bottom: 1rem; position: relative; z-index: 1; letter-spacing: -0.5px; }
.insight-hero p { font-size: 1.1rem; color: #cbd5e1; line-height: 1.7; position: relative; z-index: 1; font-weight: 500; }
.insight-hero .insight-icon { font-size: 3rem; margin-bottom: 0.75rem; position: relative; z-index: 1; }

/* === Metric Cards === */
.metric-card { background: rgba(25,35,55,0.75); backdrop-filter: blur(12px); border: 1.5px solid rgba(99,102,241,0.15); border-radius: 16px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.25); }
.metric-card:hover { border-color: rgba(99,102,241,0.35); transform: translateY(-3px); box-shadow: 0 8px 28px rgba(99,102,241,0.12); }
.metric-card .metric-value { font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #6366f1, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; }
.metric-card .metric-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem; font-weight: 700; }
.metric-card .metric-delta { font-size: 0.95rem; font-weight: 700; margin-top: 0.5rem; }
.delta-up { color: #10b981; }
.delta-down { color: #f43f5e; }

/* === Anomaly Cards === */
.anomaly-card { background: rgba(244,63,94,0.08); border: 1.5px solid rgba(244,63,94,0.25); border-radius: 14px; padding: 1.25rem; margin-bottom: 0.75rem; border-left: 5px solid #f43f5e; box-shadow: 0 2px 12px rgba(244,63,94,0.08); }
.anomaly-card strong { color: #f8fafc; font-weight: 700; }
.anomaly-card.warning { background: rgba(245,158,11,0.08); border-color: rgba(245,158,11,0.25); border-left-color: #f59e0b; box-shadow: 0 2px 12px rgba(245,158,11,0.08); }
.anomaly-card.info { background: rgba(56,189,248,0.08); border-color: rgba(56,189,248,0.25); border-left-color: #38bdf8; box-shadow: 0 2px 12px rgba(56,189,248,0.08); }

/* === Confidence Bar === */
.confidence-bar-container { margin: 0.75rem 0; }
.confidence-bar-bg { background: rgba(99,102,241,0.12); border-radius: 10px; height: 12px; overflow: hidden; border: 1px solid rgba(99,102,241,0.1); }
.confidence-bar-fill { height: 100%; border-radius: 10px; transition: width 0.8s cubic-bezier(0.4,0,0.2,1); background: linear-gradient(90deg, #6366f1, #a78bfa); box-shadow: 0 0 8px rgba(99,102,241,0.3); }
.confidence-bar-fill.high { background: linear-gradient(90deg, #10b981, #6ee7b7); box-shadow: 0 0 8px rgba(16,185,129,0.3); }
.confidence-bar-fill.medium { background: linear-gradient(90deg, #f59e0b, #fcd34d); box-shadow: 0 0 8px rgba(245,158,11,0.3); }
.confidence-bar-fill.low { background: linear-gradient(90deg, #f43f5e, #fb7185); box-shadow: 0 0 8px rgba(244,63,94,0.3); }
.confidence-label { display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-bottom: 6px; font-weight: 600; }

/* === Action Card === */
.action-card { background: linear-gradient(145deg, rgba(16,185,129,0.12) 0%, rgba(20,184,166,0.08) 100%); border: 1.5px solid rgba(16,185,129,0.25); border-radius: 16px; padding: 1.75rem; margin-bottom: 1.25rem; box-shadow: 0 4px 16px rgba(16,185,129,0.08); transition: all 0.3s ease; }
.action-card:hover { border-color: rgba(16,185,129,0.35); box-shadow: 0 6px 24px rgba(16,185,129,0.12); transform: translateY(-2px); }
.action-card h3 { color: #10b981; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem; letter-spacing: -0.3px; }
.action-card p { color: #cbd5e1; font-size: 0.98rem; line-height: 1.6; font-weight: 500; }

/* === Section Headers === */
.section-header { font-size: 1.3rem; font-weight: 800; color: #f0f4f8; margin: 2rem 0 1.25rem 0; padding-bottom: 0.75rem; border-bottom: 2px solid rgba(99,102,241,0.2); display: flex; align-items: center; gap: 0.75rem; letter-spacing: -0.3px; }

/* === Upload Zone === */
.upload-zone { border: 2.5px dashed rgba(99,102,241,0.4); border-radius: 20px; padding: 3rem 2rem; text-align: center; background: rgba(99,102,241,0.05); transition: all 0.3s ease; }
.upload-zone:hover { border-color: #6366f1; background: rgba(99,102,241,0.08); box-shadow: 0 8px 24px rgba(99,102,241,0.1); }

/* === Mobile === */
@media (max-width: 768px) {
    .insight-hero { padding: 1.5rem; }
    .insight-hero h2 { font-size: 1.4rem; }
    .insight-hero .insight-icon { font-size: 2.5rem; }
    .metric-card .metric-value { font-size: 1.8rem; }
    .pulse-card { padding: 1.25rem; }
    .section-header { font-size: 1.1rem; }
}

/* === Buttons === */
.stButton > button { border-radius: 12px !important; border: 1.5px solid rgba(99,102,241,0.25) !important; font-weight: 700 !important; transition: all 0.3s ease !important; background: rgba(99,102,241,0.1) !important; color: #f0f4f8 !important; }
.stButton > button:hover { border-color: #6366f1 !important; box-shadow: 0 0 24px rgba(99,102,241,0.25) !important; background: rgba(99,102,241,0.15) !important; }

/* === Data Table === */
.stDataFrame { border-radius: 14px; overflow: hidden; border: 1.5px solid rgba(99,102,241,0.15); }

/* Fix for 'uploadUpload' overlap and broken icons */
[data-testid="stFileUploader"] section button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
}
</style>"""

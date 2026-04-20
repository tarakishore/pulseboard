"""
PulseBoard Reusable UI Components
Cards, metrics, confidence bars, and layout helpers.
"""
import streamlit as st
from ui.theme import Colors, confidence_color


def insight_card(title: str, body: str, confidence: float = 85.0, icon: str = "💡"):
    """Render the hero Insight of the Day card with enhanced clarity."""
    conf_cls = "high" if confidence >= 80 else ("medium" if confidence >= 60 else "low")
    confidence_text = "High" if confidence >= 80 else ("Good" if confidence >= 60 else "Moderate")
    st.markdown(f"""
    <div class="insight-hero">
        <div class="insight-icon">{icon}</div>
        <h2>{title}</h2>
        <p>{body}</p>
        <div class="confidence-bar-container" style="margin-top:1.5rem;">
            <div class="confidence-label"><span>💯 Confidence Level: {confidence_text}</span><span>{confidence:.0f}%</span></div>
            <div class="confidence-bar-bg"><div class="confidence-bar-fill {conf_cls}" style="width:{confidence}%"></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str = None, delta_direction: str = "up"):
    """Render a single KPI metric card with enhanced clarity."""
    delta_html = ""
    if delta:
        cls = "delta-up" if delta_direction == "up" else "delta-down"
        arrow = "📈" if delta_direction == "up" else "📉"
        delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 {label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def anomaly_card(title: str, description: str, severity: str = "danger"):
    """Render an anomaly alert card with severity levels. severity: danger | warning | info"""
    if severity == "danger":
        icon = "🚨"
        severity_text = "Critical Alert"
    elif severity == "warning":
        icon = "⚠️"
        severity_text = "Warning"
    else:
        icon = "ℹ️"
        severity_text = "Info"
    
    cls = severity if severity in ("warning", "info") else "danger"
    st.markdown(f"""
    <div class="anomaly-card {cls}">
        <div style="font-weight:bold; font-size:1.1rem; margin-bottom:0.5rem;">{icon} {severity_text}</div>
        <div style="font-size:1.05rem; font-weight:600; color:#f8fafc; margin-bottom:0.3rem;">{title}</div>
        <div style="font-size:0.95rem; color:#cbd5e1; line-height:1.5;">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def action_card(title: str, body: str, icon: str = "🎯"):
    """Render the daily recommended action card."""
    st.markdown(f"""
    <div class="action-card">
        <h3>{icon} {title}</h3>
        <p style="margin:0.75rem 0 0 0; line-height:1.6; color:#e2e8f0;">{body}</p>
    </div>
    """, unsafe_allow_html=True)


def confidence_bar(label: str, score: float):
    """Render a standalone confidence progress bar."""
    cls = "high" if score >= 80 else ("medium" if score >= 60 else "low")
    st.markdown(f"""
    <div class="confidence-bar-container">
        <div class="confidence-label"><span>{label}</span><span>{score:.0f}%</span></div>
        <div class="confidence-bar-bg"><div class="confidence-bar-fill {cls}" style="width:{score}%"></div></div>
    </div>
    """, unsafe_allow_html=True)


def section_header(text: str, icon: str = ""):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{icon} {text}</div>', unsafe_allow_html=True)


def info_card(title: str, body: str):
    """Render a styled info card."""
    st.markdown(f"""
    <div class="pulse-card">
        <strong style="color:#f0f4f8; font-size:1.05rem;">{title}</strong>
        <p style="color:#94a3b8; margin:0.4rem 0 0 0; font-size:0.93rem;">{body}</p>
    </div>
    """, unsafe_allow_html=True)


def kpi_row(metrics: list):
    """Render a horizontal row of metric cards.
    metrics: list of dicts with keys: label, value, delta (optional), direction (optional)
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            metric_card(
                label=m["label"],
                value=m["value"],
                delta=m.get("delta"),
                delta_direction=m.get("direction", "up"),
            )

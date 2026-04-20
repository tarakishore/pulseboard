"""
PulseBoard — Page 2: Main Dashboard
Insight of the Day, KPIs, Revenue Chart, Anomaly Alerts, Action Card.
"""
import streamlit as st
import pandas as pd
from core.session import init_session_state, has_data, get_data
from data.preprocessor import prepare_prophet_data
from ml.forecaster import run_forecast
from ml.anomaly import detect_anomalies, get_anomaly_summary
from ml.metrics import calculate_kpis
from ai.insights import get_insight_of_the_day, get_action_of_the_day
from ui.styles import inject_custom_css
from ui.components import (
    insight_card, metric_card, anomaly_card, action_card,
    confidence_bar, section_header, kpi_row, info_card,
)
from ui.charts import revenue_chart, anomaly_chart, weekly_pattern_chart
from ui.theme import Colors

st.set_page_config(page_title="PulseBoard — Dashboard", page_icon="📊", layout="wide")
inject_custom_css()
init_session_state()

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:1rem;">
    <h1 style="background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;font-weight:800;font-size:2rem;margin-bottom:0.25rem;">
    📊 Dashboard</h1>
    <p style="color:#94a3b8;font-size:0.95rem;">Your business intelligence at a glance</p>
</div>
""", unsafe_allow_html=True)

# ─── Check for Data ──────────────────────────────────────────────────────────
if not has_data():
    st.markdown("""
    <div class="pulse-card" style="text-align:center;padding:3rem;">
        <div style="font-size:3rem;margin-bottom:1rem;">📤</div>
        <h3 style="color:#e2e8f0;">No Data Loaded</h3>
        <p style="color:#94a3b8;">Upload your sales data or load the demo dataset to get started.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("➡️ Go to Data Upload", use_container_width=True):
        st.switch_page("pages/1_📤_Data_Upload.py")
    st.stop()

# ─── Load & Process ──────────────────────────────────────────────────────────
df, date_col, revenue_col = get_data()

with st.spinner("🔮 Analyzing your data..."):
    # Prepare Prophet data & run forecast
    prophet_df = prepare_prophet_data(df, date_col, revenue_col)

    # Run forecast (cached)
    if st.session_state.forecast_results is None:
        forecast_result = run_forecast(prophet_df)
        st.session_state.forecast_results = forecast_result
        st.session_state.forecast_model = forecast_result['model_name']
        st.session_state.forecast_accuracy = forecast_result['accuracy']
    else:
        forecast_result = st.session_state.forecast_results

    forecast_df = forecast_result['forecast_df']
    accuracy = forecast_result['accuracy']

    # Detect anomalies
    if not st.session_state.anomalies:
        anomalies = detect_anomalies(df, date_col, revenue_col)
        st.session_state.anomalies = anomalies
    else:
        anomalies = st.session_state.anomalies

    # Calculate KPIs
    kpis = calculate_kpis(df, date_col, revenue_col, accuracy)

    # Generate insights
    insight = get_insight_of_the_day(kpis, anomalies)
    action = get_action_of_the_day(kpis, anomalies, forecast_df)

# ─── Insight of the Day (Hero) ───────────────────────────────────────────────
insight_card(
    title=insight.get('title', 'Business Insight'),
    body=insight.get('body', 'Analyzing your data...'),
    confidence=insight.get('confidence', 80),
    icon=insight.get('icon', '💡'),
)

# ─── KPI Metrics Row ─────────────────────────────────────────────────────────
section_header("Key Metrics", "📈")

kpi_row([
    {
        "label": "This Week's Revenue",
        "value": f"${kpis['current_week_revenue']:,.0f}",
        "delta": f"{kpis['revenue_change_pct']:+.1f}%",
        "direction": "up" if kpis['revenue_change_pct'] >= 0 else "down",
    },
    {
        "label": "Forecast Accuracy",
        "value": f"{accuracy:.0f}%",
        "delta": "Strong" if accuracy >= 80 else "Building",
        "direction": "up" if accuracy >= 80 else "down",
    },
    {
        "label": "Weekly Return Rate",
        "value": f"{kpis['weekly_return_rate']}%",
        "delta": "Normal range",
        "direction": "up",
    },
    {
        "label": "Est. Waste Reduction",
        "value": f"{kpis['waste_reduction']:.0f}%",
        "delta": "With PulseBoard",
        "direction": "up",
    },
])

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ─── Revenue Chart ───────────────────────────────────────────────────────────
section_header("Revenue Trend", "📈")

# Merge historical + forecast for chart
full_forecast = forecast_result.get('full_forecast')
fig = revenue_chart(df, date_col, revenue_col, full_forecast)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Confidence bar for the forecast model
col_conf1, col_conf2 = st.columns(2)
with col_conf1:
    confidence_bar(f"Model Confidence ({forecast_result['model_name']})", accuracy)
with col_conf2:
    data_quality = min(100, len(df) / 1.8)
    confidence_bar("Data Quality Score", data_quality)

# ─── Anomaly Alerts ──────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
section_header(f"Anomaly Alerts ({len(anomalies)} detected)", "⚠️")

if anomalies:
    # Show top 3 anomalies by default
    for a in anomalies[:3]:
        severity = "danger" if a.get('severity') == 'high' else "warning"
        anomaly_card(
            title=f"{a['date'].strftime('%b %d, %Y') if hasattr(a['date'], 'strftime') else a['date']}",
            description=a['description'],
            severity=severity,
        )

    if len(anomalies) > 3:
        with st.expander(f"View all {len(anomalies)} anomalies"):
            for a in anomalies[3:]:
                anomaly_card(
                    title=f"{a['date'].strftime('%b %d, %Y') if hasattr(a['date'], 'strftime') else a['date']}",
                    description=a['description'],
                    severity="warning",
                )
else:
    info_card("✅ No Anomalies", "Your revenue patterns look normal. No unusual spikes or drops detected.")

# ─── Action Card ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
section_header("Recommended Action", "🎯")
action_card(
    title=action.get('title', "Review Your Data"),
    body=action.get('body', "Check your latest sales trends and plan accordingly."),
    icon="🎯",
)

# ─── Advanced View Toggle ────────────────────────────────────────────────────
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.divider()

advanced = st.toggle("🔬 Advanced View", value=st.session_state.get('advanced_view', False), key="adv_toggle")
st.session_state.advanced_view = advanced

if advanced:
    section_header("Day-of-Week Patterns", "📊")
    fig_weekly = weekly_pattern_chart(df, date_col, revenue_col)
    st.plotly_chart(fig_weekly, use_container_width=True, config={'displayModeBar': False})

    section_header("Anomaly Map", "🗺️")
    fig_anom = anomaly_chart(df, date_col, revenue_col, anomalies)
    st.plotly_chart(fig_anom, use_container_width=True, config={'displayModeBar': False})

    section_header("Raw Data Explorer", "🔍")
    st.dataframe(df.tail(50).style.format(precision=2), use_container_width=True, height=400)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:2rem 0 1rem;color:#64748b;font-size:0.8rem;">
    Powered by {forecast_result['model_name']} • Model accuracy: {accuracy:.0f}% •
    {len(df)} data points analyzed
</div>
""", unsafe_allow_html=True)

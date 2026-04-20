"""
PulseBoard — Page 3: Forecast
4-week revenue forecast, inventory predictions, confidence intervals.
"""
import streamlit as st
import pandas as pd
from core.session import init_session_state, has_data, get_data
from data.preprocessor import prepare_prophet_data
from ml.forecaster import run_forecast
from ml.inventory import predict_inventory
from ui.styles import inject_custom_css
from ui.components import (
    section_header, metric_card, confidence_bar, info_card, kpi_row,
)
from ui.charts import forecast_chart, inventory_chart
from ui.theme import Colors

st.set_page_config(page_title="PulseBoard — Forecast", page_icon="🔮", layout="wide")
inject_custom_css()
init_session_state()

st.markdown("""
<div style="margin-bottom:1rem;">
    <h1 style="background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;font-weight:800;font-size:2rem;margin-bottom:0.25rem;">
    🔮 Revenue Forecast</h1>
    <p style="color:#94a3b8;font-size:0.95rem;">AI-powered predictions for the next 4 weeks</p>
</div>
""", unsafe_allow_html=True)

if not has_data():
    st.markdown("""
    <div class="pulse-card" style="text-align:center;padding:3rem;">
        <div style="font-size:3rem;margin-bottom:1rem;">📤</div>
        <h3 style="color:#e2e8f0;">No Data Loaded</h3>
        <p style="color:#94a3b8;">Upload your sales data first to generate forecasts.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("➡️ Go to Data Upload", use_container_width=True):
        st.switch_page("pages/1_📤_Data_Upload.py")
    st.stop()

# ─── Load Data & Forecast ────────────────────────────────────────────────────
df, date_col, revenue_col = get_data()
prophet_df = prepare_prophet_data(df, date_col, revenue_col)

with st.spinner("🔮 Generating forecasts..."):
    if st.session_state.forecast_results is None:
        forecast_result = run_forecast(prophet_df)
        st.session_state.forecast_results = forecast_result
        st.session_state.forecast_model = forecast_result['model_name']
        st.session_state.forecast_accuracy = forecast_result['accuracy']
    else:
        forecast_result = st.session_state.forecast_results

    forecast_df = forecast_result['forecast_df']
    accuracy = forecast_result['accuracy']
    model_name = forecast_result['model_name']

# ─── Forecast Summary Metrics ────────────────────────────────────────────────
section_header("Forecast Summary", "📈")

# Weekly forecast sums
if len(forecast_df) >= 28:
    week1 = forecast_df.iloc[:7]['yhat'].sum()
    week2 = forecast_df.iloc[7:14]['yhat'].sum()
    week3 = forecast_df.iloc[14:21]['yhat'].sum()
    week4 = forecast_df.iloc[21:28]['yhat'].sum()
else:
    total = forecast_df['yhat'].sum()
    week1 = total * 0.25
    week2 = total * 0.25
    week3 = total * 0.25
    week4 = total * 0.25

total_forecast = forecast_df['yhat'].sum()
current_week_actual = df.tail(7)[revenue_col].sum()
forecast_change = ((week1 - current_week_actual) / current_week_actual * 100) if current_week_actual > 0 else 0

kpi_row([
    {"label": "Next 4 Weeks Total", "value": f"${total_forecast:,.0f}",
     "delta": f"vs ${current_week_actual*4:,.0f} projected", "direction": "up" if forecast_change >= 0 else "down"},
    {"label": "Week 1 Forecast", "value": f"${week1:,.0f}",
     "delta": f"{forecast_change:+.1f}% vs current", "direction": "up" if forecast_change >= 0 else "down"},
    {"label": "Model Used", "value": model_name, "delta": f"{accuracy:.0f}% accuracy", "direction": "up"},
    {"label": "Forecast Horizon", "value": "28 days", "delta": f"{len(forecast_df)} data points", "direction": "up"},
])

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ─── Forecast Chart ──────────────────────────────────────────────────────────
section_header("4-Week Revenue Forecast", "🔮")

fig = forecast_chart(forecast_df, prophet_df, date_col='ds', revenue_col='y')
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Confidence bars
col1, col2 = st.columns(2)
with col1:
    confidence_bar("Forecast Confidence", accuracy)
with col2:
    # Calculate average confidence interval width
    if 'yhat_upper' in forecast_df.columns and 'yhat_lower' in forecast_df.columns:
        avg_width = (forecast_df['yhat_upper'] - forecast_df['yhat_lower']).mean()
        avg_yhat = forecast_df['yhat'].mean()
        precision = max(0, 100 - (avg_width / avg_yhat * 50)) if avg_yhat > 0 else 70
    else:
        precision = 75
    confidence_bar("Prediction Precision", precision)

# ─── Weekly Forecast Breakdown ───────────────────────────────────────────────
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
section_header("Weekly Breakdown", "📅")

weeks_data = []
for i in range(4):
    start_idx = i * 7
    end_idx = min(start_idx + 7, len(forecast_df))
    if start_idx < len(forecast_df):
        week_slice = forecast_df.iloc[start_idx:end_idx]
        week_rev = week_slice['yhat'].sum()
        week_low = week_slice['yhat_lower'].sum() if 'yhat_lower' in week_slice.columns else week_rev * 0.85
        week_high = week_slice['yhat_upper'].sum() if 'yhat_upper' in week_slice.columns else week_rev * 1.15
        start_date = week_slice['ds'].iloc[0].strftime('%b %d') if hasattr(week_slice['ds'].iloc[0], 'strftime') else str(week_slice['ds'].iloc[0])[:10]
        end_date = week_slice['ds'].iloc[-1].strftime('%b %d') if hasattr(week_slice['ds'].iloc[-1], 'strftime') else str(week_slice['ds'].iloc[-1])[:10]
        weeks_data.append({
            'Week': f"Week {i+1}",
            'Period': f"{start_date} — {end_date}",
            'Forecast': f"${week_rev:,.0f}",
            'Low Estimate': f"${week_low:,.0f}",
            'High Estimate': f"${week_high:,.0f}",
            'Confidence': f"{accuracy:.0f}%",
        })

if weeks_data:
    weeks_table = pd.DataFrame(weeks_data)
    st.dataframe(weeks_table, use_container_width=True, hide_index=True)

# ─── Inventory Predictions ───────────────────────────────────────────────────
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
section_header("Inventory Predictions", "📦")

with st.spinner("Calculating inventory projections..."):
    inv = predict_inventory(df, date_col, revenue_col, forecast_df)
    st.session_state.inventory_predictions = inv

inv_col1, inv_col2, inv_col3, inv_col4 = st.columns(4)
with inv_col1:
    metric_card("Daily Sales Velocity", f"{inv['daily_velocity']:.0f} units/day")
with inv_col2:
    metric_card("Weekly Demand", f"{inv['weekly_demand']:.0f} units")
with inv_col3:
    color_class = "delta-up" if inv['days_until_stockout'] > 14 else "delta-down"
    metric_card("Days Until Stockout", f"{inv['days_until_stockout']} days",
                delta="Healthy" if inv['days_until_stockout'] > 14 else "Reorder Soon",
                delta_direction="up" if inv['days_until_stockout'] > 14 else "down")
with inv_col4:
    metric_card("Reorder Point", f"{inv['reorder_point']:.0f} units")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# Inventory chart
fig_inv = inventory_chart(inv['inventory_df'])
st.plotly_chart(fig_inv, use_container_width=True, config={'displayModeBar': False})

confidence_bar("Inventory Prediction Confidence", accuracy * 0.9)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:2rem 0 1rem;color:#64748b;font-size:0.8rem;">
    Forecast generated by {model_name} • {accuracy:.0f}% accuracy •
    Next update available after new data upload
</div>
""", unsafe_allow_html=True)

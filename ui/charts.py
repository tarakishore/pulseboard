"""
PulseBoard Plotly Chart Builders
All charts use dark theme with consistent styling.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from ui.theme import Colors, PLOTLY_LAYOUT, PLOTLY_COLORS


def _apply_layout(fig, title: str = "", height: int = 400):
    """Apply the global dark theme layout to a figure."""
    fig.update_layout(**PLOTLY_LAYOUT, title_text=title, height=height)
    return fig


def revenue_chart(df: pd.DataFrame, date_col: str, revenue_col: str,
                  forecast_df: pd.DataFrame = None) -> go.Figure:
    """Line chart: actual revenue vs forecast with confidence band."""
    fig = go.Figure()

    # Actual revenue line
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[revenue_col],
        mode='lines+markers', name='Actual Revenue',
        line=dict(color=Colors.INDIGO_500, width=2.5),
        marker=dict(size=4, color=Colors.INDIGO_400),
        fill='tozeroy',
        fillcolor='rgba(99,102,241,0.06)',
    ))

    # Forecast overlay
    if forecast_df is not None and len(forecast_df) > 0:
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat'],
            mode='lines', name='Forecast',
            line=dict(color=Colors.VIOLET_500, width=2, dash='dot'),
        ))
        # Confidence band
        if 'yhat_upper' in forecast_df.columns:
            fig.add_trace(go.Scatter(
                x=pd.concat([forecast_df['ds'], forecast_df['ds'][::-1]]),
                y=pd.concat([forecast_df['yhat_upper'], forecast_df['yhat_lower'][::-1]]),
                fill='toself', fillcolor='rgba(139,92,246,0.1)',
                line=dict(color='rgba(0,0,0,0)'), name='Confidence Interval',
                showlegend=True, hoverinfo='skip',
            ))

    _apply_layout(fig, "📈 Revenue Trend", 420)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Revenue ($)")
    return fig


def forecast_chart(forecast_df: pd.DataFrame, history_df: pd.DataFrame = None,
                   date_col: str = 'ds', revenue_col: str = 'y') -> go.Figure:
    """4-week forecast chart with confidence intervals."""
    fig = go.Figure()

    if history_df is not None:
        fig.add_trace(go.Scatter(
            x=history_df[date_col], y=history_df[revenue_col],
            mode='lines', name='Historical', line=dict(color=Colors.INDIGO_500, width=2),
        ))

    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat'],
        mode='lines+markers', name='Forecast',
        line=dict(color=Colors.VIOLET_500, width=2.5),
        marker=dict(size=5, color=Colors.VIOLET_500),
    ))

    if 'yhat_upper' in forecast_df.columns:
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat_upper'],
            mode='lines', name='Upper Bound',
            line=dict(width=0), showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat_lower'],
            mode='lines', name='Confidence Interval',
            line=dict(width=0), fill='tonexty',
            fillcolor='rgba(139,92,246,0.12)',
        ))

    _apply_layout(fig, "🔮 4-Week Revenue Forecast", 450)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Forecasted Revenue ($)")
    return fig


def anomaly_chart(df: pd.DataFrame, date_col: str, revenue_col: str,
                  anomalies: list) -> go.Figure:
    """Revenue chart with anomaly points highlighted."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[revenue_col],
        mode='lines', name='Revenue',
        line=dict(color=Colors.INDIGO_500, width=2),
    ))

    if anomalies:
        anom_dates = [a['date'] for a in anomalies]
        anom_values = [a['actual'] for a in anomalies]
        colors = [Colors.DANGER if a.get('severity') == 'high' else Colors.WARNING for a in anomalies]
        fig.add_trace(go.Scatter(
            x=anom_dates, y=anom_values,
            mode='markers', name='Anomalies',
            marker=dict(size=12, color=colors, symbol='diamond',
                        line=dict(width=2, color='white')),
        ))

    _apply_layout(fig, "⚠️ Anomaly Detection", 400)
    return fig


def weekly_pattern_chart(df: pd.DataFrame, date_col: str, revenue_col: str) -> go.Figure:
    """Day-of-week revenue pattern heatmap / bar chart."""
    df = df.copy()
    df['day_of_week'] = pd.to_datetime(df[date_col]).dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    avg_by_day = df.groupby('day_of_week')[revenue_col].mean().reindex(day_order)

    fig = go.Figure(go.Bar(
        x=avg_by_day.index, y=avg_by_day.values,
        marker=dict(
            color=avg_by_day.values,
            colorscale=[[0, Colors.INDIGO_600], [0.5, Colors.INDIGO_500], [1, Colors.VIOLET_500]],
            cornerradius=6,
        ),
    ))

    _apply_layout(fig, "📊 Average Revenue by Day of Week", 350)
    fig.update_xaxes(title_text="Day")
    fig.update_yaxes(title_text="Avg Revenue ($)")
    return fig


def inventory_chart(inventory_df: pd.DataFrame) -> go.Figure:
    """Inventory levels with projected stockout line."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=inventory_df['date'], y=inventory_df['projected_stock'],
        mode='lines+markers', name='Projected Stock',
        line=dict(color=Colors.INFO, width=2.5),
        marker=dict(size=4),
        fill='tozeroy', fillcolor='rgba(56,189,248,0.06)',
    ))

    if 'reorder_point' in inventory_df.columns:
        fig.add_hline(
            y=inventory_df['reorder_point'].iloc[0],
            line_dash="dash", line_color=Colors.WARNING,
            annotation_text="Reorder Point",
            annotation_font_color=Colors.WARNING,
        )

    _apply_layout(fig, "📦 Inventory Projection", 380)
    fig.update_yaxes(title_text="Units")
    return fig

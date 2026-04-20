"""
PulseBoard Forecasting Engine
Prophet (primary) + ARIMA (fallback) for time-series revenue forecasting.
"""
import pandas as pd
import numpy as np
import streamlit as st
from core.config import Config


@st.cache_data(ttl=3600, show_spinner=False)
def run_forecast(df: pd.DataFrame, horizon_days: int = None) -> dict:
    """Run forecasting on prepared Prophet-format data (columns: ds, y).
    Returns dict with keys: forecast_df, model_name, accuracy, components.
    """
    if horizon_days is None:
        horizon_days = Config.FORECAST_HORIZON_DAYS

    # Try Prophet first, fall back to ARIMA
    try:
        return _prophet_forecast(df, horizon_days)
    except Exception as e:
        st.warning(f"Prophet unavailable ({e}). Using ARIMA fallback.")
        return _arima_forecast(df, horizon_days)


def _prophet_forecast(df: pd.DataFrame, horizon_days: int) -> dict:
    """Forecast using Facebook Prophet."""
    from prophet import Prophet

    # Configure Prophet for potentially short time-series
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=len(df) > 180,
        changepoint_prior_scale=0.05 if len(df) < 60 else 0.15,
        seasonality_prior_scale=0.1 if len(df) < 60 else 1.0,
        interval_width=0.90,
    )

    # Suppress Prophet's verbose logging
    import logging
    logging.getLogger('prophet').setLevel(logging.WARNING)
    logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

    model.fit(df)

    # Create future dataframe
    future = model.make_future_dataframe(periods=horizon_days)
    forecast = model.predict(future)

    # Split into historical fit and future forecast
    future_only = forecast[forecast['ds'] > df['ds'].max()].copy()
    historical_fit = forecast[forecast['ds'] <= df['ds'].max()].copy()

    # Calculate accuracy on historical data
    accuracy = _calculate_accuracy(df, historical_fit)

    return {
        "forecast_df": future_only[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].reset_index(drop=True),
        "full_forecast": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
        "model_name": "Prophet",
        "accuracy": accuracy,
        "historical_fit": historical_fit,
    }


def _arima_forecast(df: pd.DataFrame, horizon_days: int) -> dict:
    """Forecast using ARIMA as fallback."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    # Use Holt-Winters for simplicity and robustness
    ts = df.set_index('ds')['y']

    # Determine seasonal period
    if len(ts) >= 14:
        seasonal_periods = 7  # Weekly
    else:
        seasonal_periods = None

    try:
        if seasonal_periods and len(ts) >= 2 * seasonal_periods:
            model = ExponentialSmoothing(
                ts, trend='add', seasonal='add',
                seasonal_periods=seasonal_periods,
                initialization_method='estimated'
            ).fit(optimized=True)
        else:
            model = ExponentialSmoothing(
                ts, trend='add', seasonal=None,
                initialization_method='estimated'
            ).fit(optimized=True)
    except Exception:
        # Simplest fallback
        model = ExponentialSmoothing(
            ts, trend='add', initialization_method='estimated'
        ).fit(optimized=True)

    # Forecast
    forecast_values = model.forecast(horizon_days)
    future_dates = pd.date_range(start=ts.index.max() + pd.Timedelta(days=1), periods=horizon_days, freq='D')

    # Estimate confidence intervals (using residual std)
    residuals = ts - model.fittedvalues
    std_resid = residuals.std()

    forecast_df = pd.DataFrame({
        'ds': future_dates,
        'yhat': forecast_values.values,
        'yhat_lower': forecast_values.values - 1.645 * std_resid,
        'yhat_upper': forecast_values.values + 1.645 * std_resid,
    })

    # Historical fit
    historical_fit = pd.DataFrame({
        'ds': ts.index,
        'yhat': model.fittedvalues.values,
        'yhat_lower': model.fittedvalues.values - 1.645 * std_resid,
        'yhat_upper': model.fittedvalues.values + 1.645 * std_resid,
    })

    accuracy = _calculate_accuracy(df, historical_fit)

    return {
        "forecast_df": forecast_df,
        "full_forecast": pd.concat([historical_fit, forecast_df], ignore_index=True),
        "model_name": "Holt-Winters",
        "accuracy": accuracy,
        "historical_fit": historical_fit,
    }


def _calculate_accuracy(actual_df: pd.DataFrame, fit_df: pd.DataFrame) -> float:
    """Calculate forecast accuracy as 100 - MAPE."""
    merged = actual_df.merge(fit_df[['ds', 'yhat']], on='ds', how='inner')
    if len(merged) == 0:
        return 75.0  # Default

    actual = merged['y'].values
    predicted = merged['yhat'].values

    # Avoid division by zero
    mask = actual != 0
    if mask.sum() == 0:
        return 75.0

    mape = np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100
    accuracy = max(0, min(100, 100 - mape))
    return round(accuracy, 1)

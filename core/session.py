"""
PulseBoard Session State Manager
Manages Streamlit session state for data persistence across page navigations.
"""
import streamlit as st
import pandas as pd
from datetime import datetime


def init_session_state():
    """Initialize all session state variables with defaults."""
    defaults = {
        # --- Auth ---
        "authenticated": False,
        "user_email": "",
        "user_id": "",

        # --- Business Profile ---
        "business_name": "My Business",
        "business_category": "Retail Store",

        # --- Data ---
        "raw_data": None,           # Original uploaded DataFrame
        "processed_data": None,     # Cleaned & preprocessed DataFrame
        "date_column": None,        # Detected/selected date column name
        "revenue_column": None,     # Detected/selected revenue column name
        "data_uploaded_at": None,   # Timestamp of last upload

        # --- Forecasting ---
        "forecast_results": None,   # Prophet/ARIMA forecast DataFrame
        "forecast_model": None,     # 'prophet' or 'arima'
        "forecast_accuracy": None,  # MAPE-based accuracy score
        "forecast_generated_at": None,

        # --- Anomalies ---
        "anomalies": [],            # List of detected anomalies

        # --- AI Insights ---
        "insight_of_the_day": None, # Dict with title, body, confidence, action
        "ai_summaries": {},         # Cached AI summaries
        "last_insight_date": None,

        # --- Inventory ---
        "inventory_predictions": None,

        # --- UI State ---
        "advanced_view": False,     # Advanced charts toggle
        "current_page": "Dashboard",

        # --- Settings ---
        "notification_email": True,
        "notification_frequency": "Weekly",
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def set_data(raw_df: pd.DataFrame, date_col: str, revenue_col: str):
    """Store uploaded and validated data in session state."""
    st.session_state.raw_data = raw_df
    st.session_state.date_column = date_col
    st.session_state.revenue_column = revenue_col
    st.session_state.data_uploaded_at = datetime.now().isoformat()
    # Clear stale results
    st.session_state.forecast_results = None
    st.session_state.anomalies = []
    st.session_state.insight_of_the_day = None
    st.session_state.inventory_predictions = None


def get_data() -> tuple:
    """Retrieve the current data from session state.
    Returns (processed_data or raw_data, date_col, revenue_col) or (None, None, None).
    """
    df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.raw_data
    return df, st.session_state.date_column, st.session_state.revenue_column


def has_data() -> bool:
    """Check if data has been uploaded and validated."""
    return st.session_state.raw_data is not None and st.session_state.date_column is not None


def clear_data():
    """Clear all data and related results from session state."""
    keys_to_clear = [
        "raw_data", "processed_data", "date_column", "revenue_column",
        "data_uploaded_at", "forecast_results", "forecast_model",
        "forecast_accuracy", "forecast_generated_at", "anomalies",
        "insight_of_the_day", "ai_summaries", "inventory_predictions",
    ]
    for key in keys_to_clear:
        st.session_state[key] = None if key != "anomalies" else []

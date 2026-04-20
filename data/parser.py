"""
PulseBoard Data Parser
Handles CSV, Excel file uploads and auto-detection.
"""
import pandas as pd
import streamlit as st
import io


def parse_uploaded_file(uploaded_file) -> pd.DataFrame:
    """Parse an uploaded CSV or Excel file into a DataFrame."""
    if uploaded_file is None:
        return None

    filename = uploaded_file.name.lower()
    try:
        if filename.endswith('.csv'):
            return _parse_csv(uploaded_file)
        elif filename.endswith(('.xlsx', '.xls')):
            return _parse_excel(uploaded_file)
        else:
            st.error(f"Unsupported file type: {filename}. Please upload CSV or Excel.")
            return None
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")
        return None


def _parse_csv(file) -> pd.DataFrame:
    """Parse CSV with encoding detection and delimiter guessing."""
    content = file.read()
    file.seek(0)

    # Try common encodings
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            text = content.decode(encoding)
            # Detect delimiter
            first_line = text.split('\n')[0]
            if '\t' in first_line:
                sep = '\t'
            elif ';' in first_line:
                sep = ';'
            else:
                sep = ','
            df = pd.read_csv(io.StringIO(text), sep=sep)
            return df
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue

    st.error("Could not parse the CSV file. Please check the file encoding.")
    return None


def _parse_excel(file) -> pd.DataFrame:
    """Parse Excel file."""
    return pd.read_excel(file, engine='openpyxl')


def load_sample_data() -> pd.DataFrame:
    """Load the built-in sample dataset for demo purposes."""
    import os
    sample_path = os.path.join(os.path.dirname(__file__), 'sample_data.csv')
    if os.path.exists(sample_path):
        return pd.read_csv(sample_path)
    else:
        return _generate_sample_data()


def _generate_sample_data() -> pd.DataFrame:
    """Generate synthetic sample data if the CSV is missing."""
    import numpy as np
    np.random.seed(42)
    dates = pd.date_range(start='2025-10-01', end='2026-04-15', freq='D')
    n = len(dates)

    # Base revenue with trend + seasonality
    base = 1200
    trend = np.linspace(0, 200, n)
    weekly_pattern = np.array([0.85, 0.78, 0.90, 0.95, 1.15, 1.30, 1.10])
    day_factors = np.array([weekly_pattern[d.weekday()] for d in dates])
    noise = np.random.normal(0, 80, n)

    revenue = (base + trend) * day_factors + noise
    revenue = np.maximum(revenue, 100)  # Floor

    # Add a few anomalies
    revenue[45] *= 1.8   # Spike
    revenue[120] *= 0.4  # Drop
    revenue[160] *= 1.6  # Spike

    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'revenue': np.round(revenue, 2),
        'transactions': np.random.randint(15, 85, n),
        'avg_order_value': np.round(revenue / np.random.randint(15, 85, n), 2),
    })
    return df

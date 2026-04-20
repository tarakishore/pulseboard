"""
PulseBoard Data Preprocessor
Cleaning, normalization, and synthetic bootstrapping for sparse data.
"""
import pandas as pd
import numpy as np


def preprocess_data(df: pd.DataFrame, date_col: str, revenue_col: str) -> pd.DataFrame:
    """Clean and preprocess data for forecasting."""
    df = df.copy()

    # Convert date column to datetime
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=[date_col])

    # Sort by date
    df = df.sort_values(date_col).reset_index(drop=True)

    # Handle missing revenue values via interpolation
    if df[revenue_col].isna().any():
        df[revenue_col] = df[revenue_col].interpolate(method='linear').ffill().bfill()

    # Ensure revenue is numeric
    df[revenue_col] = pd.to_numeric(df[revenue_col], errors='coerce')
    df = df.dropna(subset=[revenue_col])

    return df


def prepare_prophet_data(df: pd.DataFrame, date_col: str, revenue_col: str) -> pd.DataFrame:
    """Convert data to Prophet's expected format: columns 'ds' and 'y'."""
    prophet_df = df[[date_col, revenue_col]].copy()
    prophet_df.columns = ['ds', 'y']
    prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
    return prophet_df


def bootstrap_sparse_data(df: pd.DataFrame, date_col: str, revenue_col: str,
                          target_rows: int = 60) -> pd.DataFrame:
    """Generate synthetic data for very short time-series (<30 data points).
    Uses pattern replication with noise to extend the dataset.
    """
    if len(df) >= target_rows:
        return df

    df = df.copy()
    n_existing = len(df)
    n_needed = target_rows - n_existing

    # Calculate stats from existing data
    mean_rev = df[revenue_col].mean()
    std_rev = df[revenue_col].std()
    if std_rev == 0:
        std_rev = mean_rev * 0.1

    # Get the date frequency
    dates = pd.to_datetime(df[date_col])
    if len(dates) >= 2:
        freq = pd.infer_freq(dates) or 'D'
    else:
        freq = 'D'

    # Generate synthetic dates before the start of existing data
    start_date = dates.min()
    synthetic_dates = pd.date_range(end=start_date - pd.Timedelta(days=1), periods=n_needed, freq=freq)

    # Generate synthetic revenue with similar patterns
    if n_existing >= 7:
        # Replicate weekly patterns
        weekly_pattern = []
        for i in range(7):
            day_data = df[pd.to_datetime(df[date_col]).dt.dayofweek == i][revenue_col]
            weekly_pattern.append(day_data.mean() if len(day_data) > 0 else mean_rev)
        weekly_pattern = np.array(weekly_pattern)
        synthetic_revenue = np.array([weekly_pattern[d.weekday()] for d in synthetic_dates])
        noise = np.random.normal(0, std_rev * 0.3, n_needed)
        synthetic_revenue += noise
    else:
        synthetic_revenue = np.random.normal(mean_rev, std_rev * 0.5, n_needed)

    synthetic_revenue = np.maximum(synthetic_revenue, 0)

    synthetic_df = pd.DataFrame({
        date_col: synthetic_dates,
        revenue_col: np.round(synthetic_revenue, 2),
    })

    # Add any other numeric columns with reasonable defaults
    for col in df.select_dtypes(include=[np.number]).columns:
        if col != revenue_col and col not in synthetic_df.columns:
            synthetic_df[col] = df[col].mean()

    combined = pd.concat([synthetic_df, df], ignore_index=True)
    combined = combined.sort_values(date_col).reset_index(drop=True)
    return combined

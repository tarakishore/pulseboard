"""
PulseBoard Data Validator
Auto-detect date and revenue columns, validate data quality.
"""
import pandas as pd
import numpy as np
import re


def detect_date_column(df: pd.DataFrame) -> str:
    """Auto-detect the date/datetime column in a DataFrame."""
    # 1. Check for datetime dtype columns
    dt_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if dt_cols:
        return dt_cols[0]

    # 2. Check column names for date-like names
    date_keywords = ['date', 'time', 'day', 'month', 'year', 'period', 'timestamp', 'dt']
    for col in df.columns:
        if any(kw in col.lower() for kw in date_keywords):
            # Try to parse it
            try:
                pd.to_datetime(df[col].head(20))
                return col
            except (ValueError, TypeError):
                continue

    # 3. Try parsing every object column
    for col in df.select_dtypes(include=['object']).columns:
        try:
            parsed = pd.to_datetime(df[col].head(20))
            if parsed.notna().sum() >= 15:
                return col
        except (ValueError, TypeError):
            continue

    return None


def detect_revenue_column(df: pd.DataFrame, date_col: str = None) -> str:
    """Auto-detect the revenue/sales column."""
    # 1. Check column names for revenue-like names
    revenue_keywords = ['revenue', 'sales', 'amount', 'total', 'income', 'value', 'price', 'gross', 'net']
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in numeric_cols:
        if any(kw in col.lower() for kw in revenue_keywords):
            return col

    # 2. Exclude date column, pick the first numeric column with reasonable values
    candidates = [c for c in numeric_cols if c != date_col]
    if candidates:
        # Prefer columns with higher variance (likely revenue, not counts)
        best = max(candidates, key=lambda c: df[c].std() if df[c].std() > 0 else 0)
        return best

    return None


def validate_data(df: pd.DataFrame, date_col: str, revenue_col: str) -> dict:
    """Validate data quality and return a report."""
    report = {
        "is_valid": True,
        "row_count": len(df),
        "warnings": [],
        "errors": [],
        "stats": {},
    }

    # Check minimum rows
    if len(df) < 7:
        report["errors"].append("Need at least 7 data points for any analysis.")
        report["is_valid"] = False
    elif len(df) < 14:
        report["warnings"].append(f"Only {len(df)} data points. Forecasts may be less accurate. 30+ recommended.")

    # Check for nulls
    null_dates = df[date_col].isna().sum()
    null_revenue = df[revenue_col].isna().sum()
    if null_dates > 0:
        report["warnings"].append(f"{null_dates} missing date values will be removed.")
    if null_revenue > 0:
        pct = null_revenue / len(df) * 100
        report["warnings"].append(f"{null_revenue} missing revenue values ({pct:.1f}%). These will be interpolated.")

    # Check for negative values
    neg_count = (df[revenue_col] < 0).sum()
    if neg_count > 0:
        report["warnings"].append(f"{neg_count} negative revenue values detected. These may indicate returns.")

    # Basic stats
    report["stats"] = {
        "min_date": str(df[date_col].min()),
        "max_date": str(df[date_col].max()),
        "avg_revenue": float(df[revenue_col].mean()),
        "total_revenue": float(df[revenue_col].sum()),
        "std_revenue": float(df[revenue_col].std()),
    }

    return report

"""
PulseBoard Anomaly Detection
Detects unusual spikes and drops in revenue data.
"""
import pandas as pd
import numpy as np


def detect_anomalies(df: pd.DataFrame, date_col: str, revenue_col: str,
                     z_threshold: float = 2.0) -> list:
    """Detect anomalies using Z-score and day-of-week comparison.
    Returns list of anomaly dicts with: date, actual, expected, deviation_pct, severity, description.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    anomalies = []

    # --- Method 1: Global Z-score ---
    mean_rev = df[revenue_col].mean()
    std_rev = df[revenue_col].std()
    if std_rev > 0:
        df['z_score'] = (df[revenue_col] - mean_rev) / std_rev
        z_anomalies = df[df['z_score'].abs() > z_threshold]

        for _, row in z_anomalies.iterrows():
            dev_pct = ((row[revenue_col] - mean_rev) / mean_rev) * 100
            direction = "spike" if dev_pct > 0 else "drop"
            severity = "high" if abs(row['z_score']) > 3 else "medium"
            anomalies.append({
                'date': row[date_col],
                'actual': round(float(row[revenue_col]), 2),
                'expected': round(float(mean_rev), 2),
                'deviation_pct': round(float(dev_pct), 1),
                'severity': severity,
                'direction': direction,
                'description': f"Revenue {direction} of {abs(dev_pct):.0f}% on {row[date_col].strftime('%A, %b %d')}",
                'method': 'z_score',
            })

    # --- Method 2: Day-of-week comparison ---
    df['day_name'] = df[date_col].dt.day_name()
    day_stats = df.groupby('day_name')[revenue_col].agg(['mean', 'std']).to_dict('index')

    for _, row in df.iterrows():
        day = row['day_name']
        if day in day_stats and day_stats[day]['std'] > 0:
            day_mean = day_stats[day]['mean']
            day_std = day_stats[day]['std']
            day_z = abs(row[revenue_col] - day_mean) / day_std
            dev_pct = ((row[revenue_col] - day_mean) / day_mean) * 100

            if day_z > z_threshold and abs(dev_pct) > 25:
                # Avoid duplicates
                date_already = any(a['date'] == row[date_col] for a in anomalies)
                if not date_already:
                    direction = "higher" if dev_pct > 0 else "lower"
                    anomalies.append({
                        'date': row[date_col],
                        'actual': round(float(row[revenue_col]), 2),
                        'expected': round(float(day_mean), 2),
                        'deviation_pct': round(float(dev_pct), 1),
                        'severity': 'medium',
                        'direction': direction,
                        'description': f"Your {day} sales are {abs(dev_pct):.0f}% {direction} than usual",
                        'method': 'day_of_week',
                    })

    # Sort by date descending (most recent first), limit to top 10
    anomalies.sort(key=lambda x: x['date'], reverse=True)
    return anomalies[:10]


def get_anomaly_summary(anomalies: list) -> str:
    """Generate a short summary of detected anomalies."""
    if not anomalies:
        return "No unusual patterns detected. Your revenue is trending normally."

    n = len(anomalies)
    spikes = sum(1 for a in anomalies if 'spike' in a.get('direction', '') or 'higher' in a.get('direction', ''))
    drops = n - spikes

    parts = []
    if spikes:
        parts.append(f"{spikes} unusual spike{'s' if spikes > 1 else ''}")
    if drops:
        parts.append(f"{drops} unusual drop{'s' if drops > 1 else ''}")

    return f"Detected {' and '.join(parts)} in your recent revenue data."

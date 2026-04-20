"""
PulseBoard Inventory Prediction
Estimates stock levels, reorder points, and sales velocity.
"""
import pandas as pd
import numpy as np


def predict_inventory(df: pd.DataFrame, date_col: str, revenue_col: str,
                      forecast_df: pd.DataFrame = None,
                      avg_item_price: float = None) -> dict:
    """Generate inventory predictions based on sales velocity.
    Returns dict with: daily_velocity, days_projection, reorder_point, inventory_df.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    # Estimate units sold (if we only have revenue, estimate from avg price)
    if avg_item_price is None:
        avg_item_price = df[revenue_col].median() / 10  # Rough estimate

    df['estimated_units'] = (df[revenue_col] / avg_item_price).round(0)

    # Calculate sales velocity (7-day rolling average of units/day)
    recent = df.tail(30)
    daily_velocity = recent['estimated_units'].mean()
    velocity_std = recent['estimated_units'].std()

    # Project inventory depletion for next 28 days
    projection_days = 28
    last_date = df[date_col].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=projection_days, freq='D')

    # Use forecast to adjust velocity if available
    if forecast_df is not None and len(forecast_df) > 0:
        forecast_velocity = (forecast_df['yhat'] / avg_item_price).values
        if len(forecast_velocity) >= projection_days:
            daily_units = forecast_velocity[:projection_days]
        else:
            daily_units = np.full(projection_days, daily_velocity)
            daily_units[:len(forecast_velocity)] = forecast_velocity
    else:
        daily_units = np.full(projection_days, daily_velocity)

    # Assume starting inventory is 2 weeks worth of stock
    starting_inventory = daily_velocity * 14
    cumulative_sales = np.cumsum(daily_units)
    projected_stock = starting_inventory - cumulative_sales

    # Reorder point: when stock hits 5 days of supply
    lead_time_days = 5
    safety_stock = daily_velocity * 2
    reorder_point = (daily_velocity * lead_time_days) + safety_stock

    # Days until stockout
    stockout_idx = np.where(projected_stock <= 0)[0]
    days_until_stockout = int(stockout_idx[0]) + 1 if len(stockout_idx) > 0 else projection_days

    inventory_df = pd.DataFrame({
        'date': future_dates,
        'projected_stock': np.maximum(projected_stock, 0).round(0),
        'daily_demand': daily_units.round(0),
        'reorder_point': reorder_point,
    })

    return {
        'daily_velocity': round(float(daily_velocity), 1),
        'velocity_std': round(float(velocity_std), 1),
        'starting_inventory': round(float(starting_inventory), 0),
        'reorder_point': round(float(reorder_point), 0),
        'days_until_stockout': days_until_stockout,
        'safety_stock': round(float(safety_stock), 0),
        'weekly_demand': round(float(daily_velocity * 7), 0),
        'inventory_df': inventory_df,
    }

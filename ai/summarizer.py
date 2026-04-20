"""
PulseBoard AI Summarizer
Gemini API integration with template-based fallback using the new google-genai SDK.
"""
import json
import streamlit as st
from google import genai
from google.genai import types
from core.config import Config


def generate_insight(kpis: dict, anomalies: list, category: str = "Retail Store") -> dict:
    """Generate the Insight of the Day. Uses Gemini if available, else templates."""
    if Config.GEMINI_ENABLED:
        try:
            return _gemini_insight(kpis, anomalies)
        except Exception as e:
            st.warning(f"AI summary unavailable: {e}. Using built-in insights.")
    return _template_insight(kpis, anomalies)


def generate_action(kpis: dict, anomalies: list, forecast_df=None, category: str = "Retail Store") -> dict:
    """Generate the daily recommended action."""
    if Config.GEMINI_ENABLED:
        try:
            return _gemini_action(kpis, anomalies, forecast_df, category)
        except Exception:
            pass
    return _template_action(kpis, anomalies)


def explain_anomaly(anomaly: dict) -> str:
    """Generate a plain-English explanation for an anomaly."""
    if Config.GEMINI_ENABLED:
        try:
            return _gemini_explain_anomaly(anomaly)
        except Exception:
            pass
    return anomaly.get('description', 'Unusual revenue pattern detected.')


# ─── Gemini Implementations ─────────────────────────────────────────────────

def _get_gemini_client():
    return genai.Client(api_key=Config.GEMINI_API_KEY)


def _gemini_insight(kpis: dict, anomalies: list) -> dict:
    from ai.prompts import SYSTEM_PROMPT, INSIGHT_PROMPT
    client = _get_gemini_client()

    anomaly_details = ""
    if anomalies:
        for a in anomalies[:3]:
            anomaly_details += f"- {a['description']}\n"

    prompt = f"{SYSTEM_PROMPT}\n\n{INSIGHT_PROMPT.format(avg_daily=kpis.get('avg_daily_revenue', 0), current_week=kpis.get('current_week_revenue', 0), prev_week=kpis.get('prev_week_revenue', 0), change_pct=kpis.get('revenue_change_pct', 0), accuracy=kpis.get('forecast_accuracy', 75), anomaly_count=len(anomalies), anomaly_details=anomaly_details or 'None')}"

    response = client.models.generate_content(
        model=Config.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7)
    )
    text = response.text.strip()
    
    # Clean up markdown JSON wrappers if Gemini returns them
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"title": "Weekly Revenue Insight", "body": text, "confidence": 80, "icon": "💡"}


def _gemini_action(kpis, anomalies, forecast_df, category):
    from ai.prompts import SYSTEM_PROMPT, ACTION_PROMPT
    client = _get_gemini_client()
    
    change = kpis.get('revenue_change_pct', 0)
    trend_dir = "up" if change > 0 else "down" if change < 0 else "flat"
    top_anomaly = anomalies[0]['description'] if anomalies else "None detected"
    next_week = forecast_df['yhat'].sum() if forecast_df is not None and len(forecast_df) > 0 else kpis.get('current_week_revenue', 0)

    prompt = f"{SYSTEM_PROMPT}\n\n{ACTION_PROMPT.format(trend_direction=trend_dir, change_pct=change, top_anomaly=top_anomaly, next_week_forecast=next_week, category=category)}"

    response = client.models.generate_content(
        model=Config.GEMINI_MODEL,
        contents=prompt,
    )
    text = response.text.strip()
    
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"title": "Today's Action", "body": text}


def _gemini_explain_anomaly(anomaly):
    from ai.prompts import SYSTEM_PROMPT, ANOMALY_PROMPT
    client = _get_gemini_client()
    
    prompt = f"{SYSTEM_PROMPT}\n\n{ANOMALY_PROMPT.format(date=anomaly['date'].strftime('%B %d') if hasattr(anomaly['date'], 'strftime') else str(anomaly['date']), actual=anomaly['actual'], expected=anomaly['expected'], deviation_pct=anomaly['deviation_pct'], day_name=anomaly['date'].strftime('%A') if hasattr(anomaly['date'], 'strftime') else 'N/A')}"
    
    response = client.models.generate_content(
        model=Config.GEMINI_MODEL,
        contents=prompt,
    )
    return response.text.strip()


# ─── Template Fallbacks ──────────────────────────────────────────────────────

def _template_insight(kpis: dict, anomalies: list) -> dict:
    """Generate insight using templates when Gemini is not available."""
    change = kpis.get('revenue_change_pct', 0)
    current = kpis.get('current_week_revenue', 0)
    accuracy = kpis.get('forecast_accuracy', 75)

    if anomalies and len(anomalies) > 0:
        top = anomalies[0]
        return {
            "title": "Anomaly Detected in Your Revenue",
            "body": f"{top['description']}. Your current week revenue is ${current:,.0f} ({change:+.1f}% vs last week). Consider reviewing what changed on that day.",
            "confidence": accuracy,
            "icon": "⚠️",
        }
    elif change > 10:
        return {
            "title": "Great Week — Revenue Is Surging! 🚀",
            "body": f"Your revenue is up {change:.1f}% compared to last week, reaching ${current:,.0f}. This is a strong upward trend — keep doing what you're doing!",
            "confidence": accuracy,
            "icon": "🚀",
        }
    elif change < -10:
        return {
            "title": "Revenue Dip This Week",
            "body": f"Revenue dropped {abs(change):.1f}% to ${current:,.0f} this week. This could be seasonal. Review your recent promotions and foot traffic patterns.",
            "confidence": accuracy,
            "icon": "📉",
        }
    else:
        return {
            "title": "Steady Revenue This Week",
            "body": f"Your revenue is holding steady at ${current:,.0f} ({change:+.1f}% vs last week). Consistency is good — now's a great time to test a small promotion.",
            "confidence": accuracy,
            "icon": "💡",
        }


def _template_action(kpis: dict, anomalies: list) -> dict:
    """Generate action recommendation using templates."""
    change = kpis.get('revenue_change_pct', 0)

    if change < -15:
        return {
            "title": "Launch a Flash Promotion",
            "body": "Revenue is down significantly. Consider running a limited-time discount or bundle deal to drive traffic this week."
        }
    elif change > 15:
        return {
            "title": "Double Down on What's Working",
            "body": "Revenue is up! Review what drove this week's sales and consider extending any active promotions or restocking popular items."
        }
    elif anomalies:
        return {
            "title": "Investigate the Revenue Anomaly",
            "body": f"Review what happened around {anomalies[0]['date'].strftime('%b %d') if hasattr(anomalies[0]['date'], 'strftime') else anomalies[0]['date']}. Check for external events, weather changes, or staffing issues."
        }
    else:
        return {
            "title": "Review Your Top Sellers",
            "body": "Business is steady. Take a few minutes to review your best-selling items and ensure you have enough stock for the coming week."
        }

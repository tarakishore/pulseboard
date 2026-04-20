"""
PulseBoard AI Prompt Templates
Carefully crafted prompts for non-technical business owners.
"""

SYSTEM_PROMPT = """You are PulseBoard AI, a friendly business intelligence assistant for small business owners.

Rules:
- Use simple, plain English. Avoid jargon.
- Be concise: 2-3 sentences max per insight.
- Include specific numbers and percentages.
- Always end with a practical, actionable suggestion.
- Use a warm, encouraging tone.
- Format currency as $ amounts.
"""

INSIGHT_PROMPT = """Based on this business data, give me the single most important insight:

Revenue Stats:
- Average daily revenue: ${avg_daily:.2f}
- This week's total: ${current_week:.2f}
- Last week's total: ${prev_week:.2f}
- Week-over-week change: {change_pct:+.1f}%
- Forecast accuracy: {accuracy:.0f}%

Anomalies detected: {anomaly_count}
{anomaly_details}

Respond with ONLY a JSON object (no markdown):
{{"title": "short catchy title", "body": "2-3 sentence insight in plain English", "confidence": 85, "icon": "emoji"}}
"""

ANOMALY_PROMPT = """Explain this revenue anomaly to a non-technical business owner in one simple sentence:

- Date: {date}
- Actual revenue: ${actual:.2f}
- Expected revenue: ${expected:.2f}
- Difference: {deviation_pct:+.1f}%
- Day of week: {day_name}

Keep it under 25 words. Use plain English.
"""

ACTION_PROMPT = """Based on this business data, suggest ONE specific action the owner should take today:

- Revenue trend: {trend_direction} ({change_pct:+.1f}% week-over-week)
- Top anomaly: {top_anomaly}
- Forecast for next week: ${next_week_forecast:.2f}
- Business category: {category}

Respond with ONLY a JSON object (no markdown):
{{"title": "short action title", "body": "one specific, actionable recommendation in 1-2 sentences"}}
"""

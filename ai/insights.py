"""
PulseBoard Insight Generation
Picks the most impactful daily insight and manages insight state.
"""
import streamlit as st
from datetime import date
from ai.summarizer import generate_insight, generate_action


def get_insight_of_the_day(kpis: dict, anomalies: list, force_refresh: bool = False) -> dict:
    """Get or generate the Insight of the Day. Cached per day."""
    today = date.today().isoformat()

    # Return cached if same day and not forcing refresh
    if (not force_refresh
            and st.session_state.get('insight_of_the_day')
            and st.session_state.get('last_insight_date') == today):
        return st.session_state.insight_of_the_day

    # Generate new insight
    insight = generate_insight(kpis, anomalies)
    st.session_state.insight_of_the_day = insight
    st.session_state.last_insight_date = today
    return insight


def get_action_of_the_day(kpis: dict, anomalies: list, forecast_df=None) -> dict:
    """Get the daily recommended action."""
    category = st.session_state.get('business_category', 'Retail Store')
    return generate_action(kpis, anomalies, forecast_df, category)

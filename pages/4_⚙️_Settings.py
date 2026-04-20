"""
PulseBoard — Page 4: Settings
Business profile, notifications, API keys, data management.
"""
import streamlit as st
from core.config import Config
from core.session import init_session_state, clear_data, has_data
from core.auth import sign_out
from core.database import Database
from ui.styles import inject_custom_css
from ui.components import section_header, info_card

st.set_page_config(page_title="PulseBoard — Settings", page_icon="⚙️", layout="wide")
inject_custom_css()
init_session_state()

st.markdown("""
<div style="margin-bottom:1.5rem;">
    <h1 style="background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;font-weight:800;font-size:2rem;margin-bottom:0.25rem;">
    ⚙️ Settings</h1>
    <p style="color:#94a3b8;font-size:0.95rem;">Manage your business profile, integrations, and preferences</p>
</div>
""", unsafe_allow_html=True)

db = Database()

# ─── Business Profile ────────────────────────────────────────────────────────
section_header("Business Profile", "🏪")

col1, col2 = st.columns(2)
with col1:
    business_name = st.text_input(
        "Business Name",
        value=st.session_state.get('business_name', 'My Business'),
        key="settings_biz_name",
        placeholder="e.g., Joe's Coffee Shop"
    )

with col2:
    categories = Config.BUSINESS_CATEGORIES
    current_cat = st.session_state.get('business_category', 'Retail Store')
    cat_idx = categories.index(current_cat) if current_cat in categories else 0
    business_category = st.selectbox(
        "Business Category",
        categories,
        index=cat_idx,
        key="settings_biz_cat"
    )

if st.button("💾 Save Profile", key="btn_save_profile"):
    st.session_state.business_name = business_name
    st.session_state.business_category = business_category
    db.save_user_profile(st.session_state.get('user_id', 'demo'), {
        'business_name': business_name,
        'business_category': business_category,
    })
    st.success("✅ Profile saved!")

# ─── Notification Preferences ────────────────────────────────────────────────
st.divider()
section_header("Notifications", "🔔")

col1, col2 = st.columns(2)
with col1:
    email_notif = st.toggle(
        "Email Alerts",
        value=st.session_state.get('notification_email', True),
        key="settings_email_notif",
        help="Receive email alerts for anomalies and weekly summaries"
    )

with col2:
    frequency = st.selectbox(
        "Alert Frequency",
        ["Daily", "Weekly", "Monthly"],
        index=["Daily", "Weekly", "Monthly"].index(
            st.session_state.get('notification_frequency', 'Weekly')
        ),
        key="settings_freq"
    )

if st.button("💾 Save Notification Preferences", key="btn_save_notif"):
    st.session_state.notification_email = email_notif
    st.session_state.notification_frequency = frequency
    db.save_settings(st.session_state.get('user_id', 'demo'), {
        'email_alerts': email_notif,
        'alert_frequency': frequency,
    })
    st.success("✅ Notification preferences saved!")

# ─── API Key Management ──────────────────────────────────────────────────────
st.divider()
section_header("API Integrations", "🔑")

# Gemini
api_key = st.text_input(
    "Gemini API Key",
    value=st.session_state.get('gemini_api_key_input', ''),
    type="password",
    key="settings_gemini_key",
    placeholder="AIzaSy...",
    help="Required for AI-powered plain-English summaries. Get one at aistudio.google.com"
)

if st.button("💾 Save API Key", key="btn_save_api"):
    Config.update_gemini_key(api_key)
    st.session_state.gemini_api_key_input = api_key
    st.success("✅ API key saved!" if api_key else "⚠️ API key cleared. Using template-based summaries.")

# Status indicators
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:
    gemini_status = "🟢 Connected" if Config.GEMINI_ENABLED else "🔴 Not configured"
    st.markdown(f"""
    <div class="pulse-card">
        <strong style="color:#e2e8f0;">Gemini 1.5 Flash</strong>
        <p style="color:#94a3b8;margin:0.3rem 0 0;font-size:0.9rem;">{gemini_status}</p>
    </div>
    """, unsafe_allow_html=True)

with status_col2:
    firebase_status = "🟢 Connected" if Config.FIREBASE_ENABLED else "🟡 Demo Mode"
    st.markdown(f"""
    <div class="pulse-card">
        <strong style="color:#e2e8f0;">Firebase</strong>
        <p style="color:#94a3b8;margin:0.3rem 0 0;font-size:0.9rem;">{firebase_status}</p>
    </div>
    """, unsafe_allow_html=True)

with status_col3:
    data_status = "🟢 Data loaded" if has_data() else "🔴 No data"
    st.markdown(f"""
    <div class="pulse-card">
        <strong style="color:#e2e8f0;">Data Status</strong>
        <p style="color:#94a3b8;margin:0.3rem 0 0;font-size:0.9rem;">{data_status}</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Data Management ─────────────────────────────────────────────────────────
st.divider()
section_header("Data Management", "🗂️")

col1, col2 = st.columns(2)
with col1:
    if has_data():
        n_rows = len(st.session_state.raw_data)
        info_card("📊 Current Dataset", f"{n_rows} rows loaded • Date: {st.session_state.date_column} • Revenue: {st.session_state.revenue_column}")

        if st.button("🗑️ Clear All Data", key="btn_clear_data", type="secondary"):
            clear_data()
            st.success("✅ All data cleared.")
            st.rerun()
    else:
        info_card("📊 No Data", "Upload data from the Data Upload page to get started.")

with col2:
    if st.session_state.get('forecast_results'):
        forecast_df = st.session_state.forecast_results['forecast_df']
        csv = forecast_df.to_csv(index=False)
        st.download_button(
            "📥 Export Forecast CSV",
            csv,
            "pulseboard_forecast.csv",
            "text/csv",
            use_container_width=True,
        )
    else:
        st.markdown("""
        <div class="pulse-card" style="text-align:center;">
            <p style="color:#94a3b8;">Generate a forecast first to export.</p>
        </div>
        """, unsafe_allow_html=True)

# ─── Account ─────────────────────────────────────────────────────────────────
st.divider()
section_header("Account", "👤")

st.markdown(f"""
<div class="pulse-card">
    <strong style="color:#e2e8f0;">Signed in as</strong>
    <p style="color:#94a3b8;margin:0.3rem 0 0;font-size:0.95rem;">{st.session_state.get('user_email', 'demo@pulseboard.app')}</p>
    <p style="color:#64748b;margin:0.3rem 0 0;font-size:0.8rem;">Mode: {'Demo' if Config.DEMO_MODE else 'Production'}</p>
</div>
""", unsafe_allow_html=True)

if st.button("🚪 Sign Out", key="btn_signout", type="secondary"):
    sign_out()
    clear_data()
    st.success("Signed out successfully.")
    st.rerun()

# ─── App Info ─────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"""
<div style="text-align:center;padding:1rem 0;color:#64748b;font-size:0.8rem;">
    PulseBoard v{Config.APP_VERSION} •
    Predictive Business Intelligence for SMBs<br>
    Built with Streamlit • Prophet • Gemini AI • Firebase
</div>
""", unsafe_allow_html=True)

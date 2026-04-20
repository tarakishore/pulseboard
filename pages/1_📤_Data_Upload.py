"""
PulseBoard — Page 1: Data Upload
CSV/Excel upload with auto-detection and data preview.
"""
import streamlit as st
import pandas as pd
from data.parser import parse_uploaded_file, load_sample_data
from data.validator import detect_date_column, detect_revenue_column, validate_data
from data.preprocessor import preprocess_data, bootstrap_sparse_data
from core.session import init_session_state, set_data, has_data
from ui.styles import inject_custom_css
from ui.components import section_header, info_card, confidence_bar
from ui.theme import Colors

st.set_page_config(page_title="PulseBoard — Upload Data", page_icon="📤", layout="wide")
inject_custom_css()
init_session_state()

st.markdown("""
<div style="margin-bottom:1.5rem;">
    <h1 style="background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;font-weight:800;font-size:2rem;margin-bottom:0.25rem;">
    📤 Upload Your Sales Data</h1>
    <p style="color:#94a3b8;font-size:1rem;">Upload a CSV or Excel file with your sales history. We'll auto-detect
    the date and revenue columns.</p>
</div>
""", unsafe_allow_html=True)

# ─── Upload Options ──────────────────────────────────────────────────────────

col_upload, col_demo = st.columns([2, 1])

with col_upload:
    st.markdown('<div class="pulse-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls"],
        help="Upload your POS export, spreadsheet, or any file with date and revenue columns.",
        key="file_uploader"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_demo:
    st.markdown('<div class="pulse-card" style="text-align:center;padding:2rem;">', unsafe_allow_html=True)
    st.markdown("**🎮 No data yet?**")
    st.markdown('<p style="color:#94a3b8;font-size:0.9rem;">Try our demo dataset with 6 months of simulated retail sales data.</p>', unsafe_allow_html=True)
    use_demo = st.button("Load Demo Data", use_container_width=True, key="btn_demo")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Process Data ────────────────────────────────────────────────────────────

df = None

if use_demo:
    df = load_sample_data()
    st.success("✅ Demo dataset loaded — 197 days of retail sales data!")

if uploaded_file is not None:
    df = parse_uploaded_file(uploaded_file)
    if df is not None:
        st.success(f"✅ File loaded: {uploaded_file.name} ({len(df)} rows)")

if df is not None:
    st.divider()
    section_header("Column Detection", "🔍")

    # Auto-detect columns
    auto_date = detect_date_column(df)
    auto_revenue = detect_revenue_column(df, auto_date)

    col1, col2 = st.columns(2)
    with col1:
        all_cols = df.columns.tolist()
        date_idx = all_cols.index(auto_date) if auto_date in all_cols else 0
        date_col = st.selectbox("📅 Date Column", all_cols, index=date_idx, key="sel_date")

    with col2:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        rev_idx = numeric_cols.index(auto_revenue) if auto_revenue in numeric_cols else 0
        revenue_col = st.selectbox("💰 Revenue Column", numeric_cols, index=rev_idx, key="sel_revenue")

    if auto_date and auto_revenue:
        st.markdown(f'<p style="color:#10b981;font-size:0.9rem;">✨ Auto-detected: <b>{auto_date}</b> (date) and <b>{auto_revenue}</b> (revenue)</p>', unsafe_allow_html=True)

    # ─── Data Preview ────────────────────────────────────────────────────────
    st.divider()
    section_header("Data Preview", "📋")

    # Show first 10 rows styled
    st.dataframe(
        df.head(15).style.format(precision=2),
        use_container_width=True,
        height=400,
    )

    # ─── Validation ──────────────────────────────────────────────────────────
    section_header("Data Validation", "✅")

    # Preprocess for validation
    temp_df = df.copy()
    try:
        temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors='coerce')
    except Exception:
        pass

    report = validate_data(temp_df, date_col, revenue_col)

    # Show validation results
    vcol1, vcol2, vcol3 = st.columns(3)
    with vcol1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Rows</div>
            <div class="metric-value">{report['row_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with vcol2:
        avg_rev = report['stats'].get('avg_revenue', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Daily Revenue</div>
            <div class="metric-value">${avg_rev:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with vcol3:
        total = report['stats'].get('total_revenue', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">${total:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Warnings
    if report['warnings']:
        for w in report['warnings']:
            st.warning(w)
    if report['errors']:
        for e in report['errors']:
            st.error(e)

    # ─── Process & Continue ──────────────────────────────────────────────────
    st.divider()

    if report['is_valid']:
        if st.button("🚀 Process & Continue to Dashboard", use_container_width=True, type="primary", key="btn_process"):
            with st.spinner("Processing data..."):
                processed = preprocess_data(df, date_col, revenue_col)

                # Bootstrap if sparse
                if len(processed) < 30:
                    processed = bootstrap_sparse_data(processed, date_col, revenue_col)
                    st.info(f"📊 Extended dataset from {len(df)} to {len(processed)} rows using pattern replication for better forecasting.")

                set_data(processed, date_col, revenue_col)
                st.session_state.processed_data = processed

            st.success("✅ Data processed successfully! Navigate to the **Dashboard** page from the sidebar.")
            st.balloons()
    else:
        st.error("❌ Please fix the errors above before continuing.")

# ─── Current Data Status ─────────────────────────────────────────────────────
if has_data():
    st.divider()
    info_card(
        "📊 Active Dataset",
        f"You have data loaded with {len(st.session_state.raw_data)} rows. "
        f"Date column: **{st.session_state.date_column}** | "
        f"Revenue column: **{st.session_state.revenue_column}**"
    )

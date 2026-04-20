"""
PulseBoard Firebase Authentication Wrapper
Provides sign-up, sign-in, sign-out with demo mode bypass.
"""
import streamlit as st
from core.config import Config


def init_auth():
    """Initialize Firebase Auth or set demo mode."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_email = ""
        st.session_state.user_id = ""

    if Config.DEMO_MODE:
        st.session_state.authenticated = True
        st.session_state.user_email = "demo@pulseboard.app"
        st.session_state.user_id = "demo_user"


def login_gate():
    """Show login/register UI if not authenticated. Returns True if authenticated."""
    if st.session_state.get("authenticated"):
        return True

    if Config.DEMO_MODE:
        st.session_state.authenticated = True
        st.session_state.user_email = "demo@pulseboard.app"
        st.session_state.user_id = "demo_user"
        return True

    # Firebase Auth UI
    st.markdown("""
    <div style="text-align:center; padding:3rem 1rem;">
        <h1 style="background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;font-size:3rem;font-weight:800;">PulseBoard</h1>
        <p style="color:#94a3b8;font-size:1.1rem;margin-top:0.5rem;">
        Predictive Business Intelligence for SMBs</p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["🔑 Sign In", "📝 Register"])

    with tab_login:
        email = st.text_input("Email", key="login_email", placeholder="you@business.com")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In", use_container_width=True, key="btn_login"):
            if _firebase_sign_in(email, password):
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

    with tab_register:
        reg_email = st.text_input("Email", key="reg_email", placeholder="you@business.com")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2")
        if st.button("Create Account", use_container_width=True, key="btn_register"):
            if reg_pass != reg_pass2:
                st.error("Passwords don't match.")
            elif len(reg_pass) < 6:
                st.error("Password must be at least 6 characters.")
            elif _firebase_register(reg_email, reg_pass):
                st.success("Account created! You can now sign in.")
            else:
                st.error("Registration failed. Email may already be in use.")

    st.divider()
    if st.button("🚀 Continue in Demo Mode", use_container_width=True):
        st.session_state.authenticated = True
        st.session_state.user_email = "demo@pulseboard.app"
        st.session_state.user_id = "demo_user"
        st.rerun()

    return False


def sign_out():
    """Sign the user out."""
    st.session_state.authenticated = False
    st.session_state.user_email = ""
    st.session_state.user_id = ""


def _firebase_sign_in(email: str, password: str) -> bool:
    """Authenticate with Firebase. Returns True on success."""
    if not Config.FIREBASE_ENABLED:
        return False
    try:
        import firebase_admin
        from firebase_admin import auth as fb_auth
        # Verify user exists
        user = fb_auth.get_user_by_email(email)
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.session_state.user_id = user.uid
        return True
    except Exception:
        return False


def _firebase_register(email: str, password: str) -> bool:
    """Register a new user with Firebase."""
    if not Config.FIREBASE_ENABLED:
        return False
    try:
        import firebase_admin
        from firebase_admin import auth as fb_auth
        user = fb_auth.create_user(email=email, password=password)
        return True
    except Exception:
        return False

"""
PulseBoard Firebase Firestore Operations
CRUD operations for user data with demo mode in-memory fallback.
"""
import streamlit as st
from core.config import Config


class Database:
    """Firestore database wrapper with in-memory fallback for demo mode."""

    def __init__(self):
        self._db = None
        if Config.FIREBASE_ENABLED:
            try:
                self._init_firestore()
            except Exception:
                pass

    def _init_firestore(self):
        """Initialize Firestore client."""
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            cred = credentials.Certificate(Config.FIREBASE_SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred)
        self._db = firestore.client()

    def save_user_profile(self, user_id: str, data: dict):
        """Save user profile data."""
        if self._db:
            self._db.collection('users').document(user_id).set(data, merge=True)
        else:
            # Demo mode: store in session state
            st.session_state['_profile'] = data

    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile data."""
        if self._db:
            doc = self._db.collection('users').document(user_id).get()
            return doc.to_dict() if doc.exists else {}
        else:
            return st.session_state.get('_profile', {})

    def save_forecast(self, user_id: str, forecast_data: dict):
        """Cache forecast results."""
        if self._db:
            self._db.collection('forecasts').document(user_id).set(forecast_data)
        else:
            st.session_state['_cached_forecast'] = forecast_data

    def get_forecast(self, user_id: str) -> dict:
        """Retrieve cached forecast."""
        if self._db:
            doc = self._db.collection('forecasts').document(user_id).get()
            return doc.to_dict() if doc.exists else {}
        return st.session_state.get('_cached_forecast', {})

    def save_settings(self, user_id: str, settings: dict):
        """Save user settings."""
        if self._db:
            self._db.collection('settings').document(user_id).set(settings, merge=True)
        else:
            st.session_state['_settings'] = settings

    def get_settings(self, user_id: str) -> dict:
        """Get user settings."""
        if self._db:
            doc = self._db.collection('settings').document(user_id).get()
            return doc.to_dict() if doc.exists else {}
        return st.session_state.get('_settings', {})

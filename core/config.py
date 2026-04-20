"""
PulseBoard Configuration Module
Handles environment variables, feature flags, and app settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    # --- App Settings ---
    APP_NAME = "PulseBoard"
    APP_VERSION = "1.0.0"
    APP_TAGLINE = "Predictive Business Intelligence for SMBs"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # --- Demo Mode ---
    # When True, Firebase auth/db is bypassed, and mock data is used as needed.
    DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

    # --- Gemini ---
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
    GEMINI_ENABLED = bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")

    # --- Firebase ---
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")
    FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN", "")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")
    FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "firebase/service_account.json")
    FIREBASE_ENABLED = bool(FIREBASE_PROJECT_ID and FIREBASE_API_KEY)

    # --- Forecasting ---
    FORECAST_HORIZON_DAYS = int(os.getenv("FORECAST_HORIZON_DAYS", "28"))  # 4 weeks
    MIN_DATA_POINTS = int(os.getenv("MIN_DATA_POINTS", "14"))  # Minimum rows for forecasting
    BOOTSTRAP_TARGET = int(os.getenv("BOOTSTRAP_TARGET", "60"))  # Synthetic data target rows

    # --- Business Categories ---
    BUSINESS_CATEGORIES = [
        "Retail Store",
        "Food & Beverage",
        "Salon & Spa",
        "E-commerce",
        "Professional Services",
        "Healthcare",
        "Fitness & Wellness",
        "Other",
    ]

    @classmethod
    def update_gemini_key(cls, key: str):
        """Update the Gemini API key at runtime (from Settings page)."""
        cls.GEMINI_API_KEY = key
        cls.GEMINI_ENABLED = bool(key and key != "your_gemini_api_key_here")
        os.environ["GEMINI_API_KEY"] = key

    @classmethod
    def get_status(cls) -> dict:
        """Return a status summary of all integrations."""
        return {
            "demo_mode": cls.DEMO_MODE,
            "gemini_enabled": cls.GEMINI_ENABLED,
            "firebase_enabled": cls.FIREBASE_ENABLED,
            "forecast_horizon": cls.FORECAST_HORIZON_DAYS,
            "min_data_points": cls.MIN_DATA_POINTS,
        }

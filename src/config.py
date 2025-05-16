"""
Configuration file for LinkX AI Agent
------------------------------------
Manages environment variables and application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and credentials
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "t", "1")
PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "127.0.0.1")

# Model settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-pro")
ADK_MODEL = os.getenv("ADK_MODEL", "gemini-1.5-pro-latest")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", 1024))

# Feature flags
ENABLE_TWITTER = os.getenv("ENABLE_TWITTER", "True").lower() in ("true", "t", "1")
ENABLE_LINKEDIN = os.getenv("ENABLE_LINKEDIN", "True").lower() in ("true", "t", "1")
ENABLE_ADK = os.getenv("ENABLE_ADK", "True").lower() in ("true", "t", "1")

def validate_config():
    """Validate the configuration and return a list of any issues."""
    issues = []
    
    if not GOOGLE_API_KEY:
        issues.append("GOOGLE_API_KEY is not set. This is required for the AI functionality.")
    
    if ENABLE_TWITTER:
        if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
            issues.append("Twitter API credentials are incomplete. Publishing to Twitter will be disabled.")
    
    if ENABLE_LINKEDIN:
        if not all([LINKEDIN_EMAIL, LINKEDIN_PASSWORD]):
            issues.append("LinkedIn credentials are incomplete. Publishing to LinkedIn will be disabled.")
    
    return issues

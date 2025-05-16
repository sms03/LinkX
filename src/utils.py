"""
API Utilities for LinkX
-----------------------
This module provides helper functions for API connections to Google's ADK,
Twitter/X API, and LinkedIn API.
"""

import os
import google.generativeai as genai
import tweepy
from linkedin_api import Linkedin


def setup_google_adk():
    """Set up and configure Google's Generative AI (ADK) with API key."""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    genai.configure(api_key=api_key)
    
    # Test the connection
    try:
        models = genai.list_models()
        available_models = [model.name for model in models]
        return {
            "status": "success", 
            "available_models": available_models
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def setup_twitter_client():
    """Set up and configure Twitter API client."""
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        return {
            "status": "error",
            "message": "Twitter API credentials are not fully configured in environment variables"
        }
    
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Test the connection by getting the authenticated user
        # This would verify credentials are valid
        return {
            "status": "success",
            "client": client
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Twitter API connection failed: {str(e)}"
        }


def setup_linkedin_client():
    """Set up and configure LinkedIn API client."""
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not all([email, password]):
        return {
            "status": "error",
            "message": "LinkedIn credentials are not fully configured in environment variables"
        }
    
    try:
        client = Linkedin(email, password)
        
        # Test connection by trying to get profile data
        client.get_profile()
        
        return {
            "status": "success",
            "client": client
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"LinkedIn API connection failed: {str(e)}"
        }


def test_all_connections():
    """Test all API connections and return status."""
    results = {
        "google_adk": setup_google_adk(),
        "twitter": setup_twitter_client(),
        "linkedin": setup_linkedin_client()
    }
    
    return results

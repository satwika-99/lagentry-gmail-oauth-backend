"""
OAuth authentication module for Gmail OAuth Backend
Handles Google OAuth 2.0 flow and token management
"""

import httpx
import secrets
from urllib.parse import urlencode
from typing import Optional, Dict, Any

from config import config
from storage import store_tokens, get_valid_tokens

def refresh_access_token(refresh_token: str) -> Optional[Dict[str, Any]]:
    """Refresh access token using refresh token"""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "client_secret": config.GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            return {
                "access_token": token_data["access_token"],
                "expires_in": token_data.get("expires_in", 3600)
            }
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return None

def generate_auth_url() -> str:
    """Generate Google OAuth authorization URL"""
    if not config.GOOGLE_CLIENT_ID:
        raise ValueError("Google Client ID not configured")
    
    # Generate state parameter for security
    state = secrets.token_urlsafe(32)
    
    # Build authorization URL
    auth_params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "scope": " ".join(config.SCOPES),
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"

async def handle_oauth_callback(code: str, state: str) -> Dict[str, Any]:
    """Handle OAuth callback from Google"""
    try:
        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": config.GOOGLE_CLIENT_ID,
            "client_secret": config.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": config.REDIRECT_URI
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=token_data)
            response.raise_for_status()
            tokens = response.json()
        
        # Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        
        async with httpx.AsyncClient() as client:
            user_response = await client.get(user_info_url, headers=headers)
            user_response.raise_for_status()
            user_info = user_response.json()
        
        # Store tokens
        store_tokens(
            user_info["email"],
            tokens["access_token"],
            tokens["refresh_token"],
            tokens["expires_in"]
        )
        
        return {
            "message": "OAuth successful",
            "user_email": user_info["email"],
            "access_token": tokens["access_token"][:20] + "...",  # Show partial token for security
            "expires_in": tokens["expires_in"]
        }
        
    except Exception as e:
        raise Exception(f"OAuth error: {str(e)}")

def get_access_token_for_user(user_email: str) -> Optional[str]:
    """Get valid access token for a user, refreshing if necessary"""
    tokens = get_valid_tokens(user_email)
    if not tokens:
        return None
    
    # Check if token needs refresh
    from datetime import datetime
    if datetime.now() >= tokens["expires_at"]:
        refreshed = refresh_access_token(tokens["refresh_token"])
        if refreshed:
            store_tokens(user_email, refreshed["access_token"], tokens["refresh_token"], refreshed["expires_in"])
            return refreshed["access_token"]
        else:
            return None
    else:
        return tokens["access_token"]

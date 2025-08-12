"""
Google OAuth Provider Implementation
Handles authentication for all Google services (Gmail, Drive, Calendar, etc.)
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

from app.core.auth import OAuthProvider
from app.core.config import settings
from app.core.database import db_manager
from app.core.exceptions import OAuthError, TokenError


class GoogleOAuthProvider(OAuthProvider):
    """Google OAuth provider with support for multiple Google services"""
    
    def __init__(self):
        super().__init__("google")
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri
        self.scopes = settings.google_scopes
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        
        # Google service endpoints
        self.gmail_api_url = "https://gmail.googleapis.com/gmail/v1"
        self.drive_api_url = "https://www.googleapis.com/drive/v3"
        self.calendar_api_url = "https://www.googleapis.com/calendar/v3"
        self.photos_api_url = "https://photoslibrary.googleapis.com/v1"
        self.docs_api_url = "https://docs.googleapis.com/v1"
        self.youtube_api_url = "https://www.googleapis.com/youtube/v3"
    
    def get_auth_url(self, state: Optional[str] = None, scopes: Optional[List[str]] = None) -> str:
        """Generate Google OAuth authorization URL"""
        if not self.client_id:
            raise OAuthError("Google client ID not configured")
        
        # Use provided scopes or default scopes
        requested_scopes = scopes or self.scopes
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(requested_scopes),
            "access_type": "offline",
            "prompt": "consent"
        }
        
        if state:
            params["state"] = state
            
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    
    async def handle_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for tokens"""
        if not code:
            raise OAuthError("Authorization code is required")
        
        try:
            async with httpx.AsyncClient() as client:
                # Exchange code for tokens
                token_data = {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri
                }
                
                response = await client.post(self.token_url, data=token_data)
                response.raise_for_status()
                token_info = response.json()
                
                # Get user info
                headers = {"Authorization": f"Bearer {token_info['access_token']}"}
                user_response = await client.get(self.userinfo_url, headers=headers)
                user_response.raise_for_status()
                user_info = user_response.json()
                
                # Store tokens
                expires_at = datetime.now() + timedelta(seconds=token_info.get("expires_in", 3600))
                db_manager.store_tokens(
                    user_email=user_info["email"],
                    provider="google",
                    access_token=token_info["access_token"],
                    refresh_token=token_info.get("refresh_token"),
                    expires_at=expires_at,
                    scopes=" ".join(self.scopes)
                )
                
                return {
                    "success": True,
                    "user_email": user_info["email"],
                    "user_name": user_info.get("name"),
                    "picture": user_info.get("picture"),
                    "access_token": token_info["access_token"],
                    "expires_at": expires_at.isoformat(),
                    "scopes": self.scopes
                }
                
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"Token exchange failed: {e.response.text}")
        except Exception as e:
            raise OAuthError(f"OAuth callback failed: {str(e)}")
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh access token using refresh token"""
        try:
            async with httpx.AsyncClient() as client:
                token_data = {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
                
                response = await client.post(self.token_url, data=token_data)
                response.raise_for_status()
                token_info = response.json()
                
                return {
                    "access_token": token_info["access_token"],
                    "expires_in": token_info.get("expires_in", 3600),
                    "token_type": token_info.get("token_type", "Bearer")
                }
                
        except httpx.HTTPStatusError as e:
            raise TokenError(f"Token refresh failed: {e.response.text}")
        except Exception as e:
            raise TokenError(f"Token refresh error: {str(e)}")
    
    async def revoke_tokens(self, user_email: str) -> bool:
        """Revoke access tokens for a user"""
        try:
            tokens = db_manager.get_valid_tokens(user_email, "google")
            if not tokens:
                return True
            
            async with httpx.AsyncClient() as client:
                # Revoke access token
                if tokens.get("access_token"):
                    revoke_url = "https://oauth2.googleapis.com/revoke"
                    await client.post(revoke_url, data={"token": tokens["access_token"]})
                
                # Delete from database
                db_manager.delete_user_tokens(user_email, "google")
                return True
                
        except Exception as e:
            raise OAuthError(f"Token revocation failed: {str(e)}")
    
    async def validate_tokens(self, user_email: str) -> Dict[str, Any]:
        """Validate if tokens are still valid"""
        try:
            tokens = db_manager.get_valid_tokens(user_email, "google")
            if not tokens:
                return {"valid": False, "reason": "No tokens found"}
            
            # Test token with a simple API call
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(self.userinfo_url, headers=headers)
                
                if response.status_code == 200:
                    return {
                        "valid": True,
                        "user_info": response.json(),
                        "expires_at": tokens.get("expires_at")
                    }
                else:
                    return {"valid": False, "reason": "Token expired or invalid"}
                    
        except Exception as e:
            return {"valid": False, "reason": f"Validation error: {str(e)}"}
    
    def get_available_scopes(self) -> Dict[str, List[str]]:
        """Get available Google API scopes"""
        return {
            "gmail": [
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.modify",
                "https://www.googleapis.com/auth/gmail.compose",
                "https://www.googleapis.com/auth/gmail.send"
            ],
            "drive": [
                "https://www.googleapis.com/auth/drive.readonly",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"
            ],
            "calendar": [
                "https://www.googleapis.com/auth/calendar.readonly",
                "https://www.googleapis.com/auth/calendar.events",
                "https://www.googleapis.com/auth/calendar"
            ],
            "photos": [
                "https://www.googleapis.com/auth/photoslibrary.readonly",
                "https://www.googleapis.com/auth/photoslibrary"
            ],
            "docs": [
                "https://www.googleapis.com/auth/documents.readonly",
                "https://www.googleapis.com/auth/documents"
            ],
            "youtube": [
                "https://www.googleapis.com/auth/youtube.readonly",
                "https://www.googleapis.com/auth/youtube"
            ],
            "userinfo": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
            ]
        }


# Provider instance
google_provider = GoogleOAuthProvider() 
"""
Base OAuth classes for provider implementations
"""

import secrets
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from urllib.parse import urlencode
from datetime import datetime, timedelta

from .config import settings
from .database import db_manager


class OAuthProvider(ABC):
    """Base class for OAuth providers"""
    
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
    
    @abstractmethod
    def get_auth_url(self, state: Optional[str] = None) -> str:
        """Generate OAuth authorization URL"""
        pass
    
    @abstractmethod
    async def handle_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle OAuth callback and token exchange"""
        pass
    
    @abstractmethod
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh expired access token"""
        pass
    
    def generate_state(self) -> str:
        """Generate a random state parameter for CSRF protection"""
        return secrets.token_urlsafe(32)
    
    def validate_state(self, received_state: str, original_state: str) -> bool:
        """Validate state parameter"""
        return received_state == original_state
    
    def store_tokens(self, user_email: str, access_token: str, refresh_token: str, 
                    expires_in: int, scopes: Optional[List[str]] = None) -> bool:
        """Store tokens in database"""
        return db_manager.store_tokens(
            user_email, self.provider_name, access_token, 
            refresh_token, expires_in, scopes
        )
    
    def get_valid_tokens(self, user_email: str) -> Optional[Dict[str, Any]]:
        """Get valid tokens for user"""
        return db_manager.get_valid_tokens(user_email, self.provider_name)
    
    def log_activity(self, user_email: str, action: str, details: Optional[Dict] = None) -> bool:
        """Log user activity"""
        return db_manager.log_activity(user_email, self.provider_name, action, details)


class GoogleOAuthProvider(OAuthProvider):
    """Google OAuth implementation"""
    
    def __init__(self):
        super().__init__("google")
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri
        self.scopes = settings.google_scopes
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def get_auth_url(self, state: Optional[str] = None) -> str:
        """Generate Google OAuth authorization URL"""
        if not self.client_id:
            raise ValueError("Google OAuth not configured")
        
        state = state or self.generate_state()
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "response_type": "code",
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }
        
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    async def handle_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle Google OAuth callback"""
        try:
            # Exchange code for tokens
            token_data = await self._exchange_code_for_tokens(code)
            
            # Get user info
            user_info = await self._get_user_info(token_data["access_token"])
            
            # Store tokens
            self.store_tokens(
                user_info["email"],
                token_data["access_token"],
                token_data["refresh_token"],
                token_data["expires_in"],
                self.scopes
            )
            
            # Log activity
            self.log_activity(user_info["email"], "oauth_success", {
                "provider": "google",
                "scopes": self.scopes
            })
            
            return {
                "message": "OAuth successful",
                "user_email": user_info["email"],
                "access_token": token_data["access_token"][:20] + "...",  # Partial for security
                "expires_in": token_data["expires_in"]
            }
            
        except Exception as e:
            print(f"❌ Google OAuth callback failed: {e}")
            raise
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh Google access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.token_url, data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                })
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"❌ Token refresh failed: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Token refresh error: {e}")
            return None
    
    async def _exchange_code_for_tokens(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for tokens"""
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri
            })
            
            if response.status_code != 200:
                raise Exception(f"Token exchange failed: {response.text}")
            
            return response.json()
    
    async def _get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(self.userinfo_url, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Failed to get user info: {response.text}")
            
            return response.json()


# Provider registry
PROVIDERS = {
    "google": GoogleOAuthProvider()
}


def get_provider(provider_name: str) -> OAuthProvider:
    """Get OAuth provider by name"""
    if provider_name not in PROVIDERS:
        raise ValueError(f"Provider '{provider_name}' not supported")
    return PROVIDERS[provider_name]


def validate_google_config() -> bool:
    """Validate that Google OAuth configuration is complete"""
    if not settings.google_client_id:
        raise ValueError("GOOGLE_CLIENT_ID is required")
    if not settings.google_client_secret:
        raise ValueError("GOOGLE_CLIENT_SECRET is required")
    return True 
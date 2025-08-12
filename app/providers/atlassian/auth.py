"""
Atlassian OAuth Provider Implementation
Handles authentication for Jira, Confluence, and other Atlassian services
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

from app.core.auth import OAuthProvider
from app.core.config import settings
from app.core.database import db_manager
from app.core.exceptions import OAuthError, TokenError


class AtlassianOAuthProvider(OAuthProvider):
    """Atlassian OAuth provider for Jira, Confluence, and other services"""
    
    def __init__(self):
        super().__init__("atlassian")
        self.client_id = settings.atlassian_client_id
        self.client_secret = settings.atlassian_client_secret
        self.redirect_uri = settings.atlassian_redirect_uri
        self.scopes = settings.atlassian_scopes
        self.token_url = "https://auth.atlassian.com/oauth/token"
        self.userinfo_url = "https://api.atlassian.com/me"
        
        # Atlassian API endpoints
        self.api_base_url = "https://api.atlassian.com"
        self.jira_api_url = "https://api.atlassian.com/ex/jira"
        self.confluence_api_url = "https://api.atlassian.com/ex/confluence"
        self.bitbucket_api_url = "https://api.atlassian.com/ex/bitbucket"
    
    def get_auth_url(self, state: Optional[str] = None, scopes: Optional[List[str]] = None) -> str:
        """Generate Atlassian OAuth authorization URL"""
        if not self.client_id:
            raise OAuthError("Atlassian client ID not configured")
        
        # Use provided scopes or default scopes
        requested_scopes = scopes or self.scopes
        
        params = {
            "audience": "api.atlassian.com",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(requested_scopes),
            "response_type": "code",
            "prompt": "consent",
            "state": state or ""
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://auth.atlassian.com/authorize?{query_string}"
    
    async def handle_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for tokens"""
        if not code:
            raise OAuthError("Authorization code is required")
        
        try:
            async with httpx.AsyncClient() as client:
                # Exchange code for tokens
                token_data = {
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri
                }
                
                response = await client.post(self.token_url, data=token_data)
                response.raise_for_status()
                token_info = response.json()
                
                if "error" in token_info:
                    raise OAuthError(f"Atlassian OAuth error: {token_info.get('error_description', 'Unknown error')}")
                
                # Get user info
                headers = {"Authorization": f"Bearer {token_info['access_token']}"}
                user_response = await client.get(self.userinfo_url, headers=headers)
                user_response.raise_for_status()
                user_info = user_response.json()
                
                # Store tokens
                expires_at = datetime.now() + timedelta(seconds=token_info.get("expires_in", 3600))
                db_manager.store_tokens(
                    user_email=user_info.get("email"),
                    provider="atlassian",
                    access_token=token_info["access_token"],
                    refresh_token=token_info.get("refresh_token"),
                    expires_at=expires_at,
                    scopes=" ".join(self.scopes)
                )
                
                return {
                    "success": True,
                    "user_id": user_info.get("account_id"),
                    "user_name": user_info.get("name"),
                    "user_email": user_info.get("email"),
                    "access_token": token_info["access_token"],
                    "refresh_token": token_info.get("refresh_token"),
                    "expires_at": expires_at.isoformat(),
                    "scopes": self.scopes
                }
                
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"Token exchange failed: {e.response.text}")
        except Exception as e:
            raise OAuthError(f"OAuth callback failed: {str(e)}")
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh Atlassian access token"""
        if not refresh_token:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                token_data = {
                    "grant_type": "refresh_token",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token
                }
                
                response = await client.post(self.token_url, data=token_data)
                response.raise_for_status()
                token_info = response.json()
                
                if "error" in token_info:
                    return None
                
                return {
                    "access_token": token_info["access_token"],
                    "refresh_token": token_info.get("refresh_token"),
                    "expires_in": token_info.get("expires_in", 3600)
                }
                
        except Exception as e:
            raise TokenError(f"Token refresh failed: {str(e)}")
    
    async def revoke_tokens(self, user_email: str) -> bool:
        """Revoke Atlassian tokens"""
        try:
            tokens = db_manager.get_valid_tokens(user_email, "atlassian")
            if not tokens:
                return True
            
            async with httpx.AsyncClient() as client:
                # Atlassian doesn't have a standard token revocation endpoint
                # We'll just remove from our database
                db_manager.delete_user_tokens(user_email, "atlassian")
                return True
                
        except Exception as e:
            raise TokenError(f"Token revocation failed: {str(e)}")
    
    async def validate_tokens(self, user_email: str) -> Dict[str, Any]:
        """Validate Atlassian tokens and get user info"""
        try:
            tokens = db_manager.get_valid_tokens(user_email, "atlassian")
            if not tokens:
                return {"valid": False, "reason": "No tokens found"}
            
            # Check if token is expired
            if tokens.get("expires_at") and datetime.fromisoformat(tokens["expires_at"]) < datetime.now():
                # Try to refresh
                refresh_result = await self.refresh_access_token(tokens.get("refresh_token"))
                if refresh_result:
                    # Update stored tokens
                    db_manager.refresh_tokens(
                        user_email, "atlassian",
                        refresh_result["access_token"],
                        refresh_result.get("refresh_token", ""),
                        refresh_result["expires_in"]
                    )
                    tokens["access_token"] = refresh_result["access_token"]
                else:
                    return {"valid": False, "reason": "Token expired and refresh failed"}
            
            # Validate by making API call
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {tokens['access_token']}"}
                response = await client.get(self.userinfo_url, headers=headers)
                
                if response.status_code == 200:
                    user_info = response.json()
                    return {
                        "valid": True,
                        "user_info": user_info,
                        "scopes": tokens.get("scopes", "").split()
                    }
                else:
                    return {"valid": False, "reason": "API validation failed"}
                    
        except Exception as e:
            return {"valid": False, "reason": f"Validation error: {str(e)}"}
    
    def get_available_scopes(self) -> Dict[str, List[str]]:
        """Get available Atlassian OAuth scopes"""
        return {
            "jira": [
                "read:jira-work",
                "write:jira-work",
                "read:jira-user",
                "write:jira-user",
                "manage:jira-project",
                "manage:jira-configuration"
            ],
            "confluence": [
                "read:confluence-content.all",
                "write:confluence-content",
                "read:confluence-space.summary",
                "read:confluence-user",
                "read:confluence-content.summary",
                "read:confluence-props",
                "write:confluence-props"
            ],
            "bitbucket": [
                "read:repository",
                "write:repository",
                "read:project",
                "write:project"
            ],
            "user": [
                "read:me",
                "write:me"
            ]
        }


# Global instance
atlassian_oauth = AtlassianOAuthProvider() 
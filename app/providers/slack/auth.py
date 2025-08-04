"""
Slack OAuth Provider Implementation
Handles authentication for Slack workspace access
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

from ...core.auth import OAuthProvider
from ...core.config import settings
from ...core.database import db_manager
from ...core.exceptions import OAuthError, TokenError


class SlackOAuthProvider(OAuthProvider):
    """Slack OAuth provider for workspace access"""
    
    def __init__(self):
        super().__init__("slack")
        self.client_id = settings.slack_client_id
        self.client_secret = settings.slack_client_secret
        self.redirect_uri = settings.slack_redirect_uri
        self.scopes = settings.slack_scopes
        self.token_url = "https://slack.com/api/oauth.v2.access"
        self.userinfo_url = "https://slack.com/api/users.info"
        
        # Slack API endpoints
        self.api_base_url = "https://slack.com/api"
    
    def get_auth_url(self, state: Optional[str] = None, scopes: Optional[List[str]] = None) -> str:
        """Generate Slack OAuth authorization URL"""
        if not self.client_id:
            raise OAuthError("Slack client ID not configured")
        
        # Use provided scopes or default scopes
        requested_scopes = scopes or self.scopes
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": ",".join(requested_scopes),
            "state": state or ""
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://slack.com/oauth/v2/authorize?{query_string}"
    
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
                    "redirect_uri": self.redirect_uri
                }
                
                response = await client.post(self.token_url, data=token_data)
                response.raise_for_status()
                token_info = response.json()
                
                if not token_info.get("ok"):
                    raise OAuthError(f"Slack OAuth error: {token_info.get('error', 'Unknown error')}")
                
                # Get user info
                user_info = token_info.get("authed_user", {})
                team_info = token_info.get("team", {})
                
                # Store tokens
                expires_at = datetime.now() + timedelta(days=365)  # Slack tokens don't expire
                db_manager.store_tokens(
                    user_email=user_info.get("id"),  # Use Slack user ID as email
                    provider="slack",
                    access_token=token_info["access_token"],
                    refresh_token=None,  # Slack doesn't use refresh tokens
                    expires_at=expires_at,
                    scopes=",".join(self.scopes)
                )
                
                return {
                    "success": True,
                    "user_id": user_info.get("id"),
                    "user_name": user_info.get("name"),
                    "team_id": team_info.get("id"),
                    "team_name": team_info.get("name"),
                    "access_token": token_info["access_token"],
                    "expires_at": expires_at.isoformat(),
                    "scopes": self.scopes
                }
                
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"Token exchange failed: {e.response.text}")
        except Exception as e:
            raise OAuthError(f"OAuth callback failed: {str(e)}")
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh access token (not applicable for Slack)"""
        # Slack tokens don't expire, so refresh is not needed
        return None
    
    async def revoke_tokens(self, user_email: str) -> bool:
        """Revoke access tokens for a user"""
        try:
            tokens = db_manager.get_valid_tokens(user_email, "slack")
            if not tokens:
                return True
            
            # Delete from database
            db_manager.delete_user_tokens(user_email, "slack")
            return True
                
        except Exception as e:
            raise OAuthError(f"Token revocation failed: {str(e)}")
    
    async def validate_tokens(self, user_email: str) -> Dict[str, Any]:
        """Validate if tokens are still valid"""
        try:
            tokens = db_manager.get_valid_tokens(user_email, "slack")
            if not tokens:
                return {"valid": False, "reason": "No tokens found"}
            
            # Test token with a simple API call
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_base_url}/auth.test", headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        return {
                            "valid": True,
                            "user_info": result,
                            "expires_at": tokens.get("expires_at")
                        }
                    else:
                        return {"valid": False, "reason": "Token invalid"}
                else:
                    return {"valid": False, "reason": "Token expired or invalid"}
                    
        except Exception as e:
            return {"valid": False, "reason": f"Validation error: {str(e)}"}
    
    def get_available_scopes(self) -> Dict[str, List[str]]:
        """Get available Slack API scopes"""
        return {
            "channels": [
                "channels:read",
                "channels:history",
                "channels:write",
                "channels:join"
            ],
            "messages": [
                "chat:write",
                "chat:write.public",
                "chat:write.customize"
            ],
            "users": [
                "users:read",
                "users:read.email",
                "users.profile:read"
            ],
            "files": [
                "files:read",
                "files:write"
            ],
            "groups": [
                "groups:read",
                "groups:history",
                "groups:write"
            ],
            "im": [
                "im:read",
                "im:history",
                "im:write"
            ],
            "mpim": [
                "mpim:read",
                "mpim:history",
                "mpim:write"
            ],
            "admin": [
                "admin.users:read",
                "admin.users:write",
                "admin.channels:read",
                "admin.channels:write"
            ]
        }


# Provider instance
slack_provider = SlackOAuthProvider() 
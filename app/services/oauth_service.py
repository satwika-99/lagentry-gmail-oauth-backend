"""
Unified OAuth Service
Handles authentication for all providers using the modular structure
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from ..core.database import db_manager
from ..core.exceptions import OAuthError, TokenError
from ..providers.google.auth import google_provider
from ..providers.slack.auth import slack_provider
from ..providers.atlassian.auth import atlassian_oauth


class OAuthService:
    """Unified OAuth service for all providers"""
    
    def __init__(self):
        self.providers = {
            "google": google_provider,
            "slack": slack_provider,
            "atlassian": atlassian_oauth
        }
    
    def get_provider(self, provider_name: str):
        """Get OAuth provider by name"""
        if provider_name not in self.providers:
            raise OAuthError(f"Provider '{provider_name}' not supported")
        return self.providers[provider_name]
    
    def get_auth_url(self, provider: str, state: Optional[str] = None, scopes: Optional[List[str]] = None) -> str:
        """Get OAuth authorization URL for a provider"""
        try:
            provider_instance = self.get_provider(provider)
            return provider_instance.get_auth_url(state=state, scopes=scopes)
        except Exception as e:
            raise OAuthError(f"Failed to get auth URL for {provider}: {str(e)}")
    
    async def handle_callback(self, provider: str, code: str, state: str) -> Dict[str, Any]:
        """Handle OAuth callback for a provider"""
        try:
            provider_instance = self.get_provider(provider)
            result = await provider_instance.handle_callback(code, state)
            
            # Log successful authentication
            db_manager.log_activity(
                user_email=result.get("user_email") or result.get("user_id"),
                provider=provider,
                action="oauth_success",
                details={
                    "provider": provider,
                    "scopes": result.get("scopes", [])
                }
            )
            
            return result
        except Exception as e:
            raise OAuthError(f"OAuth callback failed for {provider}: {str(e)}")
    
    async def validate_tokens(self, provider: str, user_email: str) -> Dict[str, Any]:
        """Validate tokens for a provider"""
        try:
            provider_instance = self.get_provider(provider)
            return await provider_instance.validate_tokens(user_email)
        except Exception as e:
            raise OAuthError(f"Token validation failed for {provider}: {str(e)}")
    
    async def refresh_tokens(self, provider: str, user_email: str) -> Optional[Dict[str, Any]]:
        """Refresh tokens for a provider"""
        try:
            tokens = db_manager.get_valid_tokens(user_email, provider)
            if not tokens or not tokens.get("refresh_token"):
                return None
            
            provider_instance = self.get_provider(provider)
            refresh_result = await provider_instance.refresh_access_token(tokens["refresh_token"])
            
            if refresh_result:
                # Update stored tokens
                db_manager.update_tokens(
                    user_email, provider,
                    access_token=refresh_result["access_token"],
                    refresh_token=refresh_result.get("refresh_token"),
                    expires_at=datetime.now() + timedelta(seconds=refresh_result["expires_in"])
                )
                
                db_manager.log_activity(
                    user_email=user_email,
                    provider=provider,
                    action="token_refreshed"
                )
            
            return refresh_result
        except Exception as e:
            raise OAuthError(f"Token refresh failed for {provider}: {str(e)}")
    
    async def revoke_tokens(self, provider: str, user_email: str) -> bool:
        """Revoke tokens for a provider"""
        try:
            provider_instance = self.get_provider(provider)
            result = await provider_instance.revoke_tokens(user_email)
            
            if result:
                db_manager.log_activity(
                    user_email=user_email,
                    provider=provider,
                    action="tokens_revoked"
                )
            
            return result
        except Exception as e:
            raise OAuthError(f"Token revocation failed for {provider}: {str(e)}")
    
    async def get_user_status(self, user_email: str) -> Dict[str, Any]:
        """Get OAuth status for all providers for a user"""
        try:
            status = {}
            
            for provider_name in self.providers.keys():
                try:
                    tokens = db_manager.get_valid_tokens(user_email, provider_name)
                    if tokens:
                        # Test connection
                        provider_instance = self.get_provider(provider_name)
                        validation = await provider_instance.validate_tokens(user_email)
                        status[provider_name] = {
                            "connected": validation.get("valid", False),
                            "user_info": validation.get("user_info"),
                            "expires_at": tokens.get("expires_at")
                        }
                    else:
                        status[provider_name] = {
                            "connected": False,
                            "reason": "No tokens found"
                        }
                except Exception as e:
                    status[provider_name] = {
                        "connected": False,
                        "error": str(e)
                    }
            
            return {
                "success": True,
                "user_email": user_email,
                "providers": status
            }
        except Exception as e:
            raise OAuthError(f"Failed to get user status: {str(e)}")
    
    def get_available_providers(self) -> Dict[str, Any]:
        """Get list of available OAuth providers"""
        providers_info = {}
        
        for provider_name, provider_instance in self.providers.items():
            try:
                providers_info[provider_name] = {
                    "name": provider_name,
                    "configured": bool(provider_instance.client_id and provider_instance.client_secret),
                    "scopes": provider_instance.get_available_scopes(),
                    "redirect_uri": provider_instance.redirect_uri
                }
            except Exception as e:
                providers_info[provider_name] = {
                    "name": provider_name,
                    "configured": False,
                    "error": str(e)
                }
        
        return {
            "success": True,
            "providers": providers_info
        }


# Global OAuth service instance
oauth_service = OAuthService() 
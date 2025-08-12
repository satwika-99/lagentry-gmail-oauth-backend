"""
Authentication API endpoints for v1
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from typing import List, Dict, Any, Optional

from app.core.auth import get_provider
from app.core.database import db_manager
from app.core.exceptions import OAuthCallbackException, InvalidProviderException
from app.core.utils import create_success_response, create_error_response, validate_provider
from app.schemas.auth import (
    OAuthCallbackResponse, AuthUrlResponse, UserTokensResponse,
    TokenValidationResponse, RevokeTokenResponse, ProviderInfo
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/")
async def auth_status():
    """Get authentication API status"""
    return {
        "success": True,
        "provider": "auth",
        "description": "Authentication API for all OAuth providers",
        "supported_providers": ["google", "microsoft", "atlassian", "slack"],
        "endpoints": [
            "/{provider}",
            "/{provider}/callback",
            "/{provider}/refresh",
            "/{provider}/validate",
            "/{provider}/revoke",
            "/tokens/{user_email}",
            "/tokens/{user_email}/{provider}"
        ]
    }


@router.get("")
async def auth_status_no_slash():
    """Get authentication API status (no trailing slash)"""
    return {
        "success": True,
        "provider": "auth",
        "description": "Authentication API for all OAuth providers",
        "supported_providers": ["google", "microsoft", "atlassian", "slack"],
        "endpoints": [
            "/{provider}",
            "/{provider}/callback",
            "/{provider}/refresh",
            "/{provider}/validate",
            "/{provider}/revoke",
            "/tokens/{user_email}",
            "/tokens/{user_email}/{provider}"
        ]
    }


@router.get("/{provider}", response_model=AuthUrlResponse)
async def initiate_oauth(provider: str):
    """Initiate OAuth flow for a provider"""
    try:
        # Validate provider
        if not validate_provider(provider, ["google", "microsoft", "atlassian", "slack"]):
            raise InvalidProviderException(f"Provider '{provider}' not supported")
        
        # Get OAuth provider
        oauth_provider = get_provider(provider)
        
        # Generate auth URL
        state = oauth_provider.generate_state()
        auth_url = oauth_provider.get_auth_url(state)
        
        return AuthUrlResponse(
            auth_url=auth_url,
            state=state,
            provider=provider
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{provider}/callback", response_model=OAuthCallbackResponse)
async def oauth_callback(
    provider: str,
    code: str = Query(..., description="Authorization code"),
    state: str = Query(..., description="State parameter")
):
    """Handle OAuth callback"""
    try:
        # Validate provider
        if not validate_provider(provider, ["google", "microsoft", "atlassian", "slack"]):
            raise InvalidProviderException(f"Provider '{provider}' not supported")
        
        # Get OAuth provider
        oauth_provider = get_provider(provider)
        
        # Handle callback
        result = await oauth_provider.handle_callback(code, state)
        
        return OAuthCallbackResponse(**result)
        
    except OAuthCallbackException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")


@router.get("/{provider}/refresh")
async def refresh_tokens(provider: str, user_email: str):
    """Refresh access tokens"""
    try:
        # Validate provider
        if not validate_provider(provider, ["google", "microsoft", "atlassian", "slack"]):
            raise InvalidProviderException(f"Provider '{provider}' not supported")
        
        # Get OAuth provider
        oauth_provider = get_provider(provider)
        
        # Get current tokens
        tokens = oauth_provider.get_valid_tokens(user_email)
        if not tokens:
            raise HTTPException(status_code=404, detail="No tokens found for user")
        
        # Refresh tokens
        new_tokens = await oauth_provider.refresh_access_token(tokens["refresh_token"])
        if not new_tokens:
            raise HTTPException(status_code=400, detail="Token refresh failed")
        
        # Update tokens in database
        success = oauth_provider.store_tokens(
            user_email,
            new_tokens["access_token"],
            new_tokens.get("refresh_token", tokens["refresh_token"]),
            new_tokens["expires_in"]
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update tokens")
        
        return create_success_response({
            "message": "Tokens refreshed successfully",
            "access_token": new_tokens["access_token"][:20] + "...",
            "expires_in": new_tokens["expires_in"]
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")


@router.get("/{provider}/validate", response_model=TokenValidationResponse)
async def validate_tokens(provider: str, user_email: str):
    """Validate user tokens"""
    try:
        # Validate provider
        if not validate_provider(provider, ["google", "microsoft", "atlassian", "slack"]):
            raise InvalidProviderException(f"Provider '{provider}' not supported")
        
        # Get OAuth provider
        oauth_provider = get_provider(provider)
        
        # Get tokens
        tokens = oauth_provider.get_valid_tokens(user_email)
        
        if not tokens:
            return TokenValidationResponse(
                is_valid=False,
                needs_refresh=False
            )
        
        # Check if token needs refresh (expires within 5 minutes)
        from datetime import datetime, timedelta
        expires_at = datetime.fromisoformat(tokens["expires_at"])
        needs_refresh = (expires_at - datetime.now()) < timedelta(minutes=5)
        
        return TokenValidationResponse(
            is_valid=True,
            expires_at=expires_at,
            scopes=tokens.get("scopes"),
            needs_refresh=needs_refresh
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token validation failed: {str(e)}")


@router.delete("/{provider}/revoke", response_model=RevokeTokenResponse)
async def revoke_tokens(provider: str, user_email: str):
    """Revoke user tokens"""
    try:
        # Validate provider
        if not validate_provider(provider, ["google", "microsoft", "atlassian", "slack"]):
            raise InvalidProviderException(f"Provider '{provider}' not supported")
        
        # Delete tokens
        success = db_manager.delete_user_tokens(user_email, provider)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to revoke tokens")
        
        # Log activity
        db_manager.log_activity(user_email, provider, "token_revoked")
        
        return RevokeTokenResponse(
            message="Tokens revoked successfully",
            revoked_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token revocation failed: {str(e)}")


@router.get("/users", response_model=List[str])
async def get_users(provider: Optional[str] = None):
    """Get all users with stored tokens"""
    try:
        users = db_manager.get_all_users(provider)
        return users
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get users: {str(e)}")


@router.get("/users/{user_email}/tokens", response_model=UserTokensResponse)
async def get_user_tokens(user_email: str, provider: str):
    """Get user token information"""
    try:
        # Validate provider
        if not validate_provider(provider, ["google", "microsoft", "atlassian", "slack"]):
            raise InvalidProviderException(f"Provider '{provider}' not supported")
        
        # Get OAuth provider
        oauth_provider = get_provider(provider)
        
        # Get tokens
        tokens = oauth_provider.get_valid_tokens(user_email)
        
        if not tokens:
            return UserTokensResponse(
                user_email=user_email,
                provider=provider,
                has_valid_tokens=False
            )
        
        return UserTokensResponse(
            user_email=user_email,
            provider=provider,
            has_valid_tokens=True,
            expires_at=datetime.fromisoformat(tokens["expires_at"]),
            scopes=tokens.get("scopes")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user tokens: {str(e)}")


@router.get("/providers", response_model=List[ProviderInfo])
async def get_providers():
    """Get available OAuth providers"""
    providers = [
        ProviderInfo(
            name="google",
            display_name="Google",
            auth_url="/auth/google",
            scopes=["gmail.readonly", "userinfo.email"],
            is_configured=True  # You can check actual configuration here
        ),
        ProviderInfo(
            name="microsoft",
            display_name="Microsoft",
            auth_url="/auth/microsoft",
            scopes=["mail.read", "user.read"],
            is_configured=False
        ),
        ProviderInfo(
            name="atlassian",
            display_name="Atlassian",
            auth_url="/auth/atlassian",
            scopes=["read:jira-work", "read:confluence-content"],
            is_configured=False
        ),
        ProviderInfo(
            name="slack",
            display_name="Slack",
            auth_url="/auth/slack",
            scopes=["channels:read", "chat:write"],
            is_configured=False
        )
    ]
    
    return providers 
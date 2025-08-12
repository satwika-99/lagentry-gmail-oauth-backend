"""
Salesforce OAuth connector for authentication and token management
"""

import httpx
from typing import Dict, Any, Optional, List
from urllib.parse import urlencode
import json

from app.core.database import db_manager
from app.core.exceptions import AuthenticationException, TokenError
from app.core.config import settings


def get_auth_url(user_email: str, scope: str = "api refresh_token") -> str:
    """
    Generate Salesforce OAuth authorization URL
    
    Args:
        user_email: User email for state parameter
        scope: OAuth scopes (default: "api refresh_token")
    
    Returns:
        Salesforce OAuth authorization URL
    """
    # Salesforce OAuth configuration
    client_id = settings.salesforce_client_id
    redirect_uri = settings.salesforce_redirect_uri
    
    # Salesforce authorization URL
    auth_url = "https://login.salesforce.com/services/oauth2/authorize"
    
    # OAuth parameters
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": user_email  # Use email as state for callback
    }
    
    return f"{auth_url}?{urlencode(params)}"


async def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """
    Exchange authorization code for access token
    
    Args:
        code: Authorization code from Salesforce
    
    Returns:
        Token data including access_token, refresh_token, etc.
    """
    client_id = settings.salesforce_client_id
    client_secret = settings.salesforce_client_secret
    redirect_uri = settings.salesforce_redirect_uri
    
    # Salesforce token URL
    token_url = "https://login.salesforce.com/services/oauth2/token"
    
    # Token exchange parameters
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        
        if response.status_code != 200:
            raise TokenError(f"Token exchange failed: {response.text}")
        
        token_data = response.json()
        return token_data


async def validate_token(user_email: str) -> Dict[str, Any]:
    """
    Validate Salesforce access token
    
    Args:
        user_email: User email to get stored tokens
    
    Returns:
        Token validation result
    """
    try:
        # Get stored tokens
        tokens = db_manager.get_tokens(user_email, "salesforce")
        if not tokens:
            raise AuthenticationException("No Salesforce tokens found")
        
        access_token = tokens.get("access_token")
        instance_url = tokens.get("instance_url")
        
        if not access_token or not instance_url:
            raise AuthenticationException("Invalid token data")
        
        # Validate token by calling Salesforce identity endpoint
        identity_url = f"{instance_url}/services/oauth2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(identity_url, headers=headers)
            
            if response.status_code == 200:
                user_info = response.json()
                return {
                    "valid": True,
                    "message": "Token is valid",
                    "user_info": user_info,
                    "expires_at": tokens.get("expires_at"),
                    "scopes": tokens.get("scopes", [])
                }
            else:
                return {
                    "valid": False,
                    "message": "Token validation failed",
                    "expires_at": tokens.get("expires_at"),
                    "scopes": tokens.get("scopes", [])
                }
                
    except AuthenticationException as e:
        raise e
    except Exception as e:
        raise TokenError(f"Token validation error: {str(e)}")


async def get_user_info(user_email: str) -> Dict[str, Any]:
    """
    Get Salesforce user information
    
    Args:
        user_email: User email to get stored tokens
    
    Returns:
        User information from Salesforce
    """
    try:
        # Get stored tokens
        tokens = db_manager.get_tokens(user_email, "salesforce")
        if not tokens:
            raise AuthenticationException("No Salesforce tokens found")
        
        access_token = tokens.get("access_token")
        instance_url = tokens.get("instance_url")
        
        if not access_token or not instance_url:
            raise AuthenticationException("Invalid token data")
        
        # Get user info from Salesforce
        identity_url = f"{instance_url}/services/oauth2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(identity_url, headers=headers)
            
            if response.status_code == 200:
                user_info = response.json()
                return {
                    "success": True,
                    "user": user_info
                }
            else:
                return {
                    "success": False,
                    "user": None,
                    "message": f"Failed to get user info: {response.text}"
                }
                
    except AuthenticationException as e:
        raise e
    except Exception as e:
        return {
            "success": False,
            "user": None,
            "message": f"Error getting user info: {str(e)}"
        }


async def refresh_access_token(user_email: str) -> Dict[str, Any]:
    """
    Refresh Salesforce access token
    
    Args:
        user_email: User email to get stored tokens
    
    Returns:
        New token data
    """
    try:
        # Get stored tokens
        tokens = db_manager.get_tokens(user_email, "salesforce")
        if not tokens:
            raise AuthenticationException("No Salesforce tokens found")
        
        refresh_token = tokens.get("refresh_token")
        if not refresh_token:
            raise AuthenticationException("No refresh token found")
        
        client_id = settings.salesforce_client_id
        client_secret = settings.salesforce_client_secret
        
        # Salesforce token URL
        token_url = "https://login.salesforce.com/services/oauth2/token"
        
        # Token refresh parameters
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            
            if response.status_code != 200:
                raise TokenError(f"Token refresh failed: {response.text}")
            
            token_data = response.json()
            
            # Update stored tokens
            new_access_token = token_data.get("access_token")
            new_expires_in = int(token_data.get("expires_in", 7200))
            
            db_manager.update_access_token(user_email, "salesforce", new_access_token, new_expires_in)
            
            return token_data
            
    except AuthenticationException as e:
        raise e
    except Exception as e:
        raise TokenError(f"Token refresh error: {str(e)}")


def get_salesforce_scopes() -> List[str]:
    """
    Get available Salesforce OAuth scopes
    
    Returns:
        List of available scopes
    """
    return [
        "api",                    # Full access to Salesforce APIs
        "refresh_token",          # Ability to refresh access tokens
        "offline_access",         # Access when user is not present
        "web",                    # Web application access
        "mobile",                 # Mobile application access
        "full",                   # Full access (includes all scopes)
        "visualforce",            # Visualforce page access
        "chatter_api",            # Chatter API access
        "custom_permissions",     # Custom permissions access
        "wave_api",               # Einstein Analytics API access
        "lightning",              # Lightning platform access
        "content",                # Content API access
        "openid",                 # OpenID Connect
        "profile",                # Profile information
        "email",                  # Email address
        "address",                # Address information
        "phone"                   # Phone number
    ]


async def revoke_token(user_email: str) -> Dict[str, Any]:
    """
    Revoke Salesforce access token
    
    Args:
        user_email: User email to get stored tokens
    
    Returns:
        Revocation result
    """
    try:
        # Get stored tokens
        tokens = db_manager.get_tokens(user_email, "salesforce")
        if not tokens:
            raise AuthenticationException("No Salesforce tokens found")
        
        access_token = tokens.get("access_token")
        if not access_token:
            raise AuthenticationException("No access token found")
        
        # Salesforce token revocation URL
        revoke_url = "https://login.salesforce.com/services/oauth2/revoke"
        
        # Revocation parameters
        data = {"token": access_token}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(revoke_url, data=data)
            
            if response.status_code == 200:
                # Remove tokens from database
                db_manager.remove_tokens(user_email, "salesforce")
                return {
                    "success": True,
                    "message": "Token revoked successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Token revocation failed: {response.text}"
                }
                
    except AuthenticationException as e:
        raise e
    except Exception as e:
        return {
            "success": False,
            "message": f"Token revocation error: {str(e)}"
        }

"""
Authentication schemas for the Lagentry OAuth Backend
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class OAuthCallbackRequest(BaseModel):
    """OAuth callback request schema"""
    code: str = Field(..., description="Authorization code from OAuth provider")
    state: str = Field(..., description="State parameter for CSRF protection")


class OAuthCallbackResponse(BaseModel):
    """OAuth callback response schema"""
    message: str = Field(..., description="Success message")
    user_email: str = Field(..., description="User email address")
    access_token: str = Field(..., description="Partial access token for security")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenInfo(BaseModel):
    """Token information schema"""
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    expires_at: datetime = Field(..., description="Token expiration time")
    scopes: Optional[List[str]] = Field(None, description="Token scopes")


class UserInfo(BaseModel):
    """User information schema"""
    email: EmailStr = Field(..., description="User email address")
    name: Optional[str] = Field(None, description="User display name")
    provider: str = Field(..., description="OAuth provider name")
    is_active: bool = Field(True, description="User active status")
    created_at: datetime = Field(..., description="User creation time")
    updated_at: datetime = Field(..., description="User last update time")


class AuthUrlResponse(BaseModel):
    """OAuth authorization URL response schema"""
    auth_url: str = Field(..., description="OAuth authorization URL")
    state: str = Field(..., description="State parameter for CSRF protection")
    provider: str = Field(..., description="OAuth provider name")


class TokenRefreshRequest(BaseModel):
    """Token refresh request schema"""
    user_email: EmailStr = Field(..., description="User email address")
    provider: str = Field(..., description="OAuth provider name")


class TokenRefreshResponse(BaseModel):
    """Token refresh response schema"""
    message: str = Field(..., description="Success message")
    access_token: str = Field(..., description="New access token (partial)")
    expires_in: int = Field(..., description="New token expiration time")


class UserTokensResponse(BaseModel):
    """User tokens response schema"""
    user_email: str = Field(..., description="User email address")
    provider: str = Field(..., description="OAuth provider name")
    has_valid_tokens: bool = Field(..., description="Whether user has valid tokens")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")
    scopes: Optional[List[str]] = Field(None, description="Token scopes")


class AuthErrorResponse(BaseModel):
    """Authentication error response schema"""
    error: bool = Field(True, description="Error flag")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")


class AuthSuccessResponse(BaseModel):
    """Authentication success response schema"""
    error: bool = Field(False, description="Error flag")
    message: str = Field(..., description="Success message")
    data: Dict[str, Any] = Field(..., description="Response data")
    timestamp: datetime = Field(..., description="Response timestamp")


class ProviderInfo(BaseModel):
    """OAuth provider information schema"""
    name: str = Field(..., description="Provider name")
    display_name: str = Field(..., description="Provider display name")
    auth_url: str = Field(..., description="Provider OAuth URL")
    scopes: List[str] = Field(..., description="Available scopes")
    is_configured: bool = Field(..., description="Whether provider is configured")


class AuthActivity(BaseModel):
    """Authentication activity log schema"""
    user_email: str = Field(..., description="User email address")
    provider: str = Field(..., description="OAuth provider name")
    action: str = Field(..., description="Activity action")
    details: Optional[Dict[str, Any]] = Field(None, description="Activity details")
    created_at: datetime = Field(..., description="Activity timestamp")


class OAuthState(BaseModel):
    """OAuth state management schema"""
    state: str = Field(..., description="State parameter")
    provider: str = Field(..., description="OAuth provider name")
    created_at: datetime = Field(..., description="State creation time")
    expires_at: datetime = Field(..., description="State expiration time")


class TokenValidationRequest(BaseModel):
    """Token validation request schema"""
    user_email: EmailStr = Field(..., description="User email address")
    provider: str = Field(..., description="OAuth provider name")


class TokenValidationResponse(BaseModel):
    """Token validation response schema"""
    is_valid: bool = Field(..., description="Whether token is valid")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")
    scopes: Optional[List[str]] = Field(None, description="Token scopes")
    needs_refresh: bool = Field(..., description="Whether token needs refresh")


class RevokeTokenRequest(BaseModel):
    """Token revocation request schema"""
    user_email: EmailStr = Field(..., description="User email address")
    provider: str = Field(..., description="OAuth provider name")


class RevokeTokenResponse(BaseModel):
    """Token revocation response schema"""
    message: str = Field(..., description="Success message")
    revoked_at: datetime = Field(..., description="Token revocation time") 
"""
Custom exceptions for the Lagentry OAuth Backend
"""

from typing import Optional, Dict, Any


class LagentryException(Exception):
    """Base exception for Lagentry OAuth Backend"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class OAuthException(LagentryException):
    """Exception raised during OAuth operations"""
    pass


class TokenException(LagentryException):
    """Exception raised during token operations"""
    pass


class ProviderException(LagentryException):
    """Exception raised by provider-specific operations"""
    pass


class DatabaseException(LagentryException):
    """Exception raised during database operations"""
    pass


class ConfigurationException(LagentryException):
    """Exception raised when configuration is invalid"""
    pass


class ValidationException(LagentryException):
    """Exception raised when data validation fails"""
    pass


class APIException(LagentryException):
    """Exception raised during API operations"""
    pass


class AuthenticationException(LagentryException):
    """Exception raised when authentication fails"""
    pass


class AuthorizationException(LagentryException):
    """Exception raised when authorization fails"""
    pass


class RateLimitException(LagentryException):
    """Exception raised when rate limits are exceeded"""
    pass


class NetworkException(LagentryException):
    """Exception raised when network operations fail"""
    pass


# Specific OAuth exceptions
class OAuthError(OAuthException):
    """Exception raised during OAuth operations"""
    pass


class OAuthCallbackException(OAuthException):
    """Exception raised during OAuth callback processing"""
    pass


class TokenError(TokenException):
    """Exception raised when token operations fail"""
    pass


class TokenRefreshException(TokenException):
    """Exception raised when token refresh fails"""
    pass


class TokenExpiredException(TokenException):
    """Exception raised when token has expired"""
    pass


class InvalidTokenException(TokenException):
    """Exception raised when token is invalid"""
    pass


# Provider-specific exceptions
class GoogleAPIException(ProviderException):
    """Exception raised by Google API operations"""
    pass


class MicrosoftAPIException(ProviderException):
    """Exception raised by Microsoft API operations"""
    pass


class AtlassianAPIException(ProviderException):
    """Exception raised by Atlassian API operations"""
    pass


class SlackAPIException(ProviderException):
    """Exception raised by Slack API operations"""
    pass


class ConnectorError(ProviderException):
    """Exception raised by connector operations"""
    pass


# Database exceptions
class DatabaseConnectionException(DatabaseException):
    """Exception raised when database connection fails"""
    pass


class DatabaseQueryException(DatabaseException):
    """Exception raised when database query fails"""
    pass


class DatabaseMigrationException(DatabaseException):
    """Exception raised when database migration fails"""
    pass


# Configuration exceptions
class MissingConfigurationException(ConfigurationException):
    """Exception raised when required configuration is missing"""
    pass


class InvalidConfigurationException(ConfigurationException):
    """Exception raised when configuration is invalid"""
    pass


# Validation exceptions
class InvalidEmailException(ValidationException):
    """Exception raised when email is invalid"""
    pass


class InvalidTokenFormatException(ValidationException):
    """Exception raised when token format is invalid"""
    pass


class InvalidProviderException(ValidationException):
    """Exception raised when provider is invalid"""
    pass


# API exceptions
class APIError(APIException):
    """Exception raised when API operations fail"""
    pass


class APIResponseException(APIException):
    """Exception raised when API response is invalid"""
    pass


class APIRequestException(APIException):
    """Exception raised when API request fails"""
    pass


class APITimeoutException(APIException):
    """Exception raised when API request times out"""
    pass


# Authentication exceptions
class InvalidCredentialsException(AuthenticationException):
    """Exception raised when credentials are invalid"""
    pass


class ExpiredCredentialsException(AuthenticationException):
    """Exception raised when credentials have expired"""
    pass


# Authorization exceptions
class InsufficientPermissionsException(AuthorizationException):
    """Exception raised when user lacks required permissions"""
    pass


class ScopeMismatchException(AuthorizationException):
    """Exception raised when requested scopes don't match granted scopes"""
    pass


# Rate limiting exceptions
class RateLimitExceededException(RateLimitException):
    """Exception raised when rate limit is exceeded"""
    pass


class QuotaExceededException(RateLimitException):
    """Exception raised when quota is exceeded"""
    pass


# Network exceptions
class ConnectionTimeoutException(NetworkException):
    """Exception raised when connection times out"""
    pass


class ConnectionRefusedException(NetworkException):
    """Exception raised when connection is refused"""
    pass


class DNSResolutionException(NetworkException):
    """Exception raised when DNS resolution fails"""
    pass 
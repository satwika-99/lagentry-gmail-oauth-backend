"""
Centralized configuration management for the Lagentry OAuth Backend
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application settings
    app_name: str = "Lagentry OAuth Backend"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server settings
    host: str = Field(default="127.0.0.1", env="HOST")
    port: int = Field(default=8083, env="PORT")
    
    # Database settings
    database_path: str = Field(default="oauth_tokens.db", env="DATABASE_PATH")
    
    # CORS settings
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://127.0.0.1:8081",
            "http://127.0.0.1:8083"
        ],
        env="CORS_ORIGINS"
    )
    
    # Google OAuth settings
    google_client_id: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(
        default="http://127.0.0.1:8081/auth/google/callback",
        env="GOOGLE_REDIRECT_URI"
    )
    google_scopes: List[str] = Field(
        default=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/userinfo.email"
        ],
        env="GOOGLE_SCOPES"
    )
    
    # Microsoft OAuth settings
    microsoft_client_id: Optional[str] = Field(default=None, env="MICROSOFT_CLIENT_ID")
    microsoft_client_secret: Optional[str] = Field(default=None, env="MICROSOFT_CLIENT_SECRET")
    microsoft_tenant_id: Optional[str] = Field(default=None, env="MICROSOFT_TENANT_ID")
    microsoft_redirect_uri: str = Field(
        default="http://localhost:8084/api/v1/microsoft/callback",
        env="MICROSOFT_REDIRECT_URI"
    )

    # Notion OAuth settings
    notion_client_id: Optional[str] = Field(default=None, env="NOTION_CLIENT_ID")
    notion_client_secret: Optional[str] = Field(default=None, env="NOTION_CLIENT_SECRET")
    notion_redirect_uri: str = Field(
        default="http://localhost:8084/api/v1/notion/callback",
        env="NOTION_REDIRECT_URI"
    )
    
    # Atlassian OAuth settings (for future use)
    atlassian_client_id: Optional[str] = Field(default=None, env="ATLASSIAN_CLIENT_ID")
    atlassian_client_secret: Optional[str] = Field(default=None, env="ATLASSIAN_CLIENT_SECRET")
    atlassian_redirect_uri: str = Field(
        default="http://127.0.0.1:8081/auth/atlassian/callback",
        env="ATLASSIAN_REDIRECT_URI"
    )
    atlassian_scopes: List[str] = Field(
        default=[
            "read:jira-work",
            "read:jira-user",
            "read:me"
        ],
        env="ATLASSIAN_SCOPES"
    )
    
    # Confluence OAuth settings (uses same Atlassian OAuth as Jira)
    confluence_redirect_uri: str = Field(
        default="http://127.0.0.1:8083/api/v1/confluence/auth/callback",
        env="CONFLUENCE_REDIRECT_URI"
    )
    
    # Jira Configuration (for API token authentication)
    jira_instance_url: Optional[str] = Field(default=None, env="JIRA_INSTANCE_URL")
    jira_username: Optional[str] = Field(default=None, env="JIRA_USERNAME")
    jira_api_token: Optional[str] = Field(default=None, env="JIRA_API_TOKEN")
    
    # Slack OAuth settings (for future use)
    slack_client_id: Optional[str] = Field(default=None, env="SLACK_CLIENT_ID")
    slack_client_secret: Optional[str] = Field(default=None, env="SLACK_CLIENT_SECRET")
    slack_redirect_uri: str = Field(
        default="http://127.0.0.1:8083/auth/slack/callback",
        env="SLACK_REDIRECT_URI"
    )
    slack_scopes: List[str] = Field(
        default=[
            "channels:read",
            "channels:history",
            "chat:write",
            "users:read",
            "users:read.email"
        ],
        env="SLACK_SCOPES"
    )
    slack_bot_token: Optional[str] = Field(default=None, env="SLACK_BOT_TOKEN")
    
    # Salesforce OAuth settings
    salesforce_client_id: Optional[str] = Field(default=None, env="SALESFORCE_CLIENT_ID")
    salesforce_client_secret: Optional[str] = Field(default=None, env="SALESFORCE_CLIENT_SECRET")
    salesforce_redirect_uri: str = Field(
        default="http://127.0.0.1:8083/api/v1/salesforce/callback",
        env="SALESFORCE_REDIRECT_URI"
    )
    salesforce_scopes: List[str] = Field(
        default=[
            "api",
            "refresh_token",
            "offline_access"
        ],
        env="SALESFORCE_SCOPES"
    )
    
    # Security settings
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    token_expiry_hours: int = Field(default=24, env="TOKEN_EXPIRY_HOURS")
    
    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def validate_google_config() -> bool:
    """Validate that Google OAuth configuration is complete"""
    if not settings.google_client_id:
        raise ValueError("GOOGLE_CLIENT_ID is required")
    if not settings.google_client_secret:
        raise ValueError("GOOGLE_CLIENT_SECRET is required")
    return True


def validate_microsoft_config() -> bool:
    """Validate that Microsoft OAuth configuration is complete"""
    if not settings.microsoft_client_id:
        raise ValueError("MICROSOFT_CLIENT_ID is required")
    if not settings.microsoft_client_secret:
        raise ValueError("MICROSOFT_CLIENT_SECRET is required")
    return True


def validate_atlassian_config() -> bool:
    """Validate that Atlassian OAuth configuration is complete"""
    if not settings.atlassian_client_id:
        raise ValueError("ATLASSIAN_CLIENT_ID is required")
    if not settings.atlassian_client_secret:
        raise ValueError("ATLASSIAN_CLIENT_SECRET is required")
    return True


def validate_slack_config() -> bool:
    """Validate that Slack OAuth configuration is complete"""
    if not settings.slack_client_id:
        raise ValueError("SLACK_CLIENT_ID is required")
    if not settings.slack_client_secret:
        raise ValueError("SLACK_CLIENT_SECRET is required")
    return True


def validate_jira_config() -> bool:
    """Validate that Jira configuration is complete"""
    if not settings.jira_instance_url:
        raise ValueError("JIRA_INSTANCE_URL is required")
    if not settings.jira_username:
        raise ValueError("JIRA_USERNAME is required")
    if not settings.jira_api_token:
        raise ValueError("JIRA_API_TOKEN is required")
    return True


def validate_notion_config() -> bool:
    """Validate that Notion OAuth configuration is complete"""
    if not settings.notion_client_id:
        raise ValueError("NOTION_CLIENT_ID is required")
    if not settings.notion_client_secret:
        raise ValueError("NOTION_CLIENT_SECRET is required")
    return True


def validate_salesforce_config() -> bool:
    """Validate that Salesforce OAuth configuration is complete"""
    if not settings.salesforce_client_id:
        raise ValueError("SALESFORCE_CLIENT_ID is required")
    if not settings.salesforce_client_secret:
        raise ValueError("SALESFORCE_CLIENT_SECRET is required")
    return True 
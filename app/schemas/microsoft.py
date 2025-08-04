"""
Microsoft Service Schemas
Pydantic models for Microsoft API responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Microsoft Outlook Schemas
class OutlookEmailListResponse(BaseModel):
    """Response model for Outlook email list"""
    success: bool = Field(..., description="Operation success status")
    emails: List[Dict[str, Any]] = Field(default_factory=list, description="List of email messages")
    total: int = Field(0, description="Total number of messages")
    query: Optional[str] = Field(None, description="Search query used")


class OutlookEmailResponse(BaseModel):
    """Response model for single Outlook email"""
    success: bool = Field(..., description="Operation success status")
    email: Dict[str, Any] = Field(..., description="Email message data")


class OutlookFolderResponse(BaseModel):
    """Response model for Outlook folders"""
    success: bool = Field(..., description="Operation success status")
    folders: List[Dict[str, Any]] = Field(default_factory=list, description="List of Outlook folders")


# Microsoft OneDrive Schemas
class OneDriveFileListResponse(BaseModel):
    """Response model for OneDrive file list"""
    success: bool = Field(..., description="Operation success status")
    files: List[Dict[str, Any]] = Field(default_factory=list, description="List of OneDrive files")
    total: int = Field(0, description="Total number of files")
    next_page_token: Optional[str] = Field(None, description="Token for next page")


class OneDriveFileResponse(BaseModel):
    """Response model for single OneDrive file"""
    success: bool = Field(..., description="Operation success status")
    file: Dict[str, Any] = Field(..., description="OneDrive file data")


class OneDriveSearchResponse(BaseModel):
    """Response model for OneDrive search results"""
    success: bool = Field(..., description="Operation success status")
    files: List[Dict[str, Any]] = Field(default_factory=list, description="List of search results")
    total: int = Field(0, description="Total number of results")
    query: str = Field(..., description="Search query used")


# Microsoft Teams Schemas
class TeamsChannelListResponse(BaseModel):
    """Response model for Teams channel list"""
    success: bool = Field(..., description="Operation success status")
    channels: List[Dict[str, Any]] = Field(default_factory=list, description="List of Teams channels")


class TeamsMessageListResponse(BaseModel):
    """Response model for Teams message list"""
    success: bool = Field(..., description="Operation success status")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="List of Teams messages")
    total: int = Field(0, description="Total number of messages")
    channel_id: str = Field(..., description="Channel ID")


class TeamsMessageResponse(BaseModel):
    """Response model for single Teams message"""
    success: bool = Field(..., description="Operation success status")
    message: Dict[str, Any] = Field(..., description="Teams message data")


# Microsoft SharePoint Schemas
class SharePointSiteListResponse(BaseModel):
    """Response model for SharePoint site list"""
    success: bool = Field(..., description="Operation success status")
    sites: List[Dict[str, Any]] = Field(default_factory=list, description="List of SharePoint sites")


class SharePointListResponse(BaseModel):
    """Response model for SharePoint list"""
    success: bool = Field(..., description="Operation success status")
    lists: List[Dict[str, Any]] = Field(default_factory=list, description="List of SharePoint lists")
    site_id: str = Field(..., description="Site ID")


class SharePointItemListResponse(BaseModel):
    """Response model for SharePoint item list"""
    success: bool = Field(..., description="Operation success status")
    items: List[Dict[str, Any]] = Field(default_factory=list, description="List of SharePoint items")
    total: int = Field(0, description="Total number of items")
    site_id: str = Field(..., description="Site ID")
    list_id: str = Field(..., description="List ID")


# Microsoft Graph Schemas
class MicrosoftGraphUserResponse(BaseModel):
    """Response model for Microsoft Graph user information"""
    success: bool = Field(..., description="Operation success status")
    user: Dict[str, Any] = Field(..., description="User data from Microsoft Graph")


class MicrosoftGraphTokenResponse(BaseModel):
    """Response model for Microsoft Graph token information"""
    success: bool = Field(..., description="Operation success status")
    access_token: str = Field(..., description="Access token")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    expires_at: datetime = Field(..., description="Token expiration time")
    scopes: List[str] = Field(default_factory=list, description="Token scopes")
    token_type: str = Field("Bearer", description="Token type")


# Microsoft Service Status Schemas
class MicrosoftServiceStatusResponse(BaseModel):
    """Response model for Microsoft service status"""
    success: bool = Field(..., description="Operation success status")
    provider: str = Field("microsoft", description="OAuth provider")
    connected: bool = Field(..., description="Whether user is connected")
    services: Dict[str, str] = Field(..., description="Status of each service")
    message: Optional[str] = Field(None, description="Status message")


# Microsoft OAuth Schemas
class MicrosoftOAuthRequest(BaseModel):
    """Request model for Microsoft OAuth"""
    client_id: str = Field(..., description="Microsoft application client ID")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    scopes: List[str] = Field(default_factory=list, description="Requested scopes")
    state: Optional[str] = Field(None, description="OAuth state parameter")


class MicrosoftOAuthResponse(BaseModel):
    """Response model for Microsoft OAuth callback"""
    success: bool = Field(..., description="OAuth success status")
    user_email: str = Field(..., description="User email address")
    user_name: Optional[str] = Field(None, description="User display name")
    access_token: str = Field(..., description="Access token")
    expires_at: datetime = Field(..., description="Token expiration time")
    scopes: List[str] = Field(default_factory=list, description="Granted scopes")


# Microsoft Error Schemas
class MicrosoftErrorResponse(BaseModel):
    """Response model for Microsoft API errors"""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Microsoft Graph error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


# Microsoft Calendar Schemas (if needed)
class MicrosoftCalendarListResponse(BaseModel):
    """Response model for Microsoft Calendar list"""
    success: bool = Field(..., description="Operation success status")
    calendars: List[Dict[str, Any]] = Field(default_factory=list, description="List of calendars")


class MicrosoftEventListResponse(BaseModel):
    """Response model for Microsoft Calendar event list"""
    success: bool = Field(..., description="Operation success status")
    events: List[Dict[str, Any]] = Field(default_factory=list, description="List of calendar events")
    total: int = Field(0, description="Total number of events")


class MicrosoftEventResponse(BaseModel):
    """Response model for single Microsoft Calendar event"""
    success: bool = Field(..., description="Operation success status")
    event: Dict[str, Any] = Field(..., description="Calendar event data")


# Microsoft To-Do Schemas (if needed)
class MicrosoftTodoListResponse(BaseModel):
    """Response model for Microsoft To-Do list"""
    success: bool = Field(..., description="Operation success status")
    todo_lists: List[Dict[str, Any]] = Field(default_factory=list, description="List of To-Do lists")


class MicrosoftTodoTaskListResponse(BaseModel):
    """Response model for Microsoft To-Do task list"""
    success: bool = Field(..., description="Operation success status")
    tasks: List[Dict[str, Any]] = Field(default_factory=list, description="List of To-Do tasks")
    total: int = Field(0, description="Total number of tasks")
    list_id: str = Field(..., description="To-Do list ID")


class MicrosoftTodoTaskResponse(BaseModel):
    """Response model for single Microsoft To-Do task"""
    success: bool = Field(..., description="Operation success status")
    task: Dict[str, Any] = Field(..., description="To-Do task data") 
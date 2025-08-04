"""
Slack Service Schemas
Pydantic models for Slack API responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Slack Channel Schemas
class ChannelListResponse(BaseModel):
    """Response model for Slack channel list"""
    success: bool = Field(..., description="Operation success status")
    channels: List[Dict[str, Any]] = Field(default_factory=list, description="List of Slack channels")
    total: int = Field(0, description="Total number of channels")


class ChannelResponse(BaseModel):
    """Response model for single Slack channel"""
    success: bool = Field(..., description="Operation success status")
    channel: Dict[str, Any] = Field(..., description="Slack channel data")


# Slack Message Schemas
class MessageListResponse(BaseModel):
    """Response model for Slack message list"""
    success: bool = Field(..., description="Operation success status")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="List of Slack messages")
    total: int = Field(0, description="Total number of messages")
    channel_id: str = Field(..., description="Channel ID")


class MessageResponse(BaseModel):
    """Response model for single Slack message"""
    success: bool = Field(..., description="Operation success status")
    message: Dict[str, Any] = Field(..., description="Slack message data")


# Slack File Schemas
class FileListResponse(BaseModel):
    """Response model for Slack file list"""
    success: bool = Field(..., description="Operation success status")
    files: List[Dict[str, Any]] = Field(default_factory=list, description="List of Slack files")
    total: int = Field(0, description="Total number of files")


class FileResponse(BaseModel):
    """Response model for single Slack file"""
    success: bool = Field(..., description="Operation success status")
    file: Dict[str, Any] = Field(..., description="Slack file data")


# Slack User Schemas
class UserListResponse(BaseModel):
    """Response model for Slack user list"""
    success: bool = Field(..., description="Operation success status")
    users: List[Dict[str, Any]] = Field(default_factory=list, description="List of Slack users")
    total: int = Field(0, description="Total number of users")


class UserResponse(BaseModel):
    """Response model for single Slack user"""
    success: bool = Field(..., description="Operation success status")
    user: Dict[str, Any] = Field(..., description="Slack user data")


# Slack Workspace Schemas
class WorkspaceInfoResponse(BaseModel):
    """Response model for Slack workspace information"""
    success: bool = Field(..., description="Operation success status")
    workspace: Dict[str, Any] = Field(..., description="Slack workspace data")


class WorkspaceStatsResponse(BaseModel):
    """Response model for Slack workspace statistics"""
    success: bool = Field(..., description="Operation success status")
    stats: Dict[str, Any] = Field(..., description="Slack workspace statistics")


# Slack Search Schemas
class SearchResponse(BaseModel):
    """Response model for Slack search results"""
    success: bool = Field(..., description="Operation success status")
    query: str = Field(..., description="Search query used")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Search results")
    total: int = Field(0, description="Total number of results")
    page: Optional[str] = Field(None, description="Next page token")


# Slack OAuth Schemas
class SlackOAuthRequest(BaseModel):
    """Request model for Slack OAuth"""
    client_id: str = Field(..., description="Slack application client ID")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    scopes: List[str] = Field(default_factory=list, description="Requested scopes")
    state: Optional[str] = Field(None, description="OAuth state parameter")


class SlackOAuthResponse(BaseModel):
    """Response model for Slack OAuth callback"""
    success: bool = Field(..., description="OAuth success status")
    user_id: str = Field(..., description="Slack user ID")
    user_name: Optional[str] = Field(None, description="Slack user name")
    team_id: str = Field(..., description="Slack team ID")
    team_name: str = Field(..., description="Slack team name")
    access_token: str = Field(..., description="Access token")
    expires_at: datetime = Field(..., description="Token expiration time")
    scopes: List[str] = Field(default_factory=list, description="Granted scopes")


# Slack Service Status Schemas
class SlackServiceStatusResponse(BaseModel):
    """Response model for Slack service status"""
    success: bool = Field(..., description="Operation success status")
    provider: str = Field("slack", description="OAuth provider")
    connected: bool = Field(..., description="Whether user is connected")
    services: Dict[str, str] = Field(..., description="Status of each service")
    message: Optional[str] = Field(None, description="Status message")


# Slack Error Schemas
class SlackErrorResponse(BaseModel):
    """Response model for Slack API errors"""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Slack API error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


# Slack Message Schemas (for creating/updating messages)
class SlackMessageRequest(BaseModel):
    """Request model for creating/updating Slack messages"""
    text: str = Field(..., description="Message text content")
    channel: str = Field(..., description="Channel ID")
    thread_ts: Optional[str] = Field(None, description="Thread timestamp")
    attachments: Optional[List[Dict[str, Any]]] = Field(None, description="Message attachments")
    blocks: Optional[List[Dict[str, Any]]] = Field(None, description="Message blocks")


class SlackMessageUpdateRequest(BaseModel):
    """Request model for updating Slack messages"""
    text: str = Field(..., description="Updated message text content")
    attachments: Optional[List[Dict[str, Any]]] = Field(None, description="Updated message attachments")
    blocks: Optional[List[Dict[str, Any]]] = Field(None, description="Updated message blocks")


# Slack File Upload Schemas
class SlackFileUploadRequest(BaseModel):
    """Request model for uploading files to Slack"""
    file: bytes = Field(..., description="File content")
    filename: str = Field(..., description="File name")
    title: Optional[str] = Field(None, description="File title")
    initial_comment: Optional[str] = Field(None, description="Initial comment")
    channels: Optional[List[str]] = Field(None, description="Channels to share file with")


# Slack User Profile Schemas
class SlackUserProfileResponse(BaseModel):
    """Response model for Slack user profile"""
    success: bool = Field(..., description="Operation success status")
    profile: Dict[str, Any] = Field(..., description="User profile data")
    user_id: str = Field(..., description="Slack user ID")


# Slack Channel History Schemas
class SlackChannelHistoryResponse(BaseModel):
    """Response model for Slack channel history"""
    success: bool = Field(..., description="Operation success status")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Channel messages")
    has_more: bool = Field(False, description="Whether there are more messages")
    latest: Optional[str] = Field(None, description="Latest message timestamp")
    oldest: Optional[str] = Field(None, description="Oldest message timestamp")
    channel_id: str = Field(..., description="Channel ID")


# Slack Reaction Schemas
class SlackReactionResponse(BaseModel):
    """Response model for Slack reactions"""
    success: bool = Field(..., description="Operation success status")
    reactions: List[Dict[str, Any]] = Field(default_factory=list, description="Message reactions")
    message_id: str = Field(..., description="Message ID")


# Slack Emoji Schemas
class SlackEmojiListResponse(BaseModel):
    """Response model for Slack emoji list"""
    success: bool = Field(..., description="Operation success status")
    emoji: Dict[str, str] = Field(default_factory=dict, description="Emoji mappings")
    total: int = Field(0, description="Total number of emoji") 
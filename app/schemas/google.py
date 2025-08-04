"""
Google Service Schemas
Pydantic models for Google API responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Gmail Schemas
class EmailListResponse(BaseModel):
    """Response model for email list"""
    success: bool = Field(..., description="Operation success status")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="List of email messages")
    total: int = Field(0, description="Total number of messages")
    query: Optional[str] = Field(None, description="Search query used")


class EmailResponse(BaseModel):
    """Response model for single email"""
    success: bool = Field(..., description="Operation success status")
    message: Dict[str, Any] = Field(..., description="Email message data")


class LabelResponse(BaseModel):
    """Response model for Gmail labels"""
    success: bool = Field(..., description="Operation success status")
    labels: List[Dict[str, Any]] = Field(default_factory=list, description="List of Gmail labels")


class ProfileResponse(BaseModel):
    """Response model for Gmail user profile"""
    success: bool = Field(..., description="Operation success status")
    profile: Dict[str, Any] = Field(..., description="User profile data")


# Google Drive Schemas
class DriveFileListResponse(BaseModel):
    """Response model for Drive file list"""
    success: bool = Field(..., description="Operation success status")
    files: List[Dict[str, Any]] = Field(default_factory=list, description="List of Drive files")
    total: int = Field(0, description="Total number of files")
    next_page_token: Optional[str] = Field(None, description="Token for next page")


class DriveFileResponse(BaseModel):
    """Response model for single Drive file"""
    success: bool = Field(..., description="Operation success status")
    file: Dict[str, Any] = Field(..., description="Drive file data")


class DriveSearchResponse(BaseModel):
    """Response model for Drive search results"""
    success: bool = Field(..., description="Operation success status")
    files: List[Dict[str, Any]] = Field(default_factory=list, description="List of search results")
    total: int = Field(0, description="Total number of results")
    query: str = Field(..., description="Search query used")


# Google Calendar Schemas
class CalendarListResponse(BaseModel):
    """Response model for calendar list"""
    success: bool = Field(..., description="Operation success status")
    calendars: List[Dict[str, Any]] = Field(default_factory=list, description="List of calendars")


class EventListResponse(BaseModel):
    """Response model for event list"""
    success: bool = Field(..., description="Operation success status")
    events: List[Dict[str, Any]] = Field(default_factory=list, description="List of calendar events")
    total: int = Field(0, description="Total number of events")


class EventResponse(BaseModel):
    """Response model for single calendar event"""
    success: bool = Field(..., description="Operation success status")
    event: Dict[str, Any] = Field(..., description="Calendar event data")


class EventCreateRequest(BaseModel):
    """Request model for creating calendar events"""
    summary: str = Field(..., description="Event summary/title")
    start_time: datetime = Field(..., description="Event start time")
    end_time: datetime = Field(..., description="Event end time")
    description: Optional[str] = Field(None, description="Event description")
    location: Optional[str] = Field(None, description="Event location")
    attendees: Optional[List[str]] = Field(None, description="List of attendee emails")


# Google Photos Schemas
class PhotoListResponse(BaseModel):
    """Response model for photo list"""
    success: bool = Field(..., description="Operation success status")
    photos: List[Dict[str, Any]] = Field(default_factory=list, description="List of photos")
    total: int = Field(0, description="Total number of photos")
    next_page_token: Optional[str] = Field(None, description="Token for next page")


class PhotoResponse(BaseModel):
    """Response model for single photo"""
    success: bool = Field(..., description="Operation success status")
    photo: Dict[str, Any] = Field(..., description="Photo data")


# Google Docs Schemas
class DocListResponse(BaseModel):
    """Response model for document list"""
    success: bool = Field(..., description="Operation success status")
    documents: List[Dict[str, Any]] = Field(default_factory=list, description="List of documents")
    total: int = Field(0, description="Total number of documents")


class DocResponse(BaseModel):
    """Response model for single document"""
    success: bool = Field(..., description="Operation success status")
    document: Dict[str, Any] = Field(..., description="Document data")


# Google YouTube Schemas
class VideoListResponse(BaseModel):
    """Response model for video list"""
    success: bool = Field(..., description="Operation success status")
    videos: List[Dict[str, Any]] = Field(default_factory=list, description="List of videos")
    total: int = Field(0, description="Total number of videos")
    next_page_token: Optional[str] = Field(None, description="Token for next page")


class VideoResponse(BaseModel):
    """Response model for single video"""
    success: bool = Field(..., description="Operation success status")
    video: Dict[str, Any] = Field(..., description="Video data")


# Common Google Schemas
class GoogleServiceStatus(BaseModel):
    """Response model for Google service status"""
    service: str = Field(..., description="Service name (gmail, drive, calendar, etc.)")
    status: str = Field(..., description="Service status (available, unavailable, error)")
    last_check: datetime = Field(..., description="Last status check time")
    error_message: Optional[str] = Field(None, description="Error message if status is error")


class GoogleUserInfo(BaseModel):
    """Response model for Google user information"""
    email: str = Field(..., description="User email address")
    name: Optional[str] = Field(None, description="User display name")
    picture: Optional[str] = Field(None, description="User profile picture URL")
    locale: Optional[str] = Field(None, description="User locale")
    verified_email: bool = Field(False, description="Whether email is verified")
    provider: str = Field("google", description="OAuth provider")


class GoogleTokenInfo(BaseModel):
    """Response model for Google token information"""
    access_token: str = Field(..., description="Access token")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    expires_at: datetime = Field(..., description="Token expiration time")
    scopes: List[str] = Field(default_factory=list, description="Token scopes")
    token_type: str = Field("Bearer", description="Token type")


class GoogleScopeInfo(BaseModel):
    """Response model for Google scope information"""
    service: str = Field(..., description="Service name")
    scopes: List[str] = Field(default_factory=list, description="Available scopes for the service")
    description: str = Field(..., description="Service description")


# Error Response Schemas
class GoogleErrorResponse(BaseModel):
    """Response model for Google API errors"""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp") 
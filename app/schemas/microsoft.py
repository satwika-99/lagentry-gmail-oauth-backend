"""
Microsoft API Schemas
Defines request and response models for Microsoft services
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Microsoft OAuth Schemas
class MicrosoftOAuthRequest(BaseModel):
    """Request model for Microsoft OAuth"""
    client_id: str = Field(..., description="Microsoft application client ID")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    scopes: List[str] = Field(default_factory=list, description="Requested scopes")
    state: Optional[str] = Field(None, description="OAuth state parameter")


class MicrosoftOAuthResponse(BaseModel):
    """Response model for Microsoft OAuth"""
    success: bool = Field(..., description="OAuth success status")
    token_data: Optional[Dict[str, Any]] = Field(None, description="Token information")


# Outlook/Email Schemas
class OutlookEmailAddress(BaseModel):
    """Email address model"""
    name: Optional[str] = Field(None, description="Display name")
    address: str = Field(..., description="Email address")


class OutlookEmailBody(BaseModel):
    """Email body model"""
    contentType: str = Field(..., description="Content type (HTML or Text)")
    content: str = Field(..., description="Email body content")


class OutlookEmail(BaseModel):
    """Outlook email model"""
    id: str = Field(..., description="Email ID")
    subject: Optional[str] = Field(None, description="Email subject")
    bodyPreview: Optional[str] = Field(None, description="Email body preview")
    body: Optional[OutlookEmailBody] = Field(None, description="Email body")
    from_: Optional[OutlookEmailAddress] = Field(None, alias="from", description="Sender")
    toRecipients: Optional[List[OutlookEmailAddress]] = Field(None, description="To recipients")
    ccRecipients: Optional[List[OutlookEmailAddress]] = Field(None, description="CC recipients")
    bccRecipients: Optional[List[OutlookEmailAddress]] = Field(None, description="BCC recipients")
    receivedDateTime: Optional[datetime] = Field(None, description="Received date/time")
    sentDateTime: Optional[datetime] = Field(None, description="Sent date/time")
    isRead: Optional[bool] = Field(None, description="Read status")
    hasAttachments: Optional[bool] = Field(None, description="Has attachments")
    importance: Optional[str] = Field(None, description="Importance level")


class OutlookEmailListResponse(BaseModel):
    """Response model for Outlook email list"""
    success: bool = Field(..., description="Request success status")
    emails: List[OutlookEmail] = Field(..., description="List of emails")
    total: int = Field(..., description="Total number of emails")


class OutlookEmailResponse(BaseModel):
    """Response model for single Outlook email"""
    success: bool = Field(..., description="Request success status")
    email: OutlookEmail = Field(..., description="Email details")


class OutlookFolder(BaseModel):
    """Outlook folder model"""
    id: str = Field(..., description="Folder ID")
    displayName: str = Field(..., description="Folder display name")
    totalItemCount: Optional[int] = Field(None, description="Total items in folder")
    unreadItemCount: Optional[int] = Field(None, description="Unread items in folder")


class OutlookFolderResponse(BaseModel):
    """Response model for Outlook folders"""
    success: bool = Field(..., description="Request success status")
    folders: List[OutlookFolder] = Field(..., description="List of folders")
    total: int = Field(..., description="Total number of folders")


class SendEmailRequest(BaseModel):
    """Request model for sending email"""
    to: str = Field(..., description="Recipient email")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")
    cc: Optional[str] = Field(None, description="CC recipient")
    bcc: Optional[str] = Field(None, description="BCC recipient")


# OneDrive Schemas
class OneDriveFile(BaseModel):
    """OneDrive file model"""
    id: str = Field(..., description="File ID")
    name: str = Field(..., description="File name")
    size: Optional[int] = Field(None, description="File size in bytes")
    lastModifiedDateTime: Optional[datetime] = Field(None, description="Last modified date/time")
    createdDateTime: Optional[datetime] = Field(None, description="Created date/time")
    webUrl: Optional[str] = Field(None, description="Web URL")
    downloadUrl: Optional[str] = Field(None, description="Download URL")
    file: Optional[Dict[str, Any]] = Field(None, description="File metadata")
    folder: Optional[Dict[str, Any]] = Field(None, description="Folder metadata")
    parentReference: Optional[Dict[str, Any]] = Field(None, description="Parent folder reference")


class OneDriveFileListResponse(BaseModel):
    """Response model for OneDrive file list"""
    success: bool = Field(..., description="Request success status")
    files: List[OneDriveFile] = Field(..., description="List of files")
    total: int = Field(..., description="Total number of files")


class OneDriveFileResponse(BaseModel):
    """Response model for single OneDrive file"""
    success: bool = Field(..., description="Request success status")
    file: OneDriveFile = Field(..., description="File details")


class OneDriveSearchResponse(BaseModel):
    """Response model for OneDrive search"""
    success: bool = Field(..., description="Request success status")
    files: List[OneDriveFile] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results")


class CreateFileRequest(BaseModel):
    """Request model for creating OneDrive file"""
    name: str = Field(..., description="File name")
    content: Optional[str] = Field(None, description="File content")
    folder_id: Optional[str] = Field(None, description="Parent folder ID")


# Teams Schemas
class TeamsChannel(BaseModel):
    """Teams channel model"""
    id: str = Field(..., description="Channel ID")
    displayName: str = Field(..., description="Channel display name")
    description: Optional[str] = Field(None, description="Channel description")
    teamId: Optional[str] = Field(None, description="Team ID")
    teamName: Optional[str] = Field(None, description="Team name")
    isFavoriteByDefault: Optional[bool] = Field(None, description="Is favorite by default")
    email: Optional[str] = Field(None, description="Channel email")


class TeamsMessage(BaseModel):
    """Teams message model"""
    id: str = Field(..., description="Message ID")
    body: Optional[Dict[str, Any]] = Field(None, description="Message body")
    createdDateTime: Optional[datetime] = Field(None, description="Created date/time")
    lastModifiedDateTime: Optional[datetime] = Field(None, description="Last modified date/time")
    from_: Optional[Dict[str, Any]] = Field(None, alias="from", description="Message sender")
    importance: Optional[str] = Field(None, description="Message importance")
    subject: Optional[str] = Field(None, description="Message subject")


class TeamsChannelListResponse(BaseModel):
    """Response model for Teams channels"""
    success: bool = Field(..., description="Request success status")
    channels: List[TeamsChannel] = Field(..., description="List of channels")
    total: int = Field(..., description="Total number of channels")


class TeamsMessageListResponse(BaseModel):
    """Response model for Teams messages"""
    success: bool = Field(..., description="Request success status")
    messages: List[TeamsMessage] = Field(..., description="List of messages")
    total: int = Field(..., description="Total number of messages")


class SendTeamsMessageRequest(BaseModel):
    """Request model for sending Teams message"""
    message: str = Field(..., description="Message content")


# SharePoint Schemas
class SharePointSite(BaseModel):
    """SharePoint site model"""
    id: str = Field(..., description="Site ID")
    displayName: str = Field(..., description="Site display name")
    name: str = Field(..., description="Site name")
    webUrl: str = Field(..., description="Site web URL")
    createdDateTime: Optional[datetime] = Field(None, description="Created date/time")
    lastModifiedDateTime: Optional[datetime] = Field(None, description="Last modified date/time")


class SharePointList(BaseModel):
    """SharePoint list model"""
    id: str = Field(..., description="List ID")
    displayName: str = Field(..., description="List display name")
    name: str = Field(..., description="List name")
    createdDateTime: Optional[datetime] = Field(None, description="Created date/time")
    lastModifiedDateTime: Optional[datetime] = Field(None, description="Last modified date/time")
    list_template: Optional[str] = Field(None, alias="list.template", description="List template")


class SharePointItem(BaseModel):
    """SharePoint list item model"""
    id: str = Field(..., description="Item ID")
    createdDateTime: Optional[datetime] = Field(None, description="Created date/time")
    lastModifiedDateTime: Optional[datetime] = Field(None, description="Last modified date/time")
    fields: Optional[Dict[str, Any]] = Field(None, description="Item fields")


class SharePointSiteListResponse(BaseModel):
    """Response model for SharePoint sites"""
    success: bool = Field(..., description="Request success status")
    sites: List[SharePointSite] = Field(..., description="List of sites")
    total: int = Field(..., description="Total number of sites")


class SharePointListResponse(BaseModel):
    """Response model for SharePoint lists"""
    success: bool = Field(..., description="Request success status")
    lists: List[SharePointList] = Field(..., description="List of lists")
    total: int = Field(..., description="Total number of lists")


class SharePointItemListResponse(BaseModel):
    """Response model for SharePoint items"""
    success: bool = Field(..., description="Request success status")
    items: List[SharePointItem] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")


# Calendar Schemas
class CalendarEventLocation(BaseModel):
    """Calendar event location model"""
    displayName: Optional[str] = Field(None, description="Location display name")
    locationType: Optional[str] = Field(None, description="Location type")
    uniqueId: Optional[str] = Field(None, description="Unique location ID")


class CalendarEventTime(BaseModel):
    """Calendar event time model"""
    dateTime: str = Field(..., description="Event date/time")
    timeZone: str = Field(..., description="Time zone")


class CalendarEventAttendee(BaseModel):
    """Calendar event attendee model"""
    type: Optional[str] = Field(None, description="Attendee type")
    status: Optional[Dict[str, Any]] = Field(None, description="Response status")
    emailAddress: Optional[Dict[str, Any]] = Field(None, description="Email address")


class CalendarEvent(BaseModel):
    """Calendar event model"""
    id: str = Field(..., description="Event ID")
    subject: str = Field(..., description="Event subject")
    start: CalendarEventTime = Field(..., description="Start time")
    end: CalendarEventTime = Field(..., description="End time")
    location: Optional[CalendarEventLocation] = Field(None, description="Event location")
    attendees: Optional[List[CalendarEventAttendee]] = Field(None, description="Event attendees")
    body: Optional[Dict[str, Any]] = Field(None, description="Event body")
    isAllDay: Optional[bool] = Field(None, description="Is all day event")
    isCancelled: Optional[bool] = Field(None, description="Is cancelled")
    organizer: Optional[Dict[str, Any]] = Field(None, description="Event organizer")


class CalendarEventListResponse(BaseModel):
    """Response model for calendar events"""
    success: bool = Field(..., description="Request success status")
    events: List[CalendarEvent] = Field(..., description="List of events")
    total: int = Field(..., description="Total number of events")


class CalendarEventResponse(BaseModel):
    """Response model for single calendar event"""
    success: bool = Field(..., description="Request success status")
    event: CalendarEvent = Field(..., description="Event details")


class CreateEventRequest(BaseModel):
    """Request model for creating calendar event"""
    subject: str = Field(..., description="Event subject")
    start_time: str = Field(..., description="Start time (ISO format)")
    end_time: str = Field(..., description="End time (ISO format)")
    location: Optional[str] = Field(None, description="Event location")
    attendees: Optional[str] = Field(None, description="Comma-separated attendee emails")
    body: Optional[str] = Field(None, description="Event description")


# User Profile Schemas
class UserProfile(BaseModel):
    """User profile model"""
    id: str = Field(..., description="User ID")
    displayName: str = Field(..., description="Display name")
    givenName: Optional[str] = Field(None, description="Given name")
    surname: Optional[str] = Field(None, description="Surname")
    userPrincipalName: str = Field(..., description="User principal name")
    mail: Optional[str] = Field(None, description="Email address")
    jobTitle: Optional[str] = Field(None, description="Job title")
    department: Optional[str] = Field(None, description="Department")
    officeLocation: Optional[str] = Field(None, description="Office location")
    mobilePhone: Optional[str] = Field(None, description="Mobile phone")
    businessPhones: Optional[List[str]] = Field(None, description="Business phones")


class UserProfileResponse(BaseModel):
    """Response model for user profile"""
    success: bool = Field(..., description="Request success status")
    profile: UserProfile = Field(..., description="User profile details")


class UserPhotoResponse(BaseModel):
    """Response model for user photo"""
    success: bool = Field(..., description="Request success status")
    photo: Optional[bytes] = Field(None, description="User photo data")
    message: Optional[str] = Field(None, description="Response message")


# Microsoft Service Status Schema
class MicrosoftServiceStatus(BaseModel):
    """Microsoft service status model"""
    success: bool = Field(..., description="Request success status")
    provider: str = Field(..., description="Service provider")
    connected: bool = Field(..., description="Connection status")
    services: Dict[str, str] = Field(..., description="Service implementation status")
    message: str = Field(..., description="Status message") 
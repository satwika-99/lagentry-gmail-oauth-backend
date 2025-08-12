"""
Microsoft API Endpoints
Handles Microsoft service operations (Outlook, OneDrive, Teams, etc.)
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.database import db_manager
from app.core.exceptions import APIError, TokenError
from app.schemas.microsoft import (
    OutlookEmailListResponse, OutlookEmailResponse, OutlookFolderResponse,
    OneDriveFileListResponse, OneDriveFileResponse, OneDriveSearchResponse
)
from app.connectors.microsoft.oauth import get_auth_url, exchange_code_for_token
from app.connectors.microsoft.graph_client import (
    fetch_outlook_emails, fetch_outlook_email, fetch_outlook_folders, send_outlook_email,
    fetch_onedrive_files, fetch_onedrive_file, download_onedrive_file, create_onedrive_file, 
    delete_onedrive_file, search_onedrive_files,
    fetch_teams_channels, fetch_teams_messages, send_teams_message,
    fetch_sharepoint_sites, fetch_sharepoint_lists, fetch_sharepoint_items,
    fetch_calendar_events, create_calendar_event, delete_calendar_event,
    fetch_user_profile, fetch_user_photo
)
from app.core.config import settings

router = APIRouter(prefix="/microsoft", tags=["Microsoft Services"])


@router.get("/")
async def microsoft_status():
    """Get Microsoft integration status"""
    return {
        "success": True,
        "provider": "microsoft",
        "configured": bool(settings.microsoft_client_id),
        "services": ["outlook", "onedrive", "teams", "sharepoint", "calendar"],
        "endpoints": [
            "/auth-url",
            "/callback",
            "/outlook/emails",
            "/outlook/folders",
            "/onedrive/files",
            "/teams/channels",
            "/calendar/events"
        ]
    }


@router.get("")
async def microsoft_status_no_slash():
    """Get Microsoft integration status (no trailing slash)"""
    return {
        "success": True,
        "provider": "microsoft",
        "configured": bool(settings.microsoft_client_id),
        "services": ["outlook", "onedrive", "teams", "sharepoint", "calendar"],
        "endpoints": [
            "/auth-url",
            "/callback",
            "/outlook/emails",
            "/outlook/folders",
            "/onedrive/files",
            "/teams/channels",
            "/calendar/events"
        ]
    }


@router.get("/auth-url")
def microsoft_auth_url(user_email: str = Query(...)):
    """Get Microsoft OAuth URL"""
    return {"auth_url": get_auth_url(user_email)}

@router.get("/callback")
async def microsoft_callback(code: str = Query(...), state: str = Query(...)):
    """Handle Microsoft OAuth callback and store tokens"""
    token_data = await exchange_code_for_token(code)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = int(token_data.get("expires_in", 3600))
    scopes = token_data.get("scope", "").split()
    user_email = state
    db_manager.store_tokens(user_email, "microsoft", access_token, refresh_token, expires_in, scopes)
    return {"success": True, "token_data": token_data}

# Outlook/Email Endpoints
@router.get("/outlook/emails")
async def get_outlook_emails(
    user_email: str = Query(...),
    max_results: int = Query(50),
    query: Optional[str] = Query(None)
):
    """Get emails from Outlook"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    emails = await fetch_outlook_emails(user_email, access_token, max_results, query)
    return {"success": True, "emails": emails, "total": len(emails)}

@router.get("/outlook/emails/{message_id}")
async def get_outlook_email(
    message_id: str = Path(..., description="Message ID"),
    user_email: str = Query(..., description="User email")
):
    """Get a specific email from Microsoft Outlook"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    email = await fetch_outlook_email(message_id, access_token)
    return {"success": True, "email": email}

@router.get("/outlook/folders")
async def get_outlook_folders(user_email: str = Query(..., description="User email")):
    """Get Outlook folders"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    folders = await fetch_outlook_folders(access_token)
    return {"success": True, "folders": folders, "total": len(folders)}

@router.post("/outlook/send")
async def send_outlook_email_endpoint(
    user_email: str = Query(..., description="User email"),
    to: str = Query(..., description="Recipient email"),
    subject: str = Query(..., description="Email subject"),
    body: str = Query(..., description="Email body"),
    cc: Optional[str] = Query(None, description="CC recipients"),
    bcc: Optional[str] = Query(None, description="BCC recipients")
):
    """Send an email via Microsoft Outlook"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    result = await send_outlook_email(access_token, to, subject, body, cc, bcc)
    return result

# OneDrive Endpoints
@router.get("/onedrive/files")
async def list_onedrive_files(
    user_email: str = Query(...),
    max_results: int = Query(50),
    query: Optional[str] = Query(None)
):
    """List files from OneDrive"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    files = await fetch_onedrive_files(user_email, access_token, max_results, query)
    return {"success": True, "files": files, "total": len(files)}

@router.get("/onedrive/files/{file_id}")
async def get_onedrive_file(
    file_id: str = Path(..., description="File ID"),
    user_email: str = Query(..., description="User email")
):
    """Get a specific file from Microsoft OneDrive"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    file_data = await fetch_onedrive_file(file_id, access_token)
    return {"success": True, "file": file_data}

@router.get("/onedrive/files/{file_id}/download")
async def download_onedrive_file_endpoint(
    file_id: str = Path(..., description="File ID"),
    user_email: str = Query(..., description="User email")
):
    """Download a file from Microsoft OneDrive"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    file_content = await download_onedrive_file(file_id, access_token)
    return {"success": True, "file_content": file_content}

@router.post("/onedrive/files")
async def create_onedrive_file_endpoint(
    user_email: str = Query(..., description="User email"),
    name: str = Query(..., description="File name"),
    content: Optional[str] = Query(None, description="File content"),
    folder_id: Optional[str] = Query(None, description="Parent folder ID")
):
    """Create a new file in Microsoft OneDrive"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    file_data = await create_onedrive_file(access_token, name, content, folder_id)
    return {"success": True, "file": file_data}

@router.delete("/onedrive/files/{file_id}")
async def delete_onedrive_file_endpoint(
    file_id: str = Path(..., description="File ID"),
    user_email: str = Query(..., description="User email")
):
    """Delete a file from Microsoft OneDrive"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    result = await delete_onedrive_file(file_id, access_token)
    return result

@router.get("/onedrive/search")
async def search_onedrive_files(
    user_email: str = Query(..., description="User email"),
    query: str = Query(..., description="Search query"),
    page_size: int = Query(50, description="Number of results to return")
):
    """Search for files in Microsoft OneDrive"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    files = await search_onedrive_files(access_token, query, page_size)
    return {"success": True, "files": files, "total": len(files)}

# Teams Endpoints
@router.get("/teams/channels")
async def list_teams_channels(user_email: str = Query(..., description="User email")):
    """List Microsoft Teams channels"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    channels = await fetch_teams_channels(access_token)
    return {"success": True, "channels": channels, "total": len(channels)}

@router.get("/teams/channels/{channel_id}/messages")
async def get_teams_messages(
    channel_id: str = Path(..., description="Channel ID"),
    team_id: str = Query(..., description="Team ID"),
    user_email: str = Query(..., description="User email"),
    max_results: int = Query(50, description="Maximum number of messages to return")
):
    """Get messages from a Microsoft Teams channel"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    messages = await fetch_teams_messages(channel_id, team_id, access_token, max_results)
    return {"success": True, "messages": messages, "total": len(messages)}

@router.post("/teams/channels/{channel_id}/messages")
async def send_teams_message_endpoint(
    channel_id: str = Path(..., description="Channel ID"),
    team_id: str = Query(..., description="Team ID"),
    user_email: str = Query(..., description="User email"),
    message: str = Query(..., description="Message content")
):
    """Send a message to a Microsoft Teams channel"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    result = await send_teams_message(channel_id, team_id, access_token, message)
    return {"success": True, "message": result}

# SharePoint Endpoints
@router.get("/sharepoint/sites")
async def list_sharepoint_sites(user_email: str = Query(..., description="User email")):
    """List Microsoft SharePoint sites"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    sites = await fetch_sharepoint_sites(access_token)
    return {"success": True, "sites": sites, "total": len(sites)}

@router.get("/sharepoint/sites/{site_id}/lists")
async def list_sharepoint_lists(
    site_id: str = Path(..., description="Site ID"),
    user_email: str = Query(..., description="User email")
):
    """List lists in a Microsoft SharePoint site"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    lists = await fetch_sharepoint_lists(site_id, access_token)
    return {"success": True, "lists": lists, "total": len(lists)}

@router.get("/sharepoint/sites/{site_id}/lists/{list_id}/items")
async def get_sharepoint_items(
    site_id: str = Path(..., description="Site ID"),
    list_id: str = Path(..., description="List ID"),
    user_email: str = Query(..., description="User email"),
    max_results: int = Query(50, description="Maximum number of items to return")
):
    """Get items from a Microsoft SharePoint list"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    items = await fetch_sharepoint_items(site_id, list_id, access_token, max_results)
    return {"success": True, "items": items, "total": len(items)}

# Calendar Endpoints
@router.get("/calendar/events")
async def list_calendar_events(
    user_email: str = Query(...),
    max_results: int = Query(50)
):
    """Get calendar events"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    events = await fetch_calendar_events(user_email, access_token, max_results)
    return {"success": True, "events": events, "total": len(events)}

@router.post("/calendar/events")
async def create_calendar_event_endpoint(
    user_email: str = Query(..., description="User email"),
    subject: str = Query(..., description="Event subject"),
    start_time: str = Query(..., description="Start time (ISO format)"),
    end_time: str = Query(..., description="End time (ISO format)"),
    location: Optional[str] = Query(None, description="Event location"),
    attendees: Optional[str] = Query(None, description="Comma-separated attendee emails"),
    body: Optional[str] = Query(None, description="Event description")
):
    """Create a calendar event"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    
    attendee_list = attendees.split(",") if attendees else None
    event = await create_calendar_event(access_token, subject, start_time, end_time, location, attendee_list, body)
    return {"success": True, "event": event}

@router.delete("/calendar/events/{event_id}")
async def delete_calendar_event_endpoint(
    event_id: str = Path(..., description="Event ID"),
    user_email: str = Query(..., description="User email")
):
    """Delete a calendar event"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    result = await delete_calendar_event(event_id, access_token)
    return result

# User Profile Endpoints
@router.get("/profile")
async def get_user_profile(user_email: str = Query(..., description="User email")):
    """Get current user profile"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    profile = await fetch_user_profile(access_token)
    return {"success": True, "profile": profile}

@router.get("/profile/photo")
async def get_user_photo(user_email: str = Query(..., description="User email")):
    """Get current user photo"""
    tokens = db_manager.get_valid_tokens(user_email, "microsoft")
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid Microsoft tokens. Please authenticate.")
    access_token = tokens["access_token"]
    photo = await fetch_user_photo(access_token)
    if photo:
        return {"success": True, "photo": photo}
    else:
        return {"success": False, "message": "No photo found"}

# Microsoft Service Status
@router.get("/status")
async def get_microsoft_status(user_email: str = Query(..., description="User email")):
    """Get Microsoft service status"""
    try:
        # Check if user has valid Microsoft tokens
        tokens = db_manager.get_valid_tokens(user_email, "microsoft")
        
        return {
            "success": True,
            "provider": "microsoft",
            "connected": bool(tokens),
            "services": {
                "outlook": "implemented",
                "onedrive": "implemented",
                "teams": "implemented",
                "sharepoint": "implemented",
                "calendar": "implemented",
                "profile": "implemented"
            },
            "message": "Microsoft services are fully implemented and ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
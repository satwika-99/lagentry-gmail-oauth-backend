import httpx
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .oauth import refresh_token
from app.core.database import db_manager

GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"

# Outlook/Email Functions
async def fetch_outlook_emails(user_email: str, access_token: str, max_results: int = 10, query: str = None):
    """Fetch emails from Outlook"""
    url = f"{GRAPH_API_BASE}/me/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"$top": max_results, "$orderby": "receivedDateTime desc"}
    if query:
        params["$search"] = query
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("value", [])

async def fetch_outlook_email(message_id: str, access_token: str):
    """Fetch a specific email by ID"""
    url = f"{GRAPH_API_BASE}/me/messages/{message_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

async def fetch_outlook_folders(access_token: str):
    """Fetch Outlook folders"""
    url = f"{GRAPH_API_BASE}/me/mailFolders"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json().get("value", [])

async def send_outlook_email(access_token: str, to: str, subject: str, body: str, cc: str = None, bcc: str = None):
    """Send an email via Outlook"""
    url = f"{GRAPH_API_BASE}/me/sendMail"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    message = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": body
        },
        "toRecipients": [{"emailAddress": {"address": to}}]
    }
    
    if cc:
        message["ccRecipients"] = [{"emailAddress": {"address": cc}}]
    if bcc:
        message["bccRecipients"] = [{"emailAddress": {"address": bcc}}]
    
    payload = {"message": message, "saveToSentItems": True}
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return {"success": True, "message": "Email sent successfully"}

# OneDrive Functions
async def fetch_onedrive_files(user_email: str, access_token: str, max_results: int = 10, query: str = None):
    """Fetch files from OneDrive"""
    url = f"{GRAPH_API_BASE}/me/drive/root/children"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"$top": max_results, "$orderby": "lastModifiedDateTime desc"}
    if query:
        params["$search"] = query
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("value", [])

async def fetch_onedrive_file(file_id: str, access_token: str):
    """Fetch a specific file by ID"""
    url = f"{GRAPH_API_BASE}/me/drive/items/{file_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

async def download_onedrive_file(file_id: str, access_token: str):
    """Download a file from OneDrive"""
    url = f"{GRAPH_API_BASE}/me/drive/items/{file_id}/content"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.content

async def create_onedrive_file(access_token: str, name: str, content: str = None, folder_id: str = None):
    """Create a new file in OneDrive"""
    if folder_id:
        url = f"{GRAPH_API_BASE}/me/drive/items/{folder_id}:/{name}:/content"
    else:
        url = f"{GRAPH_API_BASE}/me/drive/root:/{name}:/content"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "text/plain"
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.put(url, headers=headers, content=content or "")
        resp.raise_for_status()
        return resp.json()

async def delete_onedrive_file(file_id: str, access_token: str):
    """Delete a file from OneDrive"""
    url = f"{GRAPH_API_BASE}/me/drive/items/{file_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url, headers=headers)
        resp.raise_for_status()
        return {"success": True, "message": "File deleted successfully"}

async def search_onedrive_files(access_token: str, query: str, page_size: int = 50):
    """Search for files in OneDrive"""
    url = f"{GRAPH_API_BASE}/me/drive/root/search(q='{query}')"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"$top": page_size}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("value", [])

# Teams Functions
async def fetch_teams_channels(access_token: str):
    """Fetch Teams channels"""
    url = f"{GRAPH_API_BASE}/me/joinedTeams"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        teams = resp.json().get("value", [])
        
        all_channels = []
        for team in teams:
            team_id = team.get("id")
            if team_id:
                channels_url = f"{GRAPH_API_BASE}/teams/{team_id}/channels"
                channels_resp = await client.get(channels_url, headers=headers)
                if channels_resp.status_code == 200:
                    channels = channels_resp.json().get("value", [])
                    for channel in channels:
                        channel["teamId"] = team_id
                        channel["teamName"] = team.get("displayName", "")
                    all_channels.extend(channels)
        
        return all_channels

async def fetch_teams_messages(channel_id: str, team_id: str, access_token: str, max_results: int = 50):
    """Fetch messages from a Teams channel"""
    url = f"{GRAPH_API_BASE}/teams/{team_id}/channels/{channel_id}/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"$top": max_results, "$orderby": "createdDateTime desc"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("value", [])

async def send_teams_message(channel_id: str, team_id: str, access_token: str, message: str):
    """Send a message to a Teams channel"""
    url = f"{GRAPH_API_BASE}/teams/{team_id}/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "body": {
            "content": message
        }
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()

# SharePoint Functions
async def fetch_sharepoint_sites(access_token: str):
    """Fetch SharePoint sites"""
    url = f"{GRAPH_API_BASE}/me/sites"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json().get("value", [])

async def fetch_sharepoint_lists(site_id: str, access_token: str):
    """Fetch lists from a SharePoint site"""
    url = f"{GRAPH_API_BASE}/sites/{site_id}/lists"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json().get("value", [])

async def fetch_sharepoint_items(site_id: str, list_id: str, access_token: str, max_results: int = 50):
    """Fetch items from a SharePoint list"""
    url = f"{GRAPH_API_BASE}/sites/{site_id}/lists/{list_id}/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"$top": max_results}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("value", [])

# Calendar Functions
async def fetch_calendar_events(user_email: str, access_token: str, max_results: int = 10):
    """Fetch calendar events"""
    url = f"{GRAPH_API_BASE}/me/events"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "$top": max_results,
        "$orderby": "start/dateTime",
        "$select": "id,subject,start,end,location,attendees,body"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("value", [])

async def create_calendar_event(access_token: str, subject: str, start_time: str, end_time: str, 
                               location: str = None, attendees: List[str] = None, body: str = None):
    """Create a calendar event"""
    url = f"{GRAPH_API_BASE}/me/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "subject": subject,
        "start": {
            "dateTime": start_time,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "UTC"
        }
    }
    
    if location:
        payload["location"] = {"displayName": location}
    
    if attendees:
        payload["attendees"] = [{"emailAddress": {"address": email}} for email in attendees]
    
    if body:
        payload["body"] = {
            "contentType": "HTML",
            "content": body
        }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()

async def delete_calendar_event(event_id: str, access_token: str):
    """Delete a calendar event"""
    url = f"{GRAPH_API_BASE}/me/events/{event_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url, headers=headers)
        resp.raise_for_status()
        return {"success": True, "message": "Event deleted successfully"}

# User Profile Functions
async def fetch_user_profile(access_token: str):
    """Fetch current user profile"""
    url = f"{GRAPH_API_BASE}/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

async def fetch_user_photo(access_token: str):
    """Fetch current user photo"""
    url = f"{GRAPH_API_BASE}/me/photo/$value"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.content
        return None

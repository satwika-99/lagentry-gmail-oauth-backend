"""
Notion OAuth Handler
Handles Notion OAuth 2.0 authentication flow
"""

import os
import httpx
from urllib.parse import urlencode
from core.config import settings
from core.database import db_manager

NOTION_AUTH_BASE = "https://api.notion.com/v1/oauth/authorize"
NOTION_TOKEN_URL = "https://api.notion.com/v1/oauth/token"

SCOPES = [
    "read_content",
    "update_content", 
    "insert_content",
    "create_pages",
    "update_pages",
    "delete_pages"
]

def get_auth_url(user_email: str) -> str:
    """Generate Notion OAuth authorization URL"""
    params = {
        "client_id": settings.notion_client_id,
        "response_type": "code",
        "owner": "user",
        "redirect_uri": settings.notion_redirect_uri,
        "state": user_email
    }
    return NOTION_AUTH_BASE + "?" + urlencode(params)

async def exchange_code_for_token(code: str) -> dict:
    """Exchange authorization code for access token"""
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.notion_redirect_uri
    }
    
    headers = {
        "Authorization": f"Basic {_get_basic_auth_header()}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(NOTION_TOKEN_URL, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()

async def refresh_token(refresh_token: str) -> dict:
    """Refresh Notion access token"""
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    headers = {
        "Authorization": f"Basic {_get_basic_auth_header()}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(NOTION_TOKEN_URL, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()

def _get_basic_auth_header() -> str:
    """Generate Basic Auth header for Notion API"""
    import base64
    credentials = f"{settings.notion_client_id}:{settings.notion_client_secret}"
    return base64.b64encode(credentials.encode()).decode()

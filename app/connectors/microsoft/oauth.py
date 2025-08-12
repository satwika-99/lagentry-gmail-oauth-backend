import os
import httpx
from urllib.parse import urlencode
from app.core.config import settings
from app.core.database import db_manager

MICROSOFT_AUTH_BASE = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
MICROSOFT_TOKEN_URL = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

SCOPES = [
    "offline_access",
    "User.Read",
    "Mail.Read",
    "Mail.Send",
    "Files.Read",
    "Files.ReadWrite",
    "Calendars.Read",
    "Calendars.ReadWrite"
]

def get_auth_url(user_email: str) -> str:
    params = {
        "client_id": settings.microsoft_client_id,
        "response_type": "code",
        "redirect_uri": settings.microsoft_redirect_uri,
        "response_mode": "query",
        "scope": " ".join(SCOPES),
        "state": user_email
    }
    return MICROSOFT_AUTH_BASE.format(tenant_id=settings.microsoft_tenant_id) + "?" + urlencode(params)

async def exchange_code_for_token(code: str) -> dict:
    data = {
        "client_id": settings.microsoft_client_id,
        "scope": " ".join(SCOPES),
        "code": code,
        "redirect_uri": settings.microsoft_redirect_uri,
        "grant_type": "authorization_code",
        "client_secret": settings.microsoft_client_secret
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(MICROSOFT_TOKEN_URL.format(tenant_id=settings.microsoft_tenant_id), data=data)
        resp.raise_for_status()
        return resp.json()

async def refresh_token(refresh_token: str) -> dict:
    data = {
        "client_id": settings.microsoft_client_id,
        "scope": " ".join(SCOPES),
        "refresh_token": refresh_token,
        "redirect_uri": settings.microsoft_redirect_uri,
        "grant_type": "refresh_token",
        "client_secret": settings.microsoft_client_secret
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(MICROSOFT_TOKEN_URL.format(tenant_id=settings.microsoft_tenant_id), data=data)
        resp.raise_for_status()
        return resp.json()

# Add functions to store/retrieve tokens using db_manager as in other connectors

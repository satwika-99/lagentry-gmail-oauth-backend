"""
Unified API Router
Provides endpoints for all providers using the modular structure
"""

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from typing import Optional, List, Dict, Any
from datetime import datetime

from services.oauth_service import oauth_service
from services.connector_service import connector_service
from core.exceptions import OAuthError, ConnectorError

router = APIRouter(prefix="/unified", tags=["Unified API"])


# OAuth Endpoints
@router.get("/auth/{provider}/url")
async def get_auth_url(
    provider: str = Path(..., description="Provider name (google, slack, atlassian)"),
    state: Optional[str] = Query(None, description="State parameter"),
    scopes: Optional[List[str]] = Query(None, description="Requested scopes")
):
    """Get OAuth authorization URL for a provider"""
    try:
        auth_url = oauth_service.get_auth_url(provider, state=state, scopes=scopes)
        return {
            "success": True,
            "provider": provider,
            "auth_url": auth_url,
            "state": state
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/auth/{provider}/callback")
async def oauth_callback(
    provider: str = Path(..., description="Provider name"),
    code: str = Query(..., description="Authorization code"),
    state: str = Query("", description="State parameter")
):
    """Handle OAuth callback for a provider"""
    try:
        result = await oauth_service.handle_callback(provider, code, state)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/auth/{provider}/validate")
async def validate_tokens(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email")
):
    """Validate tokens for a provider"""
    try:
        result = await oauth_service.validate_tokens(provider, user_email)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/auth/{provider}/refresh")
async def refresh_tokens(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email")
):
    """Refresh tokens for a provider"""
    try:
        result = await oauth_service.refresh_tokens(provider, user_email)
        return {
            "success": True,
            "provider": provider,
            "user_email": user_email,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/auth/{provider}/revoke")
async def revoke_tokens(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email")
):
    """Revoke tokens for a provider"""
    try:
        result = await oauth_service.revoke_tokens(provider, user_email)
        return {
            "success": result,
            "provider": provider,
            "user_email": user_email
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/auth/status")
async def get_user_status(user_email: str = Query(..., description="User email")):
    """Get OAuth status for all providers for a user"""
    try:
        result = await oauth_service.get_user_status(user_email)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/auth/providers")
async def get_available_providers():
    """Get list of available OAuth providers"""
    try:
        result = oauth_service.get_available_providers()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Connector Endpoints
@router.get("/connectors")
async def get_available_connectors():
    """Get list of available connectors"""
    try:
        connectors = connector_service.get_available_connectors()
        return {
            "success": True,
            "connectors": connectors
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/connectors/{provider}/test")
async def test_connection(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email")
):
    """Test connection for a provider"""
    try:
        result = await connector_service.test_connection(provider, user_email)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/connectors/{provider}/capabilities")
async def get_capabilities(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email")
):
    """Get capabilities for a provider"""
    try:
        result = await connector_service.get_capabilities(provider, user_email)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Generic Data Endpoints
@router.get("/connectors/{provider}/items")
async def list_items(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email"),
    max_results: int = Query(50, description="Maximum number of items"),
    **kwargs
):
    """List items from a provider"""
    try:
        result = await connector_service.list_items(provider, user_email, max_results=max_results, **kwargs)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/connectors/{provider}/items/{item_id}")
async def get_item(
    provider: str = Path(..., description="Provider name"),
    item_id: str = Path(..., description="Item ID"),
    user_email: str = Query(..., description="User email"),
    **kwargs
):
    """Get a specific item from a provider"""
    try:
        result = await connector_service.get_item(provider, user_email, item_id, **kwargs)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/connectors/{provider}/items")
async def create_item(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email"),
    data: Dict[str, Any] = None
):
    """Create an item in a provider"""
    try:
        result = await connector_service.create_item(provider, user_email, data or {})
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/connectors/{provider}/items/{item_id}")
async def update_item(
    provider: str = Path(..., description="Provider name"),
    item_id: str = Path(..., description="Item ID"),
    user_email: str = Query(..., description="User email"),
    data: Dict[str, Any] = None
):
    """Update an item in a provider"""
    try:
        result = await connector_service.update_item(provider, user_email, item_id, data or {})
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/connectors/{provider}/items/{item_id}")
async def delete_item(
    provider: str = Path(..., description="Provider name"),
    item_id: str = Path(..., description="Item ID"),
    user_email: str = Query(..., description="User email")
):
    """Delete an item from a provider"""
    try:
        result = await connector_service.delete_item(provider, user_email, item_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/connectors/{provider}/search")
async def search_items(
    provider: str = Path(..., description="Provider name"),
    user_email: str = Query(..., description="User email"),
    query: str = Query(..., description="Search query"),
    max_results: int = Query(50, description="Maximum number of results")
):
    """Search items in a provider"""
    try:
        result = await connector_service.search_items(provider, user_email, query, max_results=max_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Provider-specific endpoints for Slack
@router.get("/slack/channels")
async def list_slack_channels(
    user_email: str = Query(..., description="User email"),
    limit: int = Query(50, description="Maximum number of channels")
):
    """List Slack channels"""
    try:
        result = await connector_service.list_channels(user_email, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/slack/channels/{channel_id}/messages")
async def send_slack_message(
    channel_id: str = Path(..., description="Channel ID"),
    user_email: str = Query(..., description="User email"),
    message: str = Query(..., description="Message content"),
    thread_ts: Optional[str] = Query(None, description="Thread timestamp")
):
    """Send a message to a Slack channel"""
    try:
        result = await connector_service.send_message(user_email, channel_id, message, thread_ts=thread_ts)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Provider-specific endpoints for Jira
@router.get("/jira/projects")
async def list_jira_projects(
    user_email: str = Query(..., description="User email"),
    max_results: int = Query(50, description="Maximum number of projects")
):
    """List Jira projects"""
    try:
        result = await connector_service.list_projects(user_email, max_results=max_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/jira/projects/{project_id}/issues")
async def list_jira_issues(
    project_id: str = Path(..., description="Project ID"),
    user_email: str = Query(..., description="User email"),
    max_results: int = Query(50, description="Maximum number of issues")
):
    """List issues in a Jira project"""
    try:
        result = await connector_service.list_issues(user_email, project_id, max_results=max_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/jira/my-issues")
async def get_my_jira_issues(
    user_email: str = Query(..., description="User email"),
    max_results: int = Query(50, description="Maximum number of issues")
):
    """Get issues assigned to the current user in Jira"""
    try:
        result = await connector_service.get_my_issues(user_email, max_results=max_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Provider-specific endpoints for Gmail
@router.get("/gmail/emails")
async def list_gmail_emails(
    user_email: str = Query(..., description="User email"),
    max_results: int = Query(50, description="Maximum number of emails"),
    query: Optional[str] = Query(None, description="Search query")
):
    """List emails from Gmail"""
    try:
        result = await connector_service.list_emails(user_email, max_results=max_results, query=query)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/gmail/send")
async def send_gmail_email(
    user_email: str = Query(..., description="User email"),
    to: str = Query(..., description="Recipient email"),
    subject: str = Query(..., description="Email subject"),
    body: str = Query(..., description="Email body"),
    cc: Optional[str] = Query(None, description="CC recipients"),
    bcc: Optional[str] = Query(None, description="BCC recipients")
):
    """Send an email via Gmail"""
    try:
        email_data = {
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc,
            "bcc": bcc
        }
        result = await connector_service.send_email(user_email, email_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gmail/labels")
async def get_gmail_labels(user_email: str = Query(..., description="User email")):
    """Get Gmail labels"""
    try:
        result = await connector_service.get_labels(user_email)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Status endpoint
@router.get("/status")
async def get_unified_status():
    """Get unified API status"""
    return {
        "success": True,
        "service": "Unified API",
        "version": "1.0.0",
        "providers": ["google", "slack", "atlassian"],
        "connectors": connector_service.get_available_connectors(),
        "endpoints": [
            "/auth/{provider}/url",
            "/auth/{provider}/callback",
            "/auth/{provider}/validate",
            "/auth/{provider}/refresh",
            "/auth/{provider}/revoke",
            "/auth/status",
            "/auth/providers",
            "/connectors",
            "/connectors/{provider}/test",
            "/connectors/{provider}/capabilities",
            "/connectors/{provider}/items",
            "/connectors/{provider}/search",
            "/slack/channels",
            "/slack/channels/{channel_id}/messages",
            "/jira/projects",
            "/jira/projects/{project_id}/issues",
            "/jira/my-issues",
            "/gmail/emails",
            "/gmail/send",
            "/gmail/labels"
        ]
    } 
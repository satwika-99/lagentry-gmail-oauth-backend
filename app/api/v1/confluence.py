"""
Confluence API endpoints
Handles Confluence operations using the same Atlassian OAuth credentials
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any

from app.core.auth import validate_atlassian_config
from app.providers.atlassian.auth import atlassian_oauth
from app.services.connector_service import connector_service
from app.schemas.atlassian import (
    SpaceListResponse,
    SpaceDetailResponse,
    PageListResponse,
    PageDetailResponse,
    PageCreateRequest,
    PageUpdateRequest
)

router = APIRouter(prefix="/confluence", tags=["confluence"])


@router.get("/")
async def confluence_status():
    """Get Confluence integration status"""
    return {
        "success": True,
        "provider": "confluence",
        "configured": bool(True),  # Uses Atlassian OAuth
        "services": ["spaces", "pages", "content"],
        "endpoints": [
            "/auth/url",
            "/auth/callback",
            "/auth/validate",
            "/auth/revoke",
            "/spaces",
            "/pages",
            "/content"
        ]
    }


@router.get("")
async def confluence_status_no_slash():
    """Get Confluence integration status (no trailing slash)"""
    return {
        "success": True,
        "provider": "confluence",
        "configured": bool(True),  # Uses Atlassian OAuth
        "services": ["spaces", "pages", "content"],
        "endpoints": [
            "/auth/url",
            "/auth/callback",
            "/auth/validate",
            "/auth/revoke",
            "/spaces",
            "/pages",
            "/content"
        ]
    }


@router.get("/auth/url")
async def get_confluence_auth_url(
    state: Optional[str] = Query(None, description="State parameter for OAuth"),
    scopes: Optional[List[str]] = Query(None, description="Requested scopes")
):
    """Get Confluence OAuth URL (uses same Atlassian OAuth as Jira)"""
    try:
        validate_atlassian_config()
        
        # Use Confluence-specific redirect URI
        from app.core.config import settings
        from urllib.parse import urlencode
        
        client_id = settings.atlassian_client_id
        redirect_uri = settings.confluence_redirect_uri
        requested_scopes = scopes or ["read:confluence-content.all", "write:confluence-content", "read:confluence-space.summary", "read:confluence-user"]
        
        params = {
            "audience": "api.atlassian.com",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(requested_scopes),
            "response_type": "code",
            "prompt": "consent",
            "state": state or ""
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        auth_url = f"https://auth.atlassian.com/authorize?{query_string}"
        
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/auth/callback")
async def confluence_oauth_callback(
    code: str = Query(..., description="Authorization code"),
    state: str = Query("", description="State parameter")
):
    """Handle Confluence OAuth callback (uses same Atlassian OAuth as Jira)"""
    try:
        result = await atlassian_oauth.handle_callback(code, state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/auth/validate")
async def validate_confluence_tokens(user_email: str = Query(..., description="User email")):
    """Validate Confluence tokens (uses same Atlassian tokens as Jira)"""
    try:
        result = await atlassian_oauth.validate_tokens(user_email)
        return result
    except Exception as e:
        # Return error response instead of raising HTTPException
        return {
            "valid": False,
            "reason": f"Validation error: {str(e)}",
            "provider": "confluence"
        }


@router.get("/auth/revoke")
async def revoke_confluence_tokens(user_email: str = Query(..., description="User email")):
    """Revoke Confluence tokens (uses same Atlassian tokens as Jira)"""
    try:
        result = await atlassian_oauth.revoke_tokens(user_email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spaces", response_model=SpaceListResponse)
async def list_confluence_spaces(
    user_email: str = Query(..., description="User email"),
    start: int = Query(0, description="Start index"),
    limit: int = Query(50, description="Maximum number of spaces to return")
):
    """List available Confluence spaces"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.list_spaces(start=start, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spaces/{space_key}", response_model=SpaceDetailResponse)
async def get_confluence_space(
    space_key: str,
    user_email: str = Query(..., description="User email")
):
    """Get Confluence space details"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.get_space(space_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spaces/{space_key}/pages", response_model=PageListResponse)
async def list_confluence_pages(
    space_key: str,
    user_email: str = Query(..., description="User email"),
    start: int = Query(0, description="Start index"),
    limit: int = Query(50, description="Maximum number of pages to return")
):
    """List pages in a Confluence space"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.list_pages(space_key, start=start, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pages/{page_id}", response_model=PageDetailResponse)
async def get_confluence_page(
    page_id: str,
    user_email: str = Query(..., description="User email")
):
    """Get a specific Confluence page"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.get_page(page_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pages", response_model=PageDetailResponse)
async def create_confluence_page(
    request: PageCreateRequest,
    user_email: str = Query(..., description="User email")
):
    """Create a new Confluence page"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.create_page(
            request.space_key,
            {
                "title": request.title,
                "content": request.content,
                "parent_id": request.parent_id
            }
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/pages/{page_id}", response_model=PageDetailResponse)
async def update_confluence_page(
    page_id: str,
    request: PageUpdateRequest,
    user_email: str = Query(..., description="User email")
):
    """Update an existing Confluence page"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.update_item(
            page_id,
            {
                "title": request.title,
                "content": request.content,
                "version": request.version
            }
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_confluence_pages(
    query: str = Query(..., description="CQL search query"),
    user_email: str = Query(..., description="User email"),
    start: int = Query(0, description="Start index"),
    limit: int = Query(50, description="Maximum number of results to return")
):
    """Search Confluence pages using CQL"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.search_pages(query, start=start, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-pages", response_model=PageListResponse)
async def get_my_confluence_pages(
    user_email: str = Query(..., description="User email"),
    start: int = Query(0, description="Start index"),
    limit: int = Query(50, description="Maximum number of pages to return")
):
    """Get pages created by the current user"""
    try:
        connector = connector_service.get_connector("confluence", user_email)
        result = await connector.get_my_pages(start=start, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def confluence_status():
    """Get Confluence integration status"""
    return {
        "success": True,
        "provider": "confluence",
        "configured": bool(validate_atlassian_config()),
        "services": ["spaces", "pages", "search"],
        "endpoints": [
            "/auth/url",
            "/auth/callback", 
            "/auth/validate",
            "/auth/revoke",
            "/spaces",
            "/spaces/{space_key}",
            "/spaces/{space_key}/pages",
            "/pages/{page_id}",
            "/pages",
            "/search",
            "/my-pages"
        ]
    } 
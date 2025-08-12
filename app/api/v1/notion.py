"""
Notion API Endpoints
Handles Notion workspace operations (databases, pages, search, etc.)
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.database import db_manager
from app.core.exceptions import APIError, TokenError, AuthenticationException
from app.schemas.notion import (
    NotionAuthUrlResponse, NotionCallbackResponse, NotionServiceStatus,
    NotionDatabaseListResponse, NotionDatabaseResponse,
    NotionPageListResponse, NotionPageResponse, NotionBlockListResponse,
    NotionUserResponse
)
from app.connectors.notion.oauth import get_auth_url, exchange_code_for_token
from app.connectors.notion.api_client import NotionAPIClient
from app.core.config import settings

router = APIRouter(prefix="/notion", tags=["Notion Services"])


@router.get("/")
async def notion_status():
    """Get Notion integration status"""
    return {
        "success": True,
        "provider": "notion",
        "configured": bool(settings.notion_client_id),
        "services": ["databases", "pages", "blocks", "users"],
        "endpoints": [
            "/auth-url",
            "/callback",
            "/databases",
            "/pages",
            "/blocks",
            "/users"
        ]
    }


@router.get("")
async def notion_status_no_slash():
    """Get Notion integration status (no trailing slash)"""
    return {
        "success": True,
        "provider": "notion",
        "configured": bool(settings.notion_client_id),
        "services": ["databases", "pages", "blocks", "users"],
        "endpoints": [
            "/auth-url",
            "/callback",
            "/databases",
            "/pages",
            "/blocks",
            "/users"
        ]
    }


@router.get("/auth-url", response_model=NotionAuthUrlResponse)
def notion_auth_url(user_email: str = Query(..., description="User email")):
    """Get Notion OAuth URL"""
    try:
        return {"auth_url": get_auth_url(user_email)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/callback", response_model=NotionCallbackResponse)
async def notion_callback(code: str = Query(...), state: str = Query(...)):
    """Handle Notion OAuth callback and store tokens"""
    try:
        token_data = await exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = int(token_data.get("expires_in", 3600))
        scopes = token_data.get("scope", "").split()
        user_email = state
        
        db_manager.store_tokens(user_email, "notion", access_token, refresh_token, expires_in, scopes)
        return {"success": True, "token_data": token_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Database Operations
@router.get("/databases", response_model=NotionDatabaseListResponse)
async def search_databases(
    user_email: str = Query(..., description="User email"),
    query: str = Query("", description="Search query"),
    page_size: int = Query(100, description="Number of results per page")
):
    """Search for databases"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.search_databases(query=query, page_size=page_size)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "databases": [],
            "total": 0,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "databases": [],
            "total": 0,
            "message": f"Error: {str(e)}"
        }

@router.get("/databases/{database_id}", response_model=NotionDatabaseResponse)
async def get_database(
    database_id: str = Path(..., description="Database ID"),
    user_email: str = Query(..., description="User email")
):
    """Get a specific database"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.get_database(database_id)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "database": None,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "database": None,
            "message": f"Error: {str(e)}"
        }

@router.get("/databases/{database_id}/query", response_model=NotionPageListResponse)
async def query_database(
    database_id: str = Path(..., description="Database ID"),
    user_email: str = Query(..., description="User email"),
    page_size: int = Query(100, description="Number of results per page"),
    filter: Optional[str] = Query(None, description="Filter criteria (JSON string)"),
    sorts: Optional[str] = Query(None, description="Sort criteria (JSON string)")
):
    """Query a database for pages"""
    try:
        client = NotionAPIClient(user_email)
        
        # Parse optional parameters
        filter_data = None
        sorts_data = None
        
        if filter:
            import json
            filter_data = json.loads(filter)
        
        if sorts:
            import json
            sorts_data = json.loads(sorts)
        
        result = await client.query_database(
            database_id, 
            page_size=page_size,
            filter=filter_data,
            sorts=sorts_data
        )
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "pages": [],
            "total": 0,
            "has_more": False,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "pages": [],
            "total": 0,
            "has_more": False,
            "message": f"Error: {str(e)}"
        }

# Page Operations
@router.get("/pages", response_model=NotionPageListResponse)
async def search_pages(
    user_email: str = Query(..., description="User email"),
    query: str = Query("", description="Search query"),
    page_size: int = Query(100, description="Number of results per page")
):
    """Search for pages"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.search_pages(query=query, page_size=page_size)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "pages": [],
            "total": 0,
            "query": query,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "pages": [],
            "total": 0,
            "query": query,
            "message": f"Error: {str(e)}"
        }

@router.get("/pages/{page_id}", response_model=NotionPageResponse)
async def get_page(
    page_id: str = Path(..., description="Page ID"),
    user_email: str = Query(..., description="User email")
):
    """Get a specific page"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.get_page(page_id)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "page": None,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "page": None,
            "message": f"Error: {str(e)}"
        }

@router.get("/pages/{page_id}/content", response_model=NotionBlockListResponse)
async def get_page_content(
    page_id: str = Path(..., description="Page ID"),
    user_email: str = Query(..., description="User email")
):
    """Get page content (blocks)"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.get_page_content(page_id)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "blocks": [],
            "total": 0,
            "has_more": False,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "blocks": [],
            "total": 0,
            "has_more": False,
            "message": f"Error: {str(e)}"
        }

@router.post("/pages", response_model=NotionPageResponse)
async def create_page(
    user_email: str = Query(..., description="User email"),
    page_data: Dict[str, Any] = Body(..., description="Page data")
):
    """Create a new page"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.create_page(page_data)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "page": None,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "page": None,
            "message": f"Error: {str(e)}"
        }

@router.patch("/pages/{page_id}", response_model=NotionPageResponse)
async def update_page(
    page_id: str = Path(..., description="Page ID"),
    user_email: str = Query(..., description="User email"),
    page_data: Dict[str, Any] = Body(..., description="Page update data")
):
    """Update an existing page"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.update_page(page_id, page_data)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "page": None,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "page": None,
            "message": f"Error: {str(e)}"
        }

@router.delete("/pages/{page_id}")
async def delete_page(
    page_id: str = Path(..., description="Page ID"),
    user_email: str = Query(..., description="User email")
):
    """Delete a page (archive it)"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.delete_page(page_id)
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

# User Operations
@router.get("/user", response_model=NotionUserResponse)
async def get_user(user_email: str = Query(..., description="User email")):
    """Get current user information"""
    try:
        client = NotionAPIClient(user_email)
        result = await client.get_user()
        return result
    except AuthenticationException as e:
        return {
            "success": True,
            "user": None,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "user": None,
            "message": f"Error: {str(e)}"
        }

# Service Status
@router.get("/status", response_model=NotionServiceStatus)
async def get_notion_status(user_email: str = Query(..., description="User email")):
    """Get Notion service status"""
    try:
        # Check if user has valid Notion tokens
        tokens = db_manager.get_valid_tokens(user_email, "notion")
        
        return {
            "success": True,
            "provider": "notion",
            "connected": bool(tokens),
            "services": {
                "databases": "implemented",
                "pages": "implemented",
                "search": "implemented",
                "blocks": "implemented",
                "user": "implemented"
            },
            "message": "Notion services are fully implemented and ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

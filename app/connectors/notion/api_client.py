"""
Notion API Client
Handles all Notion API operations (databases, pages, search, etc.)
"""

import httpx
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.core.database import db_manager
from app.core.exceptions import ConnectorError, AuthenticationException

class NotionAPIClient:
    """Notion API client for database and page operations"""
    
    def __init__(self, user_email: str):
        self.user_email = user_email
        self.base_url = "https://api.notion.com/v1"
        self.headers = self._get_headers()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get Notion API headers with authentication"""
        tokens = db_manager.get_valid_tokens(self.user_email, "notion")
        if not tokens:
            raise AuthenticationException("No valid Notion tokens found. Please authenticate first.")
        
        return {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    async def search_databases(self, query: str = "", **kwargs) -> Dict[str, Any]:
        """Search for databases"""
        try:
            url = f"{self.base_url}/search"
            data = {
                "filter": {"property": "object", "value": "database"},
                "query": query,
                "page_size": kwargs.get("page_size", 100)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                result = response.json()
            
            databases = []
            for db in result.get("results", []):
                databases.append({
                    "id": db.get("id"),
                    "title": _extract_title(db.get("title", [])),
                    "description": _extract_rich_text(db.get("description", [])),
                    "url": db.get("url"),
                    "created_time": db.get("created_time"),
                    "last_edited_time": db.get("last_edited_time")
                })
            
            return {
                "success": True,
                "databases": databases,
                "total": len(databases)
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error searching databases: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error searching databases: {str(e)}")
    
    async def get_database(self, database_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific database"""
        try:
            url = f"{self.base_url}/databases/{database_id}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                db = response.json()
            
            return {
                "success": True,
                "database": {
                    "id": db.get("id"),
                    "title": _extract_title(db.get("title", [])),
                    "description": _extract_rich_text(db.get("description", [])),
                    "url": db.get("url"),
                    "properties": db.get("properties", {}),
                    "created_time": db.get("created_time"),
                    "last_edited_time": db.get("last_edited_time")
                }
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error getting database: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error getting database: {str(e)}")
    
    async def query_database(self, database_id: str, **kwargs) -> Dict[str, Any]:
        """Query a database for pages"""
        try:
            url = f"{self.base_url}/databases/{database_id}/query"
            
            # Build query parameters
            query_data = {
                "page_size": kwargs.get("page_size", 100)
            }
            
            # Add filters if provided
            if "filter" in kwargs:
                query_data["filter"] = kwargs["filter"]
            
            # Add sorts if provided
            if "sorts" in kwargs:
                query_data["sorts"] = kwargs["sorts"]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=query_data, headers=self.headers)
                response.raise_for_status()
                result = response.json()
            
            pages = []
            for page in result.get("results", []):
                pages.append({
                    "id": page.get("id"),
                    "title": _extract_title(page.get("properties", {}).get("title", {}).get("title", [])),
                    "url": page.get("url"),
                    "created_time": page.get("created_time"),
                    "last_edited_time": page.get("last_edited_time"),
                    "properties": page.get("properties", {})
                })
            
            return {
                "success": True,
                "pages": pages,
                "total": len(pages),
                "has_more": result.get("has_more", False),
                "next_cursor": result.get("next_cursor")
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error querying database: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error querying database: {str(e)}")
    
    async def get_page(self, page_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific page"""
        try:
            url = f"{self.base_url}/pages/{page_id}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                page = response.json()
            
            return {
                "success": True,
                "page": {
                    "id": page.get("id"),
                    "title": _extract_title(page.get("properties", {}).get("title", {}).get("title", [])),
                    "url": page.get("url"),
                    "created_time": page.get("created_time"),
                    "last_edited_time": page.get("last_edited_time"),
                    "properties": page.get("properties", {}),
                    "parent": page.get("parent", {})
                }
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error getting page: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error getting page: {str(e)}")
    
    async def get_page_content(self, page_id: str, **kwargs) -> Dict[str, Any]:
        """Get page content (blocks)"""
        try:
            url = f"{self.base_url}/blocks/{page_id}/children"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
            
            blocks = []
            for block in result.get("results", []):
                blocks.append({
                    "id": block.get("id"),
                    "type": block.get("type"),
                    "content": block.get(block.get("type", {}), {}),
                    "has_children": block.get("has_children", False),
                    "created_time": block.get("created_time"),
                    "last_edited_time": block.get("last_edited_time")
                })
            
            return {
                "success": True,
                "blocks": blocks,
                "total": len(blocks),
                "has_more": result.get("has_more", False),
                "next_cursor": result.get("next_cursor")
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error getting page content: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error getting page content: {str(e)}")
    
    async def create_page(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create a new page"""
        try:
            url = f"{self.base_url}/pages"
            
            # Ensure required fields
            if "parent" not in data:
                raise ConnectorError("Parent database or page ID is required")
            
            if "properties" not in data:
                raise ConnectorError("Page properties are required")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                page = response.json()
            
            return {
                "success": True,
                "page": {
                    "id": page.get("id"),
                    "title": _extract_title(page.get("properties", {}).get("title", {}).get("title", [])),
                    "url": page.get("url"),
                    "created_time": page.get("created_time"),
                    "last_edited_time": page.get("last_edited_time")
                }
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error creating page: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error creating page: {str(e)}")
    
    async def update_page(self, page_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an existing page"""
        try:
            url = f"{self.base_url}/pages/{page_id}"
            
            async with httpx.AsyncClient() as client:
                response = await client.patch(url, json=data, headers=self.headers)
                response.raise_for_status()
                page = response.json()
            
            return {
                "success": True,
                "page": {
                    "id": page.get("id"),
                    "title": _extract_title(page.get("properties", {}).get("title", {}).get("title", [])),
                    "url": page.get("url"),
                    "last_edited_time": page.get("last_edited_time")
                }
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error updating page: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error updating page: {str(e)}")
    
    async def delete_page(self, page_id: str, **kwargs) -> Dict[str, Any]:
        """Delete a page (archive it)"""
        try:
            url = f"{self.base_url}/pages/{page_id}"
            data = {"archived": True}
            
            async with httpx.AsyncClient() as client:
                response = await client.patch(url, json=data, headers=self.headers)
                response.raise_for_status()
            
            return {
                "success": True,
                "message": f"Page {page_id} archived successfully"
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error deleting page: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error deleting page: {str(e)}")
    
    async def search_pages(self, query: str = "", **kwargs) -> Dict[str, Any]:
        """Search for pages"""
        try:
            url = f"{self.base_url}/search"
            data = {
                "query": query,
                "filter": {"property": "object", "value": "page"},
                "page_size": kwargs.get("page_size", 100)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                result = response.json()
            
            pages = []
            for page in result.get("results", []):
                pages.append({
                    "id": page.get("id"),
                    "title": _extract_title(page.get("properties", {}).get("title", {}).get("title", [])),
                    "url": page.get("url"),
                    "created_time": page.get("created_time"),
                    "last_edited_time": page.get("last_edited_time"),
                    "parent": page.get("parent", {})
                })
            
            return {
                "success": True,
                "pages": pages,
                "total": len(pages),
                "query": query
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error searching pages: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error searching pages: {str(e)}")
    
    async def get_user(self, **kwargs) -> Dict[str, Any]:
        """Get current user information"""
        try:
            url = f"{self.base_url}/users/me"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                user = response.json()
            
            return {
                "success": True,
                "user": {
                    "id": user.get("id"),
                    "name": user.get("name"),
                    "avatar_url": user.get("avatar_url"),
                    "type": user.get("type"),
                    "person": user.get("person", {})
                }
            }
        except httpx.HTTPStatusError as e:
            raise ConnectorError(f"Notion API error getting user: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ConnectorError(f"Notion API error getting user: {str(e)}")

# Helper functions for extracting Notion content
def _extract_title(title_array: List[Dict]) -> str:
    """Extract plain text from Notion title array"""
    if not title_array:
        return "Untitled"
    return "".join([item.get("plain_text", "") for item in title_array])

def _extract_rich_text(rich_text_array: List[Dict]) -> str:
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])

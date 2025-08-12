"""
Confluence Connector Implementation
Handles Confluence operations using the modular connector pattern
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime

from connectors.base import DataConnector
from core.database import db_manager
from core.exceptions import ConnectorError, TokenError
from providers.atlassian.auth import atlassian_oauth


class ConfluenceConnector(DataConnector):
    """Confluence connector for page and space operations"""
    
    def __init__(self, user_email: str):
        super().__init__("atlassian", user_email)
        self.api_base_url = "https://api.atlassian.com/ex/confluence"
        self.oauth_provider = atlassian_oauth
    
    async def connect(self) -> bool:
        """Establish connection to Confluence API"""
        try:
            tokens = self._get_tokens()
            if not tokens:
                raise ConnectorError("No valid Confluence tokens found")
            
            # Test connection with user info
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/rest/api/user/current", headers=headers)
                if response.status_code == 200:
                    self._log_activity("connected")
                    return True
                else:
                    raise ConnectorError("Failed to connect to Confluence API")
                    
        except Exception as e:
            self._log_activity("connection_failed", {"error": str(e)})
            raise ConnectorError(f"Confluence connection failed: {str(e)}")
    
    async def disconnect(self) -> bool:
        """Disconnect from Confluence API"""
        self._log_activity("disconnected")
        return True
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Confluence API connection"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/rest/api/user/current", headers=headers)
                
                if response.status_code == 200:
                    user_info = response.json()
                    return {
                        "connected": True,
                        "user_id": user_info.get("userKey"),
                        "user_name": user_info.get("displayName"),
                        "email": user_info.get("email"),
                        "active": user_info.get("active", False)
                    }
                else:
                    return {"connected": False, "error": "API call failed"}
                    
        except Exception as e:
            return {"connected": False, "error": str(e)}
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get Confluence API capabilities"""
        return {
            "provider": "confluence",
            "capabilities": [
                "list_spaces",
                "get_space",
                "list_pages",
                "get_page",
                "create_page",
                "update_page",
                "search_pages",
                "get_my_pages"
            ],
            "scopes": [
                "read:confluence-content",
                "write:confluence-content",
                "read:confluence-space",
                "write:confluence-space"
            ]
        }
    
    async def list_spaces(self, **kwargs) -> Dict[str, Any]:
        """List available Confluence spaces"""
        try:
            start = kwargs.get("start", 0)
            limit = kwargs.get("limit", 50)
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_spaces = [
                    {
                        "id": 10001,
                        "key": "DEMO",
                        "name": "Demo Space",
                        "type": "global",
                        "status": "current"
                    },
                    {
                        "id": 10002,
                        "key": "TEST",
                        "name": "Test Space",
                        "type": "global",
                        "status": "current"
                    },
                    {
                        "id": 10003,
                        "key": "DEV",
                        "name": "Development Space",
                        "type": "global",
                        "status": "current"
                    }
                ]
                
                self._log_activity("list_spaces", {"count": len(mock_spaces), "mock": True})
                return {
                    "success": True,
                    "spaces": mock_spaces,
                    "total": len(mock_spaces),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real spaces"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "start": start,
                "limit": limit
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/space",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    spaces = data.get("results", [])
                    self._log_activity("list_spaces", {"count": len(spaces)})
                    return {
                        "success": True,
                        "spaces": spaces,
                        "total": len(spaces),
                        "start": start,
                        "limit": limit
                    }
                else:
                    raise ConnectorError(f"Failed to list spaces: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_spaces_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list spaces: {str(e)}")
    
    async def get_space(self, space_key: str, **kwargs) -> Dict[str, Any]:
        """Get space details"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/space/{space_key}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    space = response.json()
                    self._log_activity("get_space", {"space_key": space_key})
                    return {
                        "success": True,
                        "space": space
                    }
                else:
                    raise ConnectorError(f"Failed to get space: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_space_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get space: {str(e)}")
    
    async def list_pages(self, space_key: str, **kwargs) -> Dict[str, Any]:
        """List pages in a space"""
        try:
            start = kwargs.get("start", 0)
            limit = kwargs.get("limit", 50)
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_pages = [
                    {
                        "id": "10001",
                        "title": "Welcome to Demo Space",
                        "type": "page",
                        "status": "current",
                        "space": {"key": space_key, "name": f"{space_key} Space"},
                        "created": "2024-01-01T10:00:00.000Z",
                        "updated": "2024-01-01T10:00:00.000Z"
                    },
                    {
                        "id": "10002",
                        "title": "Getting Started Guide",
                        "type": "page",
                        "status": "current",
                        "space": {"key": space_key, "name": f"{space_key} Space"},
                        "created": "2024-01-01T11:00:00.000Z",
                        "updated": "2024-01-01T11:00:00.000Z"
                    }
                ]
                
                self._log_activity("list_pages", {"space_key": space_key, "count": len(mock_pages), "mock": True})
                return {
                    "success": True,
                    "pages": mock_pages,
                    "total": len(mock_pages),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real pages"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "spaceKey": space_key,
                "start": start,
                "limit": limit,
                "expand": "space"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/content",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    pages = data.get("results", [])
                    self._log_activity("list_pages", {"space_key": space_key, "count": len(pages)})
                    return {
                        "success": True,
                        "pages": pages,
                        "total": len(pages),
                        "start": start,
                        "limit": limit
                    }
                else:
                    raise ConnectorError(f"Failed to list pages: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_pages_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list pages: {str(e)}")
    
    async def create_page(self, space_key: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create a new page"""
        try:
            title = data.get("title")
            content = data.get("content")
            parent_id = data.get("parent_id")
            
            if not title or not content:
                raise ConnectorError("Title and content are required")
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_page = {
                    "id": "10001",
                    "title": title,
                    "type": "page",
                    "status": "current",
                    "space": {"key": space_key, "name": f"{space_key} Space"},
                    "body": {"storage": {"value": content}},
                    "created": "2024-01-01T10:00:00.000Z",
                    "updated": "2024-01-01T10:00:00.000Z"
                }
                
                self._log_activity("create_page", {
                    "space_key": space_key,
                    "title": title,
                    "mock": True
                })
                return {
                    "success": True,
                    "page": mock_page,
                    "mock_data": True,
                    "message": "Mock data - authenticate to create real pages"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}", "Content-Type": "application/json"}
            
            page_data = {
                "type": "page",
                "title": title,
                "space": {"key": space_key},
                "body": {
                    "storage": {
                        "value": content,
                        "representation": "storage"
                    }
                }
            }
            
            if parent_id:
                page_data["ancestors"] = [{"id": parent_id}]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/rest/api/content",
                    headers=headers,
                    json=page_data
                )
                
                if response.status_code == 200:
                    page = response.json()
                    self._log_activity("create_page", {
                        "space_key": space_key,
                        "title": title
                    })
                    return {
                        "success": True,
                        "page": page
                    }
                else:
                    raise ConnectorError(f"Failed to create page: {response.text}")
                    
        except Exception as e:
            self._log_activity("create_page_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to create page: {str(e)}")
    
    async def get_page(self, page_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific page"""
        try:
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_page = {
                    "id": page_id,
                    "title": f"Mock Page - {page_id}",
                    "type": "page",
                    "status": "current",
                    "space": {"key": "DEMO", "name": "Demo Space"},
                    "body": {"storage": {"value": "This is a mock page created for testing purposes."}},
                    "created": "2024-01-01T10:00:00.000Z",
                    "updated": "2024-01-01T10:00:00.000Z"
                }
                
                self._log_activity("get_page", {"page_id": page_id, "mock": True})
                return {
                    "success": True,
                    "page": mock_page,
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real pages"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {"expand": "body.storage,space"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/content/{page_id}",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    page = response.json()
                    self._log_activity("get_page", {"page_id": page_id})
                    return {
                        "success": True,
                        "page": page
                    }
                else:
                    raise ConnectorError(f"Failed to get page: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_page_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get page: {str(e)}")
    
    async def search_pages(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search pages using CQL"""
        try:
            start = kwargs.get("start", 0)
            limit = kwargs.get("limit", 50)
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_pages = [
                    {
                        "id": "10001",
                        "title": "Mock Search Result 1",
                        "type": "page",
                        "status": "current",
                        "space": {"key": "DEMO", "name": "Demo Space"},
                        "created": "2024-01-01T10:00:00.000Z",
                        "updated": "2024-01-01T10:00:00.000Z"
                    },
                    {
                        "id": "10002",
                        "title": "Mock Search Result 2",
                        "type": "page",
                        "status": "current",
                        "space": {"key": "DEMO", "name": "Demo Space"},
                        "created": "2024-01-01T11:00:00.000Z",
                        "updated": "2024-01-01T11:00:00.000Z"
                    }
                ]
                
                self._log_activity("search_pages", {"query": query, "count": len(mock_pages), "mock": True})
                return {
                    "success": True,
                    "pages": mock_pages,
                    "total": len(mock_pages),
                    "query": query,
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real search results"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "cql": query,
                "start": start,
                "limit": limit,
                "expand": "space"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/content/search",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    pages = data.get("results", [])
                    self._log_activity("search_pages", {"query": query, "count": len(pages)})
                    return {
                        "success": True,
                        "pages": pages,
                        "total": len(pages),
                        "query": query
                    }
                else:
                    raise ConnectorError(f"Failed to search pages: {response.text}")
                    
        except Exception as e:
            self._log_activity("search_pages_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to search pages: {str(e)}")
    
    async def get_my_pages(self, **kwargs) -> Dict[str, Any]:
        """Get pages created by the current user"""
        try:
            start = kwargs.get("start", 0)
            limit = kwargs.get("limit", 50)
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_pages = [
                    {
                        "id": "10001",
                        "title": "My Test Page 1",
                        "type": "page",
                        "status": "current",
                        "space": {"key": "DEMO", "name": "Demo Space"},
                        "created": "2024-01-01T10:00:00.000Z",
                        "updated": "2024-01-01T10:00:00.000Z"
                    },
                    {
                        "id": "10002",
                        "title": "My Test Page 2",
                        "type": "page",
                        "status": "current",
                        "space": {"key": "TEST", "name": "Test Space"},
                        "created": "2024-01-01T11:00:00.000Z",
                        "updated": "2024-01-01T11:00:00.000Z"
                    }
                ]
                
                self._log_activity("get_my_pages", {"count": len(mock_pages), "mock": True})
                return {
                    "success": True,
                    "pages": mock_pages,
                    "total": len(mock_pages),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real pages"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "type": "page",
                "start": start,
                "limit": limit,
                "expand": "space"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/content",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    pages = data.get("results", [])
                    self._log_activity("get_my_pages", {"count": len(pages)})
                    return {
                        "success": True,
                        "pages": pages,
                        "total": len(pages),
                        "start": start,
                        "limit": limit
                    }
                else:
                    raise ConnectorError(f"Failed to get my pages: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_my_pages_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get my pages: {str(e)}")
    
    # Required methods from DataConnector
    async def list_items(self, **kwargs) -> Dict[str, Any]:
        """List items (pages) from Confluence"""
        space_key = kwargs.get("space_key")
        if space_key:
            return await self.list_pages(space_key, **kwargs)
        else:
            return await self.get_my_pages(**kwargs)
    
    async def get_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific item (page) from Confluence"""
        return await self.get_page(item_id, **kwargs)
    
    async def create_item(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create an item (page) in Confluence"""
        space_key = data.get("space_key")
        if not space_key:
            raise ConnectorError("space_key is required")
        return await self.create_page(space_key, data, **kwargs)
    
    async def update_item(self, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an item (page) in Confluence"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}", "Content-Type": "application/json"}
            
            update_data = {
                "version": {"number": data.get("version", 1)},
                "title": data.get("title"),
                "type": "page",
                "body": {
                    "storage": {
                        "value": data.get("content", ""),
                        "representation": "storage"
                    }
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.api_base_url}/rest/api/content/{item_id}",
                    headers=headers,
                    json=update_data
                )
                
                if response.status_code == 200:
                    page = response.json()
                    self._log_activity("update_page", {"page_id": item_id})
                    return {
                        "success": True,
                        "page": page
                    }
                else:
                    raise ConnectorError(f"Failed to update page: {response.text}")
                    
        except Exception as e:
            self._log_activity("update_page_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to update page: {str(e)}")
    
    async def delete_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Delete an item (page) in Confluence - not supported"""
        raise ConnectorError("Page deletion not supported in Confluence")
    
    async def search_items(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for items (pages) in Confluence"""
        return await self.search_pages(query, **kwargs) 
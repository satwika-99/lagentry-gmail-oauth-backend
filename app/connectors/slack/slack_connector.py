"""
Slack Connector Implementation
Handles Slack operations using the modular connector pattern
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime

from connectors.base import CommunicationConnector
from core.database import db_manager
from core.exceptions import ConnectorError, TokenError
from providers.slack.auth import slack_provider


class SlackConnector(CommunicationConnector):
    """Slack connector for channel and message operations"""
    
    def __init__(self, user_email: str):
        super().__init__("slack", user_email)
        self.api_base_url = "https://slack.com/api"
        self.oauth_provider = slack_provider
    
    async def connect(self) -> bool:
        """Establish connection to Slack API"""
        try:
            tokens = self._get_tokens()
            if not tokens:
                raise ConnectorError("No valid Slack tokens found")
            
            # Test connection with auth.test
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_base_url}/auth.test", headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        self._log_activity("connected")
                        return True
                    else:
                        raise ConnectorError("Slack API authentication failed")
                else:
                    raise ConnectorError("Failed to connect to Slack API")
                    
        except Exception as e:
            self._log_activity("connection_failed", {"error": str(e)})
            raise ConnectorError(f"Slack connection failed: {str(e)}")
    
    async def disconnect(self) -> bool:
        """Disconnect from Slack API"""
        self._log_activity("disconnected")
        return True
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Slack API connection"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_base_url}/auth.test", headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        return {
                            "connected": True,
                            "user_id": result.get("user_id"),
                            "user_name": result.get("user"),
                            "team_id": result.get("team_id"),
                            "team_name": result.get("team")
                        }
                    else:
                        return {"connected": False, "error": "Authentication failed"}
                else:
                    return {"connected": False, "error": "API call failed"}
                    
        except Exception as e:
            return {"connected": False, "error": str(e)}
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get Slack API capabilities"""
        return {
            "provider": "slack",
            "capabilities": [
                "list_channels",
                "get_channel",
                "list_messages",
                "send_message",
                "get_message",
                "search_messages",
                "list_users",
                "get_user"
            ],
            "scopes": [
                "channels:read",
                "channels:history",
                "channels:write",
                "chat:write",
                "chat:write.public",
                "users:read",
                "users:read.email"
            ]
        }
    
    async def list_channels(self, **kwargs) -> Dict[str, Any]:
        """List available Slack channels"""
        try:
            limit = kwargs.get("limit", 50)
            exclude_archived = kwargs.get("exclude_archived", True)
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_channels = [
                    {
                        "id": "C1234567890",
                        "name": "general",
                        "is_channel": True,
                        "is_private": False,
                        "is_archived": False,
                        "num_members": 15
                    },
                    {
                        "id": "C1234567891", 
                        "name": "random",
                        "is_channel": True,
                        "is_private": False,
                        "is_archived": False,
                        "num_members": 8
                    },
                    {
                        "id": "C1234567892",
                        "name": "announcements",
                        "is_channel": True,
                        "is_private": False,
                        "is_archived": False,
                        "num_members": 25
                    }
                ]
                
                self._log_activity("list_channels", {"count": len(mock_channels), "mock": True})
                return {
                    "success": True,
                    "channels": mock_channels,
                    "total": len(mock_channels),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real channels"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "limit": limit,
                "exclude_archived": exclude_archived
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/conversations.list",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        channels = data.get("channels", [])
                        self._log_activity("list_channels", {"count": len(channels)})
                        return {
                            "success": True,
                            "channels": channels,
                            "total": len(channels),
                            "next_cursor": data.get("response_metadata", {}).get("next_cursor")
                        }
                    else:
                        raise ConnectorError(f"Slack API error: {data.get('error')}")
                else:
                    raise ConnectorError(f"Failed to list channels: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_channels_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list channels: {str(e)}")
    
    async def get_channel(self, channel_id: str, **kwargs) -> Dict[str, Any]:
        """Get channel details"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {"channel": channel_id}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/conversations.info",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        channel = data.get("channel", {})
                        self._log_activity("get_channel", {"channel_id": channel_id})
                        return {
                            "success": True,
                            "channel": channel
                        }
                    else:
                        raise ConnectorError(f"Slack API error: {data.get('error')}")
                else:
                    raise ConnectorError(f"Failed to get channel: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_channel_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get channel: {str(e)}")
    
    async def list_messages(self, channel_id: str, **kwargs) -> Dict[str, Any]:
        """List messages in a channel"""
        try:
            limit = kwargs.get("limit", 50)
            oldest = kwargs.get("oldest")
            latest = kwargs.get("latest")
            
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "channel": channel_id,
                "limit": limit
            }
            
            if oldest:
                params["oldest"] = oldest
            if latest:
                params["latest"] = latest
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/conversations.history",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        messages = data.get("messages", [])
                        self._log_activity("list_messages", {
                            "channel_id": channel_id,
                            "count": len(messages)
                        })
                        return {
                            "success": True,
                            "messages": messages,
                            "total": len(messages),
                            "has_more": data.get("has_more", False)
                        }
                    else:
                        raise ConnectorError(f"Slack API error: {data.get('error')}")
                else:
                    raise ConnectorError(f"Failed to list messages: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_messages_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list messages: {str(e)}")
    
    async def send_message(self, channel_id: str, message: str, **kwargs) -> Dict[str, Any]:
        """Send a message to a channel"""
        try:
            thread_ts = kwargs.get("thread_ts")
            
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            data = {
                "channel": channel_id,
                "text": message
            }
            
            if thread_ts:
                data["thread_ts"] = thread_ts
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/chat.postMessage",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        self._log_activity("send_message", {
                            "channel_id": channel_id,
                            "message_ts": result.get("ts")
                        })
                        return {
                            "success": True,
                            "ts": result.get("ts"),
                            "channel": result.get("channel"),
                            "message": result.get("message", {})
                        }
                    else:
                        raise ConnectorError(f"Slack API error: {result.get('error')}")
                else:
                    raise ConnectorError(f"Failed to send message: {response.text}")
                    
        except Exception as e:
            self._log_activity("send_message_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to send message: {str(e)}")
    
    async def get_message(self, message_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific message"""
        try:
            channel_id = kwargs.get("channel_id")
            if not channel_id:
                raise ConnectorError("channel_id is required to get a message")
            
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "channel": channel_id,
                "latest": message_id,
                "limit": 1,
                "inclusive": True
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/conversations.history",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        messages = data.get("messages", [])
                        if messages:
                            message = messages[0]
                            self._log_activity("get_message", {"message_id": message_id})
                            return {
                                "success": True,
                                "message": message
                            }
                        else:
                            raise ConnectorError("Message not found")
                    else:
                        raise ConnectorError(f"Slack API error: {data.get('error')}")
                else:
                    raise ConnectorError(f"Failed to get message: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_message_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get message: {str(e)}")
    
    async def search_messages(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for messages across channels"""
        try:
            count = kwargs.get("count", 20)
            sort = kwargs.get("sort", "timestamp")
            sort_dir = kwargs.get("sort_dir", "desc")
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_messages = [
                    {
                        "type": "message",
                        "user": "U1234567890",
                        "text": f"Mock message containing: {query}",
                        "ts": "1640995200.000000",
                        "channel": {
                            "id": "C1234567890",
                            "name": "general"
                        }
                    },
                    {
                        "type": "message",
                        "user": "U0987654321",
                        "text": f"Another mock message with: {query}",
                        "ts": "1640995200.000000",
                        "channel": {
                            "id": "C1234567890",
                            "name": "general"
                        }
                    }
                ]
                
                self._log_activity("search_messages", {"query": query, "count": len(mock_messages), "mock": True})
                return {
                    "success": True,
                    "messages": mock_messages,
                    "total": len(mock_messages),
                    "query": query,
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real search results"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "query": query,
                "count": count,
                "sort": sort,
                "sort_dir": sort_dir
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/search.messages",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        messages = data.get("messages", {}).get("matches", [])
                        self._log_activity("search_messages", {
                            "query": query,
                            "count": len(messages)
                        })
                        return {
                            "success": True,
                            "messages": messages,
                            "total": len(messages),
                            "query": query
                        }
                    else:
                        raise ConnectorError(f"Slack API error: {data.get('error')}")
                else:
                    raise ConnectorError(f"Failed to search messages: {response.text}")
                    
        except Exception as e:
            self._log_activity("search_messages_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to search messages: {str(e)}")
    
    async def list_users(self, **kwargs) -> Dict[str, Any]:
        """List Slack users"""
        try:
            limit = kwargs.get("limit", 50)
            cursor = kwargs.get("cursor")
            
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {"limit": limit}
            if cursor:
                params["cursor"] = cursor
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/users.list",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        users = data.get("members", [])
                        self._log_activity("list_users", {"count": len(users)})
                        return {
                            "success": True,
                            "users": users,
                            "total": len(users),
                            "next_cursor": data.get("response_metadata", {}).get("next_cursor")
                        }
                    else:
                        raise ConnectorError(f"Slack API error: {data.get('error')}")
                else:
                    raise ConnectorError(f"Failed to list users: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_users_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list users: {str(e)}")
    
    async def get_user(self, user_id: str, **kwargs) -> Dict[str, Any]:
        """Get user details"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {"user": user_id}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/users.info",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        user = data.get("user", {})
                        self._log_activity("get_user", {"user_id": user_id})
                        return {
                            "success": True,
                            "user": user
                        }
                    else:
                        raise ConnectorError(f"Slack API error: {data.get('error')}")
                else:
                    raise ConnectorError(f"Failed to get user: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_user_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get user: {str(e)}")
    
    # Required methods from BaseConnector
    async def list_items(self, **kwargs) -> Dict[str, Any]:
        """List items (messages) from Slack"""
        return await self.search_messages("", **kwargs)
    
    async def get_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific item (message) from Slack"""
        return await self.get_message(item_id, **kwargs)
    
    async def create_item(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create an item (send message) in Slack"""
        channel_id = data.get("channel_id")
        message = data.get("message")
        if not channel_id or not message:
            raise ConnectorError("channel_id and message are required")
        return await self.send_message(channel_id, message, **kwargs)
    
    async def update_item(self, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an item (message) in Slack - not supported"""
        raise ConnectorError("Message updates not supported in Slack")
    
    async def delete_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Delete an item (message) in Slack - not supported"""
        raise ConnectorError("Message deletion not supported in Slack")
    
    async def search_items(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for items (messages) in Slack"""
        return await self.search_messages(query, **kwargs) 
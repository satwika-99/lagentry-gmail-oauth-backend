"""
Slack Channels API Client Implementation
Handles Slack channel and message operations
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime

from ...core.database import db_manager
from ...core.exceptions import APIError


class SlackChannelsAPI:
    """Slack API client for channel and message operations"""
    
    def __init__(self):
        self.base_url = "https://slack.com/api"
    
    async def _get_headers(self, user_email: str) -> Dict[str, str]:
        """Get authorization headers for API calls"""
        tokens = db_manager.get_valid_tokens(user_email, "slack")
        if not tokens:
            raise APIError("No valid Slack tokens found")
        
        return {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Content-Type": "application/json"
        }
    
    async def list_channels(self, user_email: str, exclude_archived: bool = True) -> Dict[str, Any]:
        """List all channels accessible to the user"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "exclude_archived": exclude_archived
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/conversations.list", headers=headers, params=params)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                channels = result.get("channels", [])
                return {
                    "success": True,
                    "channels": channels,
                    "total": len(channels),
                    "exclude_archived": exclude_archived
                }
        except Exception as e:
            raise APIError(f"Failed to list channels: {str(e)}")
    
    async def get_channel_info(self, user_email: str, channel_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific channel"""
        try:
            headers = await self._get_headers(user_email)
            params = {"channel": channel_id}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/conversations.info", headers=headers, params=params)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                return result.get("channel", {})
        except Exception as e:
            raise APIError(f"Failed to get channel info: {str(e)}")
    
    async def get_channel_messages(self, user_email: str, channel_id: str, 
                                  limit: int = 100, latest: Optional[str] = None) -> Dict[str, Any]:
        """Get messages from a specific channel"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "channel": channel_id,
                "limit": limit
            }
            if latest:
                params["latest"] = latest
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/conversations.history", headers=headers, params=params)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                messages = result.get("messages", [])
                return {
                    "success": True,
                    "messages": messages,
                    "total": len(messages),
                    "channel_id": channel_id,
                    "has_more": result.get("has_more", False),
                    "latest": result.get("latest"),
                    "oldest": result.get("oldest")
                }
        except Exception as e:
            raise APIError(f"Failed to get channel messages: {str(e)}")
    
    async def send_message(self, user_email: str, channel_id: str, text: str, 
                          thread_ts: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to a channel"""
        try:
            headers = await self._get_headers(user_email)
            data = {
                "channel": channel_id,
                "text": text
            }
            if thread_ts:
                data["thread_ts"] = thread_ts
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/chat.postMessage", headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                return {
                    "success": True,
                    "message": result.get("message", {}),
                    "channel": result.get("channel"),
                    "ts": result.get("ts")
                }
        except Exception as e:
            raise APIError(f"Failed to send message: {str(e)}")
    
    async def search_messages(self, user_email: str, query: str, 
                             channel_id: Optional[str] = None, count: int = 20) -> Dict[str, Any]:
        """Search messages across channels"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "query": query,
                "count": count
            }
            if channel_id:
                params["channel"] = channel_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/search.messages", headers=headers, params=params)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                matches = result.get("messages", {}).get("matches", [])
                return {
                    "success": True,
                    "messages": matches,
                    "total": len(matches),
                    "query": query,
                    "total_found": result.get("messages", {}).get("total", 0)
                }
        except Exception as e:
            raise APIError(f"Failed to search messages: {str(e)}")
    
    async def get_channel_members(self, user_email: str, channel_id: str) -> Dict[str, Any]:
        """Get list of members in a channel"""
        try:
            headers = await self._get_headers(user_email)
            params = {"channel": channel_id}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/conversations.members", headers=headers, params=params)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                members = result.get("members", [])
                return {
                    "success": True,
                    "members": members,
                    "total": len(members),
                    "channel_id": channel_id
                }
        except Exception as e:
            raise APIError(f"Failed to get channel members: {str(e)}")
    
    async def join_channel(self, user_email: str, channel_id: str) -> Dict[str, Any]:
        """Join a channel"""
        try:
            headers = await self._get_headers(user_email)
            data = {"channel": channel_id}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/conversations.join", headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                return {
                    "success": True,
                    "channel": result.get("channel", {}),
                    "channel_id": channel_id
                }
        except Exception as e:
            raise APIError(f"Failed to join channel: {str(e)}")
    
    async def leave_channel(self, user_email: str, channel_id: str) -> Dict[str, Any]:
        """Leave a channel"""
        try:
            headers = await self._get_headers(user_email)
            data = {"channel": channel_id}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/conversations.leave", headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                
                if not result.get("ok"):
                    raise APIError(f"Slack API error: {result.get('error', 'Unknown error')}")
                
                return {
                    "success": True,
                    "channel_id": channel_id
                }
        except Exception as e:
            raise APIError(f"Failed to leave channel: {str(e)}")


# Global instance
slack_channels_api = SlackChannelsAPI() 
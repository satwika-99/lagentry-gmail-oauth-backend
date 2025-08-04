"""
Base Connector Class
Provides common interface for all connector implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import asyncio

from ..core.database import db_manager
from ..core.exceptions import ConnectorError, TokenError


class BaseConnector(ABC):
    """Abstract base class for all connectors"""
    
    def __init__(self, provider: str, user_email: str):
        self.provider = provider
        self.user_email = user_email
        self._tokens = None
        self._last_sync = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the service"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from the service"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test if the connection is working"""
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get available capabilities of this connector"""
        pass
    
    async def _get_tokens(self) -> Optional[Dict[str, Any]]:
        """Get valid tokens for the user"""
        if not self._tokens:
            self._tokens = await db_manager.get_valid_tokens(self.user_email, self.provider)
        return self._tokens
    
    async def _validate_tokens(self) -> bool:
        """Validate if tokens are still valid"""
        tokens = await self._get_tokens()
        if not tokens:
            raise TokenError(f"No valid tokens found for {self.provider}")
        return True
    
    async def _log_activity(self, action: str, details: Dict[str, Any] = None) -> None:
        """Log connector activity"""
        await db_manager.log_activity(
            user_email=self.user_email,
            provider=self.provider,
            action=action,
            details=details or {}
        )
    
    async def _update_sync_time(self) -> None:
        """Update last sync time"""
        self._last_sync = datetime.now()
    
    def get_last_sync(self) -> Optional[datetime]:
        """Get last sync time"""
        return self._last_sync
    
    async def get_status(self) -> Dict[str, Any]:
        """Get connector status"""
        try:
            tokens = await self._get_tokens()
            connection_test = await self.test_connection()
            
            return {
                "provider": self.provider,
                "user_email": self.user_email,
                "connected": bool(tokens),
                "last_sync": self._last_sync.isoformat() if self._last_sync else None,
                "connection_test": connection_test,
                "capabilities": await self.get_capabilities()
            }
        except Exception as e:
            return {
                "provider": self.provider,
                "user_email": self.user_email,
                "connected": False,
                "error": str(e)
            }


class DataConnector(BaseConnector):
    """Base class for data connectors (files, emails, etc.)"""
    
    @abstractmethod
    async def list_items(self, **kwargs) -> Dict[str, Any]:
        """List items from the service"""
        pass
    
    @abstractmethod
    async def get_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific item by ID"""
        pass
    
    @abstractmethod
    async def create_item(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create a new item"""
        pass
    
    @abstractmethod
    async def update_item(self, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an existing item"""
        pass
    
    @abstractmethod
    async def delete_item(self, item_id: str, **kwargs) -> bool:
        """Delete an item"""
        pass
    
    @abstractmethod
    async def search_items(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for items"""
        pass
    
    async def sync_items(self, **kwargs) -> Dict[str, Any]:
        """Sync items with local storage"""
        try:
            await self._log_activity("sync_started")
            
            # Get items from service
            items = await self.list_items(**kwargs)
            
            # Process items (implement in subclasses)
            processed = await self._process_items(items)
            
            # Update sync time
            await self._update_sync_time()
            await self._log_activity("sync_completed", {"items_count": len(processed)})
            
            return {
                "success": True,
                "items_synced": len(processed),
                "last_sync": self._last_sync.isoformat() if self._last_sync else None
            }
            
        except Exception as e:
            await self._log_activity("sync_failed", {"error": str(e)})
            raise ConnectorError(f"Sync failed: {str(e)}")
    
    async def _process_items(self, items: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process items during sync (override in subclasses)"""
        return items.get("items", [])


class CommunicationConnector(BaseConnector):
    """Base class for communication connectors (messages, channels, etc.)"""
    
    @abstractmethod
    async def list_channels(self, **kwargs) -> Dict[str, Any]:
        """List available channels"""
        pass
    
    @abstractmethod
    async def get_channel(self, channel_id: str, **kwargs) -> Dict[str, Any]:
        """Get channel details"""
        pass
    
    @abstractmethod
    async def list_messages(self, channel_id: str, **kwargs) -> Dict[str, Any]:
        """List messages in a channel"""
        pass
    
    @abstractmethod
    async def send_message(self, channel_id: str, message: str, **kwargs) -> Dict[str, Any]:
        """Send a message to a channel"""
        pass
    
    @abstractmethod
    async def get_message(self, message_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific message"""
        pass
    
    async def search_messages(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for messages across channels"""
        try:
            channels = await self.list_channels(**kwargs)
            all_messages = []
            
            for channel in channels.get("channels", []):
                messages = await self.list_messages(channel["id"], **kwargs)
                all_messages.extend(messages.get("messages", []))
            
            # Filter by query (implement in subclasses)
            filtered = await self._filter_messages(all_messages, query)
            
            return {
                "messages": filtered,
                "total": len(filtered),
                "query": query
            }
            
        except Exception as e:
            raise ConnectorError(f"Message search failed: {str(e)}")
    
    async def _filter_messages(self, messages: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Filter messages by query (override in subclasses)"""
        return [msg for msg in messages if query.lower() in msg.get("text", "").lower()]


class ProjectConnector(BaseConnector):
    """Base class for project management connectors (issues, tasks, etc.)"""
    
    @abstractmethod
    async def list_projects(self, **kwargs) -> Dict[str, Any]:
        """List available projects"""
        pass
    
    @abstractmethod
    async def get_project(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """Get project details"""
        pass
    
    @abstractmethod
    async def list_issues(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """List issues in a project"""
        pass
    
    @abstractmethod
    async def create_issue(self, project_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create a new issue"""
        pass
    
    @abstractmethod
    async def update_issue(self, issue_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an existing issue"""
        pass
    
    @abstractmethod
    async def get_issue(self, issue_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific issue"""
        pass
    
    async def get_project_summary(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """Get project summary with statistics"""
        try:
            project = await self.get_project(project_id, **kwargs)
            issues = await self.list_issues(project_id, **kwargs)
            
            # Calculate statistics
            total_issues = len(issues.get("issues", []))
            open_issues = len([i for i in issues.get("issues", []) if i.get("status") != "closed"])
            closed_issues = total_issues - open_issues
            
            return {
                "project": project,
                "statistics": {
                    "total_issues": total_issues,
                    "open_issues": open_issues,
                    "closed_issues": closed_issues,
                    "completion_rate": (closed_issues / total_issues * 100) if total_issues > 0 else 0
                }
            }
            
        except Exception as e:
            raise ConnectorError(f"Failed to get project summary: {str(e)}")


class ConnectorFactory:
    """Factory for creating connector instances"""
    
    _connectors = {}
    
    @classmethod
    def register(cls, provider: str, connector_class: type):
        """Register a connector class"""
        cls._connectors[provider] = connector_class
    
    @classmethod
    def create(cls, provider: str, user_email: str, **kwargs) -> BaseConnector:
        """Create a connector instance"""
        if provider not in cls._connectors:
            raise ConnectorError(f"No connector registered for provider: {provider}")
        
        connector_class = cls._connectors[provider]
        return connector_class(user_email=user_email, **kwargs)
    
    @classmethod
    def get_available_connectors(cls) -> List[str]:
        """Get list of available connectors"""
        return list(cls._connectors.keys()) 
"""
Unified Connector Service
Manages all connectors using the factory pattern
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from ..connectors import ConnectorFactory
from ..core.database import db_manager
from ..core.exceptions import ConnectorError, TokenError


class ConnectorService:
    """Unified connector service for all providers"""
    
    def __init__(self):
        self.connectors = {}
    
    def get_connector(self, provider: str, user_email: str):
        """Get or create a connector instance"""
        connector_key = f"{provider}_{user_email}"
        
        if connector_key not in self.connectors:
            try:
                connector = ConnectorFactory.create(provider, user_email)
                self.connectors[connector_key] = connector
            except Exception as e:
                raise ConnectorError(f"Failed to create connector for {provider}: {str(e)}")
        
        return self.connectors[connector_key]
    
    async def test_connection(self, provider: str, user_email: str) -> Dict[str, Any]:
        """Test connection for a specific provider"""
        try:
            connector = self.get_connector(provider, user_email)
            result = await connector.test_connection()
            
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="connection_test",
                details=result
            )
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="connection_test_failed",
                details={"error": str(e)}
            )
            raise ConnectorError(f"Connection test failed for {provider}: {str(e)}")
    
    async def get_capabilities(self, provider: str, user_email: str) -> Dict[str, Any]:
        """Get capabilities for a specific provider"""
        try:
            connector = self.get_connector(provider, user_email)
            capabilities = await connector.get_capabilities()
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "capabilities": capabilities
            }
        except Exception as e:
            raise ConnectorError(f"Failed to get capabilities for {provider}: {str(e)}")
    
    async def list_items(self, provider: str, user_email: str, **kwargs) -> Dict[str, Any]:
        """List items from a provider"""
        try:
            connector = self.get_connector(provider, user_email)
            result = await connector.list_items(**kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="list_items",
                details={"count": result.get("total", 0)}
            )
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="list_items_failed",
                details={"error": str(e)}
            )
            raise ConnectorError(f"Failed to list items for {provider}: {str(e)}")
    
    async def get_item(self, provider: str, user_email: str, item_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific item from a provider"""
        try:
            connector = self.get_connector(provider, user_email)
            result = await connector.get_item(item_id, **kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="get_item",
                details={"item_id": item_id}
            )
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="get_item_failed",
                details={"error": str(e), "item_id": item_id}
            )
            raise ConnectorError(f"Failed to get item for {provider}: {str(e)}")
    
    async def create_item(self, provider: str, user_email: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create an item in a provider"""
        try:
            connector = self.get_connector(provider, user_email)
            result = await connector.create_item(data, **kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="create_item",
                details={"item_id": result.get("id") or result.get("key")}
            )
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="create_item_failed",
                details={"error": str(e)}
            )
            raise ConnectorError(f"Failed to create item for {provider}: {str(e)}")
    
    async def update_item(self, provider: str, user_email: str, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an item in a provider"""
        try:
            connector = self.get_connector(provider, user_email)
            result = await connector.update_item(item_id, data, **kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="update_item",
                details={"item_id": item_id}
            )
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="update_item_failed",
                details={"error": str(e), "item_id": item_id}
            )
            raise ConnectorError(f"Failed to update item for {provider}: {str(e)}")
    
    async def delete_item(self, provider: str, user_email: str, item_id: str, **kwargs) -> Dict[str, Any]:
        """Delete an item from a provider"""
        try:
            connector = self.get_connector(provider, user_email)
            result = await connector.delete_item(item_id, **kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="delete_item",
                details={"item_id": item_id}
            )
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="delete_item_failed",
                details={"error": str(e), "item_id": item_id}
            )
            raise ConnectorError(f"Failed to delete item for {provider}: {str(e)}")
    
    async def search_items(self, provider: str, user_email: str, query: str, **kwargs) -> Dict[str, Any]:
        """Search items in a provider"""
        try:
            connector = self.get_connector(provider, user_email)
            result = await connector.search_items(query, **kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="search_items",
                details={"query": query, "count": result.get("total", 0)}
            )
            
            return {
                "success": True,
                "provider": provider,
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider=provider,
                action="search_items_failed",
                details={"error": str(e), "query": query}
            )
            raise ConnectorError(f"Failed to search items for {provider}: {str(e)}")
    
    # Provider-specific methods for Slack
    async def list_channels(self, user_email: str, **kwargs) -> Dict[str, Any]:
        """List Slack channels"""
        return await self.list_items("slack", user_email, **kwargs)
    
    async def send_message(self, user_email: str, channel_id: str, message: str, **kwargs) -> Dict[str, Any]:
        """Send a message to a Slack channel"""
        try:
            connector = self.get_connector("slack", user_email)
            result = await connector.send_message(channel_id, message, **kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider="slack",
                action="send_message",
                details={"channel_id": channel_id, "message_ts": result.get("ts")}
            )
            
            return {
                "success": True,
                "provider": "slack",
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider="slack",
                action="send_message_failed",
                details={"error": str(e), "channel_id": channel_id}
            )
            raise ConnectorError(f"Failed to send message: {str(e)}")
    
    # Provider-specific methods for Jira
    async def list_projects(self, user_email: str, **kwargs) -> Dict[str, Any]:
        """List Jira projects"""
        return await self.list_items("jira", user_email, **kwargs)
    
    async def list_issues(self, user_email: str, project_id: str, **kwargs) -> Dict[str, Any]:
        """List issues in a Jira project"""
        try:
            connector = self.get_connector("jira", user_email)
            result = await connector.list_issues(project_id, **kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider="jira",
                action="list_issues",
                details={"project_id": project_id, "count": result.get("total", 0)}
            )
            
            return {
                "success": True,
                "provider": "jira",
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider="jira",
                action="list_issues_failed",
                details={"error": str(e), "project_id": project_id}
            )
            raise ConnectorError(f"Failed to list issues: {str(e)}")
    
    async def get_my_issues(self, user_email: str, **kwargs) -> Dict[str, Any]:
        """Get issues assigned to the current user in Jira"""
        try:
            connector = self.get_connector("jira", user_email)
            result = await connector.get_my_issues(**kwargs)
            
            db_manager.log_activity(
                user_email=user_email,
                provider="jira",
                action="get_my_issues",
                details={"count": result.get("total", 0)}
            )
            
            return {
                "success": True,
                "provider": "jira",
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider="jira",
                action="get_my_issues_failed",
                details={"error": str(e)}
            )
            raise ConnectorError(f"Failed to get my issues: {str(e)}")
    
    # Provider-specific methods for Gmail
    async def list_emails(self, user_email: str, **kwargs) -> Dict[str, Any]:
        """List emails from Gmail"""
        return await self.list_items("gmail", user_email, **kwargs)
    
    async def send_email(self, user_email: str, email_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Send an email via Gmail"""
        return await self.create_item("gmail", user_email, email_data, **kwargs)
    
    async def get_labels(self, user_email: str) -> Dict[str, Any]:
        """Get Gmail labels"""
        try:
            connector = self.get_connector("gmail", user_email)
            result = await connector.get_labels()
            
            db_manager.log_activity(
                user_email=user_email,
                provider="gmail",
                action="get_labels",
                details={"count": len(result.get("labels", []))}
            )
            
            return {
                "success": True,
                "provider": "gmail",
                "user_email": user_email,
                "result": result
            }
        except Exception as e:
            db_manager.log_activity(
                user_email=user_email,
                provider="gmail",
                action="get_labels_failed",
                details={"error": str(e)}
            )
            raise ConnectorError(f"Failed to get labels: {str(e)}")
    
    def get_available_connectors(self) -> List[str]:
        """Get list of available connectors"""
        return ConnectorFactory.get_available_connectors()


# Global connector service instance
connector_service = ConnectorService() 
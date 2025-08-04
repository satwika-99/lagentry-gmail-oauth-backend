"""
Gmail Connector Implementation
Handles Gmail operations through the connector interface
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from ...connectors.base import DataConnector
from ...providers.google.gmail import gmail_service
from ...core.exceptions import ConnectorError


class GmailConnector(DataConnector):
    """Gmail connector for email operations"""
    
    def __init__(self, user_email: str):
        super().__init__(provider="google", user_email=user_email)
        self.service = gmail_service
    
    async def connect(self) -> bool:
        """Establish connection to Gmail"""
        try:
            await self._validate_tokens()
            await self._log_activity("connected")
            return True
        except Exception as e:
            await self._log_activity("connection_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to connect to Gmail: {str(e)}")
    
    async def disconnect(self) -> bool:
        """Disconnect from Gmail"""
        try:
            await self._log_activity("disconnected")
            return True
        except Exception as e:
            raise ConnectorError(f"Failed to disconnect from Gmail: {str(e)}")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Gmail connection"""
        try:
            # Try to get user profile
            profile = await self.service.get_profile(self.user_email)
            return {
                "success": True,
                "profile": profile,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get Gmail connector capabilities"""
        return {
            "provider": "google",
            "service": "gmail",
            "capabilities": [
                "list_emails",
                "get_email",
                "send_email",
                "search_emails",
                "get_labels",
                "get_profile",
                "sync_emails"
            ],
            "supported_operations": [
                "read_emails",
                "send_emails",
                "search_emails",
                "manage_labels",
                "get_user_info"
            ]
        }
    
    async def list_items(self, **kwargs) -> Dict[str, Any]:
        """List emails (alias for list_emails)"""
        return await self.list_emails(**kwargs)
    
    async def list_emails(
        self, 
        max_results: int = 50,
        query: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
        include_spam_trash: bool = False
    ) -> Dict[str, Any]:
        """List emails from Gmail"""
        try:
            await self._validate_tokens()
            
            messages = await self.service.get_messages(
                user_email=self.user_email,
                max_results=max_results,
                query=query,
                label_ids=label_ids,
                include_spam_trash=include_spam_trash
            )
            
            await self._log_activity("list_emails", {
                "count": len(messages.get("messages", [])),
                "query": query
            })
            
            return messages
            
        except Exception as e:
            await self._log_activity("list_emails_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list emails: {str(e)}")
    
    async def get_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific email by ID"""
        return await self.get_email(item_id, **kwargs)
    
    async def get_email(self, message_id: str, format: str = "full") -> Dict[str, Any]:
        """Get a specific email by ID"""
        try:
            await self._validate_tokens()
            
            message = await self.service.get_message(
                user_email=self.user_email,
                message_id=message_id,
                format=format
            )
            
            await self._log_activity("get_email", {"message_id": message_id})
            
            return message
            
        except Exception as e:
            await self._log_activity("get_email_failed", {"error": str(e), "message_id": message_id})
            raise ConnectorError(f"Failed to get email: {str(e)}")
    
    async def create_item(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Send an email (alias for send_email)"""
        return await self.send_email(data, **kwargs)
    
    async def send_email(
        self, 
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send an email"""
        try:
            await self._validate_tokens()
            
            # Prepare email data
            email_data = {
                "to": to,
                "subject": subject,
                "body": body
            }
            
            if cc:
                email_data["cc"] = cc
            if bcc:
                email_data["bcc"] = bcc
            if reply_to:
                email_data["reply_to"] = reply_to
            
            # Send email (implement in gmail service)
            result = await self.service.send_message(
                user_email=self.user_email,
                email_data=email_data
            )
            
            await self._log_activity("send_email", {
                "to": to,
                "subject": subject
            })
            
            return result
            
        except Exception as e:
            await self._log_activity("send_email_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to send email: {str(e)}")
    
    async def update_item(self, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update email (modify labels, mark as read, etc.)"""
        try:
            await self._validate_tokens()
            
            # Update email (implement in gmail service)
            result = await self.service.modify_message(
                user_email=self.user_email,
                message_id=item_id,
                modifications=data
            )
            
            await self._log_activity("update_email", {
                "message_id": item_id,
                "modifications": data
            })
            
            return result
            
        except Exception as e:
            await self._log_activity("update_email_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to update email: {str(e)}")
    
    async def delete_item(self, item_id: str, **kwargs) -> bool:
        """Delete an email (move to trash)"""
        try:
            await self._validate_tokens()
            
            # Delete email (implement in gmail service)
            result = await self.service.delete_message(
                user_email=self.user_email,
                message_id=item_id
            )
            
            await self._log_activity("delete_email", {"message_id": item_id})
            
            return result
            
        except Exception as e:
            await self._log_activity("delete_email_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to delete email: {str(e)}")
    
    async def search_items(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for emails"""
        return await self.search_emails(query, **kwargs)
    
    async def search_emails(
        self, 
        query: str,
        max_results: int = 50,
        label_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Search for emails"""
        try:
            await self._validate_tokens()
            
            messages = await self.service.search_messages(
                user_email=self.user_email,
                query=query,
                max_results=max_results,
                label_ids=label_ids
            )
            
            await self._log_activity("search_emails", {
                "query": query,
                "count": len(messages.get("messages", []))
            })
            
            return messages
            
        except Exception as e:
            await self._log_activity("search_emails_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to search emails: {str(e)}")
    
    async def get_labels(self) -> Dict[str, Any]:
        """Get Gmail labels"""
        try:
            await self._validate_tokens()
            
            labels = await self.service.get_labels(self.user_email)
            
            await self._log_activity("get_labels", {
                "count": len(labels.get("labels", []))
            })
            
            return labels
            
        except Exception as e:
            await self._log_activity("get_labels_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get labels: {str(e)}")
    
    async def get_profile(self) -> Dict[str, Any]:
        """Get Gmail user profile"""
        try:
            await self._validate_tokens()
            
            profile = await self.service.get_profile(self.user_email)
            
            await self._log_activity("get_profile")
            
            return profile
            
        except Exception as e:
            await self._log_activity("get_profile_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get profile: {str(e)}")
    
    async def sync_emails(self, **kwargs) -> Dict[str, Any]:
        """Sync emails with local storage"""
        try:
            await self._log_activity("sync_emails_started")
            
            # Get recent emails
            emails = await self.list_emails(max_results=100, **kwargs)
            
            # Process emails
            processed = await self._process_items(emails)
            
            # Update sync time
            await self._update_sync_time()
            await self._log_activity("sync_emails_completed", {
                "emails_synced": len(processed)
            })
            
            return {
                "success": True,
                "emails_synced": len(processed),
                "last_sync": self._last_sync.isoformat() if self._last_sync else None
            }
            
        except Exception as e:
            await self._log_activity("sync_emails_failed", {"error": str(e)})
            raise ConnectorError(f"Email sync failed: {str(e)}")
    
    async def _process_items(self, items: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process emails during sync"""
        messages = items.get("messages", [])
        
        # Process each message to get full details
        processed_messages = []
        for message in messages[:10]:  # Limit to 10 for performance
            try:
                full_message = await self.get_email(message["id"], format="metadata")
                processed_messages.append(full_message)
            except Exception as e:
                # Skip messages that can't be processed
                continue
        
        return processed_messages


# Register the connector
from ...connectors.base import ConnectorFactory
ConnectorFactory.register("gmail", GmailConnector) 
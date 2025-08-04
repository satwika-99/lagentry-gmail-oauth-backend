"""
Gmail Connector Implementation
Handles Gmail operations using the modular connector pattern
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime

from ...connectors.base import DataConnector
from ...core.database import db_manager
from ...core.exceptions import ConnectorError, TokenError
from ...providers.google.auth import google_provider


class GmailConnector(DataConnector):
    """Gmail connector for email operations"""
    
    def __init__(self, user_email: str):
        super().__init__("gmail", user_email)
        self.api_base_url = "https://gmail.googleapis.com/gmail/v1"
        self.oauth_provider = google_provider
    
    async def connect(self) -> bool:
        """Establish connection to Gmail API"""
        try:
            tokens = self._get_tokens()
            if not tokens:
                # Return mock connection instead of throwing error
                self._log_activity("connected", {"mock": True})
                return True
            
            # Test connection with a simple API call
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/users/me/profile", headers=headers)
                if response.status_code == 200:
                    self._log_activity("connected")
                    return True
                else:
                    raise ConnectorError("Failed to connect to Gmail API")
                    
        except Exception as e:
            self._log_activity("connection_failed", {"error": str(e)})
            raise ConnectorError(f"Gmail connection failed: {str(e)}")
    
    async def disconnect(self) -> bool:
        """Disconnect from Gmail API"""
        self._log_activity("disconnected")
        return True
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Gmail API connection"""
        try:
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                return {
                    "connected": True,
                    "user_email": self.user_email,
                    "messages_total": 0,
                    "threads_total": 0,
                    "mock_data": True,
                    "message": "Mock connection - authenticate to get real data"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/users/me/profile", headers=headers)
                
                if response.status_code == 200:
                    profile = response.json()
                    return {
                        "connected": True,
                        "user_email": profile.get("emailAddress"),
                        "messages_total": profile.get("messagesTotal", 0),
                        "threads_total": profile.get("threadsTotal", 0)
                    }
                else:
                    return {"connected": False, "error": "API call failed"}
                    
        except Exception as e:
            return {"connected": False, "error": str(e)}
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get Gmail API capabilities"""
        return {
            "provider": "gmail",
            "capabilities": [
                "list_emails",
                "get_email",
                "send_email",
                "search_emails",
                "get_labels",
                "get_profile"
            ],
            "scopes": [
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.modify",
                "https://www.googleapis.com/auth/gmail.compose",
                "https://www.googleapis.com/auth/gmail.send"
            ]
        }
    
    async def list_items(self, **kwargs) -> Dict[str, Any]:
        """List emails from Gmail"""
        try:
            max_results = kwargs.get("max_results", 50)
            query = kwargs.get("query")
            label_ids = kwargs.get("label_ids")
            include_spam_trash = kwargs.get("include_spam_trash", False)
            
            tokens = self._get_tokens()
            print(f"DEBUG: tokens = {tokens}")  # Debug line
            
            # If no tokens, return mock data
            if not tokens:
                print("DEBUG: No tokens found, returning mock data")  # Debug line
                mock_messages = [
                    {
                        "id": "mock_email_1",
                        "threadId": "mock_thread_1",
                        "snippet": "This is a mock email for testing purposes",
                        "labelIds": ["INBOX"],
                        "internalDate": "1640995200000"
                    },
                    {
                        "id": "mock_email_2", 
                        "threadId": "mock_thread_2",
                        "snippet": "Another mock email to demonstrate functionality",
                        "labelIds": ["INBOX"],
                        "internalDate": "1640995200000"
                    }
                ]
                
                self._log_activity("list_emails", {"count": len(mock_messages), "mock": True})
                return {
                    "success": True,
                    "messages": mock_messages,
                    "total": len(mock_messages),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real emails"
                }
            
            print("DEBUG: Tokens found, making API call")  # Debug line
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "maxResults": max_results,
                "includeSpamTrash": include_spam_trash
            }
            
            if query:
                params["q"] = query
            if label_ids:
                params["labelIds"] = label_ids
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/users/me/messages",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self._log_activity("list_emails", {"count": len(data.get("messages", []))})
                    return {
                        "success": True,
                        "messages": data.get("messages", []),
                        "total": len(data.get("messages", [])),
                        "next_page_token": data.get("nextPageToken")
                    }
                else:
                    raise ConnectorError(f"Failed to list emails: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_emails_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list emails: {str(e)}")
    
    async def get_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific email by ID"""
        try:
            format_type = kwargs.get("format", "full")
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_message = {
                    "id": item_id,
                    "threadId": "mock_thread_1",
                    "snippet": f"This is a mock email with ID {item_id}",
                    "labelIds": ["INBOX"],
                    "internalDate": "1640995200000",
                    "payload": {
                        "headers": [
                            {"name": "Subject", "value": "Mock Email Subject"},
                            {"name": "From", "value": "mock@example.com"},
                            {"name": "To", "value": "test@example.com"}
                        ]
                    }
                }
                
                self._log_activity("get_email", {"message_id": item_id, "mock": True})
                return {
                    "success": True,
                    "message": mock_message,
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real email"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {"format": format_type}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/users/me/messages/{item_id}",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    message = response.json()
                    self._log_activity("get_email", {"message_id": item_id})
                    return {
                        "success": True,
                        "message": message
                    }
                else:
                    raise ConnectorError(f"Failed to get email: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_email_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get email: {str(e)}")
    
    async def create_item(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Send an email via Gmail"""
        try:
            to = data.get("to")
            subject = data.get("subject")
            body = data.get("body")
            cc = data.get("cc")
            bcc = data.get("bcc")
            
            if not all([to, subject, body]):
                raise ConnectorError("Missing required fields: to, subject, body")
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_message_id = "mock_message_123"
                mock_thread_id = "mock_thread_456"
                
                self._log_activity("send_email", {"message_id": mock_message_id, "mock": True})
                return {
                    "success": True,
                    "message_id": mock_message_id,
                    "thread_id": mock_thread_id,
                    "mock_data": True,
                    "message": "Mock data - authenticate to send real emails"
                }
            
            # Create email message
            message = self._create_email_message(to, subject, body, cc, bcc)
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/users/me/messages/send",
                    headers=headers,
                    json={"raw": message}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._log_activity("send_email", {"message_id": result.get("id")})
                    return {
                        "success": True,
                        "message_id": result.get("id"),
                        "thread_id": result.get("threadId")
                    }
                else:
                    raise ConnectorError(f"Failed to send email: {response.text}")
                    
        except Exception as e:
            self._log_activity("send_email_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to send email: {str(e)}")
    
    async def update_item(self, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update email labels (Gmail doesn't support direct email updates)"""
        try:
            add_label_ids = data.get("add_label_ids", [])
            remove_label_ids = data.get("remove_label_ids", [])
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_result = {
                    "id": item_id,
                    "threadId": "mock_thread_456",
                    "labelIds": ["INBOX"] + add_label_ids
                }
                
                self._log_activity("update_email", {"message_id": item_id, "mock": True})
                return {
                    "success": True,
                    "message": mock_result,
                    "mock_data": True,
                    "message": "Mock data - authenticate to update real emails"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            update_data = {}
            if add_label_ids:
                update_data["addLabelIds"] = add_label_ids
            if remove_label_ids:
                update_data["removeLabelIds"] = remove_label_ids
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/users/me/messages/{item_id}/modify",
                    headers=headers,
                    json=update_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._log_activity("update_email", {"message_id": item_id})
                    return {
                        "success": True,
                        "message": result
                    }
                else:
                    raise ConnectorError(f"Failed to update email: {response.text}")
                    
        except Exception as e:
            self._log_activity("update_email_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to update email: {str(e)}")
    
    async def delete_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Delete an email (move to trash)"""
        try:
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                self._log_activity("delete_email", {"message_id": item_id, "mock": True})
                return {
                    "success": True,
                    "message_id": item_id,
                    "action": "deleted",
                    "mock_data": True,
                    "message": "Mock data - authenticate to delete real emails"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.api_base_url}/users/me/messages/{item_id}",
                    headers=headers
                )
                
                if response.status_code == 204:
                    self._log_activity("delete_email", {"message_id": item_id})
                    return {
                        "success": True,
                        "message_id": item_id,
                        "action": "deleted"
                    }
                else:
                    raise ConnectorError(f"Failed to delete email: {response.text}")
                    
        except Exception as e:
            self._log_activity("delete_email_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to delete email: {str(e)}")
    
    async def search_items(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search emails using Gmail API"""
        try:
            max_results = kwargs.get("max_results", 50)
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_messages = [
                    {
                        "id": "mock_search_1",
                        "threadId": "mock_thread_1",
                        "snippet": f"Mock search result for: {query}",
                        "labelIds": ["INBOX"],
                        "internalDate": "1640995200000"
                    },
                    {
                        "id": "mock_search_2",
                        "threadId": "mock_thread_2", 
                        "snippet": f"Another mock result for: {query}",
                        "labelIds": ["INBOX"],
                        "internalDate": "1640995200000"
                    }
                ]
                
                self._log_activity("search_emails", {"query": query, "count": len(mock_messages), "mock": True})
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
                "q": query,
                "maxResults": max_results
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/users/me/messages",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self._log_activity("search_emails", {"query": query, "count": len(data.get("messages", []))})
                    return {
                        "success": True,
                        "messages": data.get("messages", []),
                        "total": len(data.get("messages", [])),
                        "query": query
                    }
                else:
                    raise ConnectorError(f"Failed to search emails: {response.text}")
                    
        except Exception as e:
            self._log_activity("search_emails_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to search emails: {str(e)}")
    
    async def get_labels(self) -> Dict[str, Any]:
        """Get Gmail labels"""
        try:
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_labels = [
                    {
                        "id": "INBOX",
                        "name": "INBOX",
                        "type": "system",
                        "messagesTotal": 15,
                        "messagesUnread": 3
                    },
                    {
                        "id": "SENT",
                        "name": "SENT", 
                        "type": "system",
                        "messagesTotal": 8,
                        "messagesUnread": 0
                    },
                    {
                        "id": "DRAFT",
                        "name": "DRAFT",
                        "type": "system", 
                        "messagesTotal": 2,
                        "messagesUnread": 0
                    }
                ]
                
                self._log_activity("get_labels", {"count": len(mock_labels), "mock": True})
                return {
                    "success": True,
                    "labels": mock_labels,
                    "total": len(mock_labels),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real labels"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/users/me/labels",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self._log_activity("get_labels", {"count": len(data.get("labels", []))})
                    return {
                        "success": True,
                        "labels": data.get("labels", []),
                        "total": len(data.get("labels", []))
                    }
                else:
                    raise ConnectorError(f"Failed to get labels: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_labels_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get labels: {str(e)}")
    
    def _create_email_message(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> str:
        """Create email message in base64 format"""
        import base64
        from email.mime.text import MIMEText
        
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc
        
        return base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8') 
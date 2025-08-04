"""
Gmail API implementation for Google provider
"""

import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from ...core.exceptions import GoogleAPIException, TokenExpiredException
from ...core.utils import mask_token, create_error_response, create_success_response
from ...core.database import db_manager


class GmailAPI:
    """Gmail API client"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://gmail.googleapis.com/gmail/v1/users/me"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    async def get_messages(self, max_results: int = 10, query: str = None) -> List[Dict[str, Any]]:
        """Get Gmail messages"""
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "maxResults": max_results,
                    "format": "metadata",
                    "metadataHeaders": ["Subject", "From", "Date"]
                }
                
                if query:
                    params["q"] = query
                
                response = await client.get(
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code != 200:
                    raise GoogleAPIException(f"Failed to fetch messages: {response.text}")
                
                data = response.json()
                messages = []
                
                for message in data.get("messages", []):
                    message_detail = await self._get_message_detail(message["id"])
                    if message_detail:
                        messages.append(message_detail)
                
                return messages
                
        except Exception as e:
            raise GoogleAPIException(f"Gmail API error: {str(e)}")
    
    async def get_message_detail(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed message information"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/messages/{message_id}",
                    headers=self.headers,
                    params={"format": "metadata", "metadataHeaders": ["Subject", "From", "Date", "To", "Cc"]}
                )
                
                if response.status_code != 200:
                    return None
                
                return self._parse_message(response.json())
                
        except Exception as e:
            print(f"Error getting message detail: {e}")
            return None
    
    async def _get_message_detail(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Internal method to get message detail"""
        return await self.get_message_detail(message_id)
    
    def _parse_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Gmail message data"""
        try:
            headers = message_data.get("payload", {}).get("headers", [])
            header_dict = {h["name"]: h["value"] for h in headers}
            
            return {
                "id": message_data["id"],
                "thread_id": message_data.get("threadId", ""),
                "subject": header_dict.get("Subject", "No Subject"),
                "sender": header_dict.get("From", "Unknown"),
                "recipient": header_dict.get("To", ""),
                "cc": header_dict.get("Cc", ""),
                "date": header_dict.get("Date", ""),
                "snippet": message_data.get("snippet", ""),
                "label_ids": message_data.get("labelIds", []),
                "internal_date": message_data.get("internalDate", "")
            }
            
        except Exception as e:
            print(f"Error parsing message: {e}")
            return {
                "id": message_data.get("id", ""),
                "subject": "Error parsing message",
                "sender": "Unknown",
                "date": "",
                "snippet": ""
            }
    
    async def search_messages(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search Gmail messages"""
        return await self.get_messages(max_results, query)
    
    async def get_labels(self) -> List[Dict[str, Any]]:
        """Get Gmail labels"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/labels",
                    headers=self.headers
                )
                
                if response.status_code != 200:
                    raise GoogleAPIException(f"Failed to fetch labels: {response.text}")
                
                return response.json().get("labels", [])
                
        except Exception as e:
            raise GoogleAPIException(f"Gmail API error: {str(e)}")
    
    async def get_profile(self) -> Dict[str, Any]:
        """Get Gmail profile information"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/profile",
                    headers=self.headers
                )
                
                if response.status_code != 200:
                    raise GoogleAPIException(f"Failed to fetch profile: {response.text}")
                
                return response.json()
                
        except Exception as e:
            raise GoogleAPIException(f"Gmail API error: {str(e)}")


class GmailService:
    """Gmail service for handling Gmail operations"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    async def get_user_emails(self, user_email: str, max_results: int = 10, 
                            query: str = None) -> Dict[str, Any]:
        """Get emails for a user"""
        try:
            # Get valid tokens
            tokens = self.db_manager.get_valid_tokens(user_email, "google")
            if not tokens:
                return create_error_response("No valid tokens found for user")
            
            # Create Gmail API client
            gmail_api = GmailAPI(tokens["access_token"])
            
            # Get messages
            messages = await gmail_api.get_messages(max_results, query)
            
            # Log activity
            self.db_manager.log_activity(
                user_email, 
                "fetch_emails", 
                {"count": len(messages), "query": query}
            )
            
            return create_success_response({
                "emails": messages,
                "count": len(messages),
                "user_email": user_email
            })
            
        except TokenExpiredException:
            return create_error_response("Token expired, please re-authenticate")
        except GoogleAPIException as e:
            return create_error_response(f"Gmail API error: {str(e)}")
        except Exception as e:
            return create_error_response(f"Unexpected error: {str(e)}")
    
    async def search_user_emails(self, user_email: str, query: str, 
                               max_results: int = 10) -> Dict[str, Any]:
        """Search emails for a user"""
        return await self.get_user_emails(user_email, max_results, query)
    
    async def get_user_labels(self, user_email: str) -> Dict[str, Any]:
        """Get Gmail labels for a user"""
        try:
            # Get valid tokens
            tokens = self.db_manager.get_valid_tokens(user_email, "google")
            if not tokens:
                return create_error_response("No valid tokens found for user")
            
            # Create Gmail API client
            gmail_api = GmailAPI(tokens["access_token"])
            
            # Get labels
            labels = await gmail_api.get_labels()
            
            # Log activity
            self.db_manager.log_activity(
                user_email, 
                "fetch_labels", 
                {"count": len(labels)}
            )
            
            return create_success_response({
                "labels": labels,
                "count": len(labels),
                "user_email": user_email
            })
            
        except TokenExpiredException:
            return create_error_response("Token expired, please re-authenticate")
        except GoogleAPIException as e:
            return create_error_response(f"Gmail API error: {str(e)}")
        except Exception as e:
            return create_error_response(f"Unexpected error: {str(e)}")
    
    async def get_user_profile(self, user_email: str) -> Dict[str, Any]:
        """Get Gmail profile for a user"""
        try:
            # Get valid tokens
            tokens = self.db_manager.get_valid_tokens(user_email, "google")
            if not tokens:
                return create_error_response("No valid tokens found for user")
            
            # Create Gmail API client
            gmail_api = GmailAPI(tokens["access_token"])
            
            # Get profile
            profile = await gmail_api.get_profile()
            
            # Log activity
            self.db_manager.log_activity(
                user_email, 
                "fetch_profile", 
                {"profile_id": profile.get("emailAddress", "")}
            )
            
            return create_success_response({
                "profile": profile,
                "user_email": user_email
            })
            
        except TokenExpiredException:
            return create_error_response("Token expired, please re-authenticate")
        except GoogleAPIException as e:
            return create_error_response(f"Gmail API error: {str(e)}")
        except Exception as e:
            return create_error_response(f"Unexpected error: {str(e)}")


# Global Gmail service instance
gmail_service = GmailService() 
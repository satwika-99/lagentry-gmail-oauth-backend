"""
Google Drive API Implementation
Handles file operations, sharing, and Drive management
"""

import httpx
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import base64

from ...core.database import db_manager
from ...core.exceptions import APIError, TokenError


class GoogleDriveAPI:
    """Google Drive API client for file operations"""
    
    def __init__(self):
        self.base_url = "https://www.googleapis.com/drive/v3"
        self.upload_url = "https://www.googleapis.com/upload/drive/v3"
    
    async def _get_headers(self, user_email: str) -> Dict[str, str]:
        """Get authorization headers for API requests"""
        tokens = await db_manager.get_valid_tokens(user_email, "google")
        if not tokens:
            raise TokenError("No valid tokens found for user")
        
        return {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Content-Type": "application/json"
        }
    
    async def list_files(
        self, 
        user_email: str, 
        page_size: int = 50,
        page_token: Optional[str] = None,
        query: Optional[str] = None,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """List files in Google Drive"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "pageSize": page_size,
                "fields": fields or "files(id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink,thumbnailLink),nextPageToken"
            }
            
            if page_token:
                params["pageToken"] = page_token
            
            if query:
                params["q"] = query
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/files", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to list files: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def get_file(self, user_email: str, file_id: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get file metadata by ID"""
        try:
            headers = await self._get_headers(user_email)
            params = {"fields": fields or "*"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/files/{file_id}", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to get file: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def download_file(self, user_email: str, file_id: str) -> bytes:
        """Download file content"""
        try:
            headers = await self._get_headers(user_email)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/files/{file_id}?alt=media", headers=headers)
                response.raise_for_status()
                return response.content
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to download file: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def create_file(
        self, 
        user_email: str, 
        name: str, 
        mime_type: str,
        content: Optional[bytes] = None,
        parents: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new file in Google Drive"""
        try:
            headers = await self._get_headers(user_email)
            
            # File metadata
            file_metadata = {
                "name": name,
                "mimeType": mime_type
            }
            
            if parents:
                file_metadata["parents"] = parents
            
            if content:
                # Upload with content
                params = {"uploadType": "multipart"}
                files = {
                    "metadata": (None, json.dumps(file_metadata), "application/json"),
                    "file": (name, content, mime_type)
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.upload_url}/files",
                        headers=headers,
                        params=params,
                        files=files
                    )
            else:
                # Create empty file
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/files",
                        headers=headers,
                        json=file_metadata
                    )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to create file: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def update_file(
        self, 
        user_email: str, 
        file_id: str, 
        name: Optional[str] = None,
        content: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """Update file metadata and/or content"""
        try:
            headers = await self._get_headers(user_email)
            
            if content:
                # Update with content
                params = {"uploadType": "multipart"}
                file_metadata = {}
                if name:
                    file_metadata["name"] = name
                
                files = {
                    "metadata": (None, json.dumps(file_metadata), "application/json"),
                    "file": (name or "file", content, "application/octet-stream")
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.patch(
                        f"{self.upload_url}/files/{file_id}",
                        headers=headers,
                        params=params,
                        files=files
                    )
            else:
                # Update metadata only
                file_metadata = {}
                if name:
                    file_metadata["name"] = name
                
                async with httpx.AsyncClient() as client:
                    response = await client.patch(
                        f"{self.base_url}/files/{file_id}",
                        headers=headers,
                        json=file_metadata
                    )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to update file: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def delete_file(self, user_email: str, file_id: str) -> bool:
        """Delete a file from Google Drive"""
        try:
            headers = await self._get_headers(user_email)
            
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{self.base_url}/files/{file_id}", headers=headers)
                response.raise_for_status()
                return True
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to delete file: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def share_file(
        self, 
        user_email: str, 
        file_id: str, 
        email: str, 
        role: str = "reader",
        type: str = "user"
    ) -> Dict[str, Any]:
        """Share a file with another user"""
        try:
            headers = await self._get_headers(user_email)
            
            permission = {
                "type": type,
                "role": role,
                "emailAddress": email
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/files/{file_id}/permissions",
                    headers=headers,
                    json=permission
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to share file: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def search_files(
        self, 
        user_email: str, 
        query: str,
        page_size: int = 50,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search for files in Google Drive"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "q": query,
                "pageSize": page_size,
                "fields": "files(id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink),nextPageToken"
            }
            
            if page_token:
                params["pageToken"] = page_token
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/files", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to search files: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")
    
    async def get_drive_info(self, user_email: str) -> Dict[str, Any]:
        """Get Drive storage information"""
        try:
            headers = await self._get_headers(user_email)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/about", headers=headers, params={"fields": "storageQuota,user"})
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to get drive info: {e.response.text}")
        except Exception as e:
            raise APIError(f"Drive API error: {str(e)}")


# API instance
drive_api = GoogleDriveAPI() 
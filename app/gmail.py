"""
Gmail API integration module for Gmail OAuth Backend
Handles Gmail API calls and email operations
"""

import httpx
from typing import List, Dict, Any, Optional
from auth import get_access_token_for_user, refresh_access_token
from storage import get_valid_tokens, store_tokens
from datetime import datetime

async def get_valid_access_token(user_email: str) -> str:
    """Get a valid access token, refreshing if necessary"""
    # Get current tokens
    tokens = get_valid_tokens(user_email)
    if not tokens:
        return None
    
    # Check if token is expired
    now = datetime.now()
    
    # Handle expires_at - it might be a datetime object or a string
    expires_at = tokens['expires_at']
    if isinstance(expires_at, str):
        try:
            # Try to parse the datetime string
            expires_at = datetime.fromisoformat(expires_at)
        except ValueError:
            # If fromisoformat fails, try parsing with strptime
            try:
                expires_at = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                # If that fails too, try without microseconds
                expires_at = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S')
    # If it's already a datetime object, use it directly
    
    if now > expires_at:
        # Token is expired, refresh it
        try:
            new_tokens = await refresh_access_token(tokens['refresh_token'])
            if new_tokens:
                # Store the new tokens
                store_tokens(user_email, new_tokens['access_token'], 
                           tokens['refresh_token'], new_tokens['expires_at'])
                return new_tokens['access_token']
            else:
                return None
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None
    else:
        # Token is still valid
        return tokens['access_token']

async def fetch_emails(user_email: str, max_results: int = 10) -> Dict[str, Any]:
    """Fetch emails from Gmail API"""
    if not user_email:
        raise ValueError("user_email parameter required")
    
    # Get valid access token directly (we know this works)
    tokens = get_valid_tokens(user_email)
    if not tokens:
        raise ValueError("No valid tokens found. Please authenticate first.")
    access_token = tokens['access_token']
    
    # Fetch emails from Gmail API
    gmail_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "maxResults": max_results,
        "q": "is:inbox"  # Only inbox emails
    }
    
    try:
        # Use a single HTTP client for all requests
        async with httpx.AsyncClient() as client:
            # Get messages list
            response = await client.get(gmail_url, headers=headers, params=params)
            response.raise_for_status()
            messages_data = response.json()
            
            # Get detailed message information
            emails = []
            for message in messages_data.get("messages", []):
                message_id = message["id"]
                message_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages/{message_id}"
                
                msg_response = await client.get(message_url, headers=headers)
                msg_response.raise_for_status()
                msg_data = msg_response.json()
            
            # Extract email details
            headers = msg_data.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
            from_header = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
            date_header = next((h["value"] for h in headers if h["name"] == "Date"), "")
            
            emails.append({
                "id": message_id,
                "subject": subject,
                "from": from_header,
                "date": date_header,
                "snippet": msg_data.get("snippet", "")
            })
        
        return {
            "user_email": user_email,
            "emails": emails,
            "total_count": len(emails)
        }
        
    except Exception as e:
        raise Exception(f"Gmail API error: {str(e)}")

async def fetch_email_content(user_email: str, message_id: str) -> Dict[str, Any]:
    """Fetch detailed content of a specific email"""
    access_token = await get_valid_access_token(user_email)
    if not access_token:
        raise ValueError("No valid tokens found. Please authenticate first.")
    
    message_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages/{message_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(message_url, headers=headers)
            response.raise_for_status()
            msg_data = response.json()
        
        # Extract detailed email information
        headers = msg_data.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        from_header = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        to_header = next((h["value"] for h in headers if h["name"] == "To"), "")
        date_header = next((h["value"] for h in headers if h["name"] == "Date"), "")
        
        # Extract email body
        body = ""
        payload = msg_data.get("payload", {})
        if payload.get("body", {}).get("data"):
            import base64
            body_data = payload["body"]["data"]
            body = base64.urlsafe_b64decode(body_data).decode("utf-8")
        elif payload.get("parts"):
            # Handle multipart messages
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                    import base64
                    body_data = part["body"]["data"]
                    body = base64.urlsafe_b64decode(body_data).decode("utf-8")
                    break
        
        return {
            "id": message_id,
            "subject": subject,
            "from": from_header,
            "to": to_header,
            "date": date_header,
            "body": body,
            "snippet": msg_data.get("snippet", "")
        }
        
    except Exception as e:
        raise Exception(f"Gmail API error: {str(e)}")

async def search_emails(user_email: str, query: str, max_results: int = 10) -> Dict[str, Any]:
    """Search emails using Gmail API query syntax"""
    access_token = await get_valid_access_token(user_email)
    if not access_token:
        raise ValueError("No valid tokens found. Please authenticate first.")
    
    gmail_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "maxResults": max_results,
        "q": query
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(gmail_url, headers=headers, params=params)
            response.raise_for_status()
            messages_data = response.json()
        
        # Get detailed message information
        emails = []
        for message in messages_data.get("messages", []):
            message_id = message["id"]
            message_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages/{message_id}"
            
            async with httpx.AsyncClient() as client:
                msg_response = await client.get(message_url, headers=headers)
                msg_response.raise_for_status()
                msg_data = msg_response.json()
            
            # Extract email details
            headers = msg_data.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
            from_header = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
            date_header = next((h["value"] for h in headers if h["name"] == "Date"), "")
            
            emails.append({
                "id": message_id,
                "subject": subject,
                "from": from_header,
                "date": date_header,
                "snippet": msg_data.get("snippet", "")
            })
        
        return {
            "user_email": user_email,
            "query": query,
            "emails": emails,
            "total_count": len(emails)
        }
        
    except Exception as e:
        raise Exception(f"Gmail API error: {str(e)}")

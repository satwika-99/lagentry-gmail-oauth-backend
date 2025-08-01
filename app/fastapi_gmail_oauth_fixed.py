"""
FastAPI Gmail OAuth 2.0 Backend for Lagentry AI Agents - FIXED VERSION
Handles OAuth flow, token storage, and Gmail API integration
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import secrets
import asyncio
from urllib.parse import urlencode
import sqlite3
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Pydantic models for request/response
class EmailResponse(BaseModel):
    id: str
    thread_id: str
    subject: str
    sender: str
    date: str
    snippet: str

class OAuthCallbackResponse(BaseModel):
    message: str
    user_email: str
    access_token: str  # Partial token for security
    expires_in: int

class UserTokens(BaseModel):
    user_email: str
    access_token: str
    refresh_token: str
    expires_at: datetime

# FastAPI app initialization
app = FastAPI(
    title="Gmail OAuth Backend for Lagentry",
    description="Custom Gmail OAuth 2.0 backend for Lagentry AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
class Config:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://127.0.0.1:8080/auth/google/callback")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "oauth_tokens.db")  # Fixed: Use relative path
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/userinfo.email"
    ]

config = Config()

# Database initialization
def init_db():
    """Initialize SQLite database for token storage"""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS oauth_tokens (
                user_email TEXT PRIMARY KEY,
                access_token TEXT NOT NULL,
                refresh_token TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print(f"✅ Database initialized at: {config.DATABASE_PATH}")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Database path: {config.DATABASE_PATH}")

# Initialize database on startup
init_db()

# Database operations
def store_tokens(user_email: str, access_token: str, refresh_token: str, expires_in: int):
    """Store OAuth tokens in database"""
    try:
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO oauth_tokens 
            (user_email, access_token, refresh_token, expires_at, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_email, access_token, refresh_token, expires_at))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error storing tokens: {e}")
        raise

def get_valid_tokens(user_email: str) -> Optional[Dict[str, Any]]:
    """Get valid tokens for user, refresh if needed"""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT access_token, refresh_token, expires_at 
            FROM oauth_tokens 
            WHERE user_email = ?
        ''', (user_email,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            print(f"❌ No tokens found for user: {user_email}")
            return None
        
        access_token, refresh_token, expires_at = result
        expires_at = datetime.fromisoformat(expires_at)
        
        # Check if token is expired
        if datetime.now() >= expires_at:
            print(f"🔄 Token expired for {user_email}, refreshing...")
            # Refresh token
            new_tokens = refresh_access_token(refresh_token)
            if new_tokens:
                store_tokens(user_email, new_tokens["access_token"], refresh_token, new_tokens["expires_in"])
                return {
                    "access_token": new_tokens["access_token"],
                    "refresh_token": refresh_token
                }
            return None
        
        print(f"✅ Valid tokens found for {user_email}")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    except Exception as e:
        print(f"❌ Error getting tokens: {e}")
        return None

def refresh_access_token(refresh_token: str) -> Optional[Dict[str, Any]]:
    """Refresh access token using refresh token"""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "client_secret": config.GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            return {
                "access_token": token_data["access_token"],
                "expires_in": token_data.get("expires_in", 3600)
            }
    except Exception as e:
        print(f"❌ Error refreshing token: {e}")
        return None

def get_all_users() -> List[str]:
    """Get all users with stored tokens"""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT user_email FROM oauth_tokens')
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return []

# OAuth functions
def generate_auth_url() -> str:
    """Generate Google OAuth authorization URL"""
    if not config.GOOGLE_CLIENT_ID:
        raise ValueError("Google Client ID not configured")
    
    # Generate state parameter for security
    state = secrets.token_urlsafe(32)
    
    # Build authorization URL
    auth_params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "scope": " ".join(config.SCOPES),
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"

async def handle_oauth_callback(code: str, state: str) -> Dict[str, Any]:
    """Handle OAuth callback from Google"""
    try:
        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": config.GOOGLE_CLIENT_ID,
            "client_secret": config.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": config.REDIRECT_URI
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=token_data)
            response.raise_for_status()
            tokens = response.json()
        
        # Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        
        async with httpx.AsyncClient() as client:
            user_response = await client.get(user_info_url, headers=headers)
            user_response.raise_for_status()
            user_info = user_response.json()
        
        # Store tokens
        store_tokens(
            user_info["email"],
            tokens["access_token"],
            tokens["refresh_token"],
            tokens["expires_in"]
        )
        
        return {
            "message": "OAuth successful",
            "user_email": user_info["email"],
            "access_token": tokens["access_token"][:20] + "...",  # Show partial token for security
            "expires_in": tokens["expires_in"]
        }
        
    except Exception as e:
        print(f"❌ OAuth callback error: {e}")
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {str(e)}")

# Gmail API functions
async def fetch_emails(user_email: str, max_results: int = 10) -> List[EmailResponse]:
    """Fetch latest emails from Gmail API"""
    try:
        print(f"🔍 Fetching emails for {user_email}, max_results: {max_results}")
        
        # Get tokens
        tokens = get_valid_tokens(user_email)
        if not tokens:
            print(f"❌ No valid tokens found for {user_email}")
            raise HTTPException(status_code=401, detail="No valid tokens found for user")
        
        print(f"✅ Got valid tokens for {user_email}")
        
        # Gmail API endpoint for messages
        gmail_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        params = {
            "maxResults": max_results,
            "labelIds": "INBOX"
        }
        
        print(f"📧 Calling Gmail API: {gmail_url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(gmail_url, headers=headers, params=params)
            response.raise_for_status()
            messages_data = response.json()
        
        print(f"✅ Got {len(messages_data.get('messages', []))} messages from Gmail API")
        
        # Get detailed message info
        emails = []
        for i, message in enumerate(messages_data.get("messages", [])):
            try:
                message_id = message["id"]
                message_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}"
                
                print(f"📧 Processing message {i+1}/{len(messages_data.get('messages', []))}: {message_id}")
                
                async with httpx.AsyncClient() as client:
                    msg_response = await client.get(message_url, headers=headers)
                    msg_response.raise_for_status()
                    msg_data = msg_response.json()
                
                # Extract email details
                msg_headers = msg_data.get("payload", {}).get("headers", [])
                subject = next((h["value"] for h in msg_headers if h["name"] == "Subject"), "No Subject")
                sender = next((h["value"] for h in msg_headers if h["name"] == "From"), "Unknown Sender")
                date = next((h["value"] for h in msg_headers if h["name"] == "Date"), "")
                
                emails.append(EmailResponse(
                    id=message_id,
                    thread_id=msg_data.get("threadId", ""),
                    subject=subject,
                    sender=sender,
                    date=date,
                    snippet=msg_data.get("snippet", "")
                ))
                
                print(f"✅ Processed: {subject[:50]}...")
                
            except Exception as e:
                print(f"❌ Error processing message {message.get('id', 'unknown')}: {e}")
                continue
        
        print(f"✅ Successfully processed {len(emails)} emails")
        return emails
        
    except Exception as e:
        print(f"❌ Error fetching emails: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch emails: {str(e)}")

# FastAPI routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Gmail OAuth Backend for Lagentry",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/google",
            "callback": "/auth/google/callback", 
            "emails": "/emails",
            "users": "/users"
        }
    }

@app.get("/auth/google")
async def auth_google():
    """Redirect to Google OAuth consent screen"""
    try:
        auth_url = generate_auth_url()
        return RedirectResponse(url=auth_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate auth URL: {str(e)}")

@app.get("/auth/google/callback")
async def auth_google_callback(code: str, state: str):
    """Handle OAuth callback from Google"""
    try:
        result = await handle_oauth_callback(code, state)
        return OAuthCallbackResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/emails")
async def get_emails(user_email: str, max_results: int = 10):
    """Get emails for authenticated user"""
    try:
        print(f"📧 Email endpoint called for {user_email}, max_results: {max_results}")
        emails = await fetch_emails(user_email, max_results)
        return {"emails": emails}
    except Exception as e:
        print(f"❌ Email endpoint error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
async def get_users():
    """Get all users with stored tokens"""
    try:
        users = get_all_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080) 
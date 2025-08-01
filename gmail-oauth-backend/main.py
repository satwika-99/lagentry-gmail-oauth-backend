from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import base64
from urllib.parse import urlencode, parse_qs, urlparse
from config import config

app = FastAPI(title="Gmail OAuth Backend", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def init_db():
    """Initialize SQLite database for token storage"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oauth_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT UNIQUE,
            access_token TEXT,
            refresh_token TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(config.DATABASE_PATH)

def store_tokens(user_email: str, access_token: str, refresh_token: str, expires_in: int):
    """Store OAuth tokens in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    expires_at = datetime.now() + timedelta(seconds=expires_in)
    
    cursor.execute("""
        INSERT OR REPLACE INTO oauth_tokens 
        (user_email, access_token, refresh_token, expires_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_email, access_token, refresh_token, expires_at, datetime.now()))
    
    conn.commit()
    conn.close()

def get_valid_tokens(user_email: str) -> Optional[Dict[str, Any]]:
    """Get valid tokens for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT access_token, refresh_token, expires_at 
        FROM oauth_tokens 
        WHERE user_email = ?
    """, (user_email,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        access_token, refresh_token, expires_at = result
        expires_at = datetime.fromisoformat(expires_at)
        
        # Check if token is still valid
        if datetime.now() < expires_at:
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at
            }
    
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
        print(f"Error refreshing token: {e}")
        return None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Gmail OAuth Backend",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/google",
            "callback": "/auth/google/callback",
            "emails": "/emails",
            "status": "/status"
        }
    }

@app.get("/auth/google")
async def google_auth():
    """Initiate Google OAuth flow"""
    if not config.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google Client ID not configured")
    
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
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"
    
    return RedirectResponse(url=auth_url)

@app.get("/auth/google/callback")
async def google_callback(code: str, state: str):
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
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

@app.get("/emails")
async def get_emails(user_email: str = None, max_results: int = 10):
    """Fetch emails from Gmail API"""
    if not user_email:
        raise HTTPException(status_code=400, detail="user_email parameter required")
    
    # Get valid tokens
    tokens = get_valid_tokens(user_email)
    if not tokens:
        raise HTTPException(status_code=401, detail="No valid tokens found. Please authenticate first.")
    
    # Check if token needs refresh
    if datetime.now() >= tokens["expires_at"]:
        refreshed = refresh_access_token(tokens["refresh_token"])
        if refreshed:
            store_tokens(user_email, refreshed["access_token"], tokens["refresh_token"], refreshed["expires_in"])
            access_token = refreshed["access_token"]
        else:
            raise HTTPException(status_code=401, detail="Token refresh failed")
    else:
        access_token = tokens["access_token"]
    
    # Fetch emails from Gmail API
    gmail_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "maxResults": max_results,
        "q": "is:inbox"  # Only inbox emails
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
            "emails": emails,
            "total_count": len(emails)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gmail API error: {str(e)}")

@app.get("/status")
async def get_status():
    """Get API status and configuration info"""
    return {
        "status": "running",
        "google_client_id_configured": bool(config.GOOGLE_CLIENT_ID),
        "google_client_secret_configured": bool(config.GOOGLE_CLIENT_SECRET),
        "redirect_uri": config.REDIRECT_URI,
        "scopes": config.SCOPES
    }

if __name__ == "__main__":
    import uvicorn
    
    # Validate configuration
    if not config.validate():
        print(" Configuration validation failed. Please check your environment variables.")
        exit(1)
    
    # Print configuration
    config.print_config()
    
    print(f" Starting Gmail OAuth Backend on http://{config.HOST}:{config.PORT}")
    print(" API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(app, host=config.HOST, port=config.PORT)

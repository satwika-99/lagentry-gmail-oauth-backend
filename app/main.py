"""
Gmail OAuth Backend - Main FastAPI Application
Modular implementation with separate auth, gmail, and storage modules
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from config import config
from storage import init_db, get_all_users
from auth import generate_auth_url, handle_oauth_callback
from gmail import fetch_emails, fetch_email_content, search_emails

app = FastAPI(title="Gmail OAuth Backend", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
init_db()

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
            "email_content": "/emails/{message_id}",
            "search": "/emails/search",
            "users": "/users",
            "status": "/status"
        }
    }

@app.get("/auth/google")
async def google_auth():
    """Initiate Google OAuth flow"""
    auth_url = generate_auth_url()
    return RedirectResponse(url=auth_url)

@app.get("/auth/google/callback")
async def google_callback(code: str, state: str):
    """Handle OAuth callback from Google"""
    return await handle_oauth_callback(code, state)

@app.get("/emails")
async def get_emails(user_email: str = None, max_results: int = 10):
    """Fetch emails from Gmail API"""
    return await fetch_emails(user_email, max_results)

@app.get("/emails/{message_id}")
async def get_email_content(message_id: str, user_email: str):
    """Fetch detailed content of a specific email"""
    return await fetch_email_content(user_email, message_id)

@app.get("/emails/search")
async def search_emails_endpoint(user_email: str, query: str, max_results: int = 10):
    """Search emails using Gmail API query syntax"""
    return await search_emails(user_email, query, max_results)

@app.get("/users")
async def get_users():
    """Get list of all users with stored tokens"""
    users = get_all_users()
    return {
        "users": users,
        "total_count": len(users)
    }

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

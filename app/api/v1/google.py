"""
Google API endpoints for v1
"""

import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

from ...providers.google.gmail import gmail_service
from ...core.utils import create_success_response, create_error_response

router = APIRouter(prefix="/google", tags=["Google"])


@router.get("/gmail/emails")
async def get_gmail_emails(
    user_email: str = Query(..., description="User email address"),
    max_results: int = Query(10, description="Maximum number of emails to fetch"),
    query: Optional[str] = Query(None, description="Gmail search query")
):
    """Get Gmail emails for a user"""
    try:
        result = await gmail_service.get_user_emails(user_email, max_results, query)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch emails: {str(e)}")


@router.get("/gmail/search")
async def search_gmail_emails(
    user_email: str = Query(..., description="User email address"),
    query: str = Query(..., description="Gmail search query"),
    max_results: int = Query(10, description="Maximum number of emails to fetch")
):
    """Search Gmail emails for a user"""
    try:
        result = await gmail_service.search_user_emails(user_email, query, max_results)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search emails: {str(e)}")


@router.get("/gmail/labels")
async def get_gmail_labels(
    user_email: str = Query(..., description="User email address")
):
    """Get Gmail labels for a user"""
    try:
        result = await gmail_service.get_user_labels(user_email)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch labels: {str(e)}")


@router.get("/gmail/profile")
async def get_gmail_profile(
    user_email: str = Query(..., description="User email address")
):
    """Get Gmail profile for a user"""
    try:
        result = await gmail_service.get_user_profile(user_email)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")


@router.get("/gmail/message/{message_id}")
async def get_gmail_message(
    message_id: str,
    user_email: str = Query(..., description="User email address")
):
    """Get specific Gmail message"""
    try:
        # Get valid tokens
        from ...core.database import db_manager
        tokens = db_manager.get_valid_tokens(user_email, "google")
        if not tokens:
            raise HTTPException(status_code=404, detail="No valid tokens found for user")
        
        # Create Gmail API client
        from ...providers.google.gmail import GmailAPI
        gmail_api = GmailAPI(tokens["access_token"])
        
        # Get message
        message = await gmail_api.get_message_detail(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Log activity
        db_manager.log_activity(
            user_email, 
            "fetch_message", 
            {"message_id": message_id}
        )
        
        return create_success_response({
            "message": message,
            "user_email": user_email
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch message: {str(e)}")


@router.get("/gmail/thread/{thread_id}")
async def get_gmail_thread(
    thread_id: str,
    user_email: str = Query(..., description="User email address")
):
    """Get Gmail thread messages"""
    try:
        # Get valid tokens
        from ...core.database import db_manager
        tokens = db_manager.get_valid_tokens(user_email, "google")
        if not tokens:
            raise HTTPException(status_code=404, detail="No valid tokens found for user")
        
        # Create Gmail API client
        from ...providers.google.gmail import GmailAPI
        gmail_api = GmailAPI(tokens["access_token"])
        
        # Get thread messages
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{gmail_api.base_url}/threads/{thread_id}",
                headers=gmail_api.headers
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Thread not found")
            
            thread_data = response.json()
            messages = []
            
            for message in thread_data.get("messages", []):
                message_detail = await gmail_api._get_message_detail(message["id"])
                if message_detail:
                    messages.append(message_detail)
        
        # Log activity
        db_manager.log_activity(
            user_email, 
            "fetch_thread", 
            {"thread_id": thread_id, "message_count": len(messages)}
        )
        
        return create_success_response({
            "thread_id": thread_id,
            "messages": messages,
            "count": len(messages),
            "user_email": user_email
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch thread: {str(e)}")


@router.get("/gmail/stats")
async def get_gmail_stats(
    user_email: str = Query(..., description="User email address")
):
    """Get Gmail statistics for a user"""
    try:
        # Get valid tokens
        from ...core.database import db_manager
        tokens = db_manager.get_valid_tokens(user_email, "google")
        if not tokens:
            raise HTTPException(status_code=404, detail="No valid tokens found for user")
        
        # Create Gmail API client
        from ...providers.google.gmail import GmailAPI
        gmail_api = GmailAPI(tokens["access_token"])
        
        # Get profile for stats
        profile = await gmail_api.get_profile()
        
        # Get recent messages for count
        messages = await gmail_api.get_messages(max_results=100)
        
        # Calculate stats
        stats = {
            "email_address": profile.get("emailAddress", ""),
            "messages_total": profile.get("messagesTotal", 0),
            "threads_total": profile.get("threadsTotal", 0),
            "recent_messages": len(messages),
            "history_id": profile.get("historyId", ""),
            "user_email": user_email
        }
        
        # Log activity
        db_manager.log_activity(
            user_email, 
            "fetch_stats", 
            {"messages_total": stats["messages_total"]}
        )
        
        return create_success_response(stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@router.get("/gmail/labels/{label_id}")
async def get_gmail_label(
    label_id: str,
    user_email: str = Query(..., description="User email address")
):
    """Get specific Gmail label"""
    try:
        # Get valid tokens
        from ...core.database import db_manager
        tokens = db_manager.get_valid_tokens(user_email, "google")
        if not tokens:
            raise HTTPException(status_code=404, detail="No valid tokens found for user")
        
        # Create Gmail API client
        from ...providers.google.gmail import GmailAPI
        gmail_api = GmailAPI(tokens["access_token"])
        
        # Get label
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{gmail_api.base_url}/labels/{label_id}",
                headers=gmail_api.headers
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Label not found")
            
            label_data = response.json()
        
        # Log activity
        db_manager.log_activity(
            user_email, 
            "fetch_label", 
            {"label_id": label_id, "label_name": label_data.get("name", "")}
        )
        
        return create_success_response({
            "label": label_data,
            "user_email": user_email
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch label: {str(e)}")


@router.get("/gmail/labels/{label_id}/messages")
async def get_gmail_label_messages(
    label_id: str,
    user_email: str = Query(..., description="User email address"),
    max_results: int = Query(10, description="Maximum number of messages to fetch")
):
    """Get messages from a specific Gmail label"""
    try:
        # Get valid tokens
        from ...core.database import db_manager
        tokens = db_manager.get_valid_tokens(user_email, "google")
        if not tokens:
            raise HTTPException(status_code=404, detail="No valid tokens found for user")
        
        # Create Gmail API client
        from ...providers.google.gmail import GmailAPI
        gmail_api = GmailAPI(tokens["access_token"])
        
        # Get messages with label query
        query = f"label:{label_id}"
        messages = await gmail_api.get_messages(max_results, query)
        
        # Log activity
        db_manager.log_activity(
            user_email, 
            "fetch_label_messages", 
            {"label_id": label_id, "count": len(messages)}
        )
        
        return create_success_response({
            "label_id": label_id,
            "messages": messages,
            "count": len(messages),
            "user_email": user_email
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch label messages: {str(e)}") 
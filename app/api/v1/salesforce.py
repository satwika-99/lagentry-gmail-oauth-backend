"""
Salesforce API endpoints for v1
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from typing import Optional, List, Dict, Any
from datetime import datetime
import httpx

from app.core.database import db_manager
from app.core.exceptions import APIError, TokenError, AuthenticationException
from app.schemas.salesforce import (
    SalesforceAuthUrlResponse, SalesforceCallbackResponse, SalesforceServiceStatus,
    SalesforceTokenValidationResponse, SalesforceScopeResponse, SalesforceUserResponse,
    SalesforceAccountListResponse, SalesforceContactListResponse, SalesforceLeadListResponse,
    SalesforceOpportunityListResponse, SalesforceCaseListResponse
)
from app.connectors.salesforce.oauth import get_auth_url, exchange_code_for_token, validate_token, get_user_info
from app.connectors.salesforce.api_client import SalesforceAPIClient
from app.core.config import settings

router = APIRouter(prefix="/salesforce", tags=["Salesforce Services"])


@router.get("/")
async def salesforce_status():
    """Get Salesforce integration status"""
    return {
        "success": True,
        "provider": "salesforce",
        "configured": bool(settings.salesforce_client_id),
        "services": ["accounts", "contacts", "leads", "opportunities", "cases"],
        "endpoints": [
            "/auth-url",
            "/callback",
            "/validate-token",
            "/scopes",
            "/accounts",
            "/contacts",
            "/leads"
        ]
    }


@router.get("")
async def salesforce_status_no_slash():
    """Get Salesforce integration status (no trailing slash)"""
    return {
        "success": True,
        "provider": "salesforce",
        "configured": bool(settings.salesforce_client_id),
        "services": ["accounts", "contacts", "leads", "opportunities", "cases"],
        "endpoints": [
            "/auth-url",
            "/callback",
            "/validate-token",
            "/scopes",
            "/accounts",
            "/contacts",
            "/leads"
        ]
    }


@router.get("/auth-url", response_model=SalesforceAuthUrlResponse)
def salesforce_auth_url(
    user_email: str = Query(..., description="User email"),
    scope: str = Query("api refresh_token", description="OAuth scopes")
):
    """Get Salesforce OAuth URL"""
    try:
        return {"auth_url": get_auth_url(user_email, scope)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callback", response_model=SalesforceCallbackResponse)
async def salesforce_callback(
    code: str = Query(...), 
    state: str = Query(...)
):
    """Handle Salesforce OAuth callback and store tokens"""
    try:
        token_data = await exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = int(token_data.get("expires_in", 7200))  # Salesforce default 2 hours
        scope = token_data.get("scope", "")
        user_email = state
        
        db_manager.store_tokens(user_email, "salesforce", access_token, refresh_token, expires_in, scope.split())
        return {"success": True, "token_data": token_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/validate-token", response_model=SalesforceTokenValidationResponse)
async def validate_salesforce_token(
    user_email: str = Query(..., description="User email")
):
    """Validate Salesforce access token"""
    try:
        validation_result = await validate_token(user_email)
        return validation_result
    except AuthenticationException as e:
        return {
            "valid": False,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "valid": False,
            "message": f"Token validation failed: {str(e)}"
        }


@router.get("/scopes", response_model=SalesforceScopeResponse)
async def get_salesforce_scopes(
    user_email: str = Query(..., description="User email")
):
    """Get current Salesforce OAuth scopes"""
    try:
        client = SalesforceAPIClient(user_email)
        scopes = await client.get_current_scopes()
        return {
            "success": True,
            "scopes": scopes,
            "total_scopes": len(scopes)
        }
    except AuthenticationException as e:
        return {
            "success": False,
            "scopes": [],
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "scopes": [],
            "message": f"Failed to get scopes: {str(e)}"
        }


@router.get("/user", response_model=SalesforceUserResponse)
async def get_salesforce_user(
    user_email: str = Query(..., description="User email")
):
    """Get Salesforce user information"""
    try:
        user_info = await get_user_info(user_email)
        return {
            "success": True,
            "user": user_info
        }
    except AuthenticationException as e:
        return {
            "success": False,
            "user": None,
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "user": None,
            "message": f"Failed to get user info: {str(e)}"
        }


@router.get("/accounts", response_model=SalesforceAccountListResponse)
async def get_salesforce_accounts(
    user_email: str = Query(..., description="User email"),
    limit: int = Query(50, description="Maximum number of accounts to return"),
    offset: int = Query(0, description="Offset for pagination")
):
    """Get Salesforce accounts"""
    try:
        client = SalesforceAPIClient(user_email)
        accounts = await client.get_accounts(limit=limit, offset=offset)
        return {
            "success": True,
            "accounts": accounts,
            "total": len(accounts),
            "limit": limit,
            "offset": offset
        }
    except AuthenticationException as e:
        return {
            "success": False,
            "accounts": [],
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "accounts": [],
            "message": f"Failed to get accounts: {str(e)}"
        }


@router.get("/contacts", response_model=SalesforceContactListResponse)
async def get_salesforce_contacts(
    user_email: str = Query(..., description="User email"),
    limit: int = Query(50, description="Maximum number of contacts to return"),
    offset: int = Query(0, description="Offset for pagination")
):
    """Get Salesforce contacts"""
    try:
        client = SalesforceAPIClient(user_email)
        contacts = await client.get_contacts(limit=limit, offset=offset)
        return {
            "success": True,
            "contacts": contacts,
            "total": len(contacts),
            "limit": limit,
            "offset": offset
        }
    except AuthenticationException as e:
        return {
            "success": False,
            "contacts": [],
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "contacts": [],
            "message": f"Failed to get contacts: {str(e)}"
        }


@router.get("/leads", response_model=SalesforceLeadListResponse)
async def get_salesforce_leads(
    user_email: str = Query(..., description="User email"),
    limit: int = Query(50, description="Maximum number of leads to return"),
    offset: int = Query(0, description="Offset for pagination")
):
    """Get Salesforce leads"""
    try:
        client = SalesforceAPIClient(user_email)
        leads = await client.get_leads(limit=limit, offset=offset)
        return {
            "success": True,
            "leads": leads,
            "total": len(leads),
            "limit": limit,
            "offset": offset
        }
    except AuthenticationException as e:
        return {
            "success": False,
            "leads": [],
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "leads": [],
            "message": f"Failed to get leads: {str(e)}"
        }


@router.get("/opportunities", response_model=SalesforceOpportunityListResponse)
async def get_salesforce_opportunities(
    user_email: str = Query(..., description="User email"),
    limit: int = Query(50, description="Maximum number of opportunities to return"),
    offset: int = Query(0, description="Offset for pagination")
):
    """Get Salesforce opportunities"""
    try:
        client = SalesforceAPIClient(user_email)
        opportunities = await client.get_opportunities(limit=limit, offset=offset)
        return {
            "success": True,
            "opportunities": opportunities,
            "total": len(opportunities),
            "limit": limit,
            "offset": offset
        }
    except AuthenticationException as e:
        return {
            "success": False,
            "opportunities": [],
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "opportunities": [],
            "message": f"Failed to get opportunities: {str(e)}"
        }


@router.get("/cases", response_model=SalesforceCaseListResponse)
async def get_salesforce_cases(
    user_email: str = Query(..., description="User email"),
    limit: int = Query(50, description="Maximum number of cases to return"),
    offset: int = Query(0, description="Offset for pagination")
):
    """Get Salesforce cases"""
    try:
        client = SalesforceAPIClient(user_email)
        cases = await client.get_cases(limit=limit, offset=offset)
        return {
            "success": True,
            "cases": cases,
            "total": len(cases),
            "limit": limit,
            "offset": offset
        }
    except AuthenticationException as e:
        return {
            "success": False,
            "cases": [],
            "message": "No authentication tokens found. Please authenticate first.",
            "auth_required": True
        }
    except Exception as e:
        return {
            "success": False,
            "cases": [],
            "message": f"Failed to get cases: {str(e)}"
        }


@router.get("/status", response_model=SalesforceServiceStatus)
async def salesforce_status():
    """Get Salesforce integration status"""
    return {
        "success": True,
        "provider": "salesforce",
        "configured": bool(settings.salesforce_client_id and settings.salesforce_client_secret),
        "services": ["accounts", "contacts", "leads", "opportunities", "cases"],
        "endpoints": [
            "/auth-url",
            "/callback",
            "/validate-token",
            "/scopes",
            "/user",
            "/accounts",
            "/contacts",
            "/leads",
            "/opportunities",
            "/cases"
        ]
    }

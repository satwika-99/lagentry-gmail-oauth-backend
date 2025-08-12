"""
Salesforce API client for data operations
"""

import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime

from core.database import db_manager
from core.exceptions import AuthenticationException, APIError
from connectors.salesforce.oauth import refresh_access_token


class SalesforceAPIClient:
    """Salesforce API client for data operations"""
    
    def __init__(self, user_email: str):
        self.user_email = user_email
        self.access_token = None
        self.instance_url = None
        self.api_version = "v59.0"  # Latest stable API version
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the client with stored tokens"""
        tokens = db_manager.get_tokens(self.user_email, "salesforce")
        if not tokens:
            raise AuthenticationException("No Salesforce tokens found")
        
        self.access_token = tokens.get("access_token")
        self.instance_url = tokens.get("instance_url")
        
        if not self.access_token or not self.instance_url:
            raise AuthenticationException("Invalid token data")
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Salesforce API"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.instance_url}/services/data/{self.api_version}/{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, headers=headers, **kwargs)
                
                if response.status_code == 401:
                    # Token expired, try to refresh
                    await self._refresh_token()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = await client.request(method, url, headers=headers, **kwargs)
                
                if response.status_code >= 400:
                    raise APIError(f"Salesforce API error: {response.status_code} - {response.text}")
                
                return response.json() if response.content else {}
                
        except httpx.RequestError as e:
            raise APIError(f"Request error: {str(e)}")
    
    async def _refresh_token(self):
        """Refresh access token"""
        try:
            token_data = await refresh_access_token(self.user_email)
            self.access_token = token_data.get("access_token")
            self.instance_url = token_data.get("instance_url")
        except Exception as e:
            raise AuthenticationException(f"Token refresh failed: {str(e)}")
    
    async def get_current_scopes(self) -> List[str]:
        """Get current OAuth scopes"""
        tokens = db_manager.get_tokens(self.user_email, "salesforce")
        return tokens.get("scopes", []) if tokens else []
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get Salesforce service status"""
        try:
            # Test connection by getting user info
            user_info = await self._make_request("GET", "sobjects/User/describe")
            return {
                "service": "salesforce",
                "status": "connected",
                "message": "Successfully connected to Salesforce",
                "timestamp": datetime.now().isoformat(),
                "instance_url": self.instance_url,
                "api_version": self.api_version
            }
        except Exception as e:
            return {
                "service": "salesforce",
                "status": "error",
                "message": f"Connection error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "instance_url": self.instance_url,
                "api_version": self.api_version
            }
    
    async def get_accounts(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get Salesforce accounts"""
        try:
            query = f"SELECT Id, Name, Type, Industry, BillingStreet, BillingCity, BillingState, BillingPostalCode, BillingCountry, Phone, Website, Description, CreatedDate, LastModifiedDate FROM Account ORDER BY Name LIMIT {limit} OFFSET {offset}"
            result = await self._make_request("GET", f"query?q={query}")
            
            return result.get("records", [])
        except Exception as e:
            return []
    
    async def get_contacts(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get Salesforce contacts"""
        try:
            query = f"SELECT Id, FirstName, LastName, Email, Phone, Title, Department, AccountId, Account.Name, MailingStreet, MailingCity, MailingState, MailingPostalCode, MailingCountry, CreatedDate, LastModifiedDate FROM Contact ORDER BY LastName, FirstName LIMIT {limit} OFFSET {offset}"
            result = await self._make_request("GET", f"query?q={query}")
            
            return result.get("records", [])
        except Exception as e:
            return []
    
    async def get_leads(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get Salesforce leads"""
        try:
            query = f"SELECT Id, FirstName, LastName, Company, Email, Phone, Title, Status, LeadSource, Industry, Description, Street, City, State, PostalCode, Country, CreatedDate, LastModifiedDate FROM Lead ORDER BY LastName, FirstName LIMIT {limit} OFFSET {offset}"
            result = await self._make_request("GET", f"query?q={query}")
            
            return result.get("records", [])
        except Exception as e:
            return []
    
    async def get_opportunities(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get Salesforce opportunities"""
        try:
            query = f"SELECT Id, Name, Amount, StageName, Type, CloseDate, Probability, Description, AccountId, Account.Name, LeadSource, CreatedDate, LastModifiedDate FROM Opportunity ORDER BY CloseDate DESC LIMIT {limit} OFFSET {offset}"
            result = await self._make_request("GET", f"query?q={query}")
            
            return result.get("records", [])
        except Exception as e:
            return []
    
    async def get_cases(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get Salesforce cases"""
        try:
            query = f"SELECT Id, CaseNumber, Subject, Status, Priority, Type, Description, AccountId, Account.Name, ContactId, Contact.Name, Origin, Reason, CreatedDate, LastModifiedDate FROM Case ORDER BY CreatedDate DESC LIMIT {limit} OFFSET {offset}"
            result = await self._make_request("GET", f"query?q={query}")
            
            return result.get("records", [])
        except Exception as e:
            return []
    
    async def search(self, query: str, object_types: List[str] = None) -> Dict[str, Any]:
        """Search Salesforce records"""
        try:
            if object_types is None:
                object_types = ["Account", "Contact", "Lead", "Opportunity"]
            
            # Build search query
            search_query = f"FIND {{{query}}} IN ALL FIELDS RETURNING {','.join(object_types)}"
            
            result = await self._make_request("GET", f"search?q={search_query}")
            
            return {
                "success": True,
                "results": result.get("searchRecords", []),
                "total": len(result.get("searchRecords", []))
            }
        except Exception as e:
            return {
                "success": False,
                "results": [],
                "total": 0,
                "message": f"Error: {str(e)}"
            }
    
    async def create_record(self, object_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Salesforce record"""
        try:
            result = await self._make_request("POST", f"sobjects/{object_type}", json=data)
            return {
                "success": True,
                "id": result.get("id"),
                "message": "Record created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "id": None,
                "message": f"Error: {str(e)}"
            }
    
    async def update_record(self, object_type: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a Salesforce record"""
        try:
            await self._make_request("PATCH", f"sobjects/{object_type}/{record_id}", json=data)
            return {
                "success": True,
                "message": "Record updated successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    async def delete_record(self, object_type: str, record_id: str) -> Dict[str, Any]:
        """Delete a Salesforce record"""
        try:
            await self._make_request("DELETE", f"sobjects/{object_type}/{record_id}")
            return {
                "success": True,
                "message": "Record deleted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    async def get_object_describe(self, object_type: str) -> Dict[str, Any]:
        """Get object metadata and field descriptions"""
        try:
            result = await self._make_request("GET", f"sobjects/{object_type}/describe")
            return {
                "success": True,
                "object_info": result
            }
        except Exception as e:
            return {
                "success": False,
                "object_info": None,
                "message": f"Error: {str(e)}"
            }
    
    async def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh the access token"""
        try:
            token_data = await refresh_access_token(self.user_email)
            self.access_token = token_data.get("access_token")
            return token_data
        except Exception as e:
            raise AuthenticationException(f"Token refresh failed: {str(e)}")

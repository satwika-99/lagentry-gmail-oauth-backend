"""
Salesforce API schemas and data models
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# OAuth Response Models
class SalesforceAuthUrlResponse(BaseModel):
    """Response model for Salesforce OAuth URL"""
    auth_url: str = Field(..., description="Salesforce OAuth authorization URL")


class SalesforceCallbackResponse(BaseModel):
    """Response model for Salesforce OAuth callback"""
    success: bool = Field(..., description="Whether the OAuth flow was successful")
    token_data: Optional[Dict[str, Any]] = Field(None, description="Token data from Salesforce")


class SalesforceTokenValidationResponse(BaseModel):
    """Response model for token validation"""
    valid: bool = Field(..., description="Whether the token is valid")
    message: Optional[str] = Field(None, description="Validation message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")
    scopes: Optional[List[str]] = Field(None, description="Token scopes")


class SalesforceScopeResponse(BaseModel):
    """Response model for OAuth scopes"""
    success: bool = Field(..., description="Whether the request was successful")
    scopes: List[str] = Field(..., description="List of OAuth scopes")
    total_scopes: int = Field(..., description="Total number of scopes")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


class SalesforceUserResponse(BaseModel):
    """Response model for Salesforce user information"""
    success: bool = Field(..., description="Whether the request was successful")
    user: Optional[Dict[str, Any]] = Field(None, description="User information")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


# Service Status Models
class SalesforceServiceStatus(BaseModel):
    """Response model for Salesforce service status"""
    success: bool = Field(..., description="Whether the request was successful")
    provider: str = Field("salesforce", description="Service name")
    configured: bool = Field(..., description="Whether the service is configured")
    services: List[str] = Field(..., description="Available services")
    endpoints: List[str] = Field(..., description="Available endpoints")


# Salesforce Object Models
class SalesforceAccount(BaseModel):
    """Salesforce Account object model"""
    Id: Optional[str] = Field(None, description="Account ID")
    Name: Optional[str] = Field(None, description="Account name")
    Type: Optional[str] = Field(None, description="Account type")
    Industry: Optional[str] = Field(None, description="Account industry")
    BillingStreet: Optional[str] = Field(None, description="Billing street")
    BillingCity: Optional[str] = Field(None, description="Billing city")
    BillingState: Optional[str] = Field(None, description="Billing state")
    BillingPostalCode: Optional[str] = Field(None, description="Billing postal code")
    BillingCountry: Optional[str] = Field(None, description="Billing country")
    Phone: Optional[str] = Field(None, description="Account phone")
    Website: Optional[str] = Field(None, description="Account website")
    Description: Optional[str] = Field(None, description="Account description")
    CreatedDate: Optional[datetime] = Field(None, description="Creation date")
    LastModifiedDate: Optional[datetime] = Field(None, description="Last modified date")


class SalesforceContact(BaseModel):
    """Salesforce Contact object model"""
    Id: Optional[str] = Field(None, description="Contact ID")
    FirstName: Optional[str] = Field(None, description="First name")
    LastName: Optional[str] = Field(None, description="Last name")
    Email: Optional[str] = Field(None, description="Email address")
    Phone: Optional[str] = Field(None, description="Phone number")
    Title: Optional[str] = Field(None, description="Job title")
    Department: Optional[str] = Field(None, description="Department")
    AccountId: Optional[str] = Field(None, description="Associated account ID")
    Account: Optional[Dict[str, Any]] = Field(None, description="Associated account")
    MailingStreet: Optional[str] = Field(None, description="Mailing street")
    MailingCity: Optional[str] = Field(None, description="Mailing city")
    MailingState: Optional[str] = Field(None, description="Mailing state")
    MailingPostalCode: Optional[str] = Field(None, description="Mailing postal code")
    MailingCountry: Optional[str] = Field(None, description="Mailing country")
    CreatedDate: Optional[datetime] = Field(None, description="Creation date")
    LastModifiedDate: Optional[datetime] = Field(None, description="Last modified date")


class SalesforceLead(BaseModel):
    """Salesforce Lead object model"""
    Id: Optional[str] = Field(None, description="Lead ID")
    FirstName: Optional[str] = Field(None, description="First name")
    LastName: Optional[str] = Field(None, description="Last name")
    Company: Optional[str] = Field(None, description="Company name")
    Email: Optional[str] = Field(None, description="Email address")
    Phone: Optional[str] = Field(None, description="Phone number")
    Title: Optional[str] = Field(None, description="Job title")
    Status: Optional[str] = Field(None, description="Lead status")
    LeadSource: Optional[str] = Field(None, description="Lead source")
    Industry: Optional[str] = Field(None, description="Industry")
    Description: Optional[str] = Field(None, description="Lead description")
    Street: Optional[str] = Field(None, description="Street address")
    City: Optional[str] = Field(None, description="City")
    State: Optional[str] = Field(None, description="State")
    PostalCode: Optional[str] = Field(None, description="Postal code")
    Country: Optional[str] = Field(None, description="Country")
    CreatedDate: Optional[datetime] = Field(None, description="Creation date")
    LastModifiedDate: Optional[datetime] = Field(None, description="Last modified date")


class SalesforceOpportunity(BaseModel):
    """Salesforce Opportunity object model"""
    Id: Optional[str] = Field(None, description="Opportunity ID")
    Name: Optional[str] = Field(None, description="Opportunity name")
    Amount: Optional[float] = Field(None, description="Opportunity amount")
    StageName: Optional[str] = Field(None, description="Opportunity stage")
    Type: Optional[str] = Field(None, description="Opportunity type")
    CloseDate: Optional[datetime] = Field(None, description="Close date")
    Probability: Optional[float] = Field(None, description="Probability percentage")
    Description: Optional[str] = Field(None, description="Opportunity description")
    AccountId: Optional[str] = Field(None, description="Associated account ID")
    Account: Optional[Dict[str, Any]] = Field(None, description="Associated account")
    LeadSource: Optional[str] = Field(None, description="Lead source")
    CreatedDate: Optional[datetime] = Field(None, description="Creation date")
    LastModifiedDate: Optional[datetime] = Field(None, description="Last modified date")


class SalesforceCase(BaseModel):
    """Salesforce Case object model"""
    Id: Optional[str] = Field(None, description="Case ID")
    CaseNumber: Optional[str] = Field(None, description="Case number")
    Subject: Optional[str] = Field(None, description="Case subject")
    Status: Optional[str] = Field(None, description="Case status")
    Priority: Optional[str] = Field(None, description="Case priority")
    Type: Optional[str] = Field(None, description="Case type")
    Description: Optional[str] = Field(None, description="Case description")
    AccountId: Optional[str] = Field(None, description="Associated account ID")
    Account: Optional[Dict[str, Any]] = Field(None, description="Associated account")
    ContactId: Optional[str] = Field(None, description="Associated contact ID")
    Contact: Optional[Dict[str, Any]] = Field(None, description="Associated contact")
    Origin: Optional[str] = Field(None, description="Case origin")
    Reason: Optional[str] = Field(None, description="Case reason")
    CreatedDate: Optional[datetime] = Field(None, description="Creation date")
    LastModifiedDate: Optional[datetime] = Field(None, description="Last modified date")


# List Response Models
class SalesforceAccountListResponse(BaseModel):
    """Response model for Salesforce accounts list"""
    success: bool = Field(..., description="Whether the request was successful")
    accounts: List[SalesforceAccount] = Field(..., description="List of accounts")
    total: int = Field(..., description="Total number of accounts")
    limit: int = Field(..., description="Request limit")
    offset: int = Field(..., description="Request offset")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


class SalesforceContactListResponse(BaseModel):
    """Response model for Salesforce contacts list"""
    success: bool = Field(..., description="Whether the request was successful")
    contacts: List[SalesforceContact] = Field(..., description="List of contacts")
    total: int = Field(..., description="Total number of contacts")
    limit: int = Field(..., description="Request limit")
    offset: int = Field(..., description="Request offset")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


class SalesforceLeadListResponse(BaseModel):
    """Response model for Salesforce leads list"""
    success: bool = Field(..., description="Whether the request was successful")
    leads: List[SalesforceLead] = Field(..., description="List of leads")
    total: int = Field(..., description="Total number of leads")
    limit: int = Field(..., description="Request limit")
    offset: int = Field(..., description="Request offset")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


class SalesforceOpportunityListResponse(BaseModel):
    """Response model for Salesforce opportunities list"""
    success: bool = Field(..., description="Whether the request was successful")
    opportunities: List[SalesforceOpportunity] = Field(..., description="List of opportunities")
    total: int = Field(..., description="Total number of opportunities")
    limit: int = Field(..., description="Request limit")
    offset: int = Field(..., description="Request offset")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


class SalesforceCaseListResponse(BaseModel):
    """Response model for Salesforce cases list"""
    success: bool = Field(..., description="Whether the request was successful")
    cases: List[SalesforceCase] = Field(..., description="List of cases")
    total: int = Field(..., description="Total number of cases")
    limit: int = Field(..., description="Request limit")
    offset: int = Field(..., description="Request offset")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


# Search Response Models
class SalesforceSearchResult(BaseModel):
    """Model for Salesforce search results"""
    Id: str = Field(..., description="Record ID")
    Name: Optional[str] = Field(None, description="Record name")
    Type: str = Field(..., description="Object type")
    Url: str = Field(..., description="Record URL")
    attributes: Dict[str, Any] = Field(..., description="Record attributes")


class SalesforceSearchResponse(BaseModel):
    """Response model for Salesforce search"""
    success: bool = Field(..., description="Whether the search was successful")
    results: List[SalesforceSearchResult] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(False, description="Whether authentication is required")


# OAuth Configuration Models
class SalesforceOAuthConfig(BaseModel):
    """Salesforce OAuth configuration model"""
    client_id: str = Field(..., description="Salesforce client ID")
    client_secret: str = Field(..., description="Salesforce client secret")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    instance_url: str = Field(..., description="Salesforce instance URL")
    auth_url: str = Field(..., description="Salesforce authorization URL")
    token_url: str = Field(..., description="Salesforce token URL")
    default_scopes: List[str] = Field(
        default=["api", "refresh_token", "offline_access"],
        description="Default OAuth scopes"
    )

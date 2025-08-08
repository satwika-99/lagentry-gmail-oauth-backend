"""
Notion API Schemas
Pydantic models for Notion API responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# Base Models
class NotionRichText(BaseModel):
    """Notion rich text object"""
    type: str = Field(..., description="Type of rich text (text, mention, equation)")
    text: Optional[Dict[str, Any]] = Field(None, description="Text content")
    annotations: Optional[Dict[str, Any]] = Field(None, description="Text annotations")
    plain_text: str = Field(..., description="Plain text content")
    href: Optional[str] = Field(None, description="Link URL")

class NotionTitle(BaseModel):
    """Notion title object"""
    type: str = Field(..., description="Type of title")
    title: List[NotionRichText] = Field(..., description="Title content")

class NotionDescription(BaseModel):
    """Notion description object"""
    type: str = Field(..., description="Type of description")
    rich_text: List[NotionRichText] = Field(..., description="Description content")

# Database Models
class NotionDatabase(BaseModel):
    """Notion database object"""
    id: str = Field(..., description="Database ID")
    title: str = Field(..., description="Database title")
    description: str = Field(..., description="Database description")
    url: str = Field(..., description="Database URL")
    properties: Dict[str, Any] = Field(..., description="Database properties")
    created_time: datetime = Field(..., description="Creation timestamp")
    last_edited_time: datetime = Field(..., description="Last edit timestamp")

class NotionDatabaseListResponse(BaseModel):
    """Response for database list/search"""
    success: bool = Field(..., description="Operation success status")
    databases: List[NotionDatabase] = Field(..., description="List of databases")
    total: int = Field(..., description="Total number of databases")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")

class NotionDatabaseResponse(BaseModel):
    """Response for single database"""
    success: bool = Field(..., description="Operation success status")
    database: Optional[NotionDatabase] = Field(None, description="Database object")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")

# Page Models
class NotionPage(BaseModel):
    """Notion page object"""
    id: str = Field(..., description="Page ID")
    title: str = Field(..., description="Page title")
    url: str = Field(..., description="Page URL")
    created_time: datetime = Field(..., description="Creation timestamp")
    last_edited_time: datetime = Field(..., description="Last edit timestamp")
    properties: Dict[str, Any] = Field(..., description="Page properties")
    parent: Optional[Dict[str, Any]] = Field(None, description="Parent object")

class NotionPageListResponse(BaseModel):
    """Response for page list/search"""
    success: bool = Field(..., description="Operation success status")
    pages: List[NotionPage] = Field(..., description="List of pages")
    total: int = Field(..., description="Total number of pages")
    has_more: Optional[bool] = Field(None, description="Whether there are more pages")
    next_cursor: Optional[str] = Field(None, description="Next page cursor")
    query: Optional[str] = Field(None, description="Search query used")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")

class NotionPageResponse(BaseModel):
    """Response for single page"""
    success: bool = Field(..., description="Operation success status")
    page: Optional[NotionPage] = Field(None, description="Page object")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")

# Block Models
class NotionBlock(BaseModel):
    """Notion block object"""
    id: str = Field(..., description="Block ID")
    type: str = Field(..., description="Block type")
    content: Dict[str, Any] = Field(..., description="Block content")
    has_children: bool = Field(..., description="Whether block has children")
    created_time: datetime = Field(..., description="Creation timestamp")
    last_edited_time: datetime = Field(..., description="Last edit timestamp")

class NotionBlockListResponse(BaseModel):
    """Response for block list"""
    success: bool = Field(..., description="Operation success status")
    blocks: List[NotionBlock] = Field(..., description="List of blocks")
    total: int = Field(..., description="Total number of blocks")
    has_more: Optional[bool] = Field(None, description="Whether there are more blocks")
    next_cursor: Optional[str] = Field(None, description="Next page cursor")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")

# User Models
class NotionUser(BaseModel):
    """Notion user object"""
    id: str = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="User name")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    type: str = Field(..., description="User type")
    person: Optional[Dict[str, Any]] = Field(None, description="Person details")

class NotionUserResponse(BaseModel):
    """Response for user information"""
    success: bool = Field(..., description="Operation success status")
    user: Optional[NotionUser] = Field(None, description="User object")
    message: Optional[str] = Field(None, description="Response message")
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")

# OAuth Models
class NotionAuthUrlResponse(BaseModel):
    """Response for OAuth URL generation"""
    auth_url: str = Field(..., description="OAuth authorization URL")

class NotionCallbackResponse(BaseModel):
    """Response for OAuth callback"""
    success: bool = Field(..., description="Operation success status")
    token_data: Dict[str, Any] = Field(..., description="Token information")

# Status Models
class NotionServiceStatus(BaseModel):
    """Notion service status"""
    success: bool = Field(..., description="Operation success status")
    provider: str = Field(..., description="Service provider name")
    connected: bool = Field(..., description="Connection status")
    services: Dict[str, str] = Field(..., description="Available services")
    message: str = Field(..., description="Status message")

# Error Models
class NotionError(BaseModel):
    """Notion API error"""
    error: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")

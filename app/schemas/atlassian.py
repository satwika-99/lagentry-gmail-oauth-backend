"""
Atlassian Pydantic Schemas
Defines response models for Atlassian services (Jira, Confluence, Bitbucket)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# Jira Schemas
class ProjectInfo(BaseModel):
    """Jira project information"""
    id: str = Field(..., description="Project ID")
    key: str = Field(..., description="Project key")
    name: str = Field(..., description="Project name")
    projectTypeKey: Optional[str] = Field(None, description="Project type")
    simplified: Optional[bool] = Field(None, description="Simplified project")
    style: Optional[str] = Field(None, description="Project style")
    isPrivate: Optional[bool] = Field(None, description="Is private project")


class ProjectListResponse(BaseModel):
    """Response model for Jira project list"""
    success: bool = Field(..., description="Operation success status")
    projects: List[Dict[str, Any]] = Field(default_factory=list, description="List of Jira projects")
    total: int = Field(0, description="Total number of projects")
    max_results: int = Field(50, description="Maximum results requested")


class IssueInfo(BaseModel):
    """Jira issue information"""
    id: str = Field(..., description="Issue ID")
    key: str = Field(..., description="Issue key")
    fields: Dict[str, Any] = Field(..., description="Issue fields")
    self: Optional[str] = Field(None, description="Issue URL")


class IssueListResponse(BaseModel):
    """Response model for Jira issue list"""
    success: bool = Field(..., description="Operation success status")
    issues: List[Dict[str, Any]] = Field(default_factory=list, description="List of Jira issues")
    total: int = Field(0, description="Total number of issues")
    max_results: int = Field(50, description="Maximum results requested")
    jql: Optional[str] = Field(None, description="JQL query used")


class IssueDetailResponse(BaseModel):
    """Response model for Jira issue details"""
    success: bool = Field(..., description="Operation success status")
    issue: Dict[str, Any] = Field(..., description="Jira issue details")


class IssueCreateRequest(BaseModel):
    """Request model for creating Jira issues"""
    project_key: str = Field(..., description="Project key")
    summary: str = Field(..., description="Issue summary")
    description: str = Field(..., description="Issue description")
    issue_type: str = Field("Task", description="Issue type")


class IssueUpdateRequest(BaseModel):
    """Request model for updating Jira issues"""
    updates: Dict[str, Any] = Field(..., description="Fields to update")


class UserInfoResponse(BaseModel):
    """Response model for Jira user information"""
    success: bool = Field(..., description="Operation success status")
    user_info: Dict[str, Any] = Field(..., description="User information")


# Confluence Schemas
class SpaceInfo(BaseModel):
    """Confluence space information"""
    id: int = Field(..., description="Space ID")
    key: str = Field(..., description="Space key")
    name: str = Field(..., description="Space name")
    type: str = Field(..., description="Space type")
    status: str = Field(..., description="Space status")


class SpaceListResponse(BaseModel):
    """Response model for Confluence space list"""
    success: bool = Field(..., description="Operation success status")
    spaces: List[Dict[str, Any]] = Field(default_factory=list, description="List of Confluence spaces")
    total: int = Field(0, description="Total number of spaces")


class PageInfo(BaseModel):
    """Confluence page information"""
    id: str = Field(..., description="Page ID")
    title: str = Field(..., description="Page title")
    spaceId: int = Field(..., description="Space ID")
    status: str = Field(..., description="Page status")
    version: Dict[str, Any] = Field(..., description="Page version")


class PageListResponse(BaseModel):
    """Response model for Confluence page list"""
    success: bool = Field(..., description="Operation success status")
    pages: List[Dict[str, Any]] = Field(default_factory=list, description="List of Confluence pages")
    total: int = Field(0, description="Total number of pages")


# Bitbucket Schemas
class RepositoryInfo(BaseModel):
    """Bitbucket repository information"""
    uuid: str = Field(..., description="Repository UUID")
    name: str = Field(..., description="Repository name")
    slug: str = Field(..., description="Repository slug")
    project: Dict[str, Any] = Field(..., description="Project information")
    links: Dict[str, Any] = Field(..., description="Repository links")


class RepositoryListResponse(BaseModel):
    """Response model for Bitbucket repository list"""
    success: bool = Field(..., description="Operation success status")
    repositories: List[Dict[str, Any]] = Field(default_factory=list, description="List of Bitbucket repositories")
    total: int = Field(0, description="Total number of repositories")


class PullRequestInfo(BaseModel):
    """Bitbucket pull request information"""
    id: int = Field(..., description="Pull request ID")
    title: str = Field(..., description="Pull request title")
    state: str = Field(..., description="Pull request state")
    author: Dict[str, Any] = Field(..., description="Author information")
    source: Dict[str, Any] = Field(..., description="Source branch")
    destination: Dict[str, Any] = Field(..., description="Destination branch")


class PullRequestListResponse(BaseModel):
    """Response model for Bitbucket pull request list"""
    success: bool = Field(..., description="Operation success status")
    pull_requests: List[Dict[str, Any]] = Field(default_factory=list, description="List of pull requests")
    total: int = Field(0, description="Total number of pull requests")


# Common Atlassian Schemas
class AtlassianStatusResponse(BaseModel):
    """Response model for Atlassian service status"""
    success: bool = Field(..., description="Operation success status")
    provider: str = Field("atlassian", description="Provider name")
    configured: bool = Field(..., description="Whether provider is configured")
    services: List[str] = Field(..., description="Available services")
    endpoints: List[str] = Field(..., description="Available endpoints") 
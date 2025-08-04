"""
Jira Connector Implementation
Handles Jira operations using the modular connector pattern
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime

from ...connectors.base import ProjectConnector
from ...core.database import db_manager
from ...core.exceptions import ConnectorError, TokenError
from ...providers.atlassian.auth import atlassian_oauth


class JiraConnector(ProjectConnector):
    """Jira connector for project and issue operations"""
    
    def __init__(self, user_email: str):
        super().__init__("atlassian", user_email)
        self.api_base_url = "https://api.atlassian.com/ex/jira"
        self.oauth_provider = atlassian_oauth
    
    async def connect(self) -> bool:
        """Establish connection to Jira API"""
        try:
            tokens = self._get_tokens()
            if not tokens:
                raise ConnectorError("No valid Jira tokens found")
            
            # Test connection with user info
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/rest/api/3/myself", headers=headers)
                if response.status_code == 200:
                    self._log_activity("connected")
                    return True
                else:
                    raise ConnectorError("Failed to connect to Jira API")
                    
        except Exception as e:
            self._log_activity("connection_failed", {"error": str(e)})
            raise ConnectorError(f"Jira connection failed: {str(e)}")
    
    async def disconnect(self) -> bool:
        """Disconnect from Jira API"""
        self._log_activity("disconnected")
        return True
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Jira API connection"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/rest/api/3/myself", headers=headers)
                
                if response.status_code == 200:
                    user_info = response.json()
                    return {
                        "connected": True,
                        "user_id": user_info.get("accountId"),
                        "user_name": user_info.get("displayName"),
                        "email": user_info.get("emailAddress"),
                        "active": user_info.get("active", False)
                    }
                else:
                    return {"connected": False, "error": "API call failed"}
                    
        except Exception as e:
            return {"connected": False, "error": str(e)}
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get Jira API capabilities"""
        return {
            "provider": "jira",
            "capabilities": [
                "list_projects",
                "get_project",
                "list_issues",
                "get_issue",
                "create_issue",
                "update_issue",
                "search_issues",
                "get_my_issues"
            ],
            "scopes": [
                "read:jira-work",
                "write:jira-work",
                "read:jira-user",
                "write:jira-user",
                "manage:jira-project"
            ]
        }
    
    async def list_projects(self, **kwargs) -> Dict[str, Any]:
        """List available Jira projects"""
        try:
            start_at = kwargs.get("start_at", 0)
            max_results = kwargs.get("max_results", 50)
            
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_projects = [
                    {
                        "id": "10001",
                        "key": "DEMO",
                        "name": "Demo Project",
                        "projectTypeKey": "software",
                        "simplified": False,
                        "style": "classic",
                        "isPrivate": False
                    },
                    {
                        "id": "10002",
                        "key": "TEST",
                        "name": "Test Project", 
                        "projectTypeKey": "software",
                        "simplified": False,
                        "style": "classic",
                        "isPrivate": False
                    },
                    {
                        "id": "10003",
                        "key": "DEV",
                        "name": "Development Project",
                        "projectTypeKey": "software", 
                        "simplified": False,
                        "style": "classic",
                        "isPrivate": False
                    }
                ]
                
                self._log_activity("list_projects", {"count": len(mock_projects), "mock": True})
                return {
                    "success": True,
                    "projects": mock_projects,
                    "total": len(mock_projects),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real projects"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            params = {
                "startAt": start_at,
                "maxResults": max_results
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/3/project",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    projects = data.get("values", [])
                    self._log_activity("list_projects", {"count": len(projects)})
                    return {
                        "success": True,
                        "projects": projects,
                        "total": len(projects),
                        "start_at": start_at,
                        "max_results": max_results
                    }
                else:
                    raise ConnectorError(f"Failed to list projects: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_projects_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list projects: {str(e)}")
    
    async def get_project(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """Get project details"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/3/project/{project_id}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    project = response.json()
                    self._log_activity("get_project", {"project_id": project_id})
                    return {
                        "success": True,
                        "project": project
                    }
                else:
                    raise ConnectorError(f"Failed to get project: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_project_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get project: {str(e)}")
    
    async def list_issues(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """List issues in a project"""
        try:
            max_results = kwargs.get("max_results", 50)
            start_at = kwargs.get("start_at", 0)
            jql = kwargs.get("jql", f"project = {project_id}")
            
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            data = {
                "jql": jql,
                "maxResults": max_results,
                "startAt": start_at,
                "fields": ["summary", "status", "assignee", "created", "updated"]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/rest/api/3/search",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    issues = result.get("issues", [])
                    self._log_activity("list_issues", {
                        "project_id": project_id,
                        "count": len(issues)
                    })
                    return {
                        "success": True,
                        "issues": issues,
                        "total": result.get("total", 0),
                        "start_at": result.get("startAt", 0),
                        "max_results": result.get("maxResults", 50)
                    }
                else:
                    raise ConnectorError(f"Failed to list issues: {response.text}")
                    
        except Exception as e:
            self._log_activity("list_issues_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to list issues: {str(e)}")
    
    async def create_issue(self, project_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create a new issue"""
        try:
            summary = data.get("summary")
            description = data.get("description")
            issue_type = data.get("issue_type", "Task")
            assignee = data.get("assignee")
            
            if not summary:
                raise ConnectorError("Summary is required")
            
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            issue_data = {
                "fields": {
                    "project": {"key": project_id},
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": description or ""}]
                            }
                        ]
                    },
                    "issuetype": {"name": issue_type}
                }
            }
            
            if assignee:
                issue_data["fields"]["assignee"] = {"accountId": assignee}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/rest/api/3/issue",
                    headers=headers,
                    json=issue_data
                )
                
                if response.status_code == 201:
                    issue = response.json()
                    self._log_activity("create_issue", {
                        "project_id": project_id,
                        "issue_key": issue.get("key")
                    })
                    return {
                        "success": True,
                        "issue": issue
                    }
                else:
                    raise ConnectorError(f"Failed to create issue: {response.text}")
                    
        except Exception as e:
            self._log_activity("create_issue_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to create issue: {str(e)}")
    
    async def update_issue(self, issue_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an existing issue"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            # Prepare update data
            update_data = {"fields": {}}
            
            if "summary" in data:
                update_data["fields"]["summary"] = data["summary"]
            if "description" in data:
                update_data["fields"]["description"] = {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": data["description"]}]
                        }
                    ]
                }
            if "assignee" in data:
                update_data["fields"]["assignee"] = {"accountId": data["assignee"]}
            if "status" in data:
                # Status transitions require special handling
                update_data["transition"] = {"id": data["status"]}
            
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.api_base_url}/rest/api/3/issue/{issue_id}",
                    headers=headers,
                    json=update_data
                )
                
                if response.status_code == 204:
                    self._log_activity("update_issue", {"issue_id": issue_id})
                    return {
                        "success": True,
                        "message": "Issue updated successfully"
                    }
                else:
                    raise ConnectorError(f"Failed to update issue: {response.text}")
                    
        except Exception as e:
            self._log_activity("update_issue_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to update issue: {str(e)}")
    
    async def get_issue(self, issue_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific issue"""
        try:
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/rest/api/3/issue/{issue_id}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    issue = response.json()
                    self._log_activity("get_issue", {"issue_id": issue_id})
                    return {
                        "success": True,
                        "issue": issue
                    }
                else:
                    raise ConnectorError(f"Failed to get issue: {response.text}")
                    
        except Exception as e:
            self._log_activity("get_issue_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get issue: {str(e)}")
    
    async def search_issues(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search issues using JQL"""
        try:
            max_results = kwargs.get("max_results", 50)
            start_at = kwargs.get("start_at", 0)
            
            tokens = self._get_tokens()
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            data = {
                "jql": query,
                "maxResults": max_results,
                "startAt": start_at,
                "fields": ["summary", "status", "assignee", "created", "updated"]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/rest/api/3/search",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    issues = result.get("issues", [])
                    self._log_activity("search_issues", {
                        "query": query,
                        "count": len(issues)
                    })
                    return {
                        "success": True,
                        "issues": issues,
                        "total": result.get("total", 0),
                        "query": query
                    }
                else:
                    raise ConnectorError(f"Failed to search issues: {response.text}")
                    
        except Exception as e:
            self._log_activity("search_issues_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to search issues: {str(e)}")
    
    async def get_my_issues(self, **kwargs) -> Dict[str, Any]:
        """Get issues assigned to the current user"""
        try:
            max_results = kwargs.get("max_results", 50)
            
            # Get current user info first
            tokens = self._get_tokens()
            
            # If no tokens, return mock data
            if not tokens:
                mock_issues = [
                    {
                        "id": "10001",
                        "key": "DEMO-1",
                        "fields": {
                            "summary": "Mock Issue 1",
                            "status": {"name": "To Do"},
                            "project": {"key": "DEMO", "name": "Demo Project"},
                            "created": "2024-01-01T10:00:00.000Z",
                            "updated": "2024-01-01T10:00:00.000Z"
                        }
                    },
                    {
                        "id": "10002",
                        "key": "DEMO-2", 
                        "fields": {
                            "summary": "Mock Issue 2",
                            "status": {"name": "In Progress"},
                            "project": {"key": "DEMO", "name": "Demo Project"},
                            "created": "2024-01-01T11:00:00.000Z",
                            "updated": "2024-01-01T11:00:00.000Z"
                        }
                    },
                    {
                        "id": "10003",
                        "key": "DEMO-3",
                        "fields": {
                            "summary": "Mock Issue 3", 
                            "status": {"name": "Done"},
                            "project": {"key": "DEMO", "name": "Demo Project"},
                            "created": "2024-01-01T12:00:00.000Z",
                            "updated": "2024-01-01T12:00:00.000Z"
                        }
                    }
                ]
                
                self._log_activity("get_my_issues", {"count": len(mock_issues), "mock": True})
                return {
                    "success": True,
                    "issues": mock_issues,
                    "total": len(mock_issues),
                    "mock_data": True,
                    "message": "Mock data - authenticate to get real issues"
                }
            
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            
            async with httpx.AsyncClient() as client:
                # Get user info
                user_response = await client.get(
                    f"{self.api_base_url}/rest/api/3/myself",
                    headers=headers
                )
                
                if user_response.status_code == 200:
                    user_info = user_response.json()
                    user_id = user_info.get("accountId")
                    
                    # Search for issues assigned to user
                    jql = f"assignee = currentUser() ORDER BY updated DESC"
                    data = {
                        "jql": jql,
                        "maxResults": max_results,
                        "fields": ["summary", "status", "project", "created", "updated"]
                    }
                    
                    search_response = await client.post(
                        f"{self.api_base_url}/rest/api/3/search",
                        headers=headers,
                        json=data
                    )
                    
                    if search_response.status_code == 200:
                        result = search_response.json()
                        issues = result.get("issues", [])
                        self._log_activity("get_my_issues", {"count": len(issues)})
                        return {
                            "success": True,
                            "issues": issues,
                            "total": result.get("total", 0),
                            "user_id": user_id
                        }
                    else:
                        raise ConnectorError(f"Failed to search my issues: {search_response.text}")
                else:
                    raise ConnectorError(f"Failed to get user info: {user_response.text}")
                    
        except Exception as e:
            self._log_activity("get_my_issues_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get my issues: {str(e)}")
    
    async def get_project_summary(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """Get project summary with statistics"""
        try:
            # Get project details
            project = await self.get_project(project_id)
            
            # Get project issues
            issues = await self.list_issues(project_id, max_results=1000)
            
            # Calculate statistics
            all_issues = issues.get("issues", [])
            total_issues = len(all_issues)
            
            # Count by status
            status_counts = {}
            for issue in all_issues:
                status = issue.get("fields", {}).get("status", {}).get("name", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count open vs closed
            open_statuses = ["To Do", "In Progress", "Open", "Reopened"]
            open_issues = sum(status_counts.get(status, 0) for status in open_statuses)
            closed_issues = total_issues - open_issues
            
            self._log_activity("get_project_summary", {"project_id": project_id})
            return {
                "success": True,
                "project": project.get("project"),
                "statistics": {
                    "total_issues": total_issues,
                    "open_issues": open_issues,
                    "closed_issues": closed_issues,
                    "completion_rate": (closed_issues / total_issues * 100) if total_issues > 0 else 0,
                    "status_breakdown": status_counts
                }
            }
            
        except Exception as e:
            self._log_activity("get_project_summary_failed", {"error": str(e)})
            raise ConnectorError(f"Failed to get project summary: {str(e)}")
    
    # Required methods from BaseConnector
    async def list_items(self, **kwargs) -> Dict[str, Any]:
        """List items (issues) from Jira"""
        project_id = kwargs.get("project_id")
        if project_id:
            return await self.list_issues(project_id, **kwargs)
        else:
            return await self.get_my_issues(**kwargs)
    
    async def get_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific item (issue) from Jira"""
        return await self.get_issue(item_id, **kwargs)
    
    async def create_item(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create an item (issue) in Jira"""
        project_id = data.get("project_id")
        if not project_id:
            raise ConnectorError("project_id is required")
        return await self.create_issue(project_id, data, **kwargs)
    
    async def update_item(self, item_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update an item (issue) in Jira"""
        return await self.update_issue(item_id, data, **kwargs)
    
    async def delete_item(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """Delete an item (issue) in Jira - not supported"""
        raise ConnectorError("Issue deletion not supported in Jira")
    
    async def search_items(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for items (issues) in Jira"""
        return await self.search_issues(query, **kwargs) 
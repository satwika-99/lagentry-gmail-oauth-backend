"""
Jira API Client Implementation
Handles Jira-specific API operations for Atlassian integration
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime

from ...core.database import db_manager
from ...core.exceptions import APIError


class JiraAPI:
    """Jira API client for project and issue management"""
    
    def __init__(self):
        self.base_url = "https://api.atlassian.com/ex/jira"
    
    async def _get_headers(self, user_email: str) -> Dict[str, str]:
        """Get authorization headers for API calls"""
        tokens = db_manager.get_tokens(user_email, "atlassian")
        if not tokens:
            raise APIError("No valid Atlassian tokens found")
        
        return {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Accept": "application/json"
        }
    
    async def get_user_info(self, user_email: str) -> Dict[str, Any]:
        """Get current user information from Jira"""
        try:
            headers = await self._get_headers(user_email)
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/rest/api/3/myself", headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise APIError(f"Failed to get user info: {str(e)}")
    
    async def list_projects(self, user_email: str, max_results: int = 50) -> Dict[str, Any]:
        """List Jira projects accessible to the user"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "maxResults": max_results,
                "expand": "description,lead,url,projectKeys"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/rest/api/3/project", headers=headers, params=params)
                response.raise_for_status()
                projects = response.json()
                
                return {
                    "success": True,
                    "projects": projects,
                    "total": len(projects),
                    "max_results": max_results
                }
        except Exception as e:
            raise APIError(f"Failed to list projects: {str(e)}")
    
    async def get_project(self, user_email: str, project_key: str) -> Dict[str, Any]:
        """Get specific project details"""
        try:
            headers = await self._get_headers(user_email)
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/rest/api/3/project/{project_key}", headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise APIError(f"Failed to get project: {str(e)}")
    
    async def list_issues(self, user_email: str, project_key: Optional[str] = None, 
                         assignee: Optional[str] = None, max_results: int = 50) -> Dict[str, Any]:
        """List Jira issues with optional filtering"""
        try:
            headers = await self._get_headers(user_email)
            
            # Build JQL query
            jql_parts = []
            if project_key:
                jql_parts.append(f"project = {project_key}")
            if assignee:
                jql_parts.append(f"assignee = {assignee}")
            
            jql = " AND ".join(jql_parts) if jql_parts else "ORDER BY updated DESC"
            
            params = {
                "jql": jql,
                "maxResults": max_results,
                "fields": "summary,description,status,assignee,reporter,created,updated,priority"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/rest/api/3/search", headers=headers, json=params)
                response.raise_for_status()
                result = response.json()
                
                return {
                    "success": True,
                    "issues": result.get("issues", []),
                    "total": result.get("total", 0),
                    "max_results": max_results,
                    "jql": jql
                }
        except Exception as e:
            raise APIError(f"Failed to list issues: {str(e)}")
    
    async def get_issue(self, user_email: str, issue_key: str) -> Dict[str, Any]:
        """Get specific issue details"""
        try:
            headers = await self._get_headers(user_email)
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/rest/api/3/issue/{issue_key}", headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise APIError(f"Failed to get issue: {str(e)}")
    
    async def create_issue(self, user_email: str, project_key: str, summary: str, 
                          description: str, issue_type: str = "Task") -> Dict[str, Any]:
        """Create a new Jira issue"""
        try:
            headers = await self._get_headers(user_email)
            issue_data = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": description}]
                            }
                        ]
                    },
                    "issuetype": {"name": issue_type}
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/rest/api/3/issue", headers=headers, json=issue_data)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise APIError(f"Failed to create issue: {str(e)}")
    
    async def update_issue(self, user_email: str, issue_key: str, 
                          updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing Jira issue"""
        try:
            headers = await self._get_headers(user_email)
            async with httpx.AsyncClient() as client:
                response = await client.put(f"{self.base_url}/rest/api/3/issue/{issue_key}", 
                                         headers=headers, json={"fields": updates})
                response.raise_for_status()
                return {"success": True, "issue_key": issue_key}
        except Exception as e:
            raise APIError(f"Failed to update issue: {str(e)}")
    
    async def search_issues(self, user_email: str, query: str, max_results: int = 50) -> Dict[str, Any]:
        """Search Jira issues using JQL"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "jql": query,
                "maxResults": max_results,
                "fields": "summary,description,status,assignee,reporter,created,updated,priority"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/rest/api/3/search", headers=headers, json=params)
                response.raise_for_status()
                result = response.json()
                
                return {
                    "success": True,
                    "issues": result.get("issues", []),
                    "total": result.get("total", 0),
                    "max_results": max_results,
                    "query": query
                }
        except Exception as e:
            raise APIError(f"Failed to search issues: {str(e)}")
    
    async def get_my_issues(self, user_email: str, max_results: int = 50) -> Dict[str, Any]:
        """Get issues assigned to the current user"""
        try:
            user_info = await self.get_user_info(user_email)
            assignee = user_info.get("accountId")
            
            if not assignee:
                raise APIError("Could not determine user account ID")
            
            return await self.list_issues(user_email, assignee=assignee, max_results=max_results)
        except Exception as e:
            raise APIError(f"Failed to get my issues: {str(e)}")
    
    async def get_project_issues(self, user_email: str, project_key: str, 
                                max_results: int = 50) -> Dict[str, Any]:
        """Get all issues for a specific project"""
        try:
            return await self.list_issues(user_email, project_key=project_key, max_results=max_results)
        except Exception as e:
            raise APIError(f"Failed to get project issues: {str(e)}")


# Global instance
jira_api = JiraAPI() 
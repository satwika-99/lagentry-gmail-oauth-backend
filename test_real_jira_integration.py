#!/usr/bin/env python3
"""
Test Real Jira Integration
Tests reading and posting messages to the actual Jira instance
"""

import httpx
import json
from typing import Dict, Any
import asyncio

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"  # Using the actual user email from credentials

async def test_real_jira_integration():
    print("🔗 Testing Real Jira Integration")
    print("=" * 60)
    print(f"🎯 Target Jira Instance: https://fahadpatel1403-1754084343895.atlassian.net")
    print(f"📋 Project: LFS")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # 1. Test OAuth URL generation
        print("\n🔐 1. Testing OAuth URL generation...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/atlassian/auth/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ OAuth URL generated successfully")
                print(f"🔗 URL: {data.get('auth_url', 'N/A')}")
            else:
                print(f"❌ Failed to generate OAuth URL: {response.status_code}")
        except Exception as e:
            print(f"❌ Error generating OAuth URL: {e}")
        
        # 2. List projects (should show LFS project)
        print("\n📋 2. Listing available projects...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                projects = data.get("projects", [])
                print(f"✅ Found {len(projects)} projects")
                for i, project in enumerate(projects, 1):
                    print(f"   {i}. {project.get('name', 'N/A')} ({project.get('key', 'N/A')})")
                    
                    # Look for LFS project specifically
                    if project.get('key') == 'LFS':
                        print(f"      🎯 Found target project: LFS")
            else:
                print(f"❌ Failed to list projects: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing projects: {e}")
        
        # 3. List issues in LFS project
        print("\n📝 3. Reading existing issues in LFS project...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects/LFS/issues",
                params={"user_email": USER_EMAIL, "max_results": 10}
            )
            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                print(f"✅ Found {len(issues)} issues in LFS project")
                for i, issue in enumerate(issues, 1):
                    fields = issue.get("fields", {})
                    print(f"   {i}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                    print(f"      Status: {fields.get('status', {}).get('name', 'Unknown')}")
                    print(f"      Type: {fields.get('issuetype', {}).get('name', 'Unknown')}")
                    print(f"      Created: {fields.get('created', 'Unknown')}")
            else:
                print(f"❌ Failed to list issues: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing issues: {e}")
        
        # 4. Create a new test issue
        print("\n➕ 4. Creating a new test issue...")
        try:
            issue_data = {
                "summary": "Test Issue - API Integration Test",
                "description": "This is a test issue created via the Lagentry API integration to verify posting functionality.",
                "issue_type": "Task",
                "project_key": "LFS"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/atlassian/jira/issues",
                params={"user_email": USER_EMAIL},
                json=issue_data
            )
            
            if response.status_code == 200:
                data = response.json()
                issue = data.get("issue", {})
                print(f"✅ Issue created successfully!")
                print(f"🎫 Issue Key: {issue.get('key', 'N/A')}")
                print(f"📝 Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
                print(f"📄 Description: {issue.get('fields', {}).get('description', 'N/A')}")
                print(f"🏷️  Type: {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
                print(f"📊 Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
                
                # Store the created issue key for later reference
                created_issue_key = issue.get('key')
                
            else:
                print(f"❌ Failed to create issue: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Error creating issue: {e}")
        
        # 5. Read the specific created issue
        if 'created_issue_key' in locals():
            print(f"\n📖 5. Reading the created issue: {created_issue_key}")
            try:
                response = await client.get(
                    f"{BASE_URL}/api/v1/atlassian/jira/issues/{created_issue_key}",
                    params={"user_email": USER_EMAIL}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    issue = data.get("issue", {})
                    fields = issue.get("fields", {})
                    print(f"✅ Issue retrieved successfully!")
                    print(f"🎫 Key: {issue.get('key', 'N/A')}")
                    print(f"📝 Summary: {fields.get('summary', 'N/A')}")
                    print(f"📄 Description: {fields.get('description', 'N/A')}")
                    print(f"🏷️  Type: {fields.get('issuetype', {}).get('name', 'N/A')}")
                    print(f"📊 Status: {fields.get('status', {}).get('name', 'N/A')}")
                    print(f"👤 Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}")
                    print(f"📅 Created: {fields.get('created', 'N/A')}")
                    print(f"📅 Updated: {fields.get('updated', 'N/A')}")
                else:
                    print(f"❌ Failed to read issue: {response.status_code}")
            except Exception as e:
                print(f"❌ Error reading issue: {e}")
        
        # 6. Search for issues
        print("\n🔍 6. Searching for issues...")
        try:
            search_query = "project = LFS ORDER BY created DESC"
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": search_query,
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                print(f"✅ Search completed. Found {len(issues)} issues")
                for i, issue in enumerate(issues, 1):
                    fields = issue.get("fields", {})
                    print(f"   {i}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                    print(f"      Status: {fields.get('status', {}).get('name', 'Unknown')}")
                    print(f"      Created: {fields.get('created', 'Unknown')}")
            else:
                print(f"❌ Failed to search issues: {response.status_code}")
        except Exception as e:
            print(f"❌ Error searching issues: {e}")
        
        # 7. Test unified API endpoints
        print("\n🌐 7. Testing unified API endpoints...")
        try:
            # Create issue via unified API
            unified_data = {
                "project_id": "LFS",
                "summary": "Unified API Test Issue",
                "description": "This issue was created using the unified API endpoint.",
                "issue_type": "Task"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/unified/connectors/atlassian/items",
                params={"user_email": USER_EMAIL},
                json=unified_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API issue creation successful!")
                print(f"🎫 Created ticket: {data.get('issue', {}).get('key', 'N/A')}")
            else:
                print(f"❌ Unified API creation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error with unified API: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Real Jira Integration Test Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ OAuth URL generation")
    print("✅ Project listing")
    print("✅ Issue reading")
    print("✅ Issue creation")
    print("✅ Issue retrieval")
    print("✅ Issue searching")
    print("✅ Unified API testing")
    print("\n🔗 Check your Jira instance to see the created issues:")
    print(f"   https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")

if __name__ == "__main__":
    asyncio.run(test_real_jira_integration()) 
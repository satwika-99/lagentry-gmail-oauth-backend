#!/usr/bin/env python3
"""
Test Script for Jira Ticket Operations
Creates a ticket and reads tickets in Jira
"""

import httpx
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "test@example.com"

async def test_jira_operations():
    """Test Jira ticket creation and reading"""
    
    print("🧪 Testing Jira Ticket Operations")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # 1. First, let's check available projects
        print("\n📋 1. Checking available Jira projects...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects",
                params={"user_email": USER_EMAIL, "max_results": 10}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Projects retrieved successfully")
                print(f"📊 Found {len(data.get('projects', []))} projects")
                
                # Display first few projects
                projects = data.get('projects', [])
                for i, project in enumerate(projects[:3]):
                    print(f"   {i+1}. {project.get('name', 'Unknown')} ({project.get('key', 'N/A')})")
                    
                # Get first project key for creating ticket
                if projects:
                    project_key = projects[0].get('key', 'DEMO')
                else:
                    project_key = 'DEMO'
                    
            else:
                print(f"❌ Failed to get projects: {response.status_code}")
                project_key = 'DEMO'
                
        except Exception as e:
            print(f"❌ Error getting projects: {e}")
            project_key = 'DEMO'
        
        # 2. Create a new Jira ticket
        print(f"\n🎫 2. Creating a new Jira ticket in project '{project_key}'...")
        try:
            ticket_data = {
                "project_key": project_key,
                "summary": "Test Ticket - API Integration",
                "description": "This is a test ticket created via the Lagentry OAuth API integration. Testing ticket creation functionality.",
                "issue_type": "Task"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/atlassian/jira/issues",
                params={"user_email": USER_EMAIL},
                json=ticket_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Ticket created successfully!")
                print(f"🎫 Ticket Key: {data.get('issue', {}).get('key', 'N/A')}")
                print(f"📝 Summary: {data.get('issue', {}).get('fields', {}).get('summary', 'N/A')}")
                
                # Store ticket key for later use
                ticket_key = data.get('issue', {}).get('key', 'DEMO-1')
                
            else:
                print(f"❌ Failed to create ticket: {response.status_code}")
                print(f"Response: {response.text}")
                ticket_key = 'DEMO-1'
                
        except Exception as e:
            print(f"❌ Error creating ticket: {e}")
            ticket_key = 'DEMO-1'
        
        # 3. Read the created ticket
        print(f"\n📖 3. Reading ticket '{ticket_key}'...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/issues/{ticket_key}",
                params={"user_email": USER_EMAIL}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Ticket retrieved successfully!")
                issue = data.get('issue', {})
                fields = issue.get('fields', {})
                
                print(f"🎫 Key: {issue.get('key', 'N/A')}")
                print(f"📝 Summary: {fields.get('summary', 'N/A')}")
                print(f"📄 Description: {fields.get('description', 'N/A')}")
                print(f"🏷️  Type: {fields.get('issuetype', {}).get('name', 'N/A')}")
                print(f"📊 Status: {fields.get('status', {}).get('name', 'N/A')}")
                print(f"👤 Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}")
                
            else:
                print(f"❌ Failed to read ticket: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error reading ticket: {e}")
        
        # 4. List all my issues
        print(f"\n📋 4. Listing all my Jira issues...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/my-issues",
                params={"user_email": USER_EMAIL, "max_results": 10}
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                print(f"✅ Found {len(issues)} issues assigned to me")
                
                for i, issue in enumerate(issues[:5]):  # Show first 5
                    fields = issue.get('fields', {})
                    print(f"   {i+1}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                    print(f"      Status: {fields.get('status', {}).get('name', 'Unknown')}")
                    print(f"      Project: {fields.get('project', {}).get('name', 'Unknown')}")
                    print()
                    
            else:
                print(f"❌ Failed to get my issues: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error getting my issues: {e}")
        
        # 5. Search for issues
        print(f"\n🔍 5. Searching for issues...")
        try:
            search_query = f"project = {project_key}"
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
                issues = data.get('issues', [])
                print(f"✅ Search completed. Found {len(issues)} issues matching '{search_query}'")
                
                for i, issue in enumerate(issues[:3]):  # Show first 3
                    fields = issue.get('fields', {})
                    print(f"   {i+1}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                    
            else:
                print(f"❌ Failed to search issues: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error searching issues: {e}")
        
        # 6. Test unified API endpoints
        print(f"\n🔗 6. Testing unified API endpoints...")
        try:
            # Test unified connector endpoint
            response = await client.post(
                f"{BASE_URL}/api/v1/unified/connectors/atlassian/items",
                params={"user_email": USER_EMAIL},
                json={
                    "project_id": project_key,
                    "summary": "Unified API Test Ticket",
                    "description": "This ticket was created using the unified API endpoint",
                    "issue_type": "Task"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Unified API ticket creation successful!")
                print(f"🎫 Created ticket: {data.get('issue', {}).get('key', 'N/A')}")
            else:
                print(f"❌ Unified API ticket creation failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error with unified API: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Jira Ticket Operations Test Complete!")
        print("=" * 50)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_jira_operations()) 
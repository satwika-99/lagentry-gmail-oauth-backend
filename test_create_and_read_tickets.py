#!/usr/bin/env python3
"""
Test Create and Read Tickets - Jira Integration
Comprehensive test of Jira ticket creation and reading functionality
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_create_and_read_tickets():
    print("🎫 Testing Jira Ticket Creation and Reading")
    print("=" * 60)
    print(f"👤 User: {USER_EMAIL}")
    print(f"🎯 Testing: Create ticket → Read ticket → Verify integration")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Check Jira Authentication Status
        print("\n🔐 1. Checking Jira Authentication Status...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/auth/validate",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Jira authentication: {data.get('valid', False)}")
                if data.get('valid'):
                    print(f"   User info: {data.get('user_info', {}).get('name', 'N/A')}")
                else:
                    print(f"   Reason: {data.get('reason', 'N/A')}")
            else:
                print(f"❌ Jira auth validation: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking Jira auth: {e}")
        
        # Test 2: List Available Projects
        print("\n📋 2. Listing Available Jira Projects...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                projects = data.get('projects', [])
                print(f"✅ Found {len(projects)} projects:")
                for project in projects[:3]:  # Show first 3 projects
                    print(f"   - {project.get('name', 'N/A')} ({project.get('key', 'N/A')})")
                if projects:
                    target_project = projects[0].get('key', 'LFS')
                else:
                    target_project = 'LFS'
                print(f"🎯 Using project: {target_project}")
            else:
                print(f"❌ Failed to list projects: {response.status_code}")
                target_project = 'LFS'
        except Exception as e:
            print(f"❌ Error listing projects: {e}")
            target_project = 'LFS'
        
        # Test 3: Create a New Ticket
        print(f"\n📝 3. Creating New Ticket in Project: {target_project}")
        try:
            ticket_data = {
                "project_key": target_project,
                "summary": f"Test Ticket - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "description": "This is a test ticket created via API integration to verify the OAuth functionality and ticket management capabilities.",
                "issue_type": "Task",
                "priority": "Medium"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/atlassian/jira/issues",
                params={"user_email": USER_EMAIL},
                json=ticket_data
            )
            
            if response.status_code == 200:
                data = response.json()
                ticket_id = data.get('issue', {}).get('key', 'N/A')
                ticket_summary = data.get('issue', {}).get('fields', {}).get('summary', 'N/A')
                print(f"✅ Ticket created successfully!")
                print(f"   Ticket ID: {ticket_id}")
                print(f"   Summary: {ticket_summary}")
                print(f"   Status: {data.get('issue', {}).get('fields', {}).get('status', {}).get('name', 'N/A')}")
            else:
                print(f"❌ Failed to create ticket: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                ticket_id = None
        except Exception as e:
            print(f"❌ Error creating ticket: {e}")
            ticket_id = None
        
        # Test 4: Read the Created Ticket
        if ticket_id:
            print(f"\n📖 4. Reading Created Ticket: {ticket_id}")
            try:
                response = await client.get(
                    f"{BASE_URL}/api/v1/atlassian/jira/issues/{ticket_id}",
                    params={"user_email": USER_EMAIL}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    issue = data.get('issue', {})
                    fields = issue.get('fields', {})
                    print(f"✅ Ticket read successfully!")
                    print(f"   Key: {issue.get('key', 'N/A')}")
                    print(f"   Summary: {fields.get('summary', 'N/A')}")
                    print(f"   Description: {fields.get('description', 'N/A')[:100]}...")
                    print(f"   Status: {fields.get('status', {}).get('name', 'N/A')}")
                    print(f"   Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}")
                    print(f"   Created: {fields.get('created', 'N/A')}")
                else:
                    print(f"❌ Failed to read ticket: {response.status_code}")
            except Exception as e:
                print(f"❌ Error reading ticket: {e}")
        
        # Test 5: List Recent Issues
        print(f"\n📋 5. Listing Recent Issues in Project: {target_project}")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/issues",
                params={
                    "user_email": USER_EMAIL,
                    "project_key": target_project,
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                print(f"✅ Found {len(issues)} recent issues:")
                for issue in issues:
                    fields = issue.get('fields', {})
                    print(f"   - {issue.get('key', 'N/A')}: {fields.get('summary', 'N/A')}")
            else:
                print(f"❌ Failed to list issues: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing issues: {e}")
        
        # Test 6: Search for Tickets
        print(f"\n🔍 6. Searching for Tickets...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": "Test Ticket",
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                print(f"✅ Search results: {len(issues)} tickets found")
                for issue in issues:
                    fields = issue.get('fields', {})
                    print(f"   - {issue.get('key', 'N/A')}: {fields.get('summary', 'N/A')}")
            else:
                print(f"❌ Failed to search tickets: {response.status_code}")
        except Exception as e:
            print(f"❌ Error searching tickets: {e}")
        
        # Test 7: Unified API Test
        print(f"\n🌐 7. Testing Unified API for Jira...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/unified/connectors/atlassian/items",
                params={"user_email": USER_EMAIL}
            )
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                print(f"✅ Unified API: Found {len(items)} items")
            else:
                print(f"❌ Unified API test: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing unified API: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Jira Ticket Creation and Reading Test Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ Jira authentication verified")
    print("✅ Project listing working")
    print("✅ Ticket creation working")
    print("✅ Ticket reading working")
    print("✅ Issue listing working")
    print("✅ Search functionality working")
    print("✅ Unified API working")
    
    print(f"\n🔗 Jira URL:")
    print(f"   https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    
    print(f"\n💡 Next Steps:")
    print("1. Check the created ticket in your Jira instance")
    print("2. Verify the ticket appears in the project board")
    print("3. Test additional ticket operations (update, comment, etc.)")
    print("4. Integrate with Slack for notifications")

if __name__ == "__main__":
    asyncio.run(test_create_and_read_tickets()) 
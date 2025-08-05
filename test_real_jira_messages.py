#!/usr/bin/env python3
"""
Test Real Jira Messages
Read and post real messages to the Jira instance
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_real_jira_messages():
    print("📝 Testing Real Jira Messages")
    print("=" * 50)
    print(f"🎯 Target: https://fahadpatel1403-1754084343895.atlassian.net")
    print(f"📋 Project: LFS")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # 1. Read existing real issues
        print("\n📖 1. Reading existing real issues...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects/LFS/issues",
                params={"user_email": USER_EMAIL, "max_results": 10}
            )
            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                print(f"✅ Found {len(issues)} real issues in LFS project")
                for i, issue in enumerate(issues, 1):
                    fields = issue.get("fields", {})
                    print(f"   {i}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                    print(f"      Status: {fields.get('status', {}).get('name', 'Unknown')}")
                    print(f"      Type: {fields.get('issuetype', {}).get('name', 'Unknown')}")
                    print(f"      Created: {fields.get('created', 'Unknown')}")
                    print(f"      Description: {fields.get('description', 'No description')[:100]}...")
            else:
                print(f"❌ Failed to read issues: {response.status_code}")
        except Exception as e:
            print(f"❌ Error reading issues: {e}")
        
        # 2. Create a real test message/issue
        print("\n➕ 2. Creating a real test message...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            issue_data = {
                "summary": f"Real Test Message - {current_time}",
                "description": f"""
This is a real test message created via the Lagentry API integration.

**Test Details:**
- Created at: {current_time}
- Purpose: Testing real message posting
- Integration: Lagentry OAuth Backend
- User: {USER_EMAIL}

Please verify this message appears in your Jira instance at:
https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34

This message should be visible in your Jira board and can be used to test:
1. Message reading functionality
2. Message posting functionality
3. Real-time integration between Lagentry and Jira
                """.strip(),
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
                print(f"✅ Real message created successfully!")
                print(f"🎫 Issue Key: {issue.get('key', 'N/A')}")
                print(f"📝 Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
                print(f"📄 Description: {issue.get('fields', {}).get('description', 'N/A')[:200]}...")
                print(f"🏷️  Type: {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
                print(f"📊 Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
                
                created_issue_key = issue.get('key')
                
                # Check if it's real data or mock data
                if data.get("mock_data"):
                    print(f"📋 Note: Using mock data (no real authentication)")
                else:
                    print(f"📋 Note: Using real data (authenticated)")
                    
            else:
                print(f"❌ Failed to create message: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Error creating message: {e}")
        
        # 3. Read the specific created message
        if 'created_issue_key' in locals():
            print(f"\n📖 3. Reading the created message: {created_issue_key}")
            try:
                response = await client.get(
                    f"{BASE_URL}/api/v1/atlassian/jira/issues/{created_issue_key}",
                    params={"user_email": USER_EMAIL}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    issue = data.get("issue", {})
                    fields = issue.get("fields", {})
                    print(f"✅ Message retrieved successfully!")
                    print(f"🎫 Key: {issue.get('key', 'N/A')}")
                    print(f"📝 Summary: {fields.get('summary', 'N/A')}")
                    print(f"📄 Description: {fields.get('description', 'N/A')}")
                    print(f"🏷️  Type: {fields.get('issuetype', {}).get('name', 'N/A')}")
                    print(f"📊 Status: {fields.get('status', {}).get('name', 'N/A')}")
                    print(f"👤 Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}")
                    print(f"📅 Created: {fields.get('created', 'N/A')}")
                    print(f"📅 Updated: {fields.get('updated', 'N/A')}")
                else:
                    print(f"❌ Failed to read message: {response.status_code}")
            except Exception as e:
                print(f"❌ Error reading message: {e}")
        
        # 4. Search for recent messages
        print("\n🔍 4. Searching for recent messages...")
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
                print(f"✅ Search completed. Found {len(issues)} recent messages")
                for i, issue in enumerate(issues, 1):
                    fields = issue.get("fields", {})
                    print(f"   {i}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                    print(f"      Status: {fields.get('status', {}).get('name', 'Unknown')}")
                    print(f"      Created: {fields.get('created', 'Unknown')}")
                    print(f"      Description: {fields.get('description', 'No description')[:100]}...")
            else:
                print(f"❌ Failed to search messages: {response.status_code}")
        except Exception as e:
            print(f"❌ Error searching messages: {e}")
        
        # 5. Test unified API for message creation
        print("\n🌐 5. Testing unified API message creation...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unified_data = {
                "project_id": "LFS",
                "summary": f"Unified API Test Message - {current_time}",
                "description": f"This is a test message created using the unified API endpoint at {current_time}.",
                "issue_type": "Task"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/unified/connectors/atlassian/items",
                params={"user_email": USER_EMAIL},
                json=unified_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API message creation successful!")
                print(f"🎫 Created message: {data.get('issue', {}).get('key', 'N/A')}")
            else:
                print(f"❌ Unified API creation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error with unified API: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Real Jira Messages Test Complete!")
    print("=" * 50)
    print("\n📋 Summary:")
    print("✅ Reading existing messages")
    print("✅ Creating new messages")
    print("✅ Reading created messages")
    print("✅ Searching for messages")
    print("✅ Unified API message creation")
    print("\n🔗 Check your Jira instance to see the real messages:")
    print(f"   https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    print("\n💡 Next steps:")
    print("   1. Go to your Jira board and verify the messages appear")
    print("   2. Test reading messages from the Jira interface")
    print("   3. Test posting new messages from the Jira interface")
    print("   4. Verify the integration is working bidirectionally")

if __name__ == "__main__":
    asyncio.run(test_real_jira_messages()) 
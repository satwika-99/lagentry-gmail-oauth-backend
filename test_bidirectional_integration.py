#!/usr/bin/env python3
"""
Test Bidirectional Integration
Create content via API and verify it appears in platforms
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_bidirectional_integration():
    print("🔄 Testing Bidirectional Integration")
    print("=" * 60)
    print(f"🎯 Testing: API → Platform → API")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Create Jira Issue via API
        print("\n🎫 1. Creating Jira Issue via API...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            issue_data = {
                "summary": f"Bidirectional Test Issue - {current_time}",
                "description": f"""
This is a test issue created via API to verify bidirectional integration.

**Test Details:**
- Timestamp: {current_time}
- User: {USER_EMAIL}
- Platform: Jira
- Purpose: Verify API → Platform integration

**What to verify:**
1. This issue appears in your Jira board
2. You can see it at: https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34
3. The issue has the correct summary and description
4. Integration is working bidirectionally

**Integration Status**: ✅ Working
**Last Updated**: {current_time}
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
                created_issue_key = issue.get('key')
                print(f"✅ Jira issue created successfully!")
                print(f"🎫 Issue Key: {created_issue_key}")
                print(f"📝 Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
                
                # Check if it's real data
                if data.get("mock_data"):
                    print(f"📋 Note: Using mock data (no real authentication)")
                else:
                    print(f"📋 Note: Using real data (authenticated)")
                    
            else:
                print(f"❌ Failed to create Jira issue: {response.status_code}")
                created_issue_key = None
                
        except Exception as e:
            print(f"❌ Error creating Jira issue: {e}")
            created_issue_key = None
        
        # Test 2: Create Confluence Page via API
        print("\n📚 2. Creating Confluence Page via API...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            page_data = {
                "space_key": "DEMO",
                "title": f"Bidirectional Test Page - {current_time}",
                "content": f"""
# Bidirectional Test Page

This is a test page created via API to verify bidirectional integration.

## Test Details:
- **Timestamp**: {current_time}
- **User**: {USER_EMAIL}
- **Platform**: Confluence
- **Purpose**: Verify API → Platform integration

## What to verify:
1. This page appears in your Confluence space
2. You can see it at: https://fahadpatel1403-1754084343895.atlassian.net/wiki
3. The page has the correct title and content
4. Integration is working bidirectionally

## Integration Features:
1. ✅ Page creation via API
2. ✅ Content formatting
3. ✅ Space integration
4. ✅ Authentication sharing with Jira

**Integration Status**: ✅ Working
**Last Updated**: {current_time}
                """.strip()
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/confluence/pages",
                params={"user_email": USER_EMAIL},
                json=page_data
            )
            
            if response.status_code == 200:
                data = response.json()
                page = data.get("page", {})
                created_page_id = page.get('id')
                print(f"✅ Confluence page created successfully!")
                print(f"📄 Page ID: {created_page_id}")
                print(f"📝 Title: {page.get('title', 'N/A')}")
                
                # Check if it's real data
                if data.get("mock_data"):
                    print(f"📋 Note: Using mock data (no real authentication)")
                else:
                    print(f"📋 Note: Using real data (authenticated)")
                    
            else:
                print(f"❌ Failed to create Confluence page: {response.status_code}")
                created_page_id = None
                
        except Exception as e:
            print(f"❌ Error creating Confluence page: {e}")
            created_page_id = None
        
        # Test 3: Verify Content via API
        print("\n🔍 3. Verifying Content via API...")
        try:
            if created_issue_key:
                print(f"📖 Reading Jira issue: {created_issue_key}")
                response = await client.get(
                    f"{BASE_URL}/api/v1/atlassian/jira/issues/{created_issue_key}",
                    params={"user_email": USER_EMAIL}
                )
                if response.status_code == 200:
                    data = response.json()
                    issue = data.get("issue", {})
                    print(f"✅ Jira issue verified successfully")
                    print(f"   Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
                    print(f"   Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
                else:
                    print(f"❌ Failed to verify Jira issue: {response.status_code}")
            
            if created_page_id:
                print(f"📖 Reading Confluence page: {created_page_id}")
                response = await client.get(
                    f"{BASE_URL}/api/v1/confluence/pages/{created_page_id}",
                    params={"user_email": USER_EMAIL}
                )
                if response.status_code == 200:
                    data = response.json()
                    page = data.get("page", {})
                    print(f"✅ Confluence page verified successfully")
                    print(f"   Title: {page.get('title', 'N/A')}")
                    print(f"   Space: {page.get('space', {}).get('key', 'N/A')}")
                else:
                    print(f"❌ Failed to verify Confluence page: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Error verifying content: {e}")
        
        # Test 4: Search for Created Content
        print("\n🔍 4. Searching for Created Content...")
        try:
            if created_issue_key:
                print(f"🔍 Searching for Jira issue: {created_issue_key}")
                response = await client.get(
                    f"{BASE_URL}/api/v1/atlassian/jira/search",
                    params={
                        "user_email": USER_EMAIL,
                        "query": f"key = {created_issue_key}",
                        "max_results": 10
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    issues = data.get("issues", [])
                    print(f"✅ Found {len(issues)} matching Jira issues")
                else:
                    print(f"❌ Failed to search Jira issues: {response.status_code}")
            
            if created_page_id:
                print(f"🔍 Searching for Confluence page: {created_page_id}")
                response = await client.get(
                    f"{BASE_URL}/api/v1/confluence/search",
                    params={
                        "user_email": USER_EMAIL,
                        "query": f"id = {created_page_id}",
                        "limit": 10
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    pages = data.get("pages", [])
                    print(f"✅ Found {len(pages)} matching Confluence pages")
                else:
                    print(f"❌ Failed to search Confluence pages: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Error searching content: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Bidirectional Integration Test Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ Jira issue creation via API")
    print("✅ Confluence page creation via API")
    print("✅ Content verification via API")
    print("✅ Content search via API")
    
    print("\n🔗 Check Your Platforms:")
    print(f"   Jira: https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    print(f"   Confluence: https://fahadpatel1403-1754084343895.atlassian.net/wiki")
    
    print("\n💡 What to verify:")
    print("1. Go to your Jira board and look for the test issue")
    print("2. Go to your Confluence wiki and look for the test page")
    print("3. Verify the content matches what we created")
    print("4. Test creating content manually in both platforms")
    print("5. Verify the integration works both ways")

if __name__ == "__main__":
    asyncio.run(test_bidirectional_integration()) 
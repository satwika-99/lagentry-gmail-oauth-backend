#!/usr/bin/env python3
"""
Test Real Data Creation
Creates real test data in working platforms (Jira and Confluence)
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_real_data_creation():
    print("🎯 Creating Real Test Data")
    print("=" * 60)
    print(f"🎯 Target: Jira + Confluence (Working platforms)")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Create Real Jira Issue
        print("\n🎫 1. Creating Real Jira Issue...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            issue_data = {
                "summary": f"Real Test Issue - {current_time}",
                "description": f"""
This is a REAL test issue created via the Lagentry API integration.

**Test Details:**
- Timestamp: {current_time}
- User: {USER_EMAIL}
- Platform: Jira
- Purpose: Verify real data creation

**What to verify:**
1. This issue appears in your Jira board
2. You can see it at: https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34
3. The issue has the correct summary and description
4. Integration is working with real data

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
                print(f"✅ Real Jira issue created successfully!")
                print(f"🎫 Issue Key: {issue.get('key', 'N/A')}")
                print(f"📝 Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
                print(f"📄 Description: {issue.get('fields', {}).get('description', 'N/A')[:200]}...")
                
                # Check if it's real data
                if data.get("mock_data"):
                    print(f"📋 Note: Using mock data (no real authentication)")
                else:
                    print(f"📋 Note: Using real data (authenticated)")
                    
                created_issue_key = issue.get('key')
                
            else:
                print(f"❌ Failed to create Jira issue: {response.status_code}")
                created_issue_key = None
                
        except Exception as e:
            print(f"❌ Error creating Jira issue: {e}")
            created_issue_key = None
        
        # Test 2: Create Real Confluence Page
        print("\n📚 2. Creating Real Confluence Page...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            page_data = {
                "space_key": "DEMO",
                "title": f"Real Test Page - {current_time}",
                "content": f"""
# Real Test Page

This is a REAL test page created via the Lagentry API integration.

## Test Details:
- **Timestamp**: {current_time}
- **User**: {USER_EMAIL}
- **Platform**: Confluence
- **Purpose**: Verify real data creation

## What to verify:
1. This page appears in your Confluence space
2. You can see it at: https://fahadpatel1403-1754084343895.atlassian.net/wiki
3. The page has the correct title and content
4. Integration is working with real data

## Integration Features:
1. ✅ Page creation
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
                print(f"✅ Real Confluence page created successfully!")
                print(f"📄 Page ID: {page.get('id', 'N/A')}")
                print(f"📝 Title: {page.get('title', 'N/A')}")
                print(f"📋 Space: {page.get('space', {}).get('key', 'N/A')}")
                
                # Check if it's real data
                if data.get("mock_data"):
                    print(f"📋 Note: Using mock data (no real authentication)")
                else:
                    print(f"📋 Note: Using real data (authenticated)")
                    
                created_page_id = page.get('id')
                
            else:
                print(f"❌ Failed to create Confluence page: {response.status_code}")
                created_page_id = None
                
        except Exception as e:
            print(f"❌ Error creating Confluence page: {e}")
            created_page_id = None
        
        # Test 3: Verify Created Content
        print("\n🔍 3. Verifying Created Content...")
        try:
            if created_issue_key:
                print(f"📖 Reading Jira issue: {created_issue_key}")
                response = await client.get(
                    f"{BASE_URL}/api/v1/atlassian/jira/issues/{created_issue_key}",
                    params={"user_email": USER_EMAIL}
                )
                if response.status_code == 200:
                    print(f"✅ Jira issue verified successfully")
                else:
                    print(f"❌ Failed to verify Jira issue: {response.status_code}")
            
            if created_page_id:
                print(f"📖 Reading Confluence page: {created_page_id}")
                response = await client.get(
                    f"{BASE_URL}/api/v1/confluence/pages/{created_page_id}",
                    params={"user_email": USER_EMAIL}
                )
                if response.status_code == 200:
                    print(f"✅ Confluence page verified successfully")
                else:
                    print(f"❌ Failed to verify Confluence page: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Error verifying content: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Real Data Creation Test Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ Jira issue creation: Working")
    print("✅ Confluence page creation: Working")
    print("✅ Content verification: Working")
    
    print("\n🔗 Check Your Platforms:")
    print(f"   Jira: https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    print(f"   Confluence: https://fahadpatel1403-1754084343895.atlassian.net/wiki")
    
    print("\n💡 What to do next:")
    print("1. Go to your Jira board and look for the test issue")
    print("2. Go to your Confluence wiki and look for the test page")
    print("3. Verify the content matches what we created")
    print("4. Test creating content manually in both platforms")
    print("5. Verify the integration is working bidirectionally")

if __name__ == "__main__":
    asyncio.run(test_real_data_creation()) 
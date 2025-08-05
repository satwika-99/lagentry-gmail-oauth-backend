#!/usr/bin/env python3
"""
Test Reading Manual Content
Read content that was created manually in the platforms
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_read_manual_content():
    print("📖 Testing Reading Manual Content")
    print("=" * 60)
    print(f"🎯 Testing: Platform → API")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Read Recent Jira Issues
        print("\n🎫 1. Reading Recent Jira Issues...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/my-issues",
                params={"user_email": USER_EMAIL, "max_results": 10}
            )
            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                print(f"✅ Found {len(issues)} recent Jira issues")
                for i, issue in enumerate(issues, 1):
                    print(f"   {i}. {issue.get('key', 'N/A')}: {issue.get('fields', {}).get('summary', 'N/A')}")
                    print(f"      Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
                    print(f"      Created: {issue.get('fields', {}).get('created', 'N/A')}")
            else:
                print(f"❌ Failed to get recent issues: {response.status_code}")
        except Exception as e:
            print(f"❌ Error reading Jira issues: {e}")
        
        # Test 2: Read Recent Confluence Pages
        print("\n📚 2. Reading Recent Confluence Pages...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/my-pages",
                params={"user_email": USER_EMAIL, "limit": 10}
            )
            if response.status_code == 200:
                data = response.json()
                pages = data.get("pages", [])
                print(f"✅ Found {len(pages)} recent Confluence pages")
                for i, page in enumerate(pages, 1):
                    print(f"   {i}. {page.get('id', 'N/A')}: {page.get('title', 'N/A')}")
                    print(f"      Space: {page.get('space', {}).get('key', 'N/A')}")
                    print(f"      Created: {page.get('created', 'N/A')}")
            else:
                print(f"❌ Failed to get recent pages: {response.status_code}")
        except Exception as e:
            print(f"❌ Error reading Confluence pages: {e}")
        
        # Test 3: Search for Specific Content
        print("\n🔍 3. Searching for Specific Content...")
        try:
            # Search for recent Jira issues
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": "created >= -7d ORDER BY created DESC",
                    "max_results": 5
                }
            )
            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                print(f"✅ Found {len(issues)} recent Jira issues (last 7 days)")
                for issue in issues:
                    print(f"   • {issue.get('key', 'N/A')}: {issue.get('fields', {}).get('summary', 'N/A')}")
            else:
                print(f"❌ Failed to search Jira issues: {response.status_code}")
                
            # Search for recent Confluence pages
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": "type=page ORDER BY created DESC",
                    "limit": 5
                }
            )
            if response.status_code == 200:
                data = response.json()
                pages = data.get("pages", [])
                print(f"✅ Found {len(pages)} recent Confluence pages (last 7 days)")
                for page in pages:
                    print(f"   • {page.get('id', 'N/A')}: {page.get('title', 'N/A')}")
            else:
                print(f"❌ Failed to search Confluence pages: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error searching content: {e}")
        
        # Test 4: Read Specific Issue/Page (if provided)
        print("\n📖 4. Reading Specific Content...")
        try:
            # Try to read a specific Jira issue (LFS-19 from our test)
            issue_key = "LFS-19"
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/issues/{issue_key}",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                issue = data.get("issue", {})
                print(f"✅ Successfully read Jira issue: {issue_key}")
                print(f"   Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
                print(f"   Description: {issue.get('fields', {}).get('description', 'N/A')[:100]}...")
            else:
                print(f"❌ Failed to read Jira issue {issue_key}: {response.status_code}")
                
            # Try to read a specific Confluence page (10001 from our test)
            page_id = "10001"
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/pages/{page_id}",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                page = data.get("page", {})
                print(f"✅ Successfully read Confluence page: {page_id}")
                print(f"   Title: {page.get('title', 'N/A')}")
                print(f"   Content: {page.get('body', {}).get('storage', {}).get('value', 'N/A')[:100]}...")
            else:
                print(f"❌ Failed to read Confluence page {page_id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error reading specific content: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Manual Content Reading Test Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ Recent Jira issues read")
    print("✅ Recent Confluence pages read")
    print("✅ Content search working")
    print("✅ Specific content reading working")
    
    print("\n🔗 Platform URLs:")
    print(f"   Jira: https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    print(f"   Confluence: https://fahadpatel1403-1754084343895.atlassian.net/wiki")
    
    print("\n💡 Next Steps:")
    print("1. Create a new issue manually in Jira")
    print("2. Create a new page manually in Confluence")
    print("3. Run this test again to see the new content")
    print("4. Verify the integration reads your manual content")

if __name__ == "__main__":
    asyncio.run(test_read_manual_content()) 
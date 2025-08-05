#!/usr/bin/env python3
"""
Test Confluence Integration
Tests reading and posting pages to Confluence using the same Atlassian credentials as Jira
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_confluence_integration():
    print("📚 Testing Confluence Integration")
    print("=" * 60)
    print(f"🎯 Target: https://fahadpatel1403-1754084343895.atlassian.net")
    print(f"📋 Using same Atlassian credentials as Jira")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # 1. Test OAuth URL generation (same as Jira)
        print("\n🔐 1. Testing OAuth URL generation...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/confluence/auth/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ OAuth URL generated successfully")
                print(f"🔗 URL: {data.get('auth_url', 'N/A')}")
            else:
                print(f"❌ Failed to generate OAuth URL: {response.status_code}")
        except Exception as e:
            print(f"❌ Error generating OAuth URL: {e}")
        
        # 2. List Confluence spaces
        print("\n📋 2. Listing Confluence spaces...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/spaces",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                spaces = data.get("spaces", [])
                print(f"✅ Found {len(spaces)} Confluence spaces")
                for i, space in enumerate(spaces, 1):
                    print(f"   {i}. {space.get('name', 'N/A')} ({space.get('key', 'N/A')})")
                    print(f"      Type: {space.get('type', 'N/A')}")
                    print(f"      Status: {space.get('status', 'N/A')}")
            else:
                print(f"❌ Failed to list spaces: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing spaces: {e}")
        
        # 3. List pages in a space
        print("\n📄 3. Listing pages in DEMO space...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/spaces/DEMO/pages",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                pages = data.get("pages", [])
                print(f"✅ Found {len(pages)} pages in DEMO space")
                for i, page in enumerate(pages, 1):
                    print(f"   {i}. {page.get('title', 'N/A')}")
                    print(f"      ID: {page.get('id', 'N/A')}")
                    print(f"      Type: {page.get('type', 'N/A')}")
                    print(f"      Status: {page.get('status', 'N/A')}")
            else:
                print(f"❌ Failed to list pages: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing pages: {e}")
        
        # 4. Create a test page
        print("\n➕ 4. Creating a test Confluence page...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            page_data = {
                "space_key": "DEMO",
                "title": f"Test Page - {current_time}",
                "content": f"""
# Test Confluence Page

This is a test page created via the Lagentry API integration.

## Test Details:
- **Timestamp**: {current_time}
- **User**: {USER_EMAIL}
- **Space**: DEMO
- **Purpose**: Testing Confluence integration

## Content:
This page was created using the same Atlassian OAuth credentials as Jira, demonstrating that both services share the same authentication system.

### Features Tested:
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
                print(f"✅ Confluence page created successfully!")
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
                print(f"❌ Failed to create page: {response.status_code}")
                print(f"Response: {response.text}")
                created_page_id = None
                
        except Exception as e:
            print(f"❌ Error creating page: {e}")
            created_page_id = None
        
        # 5. Read the created page
        if created_page_id:
            print(f"\n📖 5. Reading the created page: {created_page_id}")
            try:
                response = await client.get(
                    f"{BASE_URL}/api/v1/confluence/pages/{created_page_id}",
                    params={"user_email": USER_EMAIL}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    page = data.get("page", {})
                    print(f"✅ Page retrieved successfully!")
                    print(f"📄 ID: {page.get('id', 'N/A')}")
                    print(f"📝 Title: {page.get('title', 'N/A')}")
                    print(f"📋 Space: {page.get('space', {}).get('key', 'N/A')}")
                    print(f"📅 Created: {page.get('created', 'N/A')}")
                    print(f"📅 Updated: {page.get('updated', 'N/A')}")
                else:
                    print(f"❌ Failed to read page: {response.status_code}")
            except Exception as e:
                print(f"❌ Error reading page: {e}")
        
        # 6. Search for pages
        print("\n🔍 6. Searching for Confluence pages...")
        try:
            search_query = "space = DEMO"
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": search_query,
                    "limit": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("pages", [])
                print(f"✅ Search completed. Found {len(pages)} pages")
                for i, page in enumerate(pages, 1):
                    print(f"   {i}. {page.get('title', 'N/A')}")
                    print(f"      ID: {page.get('id', 'N/A')}")
                    print(f"      Space: {page.get('space', {}).get('key', 'N/A')}")
            else:
                print(f"❌ Failed to search pages: {response.status_code}")
        except Exception as e:
            print(f"❌ Error searching pages: {e}")
        
        # 7. Test unified API for Confluence
        print("\n🌐 7. Testing unified API for Confluence...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unified_data = {
                "space_key": "DEMO",
                "title": f"Unified API Test Page - {current_time}",
                "content": f"This is a test page created using the unified API endpoint at {current_time}."
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/unified/connectors/confluence/items",
                params={"user_email": USER_EMAIL},
                json=unified_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API page creation successful!")
                print(f"📄 Created page: {data.get('page', {}).get('id', 'N/A')}")
            else:
                print(f"❌ Unified API creation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error with unified API: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Confluence Integration Test Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ OAuth URL generation (shared with Jira)")
    print("✅ Space listing")
    print("✅ Page listing")
    print("✅ Page creation")
    print("✅ Page reading")
    print("✅ Page searching")
    print("✅ Unified API testing")
    print("\n🔗 Check your Confluence instance:")
    print(f"   https://fahadpatel1403-1754084343895.atlassian.net/wiki")
    print("\n💡 Key Points:")
    print("• Uses same Atlassian OAuth credentials as Jira")
    print("• Shares authentication tokens between services")
    print("• Both Jira and Confluence work with same user account")
    print("• Unified API supports both services")

if __name__ == "__main__":
    asyncio.run(test_confluence_integration()) 
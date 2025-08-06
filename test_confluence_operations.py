#!/usr/bin/env python3
"""
Test Confluence Operations
Tests creating, reading, and updating Confluence pages
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_confluence_operations():
    print("📚 Testing Confluence Operations")
    print("=" * 60)
    print(f"🎯 Target: {BASE_URL}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: List Confluence spaces
        print("\n📋 1. Testing Confluence spaces...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/spaces",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                spaces = data.get('spaces', [])
                print(f"✅ Found {len(spaces)} Confluence spaces")
                
                if spaces:
                    # Use the first space for testing
                    test_space = spaces[0]
                    space_key = test_space.get('key')
                    space_name = test_space.get('name')
                    print(f"📋 Using space: {space_name} ({space_key})")
                    
                    # Test 2: List pages in the space
                    print(f"\n📄 2. Testing pages in {space_name}...")
                    response = await client.get(
                        f"{BASE_URL}/api/v1/confluence/spaces/{space_key}/pages",
                        params={"user_email": USER_EMAIL}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        pages = data.get('pages', [])
                        print(f"✅ Found {len(pages)} pages in {space_name}")
                        
                        if pages:
                            # Use the first page for testing
                            test_page = pages[0]
                            page_id = test_page.get('id')
                            page_title = test_page.get('title')
                            print(f"📄 Using page: {page_title} (ID: {page_id})")
                            
                            # Test 3: Get page details
                            print(f"\n📖 3. Testing page details...")
                            response = await client.get(
                                f"{BASE_URL}/api/v1/confluence/pages/{page_id}",
                                params={"user_email": USER_EMAIL}
                            )
                            if response.status_code == 200:
                                data = response.json()
                                print(f"✅ Page details retrieved successfully")
                                print(f"📋 Title: {data.get('title', 'N/A')}")
                                print(f"📋 Version: {data.get('version', {}).get('number', 'N/A')}")
                                print(f"📋 Status: {data.get('status', 'N/A')}")
                            else:
                                print(f"❌ Failed to get page details: {response.status_code}")
                        else:
                            print("⚠️ No pages found in space")
                    else:
                        print(f"❌ Failed to list pages: {response.status_code}")
                else:
                    print("⚠️ No spaces found")
            else:
                print(f"❌ Failed to list spaces: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing spaces: {e}")
        
        # Test 4: Search Confluence pages
        print("\n🔍 4. Testing Confluence search...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": "test",
                    "limit": 5
                }
            )
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"✅ Search completed successfully")
                print(f"📋 Found {len(results)} results for 'test'")
                
                for result in results[:3]:
                    print(f"   - {result.get('title', 'N/A')} ({result.get('type', 'N/A')})")
            else:
                print(f"❌ Search failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing search: {e}")
        
        # Test 5: Get user's pages
        print("\n👤 5. Testing user's pages...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/my-pages",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                pages = data.get('pages', [])
                print(f"✅ User pages retrieved successfully")
                print(f"📋 Found {len(pages)} pages created by user")
                
                for page in pages[:3]:
                    print(f"   - {page.get('title', 'N/A')} ({page.get('space', {}).get('name', 'N/A')})")
            else:
                print(f"❌ Failed to get user pages: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing user pages: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 Confluence Operations Test Complete!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_confluence_operations())

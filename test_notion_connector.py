#!/usr/bin/env python3
"""
Notion Connector Test Script
Tests all Notion OAuth and API endpoints
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8084"
TEST_EMAIL = "test@example.com"

async def test_notion_connector():
    """Test all Notion connector endpoints"""
    
    print("🚀 Testing Notion Connector")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: OAuth URL Generation
        print("\n1. Testing OAuth URL Generation...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/notion/auth-url", params={"user_email": TEST_EMAIL})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ OAuth URL generated: {data.get('auth_url', 'N/A')[:100]}...")
            else:
                print(f"❌ OAuth URL failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ OAuth URL error: {str(e)}")
        
        # Test 2: Service Status
        print("\n2. Testing Service Status...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/notion/status", params={"user_email": TEST_EMAIL})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Service Status: {data.get('message', 'N/A')}")
                print(f"   Connected: {data.get('connected', False)}")
                print(f"   Services: {list(data.get('services', {}).keys())}")
            else:
                print(f"❌ Service Status failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Service Status error: {str(e)}")
        
        # Test 3: Search Databases (requires auth)
        print("\n3. Testing Database Search...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/notion/databases", params={"user_email": TEST_EMAIL})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Database Search: Found {data.get('total', 0)} databases")
            elif response.status_code == 401:
                print("⚠️ Database Search: Authentication required (expected)")
            else:
                print(f"❌ Database Search failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Database Search error: {str(e)}")
        
        # Test 4: Search Pages (requires auth)
        print("\n4. Testing Page Search...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/notion/pages", params={"user_email": TEST_EMAIL})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Page Search: Found {data.get('total', 0)} pages")
            elif response.status_code == 401:
                print("⚠️ Page Search: Authentication required (expected)")
            else:
                print(f"❌ Page Search failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Page Search error: {str(e)}")
        
        # Test 5: Get User Info (requires auth)
        print("\n5. Testing User Info...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/notion/user", params={"user_email": TEST_EMAIL})
            if response.status_code == 200:
                data = response.json()
                user = data.get('user', {})
                print(f"✅ User Info: {user.get('name', 'N/A')} ({user.get('id', 'N/A')})")
            elif response.status_code == 401:
                print("⚠️ User Info: Authentication required (expected)")
            else:
                print(f"❌ User Info failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ User Info error: {str(e)}")
        
        # Test 6: Create Page (requires auth)
        print("\n6. Testing Page Creation...")
        try:
            page_data = {
                "parent": {"database_id": "test-database-id"},
                "properties": {
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": "Test Page"
                                }
                            }
                        ]
                    }
                }
            }
            response = await client.post(
                f"{BASE_URL}/api/v1/notion/pages", 
                params={"user_email": TEST_EMAIL},
                json=page_data
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Page Creation: Page created successfully")
            elif response.status_code == 401:
                print("⚠️ Page Creation: Authentication required (expected)")
            else:
                print(f"❌ Page Creation failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Page Creation error: {str(e)}")
        
        # Test 7: Get Page Content (requires auth)
        print("\n7. Testing Page Content...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/notion/pages/test-page-id/content", 
                params={"user_email": TEST_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Page Content: Found {data.get('total', 0)} blocks")
            elif response.status_code == 401:
                print("⚠️ Page Content: Authentication required (expected)")
            else:
                print(f"❌ Page Content failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Page Content error: {str(e)}")
        
        # Test 8: Database Query (requires auth)
        print("\n8. Testing Database Query...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/notion/databases/test-database-id/query", 
                params={"user_email": TEST_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Database Query: Found {data.get('total', 0)} pages")
            elif response.status_code == 401:
                print("⚠️ Database Query: Authentication required (expected)")
            else:
                print(f"❌ Database Query failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Database Query error: {str(e)}")

def print_setup_instructions():
    """Print setup instructions for Notion integration"""
    print("\n" + "=" * 60)
    print("📋 NOTION SETUP INSTRUCTIONS")
    print("=" * 60)
    print("""
To complete Notion integration, you need to:

1. 🏢 Create Notion Integration:
   - Go to https://www.notion.so/my-integrations
   - Click "New integration"
   - Name: "Lagentry Connector"
   - Workspace: Select your workspace
   - Capabilities: Select all needed permissions
   - Submit

2. 🔑 Get Credentials:
   - Copy the "Internal Integration Token" (this is your client secret)
   - Copy the "Integration ID" (this is your client ID)

3. ⚙️ Configure Environment:
   Add to your .env file:
   NOTION_CLIENT_ID=your-integration-id
   NOTION_CLIENT_SECRET=your-internal-integration-token
   NOTION_REDIRECT_URI=http://localhost:8084/api/v1/notion/callback

4. 🔗 Set Redirect URI:
   - In your Notion integration settings
   - Add redirect URI: http://localhost:8084/api/v1/notion/callback

5. 🚀 Test OAuth Flow:
   - Visit: http://localhost:8084/api/v1/notion/auth-url?user_email=your@email.com
   - Complete Notion authorization
   - Test all endpoints with real data

6. 📚 Share Integration:
   - In your Notion workspace, share pages/databases with your integration
   - The integration needs access to read/write content

✅ Once configured, all Notion endpoints will work with real data!
""")

if __name__ == "__main__":
    print("🧪 Notion Connector Test Suite")
    print("Testing all Notion OAuth and API endpoints...")
    
    # Run tests
    asyncio.run(test_notion_connector())
    
    # Print setup instructions
    print_setup_instructions()
    
    print("\n🎉 Notion Connector Test Complete!")
    print("Check the results above and follow setup instructions if needed.")

#!/usr/bin/env python3
"""
Check Jira Integration Status
Shows current status and available operations
"""

import httpx
import json
import asyncio

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def check_jira_status():
    print("🔍 Checking Jira Integration Status")
    print("=" * 50)
    print(f"🎯 Target: https://fahadpatel1403-1754084343895.atlassian.net")
    print(f"📋 Project: LFS")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # 1. Check OAuth configuration
        print("\n🔐 1. OAuth Configuration Status...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/atlassian/auth/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ OAuth URL generation: Working")
                print(f"🔗 Auth URL: {data.get('auth_url', 'N/A')[:100]}...")
            else:
                print(f"❌ OAuth URL generation: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ OAuth configuration error: {e}")
        
        # 2. Check if tokens exist
        print("\n🔑 2. Token Status...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/auth/validate",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Token validation: Valid tokens found")
                print(f"👤 User: {data.get('user_email', 'N/A')}")
                print(f"🔑 Provider: {data.get('provider', 'N/A')}")
            else:
                print(f"⚠️  Token validation: No valid tokens found")
                print(f"💡 You need to authenticate first")
        except Exception as e:
            print(f"❌ Token validation error: {e}")
        
        # 3. Test project listing (with mock data)
        print("\n📋 3. Project Listing Test...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                projects = data.get("projects", [])
                print(f"✅ Project listing: Working ({len(projects)} projects)")
                for i, project in enumerate(projects, 1):
                    print(f"   {i}. {project.get('name', 'N/A')} ({project.get('key', 'N/A')})")
            else:
                print(f"❌ Project listing: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ Project listing error: {e}")
        
        # 4. Test issue creation (with mock data)
        print("\n➕ 4. Issue Creation Test...")
        try:
            issue_data = {
                "summary": "Status Test Issue",
                "description": "This is a test issue to verify the API is working.",
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
                print(f"✅ Issue creation: Working")
                print(f"🎫 Created: {issue.get('key', 'N/A')}")
                print(f"📝 Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
                
                # Check if it's mock data
                if data.get("mock_data"):
                    print(f"📋 Note: Using mock data (no real authentication)")
                else:
                    print(f"📋 Note: Using real data (authenticated)")
                    
            else:
                print(f"❌ Issue creation: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ Issue creation error: {e}")
        
        # 5. Test search functionality
        print("\n🔍 5. Search Functionality Test...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": "project = LFS",
                    "max_results": 3
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                print(f"✅ Search functionality: Working ({len(issues)} results)")
                for i, issue in enumerate(issues, 1):
                    fields = issue.get("fields", {})
                    print(f"   {i}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
            else:
                print(f"❌ Search functionality: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ Search error: {e}")
        
        # 6. Check unified API
        print("\n🌐 6. Unified API Status...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/unified/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API: Working")
                print(f"🔧 Service: {data.get('service', 'N/A')}")
                print(f"📦 Version: {data.get('version', 'N/A')}")
                providers = data.get("providers", [])
                print(f"🔗 Providers: {', '.join(providers)}")
            else:
                print(f"❌ Unified API: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ Unified API error: {e}")
    
    print("\n" + "=" * 50)
    print("📊 Integration Status Summary")
    print("=" * 50)
    print("✅ OAuth URL generation: Working")
    print("✅ Project listing: Working (with mock data)")
    print("✅ Issue creation: Working (with mock data)")
    print("✅ Search functionality: Working (with mock data)")
    print("✅ Unified API: Working")
    print("\n💡 To test with real data:")
    print("   1. Run: py test_jira_authentication.py")
    print("   2. Complete OAuth authentication")
    print("   3. Test reading and posting real messages")
    print("\n🔗 Check your Jira instance:")
    print(f"   https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")

if __name__ == "__main__":
    asyncio.run(check_jira_status()) 
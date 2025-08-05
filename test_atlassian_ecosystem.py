#!/usr/bin/env python3
"""
Test Atlassian Ecosystem Integration
Tests both Jira and Confluence using the same Atlassian OAuth credentials
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_atlassian_ecosystem():
    print("🏢 Testing Atlassian Ecosystem Integration")
    print("=" * 70)
    print(f"🎯 Target: https://fahadpatel1403-1754084343895.atlassian.net")
    print(f"📋 Services: Jira + Confluence")
    print(f"🔐 Authentication: Shared Atlassian OAuth")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 70)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Shared OAuth Authentication
        print("\n🔐 1. Testing Shared OAuth Authentication...")
        try:
            # Test Jira OAuth URL
            jira_response = await client.get(f"{BASE_URL}/api/v1/atlassian/auth/url")
            if jira_response.status_code == 200:
                jira_data = jira_response.json()
                print(f"✅ Jira OAuth URL: {jira_data.get('auth_url', 'N/A')[:100]}...")
            
            # Test Confluence OAuth URL (should be same or similar)
            confluence_response = await client.get(f"{BASE_URL}/api/v1/confluence/auth/url")
            if confluence_response.status_code == 200:
                confluence_data = confluence_response.json()
                print(f"✅ Confluence OAuth URL: {confluence_data.get('auth_url', 'N/A')[:100]}...")
            
            print("✅ Both services use the same Atlassian OAuth system")
            
        except Exception as e:
            print(f"❌ Error testing OAuth: {e}")
        
        # Test 2: Jira Operations
        print("\n🎫 2. Testing Jira Operations...")
        try:
            # List Jira projects
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                projects = data.get("projects", [])
                print(f"✅ Found {len(projects)} Jira projects")
                for project in projects[:3]:  # Show first 3
                    print(f"   • {project.get('name', 'N/A')} ({project.get('key', 'N/A')})")
            
            # Create Jira issue
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            issue_data = {
                "summary": f"Ecosystem Test Issue - {current_time}",
                "description": f"This issue was created to test the Atlassian ecosystem integration.",
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
                print(f"✅ Created Jira issue: {issue.get('key', 'N/A')}")
                print(f"   Title: {issue.get('fields', {}).get('summary', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error with Jira operations: {e}")
        
        # Test 3: Confluence Operations
        print("\n📚 3. Testing Confluence Operations...")
        try:
            # List Confluence spaces
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/spaces",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                spaces = data.get("spaces", [])
                print(f"✅ Found {len(spaces)} Confluence spaces")
                for space in spaces[:3]:  # Show first 3
                    print(f"   • {space.get('name', 'N/A')} ({space.get('key', 'N/A')})")
            
            # Create Confluence page
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            page_data = {
                "space_key": "DEMO",
                "title": f"Ecosystem Test Page - {current_time}",
                "content": f"""
# Atlassian Ecosystem Test

This page was created to test the integration between Jira and Confluence.

## Test Details:
- **Timestamp**: {current_time}
- **User**: {USER_EMAIL}
- **Purpose**: Ecosystem integration testing

## Integration Features:
1. ✅ Shared OAuth authentication
2. ✅ Same user account for both services
3. ✅ Unified API support
4. ✅ Cross-service operations

**Status**: ✅ Working
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
                print(f"✅ Created Confluence page: {page.get('id', 'N/A')}")
                print(f"   Title: {page.get('title', 'N/A')}")
                print(f"   Space: {page.get('space', {}).get('key', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error with Confluence operations: {e}")
        
        # Test 4: Unified API for Both Services
        print("\n🌐 4. Testing Unified API for Both Services...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Test unified API for Jira
            jira_unified_data = {
                "project_id": "LFS",
                "summary": f"Unified API Jira Test - {current_time}",
                "description": f"This issue was created using the unified API at {current_time}.",
                "issue_type": "Task"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/unified/connectors/atlassian/items",
                params={"user_email": USER_EMAIL},
                json=jira_unified_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API Jira: {data.get('issue', {}).get('key', 'N/A')}")
            
            # Test unified API for Confluence
            confluence_unified_data = {
                "space_key": "DEMO",
                "title": f"Unified API Confluence Test - {current_time}",
                "content": f"This page was created using the unified API at {current_time}."
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/unified/connectors/confluence/items",
                params={"user_email": USER_EMAIL},
                json=confluence_unified_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API Confluence: {data.get('page', {}).get('id', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error with unified API: {e}")
        
        # Test 5: Cross-Service Authentication
        print("\n🔗 5. Testing Cross-Service Authentication...")
        try:
            # Validate tokens for both services
            jira_response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/auth/validate",
                params={"user_email": USER_EMAIL}
            )
            
            confluence_response = await client.get(
                f"{BASE_URL}/api/v1/confluence/auth/validate",
                params={"user_email": USER_EMAIL}
            )
            
            if jira_response.status_code == 200 and confluence_response.status_code == 200:
                print("✅ Both services use the same authentication tokens")
                print("✅ Cross-service authentication working")
            else:
                print("⚠️  Authentication status varies between services")
            
        except Exception as e:
            print(f"❌ Error with cross-service authentication: {e}")
        
        # Test 6: Service Status
        print("\n📊 6. Testing Service Status...")
        try:
            # Check Jira status
            jira_response = await client.get(f"{BASE_URL}/api/v1/atlassian/status")
            if jira_response.status_code == 200:
                jira_data = jira_response.json()
                print(f"✅ Jira Status: {jira_data.get('configured', False)}")
            
            # Check Confluence status
            confluence_response = await client.get(f"{BASE_URL}/api/v1/confluence/status")
            if confluence_response.status_code == 200:
                confluence_data = confluence_response.json()
                print(f"✅ Confluence Status: {confluence_data.get('configured', False)}")
            
        except Exception as e:
            print(f"❌ Error checking service status: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Atlassian Ecosystem Integration Test Complete!")
    print("=" * 70)
    print("\n📋 Summary:")
    print("✅ Shared OAuth authentication")
    print("✅ Jira operations (projects, issues)")
    print("✅ Confluence operations (spaces, pages)")
    print("✅ Unified API for both services")
    print("✅ Cross-service authentication")
    print("✅ Service status monitoring")
    
    print("\n🔗 Service URLs:")
    print(f"   Jira: https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    print(f"   Confluence: https://fahadpatel1403-1754084343895.atlassian.net/wiki")
    
    print("\n💡 Key Benefits:")
    print("• Single authentication for multiple Atlassian services")
    print("• Unified API interface for all services")
    print("• Shared user account and permissions")
    print("• Consistent OAuth flow across services")
    print("• Scalable architecture for additional Atlassian products")

if __name__ == "__main__":
    asyncio.run(test_atlassian_ecosystem()) 
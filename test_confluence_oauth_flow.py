#!/usr/bin/env python3
"""
Test Complete Confluence OAuth Flow
Tests the entire OAuth process from URL generation to token validation
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_confluence_oauth_flow():
    print("🔄 Testing Complete Confluence OAuth Flow")
    print("=" * 60)
    print(f"🎯 Target: {BASE_URL}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Step 1: Generate OAuth URL
        print("\n🔐 Step 1: Generate OAuth URL")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/confluence/auth/url")
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get('auth_url', '')
                print(f"✅ OAuth URL generated successfully")
                print(f"🔗 URL: {auth_url[:100]}...")
                
                # Verify redirect URI is correct
                if "127.0.0.1:8083" in auth_url:
                    print("✅ Redirect URI is correct")
                else:
                    print("❌ Redirect URI is incorrect")
                    
            else:
                print(f"❌ Failed to generate OAuth URL: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Error generating OAuth URL: {e}")
            return
        
        # Step 2: Check current token status
        print("\n🔍 Step 2: Check current token status")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/auth/validate",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('valid', False):
                    print("✅ Valid tokens found")
                    print(f"📋 User info: {data.get('user_info', {}).get('name', 'N/A')}")
                else:
                    print("⚠️ No valid tokens found - OAuth flow needed")
                    print(f"📋 Reason: {data.get('reason', 'Unknown')}")
            else:
                print(f"❌ Token validation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking token status: {e}")
        
        # Step 3: Test Confluence status endpoint
        print("\n📊 Step 3: Test Confluence status")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/confluence/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status endpoint working")
                print(f"📋 Provider: {data.get('provider', 'N/A')}")
                print(f"⚙️ Configured: {data.get('configured', False)}")
                print(f"🔗 Available endpoints: {len(data.get('endpoints', []))}")
            else:
                print(f"❌ Status endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking status: {e}")
        
        # Step 4: Test Confluence spaces (if tokens are valid)
        print("\n📚 Step 4: Test Confluence spaces")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/spaces",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                spaces = data.get('spaces', [])
                print(f"✅ Spaces endpoint working")
                print(f"📋 Found {len(spaces)} spaces")
                for space in spaces[:3]:  # Show first 3 spaces
                    print(f"   - {space.get('name', 'N/A')} ({space.get('key', 'N/A')})")
            else:
                print(f"⚠️ Spaces endpoint returned: {response.status_code}")
                print(f"📋 This is expected if no valid tokens")
        except Exception as e:
            print(f"❌ Error testing spaces: {e}")
        
        # Step 5: Compare with Atlassian OAuth
        print("\n🔄 Step 5: Compare with Atlassian OAuth")
        try:
            # Get Confluence OAuth URL
            confluence_response = await client.get(f"{BASE_URL}/api/v1/confluence/auth/url")
            confluence_data = confluence_response.json() if confluence_response.status_code == 200 else {}
            
            # Get Atlassian OAuth URL
            atlassian_response = await client.get(f"{BASE_URL}/api/v1/atlassian/auth/url")
            atlassian_data = atlassian_response.json() if atlassian_response.status_code == 200 else {}
            
            if confluence_data.get('auth_url') and atlassian_data.get('auth_url'):
                print("✅ Both OAuth URLs generated successfully")
                
                # Check if they use the same client ID
                confluence_url = confluence_data['auth_url']
                atlassian_url = atlassian_data['auth_url']
                
                if "BNoM86R3TvFGr0zttvS10FVESd9Onxh4" in confluence_url and "BNoM86R3TvFGr0zttvS10FVESd9Onxh4" in atlassian_url:
                    print("✅ Both use the same Atlassian client ID")
                else:
                    print("❌ Different client IDs detected")
                    
            else:
                print("❌ Failed to generate one or both OAuth URLs")
                
        except Exception as e:
            print(f"❌ Error comparing OAuth URLs: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 Confluence OAuth Flow Test Complete!")
        print("=" * 60)
        
        # Summary and next steps
        print("\n📋 **Next Steps:**")
        print("1. 🔐 Complete OAuth flow with Atlassian")
        print("2. 📚 Test Confluence page operations")
        print("3. 🔗 Test Jira-Confluence integration")
        print("4. 🚀 Deploy to production")

if __name__ == "__main__":
    asyncio.run(test_confluence_oauth_flow())

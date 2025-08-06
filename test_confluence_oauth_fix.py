#!/usr/bin/env python3
"""
Test Confluence OAuth Fix
Verifies that the Confluence OAuth URL generation works correctly with the fixed configuration
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"

async def test_confluence_oauth_fix():
    print("🔧 Testing Confluence OAuth Fix")
    print("=" * 60)
    print(f"🎯 Target: http://127.0.0.1:8083")
    print(f"📋 Testing OAuth URL generation with correct redirect URI")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Basic OAuth URL generation
        print("\n🔐 1. Testing basic OAuth URL generation...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/confluence/auth/url")
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get('auth_url', '')
                print(f"✅ OAuth URL generated successfully")
                print(f"🔗 URL: {auth_url[:100]}...")
                
                # Check if redirect URI is correct
                if "127.0.0.1:8083" in auth_url:
                    print("✅ Redirect URI is correctly set to port 8083")
                else:
                    print("❌ Redirect URI is incorrect")
                    
            else:
                print(f"❌ Failed to generate OAuth URL: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Error generating OAuth URL: {e}")
        
        # Test 2: OAuth URL with custom state and scopes
        print("\n🔐 2. Testing OAuth URL with custom parameters...")
        try:
            params = {
                "state": "test123",
                "scopes": [
                    "read:confluence-content.all",
                    "write:confluence-content",
                    "read:confluence-space.summary",
                    "read:confluence-user"
                ]
            }
            
            response = await client.get(f"{BASE_URL}/api/v1/confluence/auth/url", params=params)
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get('auth_url', '')
                print(f"✅ OAuth URL with custom parameters generated successfully")
                print(f"🔗 URL: {auth_url[:100]}...")
                
                # Verify parameters are included
                if "test123" in auth_url:
                    print("✅ State parameter included correctly")
                if "read:confluence-content.all" in auth_url:
                    print("✅ Custom scopes included correctly")
                    
            else:
                print(f"❌ Failed to generate OAuth URL with parameters: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error generating OAuth URL with parameters: {e}")
        
        # Test 3: Check status endpoint
        print("\n📊 3. Testing Confluence status endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/confluence/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status endpoint working")
                print(f"📋 Provider: {data.get('provider', 'N/A')}")
                print(f"⚙️ Configured: {data.get('configured', False)}")
                print(f"🔗 Endpoints: {len(data.get('endpoints', []))} available")
                
            else:
                print(f"❌ Status endpoint failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking status: {e}")
        
        # Test 4: Compare with Atlassian OAuth URL
        print("\n🔄 4. Comparing with Atlassian OAuth URL...")
        try:
            # Get Confluence OAuth URL
            confluence_response = await client.get(f"{BASE_URL}/api/v1/confluence/auth/url")
            confluence_data = confluence_response.json() if confluence_response.status_code == 200 else {}
            
            # Get Atlassian OAuth URL
            atlassian_response = await client.get(f"{BASE_URL}/api/v1/atlassian/auth/url")
            atlassian_data = atlassian_response.json() if atlassian_response.status_code == 200 else {}
            
            if confluence_data.get('auth_url') and atlassian_data.get('auth_url'):
                print("✅ Both Confluence and Atlassian OAuth URLs generated successfully")
                
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
        print("🎉 Confluence OAuth Fix Test Complete!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_confluence_oauth_fix())

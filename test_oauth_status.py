#!/usr/bin/env python3
"""
Test script to show OAuth status and explain expected behavior
"""

import asyncio
import httpx
import json

async def test_oauth_status():
    """Test the OAuth status and explain expected behavior"""
    base_url = "http://127.0.0.1:8083"

    print("🔍 OAUTH STATUS TEST")
    print("=" * 60)

    # Test OAuth URLs (should all work)
    print("\n✅ TESTING OAUTH URLs (Should all return 200 OK):")
    print("-" * 50)

    providers = ["google", "slack", "atlassian"]
    
    for provider in providers:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/api/v1/unified/auth/{provider}/url")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ {provider.upper()}: {data['auth_url'][:80]}...")
                else:
                    print(f"❌ {provider.upper()}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ {provider.upper()}: Error - {e}")

    # Test capabilities (should all work)
    print("\n✅ TESTING CAPABILITIES (Should all return 200 OK):")
    print("-" * 50)

    connectors = ["gmail", "slack", "jira"]
    
    for connector in connectors:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/api/v1/unified/connectors/{connector}/capabilities?user_email=test@example.com")
                if response.status_code == 200:
                    data = response.json()
                    capabilities = data.get("capabilities", {}).get("capabilities", [])
                    print(f"✅ {connector.upper()}: {len(capabilities)} capabilities available")
                else:
                    print(f"❌ {connector.upper()}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ {connector.upper()}: Error - {e}")

    # Test data endpoints (should return 400 - this is EXPECTED)
    print("\n⚠️  TESTING DATA ENDPOINTS (400 errors are EXPECTED - no tokens):")
    print("-" * 50)

    data_endpoints = [
        ("gmail", "/gmail/emails"),
        ("slack", "/slack/channels"),
        ("jira", "/jira/projects")
    ]
    
    for provider, endpoint in data_endpoints:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/api/v1/unified{endpoint}?user_email=test@example.com")
                if response.status_code == 400:
                    print(f"⚠️  {provider.upper()}: 400 (EXPECTED - No authentication tokens)")
                else:
                    print(f"❌ {provider.upper()}: Unexpected {response.status_code}")
        except Exception as e:
            print(f"❌ {provider.upper()}: Error - {e}")

    # Test available providers
    print("\n✅ TESTING AVAILABLE PROVIDERS:")
    print("-" * 50)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/v1/unified/auth/providers")
            if response.status_code == 200:
                data = response.json()
                providers = data.get("providers", {})
                for provider, info in providers.items():
                    status = "✅ configured" if info.get("configured") else "❌ not configured"
                    print(f"   {provider}: {status}")
            else:
                print(f"❌ Providers: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Providers: Error - {e}")

    print("\n" + "=" * 60)
    print("📋 EXPLANATION:")
    print("=" * 60)
    print("✅ OAuth URLs (200 OK): Working correctly - ready for authentication")
    print("✅ Capabilities (200 OK): Working correctly - showing available features")
    print("⚠️  Data endpoints (400): EXPECTED - No authentication tokens present")
    print("")
    print("🔑 TO FIX 400 ERRORS:")
    print("1. Visit the OAuth URLs to authenticate")
    print("2. Complete the OAuth flow to get access tokens")
    print("3. Data endpoints will then return 200 OK with real data")
    print("")
    print("🌐 OAuth URLs to visit:")
    print("- Google: http://127.0.0.1:8083/api/v1/unified/auth/google/url")
    print("- Slack: http://127.0.0.1:8083/api/v1/unified/auth/slack/url")
    print("- Atlassian: http://127.0.0.1:8083/api/v1/unified/auth/atlassian/url")

if __name__ == "__main__":
    asyncio.run(test_oauth_status()) 
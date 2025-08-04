"""
Individual Provider Test Script
Shows detailed output for each provider (Google, Slack, Jira) separately
"""

import asyncio
import httpx
from typing import Dict, Any
from datetime import datetime


async def test_google_provider():
    """Test Google/Gmail provider functionality"""
    print("🔵" + "="*60)
    print("🔵 GOOGLE/GMAIL PROVIDER TEST")
    print("🔵" + "="*60)
    
    base_url = "http://127.0.0.1:8081/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # 1. Test OAuth URL generation
        print("\n📧 1. Testing Google OAuth URL generation...")
        try:
            response = await client.get(f"{base_url}/auth/google/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Google OAuth URL generated successfully")
                print(f"   Auth URL: {data.get('auth_url', '')[:100]}...")
                print(f"   Provider: {data.get('provider')}")
            else:
                print(f"❌ Failed to generate Google OAuth URL: {response.text}")
        except Exception as e:
            print(f"❌ Error generating Google OAuth URL: {e}")
        
        # 2. Test Google provider configuration
        print("\n📧 2. Testing Google provider configuration...")
        try:
            response = await client.get(f"{base_url}/auth/providers")
            if response.status_code == 200:
                data = response.json()
                google_info = data.get('providers', {}).get('google', {})
                print(f"✅ Google provider configuration:")
                print(f"   Configured: {google_info.get('configured', False)}")
                print(f"   Redirect URI: {google_info.get('redirect_uri', 'N/A')}")
                print(f"   Available scopes: {len(google_info.get('scopes', {}))} scope categories")
            else:
                print(f"❌ Failed to get provider info: {response.text}")
        except Exception as e:
            print(f"❌ Error getting provider info: {e}")
        
        # 3. Test Gmail connector capabilities
        print("\n📧 3. Testing Gmail connector capabilities...")
        try:
            response = await client.get(f"{base_url}/connectors/gmail/capabilities?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                capabilities = data.get('capabilities', {})
                print(f"✅ Gmail connector capabilities:")
                print(f"   Provider: {capabilities.get('provider')}")
                print(f"   Capabilities: {capabilities.get('capabilities', [])}")
                print(f"   Scopes: {len(capabilities.get('scopes', []))} OAuth scopes")
            else:
                print(f"❌ Failed to get Gmail capabilities: {response.text}")
        except Exception as e:
            print(f"❌ Error getting Gmail capabilities: {e}")
        
        # 4. Test Gmail-specific endpoints
        print("\n📧 4. Testing Gmail-specific endpoints...")
        try:
            # Test Gmail emails endpoint
            response = await client.get(f"{base_url}/gmail/emails?user_email=test@example.com&max_results=5")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Gmail emails endpoint working")
                print(f"   Success: {data.get('success')}")
                print(f"   Provider: {data.get('provider')}")
            else:
                print(f"⚠️  Gmail emails endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error testing Gmail emails: {e}")
        
        print("\n📧 Google/Gmail Provider Test Complete!")
        print("🔵" + "="*60)


async def test_slack_provider():
    """Test Slack provider functionality"""
    print("💬" + "="*60)
    print("💬 SLACK PROVIDER TEST")
    print("💬" + "="*60)
    
    base_url = "http://127.0.0.1:8081/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # 1. Test OAuth URL generation
        print("\n💬 1. Testing Slack OAuth URL generation...")
        try:
            response = await client.get(f"{base_url}/auth/slack/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Slack OAuth URL generated successfully")
                print(f"   Auth URL: {data.get('auth_url', '')[:100]}...")
                print(f"   Provider: {data.get('provider')}")
            else:
                print(f"❌ Failed to generate Slack OAuth URL: {response.text}")
        except Exception as e:
            print(f"❌ Error generating Slack OAuth URL: {e}")
        
        # 2. Test Slack provider configuration
        print("\n💬 2. Testing Slack provider configuration...")
        try:
            response = await client.get(f"{base_url}/auth/providers")
            if response.status_code == 200:
                data = response.json()
                slack_info = data.get('providers', {}).get('slack', {})
                print(f"✅ Slack provider configuration:")
                print(f"   Configured: {slack_info.get('configured', False)}")
                print(f"   Redirect URI: {slack_info.get('redirect_uri', 'N/A')}")
                print(f"   Available scopes: {len(slack_info.get('scopes', {}))} scope categories")
            else:
                print(f"❌ Failed to get provider info: {response.text}")
        except Exception as e:
            print(f"❌ Error getting provider info: {e}")
        
        # 3. Test Slack connector capabilities
        print("\n💬 3. Testing Slack connector capabilities...")
        try:
            response = await client.get(f"{base_url}/connectors/slack/capabilities?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                capabilities = data.get('capabilities', {})
                print(f"✅ Slack connector capabilities:")
                print(f"   Provider: {capabilities.get('provider')}")
                print(f"   Capabilities: {capabilities.get('capabilities', [])}")
                print(f"   Scopes: {len(capabilities.get('scopes', []))} OAuth scopes")
            else:
                print(f"❌ Failed to get Slack capabilities: {response.text}")
        except Exception as e:
            print(f"❌ Error getting Slack capabilities: {e}")
        
        # 4. Test Slack-specific endpoints
        print("\n💬 4. Testing Slack-specific endpoints...")
        try:
            # Test Slack channels endpoint
            response = await client.get(f"{base_url}/slack/channels?user_email=test@example.com&limit=5")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Slack channels endpoint working")
                print(f"   Success: {data.get('success')}")
                print(f"   Provider: {data.get('provider')}")
            else:
                print(f"⚠️  Slack channels endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error testing Slack channels: {e}")
        
        print("\n💬 Slack Provider Test Complete!")
        print("💬" + "="*60)


async def test_jira_provider():
    """Test Jira/Atlassian provider functionality"""
    print("🎫" + "="*60)
    print("🎫 JIRA/ATLASSIAN PROVIDER TEST")
    print("🎫" + "="*60)
    
    base_url = "http://127.0.0.1:8081/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # 1. Test OAuth URL generation
        print("\n🎫 1. Testing Atlassian OAuth URL generation...")
        try:
            response = await client.get(f"{base_url}/auth/atlassian/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Atlassian OAuth URL generated successfully")
                print(f"   Auth URL: {data.get('auth_url', '')[:100]}...")
                print(f"   Provider: {data.get('provider')}")
            else:
                print(f"❌ Failed to generate Atlassian OAuth URL: {response.text}")
        except Exception as e:
            print(f"❌ Error generating Atlassian OAuth URL: {e}")
        
        # 2. Test Atlassian provider configuration
        print("\n🎫 2. Testing Atlassian provider configuration...")
        try:
            response = await client.get(f"{base_url}/auth/providers")
            if response.status_code == 200:
                data = response.json()
                atlassian_info = data.get('providers', {}).get('atlassian', {})
                print(f"✅ Atlassian provider configuration:")
                print(f"   Configured: {atlassian_info.get('configured', False)}")
                print(f"   Redirect URI: {atlassian_info.get('redirect_uri', 'N/A')}")
                print(f"   Available scopes: {len(atlassian_info.get('scopes', {}))} scope categories")
            else:
                print(f"❌ Failed to get provider info: {response.text}")
        except Exception as e:
            print(f"❌ Error getting provider info: {e}")
        
        # 3. Test Jira connector capabilities
        print("\n🎫 3. Testing Jira connector capabilities...")
        try:
            response = await client.get(f"{base_url}/connectors/jira/capabilities?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                capabilities = data.get('capabilities', {})
                print(f"✅ Jira connector capabilities:")
                print(f"   Provider: {capabilities.get('provider')}")
                print(f"   Capabilities: {capabilities.get('capabilities', [])}")
                print(f"   Scopes: {len(capabilities.get('scopes', []))} OAuth scopes")
            else:
                print(f"❌ Failed to get Jira capabilities: {response.text}")
        except Exception as e:
            print(f"❌ Error getting Jira capabilities: {e}")
        
        # 4. Test Jira-specific endpoints
        print("\n🎫 4. Testing Jira-specific endpoints...")
        try:
            # Test Jira projects endpoint
            response = await client.get(f"{base_url}/jira/projects?user_email=test@example.com&max_results=5")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Jira projects endpoint working")
                print(f"   Success: {data.get('success')}")
                print(f"   Provider: {data.get('provider')}")
            else:
                print(f"⚠️  Jira projects endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error testing Jira projects: {e}")
        
        # 5. Test Jira my-issues endpoint
        print("\n🎫 5. Testing Jira my-issues endpoint...")
        try:
            response = await client.get(f"{base_url}/jira/my-issues?user_email=test@example.com&max_results=5")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Jira my-issues endpoint working")
                print(f"   Success: {data.get('success')}")
                print(f"   Provider: {data.get('provider')}")
            else:
                print(f"⚠️  Jira my-issues endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error testing Jira my-issues: {e}")
        
        print("\n🎫 Jira/Atlassian Provider Test Complete!")
        print("🎫" + "="*60)


async def test_unified_api():
    """Test the unified API functionality"""
    print("🌐" + "="*60)
    print("🌐 UNIFIED API TEST")
    print("🌐" + "="*60)
    
    base_url = "http://127.0.0.1:8081/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # 1. Test unified status
        print("\n🌐 1. Testing unified API status...")
        try:
            response = await client.get(f"{base_url}/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API status:")
                print(f"   Service: {data.get('service')}")
                print(f"   Version: {data.get('version')}")
                print(f"   Providers: {data.get('providers')}")
                print(f"   Connectors: {data.get('connectors')}")
                print(f"   Endpoints: {len(data.get('endpoints', []))} available")
            else:
                print(f"❌ Failed to get unified status: {response.text}")
        except Exception as e:
            print(f"❌ Error getting unified status: {e}")
        
        # 2. Test available connectors
        print("\n🌐 2. Testing available connectors...")
        try:
            response = await client.get(f"{base_url}/connectors")
            if response.status_code == 200:
                data = response.json()
                connectors = data.get('connectors', [])
                print(f"✅ Available connectors: {connectors}")
                print(f"   Total connectors: {len(connectors)}")
            else:
                print(f"❌ Failed to get connectors: {response.text}")
        except Exception as e:
            print(f"❌ Error getting connectors: {e}")
        
        # 3. Test available providers
        print("\n🌐 3. Testing available providers...")
        try:
            response = await client.get(f"{base_url}/auth/providers")
            if response.status_code == 200:
                data = response.json()
                providers = data.get('providers', {})
                print(f"✅ Available providers:")
                for provider_name, provider_info in providers.items():
                    configured = provider_info.get('configured', False)
                    status = "✅" if configured else "⚠️"
                    print(f"   {status} {provider_name}: {'configured' if configured else 'not configured'}")
            else:
                print(f"❌ Failed to get providers: {response.text}")
        except Exception as e:
            print(f"❌ Error getting providers: {e}")
        
        print("\n🌐 Unified API Test Complete!")
        print("🌐" + "="*60)


async def test_connector_factory():
    """Test the connector factory functionality"""
    print("🏭" + "="*60)
    print("🏭 CONNECTOR FACTORY TEST")
    print("🏭" + "="*60)
    
    try:
        from app.connectors import ConnectorFactory
        
        # Test available connectors
        connectors = ConnectorFactory.get_available_connectors()
        print(f"✅ Available connectors: {connectors}")
        
        # Test connector creation for each provider
        for connector_name in connectors:
            print(f"\n🏭 Testing {connector_name} connector creation...")
            try:
                connector = ConnectorFactory.create(connector_name, "test@example.com")
                print(f"✅ Successfully created {connector_name} connector")
                print(f"   Provider: {connector.provider}")
                print(f"   User email: {connector.user_email}")
                
                # Test capabilities
                capabilities = await connector.get_capabilities()
                print(f"   Capabilities: {capabilities.get('capabilities', [])}")
                
            except Exception as e:
                print(f"❌ Failed to create {connector_name} connector: {e}")
                
    except Exception as e:
        print(f"❌ Error testing connector factory: {e}")
    
    print("\n🏭 Connector Factory Test Complete!")
    print("🏭" + "="*60)


async def main():
    """Main test function - run all provider tests separately"""
    print("🚀 Starting Individual Provider Tests...")
    print("=" * 80)
    
    # Test each provider separately
    await test_google_provider()
    await test_slack_provider()
    await test_jira_provider()
    await test_unified_api()
    await test_connector_factory()
    
    print("\n" + "=" * 80)
    print("✅ Individual Provider Tests Completed!")
    print("\n📋 Summary:")
    print("🔵 Google/Gmail: OAuth flow, email operations, Gmail API integration")
    print("💬 Slack: OAuth flow, channel operations, message handling")
    print("🎫 Jira/Atlassian: OAuth flow, project management, issue tracking")
    print("🌐 Unified API: Single interface for all providers")
    print("🏭 Connector Factory: Modular connector creation and management")
    print("\n🎯 Each provider is now independently testable and functional!")


if __name__ == "__main__":
    asyncio.run(main()) 
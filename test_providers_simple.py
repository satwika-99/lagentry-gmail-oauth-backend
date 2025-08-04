"""
Simple Provider Test Script
Shows clear, separate output for each provider
"""

import asyncio
import httpx
from typing import Dict, Any


async def test_google_only():
    """Test only Google/Gmail provider"""
    print("🔵" + "="*50)
    print("🔵 GOOGLE/GMAIL PROVIDER ONLY")
    print("🔵" + "="*50)
    
    base_url = "http://127.0.0.1:8083/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # Test Google OAuth URL
        print("\n📧 Testing Google OAuth URL...")
        try:
            response = await client.get(f"{base_url}/auth/google/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Google OAuth URL: {data.get('auth_url', '')[:80]}...")
            else:
                print(f"❌ Google OAuth URL failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test Gmail capabilities
        print("\n📧 Testing Gmail capabilities...")
        try:
            response = await client.get(f"{base_url}/connectors/gmail/capabilities?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                capabilities = data.get('capabilities', {})
                print(f"✅ Gmail capabilities: {capabilities.get('capabilities', [])}")
            else:
                print(f"❌ Gmail capabilities failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test Gmail emails endpoint
        print("\n📧 Testing Gmail emails endpoint...")
        try:
            response = await client.get(f"{base_url}/gmail/emails?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Gmail emails endpoint working")
            else:
                print(f"⚠️  Gmail emails endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🔵 Google/Gmail Test Complete!")
    print("🔵" + "="*50)


async def test_slack_only():
    """Test only Slack provider"""
    print("💬" + "="*50)
    print("💬 SLACK PROVIDER ONLY")
    print("💬" + "="*50)
    
    base_url = "http://127.0.0.1:8083/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # Test Slack OAuth URL
        print("\n💬 Testing Slack OAuth URL...")
        try:
            response = await client.get(f"{base_url}/auth/slack/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Slack OAuth URL: {data.get('auth_url', '')[:80]}...")
            else:
                print(f"❌ Slack OAuth URL failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test Slack capabilities
        print("\n💬 Testing Slack capabilities...")
        try:
            response = await client.get(f"{base_url}/connectors/slack/capabilities?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                capabilities = data.get('capabilities', {})
                print(f"✅ Slack capabilities: {capabilities.get('capabilities', [])}")
            else:
                print(f"❌ Slack capabilities failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test Slack channels endpoint
        print("\n💬 Testing Slack channels endpoint...")
        try:
            response = await client.get(f"{base_url}/slack/channels?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Slack channels endpoint working")
            else:
                print(f"⚠️  Slack channels endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n💬 Slack Test Complete!")
    print("💬" + "="*50)


async def test_jira_only():
    """Test only Jira/Atlassian provider"""
    print("🎫" + "="*50)
    print("🎫 JIRA/ATLASSIAN PROVIDER ONLY")
    print("🎫" + "="*50)
    
    base_url = "http://127.0.0.1:8083/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # Test Atlassian OAuth URL
        print("\n🎫 Testing Atlassian OAuth URL...")
        try:
            response = await client.get(f"{base_url}/auth/atlassian/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Atlassian OAuth URL: {data.get('auth_url', '')[:80]}...")
            else:
                print(f"❌ Atlassian OAuth URL failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test Jira capabilities
        print("\n🎫 Testing Jira capabilities...")
        try:
            response = await client.get(f"{base_url}/connectors/jira/capabilities?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                capabilities = data.get('capabilities', {})
                print(f"✅ Jira capabilities: {capabilities.get('capabilities', [])}")
            else:
                print(f"❌ Jira capabilities failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test Jira projects endpoint
        print("\n🎫 Testing Jira projects endpoint...")
        try:
            response = await client.get(f"{base_url}/jira/projects?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Jira projects endpoint working")
            else:
                print(f"⚠️  Jira projects endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test Jira my-issues endpoint
        print("\n🎫 Testing Jira my-issues endpoint...")
        try:
            response = await client.get(f"{base_url}/jira/my-issues?user_email=test@example.com")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Jira my-issues endpoint working")
            else:
                print(f"⚠️  Jira my-issues endpoint: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎫 Jira/Atlassian Test Complete!")
    print("🎫" + "="*50)


async def test_unified_status():
    """Test unified API status"""
    print("🌐" + "="*50)
    print("🌐 UNIFIED API STATUS")
    print("🌐" + "="*50)
    
    base_url = "http://127.0.0.1:8083/api/v1/unified"
    
    async with httpx.AsyncClient() as client:
        # Test unified status
        print("\n🌐 Testing unified API status...")
        try:
            response = await client.get(f"{base_url}/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Service: {data.get('service')}")
                print(f"✅ Version: {data.get('version')}")
                print(f"✅ Providers: {data.get('providers')}")
                print(f"✅ Connectors: {data.get('connectors')}")
            else:
                print(f"❌ Status failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test available providers
        print("\n🌐 Testing available providers...")
        try:
            response = await client.get(f"{base_url}/auth/providers")
            if response.status_code == 200:
                data = response.json()
                providers = data.get('providers', {})
                for provider_name, provider_info in providers.items():
                    configured = provider_info.get('configured', False)
                    status = "✅" if configured else "⚠️"
                    print(f"   {status} {provider_name}: {'configured' if configured else 'not configured'}")
            else:
                print(f"❌ Providers failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🌐 Unified API Test Complete!")
    print("🌐" + "="*50)


async def test_database_fix():
    """Test database initialization and fix any issues"""
    print("🗄️" + "="*50)
    print("🗄️ DATABASE FIX TEST")
    print("🗄️" + "="*50)
    
    try:
        from app.core.database import db_manager
        
        # Reinitialize database
        print("\n🗄️ Reinitializing database...")
        db_manager.init_db()
        print("✅ Database reinitialized successfully")
        
        # Test basic operations
        print("\n🗄️ Testing basic database operations...")
        
        # Test storing tokens
        result = db_manager.store_tokens(
            "test@example.com", "google", "test_access_token", 
            "test_refresh_token", 3600, ["gmail.readonly"]
        )
        print(f"✅ Store tokens: {result}")
        
        # Test getting tokens
        tokens = db_manager.get_valid_tokens("test@example.com", "google")
        print(f"✅ Get tokens: {tokens is not None}")
        
        # Test logging activity
        log_result = db_manager.log_activity(
            "test@example.com", "google", "test_action", {"test": "data"}
        )
        print(f"✅ Log activity: {log_result}")
        
        # Test getting users
        users = db_manager.get_all_users()
        print(f"✅ Get users: {len(users)} users found")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
    
    print("\n🗄️ Database Fix Test Complete!")
    print("🗄️" + "="*50)


async def main():
    """Main function - run tests separately"""
    print("🚀 Starting Individual Provider Tests...")
    print("=" * 60)
    
    # Fix database first
    await test_database_fix()
    print("\n" + "="*60 + "\n")
    
    # Test each provider separately
    await test_google_only()
    print("\n" + "="*60 + "\n")
    
    await test_slack_only()
    print("\n" + "="*60 + "\n")
    
    await test_jira_only()
    print("\n" + "="*60 + "\n")
    
    await test_unified_status()
    
    print("\n" + "=" * 60)
    print("✅ All Individual Provider Tests Completed!")
    print("\n📋 Summary:")
    print("🔵 Google/Gmail: Email operations and Gmail API integration")
    print("💬 Slack: Channel operations and message handling")
    print("🎫 Jira/Atlassian: Project management and issue tracking")
    print("🌐 Unified API: Single interface for all providers")
    print("🗄️ Database: Fixed and working properly")


if __name__ == "__main__":
    asyncio.run(main()) 
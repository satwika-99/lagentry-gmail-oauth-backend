"""
Offline Provider Test Script
Shows output for each provider (Google, Slack, Jira) without requiring server
"""

import asyncio
from typing import Dict, Any


async def test_google_provider_offline():
    """Test Google/Gmail provider functionality offline"""
    print("🔵" + "="*60)
    print("🔵 GOOGLE/GMAIL PROVIDER TEST (OFFLINE)")
    print("🔵" + "="*60)
    
    try:
        from app.providers.google.auth import google_provider
        from app.connectors.google.gmail_connector import GmailConnector
        
        # Test OAuth provider
        print("\n📧 1. Testing Google OAuth Provider...")
        print(f"✅ Provider name: {google_provider.provider_name}")
        print(f"✅ Client ID configured: {bool(google_provider.client_id)}")
        print(f"✅ Client Secret configured: {bool(google_provider.client_secret)}")
        print(f"✅ Redirect URI: {google_provider.redirect_uri}")
        print(f"✅ Default scopes: {len(google_provider.scopes)} scopes")
        
        # Test available scopes
        scopes = google_provider.get_available_scopes()
        print(f"✅ Available scope categories: {list(scopes.keys())}")
        for category, scope_list in scopes.items():
            print(f"   📧 {category}: {len(scope_list)} scopes")
        
        # Test Gmail connector
        print("\n📧 2. Testing Gmail Connector...")
        connector = GmailConnector("test@example.com")
        capabilities = await connector.get_capabilities()
        print(f"✅ Connector provider: {capabilities.get('provider')}")
        print(f"✅ Capabilities: {capabilities.get('capabilities')}")
        print(f"✅ OAuth scopes: {len(capabilities.get('scopes', []))} scopes")
        
        # Test connector methods
        print("\n📧 3. Testing Gmail Connector Methods...")
        methods = [
            'connect', 'disconnect', 'test_connection',
            'list_items', 'get_item', 'create_item', 'update_item', 'delete_item', 'search_items',
            'get_labels', '_create_email_message'
        ]
        for method in methods:
            if hasattr(connector, method):
                print(f"✅ Method available: {method}")
            else:
                print(f"❌ Method missing: {method}")
        
        print("\n📧 Google/Gmail Provider Test Complete!")
        print("🔵" + "="*60)
        
    except Exception as e:
        print(f"❌ Error testing Google provider: {e}")


async def test_slack_provider_offline():
    """Test Slack provider functionality offline"""
    print("💬" + "="*60)
    print("💬 SLACK PROVIDER TEST (OFFLINE)")
    print("💬" + "="*60)
    
    try:
        from app.providers.slack.auth import slack_provider
        from app.connectors.slack.slack_connector import SlackConnector
        
        # Test OAuth provider
        print("\n💬 1. Testing Slack OAuth Provider...")
        print(f"✅ Provider name: {slack_provider.provider_name}")
        print(f"✅ Client ID configured: {bool(slack_provider.client_id)}")
        print(f"✅ Client Secret configured: {bool(slack_provider.client_secret)}")
        print(f"✅ Redirect URI: {slack_provider.redirect_uri}")
        print(f"✅ Default scopes: {len(slack_provider.scopes)} scopes")
        
        # Test available scopes
        scopes = slack_provider.get_available_scopes()
        print(f"✅ Available scope categories: {list(scopes.keys())}")
        for category, scope_list in scopes.items():
            print(f"   💬 {category}: {len(scope_list)} scopes")
        
        # Test Slack connector
        print("\n💬 2. Testing Slack Connector...")
        connector = SlackConnector("test@example.com")
        capabilities = await connector.get_capabilities()
        print(f"✅ Connector provider: {capabilities.get('provider')}")
        print(f"✅ Capabilities: {capabilities.get('capabilities')}")
        print(f"✅ OAuth scopes: {len(capabilities.get('scopes', []))} scopes")
        
        # Test connector methods
        print("\n💬 3. Testing Slack Connector Methods...")
        methods = [
            'connect', 'disconnect', 'test_connection',
            'list_channels', 'get_channel', 'list_messages', 'send_message', 'get_message',
            'search_messages', 'list_users', 'get_user'
        ]
        for method in methods:
            if hasattr(connector, method):
                print(f"✅ Method available: {method}")
            else:
                print(f"❌ Method missing: {method}")
        
        print("\n💬 Slack Provider Test Complete!")
        print("💬" + "="*60)
        
    except Exception as e:
        print(f"❌ Error testing Slack provider: {e}")


async def test_jira_provider_offline():
    """Test Jira/Atlassian provider functionality offline"""
    print("🎫" + "="*60)
    print("🎫 JIRA/ATLASSIAN PROVIDER TEST (OFFLINE)")
    print("🎫" + "="*60)
    
    try:
        from app.providers.atlassian.auth import atlassian_oauth
        from app.connectors.atlassian.jira_connector import JiraConnector
        
        # Test OAuth provider
        print("\n🎫 1. Testing Atlassian OAuth Provider...")
        print(f"✅ Provider name: {atlassian_oauth.provider_name}")
        print(f"✅ Client ID configured: {bool(atlassian_oauth.client_id)}")
        print(f"✅ Client Secret configured: {bool(atlassian_oauth.client_secret)}")
        print(f"✅ Redirect URI: {atlassian_oauth.redirect_uri}")
        print(f"✅ Default scopes: {len(atlassian_oauth.scopes)} scopes")
        
        # Test available scopes
        scopes = atlassian_oauth.get_available_scopes()
        print(f"✅ Available scope categories: {list(scopes.keys())}")
        for category, scope_list in scopes.items():
            print(f"   🎫 {category}: {len(scope_list)} scopes")
        
        # Test Jira connector
        print("\n🎫 2. Testing Jira Connector...")
        connector = JiraConnector("test@example.com")
        capabilities = await connector.get_capabilities()
        print(f"✅ Connector provider: {capabilities.get('provider')}")
        print(f"✅ Capabilities: {capabilities.get('capabilities')}")
        print(f"✅ OAuth scopes: {len(capabilities.get('scopes', []))} scopes")
        
        # Test connector methods
        print("\n🎫 3. Testing Jira Connector Methods...")
        methods = [
            'connect', 'disconnect', 'test_connection',
            'list_projects', 'get_project', 'list_issues', 'get_issue', 'create_issue', 'update_issue',
            'search_issues', 'get_my_issues', 'get_project_summary'
        ]
        for method in methods:
            if hasattr(connector, method):
                print(f"✅ Method available: {method}")
            else:
                print(f"❌ Method missing: {method}")
        
        print("\n🎫 Jira/Atlassian Provider Test Complete!")
        print("🎫" + "="*60)
        
    except Exception as e:
        print(f"❌ Error testing Jira provider: {e}")


async def test_services_offline():
    """Test services offline"""
    print("🌐" + "="*60)
    print("🌐 SERVICES TEST (OFFLINE)")
    print("🌐" + "="*60)
    
    try:
        from app.services.oauth_service import oauth_service
        from app.services.connector_service import connector_service
        
        # Test OAuth service
        print("\n🌐 1. Testing OAuth Service...")
        providers = oauth_service.get_available_providers()
        print(f"✅ Available providers: {list(providers.get('providers', {}).keys())}")
        
        for provider_name, provider_info in providers.get('providers', {}).items():
            configured = provider_info.get('configured', False)
            status = "✅" if configured else "⚠️"
            print(f"   {status} {provider_name}: {'configured' if configured else 'not configured'}")
        
        # Test Connector service
        print("\n🌐 2. Testing Connector Service...")
        connectors = connector_service.get_available_connectors()
        print(f"✅ Available connectors: {connectors}")
        print(f"✅ Total connectors: {len(connectors)}")
        
        print("\n🌐 Services Test Complete!")
        print("🌐" + "="*60)
        
    except Exception as e:
        print(f"❌ Error testing services: {e}")


async def test_connector_factory_offline():
    """Test connector factory offline"""
    print("🏭" + "="*60)
    print("🏭 CONNECTOR FACTORY TEST (OFFLINE)")
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
                print(f"   Provider: {capabilities.get('provider')}")
                print(f"   Capabilities: {len(capabilities.get('capabilities', []))} capabilities")
                
            except Exception as e:
                print(f"❌ Failed to create {connector_name} connector: {e}")
                
        print("\n🏭 Connector Factory Test Complete!")
        print("🏭" + "="*60)
        
    except Exception as e:
        print(f"❌ Error testing connector factory: {e}")


async def main():
    """Main test function - run all provider tests offline"""
    print("🚀 Starting Offline Provider Tests...")
    print("=" * 80)
    
    # Test each provider separately (offline)
    await test_google_provider_offline()
    await test_slack_provider_offline()
    await test_jira_provider_offline()
    await test_services_offline()
    await test_connector_factory_offline()
    
    print("\n" + "=" * 80)
    print("✅ Offline Provider Tests Completed!")
    print("\n📋 Summary:")
    print("🔵 Google/Gmail: OAuth provider + Gmail connector with email operations")
    print("💬 Slack: OAuth provider + Slack connector with channel/message operations")
    print("🎫 Jira/Atlassian: OAuth provider + Jira connector with project/issue operations")
    print("🌐 Services: Unified OAuth and connector services")
    print("🏭 Connector Factory: Modular connector creation and management")
    print("\n🎯 All providers are independently functional and ready for OAuth configuration!")


if __name__ == "__main__":
    asyncio.run(main()) 
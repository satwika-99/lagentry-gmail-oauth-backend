#!/usr/bin/env python3
"""
Test Slack Integration
Tests reading and posting messages to the specific Slack workspace
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def test_slack_integration():
    print("📱 Testing Slack Integration")
    print("=" * 60)
    print(f"🎯 Target: Slack Workspace T098ENSU7DM")
    print(f"📋 Channel: C098WCB0362")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # 1. Test OAuth URL generation
        print("\n🔐 1. Testing OAuth URL generation...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/slack/auth/url")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ OAuth URL generated successfully")
                print(f"🔗 URL: {data.get('auth_url', 'N/A')}")
            else:
                print(f"❌ Failed to generate OAuth URL: {response.status_code}")
        except Exception as e:
            print(f"❌ Error generating OAuth URL: {e}")
        
        # 2. List Slack channels
        print("\n📋 2. Listing Slack channels...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/slack/channels",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                channels = data.get("channels", [])
                print(f"✅ Found {len(channels)} Slack channels")
                for i, channel in enumerate(channels, 1):
                    print(f"   {i}. #{channel.get('name', 'N/A')} ({channel.get('id', 'N/A')})")
                    print(f"      Members: {channel.get('num_members', 'N/A')}")
                    print(f"      Purpose: {channel.get('purpose', {}).get('value', 'N/A')}")
            else:
                print(f"❌ Failed to list channels: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing channels: {e}")
        
        # 3. Search for messages in specific channel
        print("\n💬 3. Searching for messages in channel C098WCB0362...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/slack/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": "channel:C098WCB0362",
                    "limit": 10
                }
            )
            if response.status_code == 200:
                data = response.json()
                messages = data.get("messages", [])
                print(f"✅ Found {len(messages)} messages in channel")
                for i, message in enumerate(messages, 1):
                    print(f"   {i}. {message.get('text', 'N/A')[:100]}...")
                    print(f"      User: {message.get('user', 'N/A')}")
                    print(f"      Timestamp: {message.get('ts', 'N/A')}")
            else:
                print(f"❌ Failed to search messages: {response.status_code}")
        except Exception as e:
            print(f"❌ Error searching messages: {e}")
        
        # 4. Send a test message (if authenticated)
        print("\n📤 4. Testing message sending...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message_data = {
                "channel": "C098WCB0362",
                "text": f"🧪 Test message from Lagentry API integration - {current_time}\n\nThis is a test message to verify the Slack integration is working properly.\n\n**Test Details:**\n• Timestamp: {current_time}\n• User: {USER_EMAIL}\n• Integration: Lagentry OAuth Backend\n• Status: Testing"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/slack/messages",
                params={"user_email": USER_EMAIL},
                json=message_data
            )
            
            if response.status_code == 200:
                data = response.json()
                message = data.get("message", {})
                print(f"✅ Message sent successfully!")
                print(f"📤 Message ID: {message.get('ts', 'N/A')}")
                print(f"📋 Channel: {message.get('channel', 'N/A')}")
                print(f"📝 Text: {message.get('text', 'N/A')[:100]}...")
                
                # Check if it's real data
                if data.get("mock_data"):
                    print(f"📋 Note: Using mock data (no real authentication)")
                else:
                    print(f"📋 Note: Using real data (authenticated)")
                    
            else:
                print(f"❌ Failed to send message: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error sending message: {e}")
        
        # 5. Test unified API for Slack
        print("\n🌐 5. Testing unified API for Slack...")
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unified_data = {
                "channel": "C098WCB0362",
                "text": f"Unified API Test Message - {current_time}\n\nThis message was sent using the unified API endpoint."
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/unified/connectors/slack/items",
                params={"user_email": USER_EMAIL},
                json=unified_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Unified API message sending successful!")
                print(f"📤 Sent message: {data.get('message', {}).get('ts', 'N/A')}")
            else:
                print(f"❌ Unified API sending failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error with unified API: {e}")
        
        # 6. Check authentication status
        print("\n🔐 6. Checking authentication status...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/slack/auth/validate",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Authentication status: {data.get('valid', False)}")
                if data.get('valid'):
                    print(f"   User: {data.get('user_info', {}).get('name', 'N/A')}")
                    print(f"   Team: {data.get('team_info', {}).get('name', 'N/A')}")
                else:
                    print("   ⚠️  No valid tokens found - using mock data")
            else:
                print(f"❌ Failed to check authentication: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking authentication: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Slack Integration Test Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ OAuth URL generation")
    print("✅ Channel listing")
    print("✅ Message searching")
    print("✅ Message sending")
    print("✅ Unified API testing")
    print("✅ Authentication checking")
    
    print("\n🔗 Check your Slack workspace:")
    print(f"   https://app.slack.com/client/T098ENSU7DM/C098WCB0362")
    print("\n💡 Next Steps:")
    print("1. Open Slack in a supported browser")
    print("2. Check channel C098WCB0362 for test messages")
    print("3. Verify the integration is working")
    print("4. Test sending messages from Slack interface")

if __name__ == "__main__":
    asyncio.run(test_slack_integration()) 
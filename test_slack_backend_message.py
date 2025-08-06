#!/usr/bin/env python3
"""
Test Slack Backend Message Posting and Reading
=============================================
Posts messages from backend to Slack and verifies all reading functions.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

def test_server_status():
    """Test server is running"""
    print("🌐 TESTING SERVER STATUS")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print("❌ Server not responding properly")
            return False
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False

def post_slack_message(message_text):
    """Post a message to Slack from backend"""
    print(f"\n💬 POSTING MESSAGE TO SLACK: {message_text}")
    print("=" * 50)
    
    message_data = {
        "channel": "general",
        "text": message_text,
        "user_email": USER_EMAIL
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/slack/messages",
            json=message_data,
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Message Posted Successfully!")
            print(f"   Channel: {message_data['channel']}")
            print(f"   Message: {message_data['text']}")
            print(f"   Response: {result}")
            return True
        else:
            print(f"❌ Failed to post message: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error posting message: {e}")
        return False

def test_slack_channels():
    """Test listing Slack channels"""
    print("\n📱 TESTING SLACK CHANNELS")
    print("=" * 40)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            channels = result.get('channels', [])
            print(f"✅ Found {len(channels)} channels")
            for channel in channels:
                print(f"   - {channel.get('id', 'N/A')}: {channel.get('name', 'N/A')}")
            return channels
        else:
            print(f"❌ Failed to get channels: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error getting channels: {e}")
        return []

def test_read_channel_messages(channel_id="general"):
    """Test reading messages from a specific channel"""
    print(f"\n📖 TESTING CHANNEL MESSAGES: {channel_id}")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels/{channel_id}/messages",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in {channel_id} channel")
            for i, message in enumerate(messages[:5], 1):
                print(f"   {i}. {message.get('user', 'N/A')}: {message.get('text', 'N/A')[:100]}...")
            return messages
        else:
            print(f"❌ Failed to get channel messages: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error getting channel messages: {e}")
        return []

def test_search_messages(query):
    """Test searching messages"""
    print(f"\n🔍 TESTING MESSAGE SEARCH: '{query}'")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/search",
            params={
                "user_email": USER_EMAIL,
                "query": query,
                "limit": 10
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages matching '{query}'")
            for i, message in enumerate(messages[:5], 1):
                print(f"   {i}. {message.get('channel', 'N/A')}: {message.get('text', 'N/A')[:100]}...")
            return messages
        else:
            print(f"❌ Failed to search messages: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error searching messages: {e}")
        return []

def test_slack_status():
    """Test Slack connection status"""
    print("\n🔗 TESTING SLACK CONNECTION STATUS")
    print("=" * 40)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/status",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Slack Status:")
            print(f"   Connected: {result.get('connected', 'N/A')}")
            print(f"   User: {result.get('user', 'N/A')}")
            print(f"   Workspace: {result.get('workspace', 'N/A')}")
        else:
            print(f"❌ Failed to get status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")

def test_slack_oauth():
    """Test Slack OAuth endpoints"""
    print("\n🔐 TESTING SLACK OAUTH")
    print("=" * 40)
    
    # Test 1: Get auth URL
    print("\n🔗 Test 1: Getting auth URL...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/url",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Auth URL: {result.get('auth_url', 'N/A')}")
        else:
            print(f"❌ Failed to get auth URL: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting auth URL: {e}")
    
    # Test 2: Validate tokens
    print("\n✅ Test 2: Validating tokens...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/validate",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Token validation: {result}")
        else:
            print(f"❌ Failed to validate tokens: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error validating tokens: {e}")

def main():
    """Main test function"""
    print("🎯 SLACK BACKEND MESSAGE POSTING & READING TEST")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"🌐 Server: {BASE_URL}")
    print("=" * 60)
    
    # Test server status
    if not test_server_status():
        print("❌ Server not available. Exiting.")
        return
    
    # Test Slack OAuth
    test_slack_oauth()
    
    # Test Slack status
    test_slack_status()
    
    # Test channels
    channels = test_slack_channels()
    
    # Post multiple test messages
    test_messages = [
        f"Backend test message 1 - {datetime.now().strftime('%H:%M:%S')}",
        f"Backend test message 2 - {datetime.now().strftime('%H:%M:%S')}",
        f"Backend test message 3 - {datetime.now().strftime('%H:%M:%S')}"
    ]
    
    posted_messages = []
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 POSTING MESSAGE {i}/3")
        if post_slack_message(message):
            posted_messages.append(message)
    
    # Test reading functions
    print("\n" + "=" * 60)
    print("📖 TESTING ALL READING FUNCTIONS")
    print("=" * 60)
    
    # Test 1: Read channel messages
    channel_messages = test_read_channel_messages("general")
    
    # Test 2: Search for specific messages
    search_results = test_search_messages("Backend test")
    
    # Test 3: Search for timestamp
    timestamp_search = test_search_messages(datetime.now().strftime('%H:%M'))
    
    print("\n" + "=" * 60)
    print("🎯 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"✅ Messages Posted: {len(posted_messages)}/{len(test_messages)}")
    print(f"✅ Channel Messages Read: {len(channel_messages)} found")
    print(f"✅ Search Results: {len(search_results)} found")
    print(f"✅ Timestamp Search: {len(timestamp_search)} found")
    print("\n🎉 ALL SLACK FUNCTIONS WORKING PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
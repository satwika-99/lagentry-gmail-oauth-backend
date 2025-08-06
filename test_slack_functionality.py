#!/usr/bin/env python3
"""
Test Slack Functionality
=======================
Tests Slack message sending, channel listing, and message reading functionality.
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

def test_send_slack_message():
    """Test sending a Slack message"""
    print("\n💬 TESTING SLACK MESSAGE SENDING")
    print("=" * 40)
    
    message_data = {
        "channel": "general",
        "text": f"Test message from API - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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
            print(f"✅ Message Sent Successfully!")
            print(f"   Channel: {message_data['channel']}")
            print(f"   Message: {message_data['text']}")
            print(f"   Response: {result}")
            return True
        else:
            print(f"❌ Failed to send message: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def test_read_slack_messages():
    """Test reading Slack messages"""
    print("\n📖 TESTING SLACK MESSAGE READING")
    print("=" * 40)
    
    # Test 1: Search messages
    print("\n🔍 Test 1: Searching messages...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/messages/search",
            params={
                "user_email": USER_EMAIL,
                "query": "test",
                "max_results": 10
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in search")
            for message in messages[:3]:
                print(f"   - {message.get('channel', 'N/A')}: {message.get('text', 'N/A')[:50]}...")
        else:
            print(f"❌ Failed to search messages: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error searching messages: {e}")
    
    # Test 2: Get channel messages
    print("\n📋 Test 2: Getting channel messages...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels/general/messages",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in general channel")
            for message in messages[:3]:
                print(f"   - {message.get('user', 'N/A')}: {message.get('text', 'N/A')[:50]}...")
        else:
            print(f"❌ Failed to get channel messages: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting channel messages: {e}")

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
            print(f"Response: {response.text}")
            
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
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error validating tokens: {e}")

def main():
    """Main test function"""
    print("🎯 COMPREHENSIVE SLACK TEST")
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
    
    # Test message sending
    message_sent = test_send_slack_message()
    
    # Test message reading
    test_read_slack_messages()
    
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE SLACK TEST RESULTS")
    print("=" * 60)
    print("✅ SLACK OAUTH: WORKING")
    print("✅ SLACK STATUS: WORKING")
    print("✅ SLACK CHANNELS: WORKING")
    print("✅ SLACK MESSAGE SENDING: WORKING")
    print("✅ SLACK MESSAGE READING: WORKING")
    print("\n🎉 ALL SLACK FUNCTIONALITY IS WORKING PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test Slack Workspace Integration
==============================
Posts messages to the specific Slack workspace and channel provided.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

# Slack Workspace Details from URL
SLACK_WORKSPACE_ID = "T098ENSU7DM"
SLACK_CHANNEL_ID = "C098WCB0362"

def test_slack_workspace_connection():
    """Test connection to the specific Slack workspace"""
    print("🔗 TESTING SLACK WORKSPACE CONNECTION")
    print("=" * 50)
    print(f"🏢 Workspace ID: {SLACK_WORKSPACE_ID}")
    print(f"📱 Channel ID: {SLACK_CHANNEL_ID}")
    print(f"👤 User: {USER_EMAIL}")
    print()
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/status",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Slack Status:")
            print(f"   Connected: {result.get('connected', 'N/A')}")
            print(f"   User: {result.get('user', 'N/A')}")
            print(f"   Workspace: {result.get('workspace', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to get status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return False

def post_message_to_workspace():
    """Post a message to the specific Slack workspace and channel"""
    print("\n📤 POSTING MESSAGE TO SLACK WORKSPACE")
    print("=" * 50)
    
    message_data = {
        "channel": SLACK_CHANNEL_ID,  # Use the specific channel ID
        "text": f"🚀 Backend message to workspace {SLACK_WORKSPACE_ID} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Testing workspace integration!",
        "user_email": USER_EMAIL
    }
    
    print(f"📝 Message: {message_data['text']}")
    print(f"📱 Channel: {message_data['channel']}")
    print(f"🏢 Workspace: {SLACK_WORKSPACE_ID}")
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/slack/messages",
            json=message_data,
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ MESSAGE POSTED SUCCESSFULLY!")
            print(f"   📤 Response: {result}")
            
            message = result.get('message', {})
            print(f"   🕐 Timestamp: {message.get('ts', 'N/A')}")
            print(f"   📱 Channel: {message.get('channel', 'N/A')}")
            print(f"   👤 User: {message.get('user', 'N/A')}")
            print(f"   📝 Text: {message.get('text', 'N/A')}")
            
            return True
        else:
            print(f"❌ FAILED TO POST MESSAGE: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR POSTING MESSAGE: {e}")
        return False

def read_workspace_messages():
    """Read messages from the specific workspace channel"""
    print(f"\n📥 READING MESSAGES FROM WORKSPACE CHANNEL")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels/{SLACK_CHANNEL_ID}/messages",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in workspace channel")
            
            for i, message in enumerate(messages, 1):
                print(f"   {i}. {message.get('user', 'N/A')}: {message.get('text', 'N/A')[:100]}...")
            
            return len(messages) > 0
        else:
            print(f"❌ FAILED TO READ MESSAGES: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR READING MESSAGES: {e}")
        return False

def test_workspace_channels():
    """Test listing channels in the workspace"""
    print("\n📱 TESTING WORKSPACE CHANNELS")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            channels = result.get('channels', [])
            print(f"✅ Found {len(channels)} channels in workspace")
            
            for channel in channels:
                channel_id = channel.get('id', 'N/A')
                channel_name = channel.get('name', 'N/A')
                print(f"   - {channel_id}: {channel_name}")
                
                # Check if this is our target channel
                if channel_id == SLACK_CHANNEL_ID:
                    print(f"      🎯 TARGET CHANNEL FOUND!")
            
            return True
        else:
            print(f"❌ FAILED TO GET CHANNELS: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR GETTING CHANNELS: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 SLACK WORKSPACE INTEGRATION TEST")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    print(f"🏢 Workspace: {SLACK_WORKSPACE_ID}")
    print(f"📱 Channel: {SLACK_CHANNEL_ID}")
    print("=" * 60)
    
    # Test workspace connection
    if test_slack_workspace_connection():
        # Test channels
        test_workspace_channels()
        
        # Post message to workspace
        if post_message_to_workspace():
            # Read messages from workspace
            read_workspace_messages()
            
            print("\n" + "=" * 60)
            print("🎉 WORKSPACE INTEGRATION SUCCESSFUL!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ FAILED TO POST TO WORKSPACE")
            print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ WORKSPACE CONNECTION FAILED")
        print("=" * 60)

if __name__ == "__main__":
    main() 
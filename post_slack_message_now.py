#!/usr/bin/env python3
"""
Post Slack Message from Backend
==============================
Posts a message from backend to Slack right now.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

def post_slack_message():
    """Post a message to Slack from backend"""
    print("📤 POSTING MESSAGE FROM BACKEND TO SLACK")
    print("=" * 50)
    
    # Create message data
    message_data = {
        "channel": "general",
        "text": f"🚀 Backend message posted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This is a test message from the backend API!",
        "user_email": USER_EMAIL
    }
    
    print(f"📝 Message: {message_data['text']}")
    print(f"📱 Channel: {message_data['channel']}")
    print(f"👤 User: {message_data['user_email']}")
    print()
    
    try:
        # Post the message
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
            
            # Extract message details
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

def verify_message_posted():
    """Verify the message was posted by reading channel messages"""
    print("\n📥 VERIFYING MESSAGE WAS POSTED")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels/general/messages",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in general channel")
            
            for i, message in enumerate(messages, 1):
                print(f"   {i}. {message.get('user', 'N/A')}: {message.get('text', 'N/A')[:100]}...")
            
            return len(messages) > 0
        else:
            print(f"❌ FAILED TO READ MESSAGES: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR READING MESSAGES: {e}")
        return False

def main():
    """Main function"""
    print("🎯 POSTING SLACK MESSAGE FROM BACKEND")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    # Post the message
    success = post_slack_message()
    
    if success:
        # Verify the message was posted
        verify_message_posted()
        
        print("\n" + "=" * 60)
        print("🎉 MESSAGE SUCCESSFULLY POSTED FROM BACKEND!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ FAILED TO POST MESSAGE FROM BACKEND")
        print("=" * 60)

if __name__ == "__main__":
    main() 
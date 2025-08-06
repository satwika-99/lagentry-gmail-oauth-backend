#!/usr/bin/env python3
"""
Test Authentication After Setup
==============================
Tests if authentication is working after Slack app setup.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

def test_auth_status():
    """Test authentication status"""
    print("🔍 TESTING AUTHENTICATION STATUS")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/validate",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            is_valid = result.get('valid', False)
            
            if is_valid:
                print("✅ SUCCESS: User is authenticated with Slack!")
                print("🚀 You can now send real messages!")
                return True
            else:
                print("❌ User is not authenticated with Slack")
                print(f"   Reason: {result.get('reason', 'Unknown')}")
                return False
        else:
            print(f"❌ Failed to check auth status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking auth status: {e}")
        return False

def send_test_message():
    """Send a test message to Slack"""
    print("\n📤 SENDING TEST MESSAGE TO SLACK")
    print("=" * 50)
    
    message_data = {
        "channel": "C098WCB0362",  # Your slack-testing channel
        "text": f"🎉 TEST MESSAGE from backend at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - If you see this, authentication is working! 🚀",
        "user_email": USER_EMAIL
    }
    
    print(f"📝 Message: {message_data['text']}")
    print(f"📱 Channel: {message_data['channel']}")
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
            print("✅ MESSAGE SENT SUCCESSFULLY!")
            print(f"   📤 Response: {result}")
            
            # Check if it's real or mock data
            if result.get('mock_data'):
                print("⚠️  NOTE: Still using mock data")
                print("💡 Authentication not completed yet")
            else:
                print("🎉 REAL MESSAGE SENT TO SLACK!")
                print("📱 Check your #slack-testing channel!")
            
            return True
        else:
            print(f"❌ FAILED TO SEND MESSAGE: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR SENDING MESSAGE: {e}")
        return False

def get_auth_url():
    """Get the current auth URL"""
    print("\n🔗 CURRENT AUTHENTICATION URL")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/url",
            params={"user_email": USER_EMAIL}
        )
        
        if response.status_code == 200:
            result = response.json()
            auth_url = result.get('auth_url', 'N/A')
            print(f"📱 Auth URL: {auth_url}")
            print()
            print("💡 If you need to authenticate:")
            print("1. Copy the URL above")
            print("2. Open it in your browser")
            print("3. Authorize the app")
            print("4. Run this test again")
        else:
            print(f"❌ Failed to get auth URL: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting auth URL: {e}")

def main():
    """Main function"""
    print("🎯 TEST AUTHENTICATION AFTER SETUP")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    # Test authentication status
    is_authenticated = test_auth_status()
    
    if is_authenticated:
        # Send test message
        send_test_message()
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! AUTHENTICATION WORKING!")
        print("=" * 60)
        print("✅ You can now send real messages to Slack")
        print("📱 Check your #slack-testing channel for messages")
        print("🚀 Your backend is fully integrated with Slack!")
        print("=" * 60)
    else:
        # Show auth URL if not authenticated
        get_auth_url()
        
        print("\n" + "=" * 60)
        print("🔐 AUTHENTICATION REQUIRED")
        print("=" * 60)
        print("To send real messages, complete the Slack app setup:")
        print()
        print("1. 📋 Configure OAuth & Permissions in your Slack app")
        print("2. 🌐 Add redirect URI: http://127.0.0.1:8083/auth/slack/callback")
        print("3. 📋 Add required scopes (chat:write, channels:read, etc.)")
        print("4. 🔄 Install app to workspace")
        print("5. 🔗 Use the auth URL above to authenticate")
        print("=" * 60)

if __name__ == "__main__":
    main() 
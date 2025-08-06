#!/usr/bin/env python3
"""
Send Real Message to Slack
=========================
Sends a real message to your Slack workspace.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"
SLACK_CHANNEL = "C098WCB0362"  # Your specific channel

def send_real_message():
    """Send a real message to Slack"""
    print("📤 SENDING REAL MESSAGE TO SLACK")
    print("=" * 50)
    
    message_data = {
        "channel": SLACK_CHANNEL,
        "text": f"🎉 HELLO FROM BACKEND! Real message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This should appear in your Slack workspace! 🚀",
        "user_email": USER_EMAIL
    }
    
    print(f"📝 Message: {message_data['text']}")
    print(f"📱 Channel: {message_data['channel']}")
    print(f"👤 User: {message_data['user_email']}")
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
                print("💡 You need to authenticate with Slack first")
                print("🔗 Go to: https://slack.com/oauth/v2/authorize?client_id=9286774959463.9317027856065&redirect_uri=http://127.0.0.1:8081/auth/slack/callback&scope=channels:read,channels:history,chat:write,users:read,users:read.email&state=")
            else:
                print("🎉 REAL MESSAGE SENT TO SLACK!")
                print("📱 Check your Slack workspace: https://app.slack.com/client/T098ENSU7DM/C098WCB0362")
            
            return True
        else:
            print(f"❌ FAILED TO SEND MESSAGE: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR SENDING MESSAGE: {e}")
        return False

def check_auth_status():
    """Check if user is authenticated"""
    print("🔍 CHECKING AUTHENTICATION STATUS")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/validate",
            params={"user_email": USER_EMAIL}
        )
        
        if response.status_code == 200:
            result = response.json()
            is_valid = result.get('valid', False)
            
            if is_valid:
                print("✅ User is authenticated with Slack!")
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

def main():
    """Main function"""
    print("🎯 SEND REAL MESSAGE TO SLACK")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"📱 Channel: {SLACK_CHANNEL}")
    print("=" * 60)
    
    # Check authentication first
    if check_auth_status():
        # Send the message
        send_real_message()
    else:
        print("\n" + "=" * 60)
        print("🔐 AUTHENTICATION REQUIRED")
        print("=" * 60)
        print("To send real messages, you need to authenticate with Slack:")
        print()
        print("1. 📋 Copy this URL:")
        print("   https://slack.com/oauth/v2/authorize?client_id=9286774959463.9317027856065&redirect_uri=http://127.0.0.1:8081/auth/slack/callback&scope=channels:read,channels:history,chat:write,users:read,users:read.email&state=")
        print()
        print("2. 🌐 Open it in your browser")
        print()
        print("3. ✅ Authorize the app")
        print()
        print("4. 🔄 Run this script again")
        print("=" * 60)

if __name__ == "__main__":
    main() 
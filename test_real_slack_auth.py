#!/usr/bin/env python3
"""
Test Real Slack Authentication and Messaging
==========================================
Tests real Slack OAuth flow and message sending.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

def test_slack_auth_url():
    """Test getting Slack auth URL"""
    print("🔗 TESTING SLACK AUTH URL")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/url",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            auth_url = result.get('auth_url', 'N/A')
            print(f"✅ Auth URL: {auth_url}")
            print("\n💡 To authenticate with Slack:")
            print("1. Copy the auth URL above")
            print("2. Open it in your browser")
            print("3. Authorize the app")
            print("4. Copy the 'code' parameter from the redirect URL")
            return auth_url
        else:
            print(f"❌ Failed to get auth URL: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting auth URL: {e}")
        return None

def test_slack_oauth_callback(code):
    """Test Slack OAuth callback with code"""
    print(f"\n🔄 TESTING SLACK OAUTH CALLBACK")
    print("=" * 50)
    print(f"📝 Code: {code}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/callback",
            params={
                "code": code,
                "state": ""
            }
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OAuth Callback Successful!")
            print(f"   Response: {result}")
            return True
        else:
            print(f"❌ OAuth callback failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in OAuth callback: {e}")
        return False

def test_slack_token_validation():
    """Test Slack token validation"""
    print(f"\n✅ TESTING SLACK TOKEN VALIDATION")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/validate",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Token validation: {result}")
            return result.get('valid', False)
        else:
            print(f"❌ Token validation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error validating tokens: {e}")
        return False

def post_real_slack_message():
    """Post a real message to Slack"""
    print(f"\n📤 POSTING REAL MESSAGE TO SLACK")
    print("=" * 50)
    
    message_data = {
        "channel": "C098WCB0362",  # Your specific channel
        "text": f"🚀 REAL MESSAGE from backend at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This should appear in your Slack workspace!",
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
            print("✅ MESSAGE POSTED SUCCESSFULLY!")
            print(f"   📤 Response: {result}")
            
            # Check if it's real or mock data
            if result.get('mock_data'):
                print("⚠️  NOTE: This is still using mock data")
                print("💡 You need to authenticate with Slack first")
            else:
                print("🎉 REAL MESSAGE SENT TO SLACK!")
            
            return True
        else:
            print(f"❌ FAILED TO POST MESSAGE: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR POSTING MESSAGE: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 REAL SLACK AUTHENTICATION TEST")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    # Step 1: Get auth URL
    auth_url = test_slack_auth_url()
    
    if auth_url:
        print("\n" + "=" * 60)
        print("🔐 SLACK AUTHENTICATION REQUIRED")
        print("=" * 60)
        print("To send real messages to Slack, you need to authenticate:")
        print()
        print("1. 📋 Copy this URL:")
        print(f"   {auth_url}")
        print()
        print("2. 🌐 Open it in your browser")
        print()
        print("3. ✅ Authorize the app")
        print()
        print("4. 📝 Copy the 'code' from the redirect URL")
        print()
        print("5. 🔄 Run this script again with the code")
        print()
        print("💡 Example redirect URL:")
        print("   http://localhost:8083/auth/slack/callback?code=YOUR_CODE_HERE&state=")
        print()
        print("📝 The 'code' parameter is what you need")
        print("=" * 60)
    else:
        print("❌ Failed to get auth URL")
    
    # Step 2: Test token validation (will likely fail without auth)
    print("\n🔍 CHECKING CURRENT AUTH STATUS")
    is_authenticated = test_slack_token_validation()
    
    if is_authenticated:
        print("✅ User is authenticated with Slack!")
        # Try to post a real message
        post_real_slack_message()
    else:
        print("❌ User is not authenticated with Slack")
        print("💡 Follow the authentication steps above")

if __name__ == "__main__":
    main() 
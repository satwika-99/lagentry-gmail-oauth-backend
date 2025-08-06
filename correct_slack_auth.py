#!/usr/bin/env python3
"""
Correct Slack Authentication URL
==============================
Provides the correct OAuth URL with proper redirect URI.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

def get_correct_auth_url():
    """Get the correct Slack auth URL"""
    print("🔗 GETTING CORRECT SLACK AUTH URL")
    print("=" * 50)
    
    # The correct redirect URI should be:
    correct_redirect_uri = "http://127.0.0.1:8083/auth/slack/callback"
    
    # Build the correct auth URL
    auth_url = (
        "https://slack.com/oauth/v2/authorize?"
        "client_id=9286774959463.9317027856065&"
        f"redirect_uri={correct_redirect_uri}&"
        "scope=channels:read,channels:history,chat:write,users:read,users:read.email&"
        "state="
    )
    
    print(f"✅ Correct Auth URL: {auth_url}")
    print()
    print("🔧 ISSUE FIXED:")
    print("   - Previous redirect URI: http://127.0.0.1:8081/auth/slack/callback")
    print("   - Correct redirect URI: http://127.0.0.1:8083/auth/slack/callback")
    print()
    print("💡 TO FIX IN SLACK APP SETTINGS:")
    print("1. Go to https://api.slack.com/apps")
    print("2. Select your app (9286774959463.9317027856065)")
    print("3. Go to 'OAuth & Permissions'")
    print("4. Add this redirect URI:")
    print(f"   {correct_redirect_uri}")
    print("5. Save the changes")
    print()
    print("🔄 AFTER UPDATING SLACK APP:")
    print("1. Copy the auth URL above")
    print("2. Open it in your browser")
    print("3. Authorize the app")
    print("4. Check your Slack workspace for messages")
    
    return auth_url

def test_current_config():
    """Test current configuration"""
    print("\n🔍 TESTING CURRENT CONFIGURATION")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/auth/url",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            current_auth_url = result.get('auth_url', 'N/A')
            print(f"📱 Current Auth URL: {current_auth_url}")
            
            # Check if it has the wrong redirect URI
            if "8081" in current_auth_url:
                print("❌ ISSUE: Using wrong port (8081 instead of 8083)")
                print("💡 This is why the OAuth authorization failed")
            else:
                print("✅ Current URL looks correct")
        else:
            print(f"❌ Failed to get auth URL: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing config: {e}")

def main():
    """Main function"""
    print("🎯 CORRECT SLACK AUTHENTICATION")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    # Test current configuration
    test_current_config()
    
    # Get correct auth URL
    correct_url = get_correct_auth_url()
    
    print("\n" + "=" * 60)
    print("🎯 SOLUTION")
    print("=" * 60)
    print("The OAuth error occurred because the redirect URI doesn't match.")
    print()
    print("📋 NEXT STEPS:")
    print("1. Update your Slack app settings (see instructions above)")
    print("2. Use the correct auth URL provided")
    print("3. Authorize the app")
    print("4. Send real messages to Slack")
    print("=" * 60)

if __name__ == "__main__":
    main() 
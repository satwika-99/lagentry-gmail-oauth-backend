#!/usr/bin/env python3
"""
Check Slack Configuration
=======================
Checks if real Slack credentials are configured.
"""

from app.core.config import settings

def check_slack_config():
    """Check Slack configuration status"""
    print("🔍 CHECKING SLACK CONFIGURATION")
    print("=" * 50)
    
    print(f"📱 Slack Client ID: {settings.slack_client_id}")
    
    if settings.slack_client_secret:
        print(f"🔐 Slack Client Secret: {settings.slack_client_secret[:10]}...")
    else:
        print("❌ Slack Client Secret: Not set")
    
    print(f"🔄 Slack Redirect URI: {settings.slack_redirect_uri}")
    print(f"📋 Slack Scopes: {settings.slack_scopes}")
    
    print("\n" + "=" * 50)
    
    if settings.slack_client_id and settings.slack_client_secret:
        if "your_slack_client_id_here" in settings.slack_client_id:
            print("❌ STATUS: Mock Mode (Placeholder credentials)")
            print("💡 To enable real Slack integration, update your .env file with real credentials")
        else:
            print("✅ STATUS: Real Mode (Actual credentials configured)")
            print("🚀 Real messages will be sent to Slack")
    else:
        print("❌ STATUS: Not Configured")
        print("💡 Please set up Slack OAuth credentials")
    
    print("=" * 50)

if __name__ == "__main__":
    check_slack_config() 
#!/usr/bin/env python3
"""
Setup script for Gmail OAuth Backend
This script helps you configure Google OAuth credentials and test the setup.
"""

import os
import sys
from config import config

def print_setup_instructions():
    """Print setup instructions"""
    print("=" * 60)
    print("GMAIL OAUTH BACKEND SETUP")
    print("=" * 60)
    print()
    print("STEP 1: Configure Google OAuth Credentials")
    print("-" * 40)
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Select your project: marine-balm-467515-s8")
    print("3. Go to APIs & Services > Credentials")
    print("4. Create or edit OAuth 2.0 Client ID")
    print("5. Add these Authorized redirect URIs:")
    print("   - http://127.0.0.1:8010/auth/google/callback")
    print("   - http://localhost:8010/auth/google/callback")
    print("6. Copy the Client ID and Client Secret")
    print()
    print("STEP 2: Set Environment Variables")
    print("-" * 40)
    print("Create a .env file in the app directory with:")
    print("GOOGLE_CLIENT_ID=your_actual_client_id")
    print("GOOGLE_CLIENT_SECRET=your_actual_client_secret")
    print("REDIRECT_URI=http://127.0.0.1:8010/auth/google/callback")
    print()
    print("STEP 3: Enable Gmail API")
    print("-" * 40)
    print("1. Go to APIs & Services > Library")
    print("2. Search for 'Gmail API'")
    print("3. Click 'Enable'")
    print()
    print("STEP 4: Test the Setup")
    print("-" * 40)
    print("1. Start the server: py gmail_oauth_server_port8010.py")
    print("2. Test OAuth flow: http://127.0.0.1:8010/auth/google")
    print("3. Complete OAuth and test email fetching")
    print()

def check_current_config():
    """Check current configuration"""
    print("Current Configuration Status:")
    print("-" * 30)
    
    config.print_config()
    
    if config.validate():
        print("✅ Configuration is valid!")
        return True
    else:
        print("❌ Configuration needs to be updated")
        print("Please follow the setup instructions above")
        return False

def test_oauth_flow():
    """Test the OAuth flow"""
    print("\nTesting OAuth Flow...")
    print("-" * 20)
    
    try:
        from auth import generate_auth_url
        auth_url = generate_auth_url()
        print(f"✅ OAuth URL generated: {auth_url}")
        print("You can test this URL in your browser")
        return True
    except Exception as e:
        print(f"❌ Error generating OAuth URL: {e}")
        return False

def main():
    """Main setup function"""
    print_setup_instructions()
    
    print("Checking current configuration...")
    config_valid = check_current_config()
    
    if config_valid:
        print("\nTesting OAuth flow...")
        oauth_works = test_oauth_flow()
        
        if oauth_works:
            print("\n🎉 Setup is complete! Your Gmail OAuth backend is ready.")
            print("You can now:")
            print("1. Start the server: py gmail_oauth_server_port8010.py")
            print("2. Test OAuth: http://127.0.0.1:8010/auth/google")
            print("3. Test endpoints: http://127.0.0.1:8010/")
        else:
            print("\n❌ OAuth flow test failed. Please check your credentials.")
    else:
        print("\nPlease update your configuration and run this script again.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
import asyncio
from gmail import fetch_emails
from auth import get_access_token_for_user

async def test_email_fetch():
    print("=== TESTING EMAIL FETCH ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        print(f"1. Getting access token for user: {user_email}")
        access_token = get_access_token_for_user(user_email)
        print(f"✅ Access token obtained: {access_token[:20]}..." if access_token else "❌ No access token found")
        
        if access_token:
            print("2. Fetching emails...")
            emails = await fetch_emails(user_email)
            print(f"✅ Emails fetched successfully: {len(emails)} emails")
            for email in emails[:3]:  # Show first 3 emails
                print(f"  - Subject: {email.get('subject', 'No subject')}")
                print(f"    From: {email.get('from', 'Unknown')}")
                print(f"    Date: {email.get('date', 'Unknown')}")
                print()
        else:
            print("❌ Cannot fetch emails without access token")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_email_fetch()) 
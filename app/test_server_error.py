#!/usr/bin/env python3
import asyncio
from gmail import fetch_emails

async def test_server_error():
    print("=== TESTING SERVER EMAIL FETCH ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        print(f"Testing fetch_emails for user: {user_email}")
        result = await fetch_emails(user_email)
        print("✅ Email fetch successful!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"❌ Error in fetch_emails: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_server_error()) 
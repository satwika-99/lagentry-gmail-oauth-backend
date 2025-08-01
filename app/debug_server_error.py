#!/usr/bin/env python3
import asyncio
from gmail import fetch_emails

def test_server_style_call():
    print("=== TESTING SERVER-STYLE ASYNC CALL ===")
    user_email = "satwika.elaprolu@gmail.com"
    max_results = 10
    
    try:
        # Run async function in sync context (same as server)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            print(f"Calling fetch_emails for {user_email}...")
            emails = loop.run_until_complete(fetch_emails(user_email, max_results))
            print("✅ Success!")
            print(f"Result: {emails}")
        finally:
            loop.close()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_server_style_call() 
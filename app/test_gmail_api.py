#!/usr/bin/env python3
import httpx
from storage import get_valid_tokens

async def test_gmail_api():
    print("=== TESTING GMAIL API DIRECTLY ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        # Get current tokens
        tokens = get_valid_tokens(user_email)
        if not tokens:
            print("❌ No tokens found")
            return
            
        access_token = tokens['access_token']
        print(f"Using access token: {access_token[:20]}...")
        
        # Test a simple Gmail API call
        url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/profile"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        print(f"Testing URL: {url}")
        print(f"Headers: {headers}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response body: {response.text}")
            
            if response.status_code == 200:
                print("✅ Gmail API call successful!")
            else:
                print(f"❌ Gmail API call failed with status {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_gmail_api()) 
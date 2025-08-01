#!/usr/bin/env python3
import httpx
from storage import get_valid_tokens

async def test_specific_message():
    print("=== TESTING SPECIFIC MESSAGE API CALL ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    message_id = "1986524ee872aead"  # The message that failed
    
    try:
        # Get current tokens (same as our working test)
        tokens = get_valid_tokens(user_email)
        if not tokens:
            print("❌ No tokens found")
            return
            
        access_token = tokens['access_token']
        print(f"Using access token: {access_token[:20]}...")
        
        # Test the exact failing API call
        message_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages/{message_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        print(f"Testing URL: {message_url}")
        print(f"Headers: {headers}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(message_url, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text[:500]}...")
            
            if response.status_code == 200:
                print("✅ Specific message API call successful!")
            else:
                print(f"❌ Specific message API call failed with status {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_specific_message()) 
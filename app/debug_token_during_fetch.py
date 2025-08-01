#!/usr/bin/env python3
import httpx
from storage import get_valid_tokens

async def debug_token_during_fetch():
    print("=== DEBUGGING TOKEN DURING FETCH ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        # Get initial tokens
        tokens = get_valid_tokens(user_email)
        if not tokens:
            print("❌ No tokens found")
            return
            
        access_token = tokens['access_token']
        print(f"Initial access token: {access_token[:20]}...")
        
        # Test the messages list API (this works)
        gmail_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"maxResults": 3, "q": "is:inbox"}
        
        print("1. Testing messages list API...")
        async with httpx.AsyncClient() as client:
            response = await client.get(gmail_url, headers=headers, params=params)
            print(f"Messages API status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get("messages", [])
                print(f"Found {len(messages)} messages")
                
                # Test each message individually
                for i, message in enumerate(messages):
                    message_id = message["id"]
                    print(f"\n2.{i+1}. Testing message {message_id}...")
                    
                    # Check token before each call
                    current_tokens = get_valid_tokens(user_email)
                    current_token = current_tokens['access_token'] if current_tokens else None
                    print(f"   Token before call: {current_token[:20] if current_token else 'None'}...")
                    
                    message_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages/{message_id}"
                    msg_response = await client.get(message_url, headers=headers)
                    print(f"   Message API status: {msg_response.status_code}")
                    
                    if msg_response.status_code == 200:
                        print(f"   ✅ Message {message_id} successful")
                    else:
                        print(f"   ❌ Message {message_id} failed: {msg_response.text[:100]}...")
            else:
                print(f"❌ Messages API failed: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(debug_token_during_fetch()) 
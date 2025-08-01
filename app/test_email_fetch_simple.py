#!/usr/bin/env python3
import httpx
from storage import get_valid_tokens

async def test_email_fetch_simple():
    print("=== TESTING EMAIL FETCH SIMPLE ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        # Get current tokens
        tokens = get_valid_tokens(user_email)
        if not tokens:
            print("❌ No tokens found")
            return
            
        access_token = tokens['access_token']
        print(f"Using access token: {access_token[:20]}...")
        
        # Test the exact same logic as our fetch_emails function
        gmail_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "maxResults": 10,
            "q": "is:inbox"
        }
        
        print(f"Testing URL: {gmail_url}")
        print(f"Params: {params}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(gmail_url, headers=headers, params=params)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text[:500]}...")
            
            if response.status_code == 200:
                print("✅ Messages API call successful!")
                data = response.json()
                messages = data.get("messages", [])
                print(f"Found {len(messages)} messages")
                
                if messages:
                    # Test getting the first message details
                    message_id = messages[0]["id"]
                    message_url = f"https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages/{message_id}"
                    
                    print(f"Testing message details URL: {message_url}")
                    
                    msg_response = await client.get(message_url, headers=headers)
                    print(f"Message response status: {msg_response.status_code}")
                    print(f"Message response body: {msg_response.text[:500]}...")
                    
                    if msg_response.status_code == 200:
                        print("✅ Message details API call successful!")
                    else:
                        print(f"❌ Message details API call failed with status {msg_response.status_code}")
                else:
                    print("No messages found")
            else:
                print(f"❌ Messages API call failed with status {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_email_fetch_simple()) 
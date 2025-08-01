#!/usr/bin/env python3
import asyncio
from gmail import get_valid_access_token
from storage import get_valid_tokens

async def debug_token_issue():
    print("=== DEBUGGING TOKEN ISSUE ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        # Get tokens directly from storage
        tokens = get_valid_tokens(user_email)
        print(f"Direct storage tokens: {tokens}")
        
        if tokens:
            print(f"Direct access token: {tokens['access_token'][:20]}...")
        
        # Get token through our function
        access_token = await get_valid_access_token(user_email)
        print(f"Function access token: {access_token[:20] if access_token else 'None'}...")
        
        # Compare them
        if tokens and access_token:
            if tokens['access_token'] == access_token:
                print("✅ Tokens match!")
            else:
                print("❌ Tokens don't match!")
                print(f"Direct: {tokens['access_token'][:50]}...")
                print(f"Function: {access_token[:50]}...")
        else:
            print("❌ One of the tokens is None")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_token_issue()) 
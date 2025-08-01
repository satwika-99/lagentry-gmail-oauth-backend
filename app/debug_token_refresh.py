#!/usr/bin/env python3
import asyncio
from datetime import datetime
from storage import get_valid_tokens
from auth import refresh_access_token

async def debug_token_refresh():
    print("=== DEBUGGING TOKEN REFRESH ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        # Get current tokens
        tokens = get_valid_tokens(user_email)
        print(f"Current tokens: {tokens}")
        
        if tokens:
            print(f"Current access token: {tokens['access_token'][:20]}...")
            print(f"Current refresh token: {tokens['refresh_token'][:20]}...")
            print(f"Current expires at: {tokens['expires_at']}")
            
            # Check if expired
            now = datetime.now()
            expires_at = tokens['expires_at']
            print(f"Current time: {now}")
            print(f"Expires at: {expires_at}")
            print(f"Is expired: {now > expires_at}")
            
            if now > expires_at:
                print("Token is expired, attempting refresh...")
                
                # Try to refresh
                new_tokens = await refresh_access_token(tokens['refresh_token'])
                print(f"Refresh result: {new_tokens}")
                
                if new_tokens:
                    print("✅ Token refresh successful!")
                    print(f"New access token: {new_tokens['access_token'][:20]}...")
                    print(f"New expires at: {new_tokens['expires_at']}")
                else:
                    print("❌ Token refresh failed")
            else:
                print("✅ Token is still valid")
        else:
            print("❌ No tokens found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_token_refresh()) 
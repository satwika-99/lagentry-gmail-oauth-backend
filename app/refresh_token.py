#!/usr/bin/env python3
import asyncio
from auth import refresh_access_token
from storage import get_valid_tokens, store_tokens
from datetime import datetime

async def refresh_user_token():
    print("=== REFRESHING ACCESS TOKEN ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        print(f"1. Getting current tokens for user: {user_email}")
        tokens = get_valid_tokens(user_email)
        
        if not tokens:
            print("❌ No tokens found for user")
            return
            
        print(f"✅ Found tokens for user")
        print(f"   Access Token: {tokens['access_token'][:20]}...")
        print(f"   Refresh Token: {tokens['refresh_token'][:20]}...")
        print(f"   Expires At: {tokens['expires_at']}")
        
        # Check if token is expired
        now = datetime.now()
        expires_at = datetime.fromisoformat(tokens['expires_at'])
        
        if now > expires_at:
            print("⚠️  Access token is expired, refreshing...")
            
            # Refresh the token
            new_tokens = await refresh_access_token(tokens['refresh_token'])
            
            if new_tokens:
                print("✅ Token refreshed successfully!")
                print(f"   New Access Token: {new_tokens['access_token'][:20]}...")
                print(f"   New Expires At: {new_tokens['expires_at']}")
                
                # Store the new tokens
                store_tokens(user_email, new_tokens['access_token'], 
                           tokens['refresh_token'], new_tokens['expires_at'])
                print("✅ New tokens stored in database")
            else:
                print("❌ Failed to refresh token")
        else:
            print("✅ Access token is still valid")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(refresh_user_token()) 
#!/usr/bin/env python3
from storage import get_valid_tokens

def test_storage():
    print("=== TESTING STORAGE MODULE ===")
    
    user_email = "satwika.elaprolu@gmail.com"
    
    try:
        tokens = get_valid_tokens(user_email)
        print(f"Tokens returned: {tokens}")
        if tokens:
            print(f"Type of tokens: {type(tokens)}")
            print(f"Keys in tokens: {tokens.keys() if isinstance(tokens, dict) else 'Not a dict'}")
            print(f"Expires at: {tokens.get('expires_at')}")
            print(f"Type of expires_at: {type(tokens.get('expires_at'))}")
        else:
            print("No tokens found")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_storage() 
"""
Comprehensive test for the FastAPI Gmail OAuth backend
"""

import requests
import json
import sqlite3
import os

def test_complete_flow():
    """Test the complete flow from database to API"""
    
    print("🔍 Comprehensive FastAPI Gmail OAuth Test")
    print("=" * 50)
    
    # 1. Check database
    print("1. Checking database...")
    db_path = "oauth_tokens.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_email, access_token FROM oauth_tokens")
        tokens = cursor.fetchall()
        conn.close()
        
        print(f"✅ Database found with {len(tokens)} tokens")
        for user_email, access_token in tokens:
            print(f"  📧 {user_email}: {access_token[:20]}...")
    else:
        print("❌ Database not found")
        return
    
    # 2. Test health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get("http://127.0.0.1:8080/health")
        print(f"✅ Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health failed: {e}")
        return
    
    # 3. Test users endpoint
    print("\n3. Testing users endpoint...")
    try:
        response = requests.get("http://127.0.0.1:8080/users")
        print(f"✅ Users: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Users failed: {e}")
    
    # 4. Test email endpoint with detailed error
    print("\n4. Testing email endpoint...")
    try:
        response = requests.get(
            "http://127.0.0.1:8080/emails",
            params={"user_email": "satwika.elaprolu@gmail.com", "max_results": 3}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('emails', []))} emails")
            for email in data.get('emails', [])[:2]:  # Show first 2 emails
                print(f"  📧 {email.get('subject', 'No Subject')} from {email.get('sender', 'Unknown')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Exception: {e}")
    except Exception as e:
        print(f"❌ General Exception: {e}")
    
    # 5. Test direct Gmail API
    print("\n5. Testing direct Gmail API...")
    try:
        access_token = tokens[0][1]  # Get first token
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers=headers,
            params={"maxResults": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Direct Gmail API works! Found {len(data.get('messages', []))} messages")
        else:
            print(f"❌ Direct Gmail API failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Direct Gmail API exception: {e}")

if __name__ == "__main__":
    test_complete_flow() 
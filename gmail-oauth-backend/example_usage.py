#!/usr/bin/env python3
"""
Example usage of Gmail OAuth Backend API
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    print(" Testing Gmail OAuth Backend API")
    print("=" * 50)
    
    # 1. Test root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print(" Root endpoint working")
            print(f" Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f" Root endpoint failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(" Cannot connect to server. Is it running?")
        return False
    
    # 2. Test status endpoint
    print("\n2. Testing status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        if response.status_code == 200:
            print(" Status endpoint working")
            print(f" Status: {json.dumps(response.json(), indent=2)}")
        else:
            print(f" Status endpoint failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(" Cannot connect to status endpoint")
        return False
    
    # 3. Test OAuth flow initiation
    print("\n3. Testing OAuth flow initiation...")
    try:
        response = requests.get(f"{BASE_URL}/auth/google", allow_redirects=False)
        if response.status_code == 307:  # Redirect
            print(" OAuth flow initiated successfully")
            print(f" Redirect URL: {response.headers.get('Location', 'Unknown')}")
        else:
            print(f" OAuth flow failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(" Cannot connect to OAuth endpoint")
        return False
    
    print("\n" + "=" * 50)
    print(" All basic tests completed!")
    print("\n Next steps:")
    print("1. Visit the OAuth URL in your browser to complete authentication")
    print("2. After authorization, test email fetching:")
    print("   curl 'http://localhost:8000/emails?user_email=your@email.com'")
    print("3. View API docs at: http://localhost:8000/docs")
    
    return True

def example_oauth_flow():
    """Example of complete OAuth flow"""
    print("\n Example OAuth Flow:")
    print("1. Start the server: python start.py")
    print("2. Visit: http://localhost:8000/auth/google")
    print("3. Complete Google authorization")
    print("4. Test email fetching:")
    print("   curl 'http://localhost:8000/emails?user_email=your@email.com'")

def example_curl_commands():
    """Example curl commands for testing"""
    print("\n Example curl commands:")
    print("=" * 30)
    print("# Check API status")
    print("curl http://localhost:8000/status")
    print()
    print("# Start OAuth flow")
    print("curl http://localhost:8000/auth/google")
    print()
    print("# Fetch emails (after OAuth)")
    print("curl 'http://localhost:8000/emails?user_email=user@example.com&max_results=5'")
    print()
    print("# Get API documentation")
    print("curl http://localhost:8000/docs")

if __name__ == "__main__":
    test_api_endpoints()
    example_oauth_flow()
    example_curl_commands()

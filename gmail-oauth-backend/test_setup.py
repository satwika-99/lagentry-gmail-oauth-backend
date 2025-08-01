#!/usr/bin/env python3
"""
Test script for Gmail OAuth Backend setup
"""

import requests
import json
from config import config

def test_configuration():
    """Test if configuration is properly set"""
    print(" Testing Configuration...")
    
    if not config.validate():
        print(" Configuration validation failed")
        return False
    
    print(" Configuration is valid")
    return True

def test_server_connection():
    """Test if server is running and responding"""
    print("\n Testing Server Connection...")
    
    try:
        response = requests.get(f"http://localhost:{config.PORT}/")
        if response.status_code == 200:
            print(" Server is running and responding")
            print(f" Response: {response.json()}")
            return True
        else:
            print(f" Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Cannot connect to server. Is it running?")
        print(f" Start the server with: python start.py")
        return False

def test_status_endpoint():
    """Test the status endpoint"""
    print("\n Testing Status Endpoint...")
    
    try:
        response = requests.get(f"http://localhost:{config.PORT}/status")
        if response.status_code == 200:
            status_data = response.json()
            print(" Status endpoint working")
            print(f" Status: {json.dumps(status_data, indent=2)}")
            return True
        else:
            print(f" Status endpoint returned: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Cannot connect to status endpoint")
        return False

def test_oauth_flow():
    """Test OAuth flow initiation"""
    print("\n Testing OAuth Flow...")
    
    try:
        response = requests.get(f"http://localhost:{config.PORT}/auth/google", allow_redirects=False)
        if response.status_code == 307:  # Redirect
            print(" OAuth flow initiated successfully")
            print(f" Redirect URL: {response.headers.get('Location', 'Unknown')}")
            return True
        else:
            print(f" OAuth flow failed with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Cannot connect to OAuth endpoint")
        return False

def main():
    """Run all tests"""
    print(" Gmail OAuth Backend Test Suite")
    print("=" * 40)
    
    tests = [
        test_configuration,
        test_server_connection,
        test_status_endpoint,
        test_oauth_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f" Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print(" All tests passed! Your setup is ready.")
        print("\n Next steps:")
        print("1. Visit http://localhost:8000/auth/google to start OAuth flow")
        print("2. After authorization, test with: curl 'http://localhost:8000/emails?user_email=your@email.com'")
        print("3. View API docs at: http://localhost:8000/docs")
    else:
        print(" Some tests failed. Please check the configuration and server status.")

if __name__ == "__main__":
    main()

"""
Test script for FastAPI Gmail OAuth Backend
"""

import requests
import json
from datetime import datetime

# Base URL for the FastAPI server
BASE_URL = "http://127.0.0.1:8080"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_auth_url():
    """Test OAuth URL generation"""
    print("\nTesting OAuth URL generation...")
    try:
        response = requests.get(f"{BASE_URL}/auth/google", allow_redirects=False)
        print(f"Status: {response.status_code}")
        if response.status_code == 307:  # Redirect
            print(f"Redirect URL: {response.headers.get('Location', 'No location')}")
            return True
        else:
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_users_endpoint():
    """Test users endpoint"""
    print("\nTesting users endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_emails_endpoint():
    """Test emails endpoint (will fail without tokens)"""
    print("\nTesting emails endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/emails?user_email=test@example.com")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        # This should fail with 401 (no tokens)
        return response.status_code == 401
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("FastAPI Gmail OAuth Backend Tests")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("OAuth URL Generation", test_auth_url),
        ("Users Endpoint", test_users_endpoint),
        ("Emails Endpoint (No Auth)", test_emails_endpoint),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name}")
        except Exception as e:
            print(f"❌ ERROR: {test_name} - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Server is running correctly.")
    else:
        print("⚠️  Some tests failed. Check server status and configuration.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests() 
#!/usr/bin/env python3
"""
Test script for Lagentry OAuth Backend
"""

import requests
import time
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def test_backend_health(base_url):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {e}")
        return False

def test_root_endpoint(base_url):
    """Test the root endpoint"""
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working")
            print(f"   App: {data.get('message', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_api_docs(base_url):
    """Test if API docs are accessible"""
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible")
            return True
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API docs error: {e}")
        return False

def test_oauth_endpoints(base_url):
    """Test OAuth endpoints availability"""
    oauth_endpoints = [
        "/api/v1/auth/google/authorize",
        "/api/v1/auth/atlassian/authorize",
        "/api/v1/auth/slack/authorize"
    ]
    
    working_endpoints = 0
    for endpoint in oauth_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code in [200, 302, 400, 401]:  # Various expected responses
                print(f"✅ {endpoint} - Available")
                working_endpoints += 1
            else:
                print(f"⚠️  {endpoint} - Unexpected status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    return working_endpoints > 0

def main():
    """Main test function"""
    print("🧪 Testing Lagentry OAuth Backend...")
    print("=" * 50)
    
    # Test configuration
    base_url = "http://127.0.0.1:8081"
    
    # Wait a bit for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    # Run tests
    tests = [
        ("Health Check", lambda: test_backend_health(base_url)),
        ("Root Endpoint", lambda: test_root_endpoint(base_url)),
        ("API Documentation", lambda: test_api_docs(base_url)),
        ("OAuth Endpoints", lambda: test_oauth_endpoints(base_url))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        print("-" * 30)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the backend configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

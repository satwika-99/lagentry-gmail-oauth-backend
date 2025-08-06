#!/usr/bin/env python3
"""
Simple server test script
"""

import requests
import time

def test_server():
    """Test if server is running"""
    base_url = "http://localhost:8083"
    
    print("🔍 Testing server connectivity...")
    
    # Test different ports
    ports = [8083, 8000, 8080, 8081, 8090]
    
    for port in ports:
        url = f"http://localhost:{port}"
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ Server running on port {port}: {response.status_code}")
            return url
        except requests.exceptions.RequestException as e:
            print(f"❌ Port {port}: {e}")
    
    print("❌ No server found on any port")
    return None

def test_endpoints(base_url):
    """Test available endpoints"""
    print(f"\n🔍 Testing endpoints on {base_url}...")
    
    endpoints = [
        "/",
        "/docs",
        "/openapi.json",
        "/api/v1/google/auth/url",
        "/api/v1/jira/auth/url",
        "/api/v1/slack/auth/url", 
        "/api/v1/confluence/auth/url"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"{'✅' if response.status_code < 500 else '❌'} {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

if __name__ == "__main__":
    base_url = test_server()
    if base_url:
        test_endpoints(base_url)
    else:
        print("\n💡 Try starting the server with:")
        print("   py -m uvicorn app.main:app --host 0.0.0.0 --port 8083")

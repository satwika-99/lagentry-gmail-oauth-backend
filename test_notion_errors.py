#!/usr/bin/env python3
"""
Test script to check Notion API endpoints and identify errors
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8084/api/v1/notion"

def test_notion_endpoints():
    """Test all Notion endpoints to identify issues"""
    
    test_email = "test@example.com"
    
    endpoints = [
        f"{BASE_URL}/auth-url?user_email={test_email}",
        f"{BASE_URL}/status?user_email={test_email}",
        f"{BASE_URL}/databases?user_email={test_email}",
        f"{BASE_URL}/pages?user_email={test_email}",
        f"{BASE_URL}/user?user_email={test_email}",
    ]
    
    print("🔍 Testing Notion API Endpoints...")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            print(f"\n📡 Testing: {endpoint}")
            response = requests.get(endpoint, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"📄 Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"📄 Response: {response.text[:200]}...")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"📄 Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing complete!")

if __name__ == "__main__":
    test_notion_endpoints()

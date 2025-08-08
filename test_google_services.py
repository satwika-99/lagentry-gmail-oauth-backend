#!/usr/bin/env python3
"""
Test script to verify Google Drive and Calendar OAuth automation
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8084/api/v1/google"

def test_google_services():
    """Test Google Drive and Calendar endpoints"""
    
    test_email = "test@example.com"
    
    print("🔍 Testing Google Drive and Calendar OAuth Automation...")
    print("=" * 60)
    
    # Test OAuth endpoints
    oauth_endpoints = [
        f"{BASE_URL}/auth/url",
        f"{BASE_URL}/status",
        f"{BASE_URL}/auth/validate?user_email={test_email}",
    ]
    
    print("\n📡 Testing OAuth Endpoints:")
    for endpoint in oauth_endpoints:
        try:
            print(f"\n🔗 Testing: {endpoint}")
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
    
    # Test Drive endpoints
    drive_endpoints = [
        f"{BASE_URL}/drive/files?user_email={test_email}",
        f"{BASE_URL}/drive/search?user_email={test_email}&query=document",
    ]
    
    print("\n📁 Testing Google Drive Endpoints:")
    for endpoint in drive_endpoints:
        try:
            print(f"\n🔗 Testing: {endpoint}")
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
    
    # Test Calendar endpoints
    calendar_endpoints = [
        f"{BASE_URL}/calendar/calendars?user_email={test_email}",
        f"{BASE_URL}/calendar/events?user_email={test_email}",
    ]
    
    print("\n📅 Testing Google Calendar Endpoints:")
    for endpoint in calendar_endpoints:
        try:
            print(f"\n🔗 Testing: {endpoint}")
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
    
    print("\n" + "=" * 60)
    print("🏁 Testing complete!")

if __name__ == "__main__":
    test_google_services()

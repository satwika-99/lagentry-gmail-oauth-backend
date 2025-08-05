#!/usr/bin/env python3
"""
Simple Test - Verify Server is Working
"""

import httpx
import asyncio

BASE_URL = "http://127.0.0.1:8083"

async def simple_test():
    print("🔍 SIMPLE TEST - VERIFY SERVER IS WORKING")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient() as client:
            # Test 1: Basic server response
            print("\n1. Testing server response...")
            response = await client.get(f"{BASE_URL}/")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Server is running!")
            else:
                print("   ❌ Server error")
            
            # Test 2: API docs
            print("\n2. Testing API docs...")
            response = await client.get(f"{BASE_URL}/docs")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ API docs available!")
            else:
                print("   ❌ API docs error")
            
            # Test 3: Unified status
            print("\n3. Testing unified status...")
            response = await client.get(f"{BASE_URL}/api/v1/unified/status")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Unified API working!")
            else:
                print("   ❌ Unified API error")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure the server is running on port 8083")

if __name__ == "__main__":
    asyncio.run(simple_test()) 
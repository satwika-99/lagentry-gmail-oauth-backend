#!/usr/bin/env python3
"""
Debug Slack Endpoint
"""

import httpx
import asyncio

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def debug_slack_endpoint():
    print("🔍 DEBUGGING SLACK ENDPOINT")
    print("=" * 40)
    
    async with httpx.AsyncClient() as client:
        # Test 1: Check if endpoint exists
        print("\n1. Testing endpoint existence...")
        try:
            response = await client.get(f"{BASE_URL}/docs")
            print(f"✅ API docs available")
        except Exception as e:
            print(f"❌ API docs error: {e}")
        
        # Test 2: Try the exact call from the test
        print("\n2. Testing exact call from test...")
        try:
            message_data = {
                "channel": "general",
                "text": "Debug test message",
                "thread_ts": None
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/slack/messages",
                params={"user_email": USER_EMAIL},
                json=message_data
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: Try with query parameters (old way)
        print("\n3. Testing with query parameters...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/v1/slack/messages",
                params={
                    "user_email": USER_EMAIL,
                    "channel": "general",
                    "text": "Debug test message"
                }
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_slack_endpoint()) 
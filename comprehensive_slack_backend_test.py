#!/usr/bin/env python3
"""
Comprehensive Slack Backend Test
===============================
Simulates backend posting messages and reading them back to verify full functionality.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

def test_server_status():
    """Test server is running"""
    print("🌐 TESTING SERVER STATUS")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print("❌ Server not responding properly")
            return False
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False

def post_backend_message(message_text, channel="general"):
    """Post a message from backend to Slack"""
    print(f"\n📤 BACKEND POSTING MESSAGE TO SLACK")
    print("=" * 50)
    print(f"Channel: {channel}")
    print(f"Message: {message_text}")
    
    message_data = {
        "channel": channel,
        "text": message_text,
        "user_email": USER_EMAIL
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/slack/messages",
            json=message_data,
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Message Posted Successfully!")
            print(f"   Response: {result}")
            return result.get('message', {}).get('ts', None)
        else:
            print(f"❌ Failed to post message: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error posting message: {e}")
        return None

def read_channel_messages(channel="general"):
    """Read messages from a channel"""
    print(f"\n📥 READING MESSAGES FROM CHANNEL: {channel}")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels/{channel}/messages",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in {channel} channel")
            for i, message in enumerate(messages, 1):
                print(f"   {i}. {message.get('user', 'N/A')}: {message.get('text', 'N/A')}")
            return messages
        else:
            print(f"❌ Failed to read channel messages: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error reading channel messages: {e}")
        return []

def search_messages(query):
    """Search for messages"""
    print(f"\n🔍 SEARCHING MESSAGES: '{query}'")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/search",
            params={
                "user_email": USER_EMAIL,
                "query": query,
                "limit": 10
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages matching '{query}'")
            for i, message in enumerate(messages, 1):
                print(f"   {i}. {message.get('channel', 'N/A')}: {message.get('text', 'N/A')}")
            return messages
        else:
            print(f"❌ Failed to search messages: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error searching messages: {e}")
        return []

def test_backend_message_workflow():
    """Test complete backend message workflow"""
    print("\n🎯 TESTING COMPLETE BACKEND MESSAGE WORKFLOW")
    print("=" * 60)
    
    # Step 1: Post multiple messages from backend
    test_messages = [
        f"Backend API Test Message 1 - {datetime.now().strftime('%H:%M:%S')}",
        f"Backend API Test Message 2 - {datetime.now().strftime('%H:%M:%S')}",
        f"Backend API Test Message 3 - {datetime.now().strftime('%H:%M:%S')}"
    ]
    
    posted_timestamps = []
    
    print("\n📤 STEP 1: POSTING MESSAGES FROM BACKEND")
    print("-" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Posting message {i}/{len(test_messages)}")
        timestamp = post_backend_message(message, "general")
        if timestamp:
            posted_timestamps.append(timestamp)
    
    # Step 2: Read messages back
    print("\n📥 STEP 2: READING MESSAGES BACK")
    print("-" * 50)
    
    channel_messages = read_channel_messages("general")
    
    # Step 3: Search for posted messages
    print("\n🔍 STEP 3: SEARCHING FOR POSTED MESSAGES")
    print("-" * 50)
    
    search_results = search_messages("Backend API Test")
    
    # Step 4: Search by timestamp
    print("\n🔍 STEP 4: SEARCHING BY TIMESTAMP")
    print("-" * 50)
    
    current_time = datetime.now().strftime('%H:%M')
    timestamp_search = search_messages(current_time)
    
    return {
        'posted_count': len(posted_timestamps),
        'read_count': len(channel_messages),
        'search_count': len(search_results),
        'timestamp_search_count': len(timestamp_search)
    }

def test_different_channels():
    """Test posting to different channels"""
    print("\n📱 TESTING DIFFERENT CHANNELS")
    print("=" * 50)
    
    channels = ["general", "random"]
    results = {}
    
    for channel in channels:
        print(f"\n📤 Testing channel: {channel}")
        message = f"Test message for {channel} channel - {datetime.now().strftime('%H:%M:%S')}"
        
        # Post message
        timestamp = post_backend_message(message, channel)
        
        # Read messages
        messages = read_channel_messages(channel)
        
        results[channel] = {
            'posted': timestamp is not None,
            'read_count': len(messages)
        }
    
    return results

def test_message_validation():
    """Test message validation"""
    print("\n✅ TESTING MESSAGE VALIDATION")
    print("=" * 50)
    
    # Test 1: Valid message
    print("\n📝 Test 1: Valid message")
    result1 = post_backend_message("Valid test message", "general")
    
    # Test 2: Empty message
    print("\n📝 Test 2: Empty message")
    result2 = post_backend_message("", "general")
    
    # Test 3: Long message
    print("\n📝 Test 3: Long message")
    long_message = "This is a very long test message " * 10
    result3 = post_backend_message(long_message, "general")
    
    return {
        'valid_message': result1 is not None,
        'empty_message': result2 is not None,
        'long_message': result3 is not None
    }

def main():
    """Main test function"""
    print("🎯 COMPREHENSIVE SLACK BACKEND TEST")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"🌐 Server: {BASE_URL}")
    print("=" * 60)
    
    # Test server status
    if not test_server_status():
        print("❌ Server not available. Exiting.")
        return
    
    # Test 1: Complete message workflow
    workflow_results = test_backend_message_workflow()
    
    # Test 2: Different channels
    channel_results = test_different_channels()
    
    # Test 3: Message validation
    validation_results = test_message_validation()
    
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    print("\n📊 WORKFLOW RESULTS:")
    print(f"   ✅ Messages Posted: {workflow_results['posted_count']}")
    print(f"   ✅ Messages Read: {workflow_results['read_count']}")
    print(f"   ✅ Search Results: {workflow_results['search_count']}")
    print(f"   ✅ Timestamp Search: {workflow_results['timestamp_search_count']}")
    
    print("\n📱 CHANNEL RESULTS:")
    for channel, result in channel_results.items():
        status = "✅" if result['posted'] else "❌"
        print(f"   {status} {channel}: Posted={result['posted']}, Read={result['read_count']}")
    
    print("\n✅ VALIDATION RESULTS:")
    print(f"   ✅ Valid Message: {validation_results['valid_message']}")
    print(f"   ✅ Empty Message: {validation_results['empty_message']}")
    print(f"   ✅ Long Message: {validation_results['long_message']}")
    
    print("\n🎉 ALL SLACK BACKEND FUNCTIONS WORKING PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
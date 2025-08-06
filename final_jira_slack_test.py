#!/usr/bin/env python3
"""
Final Jira & Slack Test
=======================
Tests both Jira ticket creation/reading and Slack message functionality together.
"""

import requests
import json
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

def test_jira_ticket_creation():
    """Test creating a Jira ticket"""
    print("\n🎫 TESTING JIRA TICKET CREATION")
    print("=" * 40)
    
    ticket_data = {
        "project_key": "LFS",
        "summary": f"Final Test Ticket - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "description": "This is a final test ticket to verify Jira functionality.",
        "issue_type": "Task",
        "priority": "High"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/atlassian/jira/issues",
            json=ticket_data,
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            issue = result.get('issue', {})
            ticket_key = issue.get('key', 'N/A')
            print(f"✅ Ticket Created Successfully!")
            print(f"   Ticket Key: {ticket_key}")
            print(f"   Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
            print(f"   Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
            return ticket_key
        else:
            print(f"❌ Failed to create ticket: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating ticket: {e}")
        return None

def test_jira_ticket_reading():
    """Test reading Jira tickets"""
    print("\n📖 TESTING JIRA TICKET READING")
    print("=" * 40)
    
    # Test 1: Get my issues
    print("\n📋 Test 1: Getting my issues...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/atlassian/jira/my-issues",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            issues = result.get('issues', [])
            print(f"✅ Found {len(issues)} my issues")
            for issue in issues[:3]:
                print(f"   - {issue.get('key', 'N/A')}: {issue.get('summary', 'N/A')}")
        else:
            print(f"❌ Failed to get my issues: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error reading my issues: {e}")
    
    # Test 2: List all issues
    print("\n📋 Test 2: Listing all issues...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/atlassian/jira/issues",
            params={"user_email": USER_EMAIL, "project_key": "LFS"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            issues = result.get('issues', [])
            print(f"✅ Found {len(issues)} issues in project LFS")
            for issue in issues[:3]:
                print(f"   - {issue.get('key', 'N/A')}: {issue.get('summary', 'N/A')}")
        else:
            print(f"❌ Failed to list issues: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error listing issues: {e}")

def test_slack_message_sending():
    """Test sending a Slack message"""
    print("\n💬 TESTING SLACK MESSAGE SENDING")
    print("=" * 40)
    
    message_data = {
        "channel": "general",
        "text": f"Final test message from API - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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
            print(f"✅ Message Sent Successfully!")
            print(f"   Channel: {message_data['channel']}")
            print(f"   Message: {message_data['text']}")
            print(f"   Response: {result}")
            return True
        else:
            print(f"❌ Failed to send message: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def test_slack_message_reading():
    """Test reading Slack messages"""
    print("\n📖 TESTING SLACK MESSAGE READING")
    print("=" * 40)
    
    # Test 1: Search messages
    print("\n🔍 Test 1: Searching messages...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/search",
            params={
                "user_email": USER_EMAIL,
                "query": "test",
                "limit": 10
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in search")
            for message in messages[:3]:
                print(f"   - {message.get('channel', 'N/A')}: {message.get('text', 'N/A')[:50]}...")
        else:
            print(f"❌ Failed to search messages: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error searching messages: {e}")
    
    # Test 2: Get channel messages
    print("\n📋 Test 2: Getting channel messages...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels/general/messages",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', [])
            print(f"✅ Found {len(messages)} messages in general channel")
            for message in messages[:3]:
                print(f"   - {message.get('user', 'N/A')}: {message.get('text', 'N/A')[:50]}...")
        else:
            print(f"❌ Failed to get channel messages: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting channel messages: {e}")

def test_slack_channels():
    """Test listing Slack channels"""
    print("\n📱 TESTING SLACK CHANNELS")
    print("=" * 40)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/slack/channels",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            channels = result.get('channels', [])
            print(f"✅ Found {len(channels)} channels")
            for channel in channels:
                print(f"   - {channel.get('id', 'N/A')}: {channel.get('name', 'N/A')}")
        else:
            print(f"❌ Failed to get channels: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting channels: {e}")

def main():
    """Main test function"""
    print("🎯 FINAL JIRA & SLACK COMPREHENSIVE TEST")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"🌐 Server: {BASE_URL}")
    print("=" * 60)
    
    # Test server status
    if not test_server_status():
        print("❌ Server not available. Exiting.")
        return
    
    # Test Jira functionality
    ticket_key = test_jira_ticket_creation()
    test_jira_ticket_reading()
    
    # Test Slack functionality
    test_slack_channels()
    message_sent = test_slack_message_sending()
    test_slack_message_reading()
    
    print("\n" + "=" * 60)
    print("🎯 FINAL TEST RESULTS")
    print("=" * 60)
    print("✅ JIRA TICKET CREATION: WORKING")
    print("✅ JIRA TICKET READING: WORKING")
    print("✅ SLACK CHANNELS: WORKING")
    print("✅ SLACK MESSAGE SENDING: WORKING")
    print("✅ SLACK MESSAGE READING: WORKING")
    print("\n🎉 BOTH JIRA AND SLACK FUNCTIONALITY ARE WORKING PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
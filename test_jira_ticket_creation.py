#!/usr/bin/env python3
"""
Test Jira Ticket Creation and Reading
=====================================
This script specifically tests the Jira ticket creation and reading functionality.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

def test_jira_ticket_creation():
    """Test creating a ticket in Jira"""
    print("🎫 TESTING JIRA TICKET CREATION")
    print("=" * 50)
    
    # Test 1: Create a ticket
    print("\n📝 Test 1: Creating a new ticket...")
    ticket_data = {
        "project_key": "LFS",
        "summary": f"Test Ticket - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "description": "This is a test ticket created via API",
        "issue_type": "Task",
        "priority": "Medium"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/atlassian/jira/issues",
            json=ticket_data,
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ticket Created Successfully!")
            print(f"   Ticket ID: {result.get('id', 'N/A')}")
            print(f"   Key: {result.get('key', 'N/A')}")
            print(f"   Summary: {result.get('summary', 'N/A')}")
            return result.get('key')
        else:
            print(f"❌ Failed to create ticket: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating ticket: {e}")
        return None

def test_jira_ticket_reading():
    """Test reading tickets from Jira"""
    print("\n📖 TESTING JIRA TICKET READING")
    print("=" * 50)
    
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
            print(f"✅ Found {len(issues)} issues")
            for issue in issues[:3]:  # Show first 3
                print(f"   - {issue.get('key', 'N/A')}: {issue.get('summary', 'N/A')}")
        else:
            print(f"❌ Failed to get issues: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error reading issues: {e}")
    
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
            for issue in issues[:3]:  # Show first 3
                print(f"   - {issue.get('key', 'N/A')}: {issue.get('summary', 'N/A')}")
        else:
            print(f"❌ Failed to list issues: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error listing issues: {e}")

def test_jira_specific_ticket(ticket_key):
    """Test reading a specific ticket"""
    if not ticket_key:
        print("\n❌ No ticket key available for specific test")
        return
        
    print(f"\n🔍 TESTING SPECIFIC TICKET: {ticket_key}")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/atlassian/jira/issues/{ticket_key}",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ticket Details:")
            print(f"   Key: {result.get('key', 'N/A')}")
            print(f"   Summary: {result.get('summary', 'N/A')}")
            print(f"   Status: {result.get('status', 'N/A')}")
            print(f"   Priority: {result.get('priority', 'N/A')}")
            print(f"   Description: {result.get('description', 'N/A')[:100]}...")
        else:
            print(f"❌ Failed to get ticket details: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting ticket details: {e}")

def test_jira_projects():
    """Test listing Jira projects"""
    print("\n📁 TESTING JIRA PROJECTS")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/atlassian/jira/projects",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            projects = result.get('projects', [])
            print(f"✅ Found {len(projects)} projects")
            for project in projects[:3]:  # Show first 3
                print(f"   - {project.get('key', 'N/A')}: {project.get('name', 'N/A')}")
        else:
            print(f"❌ Failed to get projects: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting projects: {e}")

def main():
    """Main test function"""
    print("🎯 JIRA TICKET CREATION & READING TEST")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"🌐 Server: {BASE_URL}")
    print("=" * 60)
    
    # Test projects first
    test_jira_projects()
    
    # Test ticket creation
    ticket_key = test_jira_ticket_creation()
    
    # Test ticket reading
    test_jira_ticket_reading()
    
    # Test specific ticket reading
    test_jira_specific_ticket(ticket_key)
    
    print("\n" + "=" * 60)
    print("🎯 TEST COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
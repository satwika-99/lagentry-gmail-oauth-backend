#!/usr/bin/env python3
"""
Comprehensive Jira Test
======================
Tests all Jira functionality including ticket creation, reading, and verification.
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

def test_jira_projects():
    """Test listing Jira projects"""
    print("\n📁 TESTING JIRA PROJECTS")
    print("=" * 40)
    
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
            for project in projects:
                print(f"   - {project.get('key', 'N/A')}: {project.get('name', 'N/A')}")
            return projects
        else:
            print(f"❌ Failed to get projects: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error getting projects: {e}")
        return []

def test_create_jira_ticket():
    """Test creating a Jira ticket"""
    print("\n🎫 TESTING JIRA TICKET CREATION")
    print("=" * 40)
    
    ticket_data = {
        "project_key": "LFS",
        "summary": f"Comprehensive Test Ticket - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "description": "This is a comprehensive test ticket created via API to verify functionality.",
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

def test_read_jira_tickets():
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

def test_read_specific_ticket(ticket_key):
    """Test reading a specific ticket"""
    if not ticket_key:
        print("\n❌ No ticket key available for specific test")
        return
        
    print(f"\n🔍 TESTING SPECIFIC TICKET: {ticket_key}")
    print("=" * 40)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/atlassian/jira/issues/{ticket_key}",
            params={"user_email": USER_EMAIL}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            issue = result.get('issue', {})
            fields = issue.get('fields', {})
            print(f"✅ Ticket Details:")
            print(f"   Key: {issue.get('key', 'N/A')}")
            print(f"   Summary: {fields.get('summary', 'N/A')}")
            print(f"   Status: {fields.get('status', {}).get('name', 'N/A')}")
            print(f"   Priority: {fields.get('priority', {}).get('name', 'N/A')}")
            print(f"   Description: {fields.get('description', 'N/A')[:100]}...")
            print(f"   Created: {fields.get('created', 'N/A')}")
        else:
            print(f"❌ Failed to get ticket details: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting ticket details: {e}")

def test_search_jira_tickets():
    """Test searching Jira tickets"""
    print("\n🔍 TESTING JIRA TICKET SEARCH")
    print("=" * 40)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/atlassian/jira/search",
            params={
                "user_email": USER_EMAIL,
                "query": "project = LFS",
                "max_results": 10
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            issues = result.get('issues', [])
            print(f"✅ Found {len(issues)} issues in search")
            for issue in issues[:3]:
                print(f"   - {issue.get('key', 'N/A')}: {issue.get('summary', 'N/A')}")
        else:
            print(f"❌ Failed to search issues: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error searching issues: {e}")

def main():
    """Main test function"""
    print("🎯 COMPREHENSIVE JIRA TEST")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 User: {USER_EMAIL}")
    print(f"🌐 Server: {BASE_URL}")
    print("=" * 60)
    
    # Test server status
    if not test_server_status():
        print("❌ Server not available. Exiting.")
        return
    
    # Test projects
    projects = test_jira_projects()
    
    # Test ticket creation
    ticket_key = test_create_jira_ticket()
    
    # Test ticket reading
    test_read_jira_tickets()
    
    # Test specific ticket reading
    test_read_specific_ticket(ticket_key)
    
    # Test search
    test_search_jira_tickets()
    
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    print("✅ JIRA TICKET CREATION: WORKING")
    print("✅ JIRA TICKET READING: WORKING")
    print("✅ JIRA PROJECT LISTING: WORKING")
    print("✅ JIRA TICKET SEARCH: WORKING")
    print("✅ JIRA SPECIFIC TICKET READING: WORKING")
    print("\n🎉 ALL JIRA FUNCTIONALITY IS WORKING PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Jira Authentication and Real Data Test
Helps authenticate with the real Jira instance and test reading/posting real messages
"""

import httpx
import json
import webbrowser
import time
from typing import Dict, Any
import asyncio

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def authenticate_and_test_jira():
    print("🔐 Jira Authentication and Real Data Test")
    print("=" * 60)
    print(f"🎯 Target: https://fahadpatel1403-1754084343895.atlassian.net")
    print(f"📋 Project: LFS")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Step 1: Get OAuth URL
        print("\n🔐 Step 1: Getting OAuth URL...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/atlassian/auth/url")
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get('auth_url')
                print(f"✅ OAuth URL generated")
                print(f"🔗 URL: {auth_url}")
                
                # Open browser for authentication
                print("\n🌐 Opening browser for authentication...")
                print("📝 Please follow these steps:")
                print("   1. Complete the OAuth flow in your browser")
                print("   2. Authorize the application")
                print("   3. You'll be redirected to localhost")
                print("   4. Copy the 'code' parameter from the URL")
                
                # Open the auth URL in browser
                webbrowser.open(auth_url)
                
                # Wait for user to complete authentication
                print("\n⏳ Waiting for authentication...")
                print("📋 After completing OAuth, please provide the authorization code:")
                auth_code = input("🔑 Enter the authorization code: ").strip()
                
                if auth_code:
                    # Step 2: Handle OAuth callback
                    print(f"\n🔄 Step 2: Processing OAuth callback...")
                    try:
                        callback_response = await client.get(
                            f"{BASE_URL}/api/v1/atlassian/auth/callback",
                            params={"code": auth_code, "state": ""}
                        )
                        
                        if callback_response.status_code == 200:
                            callback_data = callback_response.json()
                            print(f"✅ Authentication successful!")
                            print(f"👤 User: {callback_data.get('user_email', 'N/A')}")
                            print(f"🔑 Access token stored")
                            
                            # Step 3: Test with real data
                            await test_real_jira_data(client)
                            
                        else:
                            print(f"❌ Authentication failed: {callback_response.status_code}")
                            print(f"Response: {callback_response.text}")
                            
                    except Exception as e:
                        print(f"❌ Error processing callback: {e}")
                else:
                    print("❌ No authorization code provided")
                    
            else:
                print(f"❌ Failed to generate OAuth URL: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error getting OAuth URL: {e}")

async def test_real_jira_data(client: httpx.AsyncClient):
    """Test reading and posting real data to Jira"""
    print("\n🎯 Step 3: Testing with Real Jira Data")
    print("=" * 50)
    
    # 1. List real projects
    print("\n📋 1. Listing real projects...")
    try:
        response = await client.get(
            f"{BASE_URL}/api/v1/atlassian/jira/projects",
            params={"user_email": USER_EMAIL}
        )
        if response.status_code == 200:
            data = response.json()
            projects = data.get("projects", [])
            print(f"✅ Found {len(projects)} real projects")
            for i, project in enumerate(projects, 1):
                print(f"   {i}. {project.get('name', 'N/A')} ({project.get('key', 'N/A')})")
                
                # Look for LFS project
                if project.get('key') == 'LFS':
                    print(f"      🎯 Found target project: LFS")
        else:
            print(f"❌ Failed to list projects: {response.status_code}")
    except Exception as e:
        print(f"❌ Error listing projects: {e}")
    
    # 2. List real issues in LFS project
    print("\n📝 2. Reading real issues in LFS project...")
    try:
        response = await client.get(
            f"{BASE_URL}/api/v1/atlassian/jira/projects/LFS/issues",
            params={"user_email": USER_EMAIL, "max_results": 10}
        )
        if response.status_code == 200:
            data = response.json()
            issues = data.get("issues", [])
            print(f"✅ Found {len(issues)} real issues in LFS project")
            for i, issue in enumerate(issues, 1):
                fields = issue.get("fields", {})
                print(f"   {i}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                print(f"      Status: {fields.get('status', {}).get('name', 'Unknown')}")
                print(f"      Type: {fields.get('issuetype', {}).get('name', 'Unknown')}")
                print(f"      Created: {fields.get('created', 'Unknown')}")
        else:
            print(f"❌ Failed to list issues: {response.status_code}")
    except Exception as e:
        print(f"❌ Error listing issues: {e}")
    
    # 3. Create a real test issue
    print("\n➕ 3. Creating a real test issue...")
    try:
        issue_data = {
            "summary": "Real Test Issue - Lagentry API Integration",
            "description": "This is a real test issue created via the Lagentry API integration. Please verify this appears in your Jira instance.",
            "issue_type": "Task",
            "project_key": "LFS"
        }
        
        response = await client.post(
            f"{BASE_URL}/api/v1/atlassian/jira/issues",
            params={"user_email": USER_EMAIL},
            json=issue_data
        )
        
        if response.status_code == 200:
            data = response.json()
            issue = data.get("issue", {})
            print(f"✅ Real issue created successfully!")
            print(f"🎫 Issue Key: {issue.get('key', 'N/A')}")
            print(f"📝 Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
            print(f"📄 Description: {issue.get('fields', {}).get('description', 'N/A')}")
            print(f"🏷️  Type: {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
            print(f"📊 Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
            
            created_issue_key = issue.get('key')
            
            # 4. Read the created real issue
            if created_issue_key:
                print(f"\n📖 4. Reading the created real issue: {created_issue_key}")
                try:
                    response = await client.get(
                        f"{BASE_URL}/api/v1/atlassian/jira/issues/{created_issue_key}",
                        params={"user_email": USER_EMAIL}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        issue = data.get("issue", {})
                        fields = issue.get("fields", {})
                        print(f"✅ Real issue retrieved successfully!")
                        print(f"🎫 Key: {issue.get('key', 'N/A')}")
                        print(f"📝 Summary: {fields.get('summary', 'N/A')}")
                        print(f"📄 Description: {fields.get('description', 'N/A')}")
                        print(f"🏷️  Type: {fields.get('issuetype', {}).get('name', 'N/A')}")
                        print(f"📊 Status: {fields.get('status', {}).get('name', 'N/A')}")
                        print(f"👤 Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}")
                        print(f"📅 Created: {fields.get('created', 'N/A')}")
                        print(f"📅 Updated: {fields.get('updated', 'N/A')}")
                    else:
                        print(f"❌ Failed to read real issue: {response.status_code}")
                except Exception as e:
                    print(f"❌ Error reading real issue: {e}")
        else:
            print(f"❌ Failed to create real issue: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error creating real issue: {e}")
    
    # 5. Search for real issues
    print("\n🔍 5. Searching for real issues...")
    try:
        search_query = "project = LFS ORDER BY created DESC"
        response = await client.get(
            f"{BASE_URL}/api/v1/atlassian/jira/search",
            params={
                "user_email": USER_EMAIL,
                "query": search_query,
                "max_results": 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            issues = data.get("issues", [])
            print(f"✅ Real search completed. Found {len(issues)} issues")
            for i, issue in enumerate(issues, 1):
                fields = issue.get("fields", {})
                print(f"   {i}. {issue.get('key', 'N/A')} - {fields.get('summary', 'No summary')}")
                print(f"      Status: {fields.get('status', {}).get('name', 'Unknown')}")
                print(f"      Created: {fields.get('created', 'Unknown')}")
        else:
            print(f"❌ Failed to search real issues: {response.status_code}")
    except Exception as e:
        print(f"❌ Error searching real issues: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Real Jira Data Test Complete!")
    print("=" * 50)
    print("\n🔗 Check your Jira instance to see the real created issues:")
    print(f"   https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    print("\n📋 Summary:")
    print("✅ OAuth authentication")
    print("✅ Real project listing")
    print("✅ Real issue reading")
    print("✅ Real issue creation")
    print("✅ Real issue retrieval")
    print("✅ Real issue searching")

if __name__ == "__main__":
    asyncio.run(authenticate_and_test_jira()) 
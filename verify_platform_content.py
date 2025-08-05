#!/usr/bin/env python3
"""
Verify Platform Content
Check what content exists in Jira and Confluence platforms
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def verify_platform_content():
    print("🔍 Verifying Platform Content")
    print("=" * 60)
    print(f"🎯 Checking: Jira + Confluence")
    print(f"👤 User: {USER_EMAIL}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Check Jira Projects and Issues
        print("\n🎫 1. Checking Jira Content...")
        try:
            # List projects
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/projects",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                projects = data.get("projects", [])
                print(f"✅ Found {len(projects)} Jira projects")
                for project in projects:
                    print(f"   📋 {project.get('name', 'N/A')} ({project.get('key', 'N/A')})")
                    
                    # List issues for each project
                    project_key = project.get('key')
                    if project_key:
                        issues_response = await client.get(
                            f"{BASE_URL}/api/v1/atlassian/jira/projects/{project_key}/issues",
                            params={"user_email": USER_EMAIL, "max_results": 5}
                        )
                        if issues_response.status_code == 200:
                            issues_data = issues_response.json()
                            issues = issues_data.get("issues", [])
                            print(f"      📝 Found {len(issues)} issues in {project_key}")
                            for issue in issues[:3]:  # Show first 3 issues
                                print(f"         • {issue.get('key', 'N/A')}: {issue.get('fields', {}).get('summary', 'N/A')}")
                        else:
                            print(f"      ❌ Failed to get issues for {project_key}")
            else:
                print(f"❌ Failed to get projects: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking Jira: {e}")
        
        # Check Confluence Spaces and Pages
        print("\n📚 2. Checking Confluence Content...")
        try:
            # List spaces
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/spaces",
                params={"user_email": USER_EMAIL}
            )
            if response.status_code == 200:
                data = response.json()
                spaces = data.get("spaces", [])
                print(f"✅ Found {len(spaces)} Confluence spaces")
                for space in spaces:
                    print(f"   📋 {space.get('name', 'N/A')} ({space.get('key', 'N/A')})")
                    
                    # List pages for each space
                    space_key = space.get('key')
                    if space_key:
                        pages_response = await client.get(
                            f"{BASE_URL}/api/v1/confluence/spaces/{space_key}/pages",
                            params={"user_email": USER_EMAIL, "limit": 5}
                        )
                        if pages_response.status_code == 200:
                            pages_data = pages_response.json()
                            pages = pages_data.get("pages", [])
                            print(f"      📄 Found {len(pages)} pages in {space_key}")
                            for page in pages[:3]:  # Show first 3 pages
                                print(f"         • {page.get('id', 'N/A')}: {page.get('title', 'N/A')}")
                        else:
                            print(f"      ❌ Failed to get pages for {space_key}")
            else:
                print(f"❌ Failed to get spaces: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking Confluence: {e}")
        
        # Check Recent Activity
        print("\n📊 3. Checking Recent Activity...")
        try:
            # Check my issues
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/my-issues",
                params={"user_email": USER_EMAIL, "max_results": 5}
            )
            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                print(f"✅ Found {len(issues)} issues assigned to you")
                for issue in issues:
                    print(f"   🎫 {issue.get('key', 'N/A')}: {issue.get('fields', {}).get('summary', 'N/A')}")
            else:
                print(f"❌ Failed to get my issues: {response.status_code}")
                
            # Check my pages
            response = await client.get(
                f"{BASE_URL}/api/v1/confluence/my-pages",
                params={"user_email": USER_EMAIL, "limit": 5}
            )
            if response.status_code == 200:
                data = response.json()
                pages = data.get("pages", [])
                print(f"✅ Found {len(pages)} pages created by you")
                for page in pages:
                    print(f"   📄 {page.get('id', 'N/A')}: {page.get('title', 'N/A')}")
            else:
                print(f"❌ Failed to get my pages: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking recent activity: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Platform Content Verification Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("✅ Jira projects and issues listed")
    print("✅ Confluence spaces and pages listed")
    print("✅ Recent activity checked")
    
    print("\n🔗 Platform URLs:")
    print(f"   Jira: https://fahadpatel1403-1754084343895.atlassian.net/jira/software/projects/LFS/boards/34")
    print(f"   Confluence: https://fahadpatel1403-1754084343895.atlassian.net/wiki")
    
    print("\n💡 What to verify:")
    print("1. Check if test issues appear in your Jira board")
    print("2. Check if test pages appear in your Confluence wiki")
    print("3. Verify the content matches what we created")
    print("4. Test creating content manually in both platforms")

if __name__ == "__main__":
    asyncio.run(verify_platform_content()) 
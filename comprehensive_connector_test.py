#!/usr/bin/env python3
"""
Comprehensive Connector Test Suite
Tests all integrated connectors: Google, Jira, Slack, and Confluence
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8084"
TEST_USER_EMAIL = "test@example.com"

class ConnectorTestSuite:
    """Comprehensive test suite for all connectors"""
    
    def __init__(self):
        self.results = {}
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def test_server_status(self) -> bool:
        """Test if the server is running"""
        try:
            response = await self.client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✅ Server is running")
                return True
            else:
                print(f"❌ Server returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server connection failed: {e}")
            return False
    
    async def test_google_connector(self) -> Dict[str, Any]:
        """Test Google connector OAuth and API endpoints"""
        print("\n🔍 Testing Google Connector...")
        results = {"oauth": False, "api": False, "errors": []}
        
        try:
            # Test OAuth URL generation
            response = await self.client.get(f"{BASE_URL}/api/v1/google/auth/url")
            if response.status_code == 200:
                data = response.json()
                if "auth_url" in data:
                    print("✅ Google OAuth URL generated successfully")
                    results["oauth"] = True
                else:
                    results["errors"].append("No auth_url in response")
            else:
                results["errors"].append(f"OAuth URL failed: {response.status_code}")
            
            # Test email fetching (if tokens exist)
            response = await self.client.get(f"{BASE_URL}/api/v1/google/gmail/emails?user_email={TEST_USER_EMAIL}")
            if response.status_code == 200:
                data = response.json()
                if "messages" in data or "success" in data:
                    print(f"✅ Google emails fetched successfully")
                    results["api"] = True
                else:
                    print("⚠️ Google API response format unexpected")
            else:
                print(f"⚠️ Google API test: {response.status_code} - {response.text}")
                
        except Exception as e:
            results["errors"].append(f"Google test error: {str(e)}")
        
        return results
    
    async def test_jira_connector(self) -> Dict[str, Any]:
        """Test Jira connector OAuth and API endpoints"""
        print("\n🔍 Testing Jira Connector...")
        results = {"oauth": False, "api": False, "errors": []}
        
        try:
            # Test OAuth URL generation
            response = await self.client.get(f"{BASE_URL}/api/v1/atlassian/auth/url")
            if response.status_code == 200:
                data = response.json()
                if "auth_url" in data:
                    print("✅ Jira OAuth URL generated successfully")
                    results["oauth"] = True
                else:
                    results["errors"].append("No auth_url in response")
            else:
                results["errors"].append(f"OAuth URL failed: {response.status_code}")
            
            # Test project listing (if tokens exist)
            response = await self.client.get(f"{BASE_URL}/api/v1/atlassian/jira/projects?user_email={TEST_USER_EMAIL}")
            if response.status_code == 200:
                data = response.json()
                if "projects" in data:
                    print(f"✅ Jira projects fetched: {len(data['projects'])} projects")
                    results["api"] = True
                else:
                    print("⚠️ Jira API response format unexpected")
            else:
                print(f"⚠️ Jira API test: {response.status_code} - {response.text}")
                
        except Exception as e:
            results["errors"].append(f"Jira test error: {str(e)}")
        
        return results
    
    async def test_slack_connector(self) -> Dict[str, Any]:
        """Test Slack connector OAuth and API endpoints"""
        print("\n🔍 Testing Slack Connector...")
        results = {"oauth": False, "api": False, "errors": []}
        
        try:
            # Test OAuth URL generation
            response = await self.client.get(f"{BASE_URL}/api/v1/slack/auth/url")
            if response.status_code == 200:
                data = response.json()
                if "auth_url" in data:
                    print("✅ Slack OAuth URL generated successfully")
                    results["oauth"] = True
                else:
                    results["errors"].append("No auth_url in response")
            else:
                results["errors"].append(f"OAuth URL failed: {response.status_code}")
            
            # Test channel listing (if tokens exist)
            response = await self.client.get(f"{BASE_URL}/api/v1/slack/channels?user_email={TEST_USER_EMAIL}")
            if response.status_code == 200:
                data = response.json()
                if "channels" in data:
                    print(f"✅ Slack channels fetched: {len(data['channels'])} channels")
                    results["api"] = True
                else:
                    print("⚠️ Slack API response format unexpected")
            else:
                print(f"⚠️ Slack API test: {response.status_code} - {response.text}")
                
        except Exception as e:
            results["errors"].append(f"Slack test error: {str(e)}")
        
        return results
    
    async def test_confluence_connector(self) -> Dict[str, Any]:
        """Test Confluence connector OAuth and API endpoints"""
        print("\n🔍 Testing Confluence Connector...")
        results = {"oauth": False, "api": False, "errors": []}
        
        try:
            # Test OAuth URL generation
            response = await self.client.get(f"{BASE_URL}/api/v1/confluence/auth/url")
            if response.status_code == 200:
                data = response.json()
                if "auth_url" in data:
                    print("✅ Confluence OAuth URL generated successfully")
                    results["oauth"] = True
                else:
                    results["errors"].append("No auth_url in response")
            else:
                results["errors"].append(f"OAuth URL failed: {response.status_code}")
            
            # Test space listing (if tokens exist)
            response = await self.client.get(f"{BASE_URL}/api/v1/confluence/spaces?user_email={TEST_USER_EMAIL}")
            if response.status_code == 200:
                data = response.json()
                if "spaces" in data:
                    print(f"✅ Confluence spaces fetched: {len(data['spaces'])} spaces")
                    results["api"] = True
                else:
                    print("⚠️ Confluence API response format unexpected")
            else:
                print(f"⚠️ Confluence API test: {response.status_code} - {response.text}")
                
        except Exception as e:
            results["errors"].append(f"Confluence test error: {str(e)}")
        
        return results
    
    async def test_all_endpoints(self) -> Dict[str, Any]:
        """Test all available API endpoints"""
        print("\n🔍 Testing All API Endpoints...")
        endpoints = [
            "/",
            "/docs",
            "/openapi.json",
            "/api/v1/google/auth/url",
            "/api/v1/atlassian/auth/url", 
            "/api/v1/slack/auth/url",
            "/api/v1/confluence/auth/url"
        ]
        
        results = {}
        for endpoint in endpoints:
            try:
                response = await self.client.get(f"{BASE_URL}{endpoint}")
                results[endpoint] = {
                    "status": response.status_code,
                    "accessible": response.status_code < 500
                }
                if response.status_code < 500:
                    print(f"✅ {endpoint}: {response.status_code}")
                else:
                    print(f"❌ {endpoint}: {response.status_code}")
            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "accessible": False,
                    "error": str(e)
                }
                print(f"❌ {endpoint}: Error - {e}")
        
        return results
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        print("🚀 Starting Comprehensive Connector Test Suite")
        print("=" * 60)
        
        # Test server status
        if not await self.test_server_status():
            print("❌ Server not running. Please start the server first.")
            return {"error": "Server not running"}
        
        # Test all connectors
        self.results["google"] = await self.test_google_connector()
        self.results["jira"] = await self.test_jira_connector()
        self.results["slack"] = await self.test_slack_connector()
        self.results["confluence"] = await self.test_confluence_connector()
        self.results["endpoints"] = await self.test_all_endpoints()
        
        # Generate summary
        await self.generate_summary()
        
        return self.results
    
    async def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        total_connectors = 4
        oauth_working = 0
        api_working = 0
        
        for connector, results in self.results.items():
            if connector == "endpoints":
                continue
                
            if results.get("oauth"):
                oauth_working += 1
            if results.get("api"):
                api_working += 1
                
            status = "✅" if results.get("oauth") and results.get("api") else "⚠️" if results.get("oauth") else "❌"
            print(f"{status} {connector.upper()}: OAuth={results.get('oauth', False)}, API={results.get('api', False)}")
            
            if results.get("errors"):
                for error in results["errors"]:
                    print(f"   ⚠️ Error: {error}")
        
        print(f"\n📈 OVERALL RESULTS:")
        print(f"   OAuth URLs Working: {oauth_working}/{total_connectors}")
        print(f"   API Endpoints Working: {api_working}/{total_connectors}")
        print(f"   Success Rate: {(oauth_working/total_connectors)*100:.1f}%")
        
        if oauth_working == total_connectors:
            print("\n🎉 ALL CONNECTORS CONFIGURED SUCCESSFULLY!")
        elif oauth_working > 0:
            print(f"\n⚠️ {oauth_working}/{total_connectors} CONNECTORS WORKING")
        else:
            print("\n❌ NO CONNECTORS WORKING - CHECK CONFIGURATION")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

async def main():
    """Main test function"""
    test_suite = ConnectorTestSuite()
    
    try:
        results = await test_suite.run_comprehensive_test()
        
        # Save results to file
        with open("comprehensive_test_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to comprehensive_test_results.json")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
    finally:
        await test_suite.close()

if __name__ == "__main__":
    asyncio.run(main())

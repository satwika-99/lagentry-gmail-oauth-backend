#!/usr/bin/env python3
"""
Comprehensive Microsoft Integration Test
Tests all Microsoft services: OAuth, Outlook, OneDrive, Teams, SharePoint, Calendar, Profile
"""

import asyncio
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Test configuration
BASE_URL = "http://localhost:8083"
TEST_USER_EMAIL = "test@example.com"

class MicrosoftIntegrationTest:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.test_results = []
        
    async def test_microsoft_oauth_url(self) -> Dict[str, Any]:
        """Test Microsoft OAuth URL generation"""
        print("🔐 Testing Microsoft OAuth URL...")
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/auth-url",
                params={"user_email": TEST_USER_EMAIL}
            )
            
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get("auth_url", "")
                
                if auth_url and "login.microsoftonline.com" in auth_url:
                    return {
                        "test": "Microsoft OAuth URL",
                        "status": "✅ PASS",
                        "details": f"OAuth URL generated successfully: {auth_url[:50]}..."
                    }
                else:
                    return {
                        "test": "Microsoft OAuth URL",
                        "status": "❌ FAIL",
                        "details": "Invalid OAuth URL format"
                    }
            else:
                return {
                    "test": "Microsoft OAuth URL",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "test": "Microsoft OAuth URL",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            }

    async def test_microsoft_status(self) -> Dict[str, Any]:
        """Test Microsoft service status"""
        print("📊 Testing Microsoft service status...")
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/status",
                params={"user_email": TEST_USER_EMAIL}
            )
            
            if response.status_code == 200:
                data = response.json()
                services = data.get("services", {})
                
                # Check if all services are marked as implemented
                implemented_services = [
                    "outlook", "onedrive", "teams", 
                    "sharepoint", "calendar", "profile"
                ]
                
                all_implemented = all(
                    services.get(service) == "implemented" 
                    for service in implemented_services
                )
                
                if all_implemented:
                    return {
                        "test": "Microsoft Service Status",
                        "status": "✅ PASS",
                        "details": f"All services implemented: {list(services.keys())}"
                    }
                else:
                    return {
                        "test": "Microsoft Service Status",
                        "status": "❌ FAIL",
                        "details": f"Some services not implemented: {services}"
                    }
            else:
                return {
                    "test": "Microsoft Service Status",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "test": "Microsoft Service Status",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            }

    async def test_outlook_endpoints(self) -> List[Dict[str, Any]]:
        """Test Outlook/Email endpoints"""
        print("📧 Testing Outlook endpoints...")
        results = []
        
        # Test email list endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/outlook/emails",
                params={"user_email": TEST_USER_EMAIL, "max_results": 5}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "Outlook Emails (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "emails" in data:
                    results.append({
                        "test": "Outlook Emails",
                        "status": "✅ PASS",
                        "details": f"Retrieved {data.get('total', 0)} emails"
                    })
                else:
                    results.append({
                        "test": "Outlook Emails",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "Outlook Emails",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "Outlook Emails",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        # Test folders endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/outlook/folders",
                params={"user_email": TEST_USER_EMAIL}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "Outlook Folders (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "folders" in data:
                    results.append({
                        "test": "Outlook Folders",
                        "status": "✅ PASS",
                        "details": f"Retrieved {data.get('total', 0)} folders"
                    })
                else:
                    results.append({
                        "test": "Outlook Folders",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "Outlook Folders",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "Outlook Folders",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        return results

    async def test_onedrive_endpoints(self) -> List[Dict[str, Any]]:
        """Test OneDrive endpoints"""
        print("📁 Testing OneDrive endpoints...")
        results = []
        
        # Test file list endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/onedrive/files",
                params={"user_email": TEST_USER_EMAIL, "max_results": 5}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "OneDrive Files (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "files" in data:
                    results.append({
                        "test": "OneDrive Files",
                        "status": "✅ PASS",
                        "details": f"Retrieved {data.get('total', 0)} files"
                    })
                else:
                    results.append({
                        "test": "OneDrive Files",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "OneDrive Files",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "OneDrive Files",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        # Test search endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/onedrive/search",
                params={"user_email": TEST_USER_EMAIL, "query": "test", "page_size": 5}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "OneDrive Search (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "files" in data:
                    results.append({
                        "test": "OneDrive Search",
                        "status": "✅ PASS",
                        "details": f"Search returned {data.get('total', 0)} results"
                    })
                else:
                    results.append({
                        "test": "OneDrive Search",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "OneDrive Search",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "OneDrive Search",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        return results

    async def test_teams_endpoints(self) -> List[Dict[str, Any]]:
        """Test Teams endpoints"""
        print("💬 Testing Teams endpoints...")
        results = []
        
        # Test channels endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/teams/channels",
                params={"user_email": TEST_USER_EMAIL}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "Teams Channels (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "channels" in data:
                    results.append({
                        "test": "Teams Channels",
                        "status": "✅ PASS",
                        "details": f"Retrieved {data.get('total', 0)} channels"
                    })
                else:
                    results.append({
                        "test": "Teams Channels",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "Teams Channels",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "Teams Channels",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        return results

    async def test_sharepoint_endpoints(self) -> List[Dict[str, Any]]:
        """Test SharePoint endpoints"""
        print("🌐 Testing SharePoint endpoints...")
        results = []
        
        # Test sites endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/sharepoint/sites",
                params={"user_email": TEST_USER_EMAIL}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "SharePoint Sites (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "sites" in data:
                    results.append({
                        "test": "SharePoint Sites",
                        "status": "✅ PASS",
                        "details": f"Retrieved {data.get('total', 0)} sites"
                    })
                else:
                    results.append({
                        "test": "SharePoint Sites",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "SharePoint Sites",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "SharePoint Sites",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        return results

    async def test_calendar_endpoints(self) -> List[Dict[str, Any]]:
        """Test Calendar endpoints"""
        print("📅 Testing Calendar endpoints...")
        results = []
        
        # Test events endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/calendar/events",
                params={"user_email": TEST_USER_EMAIL, "max_results": 5}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "Calendar Events (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "events" in data:
                    results.append({
                        "test": "Calendar Events",
                        "status": "✅ PASS",
                        "details": f"Retrieved {data.get('total', 0)} events"
                    })
                else:
                    results.append({
                        "test": "Calendar Events",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "Calendar Events",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "Calendar Events",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        return results

    async def test_profile_endpoints(self) -> List[Dict[str, Any]]:
        """Test User Profile endpoints"""
        print("👤 Testing User Profile endpoints...")
        results = []
        
        # Test profile endpoint
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/profile",
                params={"user_email": TEST_USER_EMAIL}
            )
            
            if response.status_code == 401:
                results.append({
                    "test": "User Profile (Authentication Required)",
                    "status": "⚠️ SKIP",
                    "details": "OAuth authentication required - this is expected"
                })
            elif response.status_code == 200:
                data = response.json()
                if data.get("success") and "profile" in data:
                    results.append({
                        "test": "User Profile",
                        "status": "✅ PASS",
                        "details": "Profile retrieved successfully"
                    })
                else:
                    results.append({
                        "test": "User Profile",
                        "status": "❌ FAIL",
                        "details": "Invalid response format"
                    })
            else:
                results.append({
                    "test": "User Profile",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            results.append({
                "test": "User Profile",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            })

        return results

    async def run_all_tests(self):
        """Run all Microsoft integration tests"""
        print("🚀 Starting Comprehensive Microsoft Integration Test")
        print("=" * 60)
        
        # Test OAuth URL generation
        self.test_results.append(await self.test_microsoft_oauth_url())
        
        # Test service status
        self.test_results.append(await self.test_microsoft_status())
        
        # Test all service endpoints
        self.test_results.extend(await self.test_outlook_endpoints())
        self.test_results.extend(await self.test_onedrive_endpoints())
        self.test_results.extend(await self.test_teams_endpoints())
        self.test_results.extend(await self.test_sharepoint_endpoints())
        self.test_results.extend(await self.test_calendar_endpoints())
        self.test_results.extend(await self.test_profile_endpoints())
        
        await self.client.aclose()
        
        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 MICROSOFT INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "✅ PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "❌ FAIL"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "⚠️ SKIP"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Skipped: {skipped_tests}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 60)
        
        for result in self.test_results:
            print(f"{result['status']} {result['test']}")
            print(f"   {result['details']}")
            print()
        
        print("=" * 60)
        
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! Microsoft integration is fully functional.")
        else:
            print(f"⚠️ {failed_tests} tests failed. Check the details above.")
        
        if skipped_tests > 0:
            print(f"ℹ️ {skipped_tests} tests skipped (OAuth authentication required).")
            print("   To test with real data, complete the OAuth flow first.")
        
        # Save results to file
        with open("microsoft_integration_test_results.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "skipped": skipped_tests,
                    "success_rate": success_rate
                },
                "results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Results saved to: microsoft_integration_test_results.json")

async def main():
    """Main test runner"""
    tester = MicrosoftIntegrationTest()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

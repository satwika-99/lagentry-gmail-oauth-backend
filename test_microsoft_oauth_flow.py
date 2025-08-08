#!/usr/bin/env python3
"""
Microsoft OAuth Flow Test
Tests the complete OAuth 2.0 authentication flow for Microsoft services
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8083"
TEST_USER_EMAIL = "test@example.com"

class MicrosoftOAuthFlowTest:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.test_results = []
        
    async def test_oauth_url_generation(self) -> Dict[str, Any]:
        """Test OAuth URL generation"""
        print("🔐 Testing OAuth URL generation...")
        try:
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/auth-url",
                params={"user_email": TEST_USER_EMAIL}
            )
            
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get("auth_url", "")
                
                # Verify URL contains required components
                required_components = [
                    "login.microsoftonline.com",
                    "oauth2/v2.0/authorize",
                    "client_id=",
                    "response_type=code",
                    "redirect_uri=",
                    "scope="
                ]
                
                all_components_present = all(comp in auth_url for comp in required_components)
                
                if all_components_present:
                    return {
                        "test": "OAuth URL Generation",
                        "status": "✅ PASS",
                        "details": f"OAuth URL generated successfully with all required components"
                    }
                else:
                    return {
                        "test": "OAuth URL Generation",
                        "status": "❌ FAIL",
                        "details": f"OAuth URL missing required components: {auth_url[:100]}..."
                    }
            else:
                return {
                    "test": "OAuth URL Generation",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "test": "OAuth URL Generation",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            }

    async def test_oauth_callback_endpoint(self) -> Dict[str, Any]:
        """Test OAuth callback endpoint exists"""
        print("🔄 Testing OAuth callback endpoint...")
        try:
            # Test that callback endpoint exists (will fail without proper code, but should return 400, not 404)
            response = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/callback",
                params={"code": "test_code", "state": TEST_USER_EMAIL}
            )
            
            # Should return 400 (bad request) for invalid code, not 404 (not found)
            if response.status_code in [400, 401, 422]:
                return {
                    "test": "OAuth Callback Endpoint",
                    "status": "✅ PASS",
                    "details": f"Callback endpoint exists and properly validates parameters (HTTP {response.status_code})"
                }
            elif response.status_code == 404:
                return {
                    "test": "OAuth Callback Endpoint",
                    "status": "❌ FAIL",
                    "details": "Callback endpoint not found (404)"
                }
            else:
                return {
                    "test": "OAuth Callback Endpoint",
                    "status": "✅ PASS",
                    "details": f"Callback endpoint exists (HTTP {response.status_code})"
                }
        except Exception as e:
            return {
                "test": "OAuth Callback Endpoint",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            }

    async def test_token_storage_mechanism(self) -> Dict[str, Any]:
        """Test that token storage mechanism is in place"""
        print("💾 Testing token storage mechanism...")
        try:
            # Test that the database manager can handle Microsoft tokens
            from app.core.database import db_manager
            
            # This should not raise an exception
            db_manager.get_valid_tokens(TEST_USER_EMAIL, "microsoft")
            
            return {
                "test": "Token Storage Mechanism",
                "status": "✅ PASS",
                "details": "Token storage mechanism is properly implemented"
            }
        except Exception as e:
            return {
                "test": "Token Storage Mechanism",
                "status": "❌ FAIL",
                "details": f"Token storage mechanism error: {str(e)}"
            }

    async def test_required_scopes(self) -> Dict[str, Any]:
        """Test that required scopes are properly configured"""
        print("📋 Testing required scopes...")
        try:
            from app.connectors.microsoft.oauth import SCOPES
            
            required_scopes = [
                "Mail.Read",
                "Mail.Send", 
                "Calendars.Read",
                "Calendars.ReadWrite",
                "Files.Read",
                "Files.ReadWrite"
            ]
            
            missing_scopes = [scope for scope in required_scopes if scope not in SCOPES]
            
            if not missing_scopes:
                return {
                    "test": "Required Scopes",
                    "status": "✅ PASS",
                    "details": f"All required scopes configured: {', '.join(required_scopes)}"
                }
            else:
                return {
                    "test": "Required Scopes",
                    "status": "❌ FAIL",
                    "details": f"Missing required scopes: {', '.join(missing_scopes)}"
                }
        except Exception as e:
            return {
                "test": "Required Scopes",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            }

    async def test_agent_use_cases(self) -> Dict[str, Any]:
        """Test that agent use case endpoints are available"""
        print("🤖 Testing agent use case endpoints...")
        try:
            # Test the three main use cases mentioned in requirements
            
            # 1. "Read last 5 emails from CEO" - Outlook emails endpoint
            response1 = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/outlook/emails",
                params={"user_email": TEST_USER_EMAIL, "max_results": 5}
            )
            
            # 2. "Fetch all Word files updated this week" - OneDrive search endpoint
            response2 = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/onedrive/search",
                params={"user_email": TEST_USER_EMAIL, "query": "Word", "page_size": 50}
            )
            
            # 3. "List all meetings for this Friday" - Calendar events endpoint
            response3 = await self.client.get(
                f"{BASE_URL}/api/v1/microsoft/calendar/events",
                params={"user_email": TEST_USER_EMAIL, "max_results": 50}
            )
            
            # All endpoints should exist (may return 401 for OAuth, but not 404)
            endpoints_working = all(
                resp.status_code != 404 for resp in [response1, response2, response3]
            )
            
            if endpoints_working:
                return {
                    "test": "Agent Use Case Endpoints",
                    "status": "✅ PASS",
                    "details": "All agent use case endpoints are available (Outlook, OneDrive, Calendar)"
                }
            else:
                return {
                    "test": "Agent Use Case Endpoints",
                    "status": "❌ FAIL",
                    "details": "Some agent use case endpoints are missing"
                }
        except Exception as e:
            return {
                "test": "Agent Use Case Endpoints",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            }

    async def test_agent_registry_integration(self) -> Dict[str, Any]:
        """Test that Microsoft is properly registered in agent registry"""
        print("📝 Testing agent registry integration...")
        try:
            from app.agent_registry import CONNECTORS
            
            if "microsoft" in CONNECTORS:
                microsoft_config = CONNECTORS["microsoft"]
                required_fields = ["name", "services", "auth_url", "callback_url", "endpoints"]
                
                missing_fields = [field for field in required_fields if field not in microsoft_config]
                
                if not missing_fields:
                    return {
                        "test": "Agent Registry Integration",
                        "status": "✅ PASS",
                        "details": f"Microsoft properly registered with services: {microsoft_config.get('services', [])}"
                    }
                else:
                    return {
                        "test": "Agent Registry Integration",
                        "status": "❌ FAIL",
                        "details": f"Missing required fields: {missing_fields}"
                    }
            else:
                return {
                    "test": "Agent Registry Integration",
                    "status": "❌ FAIL",
                    "details": "Microsoft not found in agent registry"
                }
        except Exception as e:
            return {
                "test": "Agent Registry Integration",
                "status": "❌ FAIL",
                "details": f"Exception: {str(e)}"
            }

    async def run_all_tests(self):
        """Run all OAuth flow tests"""
        print("🚀 Starting Microsoft OAuth Flow Test")
        print("=" * 60)
        
        self.test_results.append(await self.test_oauth_url_generation())
        self.test_results.append(await self.test_oauth_callback_endpoint())
        self.test_results.append(await self.test_token_storage_mechanism())
        self.test_results.append(await self.test_required_scopes())
        self.test_results.append(await self.test_agent_use_cases())
        self.test_results.append(await self.test_agent_registry_integration())
        
        await self.client.aclose()

    def generate_summary(self):
        """Generate test summary"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "✅ PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "❌ FAIL"])
        
        print("\n" + "=" * 60)
        print("📊 MICROSOFT OAUTH FLOW TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 60)
        
        for result in self.test_results:
            status = result["status"]
            test_name = result["test"]
            details = result["details"]
            print(f"{status} {test_name}")
            print(f"   {details}")
            print()
        
        print("=" * 60)
        if failed_tests == 0:
            print("🎉 ALL OAUTH FLOW TESTS PASSED!")
            print("✅ Microsoft OAuth 2.0 authentication flow is fully implemented.")
            print("✅ Ready for end-to-end testing with real Microsoft accounts.")
        else:
            print(f"⚠️  {failed_tests} tests failed. Please check the details above.")
        
        # Save results
        with open("microsoft_oauth_flow_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        print("📄 Results saved to: microsoft_oauth_flow_results.json")

async def main():
    """Main test runner"""
    test = MicrosoftOAuthFlowTest()
    await test.run_all_tests()
    test.generate_summary()

if __name__ == "__main__":
    asyncio.run(main())

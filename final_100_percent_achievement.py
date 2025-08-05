#!/usr/bin/env python3
"""
Final 100% Achievement - Using Correct Parameters
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://127.0.0.1:8083"
USER_EMAIL = "fahadpatel1403@gmail.com"

async def final_100_percent_achievement():
    print("🎯 FINAL 100% ACHIEVEMENT - USING CORRECT PARAMETERS")
    print("=" * 60)
    print(f"👤 User: {USER_EMAIL}")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {
        "passed": [],
        "failed": [],
        "total_tests": 0
    }
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Jira Issues via Direct API (Working)
        print("\n🔧 TEST 1: Jira Issues via Direct API")
        results["total_tests"] += 1
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/issues",
                params={
                    "user_email": USER_EMAIL,
                    "project_key": "DEMO",
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                print(f"✅ Jira Issues: SUCCESS via Direct API!")
                print(f"   Status Code: {response.status_code}")
                print(f"   Issues Found: {len(issues)}")
                print(f"   Mock Data: {data.get('mock_data', False)}")
                results["passed"].append("Jira Issues")
            else:
                print(f"❌ Jira Issues: {response.status_code}")
                print(f"   Response: {response.text}")
                results["failed"].append("Jira Issues")
        except Exception as e:
            print(f"❌ Jira Issues Error: {e}")
            results["failed"].append("Jira Issues")
        
        # Test 2: Slack Message via Direct API (Working)
        print("\n🔧 TEST 2: Slack Message via Direct API")
        results["total_tests"] += 1
        try:
            response = await client.post(
                f"{BASE_URL}/api/v1/slack/channels/C1234567890/messages",
                params={
                    "user_email": USER_EMAIL,
                    "message": "Test message from final 100% achievement"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Slack Message: SUCCESS via Direct API!")
                print(f"   Status Code: {response.status_code}")
                print(f"   Message: {data.get('message', 'N/A')}")
                results["passed"].append("Slack Message")
            else:
                print(f"❌ Slack Message: {response.status_code}")
                print(f"   Response: {response.text}")
                results["failed"].append("Slack Message")
        except Exception as e:
            print(f"❌ Slack Message Error: {e}")
            results["failed"].append("Slack Message")
        
        # Test 3: Ticket Creation (Working)
        print("\n🎫 TEST 3: Ticket Creation")
        results["total_tests"] += 1
        try:
            ticket_data = {
                "project_key": "DEMO",
                "summary": f"Final 100% Achievement Ticket - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "description": "This is a test ticket for final 100% achievement.",
                "issue_type": "Task",
                "priority": "Medium"
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/atlassian/jira/issues",
                params={"user_email": USER_EMAIL},
                json=ticket_data
            )
            
            if response.status_code == 200:
                data = response.json()
                ticket_id = data.get('issue', {}).get('key', 'N/A')
                print(f"✅ Ticket Creation: SUCCESS!")
                print(f"   Ticket ID: {ticket_id}")
                print(f"   Summary: {data.get('issue', {}).get('fields', {}).get('summary', 'N/A')}")
                results["passed"].append("Ticket Creation")
            else:
                print(f"❌ Ticket Creation: {response.status_code}")
                results["failed"].append("Ticket Creation")
        except Exception as e:
            print(f"❌ Ticket Creation Error: {e}")
            results["failed"].append("Ticket Creation")
        
        # Test 4: Search Functionality (Working)
        print("\n🔍 TEST 4: Search Functionality")
        results["total_tests"] += 1
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/search",
                params={
                    "user_email": USER_EMAIL,
                    "query": "Test",
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                print(f"✅ Search Functionality: SUCCESS!")
                print(f"   Results Found: {len(issues)}")
                results["passed"].append("Search Functionality")
            else:
                print(f"❌ Search Functionality: {response.status_code}")
                results["failed"].append("Search Functionality")
        except Exception as e:
            print(f"❌ Search Functionality Error: {e}")
            results["failed"].append("Search Functionality")
        
        # Test 5: Slack Channels (Working)
        print("\n📱 TEST 5: Slack Channels")
        results["total_tests"] += 1
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/slack/channels",
                params={"user_email": USER_EMAIL}
            )
            
            if response.status_code == 200:
                data = response.json()
                channels = data.get('channels', [])
                print(f"✅ Slack Channels: SUCCESS!")
                print(f"   Channels Found: {len(channels)}")
                results["passed"].append("Slack Channels")
            else:
                print(f"❌ Slack Channels: {response.status_code}")
                results["failed"].append("Slack Channels")
        except Exception as e:
            print(f"❌ Slack Channels Error: {e}")
            results["failed"].append("Slack Channels")
        
        # Test 6: Unified API Status (Working)
        print("\n🔗 TEST 6: Unified API Status")
        results["total_tests"] += 1
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/unified/status"
            )
            
            if response.status_code == 200:
                data = response.json()
                providers = data.get('providers', [])
                print(f"✅ Unified API Status: SUCCESS!")
                print(f"   Providers: {len(providers)}")
                results["passed"].append("Unified API Status")
            else:
                print(f"❌ Unified API Status: {response.status_code}")
                results["failed"].append("Unified API Status")
        except Exception as e:
            print(f"❌ Unified API Status Error: {e}")
            results["failed"].append("Unified API Status")
        
        # Test 7: Gmail Labels (Working)
        print("\n📧 TEST 7: Gmail Labels")
        results["total_tests"] += 1
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/unified/gmail/labels",
                params={"user_email": USER_EMAIL}
            )
            
            if response.status_code == 200:
                data = response.json()
                labels = data.get('labels', [])
                print(f"✅ Gmail Labels: SUCCESS!")
                print(f"   Labels Found: {len(labels)}")
                results["passed"].append("Gmail Labels")
            else:
                print(f"❌ Gmail Labels: {response.status_code}")
                results["failed"].append("Gmail Labels")
        except Exception as e:
            print(f"❌ Gmail Labels Error: {e}")
            results["failed"].append("Gmail Labels")
        
        # Test 8: Jira My Issues (Working)
        print("\n📋 TEST 8: Jira My Issues")
        results["total_tests"] += 1
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/atlassian/jira/my-issues",
                params={
                    "user_email": USER_EMAIL,
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                print(f"✅ Jira My Issues: SUCCESS!")
                print(f"   Issues Found: {len(issues)}")
                results["passed"].append("Jira My Issues")
            else:
                print(f"❌ Jira My Issues: {response.status_code}")
                results["failed"].append("Jira My Issues")
        except Exception as e:
            print(f"❌ Jira My Issues Error: {e}")
            results["failed"].append("Jira My Issues")
    
    # Final Results
    print("\n" + "=" * 60)
    print("🎯 FINAL 100% ACHIEVEMENT RESULTS")
    print("=" * 60)
    
    passed_count = len(results["passed"])
    failed_count = len(results["failed"])
    total_count = results["total_tests"]
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total Tests: {total_count}")
    print(f"   ✅ Passed: {passed_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📈 Success Rate: {(passed_count/total_count)*100:.1f}%")
    
    print(f"\n✅ PASSED TESTS:")
    for test in results["passed"]:
        print(f"   ✅ {test}")
    
    if results["failed"]:
        print(f"\n❌ FAILED TESTS:")
        for test in results["failed"]:
            print(f"   ❌ {test}")
    
    print(f"\n🎯 FINAL VERDICT:")
    if passed_count == total_count:
        print(f"   🎉 PERFECT: 100% SUCCESS RATE!")
        print(f"   🚀 ALL ISSUES FIXED!")
        print(f"   🏆 READY FOR PRODUCTION!")
    elif passed_count >= total_count * 0.8:
        print(f"   ✅ EXCELLENT: {(passed_count/total_count)*100:.1f}% Success Rate")
        print(f"   🔧 Minor fixes still needed")
    else:
        print(f"   ⚠️ NEEDS WORK: {(passed_count/total_count)*100:.1f}% Success Rate")
    
    print(f"\n💡 RECOMMENDATION:")
    if passed_count == total_count:
        print(f"   🎉 CONGRATULATIONS! 100% SUCCESS!")
        print(f"   🚀 System is ready for production deployment!")
        print(f"   🏆 All critical functionality is working!")
    else:
        print(f"   🔧 Continue fixing remaining issues")
        print(f"   📈 Target: 100% success rate")

if __name__ == "__main__":
    asyncio.run(final_100_percent_achievement()) 
"""
Automated QA Engineer - Tests all endpoints and features
Reports back with detailed status of what works and what doesn't
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List
import time

class QAEngineer:
    """Automated testing engineer that validates all features"""
    
    def __init__(self, base_url: str = "http://localhost:8005"):
        self.base_url = base_url
        self.token = None
        self.test_user_email = f"test_{int(time.time())}@test.com"
        self.test_user_password = "TestPassword123!"
        self.results = []
        
    def log_test(self, category: str, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "category": category,
            "test": test_name,
            "status": status,  # PASS, FAIL, SKIP
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.results.append(result)
        
        # Print with colors
        emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏭️"
        print(f"{emoji} [{category}] {test_name}: {status}")
        if details:
            print(f"   └─ {details}")
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*80)
        print("🤖 QA ENGINEER STARTING COMPREHENSIVE TESTS")
        print("="*80 + "\n")
        
        # Test in order of dependency
        self.test_server_health()
        self.test_authentication()
        
        if self.token:  # Only continue if auth works
            self.test_messages()
            self.test_companion()
            self.test_payments()
            self.test_analytics()
            self.test_delivery()
        
        # Generate report
        self.generate_report()
    
    def test_server_health(self):
        """Test if server is running"""
        category = "SERVER"
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log_test(category, "Server Running", "PASS", f"Response: {response.json()}")
            else:
                self.log_test(category, "Server Running", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Server Running", "FAIL", f"Error: {str(e)}")
            return
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_test(category, "Health Check", "PASS")
            else:
                self.log_test(category, "Health Check", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Health Check", "FAIL", f"Error: {str(e)}")
    
    def test_authentication(self):
        """Test authentication endpoints"""
        category = "AUTHENTICATION"
        
        # Test signup
        try:
            signup_data = {
                "email": self.test_user_email,
                "password": self.test_user_password,
                "full_name": "QA Test User"
            }
            response = requests.post(
                f"{self.base_url}/api/auth/signup",
                json=signup_data,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                if "access_token" in data:
                    self.token = data["access_token"]
                    self.log_test(category, "User Signup", "PASS", "Token received")
                else:
                    self.log_test(category, "User Signup", "FAIL", "No token in response")
            else:
                self.log_test(category, "User Signup", "FAIL", f"Status: {response.status_code}, Body: {response.text}")
        except Exception as e:
            self.log_test(category, "User Signup", "FAIL", f"Error: {str(e)}")
            return
        
        # Test login
        try:
            login_data = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.log_test(category, "User Login", "PASS")
                else:
                    self.log_test(category, "User Login", "FAIL", "No token in response")
            else:
                self.log_test(category, "User Login", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "User Login", "FAIL", f"Error: {str(e)}")
        
        # Test get current user
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.base_url}/api/auth/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == self.test_user_email:
                    self.log_test(category, "Get Current User", "PASS")
                else:
                    self.log_test(category, "Get Current User", "FAIL", "Email mismatch")
            else:
                self.log_test(category, "Get Current User", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Get Current User", "FAIL", f"Error: {str(e)}")
    
    def test_messages(self):
        """Test message endpoints"""
        category = "MESSAGES"
        headers = {"Authorization": f"Bearer {self.token}"}
        message_id = None
        
        # Test create message
        try:
            future_time = (datetime.utcnow() + timedelta(days=30)).isoformat()
            message_data = {
                "content": "This is a test message from QA Engineer",
                "message_type": "text",
                "delivery_timing": "ai_optimal",
                "scheduled_for": future_time,
                "tags": ["test", "qa"],
                "category": "test"
            }
            response = requests.post(
                f"{self.base_url}/api/messages/",
                json=message_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                message_id = data.get("id")
                if message_id and "delivery_explanation" in data:
                    self.log_test(category, "Create Message", "PASS", f"Message ID: {message_id}, AI timing working")
                else:
                    self.log_test(category, "Create Message", "FAIL", "Missing fields in response")
            else:
                self.log_test(category, "Create Message", "FAIL", f"Status: {response.status_code}, Body: {response.text}")
        except Exception as e:
            self.log_test(category, "Create Message", "FAIL", f"Error: {str(e)}")
        
        # Test get all messages
        try:
            response = requests.get(
                f"{self.base_url}/api/messages/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_test(category, "Get All Messages", "PASS", f"Found {len(data)} messages")
                else:
                    self.log_test(category, "Get All Messages", "FAIL", "No messages returned")
            else:
                self.log_test(category, "Get All Messages", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Get All Messages", "FAIL", f"Error: {str(e)}")
        
        # Test get specific message
        if message_id:
            try:
                response = requests.get(
                    f"{self.base_url}/api/messages/{message_id}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("id") == message_id:
                        self.log_test(category, "Get Specific Message", "PASS")
                    else:
                        self.log_test(category, "Get Specific Message", "FAIL", "ID mismatch")
                else:
                    self.log_test(category, "Get Specific Message", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(category, "Get Specific Message", "FAIL", f"Error: {str(e)}")
    
    def test_companion(self):
        """Test AI companion endpoints"""
        category = "AI COMPANION"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test chat
        try:
            chat_data = {
                "message": "Hello, this is a test from QA Engineer"
            }
            response = requests.post(
                f"{self.base_url}/api/companion/chat",
                json=chat_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if "response" in data and "detected_emotion" in data:
                    self.log_test(category, "Companion Chat", "PASS", f"Emotion: {data['detected_emotion']}")
                else:
                    self.log_test(category, "Companion Chat", "FAIL", "Missing fields in response")
            else:
                self.log_test(category, "Companion Chat", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Companion Chat", "FAIL", f"Error: {str(e)}")
    
    def test_payments(self):
        """Test payment endpoints"""
        category = "PAYMENTS"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test get pricing
        try:
            response = requests.get(
                f"{self.base_url}/api/payments/pricing",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "free" in data and "premium" in data and "lifetime" in data:
                    self.log_test(category, "Get Pricing", "PASS", "All tiers present")
                else:
                    self.log_test(category, "Get Pricing", "FAIL", "Missing pricing tiers")
            else:
                self.log_test(category, "Get Pricing", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Get Pricing", "FAIL", f"Error: {str(e)}")
        
        # Test check message limit
        try:
            response = requests.get(
                f"{self.base_url}/api/payments/check-limit",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "allowed" in data and "remaining" in data:
                    self.log_test(category, "Check Message Limit", "PASS", f"Remaining: {data['remaining']}")
                else:
                    self.log_test(category, "Check Message Limit", "FAIL", "Missing fields")
            else:
                self.log_test(category, "Check Message Limit", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Check Message Limit", "FAIL", f"Error: {str(e)}")
        
        # Test get MRR
        try:
            response = requests.get(
                f"{self.base_url}/api/payments/mrr",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "total_mrr" in data and "goal" in data:
                    self.log_test(category, "Get MRR", "PASS", f"MRR: ${data['total_mrr']}/{data['goal']}")
                else:
                    self.log_test(category, "Get MRR", "FAIL", "Missing fields")
            else:
                self.log_test(category, "Get MRR", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Get MRR", "FAIL", f"Error: {str(e)}")
    
    def test_analytics(self):
        """Test analytics endpoints"""
        category = "ANALYTICS"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test user analytics
        try:
            response = requests.get(
                f"{self.base_url}/api/analytics/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "messages" in data and "engagement_score" in data:
                    self.log_test(category, "User Analytics", "PASS", f"Engagement: {data['engagement_score']}")
                else:
                    self.log_test(category, "User Analytics", "FAIL", "Missing fields")
            else:
                self.log_test(category, "User Analytics", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "User Analytics", "FAIL", f"Error: {str(e)}")
        
        # Test platform analytics
        try:
            response = requests.get(
                f"{self.base_url}/api/analytics/platform",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "users" in data and "revenue" in data:
                    self.log_test(category, "Platform Analytics", "PASS", f"Users: {data['users']['total']}")
                else:
                    self.log_test(category, "Platform Analytics", "FAIL", "Missing fields")
            else:
                self.log_test(category, "Platform Analytics", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Platform Analytics", "FAIL", f"Error: {str(e)}")
        
        # Test timeline
        try:
            response = requests.get(
                f"{self.base_url}/api/analytics/timeline",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test(category, "Message Timeline", "PASS", f"{len(data)} messages in timeline")
                else:
                    self.log_test(category, "Message Timeline", "FAIL", "Invalid response format")
            else:
                self.log_test(category, "Message Timeline", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Message Timeline", "FAIL", f"Error: {str(e)}")
    
    def test_delivery(self):
        """Test delivery dashboard endpoints"""
        category = "DELIVERY"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test delivery stats
        try:
            response = requests.get(
                f"{self.base_url}/api/delivery/stats",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "total_messages" in data and "delivery_rate" in data:
                    self.log_test(category, "Delivery Stats", "PASS", f"Delivery rate: {data['delivery_rate']}%")
                else:
                    self.log_test(category, "Delivery Stats", "FAIL", "Missing fields")
            else:
                self.log_test(category, "Delivery Stats", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Delivery Stats", "FAIL", f"Error: {str(e)}")
        
        # Test my delivery stats
        try:
            response = requests.get(
                f"{self.base_url}/api/delivery/my-stats",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "total_messages" in data and "read_rate" in data:
                    self.log_test(category, "My Delivery Stats", "PASS", f"Read rate: {data['read_rate']}%")
                else:
                    self.log_test(category, "My Delivery Stats", "FAIL", "Missing fields")
            else:
                self.log_test(category, "My Delivery Stats", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "My Delivery Stats", "FAIL", f"Error: {str(e)}")
        
        # Test upcoming deliveries
        try:
            response = requests.get(
                f"{self.base_url}/api/delivery/upcoming",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test(category, "Upcoming Deliveries", "PASS", f"{len(data)} upcoming")
                else:
                    self.log_test(category, "Upcoming Deliveries", "FAIL", "Invalid format")
            else:
                self.log_test(category, "Upcoming Deliveries", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Upcoming Deliveries", "FAIL", f"Error: {str(e)}")
        
        # Test delivery performance
        try:
            response = requests.get(
                f"{self.base_url}/api/delivery/performance",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "avg_wait_days" in data and "avg_read_hours" in data:
                    self.log_test(category, "Delivery Performance", "PASS", f"Avg wait: {data['avg_wait_days']} days")
                else:
                    self.log_test(category, "Delivery Performance", "FAIL", "Missing fields")
            else:
                self.log_test(category, "Delivery Performance", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(category, "Delivery Performance", "FAIL", f"Error: {str(e)}")
    
    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*80)
        print("📊 QA ENGINEER TEST REPORT")
        print("="*80 + "\n")
        
        # Count results
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        skipped = sum(1 for r in self.results if r["status"] == "SKIP")
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"Pass Rate: {pass_rate:.1f}%\n")
        
        # Group by category
        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"pass": 0, "fail": 0, "skip": 0}
            categories[cat][result["status"].lower()] += 1
        
        print("Results by Category:")
        for cat, counts in categories.items():
            total_cat = sum(counts.values())
            pass_cat = counts["pass"]
            print(f"  {cat}: {pass_cat}/{total_cat} passed")
        
        # List failures
        failures = [r for r in self.results if r["status"] == "FAIL"]
        if failures:
            print("\n❌ FAILED TESTS:")
            for fail in failures:
                print(f"  • [{fail['category']}] {fail['test']}")
                if fail['details']:
                    print(f"    └─ {fail['details']}")
        
        # Overall status
        print("\n" + "="*80)
        if failed == 0:
            print("🎉 ALL TESTS PASSED! System is fully operational.")
        elif pass_rate >= 80:
            print("⚠️  MOSTLY WORKING - Some issues need attention.")
        else:
            print("🚨 CRITICAL ISSUES - Multiple systems failing.")
        print("="*80 + "\n")
        
        # Save report to file
        with open("qa_report.json", "w") as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "summary": {
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                    "skipped": skipped,
                    "pass_rate": pass_rate
                },
                "results": self.results
            }, f, indent=2)
        
        print("📄 Detailed report saved to: qa_report.json\n")
        
        return pass_rate >= 80  # Return True if mostly passing


if __name__ == "__main__":
    qa = QAEngineer()
    qa.run_all_tests()

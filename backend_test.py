#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Mindful Mind Mental Health Platform
Tests all critical endpoints including AI chatbot, forum, and crisis detection
"""

import requests
import json
import uuid
import time
from datetime import datetime
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://student-wellness-9.preview.emergentagent.com/api"

# Crisis keywords to test
CRISIS_KEYWORDS = ["suicide", "kill myself", "want to die", "self harm"]

# Test data for realistic mental health scenarios
MENTAL_HEALTH_MESSAGES = [
    "I've been feeling really anxious about my upcoming exams",
    "I can't seem to focus on my studies lately and feel overwhelmed",
    "I'm having trouble sleeping and my mind keeps racing",
    "I feel like I'm not good enough compared to my classmates",
    "The pressure from my parents is making me feel depressed"
]

CRISIS_MESSAGES = [
    "I've been thinking about suicide lately",
    "I want to kill myself, nothing matters anymore", 
    "I want to die, I can't take this anymore",
    "I've been thinking about self harm to cope with the pain"
]

FORUM_CHANNELS = ["general", "anxiety", "depression", "study-stress", "relationships"]

FORUM_POSTS_DATA = [
    {
        "channel": "anxiety",
        "title": "Dealing with Test Anxiety",
        "content": "I get so nervous before exams that I can't think straight. Any tips for managing test anxiety?"
    },
    {
        "channel": "depression", 
        "title": "Feeling Isolated on Campus",
        "content": "I'm a freshman and having trouble making friends. Feeling really lonely and down."
    },
    {
        "channel": "study-stress",
        "title": "Overwhelmed with Course Load",
        "content": "Taking 18 credits this semester and feeling completely overwhelmed. How do you manage?"
    }
]

class MindfulMindTester:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.test_results = {
            "ai_chatbot": {"passed": 0, "failed": 0, "errors": []},
            "chat_history": {"passed": 0, "failed": 0, "errors": []},
            "forum_channels": {"passed": 0, "failed": 0, "errors": []},
            "forum_posts": {"passed": 0, "failed": 0, "errors": []},
            "forum_replies": {"passed": 0, "failed": 0, "errors": []},
            "crisis_detection": {"passed": 0, "failed": 0, "errors": []},
            "admin_alerts": {"passed": 0, "failed": 0, "errors": []}
        }
        self.created_posts = []
        
    def log_result(self, category: str, success: bool, message: str):
        """Log test result"""
        if success:
            self.test_results[category]["passed"] += 1
            print(f"✅ {category}: {message}")
        else:
            self.test_results[category]["failed"] += 1
            self.test_results[category]["errors"].append(message)
            print(f"❌ {category}: {message}")
    
    def test_api_health(self):
        """Test basic API health"""
        print("\n🔍 Testing API Health...")
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "Mindful Mind API is running" in data.get("message", ""):
                    print("✅ API Health: Backend is running and accessible")
                    return True
                else:
                    print(f"❌ API Health: Unexpected response: {data}")
                    return False
            else:
                print(f"❌ API Health: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API Health: Connection failed - {str(e)}")
            return False
    
    def test_ai_chatbot(self):
        """Test AI chatbot endpoint with mental health messages"""
        print("\n🤖 Testing AI Chatbot API...")
        
        for i, message in enumerate(MENTAL_HEALTH_MESSAGES):
            try:
                payload = {
                    "session_id": self.session_id,
                    "message": message
                }
                
                response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    required_fields = ["id", "response", "is_crisis", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_result("ai_chatbot", False, f"Missing fields in response: {missing_fields}")
                        continue
                    
                    # Check response quality
                    if len(data["response"]) < 10:
                        self.log_result("ai_chatbot", False, f"Response too short: '{data['response']}'")
                        continue
                    
                    # Should not be crisis for normal messages
                    if data["is_crisis"]:
                        self.log_result("ai_chatbot", False, f"False positive crisis detection for: '{message}'")
                        continue
                    
                    self.log_result("ai_chatbot", True, f"Normal message processed correctly")
                    
                else:
                    self.log_result("ai_chatbot", False, f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result("ai_chatbot", False, f"Exception: {str(e)}")
    
    def test_crisis_detection(self):
        """Test crisis detection system"""
        print("\n🚨 Testing Crisis Detection System...")
        
        for message in CRISIS_MESSAGES:
            try:
                payload = {
                    "session_id": self.session_id,
                    "message": message
                }
                
                response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Should detect crisis
                    if not data.get("is_crisis", False):
                        self.log_result("crisis_detection", False, f"Failed to detect crisis in: '{message}'")
                        continue
                    
                    # Should have crisis helpline info
                    response_text = data.get("response", "")
                    if "988" not in response_text and "crisis" not in response_text.lower():
                        self.log_result("crisis_detection", False, f"Crisis response missing helpline info")
                        continue
                    
                    self.log_result("crisis_detection", True, f"Crisis detected and handled correctly")
                    
                else:
                    self.log_result("crisis_detection", False, f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result("crisis_detection", False, f"Exception: {str(e)}")
    
    def test_chat_history(self):
        """Test chat history retrieval"""
        print("\n📜 Testing Chat History...")
        
        try:
            response = requests.get(f"{BACKEND_URL}/chat/history/{self.session_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_result("chat_history", False, f"Expected list, got: {type(data)}")
                    return
                
                # Should have messages from previous tests
                if len(data) == 0:
                    self.log_result("chat_history", False, "No chat history found despite previous messages")
                    return
                
                # Check message structure
                for msg in data:
                    required_fields = ["id", "session_id", "message", "response", "is_crisis", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in msg]
                    
                    if missing_fields:
                        self.log_result("chat_history", False, f"Missing fields in history: {missing_fields}")
                        return
                
                self.log_result("chat_history", True, f"Retrieved {len(data)} messages correctly")
                
            else:
                self.log_result("chat_history", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("chat_history", False, f"Exception: {str(e)}")
    
    def test_forum_channels(self):
        """Test forum channels endpoint"""
        print("\n📋 Testing Forum Channels...")
        
        try:
            response = requests.get(f"{BACKEND_URL}/forum/channels", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "channels" not in data:
                    self.log_result("forum_channels", False, "Missing 'channels' field in response")
                    return
                
                channels = data["channels"]
                if not isinstance(channels, list):
                    self.log_result("forum_channels", False, f"Expected list, got: {type(channels)}")
                    return
                
                # Check for default channels
                expected_channels = ["general", "anxiety", "depression", "study-stress", "relationships"]
                missing_channels = [ch for ch in expected_channels if ch not in channels]
                
                if missing_channels:
                    self.log_result("forum_channels", False, f"Missing default channels: {missing_channels}")
                    return
                
                self.log_result("forum_channels", True, f"Retrieved {len(channels)} channels correctly")
                
            else:
                self.log_result("forum_channels", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("forum_channels", False, f"Exception: {str(e)}")
    
    def test_forum_posts(self):
        """Test forum post creation and retrieval"""
        print("\n💬 Testing Forum Posts...")
        
        # Test creating posts
        for post_data in FORUM_POSTS_DATA:
            try:
                response = requests.post(f"{BACKEND_URL}/forum/{post_data['channel']}", json=post_data, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    required_fields = ["id", "channel", "title", "content", "author", "timestamp", "replies"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_result("forum_posts", False, f"Missing fields in post: {missing_fields}")
                        continue
                    
                    # Check anonymous username generation
                    if not data["author"] or len(data["author"]) < 5:
                        self.log_result("forum_posts", False, f"Invalid author name: '{data['author']}'")
                        continue
                    
                    self.created_posts.append({"id": data["id"], "channel": data["channel"]})
                    self.log_result("forum_posts", True, f"Created post in {post_data['channel']} channel")
                    
                else:
                    self.log_result("forum_posts", False, f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result("forum_posts", False, f"Exception creating post: {str(e)}")
        
        # Test retrieving posts
        for channel in FORUM_CHANNELS:
            try:
                response = requests.get(f"{BACKEND_URL}/forum/{channel}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if not isinstance(data, list):
                        self.log_result("forum_posts", False, f"Expected list for {channel}, got: {type(data)}")
                        continue
                    
                    self.log_result("forum_posts", True, f"Retrieved {len(data)} posts from {channel}")
                    
                else:
                    self.log_result("forum_posts", False, f"HTTP {response.status_code} for {channel}: {response.text}")
                    
            except Exception as e:
                self.log_result("forum_posts", False, f"Exception retrieving {channel}: {str(e)}")
    
    def test_forum_replies(self):
        """Test forum reply functionality"""
        print("\n💭 Testing Forum Replies...")
        
        if not self.created_posts:
            self.log_result("forum_replies", False, "No posts available for reply testing")
            return
        
        for post in self.created_posts[:2]:  # Test replies on first 2 posts
            try:
                reply_data = {
                    "content": "Thank you for sharing. I can relate to what you're going through. You're not alone in this."
                }
                
                response = requests.post(
                    f"{BACKEND_URL}/forum/{post['channel']}/{post['id']}/reply", 
                    json=reply_data, 
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    required_fields = ["id", "content", "author", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_result("forum_replies", False, f"Missing fields in reply: {missing_fields}")
                        continue
                    
                    # Check anonymous username
                    if not data["author"] or len(data["author"]) < 5:
                        self.log_result("forum_replies", False, f"Invalid reply author: '{data['author']}'")
                        continue
                    
                    self.log_result("forum_replies", True, f"Added reply to post in {post['channel']}")
                    
                else:
                    self.log_result("forum_replies", False, f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result("forum_replies", False, f"Exception adding reply: {str(e)}")
    
    def test_admin_crisis_alerts(self):
        """Test admin crisis alerts endpoint"""
        print("\n🚨 Testing Admin Crisis Alerts...")
        
        try:
            response = requests.get(f"{BACKEND_URL}/admin/crisis-alerts", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_result("admin_alerts", False, f"Expected list, got: {type(data)}")
                    return
                
                # Should have alerts from crisis detection tests
                if len(data) == 0:
                    self.log_result("admin_alerts", False, "No crisis alerts found despite crisis messages")
                    return
                
                # Check alert structure
                for alert in data:
                    required_fields = ["id", "session_id", "message", "timestamp", "status"]
                    missing_fields = [field for field in required_fields if field not in alert]
                    
                    if missing_fields:
                        self.log_result("admin_alerts", False, f"Missing fields in alert: {missing_fields}")
                        return
                
                self.log_result("admin_alerts", True, f"Retrieved {len(data)} crisis alerts correctly")
                
            else:
                self.log_result("admin_alerts", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("admin_alerts", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🧠 Starting Mindful Mind Backend API Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Session ID: {self.session_id}")
        
        # Check API health first
        if not self.test_api_health():
            print("❌ API is not accessible. Stopping tests.")
            return self.generate_report()
        
        # Run all tests in order
        self.test_ai_chatbot()
        self.test_crisis_detection()
        self.test_chat_history()
        self.test_forum_channels()
        self.test_forum_posts()
        self.test_forum_replies()
        self.test_admin_crisis_alerts()
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("📊 MINDFUL MIND BACKEND TEST REPORT")
        print("="*60)
        
        total_passed = sum(result["passed"] for result in self.test_results.values())
        total_failed = sum(result["failed"] for result in self.test_results.values())
        total_tests = total_passed + total_failed
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {total_passed}")
        print(f"Failed: {total_failed}")
        print(f"Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        
        print("\nDetailed Results:")
        for category, result in self.test_results.items():
            status = "✅" if result["failed"] == 0 else "❌"
            print(f"{status} {category.replace('_', ' ').title()}: {result['passed']} passed, {result['failed']} failed")
            
            if result["errors"]:
                for error in result["errors"]:
                    print(f"   - {error}")
        
        return {
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "success_rate": (total_passed/total_tests*100) if total_tests > 0 else 0,
            "details": self.test_results
        }

if __name__ == "__main__":
    tester = MindfulMindTester()
    report = tester.run_all_tests()
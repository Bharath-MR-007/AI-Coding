#!/usr/bin/env python3
"""
Test script for ChatGPT Actions API
Validates that all endpoints work correctly before setting up Actions
"""

import requests
import json
import sys
import time
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8081"
TEST_FILE_PATH = "/Users/bharathmr/Documents/AI-Coding/README.md"

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print(f"{'='*50}")

def print_test_result(test_name: str, success: bool, details: str = ""):
    """Print test result with formatting"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   └─ {details}")

def test_status_endpoint() -> bool:
    """Test the /status endpoint"""
    print_section("Testing Status Endpoint")
    
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_test_result("Status endpoint responds", True)
            print_test_result("Returns JSON", True)
            
            # Check required fields
            required_fields = ['api_status', 'ollama_status', 'success']
            for field in required_fields:
                if field in data:
                    print_test_result(f"Has {field} field", True, f"Value: {data[field]}")
                else:
                    print_test_result(f"Has {field} field", False)
                    return False
            
            # Check if Ollama is available
            if data.get('ollama_status') == 'connected':
                print_test_result("Ollama connection", True, f"Models: {data.get('available_models', [])}")
            else:
                print_test_result("Ollama connection", False, "Ollama may not be running")
                return False
            
            return True
        else:
            print_test_result("Status endpoint responds", False, f"HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test_result("Server connection", False, "API server not running")
        return False
    except Exception as e:
        print_test_result("Status endpoint test", False, f"Error: {e}")
        return False

def test_ask_endpoint() -> bool:
    """Test the /ask endpoint"""
    print_section("Testing Ask Endpoint")
    
    try:
        # Test with a simple question
        test_question = "What is 2+2? Give a very brief answer."
        payload = {
            "message": test_question,
            "model": "llama3.2:latest"
        }
        
        print(f"📤 Sending question: '{test_question}'")
        response = requests.post(
            f"{API_BASE_URL}/ask", 
            json=payload, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test_result("Ask endpoint responds", True)
            
            # Check response structure
            if 'response' in data and 'success' in data:
                print_test_result("Has required fields", True)
                
                if data.get('success'):
                    ai_response = data.get('response', '')
                    print_test_result("AI responded", True, f"Response length: {len(ai_response)} chars")
                    print(f"📥 AI Response: {ai_response[:100]}...")
                    return True
                else:
                    print_test_result("AI processing", False, "Success=False in response")
                    return False
            else:
                print_test_result("Response structure", False, "Missing required fields")
                return False
        else:
            print_test_result("Ask endpoint responds", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Ask endpoint test", False, f"Error: {e}")
        return False

def test_read_file_endpoint() -> bool:
    """Test the /read-file endpoint"""
    print_section("Testing Read File Endpoint")
    
    try:
        # Test reading a known file
        payload = {
            "filepath": TEST_FILE_PATH
        }
        
        print(f"📂 Attempting to read: {TEST_FILE_PATH}")
        response = requests.post(
            f"{API_BASE_URL}/read-file", 
            json=payload, 
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test_result("Read file endpoint responds", True)
            
            if 'content' in data and 'success' in data:
                print_test_result("Has required fields", True)
                
                if data.get('success'):
                    content = data.get('content', '')
                    size = data.get('size_bytes', 0)
                    print_test_result("File read successfully", True, f"Size: {size} bytes")
                    print(f"📄 Content preview: {content[:100]}...")
                    return True
                else:
                    print_test_result("File reading", False, "Success=False in response")
                    return False
            else:
                print_test_result("Response structure", False, "Missing required fields")
                return False
        elif response.status_code == 404:
            print_test_result("File exists", False, f"File not found: {TEST_FILE_PATH}")
            return False
        else:
            print_test_result("Read file endpoint responds", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Read file endpoint test", False, f"Error: {e}")
        return False

def test_security_restrictions() -> bool:
    """Test that security restrictions are working"""
    print_section("Testing Security Restrictions")
    
    try:
        # Test reading a file outside allowed directory
        restricted_path = "/etc/passwd"  # Common system file
        payload = {
            "filepath": restricted_path
        }
        
        print(f"🔒 Testing restricted access to: {restricted_path}")
        response = requests.post(
            f"{API_BASE_URL}/read-file", 
            json=payload, 
            timeout=10
        )
        
        if response.status_code == 403:
            print_test_result("Security restrictions", True, "Correctly blocked unauthorized file access")
            return True
        elif response.status_code == 404:
            print_test_result("Security restrictions", True, "File not found (also secure)")
            return True
        else:
            print_test_result("Security restrictions", False, f"Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Security test", False, f"Error: {e}")
        return False

def test_openapi_schema() -> bool:
    """Test that OpenAPI schema is accessible"""
    print_section("Testing OpenAPI Schema")
    
    try:
        response = requests.get(f"{API_BASE_URL}/openapi.json", timeout=10)
        
        if response.status_code == 200:
            try:
                schema = response.json()
                print_test_result("OpenAPI schema accessible", True)
                
                # Check basic OpenAPI structure
                required_fields = ['openapi', 'info', 'paths']
                for field in required_fields:
                    if field in schema:
                        print_test_result(f"Schema has {field}", True)
                    else:
                        print_test_result(f"Schema has {field}", False)
                        return False
                
                # Check if our endpoints are documented
                paths = schema.get('paths', {})
                expected_endpoints = ['/ask', '/read-file', '/status']
                for endpoint in expected_endpoints:
                    if endpoint in paths:
                        print_test_result(f"Endpoint {endpoint} documented", True)
                    else:
                        print_test_result(f"Endpoint {endpoint} documented", False)
                        return False
                
                return True
                
            except json.JSONDecodeError:
                print_test_result("OpenAPI schema format", False, "Invalid JSON")
                return False
        else:
            print_test_result("OpenAPI schema accessible", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("OpenAPI schema test", False, f"Error: {e}")
        return False

def main():
    """Run all tests and report results"""
    print("🚀 ChatGPT Actions API Test Suite")
    print("=" * 50)
    print("This script validates your Actions API before ChatGPT setup")
    print("Make sure your API server is running on port 8081")
    
    # Run all tests
    tests = [
        ("Server Status", test_status_endpoint),
        ("AI Integration", test_ask_endpoint),
        ("File Access", test_read_file_endpoint),
        ("Security", test_security_restrictions),
        ("OpenAPI Schema", test_openapi_schema)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_function in tests:
        if test_function():
            passed_tests += 1
        time.sleep(1)  # Brief pause between tests
    
    # Final summary
    print_section("Test Results Summary")
    print(f"📊 Tests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your Actions API is ready for ChatGPT setup")
        print("📚 Next step: Follow the ACTIONS_SETUP_GUIDE.md")
    else:
        print("⚠️  Some tests failed")
        print("🔧 Please fix issues before setting up ChatGPT Actions")
        print("📖 Check the API server logs and Ollama status")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
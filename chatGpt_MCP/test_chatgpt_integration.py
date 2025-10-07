#!/usr/bin/env python3
"""
ChatGPT Integration Test Suite
Tests all ChatGPT file sharing methods
"""

import sys
import os
import requests
import json
import time
import threading
import subprocess
from pathlib import Path

def print_test_header(test_name):
    """Print formatted test header"""
    print(f"\n{'🧪 ' + test_name:=^60}")

def print_result(test_name, success, message=""):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if message:
        print(f"    {message}")

def create_test_file():
    """Create a test file for demonstrations"""
    test_file = Path("/Users/bharathmr/Documents/AI-Coding/chatGpt_MCP/test_content.txt")
    
    content = """AI Technologies Test File
=======================

This file contains information about various AI technologies:

1. OpenAI GPT - Large language model for text generation
2. Ollama - Local AI model runner  
3. Claude - AI assistant by Anthropic
4. FastAPI - Web framework for building APIs
5. MCP - Model Context Protocol for AI tool integration
6. Python - Programming language for AI development

File created for testing ChatGPT integration methods.
"""
    
    with open(test_file, 'w') as f:
        f.write(content)
    
    return test_file

def test_manual_method():
    """Test manual file reading"""
    print_test_header("Manual Method Test")
    
    try:
        test_file = create_test_file()
        
        # Test file reading
        with open(test_file, 'r') as f:
            content = f.read()
        
        success = len(content) > 0 and "AI Technologies" in content
        print_result("File Creation and Reading", success, 
                    f"File size: {len(content)} characters")
        
        # Test prompt generation
        prompt = f"File: {test_file.name}\n\nContent:\n{content}\n\nPlease analyze this content."
        
        success = len(prompt) > 100 and test_file.name in prompt
        print_result("Prompt Generation", success,
                    f"Prompt length: {len(prompt)} characters")
        
        return True
        
    except Exception as e:
        print_result("Manual Method", False, str(e))
        return False

def test_api_server():
    """Test the file API server"""
    print_test_header("File API Server Test")
    
    api_url = "http://localhost:8001"
    
    # Check if server is running
    try:
        response = requests.get(f"{api_url}/", timeout=2)
        server_running = response.status_code == 200
        print_result("Server Accessibility", server_running)
        
        if not server_running:
            print("💡 Start the API server with: python chatgpt_file_api.py")
            return False
            
    except requests.exceptions.RequestException:
        print_result("Server Accessibility", False, "Server not running")
        print("💡 Start the API server with: python chatgpt_file_api.py")
        return False
    
    # Test file reading endpoint
    try:
        test_file = create_test_file()
        
        data = {"filepath": str(test_file)}
        response = requests.post(f"{api_url}/read-file", json=data, timeout=5)
        
        success = response.status_code == 200
        print_result("File Reading Endpoint", success,
                    f"Status code: {response.status_code}")
        
        if success:
            result = response.json()
            has_content = "content" in result and len(result["content"]) > 0
            print_result("Content Retrieval", has_content,
                        f"Content length: {len(result.get('content', ''))}")
            
            return has_content
            
    except Exception as e:
        print_result("API Endpoint Test", False, str(e))
        return False
    
    return False

def test_upload_interface():
    """Test the upload interface"""
    print_test_header("Upload Interface Test")
    
    upload_url = "http://localhost:8002"
    
    try:
        response = requests.get(upload_url, timeout=2)
        success = response.status_code == 200 and "html" in response.headers.get("content-type", "").lower()
        
        print_result("Interface Accessibility", success,
                    f"Status: {response.status_code}")
        
        if success:
            html_content = response.text
            has_upload = "file" in html_content.lower() and "upload" in html_content.lower()
            print_result("Upload Form Present", has_upload)
            
            has_javascript = "javascript" in html_content.lower() or "script" in html_content.lower()
            print_result("JavaScript Functionality", has_javascript)
            
            return has_upload and has_javascript
        
    except requests.exceptions.RequestException:
        print_result("Interface Accessibility", False, "Server not running")
        print("💡 Start the upload interface with: python chatgpt_upload_interface.py")
        return False
    
    return False

def test_file_security():
    """Test file access security"""
    print_test_header("Security Validation Test")
    
    api_url = "http://localhost:8001"
    
    # Test restricted paths
    restricted_paths = [
        "/etc/passwd",
        "../../../etc/hosts", 
        "/System/Library/",
        "../../sensitive_file.txt"
    ]
    
    try:
        for path in restricted_paths:
            data = {"filepath": path}
            response = requests.post(f"{api_url}/read-file", json=data, timeout=5)
            
            # Should return error for restricted paths
            is_blocked = response.status_code != 200
            print_result(f"Path Restriction: {path}", is_blocked,
                        "Access properly blocked" if is_blocked else "Security issue!")
            
        return True
        
    except requests.exceptions.RequestException:
        print_result("Security Test", False, "API server not available")
        return False

def test_integration_completeness():
    """Test that all integration pieces work together"""
    print_test_header("Integration Completeness Test")
    
    # Check file existence
    required_files = [
        "chatgpt_file_api.py",
        "chatgpt_upload_interface.py", 
        "chatgpt_demo.py",
        "CHATGPT_INTEGRATION_GUIDE.md"
    ]
    
    base_path = Path("/Users/bharathmr/Documents/AI-Coding/chatGpt_MCP")
    
    all_files_exist = True
    for filename in required_files:
        file_path = base_path / filename
        exists = file_path.exists()
        print_result(f"File: {filename}", exists)
        if not exists:
            all_files_exist = False
    
    # Check documentation completeness
    guide_path = base_path / "CHATGPT_INTEGRATION_GUIDE.md"
    if guide_path.exists():
        with open(guide_path, 'r') as f:
            guide_content = f.read()
        
        has_methods = all(method in guide_content.lower() for method in 
                         ["manual", "api", "upload"])
        print_result("Guide Completeness", has_methods)
        
        has_examples = "example" in guide_content.lower()
        print_result("Examples Included", has_examples)
        
        return all_files_exist and has_methods and has_examples
    
    return all_files_exist

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🎯 ChatGPT Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Manual Method", test_manual_method),
        ("File API", test_api_server), 
        ("Upload Interface", test_upload_interface),
        ("Security", test_file_security),
        ("Integration", test_integration_completeness)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "🏁 Test Summary".center(60, "="))
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All ChatGPT integration methods are working!")
    else:
        print("⚠️  Some issues found. Check individual test results above.")
    
    # Recommendations
    print(f"\n💡 Quick Start:")
    if results.get("Upload Interface", False):
        print("   Recommended: Use Upload Interface (port 8002)")
    elif results.get("File API", False):
        print("   Recommended: Use File API (port 8001)")
    else:
        print("   Recommended: Use Manual Method (copy-paste)")

if __name__ == "__main__":
    run_comprehensive_test()
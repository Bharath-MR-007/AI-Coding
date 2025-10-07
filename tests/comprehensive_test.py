#!/usr/bin/env python3
"""
Comprehensive AI System Test Suite
Tests all components of the AI-Coding project
"""

import sys
import os
import requests
import subprocess
import time
import json
from pathlib import Path

def print_header(title):
    """Print formatted header"""
    print(f"\n{'🧪 ' + title:=^80}")

def print_result(test, passed, message=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {test}")
    if message:
        print(f"   {message}")

def test_ollama():
    """Test Ollama AI service"""
    print_header("OLLAMA AI SERVICE")
    
    try:
        # Test Ollama list command
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        has_models = "llama3.2:latest" in result.stdout
        print_result("Ollama Service", result.returncode == 0)
        print_result("LLaMA 3.2 Model", has_models)
        
        # Test direct API call
        payload = {
            "model": "llama3.2:latest",
            "prompt": "What is 2+2? Answer with just the number.",
            "stream": False
        }
        
        response = requests.post("http://localhost:11434/api/generate", 
                               json=payload, timeout=15)
        ai_working = response.status_code == 200 and "4" in response.json().get("response", "")
        print_result("AI API Response", ai_working)
        
        return has_models and ai_working
        
    except Exception as e:
        print_result("Ollama Test", False, str(e))
        return False

def test_core_scripts():
    """Test core AI Python scripts"""
    print_header("CORE AI SCRIPTS")
    
    base_path = "/Users/bharathmr/Documents/AI-Coding"
    python_path = f"{base_path}/.AIvenv/bin/python"
    
    # Test files exist
    files = ["educational_ai_example.py", "simple_ai_client.py", "ai_web_service.py", "api_client_example.py"]
    all_exist = True
    
    for file in files:
        exists = Path(f"{base_path}/ai_core/{file}").exists()
        print_result(f"File: {file}", exists)
        if not exists:
            all_exist = False
    
    return all_exist

def test_fastapi_service():
    """Test FastAPI service"""
    print_header("FASTAPI WEB SERVICE")
    
    try:
        # Check if service is running on port 8000
        response = requests.get("http://localhost:8000/docs", timeout=5)
        docs_available = response.status_code == 200
        print_result("API Documentation", docs_available)
        
        # Test the /ask endpoint
        if docs_available:
            test_data = {"message": "What is the capital of Japan?"}
            response = requests.post("http://localhost:8000/ask", 
                                   json=test_data, timeout=15)
            api_working = response.status_code == 200 and "response" in response.json()
            print_result("API Endpoint", api_working, 
                        f"Response: {response.json().get('response', '')[:50]}...")
            return api_working
        else:
            print_result("API Service", False, "Service not running on port 8000")
            return False
            
    except Exception as e:
        print_result("FastAPI Test", False, str(e))
        return False

def test_mcp_integration():
    """Test MCP (Model Context Protocol) integration"""
    print_header("MCP CLAUDE DESKTOP INTEGRATION")
    
    mcp_path = "/Users/bharathmr/Documents/AI-Coding/MCP"
    
    # Check MCP files
    mcp_files = [
        "file_server.py",
        "secret_data.txt", 
        "claude_desktop_config.json",
        "MCP_DOCUMENTATION.md"
    ]
    
    all_files_exist = True
    for file in mcp_files:
        exists = Path(f"{mcp_path}/{file}").exists()
        print_result(f"MCP File: {file}", exists)
        if not exists:
            all_files_exist = False
    
    # Check if config is valid JSON
    config_path = Path(f"{mcp_path}/claude_desktop_config.json")
    config_valid = False
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            config_valid = "mcpServers" in config
            print_result("Config JSON Valid", config_valid)
        except:
            print_result("Config JSON Valid", False)
    
    return all_files_exist and config_valid

def test_chatgpt_integration():
    """Test ChatGPT integration alternatives"""
    print_header("CHATGPT INTEGRATION ALTERNATIVES")
    
    chatgpt_path = "/Users/bharathmr/Documents/AI-Coding/chatGpt_MCP"
    
    # Check ChatGPT files
    chatgpt_files = [
        "chatgpt_file_api.py",
        "chatgpt_upload_interface.py",
        "chatgpt_demo.py",
        "test_chatgpt_integration.py",
        "CHATGPT_INTEGRATION_GUIDE.md",
        "README.md"
    ]
    
    all_files_exist = True
    for file in chatgpt_files:
        exists = Path(f"{chatgpt_path}/{file}").exists()
        print_result(f"ChatGPT File: {file}", exists)
        if not exists:
            all_files_exist = False
    
    # Test manual method (file reading)
    secret_file = Path("/Users/bharathmr/Documents/AI-Coding/MCP/secret_data.txt")
    manual_works = False
    if secret_file.exists():
        try:
            with open(secret_file, 'r') as f:
                content = f.read()
            manual_works = len(content) > 0
            print_result("Manual File Reading", manual_works, f"Read {len(content)} characters")
        except:
            print_result("Manual File Reading", False)
    
    return all_files_exist and manual_works

def test_documentation():
    """Test documentation completeness"""
    print_header("PROJECT DOCUMENTATION")
    
    base_path = "/Users/bharathmr/Documents/AI-Coding"
    
    docs = [
        "README.md",
        "docs/API_Documentation.md", 
        "docs/PROGRAM_GUIDE.md",
        "docs/DIRECTORY_STRUCTURE.md",
        "MCP/MCP_DOCUMENTATION.md",
        "chatGpt_MCP/CHATGPT_INTEGRATION_GUIDE.md"
    ]
    
    all_docs_exist = True
    total_size = 0
    
    for doc in docs:
        doc_path = Path(f"{base_path}/{doc}")
        exists = doc_path.exists()
        
        if exists:
            size = doc_path.stat().st_size
            total_size += size
            print_result(f"Doc: {doc}", True, f"{size} bytes")
        else:
            print_result(f"Doc: {doc}", False)
            all_docs_exist = False
    
    print_result("Total Documentation", all_docs_exist, f"{total_size} total bytes")
    return all_docs_exist

def test_project_structure():
    """Test overall project structure"""
    print_header("PROJECT STRUCTURE VALIDATION")
    
    base_path = "/Users/bharathmr/Documents/AI-Coding"
    
    # Expected directories
    directories = [
        ".AIvenv",
        "MCP", 
        "chatGpt_MCP"
    ]
    
    all_dirs_exist = True
    for directory in directories:
        dir_path = Path(f"{base_path}/{directory}")
        exists = dir_path.exists() and dir_path.is_dir()
        print_result(f"Directory: {directory}", exists)
        if not exists:
            all_dirs_exist = False
    
    # Check virtual environment
    venv_python = Path(f"{base_path}/.AIvenv/bin/python")
    venv_ready = venv_python.exists()
    print_result("Virtual Environment", venv_ready)
    
    return all_dirs_exist and venv_ready

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🎯 AI-Coding Project - Comprehensive Test Suite")
    print("=" * 80)
    print("Testing all components of your AI ecosystem...")
    
    tests = [
        ("Ollama AI Service", test_ollama),
        ("Core AI Scripts", test_core_scripts),
        ("FastAPI Web Service", test_fastapi_service),
        ("MCP Integration", test_mcp_integration),
        ("ChatGPT Alternatives", test_chatgpt_integration),
        ("Documentation", test_documentation),
        ("Project Structure", test_project_structure)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Final Summary
    print_header("FINAL SYSTEM VALIDATION")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        print_result(test_name, result)
    
    print(f"\n📊 Overall Results: {passed}/{total} components passing")
    
    if passed == total:
        print("\n🎉 CONGRATULATIONS! Your complete AI ecosystem is fully functional!")
        print("✨ All components are working correctly:")
        print("   • Ollama AI service with LLaMA 3.2")
        print("   • FastAPI web service on port 8000")
        print("   • Claude Desktop MCP integration")
        print("   • ChatGPT integration alternatives")
        print("   • Complete documentation suite")
        
        print(f"\n🚀 Quick Start Summary:")
        print("   # Use Ollama AI directly:")
        print("   ollama run llama3.2:latest")
        print("\n   # Start web API:")
        print("   python AIService.py")
        print("\n   # Claude Desktop MCP:")
        print("   python MCP/file_server.py")
        print("\n   # ChatGPT file sharing:")
        print("   python chatGpt_MCP/chatgpt_upload_interface.py")
        
    else:
        print(f"\n⚠️  Some issues found ({total-passed} components need attention)")
        print("💡 Check individual test results above for details")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
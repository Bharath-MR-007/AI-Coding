#!/usr/bin/env python3
"""
ChatGPT Integration Demo Script
Demonstrates all methods for sharing files with ChatGPT
"""

import sys
import os
import requests
import json
from pathlib import Path
import time

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🤖 {title}")
    print(f"{'='*60}")

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def demo_manual_method():
    """Demonstrate manual file sharing method"""
    print_step(1, "Manual File Sharing Method (Simplest)")
    
    test_file = Path("/Users/bharathmr/Documents/AI-Coding/MCP/secret_data.txt")
    
    if test_file.exists():
        print("📁 Reading file manually:")
        with open(test_file, 'r') as f:
            content = f.read()
        
        print(f"📄 File: {test_file.name}")
        print(f"📏 Size: {len(content)} characters")
        print(f"📖 Content: {content}")
        
        # Generate ChatGPT prompt
        chatgpt_prompt = f"""File: {test_file.name}

Content:
{content}

Analysis Request:
Please analyze this file content and explain what each item means in the context of AI/software development.
"""
        
        print("\n📋 ChatGPT Prompt Format:")
        print("="*40)
        print(chatgpt_prompt)
        print("="*40)
        print("💡 Copy the above prompt and paste it into ChatGPT!")
        
    else:
        print("❌ Test file not found")

def demo_api_method():
    """Demonstrate API method"""
    print_step(2, "File API Method (Advanced)")
    
    api_url = "http://localhost:8001"
    
    # Check if API is running
    try:
        response = requests.get(f"{api_url}/", timeout=2)
        print("✅ File API is running")
        
        # Test file reading endpoint
        test_data = {
            "filepath": "/Users/bharathmr/Documents/AI-Coding/MCP/secret_data.txt"
        }
        
        print("📡 Testing file reading API...")
        response = requests.post(f"{api_url}/read-file", json=test_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ File read successfully via API")
            print(f"📄 File: {result['file_info']['name']}")
            print(f"📏 Size: {result['file_info']['size']} bytes")
            print(f"📖 Content: {result['content']}")
            
            # Generate API-based prompt for ChatGPT
            chatgpt_prompt = f"""I used an API to read a local file. Here's the result:

File Information:
- Name: {result['file_info']['name']}
- Size: {result['file_info']['size']} bytes
- Path: {result['file_info']['absolute_path']}

File Content:
{result['content']}

Please analyze this content and explain what each technology mentioned is used for.
"""
            
            print("\n📋 ChatGPT Prompt from API:")
            print("="*40)
            print(chatgpt_prompt)
            print("="*40)
            
        else:
            print(f"❌ API call failed: {response.status_code}")
            
    except requests.exceptions.RequestException:
        print("❌ File API is not running")
        print("💡 Start it with: python chatgpt_file_api.py")

def demo_upload_method():
    """Demonstrate upload interface method"""
    print_step(3, "Upload Interface Method (Recommended)")
    
    upload_url = "http://localhost:8002"
    
    try:
        response = requests.get(upload_url, timeout=2)
        print("✅ Upload interface is running")
        print(f"🌐 Open in browser: {upload_url}")
        print("📝 Instructions:")
        print("   1. Go to the URL above in your browser")
        print("   2. Upload any file using the web interface")
        print("   3. Copy the formatted content")
        print("   4. Paste into ChatGPT with your questions")
        
    except requests.exceptions.RequestException:
        print("❌ Upload interface is not running")
        print("💡 Start it with: python chatgpt_upload_interface.py")

def demo_best_practices():
    """Show best practices for ChatGPT integration"""
    print_step(4, "Best Practices for ChatGPT")
    
    practices = [
        "🎯 Be specific in your questions",
        "📝 Format content clearly with file names",
        "🔒 Remove sensitive information before sharing", 
        "📊 Break large files into manageable chunks",
        "💡 Provide context about what you want analyzed",
        "🎨 Use consistent formatting for better results"
    ]
    
    print("Best Practices:")
    for practice in practices:
        print(f"   {practice}")
    
    print(f"\n📋 Example Good Prompt Structure:")
    example_prompt = """Context: I'm analyzing a Python configuration file for security issues.

File: config.py
Content:
[file content here]

Specific Questions:
1. Are there any security vulnerabilities?
2. What improvements would you recommend?
3. Is the configuration structure following best practices?

Please provide detailed analysis with actionable recommendations.
"""
    
    print("="*50)
    print(example_prompt)
    print("="*50)

def demo_comparison():
    """Compare different methods"""
    print_step(5, "Method Comparison")
    
    methods = [
        {
            "name": "Manual Copy-Paste",
            "pros": ["Simple", "Secure", "No setup"],
            "cons": ["Manual work", "Size limits", "No automation"],
            "best_for": "Quick one-time analysis"
        },
        {
            "name": "Upload Interface", 
            "pros": ["User-friendly", "Copy button", "File validation"],
            "cons": ["Requires server", "Size limits", "Temporary storage"],
            "best_for": "Regular file analysis"
        },
        {
            "name": "File API",
            "pros": ["Automated", "Secure", "Real-time access"],
            "cons": ["Technical setup", "API knowledge needed"],
            "best_for": "Integration with other tools"
        }
    ]
    
    for method in methods:
        print(f"\n🔧 {method['name']}:")
        print(f"   ✅ Pros: {', '.join(method['pros'])}")
        print(f"   ❌ Cons: {', '.join(method['cons'])}")
        print(f"   🎯 Best for: {method['best_for']}")

def main():
    """Run the complete ChatGPT integration demo"""
    
    print_header("ChatGPT Integration Demonstration")
    print("🎬 This demo shows how to share local files with ChatGPT")
    print("   when Claude Desktop free plan is exceeded.")
    
    # Demo all methods
    demo_manual_method()
    demo_api_method() 
    demo_upload_method()
    demo_best_practices()
    demo_comparison()
    
    print_header("Demo Complete")
    print("🎉 You now have multiple ways to share files with ChatGPT!")
    print("💡 Choose the method that best fits your needs:")
    print("   • Manual: For simple, one-time tasks")
    print("   • Upload Interface: For regular use with convenience")  
    print("   • File API: For advanced automation and integration")
    
    print(f"\n🚀 Quick Start Commands:")
    print("   # Start upload interface:")
    print("   python chatgpt_upload_interface.py")
    print("\n   # Start file API:")  
    print("   python chatgpt_file_api.py")
    print("\n   # Manual read:")
    print("   cat /path/to/your/file.txt")

if __name__ == "__main__":
    main()
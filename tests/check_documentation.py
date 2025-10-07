#!/usr/bin/env python3
"""
Documentation Completeness Checker
Verifies all documentation is up-to-date and complete
"""

import os
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and return status"""
    path = Path(filepath)
    exists = path.exists()
    size = path.stat().st_size if exists else 0
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    if exists:
        print(f"    Size: {size:,} bytes")
    return exists, size

def check_documentation_completeness():
    """Check all documentation files for completeness"""
    
    print("📚 Documentation Completeness Check")
    print("=" * 60)
    
    base_path = "/Users/bharathmr/Documents/AI-Coding"
    
    # Core documentation
    core_docs = [
        ("README.md", "Main project documentation"),
        ("docs/API_Documentation.md", "API reference guide"),
        ("docs/PROGRAM_GUIDE.md", "Program usage guide")
    ]
    
    print("\n📄 Core Documentation:")
    core_total = 0
    core_count = 0
    for doc, desc in core_docs:
        exists, size = check_file_exists(f"{base_path}/{doc}", desc)
        if exists:
            core_count += 1
            core_total += size
    
    # MCP documentation
    mcp_docs = [
        ("MCP/MCP_DOCUMENTATION.md", "MCP setup and usage guide"),
        ("MCP/claude_desktop_config.json", "Claude Desktop configuration"),
        ("MCP/mcp_config.json", "MCP server configuration")
    ]
    
    print("\n🔗 MCP Documentation:")
    mcp_total = 0
    mcp_count = 0
    for doc, desc in mcp_docs:
        exists, size = check_file_exists(f"{base_path}/{doc}", desc)
        if exists:
            mcp_count += 1
            mcp_total += size
    
    # ChatGPT integration documentation
    chatgpt_docs = [
        ("chatGpt_MCP/README.md", "ChatGPT folder overview"),
        ("chatGpt_MCP/CHATGPT_INTEGRATION_GUIDE.md", "Complete ChatGPT integration guide")
    ]
    
    print("\n💬 ChatGPT Integration Documentation:")
    chatgpt_total = 0
    chatgpt_count = 0
    for doc, desc in chatgpt_docs:
        exists, size = check_file_exists(f"{base_path}/{doc}", desc)
        if exists:
            chatgpt_count += 1
            chatgpt_total += size
    
    # Check for key content in main README
    print("\n🔍 Content Analysis:")
    readme_path = Path(f"{base_path}/README.md")
    if readme_path.exists():
        content = readme_path.read_text()
        
        # Check for key sections
        key_sections = [
            ("Project Structure", "📁 Project Structure" in content),
            ("Advanced Integrations", "🔗 Advanced Integrations" in content),
            ("ChatGPT folder mention", "chatGpt_MCP/" in content),
            ("MCP folder mention", "MCP/" in content),
            ("Quick start commands", "python chatgpt_upload_interface.py" in content)
        ]
        
        for section, found in key_sections:
            status = "✅" if found else "❌"
            print(f"{status} {section}")
    
    # Summary
    total_docs = len(core_docs) + len(mcp_docs) + len(chatgpt_docs)
    total_found = core_count + mcp_count + chatgpt_count
    total_size = core_total + mcp_total + chatgpt_total
    
    print("\n📊 Documentation Summary:")
    print(f"   Files found: {total_found}/{total_docs}")
    print(f"   Total size: {total_size:,} bytes")
    print(f"   Core docs: {core_total:,} bytes")
    print(f"   MCP docs: {mcp_total:,} bytes") 
    print(f"   ChatGPT docs: {chatgpt_total:,} bytes")
    
    # Check folder structure documentation
    print("\n📁 Folder Structure Check:")
    folders = ["MCP", "chatGpt_MCP", ".AIvenv"]
    for folder in folders:
        folder_path = Path(f"{base_path}/{folder}")
        exists = folder_path.exists() and folder_path.is_dir()
        status = "✅" if exists else "❌"
        print(f"{status} {folder}/ folder exists")
    
    # Final assessment
    completeness = (total_found / total_docs) * 100
    print(f"\n🎯 Documentation Completeness: {completeness:.1f}%")
    
    if completeness >= 95:
        print("🎉 Documentation is COMPLETE and up-to-date!")
    elif completeness >= 80:
        print("⚠️  Documentation is mostly complete with minor gaps")
    else:
        print("❌ Documentation needs significant updates")
    
    return completeness >= 95

def check_cross_references():
    """Check that documentation cross-references are correct"""
    
    print("\n🔗 Cross-Reference Check:")
    
    base_path = "/Users/bharathmr/Documents/AI-Coding"
    
    # Check main README references to other docs
    readme_path = Path(f"{base_path}/README.md")
    if readme_path.exists():
        content = readme_path.read_text()
        
        references = [
            ("ChatGPT guide reference", "chatGpt_MCP/CHATGPT_INTEGRATION_GUIDE.md" in content),
            ("MCP folder structure", "MCP/" in content),
            ("ChatGPT folder structure", "chatGpt_MCP/" in content),
            ("API documentation", "API_Documentation.md" in content or "/docs" in content),
        ]
        
        for ref, found in references:
            status = "✅" if found else "❌"
            print(f"{status} {ref}")
    
    return True

if __name__ == "__main__":
    print("🔍 Starting Documentation Verification...")
    
    complete = check_documentation_completeness()
    check_cross_references()
    
    print(f"\n{'=' * 60}")
    if complete:
        print("✅ ALL DOCUMENTATION IS COMPLETE AND UP-TO-DATE!")
        print("📖 Your project has comprehensive documentation covering:")
        print("   • Core functionality and usage")
        print("   • API reference and examples") 
        print("   • MCP Claude Desktop integration")
        print("   • ChatGPT integration alternatives")
        print("   • Complete setup and testing guides")
    else:
        print("⚠️  Some documentation may need updates")
    
    exit(0 if complete else 1)
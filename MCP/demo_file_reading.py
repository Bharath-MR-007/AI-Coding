#!/usr/bin/env python3
"""
Demo script to test MCP file reading functionality
"""

import sys
import os
sys.path.append('/Users/bharathmr/Documents/AI-Coding/MCP')

from file_server import read_local_file

def demo_file_reading():
    """Demonstrate file reading capabilities"""
    print("🔍 MCP File Reading Demo")
    print("=" * 40)
    
    # Test files to read
    test_files = [
        "secret_data.txt",
        "/Users/bharathmr/Documents/AI-Coding/MCP/secret_data.txt",
        "nonexistent_file.txt"  # This should show error handling
    ]
    
    for filepath in test_files:
        print(f"\n📄 Reading: {filepath}")
        result = read_local_file(filepath)
        print(f"📖 Content: {result}")
        print("-" * 30)

if __name__ == "__main__":
    demo_file_reading()
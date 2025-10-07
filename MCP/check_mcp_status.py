#!/usr/bin/env python3
"""
Check MCP server configuration and status
"""

import json
import os
from pathlib import Path

def check_mcp_status():
    """Check MCP configuration and files"""
    print("🔧 MCP Configuration Status Check")
    print("=" * 50)
    
    # Check files
    mcp_dir = Path("/Users/bharathmr/Documents/AI-Coding/MCP")
    required_files = [
        "file_server.py",
        "secret_data.txt",
        "claude_desktop_config.json"
    ]
    
    print("\n📁 File Check:")
    for file in required_files:
        file_path = mcp_dir / file
        status = "✅ EXISTS" if file_path.exists() else "❌ MISSING"
        print(f"  {file}: {status}")
    
    # Check Claude Desktop config
    claude_config = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    print(f"\n🖥️  Claude Desktop Config: {'✅ EXISTS' if claude_config.exists() else '❌ MISSING'}")
    
    if claude_config.exists():
        try:
            with open(claude_config) as f:
                config = json.load(f)
            print("📋 Configuration loaded successfully")
            if "mcpServers" in config:
                servers = list(config["mcpServers"].keys())
                print(f"🔌 MCP Servers configured: {servers}")
        except Exception as e:
            print(f"❌ Configuration error: {e}")
    
    # Check virtual environment
    venv_python = Path("/Users/bharathmr/Documents/AI-Coding/.AIvenv/bin/python")
    print(f"\n🐍 Python Environment: {'✅ READY' if venv_python.exists() else '❌ MISSING'}")

if __name__ == "__main__":
    check_mcp_status()
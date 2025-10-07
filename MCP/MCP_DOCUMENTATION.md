# MCP (Model Context Protocol) File Reader Documentation

## 📋 Overview

This MCP setup enables Claude Desktop to read local files securely through the Model Context Protocol. It creates a bridge between Claude Desktop and your local file system, allowing the AI to access specific files for context and information retrieval.

## 🎯 What is MCP?

Model Context Protocol (MCP) is a standard that allows AI assistants like Claude to securely interact with external tools and data sources. In this case, it enables Claude to read local files on your computer.

## 📁 File Structure

```
/Users/bharathmr/Documents/AI-Coding/MCP/
├── file_server.py                 # Main MCP server implementation
├── mcp_config.json               # MCP server configuration template
├── claude_desktop_config.json    # Claude Desktop configuration template
└── secret_data.txt              # Example file for testing
```

---

## 📄 File Descriptions

### 1. `file_server.py` - MCP Server Implementation

**Purpose:** The core MCP server that provides file reading capabilities to Claude Desktop.

**Code with Line-by-Line Explanation:**

```python
import os
from fastmcp import FastMCP
# Line 1-2: Import required libraries
# - os: For file system operations (not used in this simple version)
# - fastmcp: The FastMCP framework for creating MCP servers

# 1. Define the tool function with a CLEAR docstring.
def read_local_file(filepath: str) -> str:
    """
    Reads the content of a local text file at the given filepath. 
    This tool is useful for fetching context from project files.
    """
    # Line 5-9: Function definition with type hints and docstring
    # - filepath: str -> The path to the file we want to read
    # - -> str: The function returns a string (file content)
    # - Docstring: Explains what the function does (MCP uses this description)
    
    try:
        # Security Note: In a real app, you must sanitize and restrict file paths!
        # For this simple example, we use the raw path.
        with open(filepath, 'r') as f:
            content = f.read()
        return content
        # Line 11-15: File reading logic with error handling
        # - try: Attempt to read the file
        # - open(filepath, 'r'): Open file in read mode
        # - with: Ensures file is properly closed after reading
        # - f.read(): Read entire file content into memory
        # - return content: Send the file content back to Claude
        
    except FileNotFoundError:
        return f"Error: File not found at path: {filepath}"
        # Line 16-17: Handle case when file doesn't exist
        # - Returns user-friendly error message instead of crashing
        
    except Exception as e:
        return f"An unexpected error occurred: {e}"
        # Line 18-19: Handle any other unexpected errors
        # - Catches all other exceptions and returns error description

# 2. Create the FastMCP server instance and register the tool.
app = FastMCP(tools=[read_local_file])
# Line 21-22: Create the MCP server
# - FastMCP(): Creates a new MCP server instance
# - tools=[read_local_file]: Registers our file reading function as an available tool
# - app: The server instance that Claude Desktop will communicate with

# 3. The FastMCP run method automatically handles the MCP protocol 
# (initialization, requests) using standard input/output (stdio).
if __name__ == "__main__":
    app.run()
    # Line 24-27: Start the server when script is run directly
    # - if __name__ == "__main__": Only run when script is executed directly
    # - app.run(): Start the MCP server and listen for requests from Claude Desktop
    # - Uses stdio (standard input/output) for communication with Claude Desktop
```

**Key Features:**
- ✅ **Secure file reading** with error handling
- ✅ **MCP protocol compliance** using FastMCP framework
- ✅ **Simple interface** with clear function documentation
- ✅ **Error recovery** for missing files or permission issues

---

### 2. `secret_data.txt` - Example Data File

**Purpose:** Contains sample data that demonstrates the MCP file reading capability.

**Content:**
```
This file contains the top secret launch code: ALPHACHICAGO47
```

**Usage:** This file serves as a test case to verify that Claude Desktop can successfully read local files through the MCP connection.

---

### 3. `claude_desktop_config.json` - Claude Desktop Configuration

**Purpose:** Configuration template for Claude Desktop to connect to your MCP server.

**Code with Line-by-Line Explanation:**

```json
{
  "mcpServers": {
    // Line 2: Define MCP servers section
    // This tells Claude Desktop which MCP servers are available
    
    "local-project-file-context": {
      // Line 3: Server identifier name
      // This is a unique name for your MCP server
      
      "command": "/Users/bharathmr/Documents/AI-Coding/.AIvenv/bin/python",
      // Line 4: Python executable path
      // Points to your virtual environment's Python interpreter
      // This ensures the correct dependencies are available
      
      "args": [
        "/Users/bharathmr/Documents/AI-Coding/MCP/file_server.py"
      ]
      // Line 5-7: Command arguments
      // Tells Claude Desktop which script to run
      // This is the path to your MCP server script
    }
  }
}
```

**Configuration Details:**
- **Server Name:** `local-project-file-context` (you can change this)
- **Python Path:** Points to your virtual environment
- **Script Path:** Points to the MCP server script
- **Communication:** Uses stdio (standard input/output)

---

### 4. `mcp_config.json` - Extended MCP Configuration

**Purpose:** A more detailed configuration template with additional metadata.

**Code with Line-by-Line Explanation:**

```json
{
  "mcpServers": {
    // Line 2: MCP servers configuration section
    
    "local-project-file-context": {
      // Line 3: Server identifier
      
      "type": "stdio",
      // Line 4: Communication type
      // "stdio" means communication via standard input/output
      
      "command": "/Users/bharathmr/Documents/AI-Coding/.AIvenv/bin/python",
      // Line 5: Python executable path
      // Uses your virtual environment's Python
      
      "args": [
        "/Users/bharathmr/Documents/AI-Coding/MCP/file_server.py"
      ],
      // Line 6-8: Script arguments
      // Path to the MCP server script
      
      "description": "A tool that securely retrieves context and content from local project files for use by the AI agent.",
      // Line 9: Human-readable description
      // Explains what this MCP server does
      
      "name": "ProjectFileContextReader"
      // Line 10: Display name for the MCP server
      // Friendly name shown in Claude Desktop
    }
  }
}
```

---

## 🚀 Setup and Showcase Procedure

### Prerequisites

1. **Python Environment:** Virtual environment with FastMCP installed
2. **Claude Desktop:** Installed and running
3. **File Structure:** MCP files organized in the correct directory

### Step 1: Verify Installation

```bash
# Check if virtual environment exists
ls -la /Users/bharathmr/Documents/AI-Coding/.AIvenv/

# Check if FastMCP is installed
/Users/bharathmr/Documents/AI-Coding/.AIvenv/bin/pip list | grep fastmcp

# Should show: fastmcp    2.12.4
```

### Step 2: Test MCP Server Locally

```bash
# Navigate to MCP directory
cd /Users/bharathmr/Documents/AI-Coding/MCP

# Test file reading function directly
/Users/bharathmr/Documents/AI-Coding/.AIvenv/bin/python -c "
import sys
sys.path.append('.')
from file_server import read_local_file
result = read_local_file('secret_data.txt')
print('File content:', result)
"

# Expected output: File content: This file contains the top secret launch code: ALPHACHICAGO47
```

### Step 3: Test MCP Server Communication

```bash
# Start the MCP server (will show FastMCP banner)
/Users/bharathmr/Documents/AI-Coding/.AIvenv/bin/python file_server.py

# You should see:
# ╭────────────────────────────────────────╮
# │              FastMCP  2.0              │
# │        🖥️  Server name: FastMCP-xxx     │
# │        📦 Transport: STDIO             │
# ╰────────────────────────────────────────╯

# Press Ctrl+C to stop
```

### Step 4: Configure Claude Desktop

```bash
# Copy configuration to Claude Desktop
sudo cp /Users/bharathmr/Documents/AI-Coding/MCP/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or update manually with the configuration content
```

### Step 5: Restart Claude Desktop

1. **Quit Claude Desktop** completely (Cmd+Q)
2. **Reopen Claude Desktop**
3. **Wait for initialization** (may take 10-15 seconds)

### Step 6: Verify MCP Connection

In Claude Desktop, you should see:
- 🔧 A small tools icon or indication that MCP tools are available
- The ability to use file reading capabilities

### Step 7: Test File Reading

Ask Claude Desktop to:

```
Please read the file: /Users/bharathmr/Documents/AI-Coding/MCP/secret_data.txt
```

**Expected Result:** Claude should be able to read and display the contents of the secret_data.txt file.

---

## 🧪 Demonstration Scripts

### Demo Script 1: Basic File Reading Test

```python
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
```

### Demo Script 2: MCP Server Status Check

```python
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
```

---

## 🎬 Complete Showcase Procedure

### Live Demonstration Steps

1. **Show Project Structure**
   ```bash
   tree /Users/bharathmr/Documents/AI-Coding/MCP
   ```

2. **Demonstrate Local Testing**
   ```bash
   cd /Users/bharathmr/Documents/AI-Coding/MCP
   python demo_file_reading.py
   ```

3. **Show MCP Server Startup**
   ```bash
   /Users/bharathmr/Documents/AI-Coding/.AIvenv/bin/python file_server.py
   # (Show FastMCP banner, then Ctrl+C)
   ```

4. **Verify Claude Desktop Configuration**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

5. **Live Test with Claude Desktop**
   - Open Claude Desktop
   - Ask it to read the secret_data.txt file
   - Demonstrate successful file content retrieval

6. **Show Error Handling**
   - Ask Claude to read a non-existent file
   - Demonstrate graceful error handling

---

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

**Issue 1: "Cannot connect to MCP server"**
- ✅ Check virtual environment path in configuration
- ✅ Verify FastMCP is installed: `pip list | grep fastmcp`
- ✅ Restart Claude Desktop completely

**Issue 2: "File not found" errors**
- ✅ Use absolute file paths
- ✅ Check file permissions
- ✅ Verify file exists: `ls -la /path/to/file`

**Issue 3: "Permission denied" on config file**
- ✅ Fix ownership: `sudo chown $USER ~/Library/Application\ Support/Claude/claude_desktop_config.json`
- ✅ Or use sudo to update: `sudo tee ~/Library/Application\ Support/Claude/claude_desktop_config.json`

**Issue 4: MCP tools not appearing in Claude Desktop**
- ✅ Wait 10-15 seconds after restart
- ✅ Check for typos in JSON configuration
- ✅ Verify file paths are correct

---

## 🎯 Advanced Usage Examples

### Reading Different File Types

```python
# Add to file_server.py for enhanced functionality
def read_json_file(filepath: str) -> str:
    """Read and format JSON files"""
    try:
        with open(filepath, 'r') as f:
            import json
            data = json.load(f)
            return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error reading JSON: {e}"

def read_code_file(filepath: str) -> str:
    """Read code files with syntax highlighting info"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            ext = filepath.split('.')[-1]
            return f"File type: {ext}\n\n{content}"
    except Exception as e:
        return f"Error reading code file: {e}"
```

### Security Enhancements

```python
import os
from pathlib import Path

def read_local_file_secure(filepath: str) -> str:
    """Enhanced secure file reading with path validation"""
    try:
        # Security: Restrict to specific directories
        allowed_dirs = [
            "/Users/bharathmr/Documents/AI-Coding",
            "/Users/bharathmr/Projects"
        ]
        
        # Resolve absolute path
        abs_path = Path(filepath).resolve()
        
        # Check if path is within allowed directories
        if not any(str(abs_path).startswith(allowed_dir) for allowed_dir in allowed_dirs):
            return "Error: Access denied - file outside allowed directories"
        
        # Read file
        with open(abs_path, 'r') as f:
            return f.read()
            
    except FileNotFoundError:
        return f"Error: File not found at path: {filepath}"
    except PermissionError:
        return f"Error: Permission denied for file: {filepath}"
    except Exception as e:
        return f"Error: {e}"
```

---

## 📈 Performance Monitoring

### Monitor MCP Usage

```python
import time
from datetime import datetime

class MCPLogger:
    def __init__(self):
        self.requests = []
    
    def log_request(self, filepath: str, success: bool, response_time: float):
        """Log MCP requests for monitoring"""
        self.requests.append({
            'timestamp': datetime.now().isoformat(),
            'filepath': filepath,
            'success': success,
            'response_time': response_time
        })
    
    def get_stats(self):
        """Get usage statistics"""
        total = len(self.requests)
        successful = sum(1 for r in self.requests if r['success'])
        avg_time = sum(r['response_time'] for r in self.requests) / total if total > 0 else 0
        
        return {
            'total_requests': total,
            'successful_requests': successful,
            'success_rate': successful / total if total > 0 else 0,
            'average_response_time': avg_time
        }

# Usage in file_server.py
logger = MCPLogger()

def read_local_file_monitored(filepath: str) -> str:
    """File reading with performance monitoring"""
    start_time = time.time()
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        response_time = time.time() - start_time
        logger.log_request(filepath, True, response_time)
        return content
        
    except Exception as e:
        response_time = time.time() - start_time
        logger.log_request(filepath, False, response_time)
        return f"Error: {e}"
```

This comprehensive documentation covers everything needed to understand, set up, demonstrate, and troubleshoot your MCP file reader system! 🎉📚
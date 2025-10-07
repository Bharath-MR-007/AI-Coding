# ChatGPT MCP Alternative

This folder contains ChatGPT integration tools as an alternative to Claude Desktop MCP functionality.

## 📂 Files Overview

### Core Integration Files
- **`chatgpt_file_api.py`** - REST API server for secure file access (Port 8001)
- **`chatgpt_upload_interface.py`** - Web interface for file uploads (Port 8002)

### Demonstration & Testing
- **`chatgpt_demo.py`** - Interactive demonstration of all methods
- **`test_chatgpt_integration.py`** - Comprehensive test suite

### Documentation
- **`CHATGPT_INTEGRATION_GUIDE.md`** - Complete integration guide
- **`README.md`** - This overview file

## 🚀 Quick Start

### Method 1: Upload Interface (Recommended)
```bash
cd /Users/bharathmr/Documents/AI-Coding/chatGpt_MCP
python chatgpt_upload_interface.py
# Open http://localhost:8002 in browser
```

### Method 2: File API (Advanced)
```bash
cd /Users/bharathmr/Documents/AI-Coding/chatGpt_MCP
python chatgpt_file_api.py
# API available at http://localhost:8001
```

### Method 3: Manual (Simple)
```bash
cat /path/to/your/file.txt  # Copy output to ChatGPT
```

## 🧪 Testing

Run the test suite to verify everything works:
```bash
cd /Users/bharathmr/Documents/AI-Coding/chatGpt_MCP
python test_chatgpt_integration.py
```

Run the interactive demo:
```bash
cd /Users/bharathmr/Documents/AI-Coding/chatGpt_MCP
python chatgpt_demo.py
```

## 📖 Documentation

For complete setup instructions and examples, see:
- `CHATGPT_INTEGRATION_GUIDE.md` - Comprehensive guide with examples

## 🎯 Use Cases

- **Claude Desktop free plan exceeded**: Use these alternatives
- **File sharing with ChatGPT**: Secure local file access
- **Automation**: REST API for programmatic file access
- **User-friendly**: Web interface for drag-and-drop uploads

## 🔒 Security Features

- Path validation to prevent directory traversal
- File size limits for upload interface
- Restricted access to system files
- Input sanitization for all endpoints

## 💡 Why This Folder?

This folder provides ChatGPT integration alternatives when Claude Desktop MCP isn't available or has exceeded free plan limits. All files are self-contained and don't interfere with the main MCP setup for Claude Desktop.
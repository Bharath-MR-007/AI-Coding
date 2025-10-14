# Project Directory Structure

This document explains the organized directory structure of the AI-Coding project.

## 📁 Directory Overview

```
AI-Coding/
├── ai_core/            # 🤖 Core AI Application Code
├── docs/               # 📚 Documentation Files  
├── tests/              # 🧪 Testing & Validation Scripts
├── config/             # ⚙️ Configuration Files
├── MCP/                # 🔗 Claude Desktop MCP Integration
├── chatGpt_MCP/        # 💬 ChatGPT Integration Alternatives
├── Alert_llm/          # 🚨 Alert simulation & LLM troubleshooting
├── .AIvenv/            # 🐍 Python Virtual Environment
└── README.md           # 📖 Main Project Documentation
```

---

## 📂 Directory Details

### `ai_core/` - Core AI Application Code
Contains the main AI application scripts and services:

- **`educational_ai_example.py`** - Educational tutorial with detailed explanations
- **`simple_ai_client.py`** - Production-ready minimal AI client  
- **`ai_web_service.py`** - FastAPI web service for AI interactions
- **`api_client_example.py`** - API client usage examples

**Purpose:** Houses all core AI functionality and executable scripts

### `docs/` - Documentation Files
Comprehensive documentation for the project:

- **`API_Documentation.md`** - Complete REST API reference
- **`PROGRAM_GUIDE.md`** - Detailed usage guide for all programs

**Purpose:** Centralized documentation for developers and users

### `tests/` - Testing & Validation
Scripts for testing system functionality and integrity:

- **`test_ai_connection.py`** - Basic AI connectivity validation
- **`comprehensive_test.py`** - Full system test suite
- **`check_documentation.py`** - Documentation completeness verification

**Purpose:** Ensures system reliability and validates all components

### `config/` - Configuration Files
Project configuration and environment setup:

- **`requirements.txt`** - Python package dependencies
- **`.env`** - Environment variables and secrets

**Purpose:** Manages dependencies and environment configuration

### `MCP/` - Claude Desktop Integration
Model Context Protocol setup for Claude Desktop:

- **`file_server.py`** - MCP server implementation
- **`MCP_DOCUMENTATION.md`** - Complete setup guide
- **Configuration files** - Claude Desktop config templates

**Purpose:** Enables Claude Desktop to read local files securely

### `chatGpt_MCP/` - ChatGPT Integration
Alternative file sharing solutions for ChatGPT:

- **API server** - REST endpoints for file access
- **Upload interface** - Web-based file sharing
- **Demo scripts** - Interactive demonstrations

**Purpose:** Provides ChatGPT file integration when Claude limits are exceeded

### `Alert_llm/` - Alert Simulation & LLM Troubleshooting
A self-contained mini-project for simulating alerts and receiving automated troubleshooting/RCA suggestions from a local Ollama LLM.

- **`alert_simulator.py`** - Sends simulated alerts to a webhook
- **`webhook_receiver.py`** - Receives alerts, queries LLM for troubleshooting
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Project documentation & sample output

**Purpose:** Demonstrates AI-driven troubleshooting by integrating alert simulation with a local LLM for actionable SRE advice.

---

## 🚀 Quick Commands by Directory

### Core Application (`ai_core/`)
```bash
# Run AI scripts
python ai_core/educational_ai_example.py
python ai_core/simple_ai_client.py

# Start web service  
cd ai_core && python ai_web_service.py
```

### Testing (`tests/`)
```bash
# Run system tests
python tests/comprehensive_test.py
python tests/check_documentation.py
```

### Configuration (`config/`)
```bash
# Install dependencies
pip install -r config/requirements.txt

# Setup environment
source config/.env  # if using bash/zsh
```

### Integration Services
```bash
# Claude Desktop MCP
python MCP/file_server.py

# ChatGPT alternatives
python chatGpt_MCP/chatgpt_upload_interface.py
python chatGpt_MCP/chatgpt_file_api.py
```

### Alert Simulation & Troubleshooting (`Alert_llm/`)
```bash
# Simulate alerts
python Alert_llm/alert_simulator.py

# Receive and troubleshoot alerts
python Alert_llm/webhook_receiver.py
```

---

## 📈 Benefits of This Structure

✅ **Organization** - Clear separation of concerns  
✅ **Maintainability** - Easy to find and update components  
✅ **Scalability** - Simple to add new features in appropriate directories  
✅ **Clarity** - Obvious purpose for each directory and file  
✅ **Professional** - Follows standard project organization patterns  

This structure makes the project more professional, easier to navigate, and simpler to maintain as it grows.
# ChatGPT Actions Setup Guide

## 🎯 Overview

ChatGPT Actions allow your custom GPT to call external APIs. This guide shows you how to connect your custom GPT directly to your local AI services, creating a powerful bridge between ChatGPT and your local AI infrastructure.

## 🔧 What You'll Achieve

- **Direct API Integration**: Your custom GPT can call your local AI services
- **Local AI Access**: ChatGPT can use your Ollama models through Actions
- **File System Access**: ChatGPT can read your local files via Actions
- **Seamless Experience**: Natural conversation with local AI capabilities

---

## 📋 Prerequisites

1. **ChatGPT Plus Subscription** (required for custom GPTs and Actions)
2. **Local AI Setup** (your Ollama service running)
3. **API Server** (we'll set this up)

---

## 🚀 Step-by-Step Setup

### Step 1: Start the Actions API Server

```bash
# Navigate to the actions directory
cd /Users/bharathmr/Documents/AI-Coding/chatgpt_actions

# Start the API server (runs on port 8081)
python actions_api_server.py
```

**Expected Output:**
```
🚀 Starting ChatGPT Actions API Server...
📡 ChatGPT Actions can now connect to your local AI!
📍 Server will be available at: http://localhost:8081
📚 API documentation at: http://localhost:8081/docs
🔧 Configure ChatGPT Actions with: http://localhost:8081/openapi.json
```

### Step 2: Create Your Custom GPT

1. **Go to ChatGPT**: Visit [chat.openai.com](https://chat.openai.com)
2. **Create New GPT**: Click "Explore GPTs" → "Create a GPT"
3. **Configure Your GPT**:
   - **Name**: "Local AI Assistant"
   - **Description**: "A GPT that can access my local AI models and files"
   - **Instructions**: 
   ```
   You are a Local AI Assistant with special capabilities:
   
   1. You can ask questions to my local Ollama AI using the /ask action
   2. You can read files from my local computer using the /read-file action
   3. You can check the status of my local AI services using the /status action
   
   When users ask questions that could benefit from local AI processing or need to access local files, use these actions proactively.
   
   Always explain what you're doing when you call these actions, like:
   - "Let me ask your local AI model about this..."
   - "I'll read that file from your computer..."
   - "Let me check your local AI service status..."
   ```

### Step 3: Configure Actions

1. **Go to Actions Tab**: In your GPT builder, click "Actions"

2. **Import OpenAPI Schema**: 
   - Click "Create new action"
   - Choose "Import from URL"
   - Enter: `http://localhost:8081/openapi.json`
   - Click "Import"

3. **Verify Endpoints**: You should see these actions imported:
   - `ask_local_ai` - Send questions to your local AI
   - `read_local_file` - Read files from your computer
   - `get_service_status` - Check local AI service status

4. **Test the Connection**:
   - Click "Test" next to any action
   - Try the `/status` endpoint first
   - You should see your local AI service information

### Step 4: Authentication (Optional)

For basic security, you can add authentication:

1. **In Actions Settings**: Choose "API Key"
2. **Add Custom Header**: 
   - Header Name: `X-API-Key`
   - Value: `your-secret-key-here`

Then update your server to check for this header.

---

## 🎮 Usage Examples

### Example 1: Ask Your Local AI

**You say to ChatGPT:**
> "Ask my local AI model to explain quantum computing"

**ChatGPT will:**
1. Call your `/ask` action
2. Send the question to your local Ollama
3. Return the local AI's response
4. Combine it with its own knowledge

### Example 2: Analyze Your Files

**You say to ChatGPT:**
> "Read my README.md file and summarize the project"

**ChatGPT will:**
1. Call your `/read-file` action
2. Retrieve the file contents
3. Analyze and summarize the content
4. Provide insights about your project

### Example 3: Check Local Services

**You say to ChatGPT:**
> "Check if my local AI is running and what models I have"

**ChatGPT will:**
1. Call your `/status` action
2. Report on service health
3. List available AI models
4. Suggest next steps if issues found

---

## 🔍 Testing Your Setup

### Test 1: Basic Connection
```bash
# Test if your API is working
curl http://localhost:8080/status
```

### Test 2: Ask Endpoint
```bash
curl -X POST "http://localhost:8080/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is machine learning?"}'
```

### Test 3: File Reading
```bash
curl -X POST "http://localhost:8080/read-file" \
     -H "Content-Type: application/json" \
     -d '{"filepath": "/Users/bharathmr/Documents/AI-Coding/README.md"}'
```

---

## 🛠️ Advanced Configuration

### Custom Prompts for Actions

You can customize how your GPT uses actions by modifying the instructions:

```
Advanced Instructions:

1. When users ask technical questions, ALWAYS check with the local AI first using /ask
2. When users mention files or want to see code, use /read-file to access them
3. If local AI gives different answers than you, present both perspectives
4. For coding questions, read relevant source files before answering
5. Always check /status if there are connection issues
```

### Multiple AI Models

Your local setup supports multiple models. You can instruct ChatGPT:

```
Model Selection Guidelines:
- Use "llama3.2:latest" for general questions
- Use other models if available for specialized tasks
- Always mention which model you're using
```

---

## 🔒 Security Considerations

### File Access Security
- Files are restricted to your AI-Coding project directory
- No system files or sensitive directories are accessible
- All paths are validated for security

### Network Security
- API server only accepts local connections (127.0.0.1)
- CORS is configured for ChatGPT domains only
- Consider using HTTPS for production use

### API Key Protection
- Use environment variables for API keys
- Rotate keys regularly
- Monitor access logs

---

## 🐛 Troubleshooting

### Common Issues

**Issue: "Failed to connect to action"**
```bash
# Check if API server is running
curl http://localhost:8080/status

# Restart the server
python actions_api_server.py
```

**Issue: "Ollama not available"**
```bash
# Check Ollama service
ollama list

# Start Ollama if needed
ollama serve
```

**Issue: "File access denied"**
- Ensure file paths are within the allowed directory
- Check file permissions
- Verify file exists

### Debug Mode

Enable debug logging in your API server:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🎉 What You've Accomplished

✅ **Connected ChatGPT to Local AI** - Direct API bridge established  
✅ **File System Access** - ChatGPT can read your local files  
✅ **Multi-Model Support** - Access to all your local AI models  
✅ **Secure Integration** - Protected endpoints with access controls  
✅ **Seamless Experience** - Natural conversation with enhanced capabilities  

Your custom GPT now has superpowers! It can leverage your local AI infrastructure while maintaining the conversational interface you're familiar with.

---

## 🚀 Next Steps

1. **Experiment**: Try different types of questions and file analysis
2. **Customize**: Modify the GPT instructions for your specific use cases
3. **Extend**: Add more endpoints for additional functionality
4. **Share**: Create multiple custom GPTs for different purposes

Happy AI-powered productivity! 🤖✨
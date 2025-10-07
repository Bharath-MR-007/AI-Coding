# Local AI Chatbot Service

A simple yet powerful AI chatbot service that runs locally using Ollama and FastAPI. This project provides both a simple script interface and a professional web API for interacting with AI models.

## 🚀 Features

- **Local AI Processing** - No API keys required, runs entirely on your machine
- **Multiple Interfaces** - Simple Python scripts and REST API
- **Privacy First** - Your conversations never leave your computer
- **Fast Response** - Local processing means quick results
- **Easy to Use** - Simple setup and intuitive interfaces

## 📋 Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- At least one Ollama model (we use `llama3.2:latest`)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Create a virtual environment**
   ```bash
   python -m venv .AIvenv
   source .AIvenv/bin/activate  # On Mac/Linux
   # or
   .AIvenv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make sure Ollama is running**
   ```bash
   ollama serve  # If not already running
   ollama pull llama3.2:latest  # If you don't have the model
   ```

## 📁 Project Structure

```
AI-Coding/
├── ai_core/            # Core AI application code
│   ├── educational_ai_example.py  # Educational tutorial with detailed comments
│   ├── simple_ai_client.py        # Production-ready minimal AI client
│   ├── ai_web_service.py          # FastAPI web service
│   └── api_client_example.py      # API client usage example
├── docs/               # Project documentation
│   ├── API_Documentation.md # Complete API reference
│   └── PROGRAM_GUIDE.md     # Program usage guide
├── tests/              # Testing and validation scripts
│   ├── test_ai_connection.py      # AI connectivity tests
│   ├── comprehensive_test.py      # Full system validation
│   └── check_documentation.py    # Documentation verification
├── config/             # Configuration files
│   ├── requirements.txt # Python dependencies
│   └── .env            # Environment variables
├── MCP/                # Claude Desktop MCP integration
│   ├── file_server.py  # MCP server for Claude Desktop
│   ├── secret_data.txt # Test data file
│   └── *.json          # MCP configuration files
├── chatGpt_MCP/        # ChatGPT integration alternatives
│   ├── chatgpt_file_api.py         # REST API for file access
│   ├── chatgpt_upload_interface.py # Web upload interface
│   ├── chatgpt_demo.py             # Interactive demo
│   ├── test_chatgpt_integration.py # Test suite
│   └── CHATGPT_INTEGRATION_GUIDE.md # Complete guide
└── README.md          # This documentation
```

## 🎯 Usage

### Simple Script Usage

**Run the educational tutorial:**
```bash
python ai_core/educational_ai_example.py
```

**Run the simple client:**
```bash
python ai_core/simple_ai_client.py
```

**Use in your own code:**
```python
import requests

def ask_ollama(user_message):
    payload = {
        "model": "llama3.2:latest",
        "prompt": f"You are a helpful assistant. User: {user_message}\nAssistant:",
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return response.json()["response"]

# Ask the AI anything
answer = ask_ollama("What is machine learning?")
print(answer)
```

### Web API Service

**Start the API service:**
```bash
cd ai_core && python ai_web_service.py
# or alternatively:
python -m uvicorn ai_core.ai_web_service:app --reload --port 8000
```

**Test with curl:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello AI!"}'
```

**Use in Python:**
```python
import requests

response = requests.post("http://localhost:8000/ask", 
                        json={"message": "Hello AI!"})
print(response.json())
```

**Interactive API documentation:**
Open your browser and visit: `http://localhost:8000/docs`

## 🔧 API Reference

### POST /ask

Send a message to the AI and receive a response.

**Request Body:**
```json
{
  "message": "Your question here"
}
```

**Response:**
```json
{
  "response": "AI's answer here"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the capital of France?"}'
```

**Response:**
```json
{
  "response": "The capital of France is Paris."
}
```

## 🛠️ Customization

### Change AI Model

Edit the model name in any of the files:
```python
"model": "llama3.2:latest"  # Change to your preferred model
```

Available models (install with `ollama pull <model-name>`):
- `llama3.2:latest` - General purpose, good balance
- `llama3.2:3b` - Smaller, faster model
- `codellama` - Optimized for coding tasks
- `mistral` - Another excellent general model

### Modify AI Behavior

Change the system prompt in the payload:
```python
"prompt": f"You are a helpful assistant. User: {user_message}\nAssistant:"
```

Examples:
- `"You are a coding expert. Help with programming questions."`
- `"You are a creative writer. Help write stories and poems."`
- `"You are a helpful teacher. Explain concepts simply."`

## 🚨 Troubleshooting

### Common Issues

**"Connection refused" or "Failed to connect"**
- Make sure Ollama is running: `ollama serve`
- Check if the model exists: `ollama list`

**"Model not found"**
- Install the model: `ollama pull llama3.2:latest`

**"Module not found" errors**
- Activate virtual environment: `source .AIvenv/bin/activate`
- Install dependencies: `pip install -r config/requirements.txt`

**API service won't start**
- Check if port 8000 is already in use
- Try a different port: `cd ai_core && python -c "import uvicorn; uvicorn.run('ai_web_service:app', port=8001)"`

### Checking Service Status

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check if API service is running
curl http://localhost:8000/docs

# List running processes
ps aux | grep ollama
ps aux | grep uvicorn
```

## 📊 Performance Tips

- **Use smaller models** (`llama3.2:3b`) for faster responses
- **Increase RAM** if running larger models
- **Use SSD storage** for better model loading times
- **Close other applications** when running large models

## 🔗 Advanced Integrations

### Claude Desktop MCP (Model Context Protocol)
Located in `MCP/` folder - enables Claude Desktop to read local files securely.

### ChatGPT Integration Alternatives
Located in `chatGpt_MCP/` folder - provides multiple ways to share files with ChatGPT:

- **Upload Interface**: Web-based file upload with copy-to-clipboard functionality
- **REST API**: Programmatic file access for automation
- **Manual Method**: Simple copy-paste workflow

**Quick Start:**
```bash
cd chatGpt_MCP/
python chatgpt_upload_interface.py  # Web interface on port 8002
# or
python chatgpt_file_api.py          # REST API on port 8001
```

See `chatGpt_MCP/CHATGPT_INTEGRATION_GUIDE.md` for complete setup instructions.

## 🤝 Contributing

Feel free to:
- Add new features
- Improve documentation
- Report bugs
- Suggest enhancements

## 📝 License

This project is open source and available under the MIT License.

## 🙋‍♂️ Support

If you have questions or issues:
1. Check the troubleshooting section
2. Verify Ollama is running properly
3. Make sure all dependencies are installed
4. Check the terminal for error messages

---

**Happy AI chatting!** 🤖✨
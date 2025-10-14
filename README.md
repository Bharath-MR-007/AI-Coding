def ask_ollama(user_message):
# Local AI Coding Platform

A professional, privacy-first local AI platform for experimentation, education, and advanced integrations. Supports FastAPI, Ollama, LangChain RAG, ChatGPT Actions, Claude Desktop MCP, and more.

---

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
│   ├── PROGRAM_GUIDE.md     # Program usage guide
│   ├── DIRECTORY_STRUCTURE.md # Directory structure reference
│   ├── GIT_WORKFLOW.md      # Git usage guide
│   ├── GLOSSARY.md          # Technology glossary
│   └── ...                  # Other documentation
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
├── chatgpt_actions/    # ChatGPT Actions API & guides
│   ├── actions_api_server.py       # FastAPI server for Actions
│   ├── openapi.json               # OpenAPI schema for Actions
│   ├── ACTIONS_SETUP_GUIDE.md     # Setup guide for Actions
│   ├── NGROK_SETUP.md             # ngrok setup guide
│   └── ...                        # Other integration docs
├── LangChain/          # Local RAG (LangChain + Ollama + Streamlit)
│   ├── rag_app.py                # Streamlit RAG app
│   ├── requirements.txt          # Dependencies for RAG app
│   ├── README.md                 # RAG app usage guide
│   └── USAGE_GUIDE.md            # Step-by-step usage instructions
├── Alert_llm/          # Alert simulation & LLM troubleshooting
│   ├── alert_simulator.py        # Sends simulated alerts
│   ├── webhook_receiver.py       # Receives alerts, queries LLM
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Project documentation & sample output
├── .AIvenv/            # Python virtual environment
└── README.md           # This documentation
```

---

## � Features
- Local AI processing (no API keys required)
- FastAPI web API and Python script interfaces
- Privacy-first: all data stays on your machine
- LangChain RAG demo (upload your own docs, ask questions)
- ChatGPT Actions and Claude Desktop MCP integrations
- Easy onboarding, professional documentation, and troubleshooting guides

---

## 🛠️ Quickstart

1. **Clone the repository**
2. **Create a virtual environment**
  ```bash
  python -m venv .AIvenv
  source .AIvenv/bin/activate
  ```
3. **Install dependencies**
  ```bash
  pip install -r config/requirements.txt
  pip install -r LangChain/requirements.txt  # For RAG app
  ```
4. **Start Ollama**
  ```bash
  ollama serve
  ollama pull llama3
  ```
5. **Run FastAPI server**
  ```bash
  cd ai_core && python ai_web_service.py
  # or
  python -m uvicorn ai_core.ai_web_service:app --reload --port 8000
  ```
6. **Try the RAG app**
  ```bash
  streamlit run LangChain/rag_app.py
  ```

---

## � Documentation
- See `docs/` for API reference, guides, and troubleshooting
- See `LangChain/README.md` for RAG app usage
- See `chatgpt_actions/ACTIONS_SETUP_GUIDE.md` for ChatGPT Actions
- See `MCP/` for Claude Desktop integration

---

## 📦 Project Highlights

### Alert_llm: Automated Alert Simulation & LLM Troubleshooting

A self-contained Python mini-project for simulating alerts and receiving automated troubleshooting/RCA suggestions from a local Ollama LLM.

- **Location:** `Alert_llm/`
- **Features:**
  - Simulates realistic alerts and sends them to a webhook
  - Receives alerts, prints them, and queries a local LLM for troubleshooting/root cause analysis
  - Includes a sample output in its own README
- **How to use:**
  - See [`Alert_llm/README.md`](./Alert_llm/README.md) for setup, usage, and sample output

---

## 🤝 Contributing
- Fork, branch, and submit PRs
- See `docs/GIT_WORKFLOW.md` for workflow
- All contributions welcome!

---

## 📝 License
MIT License

---

**Happy AI building!** 🚀🤖
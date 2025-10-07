# Project Glossary: AI-CODING Technologies

**RAG (Retrieval-Augmented Generation):**
A hybrid AI approach that retrieves relevant documents or text chunks from a knowledge base and then uses a language model to generate answers based on those documents. Enables grounded, document-aware Q&A. Used in this project with LangChain, Ollama, and Streamlit.

**FastAPI:**
A modern, high-performance Python web framework for building APIs. It provides automatic interactive documentation and is used here to expose AI models as RESTful endpoints (e.g., in `AIService.py`).

**MCP (Model Context Protocol):**
A protocol that allows AI assistants (like Claude or ChatGPT) to securely interact with local tools and data, such as reading files. In this project, MCP enables local file access for AI via a dedicated server.

**Streamlit:**
An open-source Python library for building interactive web apps for data science and machine learning. Used in this project to create the user interface for uploading documents and asking questions in the RAG demo.

**LangChain:**
A framework for building applications powered by language models. It provides tools for chaining together LLMs, retrievers, and other components. Used here to build the RAG pipeline connecting document retrieval, embeddings, and LLMs.

**Ollama:**
A local AI inference engine that runs LLMs (like Llama 3) on your machine. Provides privacy, speed, and no dependency on cloud APIs. Used as the backend for all LLM tasks in this project.

**ChatGPT Actions:**
A feature that allows custom GPTs to call external APIs, enabling integration between ChatGPT and your local AI services. This project includes guides and servers to enable this integration.

**ngrok:**
A tunneling tool that exposes local servers to the internet via secure public URLs. Used in this project to make local FastAPI or Streamlit endpoints accessible to external services (like ChatGPT Actions) over HTTPS, even behind firewalls or NAT.

**Uvicorn:**
A lightning-fast ASGI server for Python web apps, commonly used to run FastAPI applications in production or development.

**Pydantic:**
A Python library for data validation and settings management using Python type annotations. Used in FastAPI for request/response data models.

**Claude Desktop:**
An AI assistant by Anthropic, referenced in this project for local file access via MCP integration.

**Python Virtual Environment (.AIvenv):**
A self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages. Used to isolate project dependencies.

**REST API:**
An architectural style for designing networked applications. In this project, REST APIs are used to interact with local AI models and file servers.

**Swagger/OpenAPI:**
A specification and set of tools for describing and documenting RESTful APIs. FastAPI auto-generates OpenAPI docs for your endpoints.

**Test Suite (Pytest):**
Automated tests (often using pytest) to validate the functionality of scripts, APIs, and integrations in the project.

**Ollama Model (Llama 3):**
The specific large language model (LLM) used for local inference in this project, downloaded and run via Ollama.

**File Server:**
A simple HTTP server (e.g., in MCP or chatGpt_MCP) that allows secure file access for AI assistants.

**API Client:**
Scripts or tools that send requests to an API endpoint and process the responses. Used for both demonstration and integration testing.

---

For more details, see the respective README and documentation files in each folder.

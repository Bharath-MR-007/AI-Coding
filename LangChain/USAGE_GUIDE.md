# Local RAG App: LangChain + Ollama + Streamlit

This guide explains how to set up and use the local Retrieval-Augmented Generation (RAG) app that integrates LangChain, Ollama, and Streamlit.

## Features
- Upload your own text files and ask questions about them
- Uses Ollama (llama3) for embeddings and LLM inference
- Runs entirely on your local machine

## Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/) installed and running
- [Streamlit](https://streamlit.io/) (installed via requirements.txt)

## Setup Steps

1. **Clone or copy the LangChain folder into your project.**

2. **Create and activate a Python virtual environment (if not already):**
   ```sh
   python3 -m venv .AIvenv
   source .AIvenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r LangChain/requirements.txt
   pip install -U langchain-community
   ```

4. **Download the Ollama model (llama3):**
   ```sh
   ollama pull llama3
   ```

5. **Run the Streamlit app:**
   ```sh
   streamlit run LangChain/rag_app.py
   ```
   - Open the URL shown in the terminal (usually http://localhost:8501)

## Usage
1. **Upload one or more .txt files using the sidebar.**
2. **Enter your question in the main input box.**
3. **Click "Get Answer" to see a response grounded in your documents.**

## Troubleshooting
- If you see a model not found error, make sure you have run `ollama pull llama3`.
- If you see a duplicate button error, update the app to use unique keys for each button.
- If you get a missing module error for `langchain_community`, run `pip install -U langchain-community`.

## Notes
- All processing is local; no data is sent to the cloud.
- You can use other Ollama models by changing the model name in `rag_app.py`.

---
For more details, see the code and comments in `LangChain/rag_app.py`.

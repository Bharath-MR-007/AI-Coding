# AIService.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Define the structure of incoming request data
class UserPrompt(BaseModel):
    message: str

app = FastAPI(title="Local AI API", description="Ask your local Ollama model questions via FastAPI")

@app.post("/ask")
def ask_ollama(prompt: UserPrompt):
    """Send user prompt to local Ollama model and return AI response"""
    payload = {
        "model": "llama3.2:latest",
        "prompt": f"You are a helpful assistant.\nUser: {prompt.message}\nAssistant:",
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        return {"response": response.json()["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

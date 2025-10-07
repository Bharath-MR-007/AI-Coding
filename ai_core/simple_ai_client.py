import requests

def ask_ollama(user_message):
    payload = {
        "model": "llama3.2:latest",
        "prompt": f"You are a helpful assistant. User: {user_message}\nAssistant:",
        "stream": False
    }
    
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return response.json()["response"]

user_question = "What is the capital of France?"
ai_response = ask_ollama(user_question)
print(ai_response)
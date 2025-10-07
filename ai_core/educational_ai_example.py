# Import the library that lets us talk to websites/APIs over the internet
import requests

# Create a function that sends questions to the AI and gets answers back
def ask_ollama(user_message):
    # Package up our request with all the info the AI needs
    payload = {
        "model": "llama3.2:latest",  # Tell it which AI brain to use
        "prompt": f"You are a helpful assistant. User: {user_message}\nAssistant:",  # Give the AI context and our question
        "stream": False  # Get the full answer at once, not word by word
    }
    
    # Send our packaged request to the AI running on our computer
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    # Extract just the AI's text answer from the response and send it back
    return response.json()["response"]

# Example usage - let's try asking the AI something
user_question = "What is the capital of France?"  # This is our test question
ai_response = ask_ollama(user_question)  # Send the question to AI and get the answer
print(ai_response)  # Show the AI's answer on the screen
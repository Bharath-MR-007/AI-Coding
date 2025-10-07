#!/usr/bin/env python3
"""
Quick test script to verify AI functionality
"""
import requests

def test_ai_connection():
    """Test the AI connection with a dynamic question"""
    print("🧪 Testing AI Connection...")
    
    # Test question
    test_question = "What is 5 + 3? Give just the number."
    
    payload = {
        "model": "llama3.2:latest",
        "prompt": f"You are a helpful assistant. User: {test_question}\nAssistant:",
        "stream": False
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            result = response.json()["response"]
            print(f"✅ AI Response: {result.strip()}")
            return True
        else:
            print(f"❌ AI request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI connection error: {e}")
        return False

if __name__ == "__main__":
    test_ai_connection()
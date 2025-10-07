import requests

def ask_ai(question):
    try:
        response = requests.post("http://localhost:8000/ask", json={"message": question})
        return response.json()["response"]
    except:
        return "Error: Cannot connect to AI service"

def chat():
    print("🤖 AI Chat - Type 'quit' to exit")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            break
        if question:
            print(f"AI: {ask_ai(question)}")

if __name__ == "__main__":
    # Test with example
    print(f"Example: {ask_ai('Hello AI!')}")
    
    # Start chat
    chat()
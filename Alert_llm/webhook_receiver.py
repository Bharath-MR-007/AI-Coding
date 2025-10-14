from flask import Flask, request
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"  # Change to your preferred model name


def get_ollama_response(alert_summary):
    prompt = f"You are an expert SRE. Given this alert, provide troubleshooting steps and a possible root cause analysis (RCA):\n\n{alert_summary}\n\nRespond with clear, actionable steps and a short RCA."
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "[No response from LLM]")
        else:
            return f"[Ollama error: {response.status_code} {response.text}]"
    except Exception as e:
        return f"[Ollama exception: {e}]"


@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    print("\n🚨 Received alert:")
    print(data)

    # Extract a summary for LLM
    try:
        alert = data["alerts"][0]
        summary = alert["annotations"].get("summary", "")
        description = alert["annotations"].get("description", "")
        alertname = alert["labels"].get("alertname", "")
        severity = alert["labels"].get("severity", "")
        alert_summary = f"Alert: {alertname}\nSeverity: {severity}\nSummary: {summary}\nDescription: {description}"
    except Exception:
        alert_summary = str(data)

    print("\n🤖 Sending to Ollama for troubleshooting and RCA...")
    ollama_response = get_ollama_response(alert_summary)
    print("\n🧠 Ollama Response:")
    print(ollama_response)

    return "OK", 200

if __name__ == "__main__":
    print("🔔 Starting webhook receiver on http://localhost:8200/alert")
    app.run(host="0.0.0.0", port=8200)

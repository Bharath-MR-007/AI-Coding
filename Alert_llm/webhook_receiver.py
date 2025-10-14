from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODELS = ["llama3"]  # Add more models for multi-model reasoning
ALERT_LOG_FILE = "alert_log.json"


def get_ollama_response(alert_summary, model):
    prompt = (
        "You are an expert SRE. Given this alert, provide a structured response in JSON with these fields:\n"
        "1. troubleshooting_steps: List of immediate troubleshooting steps\n"
        "2. possible_root_causes: List of possible root causes\n"
        "3. recommended_actions: List of next actions\n"
        f"\nAlert details:\n{alert_summary}\n"
        "Respond ONLY with a valid JSON object."
    )
    payload = {
        "model": model,
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


def log_alert(alert_data):
    with open(ALERT_LOG_FILE, "a") as f:
        f.write(json.dumps(alert_data) + "\n")


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
        region = alert["labels"].get("region", "")
        instance = alert["labels"].get("instance", "")
        alert_summary = (
            f"Alert: {alertname}\nSeverity: {severity}\nRegion: {region}\nInstance: {instance}\n"
            f"Summary: {summary}\nDescription: {description}"
        )
    except Exception:
        alert_summary = str(data)

    model_responses = {}
    for model in OLLAMA_MODELS:
        print(f"\n🤖 Sending to Ollama ({model}) for structured RCA...")
        raw_response = get_ollama_response(alert_summary, model)
        # Try to extract JSON from Markdown code block or extra text
        import re
        def extract_json(text):
            # Look for JSON inside triple backticks
            match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
            if match:
                candidate = match.group(1)
            else:
                # Fallback: try to find first curly brace and parse from there
                idx = text.find('{')
                if idx != -1:
                    candidate = text[idx:]
                else:
                    candidate = text
            try:
                return json.loads(candidate)
            except Exception:
                return {"error": "Could not parse LLM response as JSON", "raw": text}

        structured = extract_json(raw_response)
        model_responses[model] = structured
        print(f"\n🧠 Ollama ({model}) Response:")
        print(json.dumps(structured, indent=2))

    # Log alert and all model responses
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "alert": data,
        "model_responses": model_responses
    }
    log_alert(log_entry)

    # Return structured JSON to client
    return jsonify(log_entry), 200


if __name__ == "__main__":
    print("🔔 Starting webhook receiver on http://localhost:8200/alert")
    app.run(host="0.0.0.0", port=8200)

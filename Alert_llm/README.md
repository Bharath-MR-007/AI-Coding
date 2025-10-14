# Alert_llm

A minimal Python project to simulate alert generation and receive alerts via a webhook, with automated troubleshooting and RCA suggestions using a local Ollama LLM.

## Features
- **alert_simulator.py**: Periodically sends realistic alert payloads to a webhook endpoint.
- **webhook_receiver.py**: Receives alerts, prints them, and queries a local Ollama LLM for troubleshooting and root cause analysis (RCA) suggestions.
- **Ollama LLM Integration**: Automatically sends alert summaries to a local LLM (e.g., llama3) for expert SRE advice.

---

## Setup

### 1. Clone and enter the project directory
```
cd /Users/bharathmr/Documents/AI-Coding/Alert_llm
```

### 2. (Optional) Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

---

## Usage

### Start the Webhook Receiver
This will listen for alerts and print both the alert and the LLM's troubleshooting/RCA response.

```
python webhook_receiver.py
```

- The receiver listens on `http://localhost:8080/alert` (POST only).
- Alerts received are printed in the terminal.
- Each alert is sent to Ollama (default: `llama3` at `http://localhost:11434/api/generate`).
- The LLM's response is printed after each alert.

### Start the Alert Simulator
In a separate terminal:

```
python alert_simulator.py
```

- Sends a random alert every 10 seconds to the webhook receiver.
- You can adjust the interval and webhook URL in the script.

---

## Configuration

- **alert_simulator.py**
  - `WEBHOOK_URL`: Change this to your webhook receiver endpoint if needed.
  - `SEND_INTERVAL`: Seconds between alerts.
  - `ALERT_TEMPLATES`: Customize or add alert types.

- **webhook_receiver.py**
  - `OLLAMA_URL`: Change if your Ollama API is running elsewhere.
  - `OLLAMA_MODEL`: Set to your preferred local LLM (e.g., `llama3`, `mistral`).
  - The prompt sent to the LLM can be customized in the code.

---

## Requirements
- Python 3.7+
- [Ollama](https://ollama.com/) running locally with a supported model (default: `llama3`)
- Flask
- Requests

Install all dependencies with:
```
pip install -r requirements.txt
```

---

## Example Workflow
1. Start Ollama and load your model (e.g., `ollama run llama3`).
2. Start the webhook receiver: `python webhook_receiver.py`
3. Start the alert simulator: `python alert_simulator.py`
4. Watch the receiver terminal for alerts and LLM troubleshooting suggestions.

---

## Notes
- The webhook endpoint only accepts POST requests. Accessing it via browser (GET) will show "Method Not Allowed".
- All code is in the `Alert_llm` folder.
- You can extend the receiver to forward alerts to other systems, store results, or trigger automations.

---

## License
MIT

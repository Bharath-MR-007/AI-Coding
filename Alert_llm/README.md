# Alert_llm

A minimal Python project to simulate alert generation and receive alerts via a webhook, with automated troubleshooting and RCA suggestions using a local Ollama LLM.


## Features
- **alert_simulator.py**: Periodically sends realistic alert payloads (with region, instance, timestamps, and random recovery) to a webhook endpoint. All generated alerts are exported to `alerts_log.json` for future analysis or Grafana ingestion.
- **webhook_receiver.py**: Receives alerts, prints them, queries a local Ollama LLM for troubleshooting and root cause analysis (RCA) suggestions, and logs every alert and LLM response to `alert_log.json`.
- **Robust LLM Output Parsing**: The receiver automatically extracts and parses JSON from LLM responses, even if wrapped in Markdown code blocks or extra text, ensuring reliable structured output.
- **Ollama LLM Integration**: Automatically sends alert summaries to a local LLM (e.g., llama3) for expert SRE advice. Multi-model support is ready for future expansion.

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
This will listen for alerts, print them, query the LLM, and log all activity.

```
python webhook_receiver.py
```

- The receiver listens on `http://localhost:8200/alert` (POST only).
- Alerts received are printed in the terminal.
- Each alert is sent to Ollama (default: `llama3` at `http://localhost:11434/api/generate`).
- The LLM's response is printed after each alert and logged to `alert_log.json` along with the original alert and timestamp.
- The receiver robustly extracts JSON from LLM responses, even if wrapped in Markdown code blocks or extra text.

### Start the Alert Simulator
In a separate terminal:

```
python alert_simulator.py
```

- Sends a random alert every 10 seconds to the webhook receiver (now on port 8200).
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


## Sample Output

When you run both scripts, your webhook receiver terminal will show output like this:

```
🔔 Starting webhook receiver on http://localhost:8200/alert

🚨 Received alert:
{ ...alert JSON... }

🤖 Sending to Ollama (llama3) for structured RCA...

🧠 Ollama (llama3) Response:
{
  "troubleshooting_steps": [ ... ],
  "possible_root_causes": [ ... ],
  "recommended_actions": [ ... ]
}

127.0.0.1 - - [14/Oct/2025 17:47:39] "POST /alert HTTP/1.1" 200 -
```

You will see a new block for each alert, with the LLM's structured troubleshooting steps, root causes, and recommended actions printed and logged after every alert received.

If the LLM response is not valid JSON (e.g., wrapped in Markdown code blocks), the receiver will automatically extract and parse the JSON. If parsing still fails, the raw LLM output and error will be logged for troubleshooting.

---


## Notes
- The webhook endpoint only accepts POST requests. Accessing it via browser (GET) will show "Method Not Allowed".
- All code is in the `Alert_llm` folder.
- All received alerts and LLM responses are logged to `alert_log.json` (receiver) and `alerts_log.json` (simulator) for audit and analysis.
- The receiver is robust to LLM output formatting issues and will log any parsing errors for further debugging.
- You can extend the receiver to forward alerts to other systems, store results, or trigger automations.

---

## License
MIT

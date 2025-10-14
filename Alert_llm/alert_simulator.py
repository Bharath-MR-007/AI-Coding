import requests
import random
import time
import json
from datetime import datetime, timedelta

# --- CONFIG ---
WEBHOOK_URL = "http://localhost:8080/alert"  # Change this to your webhook receiver
SEND_INTERVAL = 10  # seconds between alerts

# --- SAMPLE ALERT TYPES ---
ALERT_TEMPLATES = [
    {
        "alertname": "HighAPILatency",
        "severity": "critical",
        "summary": "High API latency detected",
        "description": "95th percentile latency for target http://labmuc-sysm-gnm-02.lan.ts-ian.net/nnm is greater than 500ms for the last 5 minutes."
    },
    {
        "alertname": "SlowDNSResolution",
        "severity": "warning",
        "summary": "Slow DNS resolution detected",
        "description": "90th percentile DNS resolution time is greater than 100ms for the last 5 minutes."
    },
    {
        "alertname": "TracerouteFailure",
        "severity": "critical",
        "summary": "Traceroute to external target failed",
        "description": "Traceroute to 8.8.8.8 exceeded hop limit, indicating possible routing issue."
    },
    {
        "alertname": "NNMINodeDown",
        "severity": "critical",
        "summary": "OpenText NNMi Node Down Alert",
        "description": "Node labmuc-router-01 is unreachable from NNMi for more than 10 minutes."
    },
    {
        "alertname": "NNMIHighCPU",
        "severity": "warning",
        "summary": "High CPU utilization detected in NNMi node",
        "description": "CPU utilization on node labmuc-sysm-gnm-02 exceeded 85% for last 10 minutes."
    }
]

def generate_alert_payload(alert_template, status="active"):
    now = datetime.utcnow()
    payload = {
        "receiver": "web.hook",
        "status": "firing" if status == "active" else "resolved",
        "alerts": [
            {
                "status": status,
                "labels": {
                    "alertname": alert_template["alertname"],
                    "severity": alert_template["severity"],
                    "prometheus": "labmuc-sysm-dpg-01"
                },
                "annotations": {
                    "summary": alert_template["summary"],
                    "description": alert_template["description"]
                },
                "startsAt": (now - timedelta(minutes=5)).isoformat() + "Z",
                "endsAt": (now + timedelta(minutes=5)).isoformat() + "Z",
                "generatorURL": "http://prometheus.example.com/graph",
                "fingerprint": hex(random.getrandbits(64))[2:]
            }
        ],
        "groupLabels": {"alertname": alert_template["alertname"]},
        "commonLabels": {"severity": alert_template["severity"]},
        "commonAnnotations": {"summary": alert_template["summary"]},
        "externalURL": "http://alertmanager.example.com",
        "version": "4",
        "groupKey": f"{{alertname=\"{alert_template['alertname']}\"}}"
    }
    return payload

def send_alert():
    alert_template = random.choice(ALERT_TEMPLATES)
    # 80% chance of firing, 20% chance of resolved
    status = "active" if random.random() > 0.2 else "resolved"
    payload = generate_alert_payload(alert_template, status)

    print(f"\n🚨 Sending {status.upper()} alert: {alert_template['alertname']}")
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Alert sent successfully to {WEBHOOK_URL}")
    else:
        print(f"❌ Failed to send alert ({response.status_code}): {response.text}")

    # Print JSON for debugging
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    print("🔧 Starting Alertmanager Webhook Simulator...")
    print(f"Target Webhook: {WEBHOOK_URL}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            send_alert()
            time.sleep(SEND_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Stopped alert simulation.")

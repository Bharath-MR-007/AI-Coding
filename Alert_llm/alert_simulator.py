import requests
import random
import time
import json
from datetime import datetime, timedelta
import threading

# --- CONFIG ---
WEBHOOK_URL = "http://localhost:8200/alert"  # Change this to your webhook receiver
SEND_INTERVAL = 10  # seconds between alerts
ALERT_LOG_FILE = "alerts_log.json"

REGIONS = ["us-east-1", "eu-west-1", "ap-south-1", "us-west-2"]
INSTANCES = [
    "prod-app-01", "prod-app-02", "db-primary-01", "db-replica-01",
    "edge-gateway-01", "edge-gateway-02", "cache-01", "cache-02"
]

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

all_alerts = []  # For exporting to JSON

def generate_alert_payload(alert_template, status="active"):
    now = datetime.utcnow()
    region = random.choice(REGIONS)
    instance = random.choice(INSTANCES)
    payload = {
        "receiver": "web.hook",
        "status": "firing" if status == "active" else "resolved",
        "alerts": [
            {
                "status": status,
                "labels": {
                    "alertname": alert_template["alertname"],
                    "severity": alert_template["severity"],
                    "region": region,
                    "instance": instance,
                    "prometheus": "labmuc-sysm-dpg-01"
                },
                "annotations": {
                    "summary": alert_template["summary"],
                    "description": alert_template["description"]
                },
                "startsAt": (now - timedelta(minutes=random.randint(1, 10))).isoformat() + "Z",
                "endsAt": (now + timedelta(minutes=random.randint(5, 15))).isoformat() + "Z",
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

def send_alert(thread_id=1):
    alert_template = random.choice(ALERT_TEMPLATES)
    # 80% chance of firing, 20% chance of resolved
    status = "active" if random.random() > 0.2 else "resolved"
    payload = generate_alert_payload(alert_template, status)
    all_alerts.append(payload)

    print(f"\n[Thread {thread_id}] 🚨 Sending {status.upper()} alert: {alert_template['alertname']}")
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            print(f"✅ Alert sent successfully to {WEBHOOK_URL}")
        else:
            print(f"❌ Failed to send alert ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Exception sending alert: {e}")

    # Print JSON for debugging
    print(json.dumps(payload, indent=2))

def alert_thread(thread_id):
    print(f"[Thread {thread_id}] Started.")
    try:
        while True:
            send_alert(thread_id)
            time.sleep(SEND_INTERVAL + random.randint(-2, 2))
    except KeyboardInterrupt:
        print(f"[Thread {thread_id}] Stopped.")

if __name__ == "__main__":
    print("🔧 Starting Alertmanager Webhook Simulator (multi-threaded)...")
    print(f"Target Webhook: {WEBHOOK_URL}")
    print("Press Ctrl+C to stop.\n")

    threads = []
    num_threads = 2  # Simulate 2 concurrent alert sources
    for i in range(num_threads):
        t = threading.Thread(target=alert_thread, args=(i+1,), daemon=True)
        threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopped alert simulation. Exporting alerts to alerts_log.json...")
        with open(ALERT_LOG_FILE, "w") as f:
            json.dump(all_alerts, f, indent=2)
        print(f"Exported {len(all_alerts)} alerts to {ALERT_LOG_FILE}")

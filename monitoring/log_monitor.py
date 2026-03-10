import time
import json
import os
import subprocess

ALERTS_FILE = os.path.join(os.path.dirname(__file__), "..", "alerts", "alerts.json")
PROCESSED_ALERTS_FILE = os.path.join(os.path.dirname(__file__), ".processed_alerts.txt")
AGENT_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "agent", "soc_agent.py")

def load_processed_alerts():
    if os.path.exists(PROCESSED_ALERTS_FILE):
        with open(PROCESSED_ALERTS_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_processed_alert(alert_id):
    with open(PROCESSED_ALERTS_FILE, "a") as f:
        f.write(f"{alert_id}\n")

def parse_alert(raw_alert_json):
    """
    Extracts key fields from the raw alert JSON.
    Returns a simplified dictionary.
    """
    try:
        alert = json.loads(raw_alert_json)
    except json.JSONDecodeError:
        return None

    if not alert:
        return None

    # Handle both Wazuh format and flat dictionary format
    rule_id = alert.get("rule", {}).get("id") or alert.get("rule_id", "Unknown")
    rule_description = alert.get("rule", {}).get("description") or alert.get("rule_description", "Unknown")
    severity = alert.get("rule", {}).get("level") or alert.get("severity", "Unknown")
    
    # Extract source IP from different possible fields
    source_ip = alert.get("data", {}).get("srcip") or alert.get("source_ip", "Unknown")
    if source_ip == "Unknown" and "agent" in alert:
        source_ip = alert["agent"].get("ip", "Unknown")
        
    timestamp = alert.get("timestamp", "Unknown")
    
    # Fallback to check if it's our simplified format already
    if not isinstance(alert.get("rule"), dict) and "rule_id" not in alert:
        # If the input format varies, attempt basic extractions
        pass

    # Create a unique alert ID string to prevent duplicates
    alert_id = f"{timestamp}_{rule_id}_{source_ip}"

    # Simplified format
    simplified_alert = {
        "id": alert_id,
        "rule_id": str(rule_id),
        "rule_description": str(rule_description),
        "severity": str(severity),
        "source_ip": str(source_ip),
        "timestamp": str(timestamp)
    }

    return simplified_alert

def main():
    print(f"Starting log monitor... watching {ALERTS_FILE}")
    processed_alerts = load_processed_alerts()
    print(f"Loaded {len(processed_alerts)} processed alerts.")

    while True:
        try:
            if not os.path.exists(ALERTS_FILE):
                time.sleep(2)
                continue

            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line or line == "{}":
                    continue

                parsed = parse_alert(line)
                if not parsed:
                    continue

                alert_id = parsed["id"]
                if alert_id not in processed_alerts:
                    print(f"\n[!] New Alert Detected: {parsed['rule_description']}")
                    processed_alerts.add(alert_id)
                    save_processed_alert(alert_id)
                    
                    # Send alert to the AI SOC agent
                    simplified_json = json.dumps(parsed)
                    print(f"Sending to AI SOC agent: {simplified_json}")
                    
                    try:
                        subprocess.Popen(
                            ["python", AGENT_SCRIPT, simplified_json],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                    except Exception as e:
                        print(f"Error starting soc_agent: {e}")

        except Exception as e:
            print(f"Error reading file: {e}")

        time.sleep(5)

if __name__ == "__main__":
    main()

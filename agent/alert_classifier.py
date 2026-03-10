import json
import sys

def classify_alert(alert_description: str) -> str:
    """Classifies a security alert based on keyword matching."""
    alert_lower = alert_description.lower()

    if any(keyword in alert_lower for keyword in ["authentication failure", "failed login", "brute force"]):
        return "brute_force"
    elif any(keyword in alert_lower for keyword in ["email", "phishing", "malicious link"]):
        return "phishing"
    elif any(keyword in alert_lower for keyword in ["malware", "trojan", "virus"]):
        return "malware"
    elif any(keyword in alert_lower for keyword in ["privilege", "root", "sudo", "escalation"]):
        return "privilege_escalation"
    elif any(keyword in alert_lower for keyword in ["lateral", "smb", "rdp", "pass-the-hash"]):
        return "lateral_movement"
    else:
        return "unknown"

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No alert description provided"}))
        sys.exit(1)

    alert_desc = sys.argv[1]
    alert_type = classify_alert(alert_desc)
    
    print(json.dumps({"alert_type": alert_type}))

if __name__ == "__main__":
    main()

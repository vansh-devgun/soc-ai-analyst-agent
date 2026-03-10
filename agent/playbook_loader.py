import os
import json
import sys

def load_playbook(alert_type: str) -> str:
    """Loads the appropriate SOC playbook based on alert class."""
    if alert_type not in ["brute_force", "phishing", "malware", "privilege_escalation", "lateral_movement"]:
        return "No specific playbook found for this alert type. Analyze generally."
    
    # We are under the agent/ directory typically, so go up one level to playbooks/
    # If run from the project root, this path should be playbooks/
    path = os.path.join(os.path.dirname(__file__), "..", "playbooks", f"{alert_type}_playbook.md")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Playbook file not found at {path}. Analyze generally."

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No alert type provided"}))
        sys.exit(1)

    alert_type = sys.argv[1]
    playbook_content = load_playbook(alert_type)
    
    # Output JSON so it can be parsed by other scripts/n8n
    print(json.dumps({"playbook_content": playbook_content}))

if __name__ == "__main__":
    main()

import json
import sys
import subprocess
import os
import requests

PLAYBOOK_LOADER = os.path.join(os.path.dirname(__file__), "playbook_loader.py")
ALERT_CLASSIFIER = os.path.join(os.path.dirname(__file__), "alert_classifier.py")
DASHBOARD_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "dashboard", "analyzed_alerts.json")

def generate_soc_report(alert, analysis):
    """Generates the final SOC investigation report."""
    report = f"""
SOC INCIDENT REPORT

Alert Type: {analysis.get('attack_type', 'Unknown')}
Source IP: {alert.get('source_ip', 'Unknown')}
Severity: {alert.get('severity', 'Unknown')}

MITRE Technique: {analysis.get('mitre_technique', 'Unknown')}
Attack Description:
{analysis.get('attack_description', alert.get('rule_description', 'No description available.'))}

Recommended SOC Response:
{analysis.get('recommended_response', 'No specific recommendation provided.')}

Playbook Actions:
{analysis.get('playbook_actions', 'No specific playbook actions.')}
"""
    return report.strip()

def analyze_with_ollama(prompt):
    """Sends the prompt to a local Ollama model."""
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Parse the JSON response from Ollama
        try:
            return json.loads(result.get("response", "{}"))
        except json.JSONDecodeError:
            print("Failed to decode JSON from Ollama response.", file=sys.stderr)
            return {}
            
    except Exception as e:
        print(f"Ollama API Error: {e}", file=sys.stderr)
        return {}

def main():
    if len(sys.argv) < 2:
        print("Error: No parsed alert JSON provided.")
        sys.exit(1)

    try:
        alert = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Invalid JSON provided.")
        sys.exit(1)

    print(f"Processing Alert ID: {alert.get('id', 'Unknown')}")

    # 1. Classify Alert
    classifier_cmd = ["python", ALERT_CLASSIFIER, alert.get("rule_description", "")]
    classifier_proc = subprocess.run(classifier_cmd, capture_output=True, text=True)
    
    classification = "unknown"
    try:
        class_res = json.loads(classifier_proc.stdout)
        classification = class_res.get("alert_type", "unknown")
    except json.JSONDecodeError:
        print("Warning: Could not classify alert properly.")

    # 2. Load Playbook based on Classification
    playbook_cmd = ["python", PLAYBOOK_LOADER, classification]
    playbook_proc = subprocess.run(playbook_cmd, capture_output=True, text=True)
    
    playbook_actions = "No specific playbook found."
    try:
        pb_res = json.loads(playbook_proc.stdout)
        playbook_actions = pb_res.get("playbook_content", "No specific playbook found.")
    except json.JSONDecodeError:
        pass

    # 3. Analyze with AI Model
    prompt = f"""
You are an expert AI SOC Analyst. Analyze the following security alert and provide a structured JSON response.

Alert Context:
- Rule ID: {alert.get('rule_id')}
- Description: {alert.get('rule_description')}
- Severity: {alert.get('severity')}
- Source IP: {alert.get('source_ip')}
- Timestamp: {alert.get('timestamp')}
- Target Classification: {classification}

Related SOC Playbook:
{playbook_actions}

Provide the output strictly in this JSON format:
{{
    "attack_type": "Brief classification name",
    "mitre_technique": "TXXXX - Name",
    "severity_assessment": "High/Medium/Low with brief justification",
    "attack_description": "2-3 sentences max explaining what happened",
    "recommended_response": "1-2 sentences on immediate mitigation steps"
}}
"""
    
    ai_analysis = analyze_with_ollama(prompt)
    ai_analysis["playbook_actions"] = playbook_actions

    # 4. Generate Final SOC Report
    final_report = generate_soc_report(alert, ai_analysis)
    print("\n" + "="*50 + "\n" + final_report + "\n" + "="*50 + "\n")

    # 5. Save to dashboard data file
    dashboard_data = {
        "id": alert.get("id"),
        "timestamp": alert.get("timestamp"),
        "rule_id": alert.get("rule_id"),
        "source_ip": alert.get("source_ip"),
        "severity": alert.get("severity", "Unknown"),
        "attack_type": classification,
        "mitre_technique": ai_analysis.get("mitre_technique", "Unknown"),
        "report": final_report
    }

    try:
        os.makedirs(os.path.dirname(DASHBOARD_DATA_FILE), exist_ok=True)
        
        existing_data = []
        if os.path.exists(DASHBOARD_DATA_FILE):
            with open(DASHBOARD_DATA_FILE, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
                    
        existing_data.append(dashboard_data)
        
        with open(DASHBOARD_DATA_FILE, "w") as f:
            json.dump(existing_data, f, indent=4)
            
    except Exception as e:
        print(f"Error saving to dashboard data file: {e}")

if __name__ == "__main__":
    main()

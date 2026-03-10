# SOC AI Analyst Agent

## Overview

The **SOC AI Analyst Agent** is a cybersecurity project that simulates the workflow of a **Tier-1 Security Operations Center (SOC) Analyst**.

The system monitors system logs, detects suspicious activities, analyzes alerts using a **SOC playbook**, maps attacks to **MITRE ATT&CK techniques**, and generates automated **incident response reports**.

This project demonstrates how **AI and automation can assist SOC teams in detecting and responding to cyber threats.**

---

## Project Goals

* Automate log monitoring
* Detect security alerts
* Analyze alerts using SOC playbooks
* Map attacks to MITRE ATT&CK techniques
* Generate SOC-style incident reports
* Demonstrate attacks in a controlled lab environment

---

## System Architecture

Wazuh → `alerts.json` → `log_monitor.py` → AI SOC Agent (`soc_agent.py`) → MITRE mapping & Playbook loader → Dashboard (`dashboard.py`)

---

## Project Structure

```
soc-ai-analyst-agent
│
├── agent
│   ├── soc_agent.py
│   ├── alert_classifier.py
│   └── playbook_loader.py
│
├── monitoring
│   ├── log_monitor.py
│   └── n8n_soc_ai_workflow.json
│
├── playbooks
│   ├── brute_force_playbook.md
│   ├── malware_playbook.md
│   ├── phishing_playbook.md
│   ├── privilege_escalation_playbook.md
│   └── lateral_movement_playbook.md
│
├── alerts
│   └── alerts.json
│
├── attack_simulation
│   ├── attack_notes.md
│   └── simulate_brute_force.sh
│
├── dashboard
│   ├── dashboard.py
│   └── analyzed_alerts.json (Generated)
│
├── docs
│   ├── architecture.md
│   └── local_ai_soc_agent_setup.md
│
├── requirements.txt
└── README.md
```

---

## Components

### Log Monitoring System

A Python script that continuously monitors system logs for suspicious activity.

Example logs monitored:

* `/var/log/auth.log`
* Sysmon logs
* System security logs

---

### Alert Engine

When suspicious activity is detected, the system generates a structured alert containing:

* Timestamp
* Alert type
* Source IP
* Raw log data

---

### SOC Playbook

The SOC playbook defines how the system should analyze and respond to different attack scenarios.

Example attacks:

* SSH Brute Force
* Port Scanning
* Failed Login Attempts
* Privilege Escalation

Each playbook entry includes:

* Attack description
* MITRE ATT&CK technique
* Severity level
* Investigation steps
* Recommended response

---

### SOC AI Agent

The SOC AI agent processes alerts and generates an analysis report similar to a SOC analyst.

Example output:

SOC INCIDENT REPORT

Alert Type: SSH Brute Force
MITRE Technique: T1110
Severity: High

Recommended Actions:

* Block the attacking IP
* Check successful login attempts
* Reset affected credentials
* Enable multi-factor authentication

---

### Attack Simulation

Attacks are simulated using a controlled lab environment.

Example attacks:

SSH Brute Force
Port scanning
Credential attacks

These attacks generate logs that the monitoring system detects.

---

### Dashboard (Optional)

A dashboard may be added to visualize:

* Alerts
* Attack types
* Severity levels
* Response recommendations

---

## Technologies Used

* Python
* Linux Log Monitoring
* MITRE ATT&CK Framework
* Virtual Machines
* Streamlit 
* Cybersecurity Automation

---

## Lab Setup & Installation

**1. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

**2. Setup Wazuh (Optional but recommended)**
- Install the Wazuh manager and configure agents.
- Ensure alerts are logged in line-separated JSON format to `alerts/alerts.json`.

**3. Set up n8n**
- Run `npx n8n`
- Import the `monitoring/n8n_soc_ai_workflow.json` workflow.

**4. Set up Ollama**
- Install Ollama from [ollama.com](https://ollama.com).
- Pull the model: `ollama run llama3` (Ensure it is running locally on port 11434).

**5. Start the Agent & Monitor**
```bash
python monitoring/log_monitor.py
```

**6. Start the Dashboard**
```bash
streamlit run dashboard/dashboard.py
```

**7. Run an Attack Simulation**
```bash
bash attack_simulation/simulate_brute_force.sh
```

---

## Future Improvements

* Threat intelligence integration (VirusTotal / AbuseIPDB)
* Automated response actions
* Machine learning anomaly detection
* Real-time SOC dashboard
* Integration with SIEM tools

---


## Current Implementation

The repository currently contains a working **AI-powered SOC alert analyzer** using a local LLM and n8n automation.

**Architecture:**
Manual Trigger → Alert Classification → n8n → Playbook Selection → Ollama → SOC Analysis

---

## Alert Classification

Alerts are automatically classified into logical categories (e.g., brute force, phishing, malware) before being analyzed by the AI model based on key indicator words. This classification allows the AI to apply the appropriate SOC playbook directly and generate more accurate, context-aware incident response recommendations.

---

## SOC Playbooks

The AI agent uses structured SOC playbooks to guide its analysis and response recommendations. These playbooks are concise and practical for SOC analysts.

---

## AI Playbook Engine

The AI loads the correct SOC playbook dynamically based on the classified alert type. This ensures the incident response recommendations are standardized and aligned with established SOC procedures.

## Author

Vansh Devgun

Cybersecurity student building hands-on SOC automation and AI security tools.
---

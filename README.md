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

Attack Simulation (Kali Linux VM)
↓
Target Machine Logs (Linux / Windows)
↓
Python Log Monitoring Script
↓
Alert Generation
↓
SOC AI Analyst Agent
↓
SOC Playbook Matching
↓
MITRE ATT&CK Mapping
↓
Incident Response Recommendation

---

## Project Structure

```
soc-ai-analyst-agent
│
├── agent
│   └── soc_agent.py
│
├── monitoring
│   └── log_monitor.py
│
├── playbooks
│   └── soc_playbook.json
│
├── alerts
│   └── alerts.json
│
├── attack_simulation
│   └── attack_notes.md
│
├── dashboard
│   └── dashboard.py
│
├── docs
│   └── architecture.md
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

## Lab Setup

Attacker Machine: Kali Linux
Target Machine: Ubuntu / Windows

Attack simulations generate logs that the monitoring system detects and analyzes.

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

## Author

Vansh Devgun

Cybersecurity student building hands-on SOC automation and AI security tools.
---

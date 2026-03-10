#!/bin/bash
echo "Simulating SSH Brute Force Attack..."
logger "sshd[1234]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2"
logger "sshd[1235]: Failed password for invalid user root from 192.168.1.100 port 22 ssh2"
logger "sshd[1236]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2"
logger "sshd[1237]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2"
logger "sshd[1238]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2"
echo "Attack simulation complete. Check logs."

# Also optionally append a dummy alert to alerts/alerts.json to trigger our monitor directly if Wazuh is not running
ALERTS_FILE="$(dirname "$0")/../alerts/alerts.json"
echo '{"timestamp": "'"$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")"'", "rule": {"id": "5716", "level": "5", "description": "sshd: authentication failure from IP"}, "data": {"srcip": "192.168.1.100"}}' >> "$ALERTS_FILE"
echo "Appended dummy alert to $ALERTS_FILE"

# Lateral Movement Playbook

## MITRE ATT&CK Mapping
- T1021: Remote Services
- T1550: Use Alternate Authentication Material

## Severity
High

## Investigation Steps
1. Identify the source and destination hosts involved.
2. Check for unusual RDP, SMB, or SSH connections between workstations.
3. Review authentication logs for Pass-the-Hash or Pass-the-Ticket indicators.
4. Verify if administrative shares (C$, ADMIN$) were accessed.

## Recommended Response
1. Isolate the affected source and destination hosts from the network.
2. Disable the compromised user accounts.
3. Reset passwords for any accounts that may have been exposed.
4. Hunt for further lateral movement using the identified compromised accounts.

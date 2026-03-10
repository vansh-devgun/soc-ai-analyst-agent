# Privilege Escalation Playbook

## MITRE ATT&CK Mapping
- T1068: Exploitation for Privilege Escalation
- T1548: Abuse Elevation Control Mechanism

## Severity
High / Critical

## Investigation Steps
1. Identify the user account attempting escalation.
2. Check if the attempt was successful.
3. Determine what processes/commands were executed.
4. Verify system patching status and known vulnerabilities.

## Recommended Response
1. Isolate the affected host from the network.
2. Terminate unauthorized root/admin sessions.
3. Reset compromised credentials immediately.
4. Apply necessary security patches.

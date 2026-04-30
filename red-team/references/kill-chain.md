# Kill Chain — Lockheed + MITRE ATT&CK

Single bugs are interesting. Chains are dangerous. This reference turns a confirmed finding into a real-world impact narrative.

## Lockheed Kill Chain (7 stages)

```
RECON  →  WEAPONIZE  →  DELIVERY  →  EXPLOIT  →  INSTALL  →  C2  →  ACTIONS
```

| Stage | Question | Code-review answer |
|-------|----------|--------------------|
| **Recon** | How does the attacker discover this? | Public endpoint? Error messages reveal stack? Version disclosed in headers? |
| **Weaponize** | What input triggers it? | The minimum payload that exercises the bug. |
| **Delivery** | How does the input arrive? | Endpoint, queue, file upload, email, supply chain? |
| **Exploit** | What primitive does it grant? | Read / write / exec / auth-bypass / info-disclosure |
| **Install** | How does the attacker persist? | Backdoor account, scheduled job, modified file, compromised dep |
| **C2** | How does the attacker control it? | Reverse shell, periodic poll, DNS tunnel |
| **Actions** | What's the final goal? | Exfil customer data, ransom, lateral, crypto-mine |

A **chain** strings several of these together via vulnerabilities.

## MITRE ATT&CK Mapping

For each chain step, map to ATT&CK technique IDs (sample — full list at attack.mitre.org):

| Stage | Tactic | Common techniques |
|-------|--------|-------------------|
| Recon | TA0043 Reconnaissance | T1595 Active Scanning, T1592 Gather Victim Host |
| Initial access | TA0001 Initial Access | T1190 Exploit Public-Facing App, T1078 Valid Accounts, T1566 Phishing |
| Execution | TA0002 Execution | T1059 Command and Scripting, T1203 Exploitation for Client Execution |
| Persistence | TA0003 Persistence | T1505 Server Software Component (web shell), T1136 Create Account, T1098 Account Manipulation |
| Privilege escalation | TA0004 | T1068 Exploitation for Privilege Escalation |
| Defense evasion | TA0005 | T1070 Indicator Removal, T1027 Obfuscated Files |
| Credential access | TA0006 | T1003 OS Credential Dumping, T1552 Unsecured Credentials |
| Discovery | TA0007 | T1083 File and Directory Discovery, T1018 Remote System Discovery |
| Lateral movement | TA0008 | T1021 Remote Services |
| Collection | TA0009 | T1005 Data from Local System, T1213 Data from Information Repositories |
| Exfiltration | TA0010 | T1041 Exfil over C2, T1567 Exfil over Web Service |
| Impact | TA0040 | T1486 Data Encrypted for Impact, T1485 Data Destruction |

Use these IDs in the report so blue-team / SOC can correlate with detections.

## Worked Example — From SQLi to Full Compromise

Confirmed finding: **SQL injection in `/api/search?q=`** (CWE-89).

### Chain

| # | Stage | Action | Technique |
|---|-------|--------|-----------|
| 1 | Recon | Find `/api/search` via crawled JS bundle | T1595.002 Vulnerability Scanning |
| 2 | Weaponize | Construct UNION-based SQLi payload | — |
| 3 | Delivery | GET /api/search?q=' UNION SELECT ... -- | T1190 Exploit Public-Facing App |
| 4 | Exploit | Read `users` table → exfil bcrypt hashes | T1213 Data from Info Repos |
| 5 | (Offline) | Crack hashes for low-entropy passwords | T1110.002 Password Cracking |
| 6 | Initial access | Login as admin user | T1078 Valid Accounts |
| 7 | Persistence | Create new admin account | T1136 Create Account |
| 8 | Discovery | Read internal docs / S3 buckets | T1083 File Discovery |
| 9 | Exfiltration | Bulk download customer data | T1041 Exfil over C2 |
| 10 | Impact | Encrypt + ransom OR sell on market | T1657 Financial Theft |

**Severity**: a SQLi by itself might be scored "high" defensively. The chain shows it's actually **critical** because it ends in customer-data exfil + persistence.

This is the value of chain reasoning: the chain reveals the real impact.

## When to Stop the Chain

Stop the chain at the **first out-of-scope step**. Examples:

- Chain reaches a third-party SaaS — stop, document the boundary, don't probe.
- Chain reaches customer data — stop, do not exfil even for demonstration.
- Chain requires social engineering an employee — stop, recommend awareness training.

Replace the rest of the chain with a narrative: *"At this point, an attacker would [continue with X technique], reaching [Y impact]. Mitigation: [Z]."*

## Pre-mortem Variant

For systems not yet built, run the chain **backwards** as a pre-mortem:

```
Imagine the worst-case incident:
- Customer data exfil + ransom.
- 6 months from now.

Walk backwards:
- HOW did they exfil? (T1041 over C2, S3 misconfig, dev tooling?)
- HOW did they get persistence? (admin account, web shell, scheduled job?)
- HOW did they get initial access? (public endpoint, phishing, supply chain?)
- HOW did they recon? (public assets, leaked secrets, GitHub history?)

Each "HOW" is a layer of defense to add — proactively.
```

## Output Template

```markdown
## Exploit Chain: [Finding Title]

**Starting finding**: [link to vuln writeup]

| # | Stage | Tactic / Technique | Action | Evidence (file:line) |
|---|-------|--------------------|--------|----------------------|
| 1 | Recon | T1595 | ... | ... |
| 2 | Delivery | T1190 | ... | ... |
| ...

**Final impact**: [exfil / ransom / lateral / persistence]
**Stopped at**: [step N — out of scope OR successful chain]
**Defenses needed (per stage)**:
| Stage | Control |
|-------|---------|
| Initial access | input validation + WAF rule |
| Persistence | admin-action audit + alerting |
| Exfil | DLP + egress filtering + bandwidth alert |
```

## Anti-Patterns (NEVER)

- NEVER chain into systems out of scope.
- NEVER produce real exploit payloads in writeups — describe shape, not weaponized code.
- NEVER leave a chain unscored — chains drive priority.
- NEVER assume the SOC will catch it. Verify with detection rules per chain step.

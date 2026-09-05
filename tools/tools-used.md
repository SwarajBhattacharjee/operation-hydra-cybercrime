# Tools Used — Operation Hydra Investigation

| Tool | Purpose | Example Command / Usage | Justification |
|---|---|---|---|
| **MXToolbox** | SPF/DKIM/DMARC header validation | `mxtoolbox.com/SuperTool.aspx?action=spf` → paste sending domain | Fastest way to confirm authentication failures without a mail-server sandbox |
| **VirusTotal** | Static/dynamic malware scanning, hash reputation | `vt-cli` or web UI: upload hash `d41a9c3e7f2b...` | Aggregates 70+ AV engines; used here to describe the *expected* multi-engine verdict for the simulated hash |
| **AbuseIPDB** | IP reputation / abuse confidence scoring | `curl -G https://api.abuseipdb.com/api/v2/check -d ipAddress=185.220.101.47 -H "Key: $API_KEY"` (see `scripts/ip_trace.py`) | Crowd-sourced abuse reports give a fast triage signal for C2 infrastructure |
| **WHOIS / ICANN Lookup** | Domain registration age, registrar | `whois secure-hdfcbank-verify.com` (see `scripts/whois_lookup.py`) | Newly-registered domains are one of the strongest phishing indicators |
| **dig / nslookup** | DNS record and name-server resolution | `dig MX secure-hdfcbank-verify.com` | Confirms mail-exchange records point to attacker infrastructure |
| **pandas (Python)** | Transaction log parsing & analysis | `scripts/log_parser.py` | Enables programmatic mule-chain reconstruction over CSV logs |
| **Sigma rules** | Detection-rule authoring for SOC handoff | `malware-analysis/iocs.md` §Suggested Detection Rules | Vendor-agnostic format for translating IOCs into SIEM alerts |

> Note: Where a live API key was not available in this academic
> environment, each script (`scripts/*.py`) falls back to clearly
> labeled **simulated data** matching the figures reported in
> `phishing-spoofing/analysis.md` and `malware-analysis/iocs.md`, so
> the tooling remains runnable and reviewable end-to-end.

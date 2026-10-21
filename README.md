# Operation Hydra: Unraveling a Multi-Vector Cyber Crime Involving Phishing, Spoofing & Financial Fraud

**Assignment 2 — Unit 2: Types of Cyber Crimes**

## 📌 Objective

This repository simulates the investigation and analysis of a multi-stage
cyber-crime campaign — codenamed **"Operation Hydra"** — that combines
phishing, email/web spoofing, malware injection, and financial fraud.
It applies both **technical** (log analysis, header inspection, IOC
extraction) and **legal** (IT Act, IPC, CFAA, GDPR, Budapest Convention)
lenses to reconstruct the attacker's modus operandi.

> ⚠️ **Disclaimer:** All emails, IPs, domains, malware behavior,
> transaction logs, and wallet addresses in this repository are
> **simulated / fabricated for academic purposes only**. No real
> victims, systems, or malicious infrastructure are represented or
> targeted. No functional malware or exploit code is included anywhere
> in this repository.

## 🗂 Repository Structure

```
.
├── README.md                          # This file
├── docs/
│   └── report/
│       ├── Operation_Hydra_Report.md  # Full legal-technical impact report (source)
│       └── Operation_Hydra_Report.pdf # Rendered final report (PDF)
├── phishing-spoofing/
│   ├── email-samples/                 # 5 simulated phishing email samples (raw headers)
│   └── analysis.md                    # SPF/DKIM/DMARC + WHOIS + spoofing infra analysis
├── malware-analysis/
│   ├── payload-simulation.md          # Simulated payload behavior write-up
│   └── iocs.md                        # Indicators of Compromise (IOCs)
├── financial-fraud/
│   ├── transaction-logs/
│   │   └── sample_transactions.csv    # Simulated UPI/card transaction log
│   └── tracing-analysis.md            # Mule account / crypto laundering trace
├── scripts/
│   ├── whois_lookup.py                # WHOIS lookup helper (defensive/analysis use)
│   ├── ip_trace.py                    # IP reputation / geolocation trace helper
│   └── log_parser.py                  # Transaction log parser & mule-flow grapher
├── tools/
│   └── tools-used.md                  # Tools list, commands, and justification
├── screenshots/                       # Tool output screenshots (placeholder)
└── .github/workflows/ci.yml           # CI: markdown lint + repo structure check
```

## 🔎 Sub-Problems Covered

| # | Sub-Problem | Location |
|---|---|---|
| 1 | Cybercrime decomposition & legal mapping | `docs/report/Operation_Hydra_Report.md` §1 |
| 2 | Phishing & spoofing investigation | `phishing-spoofing/` |
| 3 | Malware payload analysis | `malware-analysis/` |
| 4 | Financial fraud tracing | `financial-fraud/` |
| 5 | Legal, ethical & impact report | `docs/report/Operation_Hydra_Report.md` |

## 🛠 Setup Instructions

```bash
# Clone the repository
git clone https://github.com/SwarajBhattacharjee/operation-hydra-cybercrime.git
cd operation-hydra-cybercrime

# (Optional) create a virtual environment for the analysis scripts
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt

# Run the WHOIS / IP trace helpers on the simulated data
python scripts/whois_lookup.py --domain secure-hdfcbank-verify.com
python scripts/ip_trace.py --ip 185.220.101.47
python scripts/log_parser.py financial-fraud/transaction-logs/sample_transactions.csv
```

No external services are called with real credentials — the scripts are
designed to run against the simulated data included in this repo, or
against live public APIs (WHOIS/AbuseIPDB) only if you supply your own
API key.

## 📄 Final Report

The full 5–8 page legal-technical impact report is at
[`docs/report/Operation_Hydra_Report.pdf`](docs/report/Operation_Hydra_Report.pdf)
(source markdown also provided).

## ✅ Evaluation Mapping (10 Marks)

| Criteria | Marks | Where |
|---|---|---|
| Cybercrime classification + legal framework | 2.0 | Report §1 |
| Phishing/Spoofing technical analysis | 2.0 | `phishing-spoofing/` |
| Malware/Trojan payload behavior analysis | 2.0 | `malware-analysis/` |
| Financial fraud simulation/tracing | 2.0 | `financial-fraud/` |
| Legal/Ethical/Impact writing quality | 1.0 | Report §5 |
| GitHub documentation, structure & CI compliance | 1.0 | This README + `.github/workflows/ci.yml` |

## ✍️ Authorship Declaration

This work was prepared by **Swaraj Bhattacharjee** (Roll No. 2301730011),
**B.Tech CSE (AI & ML), Semester 7**, for Assignment 2 — Unit 2: Types
of Cyber Crimes, submitted on **05/09/2026**. All simulated artifacts (emails,
logs, IOCs, wallet addresses) were authored by the student for
educational demonstration and do not reference real individuals,
organizations, or ongoing incidents.

## 📜 License

This academic work is shared under the MIT License (see `LICENSE`).

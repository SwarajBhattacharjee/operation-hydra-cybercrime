---
title: "Operation Hydra: Unraveling a Multi-Vector Cyber Crime Involving Phishing, Spoofing & Financial Fraud"
subtitle: "Assignment 2 — Unit 2: Types of Cyber Crimes"
author: "Swaraj Bhattacharjee — Roll No. 2301730011 — B.Tech CSE (AI & ML), Sem 7"
date: "05/09/2026"
---

# Executive Summary

This report documents a simulated investigation into **"Operation
Hydra,"** a multi-stage cyber-crime campaign combining phishing,
email/domain spoofing, malware-based credential theft, and layered
financial fraud culminating in cryptocurrency laundering. The
investigation reconstructs the attacker's full kill chain — from the
initial phishing lure through to the final crypto off-ramp — maps each
stage to applicable Indian and international law, analyzes the
technical artifacts (headers, IOCs, transaction logs), and closes with
an assessment of stakeholder impact, ethical considerations, and policy
recommendations.

All artifacts referenced (emails, IPs, malware behavior, transaction
logs, wallet addresses) are **simulated for academic purposes** and do
not represent real individuals, organizations, or ongoing incidents.

---

# 1. Cybercrime Decomposition & Legal Mapping

## 1.1 The Attack Chain

Operation Hydra unfolds across five linked stages:

1. **Phishing** — five themed lure emails (banking alert, courier
   scam, OTP/KYC theft, fake job offer, B2B invoice) sent from spoofed
   brand-lookalike domains.
2. **Spoofing** — sender domains and headers forged to impersonate
   HDFC Bank, FedEx, Paytm, Infosys, and a fictitious ERP vendor, with
   SPF/DKIM/DMARC failing on every sample.
3. **Malware injection** — two attachments (a disguised `.pdf.exe`
   Trojan/infostealer and a macro-enabled spreadsheet downloader)
   establish persistence, keylog credentials, and beacon to
   attacker-controlled C2 infrastructure.
4. **Unauthorized access** — stolen credentials/OTPs are used to
   authorize fraudulent transfers from victim accounts without
   consent.
5. **Financial fraud / money laundering** — funds are layered through
   three mule accounts in under 13 minutes and converted to
   cryptocurrency, with a structured transaction (₹49,999) designed to
   dodge the ₹50,000 reporting threshold.

A sixth ancillary offense — **spamming** — is present in the bulk,
unsolicited nature of the phishing distribution itself.

## 1.2 Distinct Cyber Crimes Identified (≥ 5)

| # | Crime | Description in this case |
|---|---|---|
| 1 | **Phishing** | Brand-impersonation emails designed to induce credential/OTP disclosure |
| 2 | **Email/Domain Spoofing** | Forged `From` headers and typosquatted domains (`secure-hdfcbank-verify.com`, etc.) |
| 3 | **Malware distribution (Trojan/Dropper)** | Disguised executable and macro-dropper attachments |
| 4 | **Unauthorized access / identity theft** | Use of stolen credentials to authorize transfers |
| 5 | **Financial/Card & UPI Fraud** | Fraudulent invoice payment and advance-fee job scam |
| 6 | **Money Laundering** | Multi-hop mule layering and crypto conversion |
| 7 | **Spamming** | Bulk unsolicited distribution of the phishing lures |

## 1.3 Legal Mapping — India

| Crime | IT Act, 2000 | IPC 1860 / BNS 2023 | Other Indian Law |
|---|---|---|---|
| Phishing | §66C (identity theft), §66D (cheating by personation using computer resource) | §420 IPC / §318 BNS (cheating) | — |
| Spoofing | §66C, §66D | §465/468 IPC (forgery) / §336–338 BNS | — |
| Malware/Trojan distribution | §43 (unauthorized access/damage to computer system), §66 (computer-related offenses) | §43 read with §66 covers civil + criminal liability | CERT-In incident reporting rules (mandatory 6-hr reporting) |
| Unauthorized access | §43, §66 | §379 IPC (theft, if data/funds) | — |
| Financial fraud (UPI/card) | §66D | §420 IPC / §318 BNS | RBI Digital Payment Security Controls Directions, 2021 |
| Money laundering | §66 (as predicate offense enabler) | — | **Prevention of Money Laundering Act (PMLA), 2002** |
| Spamming | §66A *(struck down — see note below)* | — | IT (Intermediary Guidelines) Rules, 2021 for platform takedown |

> **Note:** Section 66A of the IT Act (which historically covered
> "offensive messages") was struck down by the Supreme Court in
> *Shreya Singhal v. Union of India* (2015) for being unconstitutionally
> vague. Spamming/nuisance-messaging today is generally addressed
> through platform-level takedown under the IT Rules, 2021, and through
> the cheating/fraud provisions once the spam is shown to facilitate a
> crime, rather than as a standalone speech offense.

## 1.4 Legal Mapping — Global Equivalents

| Crime | United States (CFAA) | European Union (GDPR / EU Cybercrime Directives) | International |
|---|---|---|---|
| Phishing/Spoofing | 18 U.S.C. §1030 (Computer Fraud and Abuse Act) — unauthorized access with intent to defraud | Art. 32 GDPR (security of processing) breach exposure for the impersonated brand; Directive 2013/40/EU (attacks against information systems) | **Budapest Convention on Cybercrime, Art. 8** (computer-related fraud), **Art. 7** (forgery) |
| Malware distribution | CFAA §1030(a)(5) (knowing transmission causing damage) | Directive 2013/40/EU Art. 7 (illegal system interference) | Budapest Convention Art. 6 (misuse of devices) |
| Unauthorized access | CFAA §1030(a)(2) | GDPR Art. 5, 32 (breach of confidentiality) | Budapest Convention Art. 2 (illegal access) |
| Financial fraud | 18 U.S.C. §1343 (wire fraud) | EU Payment Services Directive 2 (PSD2) liability rules | FATF Recommendations |
| Money laundering | 18 U.S.C. §1956 | EU 5th/6th Anti-Money Laundering Directives | FATF Recommendation 15 (virtual assets) |

---

# 2. Phishing & Spoofing — Technical Findings

Five simulated phishing samples were analyzed for header authenticity,
IP/domain infrastructure, and social-engineering technique. Full
detail is in [`phishing-spoofing/analysis.md`](../../phishing-spoofing/analysis.md);
key findings:

- **100% authentication failure rate**: every sample failed SPF and/or
  DKIM, and all five failed DMARC alignment — yet several would still
  reach an inbox under a permissive (`p=none`) DMARC policy, which is
  a common real-world misconfiguration this case is designed to
  illustrate.
- **Shared attacker infrastructure**: two of the five sending IPs
  resolve to the same autonomous system (a bulletproof hosting
  provider), indicating a single operator behind multiple lure themes.
- **Combosquatting domains**: every sender domain fuses a trusted brand
  name with a generic trust word (`secure`, `verify`, `track`), a
  well-documented phishing-kit pattern.
- **WHOIS freshness**: all five domains were "registered" (simulated)
  within 3–11 days of the campaign, consistent with disposable
  phishing infrastructure.

---

# 3. Malware / Trojan Payload Behavior Analysis

Full detail is in [`malware-analysis/payload-simulation.md`](../../malware-analysis/payload-simulation.md)
and [`malware-analysis/iocs.md`](../../malware-analysis/iocs.md).

- The `.pdf.exe` attachment behaves as a **Trojan infostealer/keylogger**:
  it installs persistence via a registry `Run` key, hooks the keyboard,
  and beacons to a C2 server over HTTPS.
- The `.xlsm` attachment behaves as a **macro-based Trojan downloader**,
  using an obfuscated PowerShell one-liner to retrieve the same
  second-stage payload — confirming both lures funnel into one
  campaign infrastructure.
- Neither sample exhibits wiper/ransomware behavior; the objective is
  **silent, sustained credential theft** feeding directly into the
  financial-fraud stage below.
- A consolidated IOC list (domains, IPs, hashes, registry keys, C2
  URIs) and two Sigma-style detection rules are provided for SOC
  handoff.

---

# 4. Financial Fraud Tracing

Full detail is in [`financial-fraud/tracing-analysis.md`](../../financial-fraud/tracing-analysis.md).

- Two independent victims (from the banking/invoice lure and the job-offer
  lure) were funneled into the **same first-hop mule account**,
  linking the otherwise-distinct social-engineering pretexts to one
  cash-out operation.
- A **three-layer mule chain** moved funds from victim → mule 1 → mule
  2 → mule 3 → a cryptocurrency exchange wallet → an external BTC
  wallet, completing in under 13 minutes.
- A ₹49,999 transfer — ₹1 below a commonly used ₹50,000 due-diligence
  threshold — is flagged as a probable **structuring** attempt.
- `scripts/log_parser.py` automates detection of both the mule chain
  and the structuring pattern directly from the transaction CSV.

---

# 5. Legal, Ethical & Impact Assessment

## 5.1 Breakdown of Cybercrime Types with Legal Remedies

| Stage | Primary Remedy (India) | Civil Remedy |
|---|---|---|
| Phishing/spoofing | FIR under §66C/66D IT Act + §420 IPC; report to CERT-In and the National Cyber Crime Reporting Portal (cybercrime.gov.in) | Injunction against the impersonated domain via registrar/ICANN UDRP |
| Malware distribution | §43/§66 IT Act prosecution; mandatory CERT-In breach reporting for the impersonated organization | Damages claim under §43A (compensation for negligent handling of sensitive data) |
| Financial fraud | §420 IPC/§318 BNS + §66D IT Act; bank fraud-hold and reversal request under RBI's "Limited Liability of Customers" circular | Chargeback/reversal via the paying bank's ombudsman |
| Money laundering | PMLA, 2002 investigation by the Enforcement Directorate; Financial Intelligence Unit (FIU-IND) STR filing by banks | Asset attachment proceedings under PMLA §5 |

## 5.2 Impact on Stakeholders

- **Financial:** Direct monetary loss to victims (₹64,999 across the
  two simulated victims); downstream cost to banks for fraud
  investigation, chargebacks, and regulatory reporting.
- **Emotional:** Victims of financial fraud commonly report acute
  stress, anxiety, and a lasting loss of trust in digital banking —
  effects that are well documented in cybercrime victimology
  literature and are not lessened by the amount involved being modest.
- **Reputational:** The impersonated brands (a real bank, a courier
  company, a payments wallet, and a corporate employer) all suffer
  reputational harm and customer-trust erosion even though they were
  not technically compromised — they were *impersonated*, which is
  itself a significant brand-protection and legal challenge.
- **Systemic:** Repeated incidents of this kind erode general public
  confidence in UPI and digital-first banking, a policy-relevant
  concern given India's high digital-payment adoption.

## 5.3 Ethical Dilemmas

- **Tracing cryptocurrency:** Blockchain analysis can deanonymize
  wallets, but aggressive chain-surveillance also raises privacy
  concerns for the broader (mostly innocent) user base of an exchange,
  and cross-border legal cooperation is often required to compel an
  exchange to disclose KYC data — raising jurisdictional and due-process
  questions.
- **Deceptive honeypots:** Using decoy credentials or fake mule
  accounts to bait attackers is an effective investigative technique,
  but it sits close to entrapment concerns and can implicate
  investigators in facilitating a live financial crime if not tightly
  scoped and authorized.
- **Disclosure timing:** Notifying victims/banks quickly can freeze
  funds but may tip off the attacker before the full mule network is
  mapped — a genuine tension between rapid victim protection and
  thorough investigation.
- **Attribution certainty:** Overclaiming attribution (e.g., naming a
  specific group or individual) based on infrastructure overlap alone
  risks reputational and legal harm if the attribution is wrong;
  investigators should distinguish confirmed technical links from
  inferred ones.

## 5.4 Suggestions for Public Awareness or Policy Changes

1. **Mandatory DMARC enforcement (`p=reject`)** for regulated sectors
   (banking, payments) rather than the currently common `p=none`
   monitor-only posture.
2. **Real-time domain-age scoring** integrated into bank/UPI app
   in-app link warnings, flagging destinations on domains younger than
   30 days.
3. **Lower, tiered structuring-detection thresholds** for UPI/IMPS —
   current large-value thresholds are easily undercut by
   micro-structuring, as demonstrated here.
4. **Faster inter-bank fraud-freeze cooperation**, since this
   simulation shows a full three-hop layering completing in under 13
   minutes — well inside the delay of most current manual fraud-hold
   processes.
5. **Public awareness campaigns** specifically addressing the five
   lure themes modeled here (bank suspension, courier fee, OTP/KYC,
   job-offer deposit, B2B invoice) since these remain the highest-
   volume phishing pretexts in India per CERT-In's public advisories.
6. **Simplified victim reporting** — a single, well-publicized
   national helpline number (1930) and portal (cybercrime.gov.in)
   integrated directly into banking apps to reduce the time between
   victimization and fraud-hold requests.

---

# 6. Conclusion

Operation Hydra illustrates how a single unsophisticated phishing email
can cascade into identity theft, malware compromise, and laundered
financial loss within minutes — and how each stage maps cleanly onto
existing Indian and international legal frameworks, even though
enforcement in practice remains constrained by detection speed,
cross-border cooperation, and the pace of layering compared to the
pace of manual fraud response. Closing this gap requires coordinated
technical controls (DMARC enforcement, domain-age scoring, faster
inter-bank freezes) alongside the legal remedies already available
under the IT Act, IPC/BNS, and PMLA.

---

## References

1. Information Technology Act, 2000 (as amended 2008), Government of India.
2. Indian Penal Code, 1860 / Bharatiya Nyaya Sanhita, 2023.
3. Prevention of Money Laundering Act, 2002, Government of India.
4. *Shreya Singhal v. Union of India*, (2015) 5 SCC 1.
5. Council of Europe, Convention on Cybercrime (Budapest Convention), ETS No. 185, 2001.
6. Computer Fraud and Abuse Act, 18 U.S.C. §1030.
7. Regulation (EU) 2016/679 (General Data Protection Regulation).
8. Directive 2013/40/EU on attacks against information systems.
9. Financial Action Task Force (FATF), Recommendation 15 on New Technologies.
10. CERT-In, Cyber Security Directions and public phishing advisories, cert-in.org.in.
11. Reserve Bank of India, Master Direction on Digital Payment Security Controls, 2021.

# Phishing & Spoofing Investigation — Operation Hydra

## 1. Sample Overview

| Sample | Lure Theme | Sender Domain | Attachment/Link |
|---|---|---|---|
| `sample-1-bank-alert.eml` | Bank account suspension | secure-hdfcbank-verify.com | Fake PDF→EXE + credential-harvest link |
| `sample-2-courier-scam.eml` | Parcel customs fee | fedex-track-delivery.info | Payment link |
| `sample-3-otp-phishing.eml` | Wallet KYC / OTP theft | paytm-secure-kyc.com | Credential/OTP-harvest link |
| `sample-4-job-offer.eml` | Fake WFH job offer | infosys-careers-hire.net | UPI advance-fee scam |
| `sample-5-invoice-malware.eml` | Overdue invoice (B2B) | invoice-tally-erp.com | Macro-enabled spreadsheet dropper |

## 2. Header & Authentication Analysis

All five samples were checked for **SPF, DKIM, and DMARC** alignment
(fields present in each `Authentication-Results` header):

| Sample | SPF | DKIM | DMARC | Verdict |
|---|---|---|---|---|
| 1 | fail | none | fail (p=none) | Spoofed sender, no enforcement — delivered |
| 2 | fail | fail | fail (p=reject) | Should have been rejected; simulated lax mail-gateway config allowed it through |
| 3 | softfail | none | fail (p=quarantine) | Landed in quarantine/spam in a hardened environment |
| 4 | fail | none | fail (p=none) | Spoofed sender, no enforcement |
| 5 | fail | fail | fail (p=reject) | Targeted B2B spear-phish, domain impersonation |

**Observation:** every sample fails at least SPF and DMARC alignment.
This is the single strongest technical signal of domain spoofing — a
properly configured `p=reject` DMARC policy on the *recipient* side
would have blocked samples 2 and 5 outright. The fact they were
"delivered" in this simulation models a common real-world gap: many
organizations still run permissive mail gateways that log a DMARC
failure but do not act on it.

## 3. IP & Infrastructure Trace (Simulated)

| IP | Reverse DNS (simulated) | Registrant / ASN (simulated) | Reputation (simulated AbuseIPDB score) |
|---|---|---|---|
| 185.220.101.47 | mail-relay-09.spoofnet.ru | AS-HYDRANET, bulletproof hosting, RU | 98/100 (high abuse) |
| 45.155.205.19 | vps-88214.hydra-c2.net | AS-OFFSHOREVPS, NL | 91/100 |
| 103.216.221.9 | smtp-relay-42.hydra-c2.net | AS-ASIAHOST, HK | 87/100 |
| 178.128.44.201 | mail01.bpo-hydra.asia | AS-CLOUDLEASE, SG | 76/100 |
| 91.243.85.126 | mx-out-13.hydra-c2.net | AS-HYDRANET, bulletproof hosting, RU | 95/100 |

Two IPs (185.220.101.47 and 91.243.85.126) resolve to the **same
autonomous system**, suggesting samples 1 and 5 were launched from
shared attacker-controlled infrastructure — consistent with a single
campaign operator ("Hydra") reusing a bulletproof-hosting provider
across multiple lure types.

`scripts/ip_trace.py` demonstrates how this lookup would be automated
against a real threat-intel API (AbuseIPDB / VirusTotal) — see
`tools/tools-used.md` for exact commands.

## 4. WHOIS / Domain Analysis

All five sender domains show the classic markers of freshly-registered
phishing infrastructure:

- **Registration age:** 3–11 days before the campaign email was sent (simulated).
- **Registrar:** privacy-shielded registration via low-KYC registrars.
- **Typosquatting pattern:** each domain embeds a trusted brand name
  (`hdfcbank`, `fedex`, `paytm`, `infosys`, `tally`) combined with a
  generic trust word (`secure`, `verify`, `track`, `careers`, `erp`)
  to build false legitimacy — a textbook **combosquatting** technique.
- **TLD choice:** `.com`/`.info`/`.net` chosen over the brand's real
  TLD to slip past casual visual inspection.

`scripts/whois_lookup.py` shows the automated WHOIS query pattern used
to gather this data (age, registrar, name servers) at scale across a
list of suspect domains.

## 5. Spoofing Infrastructure Summary

```
[Attacker] --controls--> [Bulletproof host: AS-HYDRANET]
                              |
        -----------------------------------------------
        |                  |                  |
  spoofnet.ru mail   hydra-c2.net mail   bpo-hydra.asia mail
        |                  |                  |
  sample-1 (bank)    sample-2, 5 (courier,   sample-4 (job offer)
                       invoice)
```

## 6. Recommended Detective Controls

1. Enforce DMARC `p=reject` (not just `p=none`/`quarantine`) on inbound filtering.
2. Block on SPF/DKIM hard-fail rather than only flagging.
3. Automated WHOIS-age scoring: block/flag domains registered < 30 days ago.
4. Attachment sandboxing for double-extension files (`.pdf.exe`) and macro-enabled Office files.
5. User-awareness training keyed to the specific lure themes observed (banking, courier, KYC/OTP, job offers, B2B invoices).

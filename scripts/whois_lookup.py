#!/usr/bin/env python3
"""
whois_lookup.py — WHOIS lookup helper for domain-spoofing investigation.

Part of the Operation Hydra cybercrime investigation assignment.
Purely for DEFENSIVE / ANALYTICAL use: given a domain, it reports
registration age, registrar, and name servers so an investigator can
judge whether a sender domain looks like freshly-registered phishing
infrastructure.

Usage:
    python whois_lookup.py --domain secure-hdfcbank-verify.com
    python whois_lookup.py --file suspect_domains.txt

If the `python-whois` package or network access is unavailable, the
script falls back to printing the simulated WHOIS record bundled in
this repo's documentation (see phishing-spoofing/analysis.md) so the
tool remains runnable offline for grading purposes.
"""

import argparse
import datetime as dt
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Simulated fallback WHOIS records matching phishing-spoofing/analysis.md
SIMULATED_RECORDS = {
    "secure-hdfcbank-verify.com": {
        "registrar": "Low-KYC Registrar Ltd.",
        "creation_date": "2026-05-01",
        "name_servers": ["ns1.hydra-dns.net", "ns2.hydra-dns.net"],
    },
    "fedex-track-delivery.info": {
        "registrar": "Cheap Domains Inc.",
        "creation_date": "2026-05-05",
        "name_servers": ["ns1.hydra-dns.net", "ns2.hydra-dns.net"],
    },
    "paytm-secure-kyc.com": {
        "registrar": "Low-KYC Registrar Ltd.",
        "creation_date": "2026-05-08",
        "name_servers": ["ns1.hydra-dns.net", "ns2.hydra-dns.net"],
    },
    "infosys-careers-hire.net": {
        "registrar": "Cheap Domains Inc.",
        "creation_date": "2026-05-09",
        "name_servers": ["ns1.bpo-hydra-dns.asia", "ns2.bpo-hydra-dns.asia"],
    },
    "invoice-tally-erp.com": {
        "registrar": "Low-KYC Registrar Ltd.",
        "creation_date": "2026-05-10",
        "name_servers": ["ns1.hydra-dns.net", "ns2.hydra-dns.net"],
    },
}


def lookup_live(domain: str):
    """Attempt a real WHOIS lookup using python-whois, if installed."""
    try:
        import whois  # python-whois
    except ImportError:
        return None
    try:
        record = whois.whois(domain)
        return record
    except Exception:
        return None


def lookup_simulated(domain: str):
    return SIMULATED_RECORDS.get(domain)


def report(domain: str):
    print(f"\n=== WHOIS report: {domain} ===")
    live = lookup_live(domain)
    if live and live.get("creation_date"):
        creation = live["creation_date"]
        registrar = live.get("registrar", "unknown")
        name_servers = live.get("name_servers", [])
    else:
        sim = lookup_simulated(domain)
        if not sim:
            print("No live or simulated record found for this domain.")
            return
        creation = sim["creation_date"]
        registrar = sim["registrar"]
        name_servers = sim["name_servers"]
        print("(using simulated record — offline/academic mode)")

    if isinstance(creation, str):
        creation_dt = dt.datetime.strptime(creation, "%Y-%m-%d")
    else:
        creation_dt = creation

    age_days = (dt.datetime.now() - creation_dt).days
    print(f"Registrar     : {registrar}")
    print(f"Creation date : {creation_dt.date()}")
    print(f"Domain age    : {age_days} days")
    print(f"Name servers  : {', '.join(name_servers)}")
    if age_days < 30:
        print("⚠️  FLAG: domain registered under 30 days ago — high phishing risk.")


def main():
    parser = argparse.ArgumentParser(description="WHOIS lookup helper")
    parser.add_argument("--domain", help="Single domain to check")
    parser.add_argument("--file", help="Path to a file with one domain per line")
    args = parser.parse_args()

    if not args.domain and not args.file:
        parser.print_help()
        sys.exit(1)

    domains = []
    if args.domain:
        domains.append(args.domain)
    if args.file:
        with open(args.file) as fh:
            domains.extend(line.strip() for line in fh if line.strip())

    for d in domains:
        report(d)


if __name__ == "__main__":
    main()

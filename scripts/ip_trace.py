#!/usr/bin/env python3
"""
ip_trace.py — IP reputation / geolocation trace helper.

Part of the Operation Hydra cybercrime investigation assignment.
Given an IP address, reports (a) reverse DNS, (b) approximate
geolocation/ASN, and (c) an abuse-confidence score. Uses AbuseIPDB's
public API if an API key is supplied via --api-key or the
ABUSEIPDB_API_KEY environment variable; otherwise falls back to the
simulated data documented in phishing-spoofing/analysis.md so the tool
runs offline for grading.

Usage:
    python ip_trace.py --ip 185.220.101.47
    python ip_trace.py --ip 185.220.101.47 --api-key YOUR_KEY
"""

import argparse
import os
import socket

SIMULATED_DATA = {
    "185.220.101.47": {
        "rdns": "mail-relay-09.spoofnet.ru",
        "asn": "AS-HYDRANET (bulletproof hosting)",
        "country": "RU",
        "abuse_score": 98,
    },
    "45.155.205.19": {
        "rdns": "vps-88214.hydra-c2.net",
        "asn": "AS-OFFSHOREVPS",
        "country": "NL",
        "abuse_score": 91,
    },
    "103.216.221.9": {
        "rdns": "smtp-relay-42.hydra-c2.net",
        "asn": "AS-ASIAHOST",
        "country": "HK",
        "abuse_score": 87,
    },
    "178.128.44.201": {
        "rdns": "mail01.bpo-hydra.asia",
        "asn": "AS-CLOUDLEASE",
        "country": "SG",
        "abuse_score": 76,
    },
    "91.243.85.126": {
        "rdns": "mx-out-13.hydra-c2.net",
        "asn": "AS-HYDRANET (bulletproof hosting)",
        "country": "RU",
        "abuse_score": 95,
    },
}


def live_abuseipdb_lookup(ip: str, api_key: str):
    try:
        import requests
    except ImportError:
        return None
    try:
        resp = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={"Key": api_key, "Accept": "application/json"},
            params={"ipAddress": ip, "maxAgeInDays": 90},
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json().get("data")
    except Exception:
        return None
    return None


def resolve_rdns(ip: str):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def report(ip: str, api_key: str | None):
    print(f"\n=== IP trace report: {ip} ===")

    rdns = resolve_rdns(ip)

    live = live_abuseipdb_lookup(ip, api_key) if api_key else None
    if live:
        print(f"Reverse DNS   : {rdns or live.get('domain', 'n/a')}")
        print(f"Country       : {live.get('countryCode')}")
        print(f"ISP           : {live.get('isp')}")
        print(f"Abuse score   : {live.get('abuseConfidenceScore')}/100")
        return

    sim = SIMULATED_DATA.get(ip)
    if not sim:
        print(f"Reverse DNS   : {rdns or 'not resolvable'}")
        print("No simulated or live threat-intel record found for this IP.")
        return

    print("(using simulated threat-intel record — offline/academic mode)")
    print(f"Reverse DNS   : {rdns or sim['rdns']}")
    print(f"ASN / Hosting : {sim['asn']}")
    print(f"Country       : {sim['country']}")
    print(f"Abuse score   : {sim['abuse_score']}/100")
    if sim["abuse_score"] >= 75:
        print("⚠️  FLAG: high-confidence malicious infrastructure.")


def main():
    parser = argparse.ArgumentParser(description="IP reputation/trace helper")
    parser.add_argument("--ip", required=True, help="IP address to check")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ABUSEIPDB_API_KEY"),
        help="AbuseIPDB API key (optional; falls back to simulated data)",
    )
    args = parser.parse_args()
    report(args.ip, args.api_key)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
log_parser.py — Transaction log parser & mule-chain flow grapher.

Part of the Operation Hydra cybercrime investigation assignment.
Reads a CSV of transactions (see
financial-fraud/transaction-logs/sample_transactions.csv) and:
  1. Flags transactions marked SUSPICIOUS.
  2. Reconstructs the mule-account transfer chain.
  3. Flags "structuring" amounts just under common reporting
     thresholds (e.g., Rs 50,000).

Usage:
    python log_parser.py financial-fraud/transaction-logs/sample_transactions.csv
"""

import argparse
import csv
from collections import defaultdict

STRUCTURING_THRESHOLD = 50000
STRUCTURING_MARGIN = 500  # flag anything within this margin below the threshold


def load_transactions(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def flag_suspicious(transactions):
    return [t for t in transactions if t.get("flag") == "SUSPICIOUS"]


def flag_structuring(transactions):
    flagged = []
    for t in transactions:
        try:
            amount = float(t["amount_inr"])
        except (KeyError, ValueError):
            continue
        if STRUCTURING_THRESHOLD - STRUCTURING_MARGIN <= amount < STRUCTURING_THRESHOLD:
            flagged.append(t)
    return flagged


def build_chain(transactions):
    """Build a simple directed graph of account -> [account, ...] for suspicious txns."""
    graph = defaultdict(list)
    for t in transactions:
        if t.get("flag") == "SUSPICIOUS":
            graph[t["sender_account"]].append(
                (t["receiver_account"], t["amount_inr"], t["channel"], t["timestamp"])
            )
    return graph


def print_chain(graph):
    print("\n=== Reconstructed Mule Transfer Chain ===")
    for src, edges in graph.items():
        for dest, amount, channel, ts in edges:
            print(f"{src}  --[{channel} ₹{amount} @ {ts}]-->  {dest}")


def main():
    parser = argparse.ArgumentParser(description="Fraud transaction log parser")
    parser.add_argument("csv_path", help="Path to transaction CSV file")
    args = parser.parse_args()

    transactions = load_transactions(args.csv_path)
    print(f"Loaded {len(transactions)} transactions from {args.csv_path}")

    suspicious = flag_suspicious(transactions)
    print(f"\n{len(suspicious)} transaction(s) flagged SUSPICIOUS:")
    for t in suspicious:
        print(f"  {t['txn_id']}: {t['sender_account']} -> {t['receiver_account']} "
              f"₹{t['amount_inr']} ({t['channel']})")

    structuring = flag_structuring(transactions)
    if structuring:
        print(f"\n⚠️  {len(structuring)} transaction(s) show possible STRUCTURING "
              f"(just under ₹{STRUCTURING_THRESHOLD} reporting threshold):")
        for t in structuring:
            print(f"  {t['txn_id']}: ₹{t['amount_inr']}")

    graph = build_chain(transactions)
    print_chain(graph)


if __name__ == "__main__":
    main()

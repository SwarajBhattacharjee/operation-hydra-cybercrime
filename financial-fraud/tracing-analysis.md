# Financial Fraud Tracing — Operation Hydra

## 1. Fraud Scenario Simulated

Two victims were funneled into paying fraud-induced transfers:

- **Victim 1** paid a fake "invoice confirmation" of ₹49,999 after
  receiving `sample-5-invoice-malware.eml`-style social engineering
  (business email compromise pattern).
- **Victim 2** paid a ₹15,000 "registration deposit" after receiving
  `sample-4-job-offer.eml` (advance-fee job scam).

Both payments landed in the same first-hop mule account
(`MULE-SB-88213321`), linking the two otherwise-unrelated lure themes
to a single cash-out operation. See
`financial-fraud/transaction-logs/sample_transactions.csv`.

## 2. Money-Flow / Layering Trace

```
VICTIM-SB-44521  ──₹49,999──┐
                             ├──> MULE-SB-88213321 ──₹45,000──> MULE-SB-77410098 ──₹42,000──> MULE-SB-99120456
VICTIM2-SB-33871 ──₹15,000──┘                                        │                              │
                                                                 ₹13,800 (2nd batch)          ₹40,000 (NEFT)
                                                                       │                              │
                                                             MULE-SB-99120456          CRYPTO-EXCHANGE-WALLET-1
                                                                                                       │
                                                                                              0.00041 BTC withdrawal
                                                                                                       │
                                                                            bc1qhydra00xample0wallet0for0demo0purpose0only
```

**Pattern identified:** classic **3-layer mule chain** (victim →
first-hop mule → second-hop mule → crypto off-ramp), executed within
minutes (`10:02` to `10:15`) to outrun bank fraud-hold windows before
funds can be frozen.

## 3. Indicators of Money Laundering

1. **Rapid layering:** three IMPS/NEFT hops completed in under 13 minutes — inconsistent with legitimate business transfers.
2. **Round-then-shaved amounts:** ₹49,999 (just under the ₹50,000 auto-reporting threshold commonly used by banks for enhanced due diligence) — a classic **structuring** indicator.
3. **Crypto off-ramp:** final conversion to BTC at a wallet with no prior transaction history, consistent with a **cash-out wallet** used once and discarded.
4. **Mule account reuse:** `MULE-SB-88213321` receives from two unrelated victims within 24 hours — a hallmark of a rented/purchased mule account rather than a personal account used in error.

## 4. Simulated Crypto Wallet Trace

| Wallet | Role | Simulated Chain Analysis Note |
|---|---|---|
| `bc1qhydra00xample0wallet0for0demo0purpose0only` | Final receiving wallet | Zero prior inbound history; funds simulated as forwarded to a mixing service within 1 hour (consistent with obfuscation behavior) |

`scripts/log_parser.py` implements the graph-construction logic used
to auto-detect this mule chain from the raw CSV (grouping by shared
timestamps/amount proximity and flagging structuring near reporting
thresholds).

## 5. Legal Hooks for This Stage

- **Section 66C/66D, IT Act 2000** — identity theft / cheating by personation using computer resource (phishing → credential theft → unauthorized transfer).
- **Section 420, IPC / Section 318, BNS 2023** — cheating and dishonestly inducing delivery of property.
- **Prevention of Money Laundering Act (PMLA), 2002** — layering and placement stages identified above.
- **RBI KYC Master Directions** — mule account onboarding failures at the receiving bank.
- Global equivalent: **FATF Recommendations on Virtual Assets**, **Budapest Convention Art. 8** (computer-related fraud).

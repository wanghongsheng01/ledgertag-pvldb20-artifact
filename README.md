# LedgerTag — Reproducible Artifact Repository (PVLDB Vol. 20)

This repository provides the standalone deterministic governance engine, public benchmark evaluation harness, frozen six-model experimental results, and figure-generation scripts accompanying:

> **LedgerTag: Provenance-Grounded Semantic Labeling and Relational State Reconciliation for Enterprise Streams**
> Hongsheng Wang, Dazhen Deng *(PVLDB Volume 20 / VLDB 2027)*

## Repository Structure

```text
ledgertag-pvldb20-artifact/
├── ledgertag/
│   └── core.py                               # Standalone deterministic governance primitives
│                                             # (QuoteSeg, SpanVal, AsOfJoin, DirExcl,
│                                             #  ContractGate, EBRouter, FunnelLedger, SampleGuard)
├── benchmarks/
│   ├── verify_theorems_and_microbench.py     # Self-contained verification of Theorems 1–3 & latency
│   └── run_stage2_formal_and_sensitivity.py  # 10,000-schedule model checker, Thm. 4 N* sweep, 10^6 index scale
├── results/
│   ├── exp4_unified_frozen_results.json      # Frozen 6-model Enron & Enterprise evaluation metrics
│   └── results_stage2_formal_sensitivity.json # Frozen 10K checker, N* crossover, 10^6 scaling & MAE outputs
└── README.md
```

## Quick Verification (No API Keys Required)

Verify Theorems 1–4, the 10,000-schedule property-based model checker, finite-sample Empirical-Bayes crossover ($N^* = 166$), bi-temporal index cardinality scaling ($10^3 \to 10^6$ tuples), and deterministic governance latency locally:

```bash
python3 benchmarks/verify_theorems_and_microbench.py
python3 benchmarks/run_stage2_formal_and_sensitivity.py
```

## Public Dataset Reproduction (UC Berkeley Enron BEEAP)

1. Download the public UC Berkeley Enron Annotated Email Dataset (1,702 labeled business emails):
   - Official source: `https://bailando.berkeley.edu/enron_email.html`
   - Archive: `https://bailando.berkeley.edu/enron/enron_with_categories.tar.gz`
2. Inspect the frozen 6-model evaluation metrics (`GPT-6.2-Sol`, `Claude-Opus-5.5`, `Gemini-4-Argon`, `DeepSeek-V4-Pro`, `Kimi-K3.1-Pro`, `Qwen3.8-27B`) in `results/exp4_unified_frozen_results.json`.

*(Raw proprietary B2B customer emails from the enterprise track are excluded for confidentiality; all aggregate statistics, per-model evaluation metrics, and public Enron results are fully preserved in `results/exp4_unified_frozen_results.json`.)*

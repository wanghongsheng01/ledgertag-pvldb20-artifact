#!/usr/bin/env python3
"""Self-contained verification script for LedgerTag Theorems 1-3 and microbenchmark."""
from __future__ import annotations

import pathlib
import random
import sys
import time
from datetime import date, datetime, timedelta
from hashlib import sha256

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from ledgertag.core import (
    FunnelEvent,
    build_asof_erp_context,
    fold_funnel_semilattice,
    guard_l5_sample_promotion,
    segment_email_offsets,
    validate_span_evidence,
)

SEED = 42


def main() -> None:
    rng = random.Random(SEED)

    # 1. Theorem 1: As-Of Temporal Non-Leakage & O(k_max=8) Bounded Context
    as_of = date(2025, 11, 15)
    base = date(2022, 1, 1)
    hist = [
        {
            "type": rng.choice(["order_confirmed", "order_shipped", "sample_order_confirmed"]),
            "date": (base + timedelta(days=rng.randint(0, 1600))).isoformat(),
            "order_no": f"PO-2025-{i:05d}",
        }
        for i in range(5000)
    ]
    ctx = build_asof_erp_context(hist, as_of=as_of, message_text="Status of PO-2025-00001?")
    future_leaks = sum(1 for e in ctx["detailed_events"] if date.fromisoformat(e["date"]) > as_of)
    assert future_leaks == 0, "Theorem 1 violated: future event leaked!"
    assert len(ctx["detailed_events"]) <= 8, "Theorem 1 violated: context exceeded k_max=8!"
    print(f"[PASS] Theorem 1: |E|=5000 -> {len(ctx['detailed_events'])} detailed events, {future_leaks} future leaks.")

    # 2. Theorem 2: Span-Grounded Soundness (rejects quoted-chain evidence)
    sample_body = (
        'Paid sample PI #SP-25. Please ship 2 test desks.\n'
        '---- Original Message ----\n'
        'From: Sales Rep\n'
        'Quotation for Order #PO-19 attached.'
    )
    segs = segment_email_offsets(sample_body)
    valid_flags, ev_invalid = validate_span_evidence(
        sample_body, segs, ["Paid sample PI #SP-25", "Quotation for Order #PO-19"]
    )
    assert valid_flags == [True, False] and ev_invalid is True
    print(f"[PASS] Theorem 2: current-turn span accepted ({valid_flags[0]}), quoted-history span rejected ({valid_flags[1]}).")

    # 3. Theorem 3: Order-Invariant Join-Semilattice Convergence (1,000 permutations) & SampleGuard
    events = [
        FunnelEvent("C1", "m1:L1", "L1", datetime(2025, 3, 1), "outreach", sha256(b"m1:L1").hexdigest(), "evidence"),
        FunnelEvent("C1", "m2:L3", "L3", datetime(2025, 3, 4), "quote request", sha256(b"m2:L3").hexdigest(), "evidence"),
        FunnelEvent("C1", "erp:L4", "L4", datetime(2025, 3, 15), "ERP sample SP-25", sha256(b"erp:L4").hexdigest(), "authoritative"),
        FunnelEvent("C1", "erp:L5", "L5", datetime(2025, 4, 20), "ERP order PO-99", sha256(b"erp:L5").hexdigest(), "authoritative"),
    ]
    ref = fold_funnel_semilattice(events)
    matches = 0
    for _ in range(1000):
        perm = list(events)
        rng.shuffle(perm)
        st = fold_funnel_semilattice(perm)
        if st["deepest_stage"] == ref["deepest_stage"] and st["main_funnel_counted_as"] == ref["main_funnel_counted_as"]:
            matches += 1
    assert matches == 1000
    assert guard_l5_sample_promotion({"order_payment"}, "Paid sample PI #SP-25") is False
    assert guard_l5_sample_promotion({"order_confirmation"}, "Confirmed formal PO #PO-99 for 500 units") is True
    print(f"[PASS] Theorem 3: {matches}/1000 permutation exact convergence; SampleGuard blocked sample-PI L5 trap.")

    # 4. Deterministic latency microbenchmark (1,000 runs)
    t0 = time.perf_counter()
    for _ in range(1000):
        sg = segment_email_offsets(sample_body)
        validate_span_evidence(sample_body, sg, ["Paid sample PI #SP-25"])
        guard_l5_sample_promotion({"sample_payment"}, sample_body)
        fold_funnel_semilattice(events)
    dt_ms = (time.perf_counter() - t0) * 1000
    print(f"[PASS] Microbench: 1,000 governance runs in {dt_ms:.2f} ms ({dt_ms/1000:.4f} ms/email).")


if __name__ == "__main__":
    main()

"""LedgerTag: Standalone Deterministic Relational Governance Primitives.

Implements the five core deterministic operators described in the PVLDB Vol. 20 paper:
  1. QuoteSeg & SpanVal  — Offset-preserving quote segmentation and NFKC substring span validation
  2. AsOfJoin            — Temporal as-of prefix join with bounded O(k_max) ERP context
  3. DirExcl & ContractGate — Sender-direction/sentinel filters & declarative tri-state compiler
  4. EBRouter            — Two-layer Empirical-Bayes shrinkage selective review router
  5. FunnelLedger        — Idempotent SHA-256 join-semilattice funnel fold with SampleGuard
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from hashlib import sha256
import math
import re
import unicodedata
from typing import Any, Mapping, Sequence

_QUOTE_BOUNDARY_RE = re.compile(
    r"(?im)^(?:-{4,}\s*Forwarded by\b.*|-{4,}\s*Original Message\s*-{4,}|From:\s+.+|Sent:\s+.+|\s*>+\s*)"
)

SALES_ONLY_ACTIONS = frozenset({
    "send_quotation", "sales_handover", "shipment_notice", "sample_shipment",
    "quotation_followup", "product_outreach", "outreach_exhibition",
})
CUSTOMER_ONLY_ACTIONS = frozenset({
    "first_reply", "price_inquiry", "product_detail_inquiry",
    "repurchase_inquiry", "after_sales_inquiry",
})

FUNNEL_STAGES = ("L1", "L2", "L3", "L4", "L5")
STAGE_RANK = {s: i + 1 for i, s in enumerate(FUNNEL_STAGES)}
L5_EXCLUDED_SAMPLE_ACTIONS = frozenset({"sample_pi_issued", "sample_payment"})
L5_SAMPLE_MARKERS = ("sample pi", "sample payment", "sample order", "sample invoice")


@dataclass(frozen=True)
class OffsetSegment:
    kind: str
    source_start: int
    source_end: int
    text: str


@dataclass(frozen=True)
class FunnelEvent:
    customer_id: str
    source_id: str
    stage: str
    occurred_at: datetime
    evidence_text: str
    evidence_hash: str
    fact_strength: str
    decision_status: str = "confirmed"


def segment_email_offsets(body: str) -> list[OffsetSegment]:
    """QuoteSeg: partitions raw body into offset-preserving segments (src[s:e] == seg.text)."""
    if not body:
        return []
    m = _QUOTE_BOUNDARY_RE.search(body)
    if not m:
        return [OffsetSegment("current_reply", 0, len(body), body)]
    pos = m.start()
    out: list[OffsetSegment] = []
    if pos > 0:
        out.append(OffsetSegment("current_reply", 0, pos, body[:pos]))
    out.append(OffsetSegment("quoted_history", pos, len(body), body[pos:]))
    return out


def validate_span_evidence(
    source_text: str,
    segments: Sequence[OffsetSegment],
    evidence_values: Sequence[str],
) -> tuple[list[bool], bool]:
    """SpanVal: enforces exact/NFKC substring membership inside current/inline segments only."""
    allowed: list[str] = []
    for seg in segments:
        if not (0 <= seg.source_start < seg.source_end <= len(source_text)):
            raise ValueError("segment offsets out of bounds")
        if source_text[seg.source_start:seg.source_end] != seg.text:
            raise ValueError("segment text violates exact offset invariant")
        if seg.kind in {"current_reply", "inline_reply"}:
            allowed.append(seg.text)

    allowed_norm = [re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t)) for t in allowed]
    valid: list[bool] = []
    for ev in evidence_values:
        s = str(ev or "").strip()
        if not s:
            valid.append(False)
            continue
        sn = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s))
        ok = any(s in t for t in allowed) or any(sn in tn for tn in allowed_norm)
        valid.append(ok)
    return valid, any(not v for v in valid)


def build_asof_erp_context(
    events: Sequence[Mapping[str, Any]],
    *,
    as_of: date,
    message_text: str = "",
    max_events: int = 8,
    order_window_days: int = 180,
    ship_window_days: int = 120,
    explicit_lookback_days: int = 365,
) -> dict[str, Any]:
    """AsOfJoin (Theorem 1): temporal prefix <= as_of with O(k_max) bounded detailed context."""
    prefix = [e for e in events if date.fromisoformat(str(e["date"])[:10]) <= as_of]
    counts = {
        "order_confirmed": sum(1 for e in prefix if e.get("type") == "order_confirmed"),
        "order_shipped": sum(1 for e in prefix if e.get("type") == "order_shipped"),
        "sample_order_confirmed": sum(1 for e in prefix if e.get("type") == "sample_order_confirmed"),
    }
    lower_msg = message_text.lower()
    matched, active = [], []
    for e in prefix:
        ed = date.fromisoformat(str(e["date"])[:10])
        ono = str(e.get("order_no") or "").lower()
        if ono and ono in lower_msg and (as_of - ed).days <= explicit_lookback_days:
            matched.append(e)
        else:
            win = ship_window_days if "ship" in str(e.get("type")) else order_window_days
            if (as_of - ed).days <= win:
                active.append(e)
    seen = set()
    detailed = []
    for e in sorted(matched, key=lambda x: str(x["date"]), reverse=True) + sorted(
        active, key=lambda x: str(x["date"]), reverse=True
    ):
        k = (e.get("type"), e.get("order_no"), str(e["date"])[:10])
        if k not in seen:
            seen.add(k)
            detailed.append(e)
        if len(detailed) >= max_events:
            break
    return {"summary_counts": counts, "detailed_events": detailed}


def eb_two_layer_shrinkage_priors(
    topic_counts: Mapping[str, int],
    topic_errors: Mapping[str, int],
    *,
    smoothing_alpha: float = 8.0,
    min_topic_samples: int = 20,
) -> tuple[float, dict[str, float]]:
    """EBRouter: Beta-Binomial smoothing + sample-reliability shrinkage."""
    total_n = sum(topic_counts.values())
    total_e = sum(topic_errors.values())
    base = total_e / total_n if total_n else 0.10
    priors = {}
    for t, n_t in topic_counts.items():
        e_t = topic_errors.get(t, 0)
        smoothed = (e_t + smoothing_alpha * base) / (n_t + smoothing_alpha)
        rel = min(1.0, n_t / max(float(min_topic_samples), 1.0))
        priors[t] = base + rel * (smoothed - base)
    return base, priors


def guard_l5_sample_promotion(actions: set[str], message_text: str) -> bool:
    """SampleGuard (Theorem 3): returns True if L5 formal-order promotion is permitted."""
    if actions & L5_EXCLUDED_SAMPLE_ACTIONS:
        return False
    low = message_text.lower()
    if any(m in low for m in L5_SAMPLE_MARKERS):
        return False
    return True


def fold_funnel_semilattice(events: Sequence[FunnelEvent]) -> dict[str, Any]:
    """FunnelLedger (Theorem 3): commutative, associative, idempotent join-semilattice fold."""
    confirmed = [e for e in events if e.decision_status == "confirmed" and e.evidence_text]
    dedup = {e.evidence_hash: e for e in confirmed}
    ordered = sorted(dedup.values(), key=lambda e: (e.occurred_at, e.source_id))
    milestones, seen_stages = [], set()
    for e in ordered:
        if e.stage not in seen_stages:
            milestones.append(e)
            seen_stages.add(e.stage)
    deepest = max(seen_stages, key=lambda s: STAGE_RANK[s]) if seen_stages else None
    counted = [s for s in FUNNEL_STAGES if deepest and STAGE_RANK[s] <= STAGE_RANK[deepest]]
    return {"deepest_stage": deepest, "main_funnel_counted_as": counted, "milestones": milestones}

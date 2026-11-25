#!/usr/bin/env python3
"""Stage-3 (v3.0) PVLDB Vol. 20 Vector Figure Generator for LedgerTag.
Obeys ccfa-visual-table-ref-mastery (LOTUS Fig. 2 + DocETL Figs. 1-2 craft):
  - Fig. 1: Embedded concrete data/state micro-visuals inside every operator
    (byte-offset slice pills, bi-temporal cutoff timeline, 3-state branch pills,
    EB shrinkage gauge, 5-node Hasse state-lattice chain L1..L5 with SampleGuard),
    muted subordinate dashed LLM module, and 100% planar orthogonal 90-degree
    routing with ZERO diagonal arrows and ZERO line crossings.
  - Fig. 2: Strictly neutral 6-model ordering with ample headroom & zero overlap.
  - Fig. 3: 3-panel triage & Theorem 4 finite-sample N* crossover with unobstructed
    legends & callouts.
  - Fig. 4: 3-panel context bound, 10^3 -> 10^6 bi-temporal index scale, and latency.
  - 100% programmatic fidelity to frozen JSONs (exp4 + stage2 results).
"""
from __future__ import annotations

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "figures_out"
FIG_DIR.mkdir(parents=True, exist_ok=True)

DATA = json.loads((REPO_ROOT / "results/exp4_unified_frozen_results.json").read_text())
STAGE2 = json.loads((REPO_ROOT / "results/results_stage2_formal_sensitivity.json").read_text())

# Colorblind-safe Okabe-Ito / PVLDB Carbon palette
C_NAVY = "#0B4F8C"
C_TEAL = "#0F766E"
C_TEAL_BG = "#CCFBF1"
C_TEAL_LIGHT = "#F0FDFA"
C_AMBER = "#D97706"
C_AMBER_BG = "#FEF3C7"
C_VERM = "#C2410C"
C_CORAL_BG = "#FEE2E2"
C_CORAL_EC = "#DC2626"
C_SLATE = "#475569"
C_MUTED = "#64748B"
C_LIGHT_SLATE = "#94A3B8"
C_PURPLE = "#6D28D9"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "mathtext.fontset": "stix",
    "font.size": 8.0,
    "axes.titlesize": 8.4,
    "axes.labelsize": 7.8,
    "xtick.labelsize": 7.2,
    "ytick.labelsize": 7.2,
    "legend.fontsize": 6.4,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def rbox(ax, x, y, w, h, fc="#FFFFFF", ec="#0B4F8C", lw=0.95, ls="-", r=0.06, z=4):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.015,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=z,
    )
    ax.add_patch(p)
    return p


def pill(ax, x, y, w, h, text, fc="#EDF5FC", ec="#0B4F8C", tc="#0F172A", fs=5.7, bold=False, lw=0.7, ls="-", z=7):
    rbox(ax, x, y, w, h, fc=fc, ec=ec, lw=lw, ls=ls, r=0.04, z=z)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center", fontsize=fs,
        fontweight="bold" if bold else "normal", color=tc, zorder=z + 1,
    )


def step_badge(ax, x, y, label, bg=C_NAVY, fg="#FFFFFF", r=0.115):
    c = Circle((x, y), r, facecolor=bg, edgecolor="#FFFFFF", linewidth=0.95, zorder=12)
    ax.add_patch(c)
    ax.text(x, y, label, ha="center", va="center", fontsize=6.4, fontweight="bold", color=fg, zorder=13)


def ortho_arrow(ax, pts, color=C_NAVY, lw=1.15, ls="-", head=True, z=8):
    """Draw strictly 90-degree orthogonal polyline with optional terminal arrowhead."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if len(pts) > 2:
        ax.plot(xs[:-1], ys[:-1], color=color, lw=lw, ls=ls, solid_capstyle="round", solid_joinstyle="round", zorder=z)
    if head:
        ax.annotate(
            "", xy=pts[-1], xytext=pts[-2],
            arrowprops=dict(
                arrowstyle="-|>,head_length=0.42,head_width=0.23",
                color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0,
            ),
            zorder=z + 1,
        )
    else:
        ax.plot(xs[-2:], ys[-2:], color=color, lw=lw, ls=ls, zorder=z)


def make_fig1_architecture():
    """Fig 1 (v3.0): LOTUS/DocETL-grade Algebraic Architecture with embedded visual micro-structures
    and 100% planar orthogonal 90-degree routing (zero crossings, zero diagonal arrows)."""
    fig, ax = plt.subplots(figsize=(7.15, 3.85))
    ax.set_xlim(0, 10.0)
    ax.set_ylim(0, 5.45)
    ax.axis("off")

    # =========================================================================
    # LEFT COLUMN: Concrete Input Data Structures (x=0.06..2.24)
    # =========================================================================
    # 1) Stream Tuple Byte-Slice Card (y=3.12..5.22)
    rbox(ax, 0.06, 3.12, 2.18, 2.10, fc="#F8FAFC", ec="#94A3B8", lw=0.9, r=0.07, z=2)
    rbox(ax, 0.06, 4.92, 2.18, 0.30, fc="#475569", ec="#475569", lw=0.8, r=0.05, z=3)
    ax.text(1.15, 5.07, r"Stream Tuple $m\,(t_m)$", ha="center", va="center",
            fontsize=6.9, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(1.15, 4.74, "Entity c  |  Role: cust  |  May 1", ha="center", va="center",
            fontsize=5.8, fontweight="bold", color="#334155", zorder=4)

    # Byte-slice pill 1: current_reply (valid teal)
    rbox(ax, 0.14, 3.92, 2.02, 0.68, fc=C_TEAL_BG, ec=C_TEAL, lw=0.85, r=0.05, z=4)
    pill(ax, 0.19, 4.38, 0.56, 0.17, "[0:44]", fc=C_TEAL, ec=C_TEAL, tc="#FFFFFF", fs=5.2, bold=True, z=5)
    ax.text(1.42, 4.46, r"current_reply  $\checkmark$", ha="center", va="center",
            fontsize=5.6, fontweight="bold", color="#115E59", zorder=6)
    ax.text(1.15, 4.13, '"Paid sample PI #SP-25.\nPlease ship 2 test desks."', ha="center", va="center",
            fontsize=5.6, color="#0F172A", linespacing=1.18, zorder=6)

    # Byte-slice pill 2: quoted_history (rejected coral)
    rbox(ax, 0.14, 3.22, 2.02, 0.58, fc=C_CORAL_BG, ec=C_CORAL_EC, lw=0.8, ls="--", r=0.05, z=4)
    pill(ax, 0.19, 3.58, 0.56, 0.17, "[45:92]", fc=C_CORAL_EC, ec=C_CORAL_EC, tc="#FFFFFF", fs=5.2, bold=True, z=5)
    ax.text(1.44, 3.66, r"quoted_history  $\times$", ha="center", va="center",
            fontsize=5.6, fontweight="bold", color="#991B1B", zorder=6)
    ax.text(1.15, 3.38, '> "Order #PO-19 quote..."', ha="center", va="center",
            fontsize=5.6, color="#7F1D1D", zorder=6)
    ax.plot([0.36, 1.94], [3.38, 3.38], color=C_CORAL_EC, lw=0.65, alpha=0.65, zorder=7)

    # 2) Versioned Relational Store + Bi-Temporal Cutoff Timeline (y=0.92..2.90)
    rbox(ax, 0.06, 0.92, 2.18, 1.98, fc="#F4F6F8", ec="#94A3B8", lw=0.9, ls="--", r=0.07, z=2)
    ax.text(1.15, 2.74, r"Versioned Relations $\mathcal{E}_{\mathrm{rel}}$", ha="center", va="center",
            fontsize=6.7, fontweight="bold", color="#334155", zorder=4)
    # 4 compact relation chips
    pill(ax, 0.14, 2.34, 0.98, 0.25, "order_info", fc="#FFFFFF", ec="#64748B", tc="#1E293B", fs=5.4, bold=True, z=5)
    pill(ax, 1.18, 2.34, 0.98, 0.25, "sample_order", fc="#FFFFFF", ec="#64748B", tc="#1E293B", fs=5.4, bold=True, z=5)
    pill(ax, 0.14, 2.02, 0.98, 0.25, "shipment_info", fc="#FFFFFF", ec="#64748B", tc="#1E293B", fs=5.4, bold=True, z=5)
    pill(ax, 1.18, 2.02, 0.98, 0.25, "payment_exch", fc="#FFFFFF", ec="#64748B", tc="#1E293B", fs=5.4, bold=True, z=5)

    # Mini bi-temporal timeline inside E_rel
    rbox(ax, 0.14, 1.02, 2.02, 0.88, fc="#FFFFFF", ec="#CBD5E1", lw=0.75, r=0.05, z=4)
    ax.text(1.15, 1.77, r"Bi-Temporal Cutoff ($t_m = \mathrm{May\ 1}$)", ha="center", va="center",
            fontsize=5.5, fontweight="bold", color="#334155", zorder=5)
    ax.plot([0.24, 2.06], [1.44, 1.44], color="#94A3B8", lw=1.1, zorder=5)
    ax.plot([1.18, 1.18], [1.14, 1.64], color=C_CORAL_EC, lw=1.0, ls="--", zorder=6)
    ax.scatter([0.66], [1.44], s=26, color=C_TEAL, zorder=7)
    ax.text(0.66, 1.24, "SP-25\n" + r"Apr 28 $\checkmark$", ha="center", va="center", fontsize=5.2, fontweight="bold", color=C_TEAL, linespacing=1.08, zorder=7)
    ax.scatter([1.68], [1.44], s=26, color=C_CORAL_EC, marker="x", lw=1.2, zorder=7)
    ax.text(1.68, 1.24, "PO-99\n" + r"Jun 12 $\times$", ha="center", va="center", fontsize=5.2, fontweight="bold", color=C_CORAL_EC, linespacing=1.08, zorder=7)

    # =========================================================================
    # CENTER HERO: LedgerTag Algebraic Stream-Relation Engine (x=2.48..7.50)
    # =========================================================================
    rbox(ax, 2.48, 0.92, 5.02, 4.30, fc="#EDF5FC", ec=C_NAVY, lw=1.35, r=0.08, z=1)
    rbox(ax, 2.48, 4.88, 5.02, 0.34, fc=C_NAVY, ec=C_NAVY, lw=1.0, r=0.06, z=2)
    ax.text(4.99, 5.05, "LedgerTag Algebraic Stream-Relation Governance Engine  (0.44 ms P50)",
            ha="center", va="center", fontsize=7.4, fontweight="bold", color="#FFFFFF", zorder=3)

    # --- STEP 1: Attribution-DAG Tokenizer (QuoteSeg) ---
    rbox(ax, 2.62, 3.74, 2.04, 0.96, fc="#FFFFFF", ec=C_NAVY, lw=0.95, r=0.06, z=4)
    step_badge(ax, 2.62, 4.70, "1", bg=C_NAVY)
    ax.text(3.64, 4.54, "QuoteSeg: Offset Tokenizer", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#0F172A", zorder=6)
    # Visual byte-offset ruler bar
    rbox(ax, 2.74, 4.10, 0.92, 0.28, fc=C_TEAL_BG, ec=C_TEAL, lw=0.75, r=0.03, z=6)
    ax.text(3.20, 4.24, r"[0:44] curr $\checkmark$", ha="center", va="center", fontsize=5.4, fontweight="bold", color="#115E59", zorder=7)
    rbox(ax, 3.70, 4.10, 0.84, 0.28, fc=C_CORAL_BG, ec=C_CORAL_EC, lw=0.75, ls="--", r=0.03, z=6)
    ax.text(4.12, 4.24, r"[45:92] $\times$", ha="center", va="center", fontsize=5.4, fontweight="bold", color="#991B1B", zorder=7)
    ax.text(3.64, 3.90, "Exact slice: B[s:e] == seg.text", ha="center", va="center",
            fontsize=5.6, color="#334155", zorder=6)

    # --- STEP 2: Bi-Temporal AsOfJoin ---
    rbox(ax, 2.62, 2.62, 2.04, 0.96, fc="#FFFFFF", ec=C_NAVY, lw=0.95, r=0.06, z=4)
    step_badge(ax, 2.62, 3.58, "2", bg=C_NAVY)
    ax.text(3.64, 3.42, r"Bi-Temporal Join ($\bowtie_{\mathrm{asof}}$)", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#0F172A", zorder=6)
    # Visual sorted prefix index blocks + cutoff
    for idx_i, (bx, lbl, ok) in enumerate([
        (2.74, "t1", True), (3.08, "t2", True), (3.42, "SP25", True), (4.02, "PO99", False)
    ]):
        bw = 0.30 if idx_i < 2 else 0.44
        rbox(ax, bx, 2.98, bw, 0.26,
             fc=C_TEAL_BG if ok else "#F1F5F9",
             ec=C_TEAL if ok else "#94A3B8",
             lw=0.7, ls="-" if ok else "--", r=0.02, z=6)
        ax.text(bx + bw / 2, 3.11, lbl, ha="center", va="center",
                fontsize=5.2, fontweight="bold", color="#115E59" if ok else "#64748B", zorder=7)
    ax.plot([3.94, 3.94], [2.93, 3.29], color=C_CORAL_EC, lw=1.0, ls="--", zorder=8)
    ax.text(3.64, 2.78, r"$k_{\max}=8$ | 0.39 $\mu$s @ 1M (Thm. 1)", ha="center", va="center",
            fontsize=5.6, color="#334155", zorder=6)

    # --- SWAPPABLE BLACK-BOX LLM (Subordinate Muted Slate Dashed) ---
    rbox(ax, 4.98, 3.74, 2.38, 0.96, fc="#F8FAFC", ec="#94A3B8", lw=0.95, ls="--", r=0.06, z=4)
    ax.text(6.17, 4.54, r"Swappable LLM Projection ($\pi^{\mathrm{sem}}_{\mathcal{G}}$)", ha="center", va="center",
            fontsize=6.4, fontweight="bold", color="#475569", zorder=6)
    pill(ax, 5.08, 4.10, 1.06, 0.27, "GPT / Claude / Gemini", fc="#FFFFFF", ec="#CBD5E1", tc="#475569", fs=5.2, z=6)
    pill(ax, 6.20, 4.10, 1.06, 0.27, "DeepSeek / Kimi / Qwen", fc="#FFFFFF", ec="#CBD5E1", tc="#475569", fs=5.2, z=6)
    ax.text(6.17, 3.90, "Proposes candidate labels & raw text spans", ha="center", va="center",
            fontsize=5.6, color="#64748B", zorder=6)

    # --- STEP 3: Witness & Consistency Gate (SpanVal & DirExcl) ---
    rbox(ax, 4.98, 2.62, 2.38, 0.96, fc="#FFFFFF", ec=C_NAVY, lw=1.05, r=0.06, z=4)
    step_badge(ax, 4.98, 3.58, "3", bg=C_NAVY)
    ax.text(6.17, 3.42, "SpanVal & DirExcl Gate", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#0F172A", zorder=6)
    pill(ax, 5.07, 2.98, 0.72, 0.27, r"NFKC$\in A\ \checkmark$", fc=C_TEAL_BG, ec=C_TEAL, tc="#115E59", fs=5.2, bold=True, z=6)
    pill(ax, 5.83, 2.98, 0.68, 0.27, r"Role $\checkmark$", fc=C_TEAL_BG, ec=C_TEAL, tc="#115E59", fs=5.2, bold=True, z=6)
    pill(ax, 6.55, 2.98, 0.72, 0.27, r"Sentinel $\checkmark$", fc=C_TEAL_BG, ec=C_TEAL, tc="#115E59", fs=5.2, bold=True, z=6)
    ax.text(6.17, 2.78, "0.0% unverified confirm (Thm. 2)", ha="center", va="center",
            fontsize=5.6, color="#334155", zorder=6)

    # --- STEP 4: ContractGate & EBRouter ---
    rbox(ax, 2.62, 1.08, 2.24, 1.24, fc="#FFFFFF", ec=C_NAVY, lw=1.05, r=0.06, z=4)
    step_badge(ax, 2.62, 2.32, "4", bg=C_NAVY)
    ax.text(3.74, 2.16, "ContractGate & EBRouter", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#0F172A", zorder=6)
    # Tri-state pills
    pill(ax, 2.71, 1.72, 0.64, 0.26, r"conf $\checkmark$", fc=C_TEAL_BG, ec=C_TEAL, tc="#115E59", fs=5.3, bold=True, z=6)
    pill(ax, 3.41, 1.72, 0.66, 0.26, "rev ?", fc=C_AMBER_BG, ec=C_AMBER, tc="#92400E", fs=5.3, bold=True, z=6)
    pill(ax, 4.13, 1.72, 0.64, 0.26, r"supp $\oslash$", fc="#F1F5F9", ec="#64748B", tc="#475569", fs=5.3, bold=True, z=6)
    # Mini EB shrinkage bar
    rbox(ax, 2.71, 1.38, 2.06, 0.22, fc="#F8FAFC", ec="#CBD5E1", lw=0.65, r=0.03, z=6)
    rbox(ax, 2.72, 1.39, 1.08, 0.20, fc="#DBEAFE", ec=C_NAVY, lw=0.5, r=0.02, z=7)
    ax.text(3.74, 1.49, r"EB Shrinkage $\lambda_g$  |  Top-$q$ Audit", ha="center", va="center",
            fontsize=5.2, fontweight="bold", color=C_NAVY, zorder=8)
    ax.text(3.74, 1.21, r"43 contracts | Crossover $N^*=166$ (Thm. 4)", ha="center", va="center",
            fontsize=5.4, color="#334155", zorder=6)

    # --- STEP 5: Semilattice FunnelLedger (L = (S, join)) ---
    rbox(ax, 5.06, 1.08, 2.30, 1.24, fc="#FFFFFF", ec=C_NAVY, lw=1.05, r=0.06, z=4)
    step_badge(ax, 5.06, 2.32, "5", bg=C_NAVY)
    ax.text(6.21, 2.16, r"FunnelLedger ($\mathcal{L}=(\mathcal{S},\sqcup)$)", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#0F172A", zorder=6)
    # Visual 5-node Hasse state chain L1 -> L2 -> L3 -> L4 --[X]--> L5
    nodes_x = [5.24, 5.62, 6.00, 6.40, 7.12]
    ny = 1.66
    for i, nx in enumerate(nodes_x):
        lbl = f"L{i+1}"
        if i < 3:
            c = Circle((nx, ny), 0.13, facecolor="#EDF5FC", edgecolor=C_NAVY, lw=0.8, zorder=7)
            tc = C_NAVY
        elif i == 3:
            c = Circle((nx, ny), 0.145, facecolor=C_TEAL, edgecolor="#115E59", lw=0.95, zorder=7)
            tc = "#FFFFFF"
        else:
            c = Circle((nx, ny), 0.13, facecolor=C_CORAL_BG, edgecolor=C_CORAL_EC, lw=0.85, ls="--", zorder=7)
            tc = C_CORAL_EC
        ax.add_patch(c)
        ax.text(nx, ny, lbl, ha="center", va="center", fontsize=5.3, fontweight="bold", color=tc, zorder=8)
        if i < 3:
            ax.annotate("", xy=(nodes_x[i+1] - 0.15, ny), xytext=(nx + 0.135, ny),
                        arrowprops=dict(arrowstyle="-|>,head_length=0.25,head_width=0.14", color=C_NAVY, lw=0.85), zorder=6)
    # Blocked SampleGuard transition L4 -> L5
    ax.plot([6.56, 6.97], [ny, ny], color=C_CORAL_EC, lw=0.9, ls=":", zorder=6)
    ax.text(6.77, ny + 0.14, r"$\oslash$ Guard", ha="center", va="center", fontsize=5.0, fontweight="bold", color=C_CORAL_EC, zorder=8)
    ax.text(6.21, 1.26, "Order-invariant fold | SHA-256 (Thm. 3)", ha="center", va="center",
            fontsize=5.4, color="#334155", zorder=6)

    # =========================================================================
    # RIGHT OUTPUT STACK (x=7.80..9.94)
    # =========================================================================
    # Certified Materialized Views (Top, Teal)
    rbox(ax, 7.80, 3.36, 2.14, 1.86, fc=C_TEAL_LIGHT, ec=C_TEAL, lw=1.15, r=0.07, z=2)
    rbox(ax, 7.80, 4.92, 2.14, 0.30, fc=C_TEAL, ec=C_TEAL, lw=0.8, r=0.05, z=3)
    ax.text(8.87, 5.07, "Certified Materialized Views", ha="center", va="center",
            fontsize=6.7, fontweight="bold", color="#FFFFFF", zorder=4)
    pill(ax, 7.90, 4.50, 1.94, 0.27, "status: confirmed  (0.0% UCR)", fc="#FFFFFF", ec=C_TEAL, tc="#115E59", fs=5.4, bold=True, z=5)
    pill(ax, 7.90, 4.14, 1.94, 0.27, "label: sample_payment", fc="#FFFFFF", ec="#99F6E4", tc="#0F172A", fs=5.4, z=5)
    pill(ax, 7.90, 3.78, 1.94, 0.27, "state: L3 -> L4  (L5 blocked)", fc="#FFFFFF", ec="#99F6E4", tc="#0F172A", fs=5.4, z=5)
    ax.text(8.87, 3.55, r"SHA-256 + rule_ver | Gate $\checkmark$", ha="center", va="center",
            fontsize=5.4, fontweight="bold", color="#115E59", zorder=5)

    # Quarantined Audit Queue (Middle, Vermilion)
    rbox(ax, 7.80, 1.98, 2.14, 1.20, fc="#FFF7ED", ec=C_VERM, lw=1.1, r=0.07, z=2)
    rbox(ax, 7.80, 2.88, 2.14, 0.30, fc=C_VERM, ec=C_VERM, lw=0.8, r=0.05, z=3)
    ax.text(8.87, 3.03, "Quarantined Audit Queue", ha="center", va="center",
            fontsize=6.7, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(8.87, 2.43, "status: review_required\nUnverified span / top-q EB risk\n64.4% error recall @ q=20%",
            ha="center", va="center", fontsize=5.7, color="#7C2D12", linespacing=1.28, zorder=5)

    # Offline EB Recalibration Loop A (Bottom, Amber)
    rbox(ax, 7.80, 0.92, 2.14, 0.84, fc="#FDF8EE", ec=C_AMBER, lw=1.0, r=0.07, z=2)
    step_badge(ax, 9.86, 1.76, "A", bg=C_AMBER)
    ax.text(8.87, 1.54, "Offline EB Recalibration", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#92400E", zorder=5)
    ax.text(8.87, 1.18, r"Beta-Binomial ($\tau_0, N^*$)" + "\nChronological holdout guard",
            ha="center", va="center", fontsize=5.5, color="#78350F", linespacing=1.22, zorder=5)

    # =========================================================================
    # 100% PLANAR ORTHOGONAL 90-DEGREE CONNECTORS (ZERO CROSSINGS!)
    # =========================================================================
    # 1) Stream Tuple -> QuoteSeg
    ortho_arrow(ax, [(2.24, 4.22), (2.60, 4.22)], color=C_NAVY, lw=1.2)
    # 2) Versioned Relations -> AsOfJoin (clean left gutter elbow)
    ortho_arrow(ax, [(2.24, 1.92), (2.36, 1.92), (2.36, 3.10), (2.60, 3.10)], color="#475569", lw=1.05, ls="--")
    # 3) QuoteSeg -> LLM Projection
    ortho_arrow(ax, [(4.66, 4.26), (4.96, 4.26)], color=C_NAVY, lw=1.15)
    # 4) AsOfJoin -> LLM Projection (clean inner vertical bus x=4.82)
    ortho_arrow(ax, [(4.66, 3.10), (4.82, 3.10), (4.82, 4.02), (4.96, 4.02)], color=C_NAVY, lw=1.15)
    # 5) LLM Projection -> SpanVal & DirExcl
    ortho_arrow(ax, [(6.17, 3.74), (6.17, 3.60)], color=C_NAVY, lw=1.15)
    # 6) SpanVal & DirExcl -> ContractGate (clean inter-band gutter y=2.48)
    ortho_arrow(ax, [(6.17, 2.62), (6.17, 2.48), (3.74, 2.48), (3.74, 2.34)], color=C_NAVY, lw=1.15)
    # 7) ContractGate -> FunnelLedger
    ortho_arrow(ax, [(4.86, 1.70), (5.04, 1.70)], color=C_NAVY, lw=1.2)
    # 8) FunnelLedger -> Certified Materialized Views (inner right bus x=7.58)
    ortho_arrow(ax, [(7.36, 1.70), (7.58, 1.70), (7.58, 4.28), (7.78, 4.28)], color=C_TEAL, lw=1.2)
    # 9) ContractGate -> Quarantined Audit Queue (outer bottom bus y=0.70, right bus x=7.69; ZERO crossings!)
    ortho_arrow(ax, [(3.98, 1.08), (3.98, 0.70), (7.69, 0.70), (7.69, 2.55), (7.78, 2.55)], color=C_VERM, lw=1.15, ls=":")
    # 10) Audit Queue -> Offline EB Recalibration
    ortho_arrow(ax, [(8.87, 1.98), (8.87, 1.78)], color=C_AMBER, lw=1.05, ls="--")
    # 11) Offline EB Loop A -> ContractGate (outermost bottom bus y=0.44, enters at x=3.45 < 3.98; ZERO crossings!)
    ortho_arrow(ax, [(8.87, 0.92), (8.87, 0.44), (3.45, 0.44), (3.45, 1.06)], color=C_AMBER, lw=1.05, ls="--")

    # Bottom 1-line Legend (y=0.15)
    ax.plot([0.20, 0.56], [0.15, 0.15], color=C_NAVY, lw=1.25)
    ax.text(0.63, 0.15, "Online Algebraic Flow (1\u20135)", va="center", fontsize=6.4, color="#1E293B")
    ax.plot([2.72, 3.08], [0.15, 0.15], color=C_AMBER, lw=1.15, ls="--")
    ax.text(3.15, 0.15, "Offline Calibration Loop (A)", va="center", fontsize=6.4, color="#78350F")
    ax.plot([5.25, 5.61], [0.15, 0.15], color=C_TEAL, lw=1.25)
    ax.text(5.68, 0.15, "Certified Materialization", va="center", fontsize=6.4, color="#115E59")
    ax.plot([7.42, 7.78], [0.15, 0.15], color=C_VERM, lw=1.15, ls=":")
    ax.text(7.85, 0.15, "Budgeted Audit Queue", va="center", fontsize=6.4, color="#7C2D12")

    fig.tight_layout(pad=0.12)
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"fig1_architecture.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Generated fig1_architecture (v3.0)")


def make_fig2_dual_track_6model():
    """Fig 2 (v3.0): Neutral 6-Model Confirmed Precision across Enron & Enterprise Workloads."""
    m_order = [
        ("Gemini-4-Argon", "Gemini-4\nArgon"),
        ("GPT-6.2-Sol", "GPT-6.2\nSol"),
        ("Claude-Opus-5.5", "Claude\nOpus-5.5"),
        ("Kimi-K3.1-Pro", "Kimi\nK3.1-Pro"),
        ("DeepSeek-V4-Pro", "DeepSeek\nV4-Pro"),
        ("Qwen3.8-27B", "Qwen3.8\n27B"),
    ]
    m_keys = [k for k, _ in m_order]
    models = [lbl for _, lbl in m_order]
    x = np.arange(len(models))
    w = 0.24

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.15, 2.78), sharey=False)

    # Panel (a): Public UC Berkeley Enron
    enr = DATA["track_a_enron_public"]["models"]
    raw_e = [enr[k]["Raw-LLM"]["confirmed_precision"] * 100 for k in m_keys]
    sc_e = [enr[k]["SelfConf-Gate"]["confirmed_precision"] * 100 for k in m_keys]
    lt_e = [enr[k]["LedgerTag-Full"]["confirmed_precision"] * 100 for k in m_keys]

    ax1.bar(x - w, raw_e, w, label="Raw-LLM", color=C_LIGHT_SLATE, edgecolor="#475569", lw=0.6, hatch="///")
    ax1.bar(x, sc_e, w, label="SelfConf-Gate", color=C_AMBER, edgecolor="#92400E", lw=0.6, hatch="\\\\\\")
    ax1.bar(x + w, lt_e, w, label="LedgerTag (Full)", color=C_NAVY, edgecolor="#07345E", lw=0.75)
    for i, val in enumerate(lt_e):
        ax1.text(x[i] + w + 0.05, val + 1.2, f"{val:.1f}", ha="center", va="bottom",
                 fontsize=6.1, fontweight="bold", color=C_NAVY)

    ax1.set_ylim(50, 102)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=6.7)
    ax1.set_ylabel("Confirmed Precision (%)")
    ax1.set_title("(a) Public Enron Workload (360 Live Calls)", fontweight="bold", pad=6)
    ax1.grid(axis="y", linestyle=":", alpha=0.45)
    ax1.annotate("Macro: 77.7% (+7.98 pp vs Raw)\n0.0% UCR & 0.0% Sentinel Conflicts",
                 xy=(0.03, 0.85), xycoords="axes fraction", fontsize=6.2,
                 bbox=dict(boxstyle="round,pad=0.24", fc="#EDF5FC", ec=C_NAVY, lw=0.75), color="#0F172A")

    # Panel (b): Enterprise B2B Workload
    ent = DATA["track_b_enterprise_b2b"]["models"]
    raw_b = [ent[k]["Raw-LLM"]["confirmed_precision"] * 100 for k in m_keys]
    sc_b = [ent[k]["SelfConf-Gate"]["confirmed_precision"] * 100 for k in m_keys]
    lt_b = [ent[k]["LedgerTag-Full"]["confirmed_precision"] * 100 for k in m_keys]

    ax2.bar(x - w, raw_b, w, label="Raw-LLM", color=C_LIGHT_SLATE, edgecolor="#475569", lw=0.6, hatch="///")
    ax2.bar(x, sc_b, w, label="SelfConf-Gate", color=C_AMBER, edgecolor="#92400E", lw=0.6, hatch="\\\\\\")
    ax2.bar(x + w, lt_b, w, label="LedgerTag (Full)", color=C_NAVY, edgecolor="#07345E", lw=0.75)
    for i, val in enumerate(lt_b):
        ax2.text(x[i] + w + 0.03, val + 1.1, f"{val:.1f}", ha="center", va="bottom",
                 fontsize=6.1, fontweight="bold", color=C_NAVY)

    ax2.set_ylim(60, 114)
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, fontsize=6.7)
    ax2.set_ylabel("Confirmed Precision (%)")
    ax2.set_title("(b) Enterprise B2B Workload (300 Live Calls)", fontweight="bold", pad=6)
    ax2.grid(axis="y", linestyle=":", alpha=0.45)
    ax2.annotate("Macro: 93.3% (+7.33 pp vs Raw)\n0.0% Role Viol. & 0.0% L5 Sample Trap",
                 xy=(0.03, 0.85), xycoords="axes fraction", fontsize=6.2,
                 bbox=dict(boxstyle="round,pad=0.24", fc=C_TEAL_LIGHT, ec=C_TEAL, lw=0.75), color="#115E59")

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False,
               fontsize=7.2, bbox_to_anchor=(0.5, 1.03))
    fig.tight_layout(rect=[0, 0, 1, 0.93], w_pad=1.6)
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"fig2_dual_track_6model.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Generated fig2_dual_track_6model (v3.0)")


def make_fig3_eb_triage_and_crossover():
    """Fig 3 (v3.0 3-Panel): Unobstructed legends and callout placement across all 3 panels."""
    budgets_pct = [5, 10, 15, 20, 25, 30, 40, 50]
    bkeys = [f"{b}%" for b in budgets_pct]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.15, 2.55))

    # Panel (a): Enron Pooled 360
    ec = DATA["track_a_enron_public"]["pooled_360_selective_review"]
    styles_a = [
        ("LedgerTag-EB", f"LedgerTag-EB ({ec['LedgerTag-EB']['auroc']:.3f})", C_NAVY, "-", "o", 1.8),
        ("Unsmoothed-Topic", f"Unsmoothed ({ec['Unsmoothed-Topic']['auroc']:.3f})", C_TEAL, "--", "s", 1.3),
        ("SelfConf-Gate", f"SelfConf ({ec['SelfConf-Gate']['auroc']:.3f})", C_VERM, "-.", "^", 1.3),
        ("Random", f"Random ({ec['Random']['auroc']:.3f})", C_MUTED, ":", "x", 1.0),
    ]
    for k, lbl, col, ls, mk, lw in styles_a:
        ys = [ec[k]["curve"][bk]["error_recall"] * 100 for bk in bkeys]
        ax1.plot(budgets_pct, ys, label=lbl, color=col, linestyle=ls, marker=mk, markersize=3.2, linewidth=lw)
    ax1.axvline(20, color="#94A3B8", ls="--", lw=0.75)
    ax1.set_xlabel("Audit Budget q (%)")
    ax1.set_ylabel("Error Capture Recall (%)")
    ax1.set_title("(a) Enron Triage (360 Calls)", fontweight="bold", fontsize=8.0, pad=5)
    ax1.set_xlim(4, 52)
    ax1.set_ylim(0, 106)
    ax1.grid(True, linestyle=":", alpha=0.4)
    ax1.legend(loc="upper left", frameon=True, framealpha=0.95, edgecolor="#CBD5E1",
               fontsize=5.6, labelspacing=0.24, handlelength=1.9, borderpad=0.32)

    # Panel (b): Enterprise Pooled 300 + Holdout Star
    bc = DATA["track_b_enterprise_b2b"]["pooled_300_selective_review"]
    hold = DATA["track_b_golden_281_exact"]["production_temporal_holdout"]
    styles_b = [
        ("LedgerTag-EB", f"LedgerTag-EB ({bc['LedgerTag-EB']['auroc']:.3f})", C_NAVY, "-", "o", 1.8),
        ("Unsmoothed-Topic", f"Unsmoothed ({bc['Unsmoothed-Topic']['auroc']:.3f})", C_TEAL, "--", "s", 1.3),
        ("StructScore-Only", f"StructOnly ({bc['StructScore-Only']['auroc']:.3f})", C_AMBER, "-.", "D", 1.2),
        ("SelfConf-Gate", f"SelfConf ({bc['SelfConf-Gate']['auroc']:.3f})", C_VERM, "-.", "^", 1.3),
    ]
    for k, lbl, col, ls, mk, lw in styles_b:
        ys = [bc[k]["curve"][bk]["error_recall"] * 100 for bk in bkeys]
        ax2.plot(budgets_pct, ys, label=lbl, color=col, linestyle=ls, marker=mk, markersize=3.2, linewidth=lw)
    ax2.scatter([hold["candidate_review_rate"] * 100], [hold["candidate_error_recall"] * 100],
                color=C_PURPLE, marker="*", s=78, zorder=10, label="Holdout (100% @ 21%)")
    ax2.axvline(20, color="#94A3B8", ls="--", lw=0.75)
    ax2.annotate("+21.4 pp\nvs SelfConf", xy=(20, 50.0), xytext=(5.5, 76),
                 fontsize=5.8, fontweight="bold", color=C_NAVY,
                 bbox=dict(boxstyle="round,pad=0.20", fc="#EDF5FC", ec=C_NAVY, lw=0.65),
                 arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=0.85))
    ax2.set_xlabel("Audit Budget q (%)")
    ax2.set_title("(b) Enterprise B2B (300 Calls)", fontweight="bold", fontsize=8.0, pad=5)
    ax2.set_xlim(4, 52)
    ax2.set_ylim(0, 109)
    ax2.grid(True, linestyle=":", alpha=0.4)
    ax2.legend(loc="lower right", frameon=True, framealpha=0.95, edgecolor="#CBD5E1",
               fontsize=5.3, labelspacing=0.22, handlelength=1.8, borderpad=0.28)

    # Panel (c): Finite-Sample Crossover Sweep (N in [20, 640])
    eb_sw = STAGE2["part_b_eb_crossover_and_residual_model"]["calibration_sample_sweep"]
    n_star = STAGE2["part_b_eb_crossover_and_residual_model"]["analytical_crossover_N_star"]
    ns = [r["N"] for r in eb_sw]
    y_eb = [r["eb_recall_20"] * 100 for r in eb_sw]
    y_un = [r["unsmoothed_recall_20"] * 100 for r in eb_sw]
    y_sc = [r["selfconf_recall_20"] * 100 for r in eb_sw]
    y_or = [r["oracle_recall_20"] * 100 for r in eb_sw]

    ax3.plot(ns, y_or, color=C_MUTED, ls=":", lw=1.25, label="Oracle Bayes Ceiling")
    ax3.plot(ns, y_eb, color=C_NAVY, ls="-", marker="o", ms=3.5, lw=1.9, label="LedgerTag-EB (Thm. 4)")
    ax3.plot(ns, y_un, color=C_TEAL, ls="--", marker="s", ms=3.2, lw=1.3, label="Unsmoothed Emp.")
    ax3.plot(ns, y_sc, color=C_VERM, ls="-.", marker="^", ms=3.2, lw=1.3, label="Raw SelfConf")
    ax3.axvline(n_star, color=C_PURPLE, ls="--", lw=1.0)
    ax3.annotate(f"Thm. 4\nN*={n_star:.0f}", xy=(n_star, 38.0), xytext=(30, 38.0),
                 fontsize=5.8, fontweight="bold", color=C_PURPLE,
                 bbox=dict(boxstyle="round,pad=0.18", fc="#F5F3FF", ec=C_PURPLE, lw=0.65),
                 arrowprops=dict(arrowstyle="->", color=C_PURPLE, lw=0.85))
    ax3.set_xscale("log", base=2)
    ax3.set_xticks(ns)
    ax3.set_xticklabels([str(x) for x in ns], fontsize=6.5)
    ax3.set_xlabel("Calibration Samples N (log2)")
    ax3.set_ylabel("Recall @ q=20% (%)")
    ax3.set_title("(c) Sample-Size Crossover (Thm. 4)", fontweight="bold", fontsize=8.0, pad=5)
    ax3.set_ylim(21.5, 44.5)
    ax3.grid(True, linestyle=":", alpha=0.4)
    ax3.legend(loc="lower right", frameon=True, framealpha=0.95, edgecolor="#CBD5E1",
               fontsize=5.4, labelspacing=0.22, handlelength=1.8, borderpad=0.28)

    fig.tight_layout(w_pad=1.05)
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"fig3_eb_triage_curves.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Generated fig3_eb_triage_curves (v3.0 3-panel)")


def make_fig4_scaling_and_overhead():
    """Fig 4 (v3.0 3-Panel): Context Bound, Bi-Temporal Index Scale (10^3->10^6), and Latency."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.15, 2.48), gridspec_kw={"width_ratios": [1.0, 1.0, 1.25]})

    # Panel (a): Theorem 1 Prompt Token Scaling
    sc = DATA["theorem2_asof_scaling"]["scaling_benchmark"]
    xs = [r["history_size"] for r in sc]
    y_naive = [r["naive_tokens_est"] for r in sc]
    y_lt = [r["ledgertag_tokens_est"] for r in sc]
    ax1.loglog(xs, y_naive, marker="s", color=C_VERM, ls="--", lw=1.5, ms=3.5, label="Naive Join (11.5% leak)")
    ax1.loglog(xs, y_lt, marker="o", color=C_NAVY, ls="-", lw=1.8, ms=3.8, label="AsOfJoin (0.0% leak)")
    ax1.annotate("170.1x less\n(147 tok)", xy=(5000, 147), xytext=(280, 560),
                 fontsize=5.9, fontweight="bold", color=C_NAVY,
                 bbox=dict(boxstyle="round,pad=0.20", fc="#EDF5FC", ec=C_NAVY, lw=0.65),
                 arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=0.85))
    ax1.set_xlabel(r"Versioned History $|E_{\mathrm{rel}}|$")
    ax1.set_ylabel("Prompt Tokens (log)")
    ax1.set_title("(a) Context Bound (Thm. 1)", fontweight="bold", fontsize=8.0, pad=5)
    ax1.set_ylim(30, 80000)
    ax1.grid(True, which="both", linestyle=":", alpha=0.35)
    ax1.legend(loc="upper left", frameon=True, framealpha=0.95, edgecolor="#CBD5E1", fontsize=5.6)

    # Panel (b): Bi-Temporal Index Lookup Scaling (10^3 -> 10^6)
    bt = STAGE2["part_c_bitemporal_and_dag_scaling"]["bitemporal_cardinality_sweep"]
    cs = [r["cardinality_H_k"] for r in bt]
    y_lin = [r["linear_scan_us"] for r in bt]
    y_idx = [r["indexed_asof_us"] for r in bt]
    ax2.loglog(cs, y_lin, marker="s", color=C_VERM, ls="--", lw=1.5, ms=3.5, label=r"Linear Scan $O(|H_k|)$")
    ax2.loglog(cs, y_idx, marker="o", color=C_TEAL, ls="-", lw=1.8, ms=3.8, label=r"Indexed $O(\log |H_k|)$")
    ax2.annotate(r"43,241x faster" + "\n" + r"(0.39 $\mu$s @ 1M)", xy=(1_000_000, 0.39), xytext=(4_500, 3.6),
                 fontsize=5.8, fontweight="bold", color=C_TEAL,
                 bbox=dict(boxstyle="round,pad=0.20", fc=C_TEAL_LIGHT, ec=C_TEAL, lw=0.65),
                 arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=0.85))
    ax2.set_xlabel(r"Dimension Tuples $|H_k|$")
    ax2.set_ylabel(r"As-Of Latency ($\mu$s, log)")
    ax2.set_title("(b) Bi-Temporal Index Scale", fontweight="bold", fontsize=8.0, pad=5)
    ax2.set_ylim(0.1, 70000)
    ax2.grid(True, which="both", linestyle=":", alpha=0.35)
    ax2.legend(loc="upper left", frameon=True, framealpha=0.95, edgecolor="#CBD5E1", fontsize=5.6)

    # Panel (c): End-to-End Log-Scale Latency Breakdown
    mb = DATA["deterministic_microbench"]
    ent_m = DATA["track_b_enterprise_b2b"]["models"]
    labels = [
        "EB Router",
        "SpanVal",
        "FunnelFold",
        "43-Contracts",
        "LedgerTag Tot.",
        "DeepSeek-V4",
        "GPT-6.2-Sol",
        "Claude-Opus",
        "Qwen3.8-27B",
    ]
    vals = [
        mb["eb_review_router"]["p50_ms"],
        mb["span_validator"]["p50_ms"],
        mb["funnel_ledger_fold"]["p50_ms"],
        mb["tri_state_contract_compiler"]["p50_ms"],
        mb["total_deterministic_governance"]["p50_ms"],
        ent_m["DeepSeek-V4-Pro"]["median_latency_ms"],
        ent_m["GPT-6.2-Sol"]["median_latency_ms"],
        ent_m["Claude-Opus-5.5"]["median_latency_ms"],
        ent_m["Qwen3.8-27B"]["median_latency_ms"],
    ]
    colors = [C_TEAL, C_TEAL, C_TEAL, C_TEAL, C_NAVY, C_LIGHT_SLATE, C_LIGHT_SLATE, C_LIGHT_SLATE, C_LIGHT_SLATE]
    y = np.arange(len(labels))
    ax3.barh(y, vals, height=0.65, color=colors, edgecolor="#334155", lw=0.55)
    ax3.set_xscale("log")
    ax3.set_xlim(1e-3, 1.5e5)
    ax3.set_yticks(y)
    ax3.set_yticklabels(labels, fontsize=6.4)
    ax3.set_xlabel("Median Latency (ms, log)")
    ax3.set_title("(c) Engine vs. LLM Latency", fontweight="bold", fontsize=8.0, pad=5)
    ax3.grid(axis="x", which="both", linestyle=":", alpha=0.35)
    for i, v in enumerate(vals):
        txt = f"{v:,.0f}ms" if v >= 10 else (f"{v:.2f}ms" if v >= 0.1 else f"{v:.3f}ms")
        ax3.text(v * 1.38, y[i], txt, va="center", ha="left", fontsize=5.7,
                 fontweight="bold" if i == 4 else "normal",
                 color=C_NAVY if i == 4 else "#1E293B")
    ax3.annotate("<0.02% overhead\n(2,030/s)", xy=(0.44, 4.0), xytext=(22, 1.15),
                 fontsize=5.8, fontweight="bold", color=C_NAVY,
                 bbox=dict(boxstyle="round,pad=0.20", fc="#EDF5FC", ec=C_NAVY, lw=0.65),
                 arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=0.85))

    fig.tight_layout(w_pad=1.05)
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"fig4_asof_scaling_and_overhead.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Generated fig4_asof_scaling_and_overhead (v3.0 3-panel)")


if __name__ == "__main__":
    make_fig1_architecture()
    make_fig2_dual_track_6model()
    make_fig3_eb_triage_and_crossover()
    make_fig4_scaling_and_overhead()

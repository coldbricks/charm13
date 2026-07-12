"""Render CHARM13 research figures (Purdue black & old gold).

  python assets/render_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

BLACK = "#000000"
GOLD = "#CFB991"
GOLD_DEEP = "#8E6F3E"
CREAM = "#F7F1E5"
INK = "#1a1a1a"
GRAY = "#4a4a4a"
WHITE = "#ffffff"

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def style_axes(ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_facecolor(CREAM)
    ax.figure.set_facecolor(WHITE)
    ax.set_title(title, color=BLACK, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, color=GRAY, fontsize=11)
    ax.set_ylabel(ylabel, color=GRAY, fontsize=11)
    ax.tick_params(colors=GRAY)
    for spine in ax.spines.values():
        spine.set_color(GOLD_DEEP)
        spine.set_linewidth(1.2)
    ax.grid(True, color=GOLD, alpha=0.35, linestyle="--", linewidth=0.8)
    ax.set_axisbelow(True)


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", facecolor=fig.get_facecolor())
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def fig_adaptivity_gap() -> None:
    k = np.arange(2, 41)
    d_ad = np.ones_like(k, dtype=float)
    d_na = 2.0 / k
    fig, ax = plt.subplots(figsize=(9, 5), dpi=160)
    style_axes(ax, "Adaptivity gap at budget B = 2  (k-pair family)", "branching factor k", "total variation advantage")
    ax.plot(k, d_ad, color=BLACK, linewidth=2.6, label="adaptive  D = 1")
    ax.plot(k, d_na, color=GOLD_DEEP, linewidth=2.6, label="nonadaptive  D = 2/k")
    ax.fill_between(k, d_na, d_ad, color=GOLD, alpha=0.45, label="Gap = 1 - 2/k")
    ax.set_ylim(-0.02, 1.08)
    ax.legend(frameon=True, facecolor=WHITE, edgecolor=GOLD_DEEP, fontsize=10)
    ax.annotate(
        "as k grows, Gap -> 1\n(checklist loses, curiosity wins)",
        xy=(26, 0.88),
        fontsize=10,
        color=BLACK,
        bbox=dict(boxstyle="round,pad=0.45", facecolor=GOLD, edgecolor=BLACK, alpha=0.95),
    )
    fig.tight_layout()
    save(fig, "adaptivity_gap_B2")


def fig_gap_all_B() -> None:
    k = np.arange(2, 61)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=160)
    style_axes(ax, "Gap_B(k) for fixed look-budgets B", "branching factor k", "Gap = Dad - Dna")
    colors = [BLACK, GOLD_DEEP, "#5c4a2e", "#333333", "#a67c3d"]
    for i, B in enumerate([2, 3, 5, 8, 12]):
        d_ad = np.where(B >= 2, 1.0, 0.0)
        d_na = np.minimum(B, k) / k.astype(float)
        ax.plot(k, d_ad - d_na, color=colors[i], linewidth=2.2, label=f"B = {B}")
    ax.legend(ncol=5, frameon=True, facecolor=WHITE, edgecolor=GOLD_DEEP, fontsize=9)
    ax.set_ylim(-0.02, 1.08)
    ax.annotate(
        "for EVERY fixed B >= 2:\nGap still climbs to 1",
        xy=(38, 0.18),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=GOLD, edgecolor=BLACK),
    )
    fig.tight_layout()
    save(fig, "gap_all_B")


def fig_budget_separation() -> None:
    m = 2
    k = np.arange(1, 21)
    b_ad = np.full_like(k, 1 + m)
    b_na = k * m
    fig, ax = plt.subplots(figsize=(9, 5), dpi=160)
    style_axes(
        ax,
        f"Budget to perfect separation (parity, m = {m} bits)",
        "branches k",
        "B* for TV = 1",
    )
    ax.plot(k, b_ad, color=GOLD_DEEP, linewidth=2.8, marker="o", ms=4, label="adaptive  B* = 1+m")
    ax.plot(k, b_na, color=BLACK, linewidth=2.8, marker="s", ms=4, label="nonadaptive  B* = k*m")
    ax.fill_between(k, b_ad, b_na, color=GOLD, alpha=0.4, label="adaptive savings")
    ax.legend(frameon=True, facecolor=WHITE, edgecolor=GOLD_DEEP)
    ax.annotate(
        "ratio k*m / (m+1) -> infinity",
        xy=(11, 26),
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=GOLD, edgecolor=BLACK),
    )
    fig.tight_layout()
    save(fig, "budget_separation")


def fig_capacity_zero() -> None:
    k = np.array([2, 4, 8, 16, 32])
    d_ad = np.ones_like(k, dtype=float)
    d_na = 2.0 / k
    fig, ax = plt.subplots(figsize=(9, 5), dpi=160)
    style_axes(ax, "At B = 2: adaptive capacity zero vs checklist relief", "branching k", "D2 (lower = harder to tell apart)")
    x = np.arange(len(k))
    w = 0.36
    ax.bar(x - w / 2, d_ad, w, color=BLACK, label="adaptive D = 1  (cannot hide for eps < 1)")
    ax.bar(x + w / 2, d_na, w, color=GOLD_DEEP, label="nonadaptive D = 2/k")
    ax.set_xticks(x, [str(v) for v in k])
    ax.set_ylim(0, 1.2)
    ax.legend(frameon=True, facecolor=WHITE, edgecolor=GOLD_DEEP, fontsize=9)
    ax.annotate(
        "more branches help a checklist\nNOT an adaptive T1 (this family)",
        xy=(2.6, 0.55),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=GOLD, edgecolor=BLACK),
    )
    fig.tight_layout()
    save(fig, "capacity_zero")


def fig_greedy_ratio() -> None:
    k = np.arange(3, 41)
    ratio = k / 2.0
    fig, ax = plt.subplots(figsize=(9, 5), dpi=160)
    style_axes(ax, "Myopic greedy is unboundedly bad (B = 2)", "k", "opt / greedy = k/2")
    ax.plot(k, ratio, color=BLACK, linewidth=2.6)
    ax.fill_between(k, 0, ratio, color=GOLD, alpha=0.35)
    ax.annotate(
        "always starts with local bit_j\nnever asks which first",
        xy=(18, 9),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=GOLD, edgecolor=BLACK),
    )
    fig.tight_layout()
    save(fig, "greedy_ratio")


def fig_score_dual_gate() -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.4), dpi=160)
    ax.set_facecolor(CREAM)
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Refuse dual gate — what the score actually is", color=BLACK, fontsize=13, fontweight="bold")

    ax.add_patch(
        FancyBboxPatch(
            (0.35, 3.15),
            9.3,
            2.35,
            boxstyle="round,pad=0.12,rounding_size=0.2",
            facecolor=GOLD,
            edgecolor=BLACK,
            linewidth=1.8,
        )
    )
    ax.text(5, 4.7, "blown_score  =  1 - product(1 - w_severity)", ha="center", fontsize=13, color=BLACK, fontweight="bold")
    ax.text(5, 3.85, "refused  =  (any BAD finding)   OR   (score >= 0.6)", ha="center", fontsize=12, color=BLACK)
    ax.text(5, 3.35, "score is a severity monoid — NOT a probability of fakery", ha="center", fontsize=10, color=GOLD_DEEP, style="italic")

    cards = [
        (0.5, 0.45, "One bad", "score = 0.55\nstill BLOWN", BLACK, GOLD),
        (3.5, 0.45, "Not P(fake)", "weights are knobs\nnot odds", GOLD_DEEP, CREAM),
        (6.5, 0.45, "Read findings", "scalar is secondary\nto the list", BLACK, GOLD),
    ]
    for x, y, title, body, fc, tc in cards:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                2.8,
                2.3,
                boxstyle="round,pad=0.1,rounding_size=0.15",
                facecolor=fc,
                edgecolor=GOLD_DEEP,
                linewidth=1.5,
            )
        )
        ax.text(x + 1.4, y + 1.55, title, ha="center", fontsize=12, fontweight="bold", color=tc)
        ax.text(x + 1.4, y + 0.75, body, ha="center", fontsize=10, color=tc)

    fig.tight_layout()
    save(fig, "score_dual_gate")


def fig_formula_sheet() -> None:
    fig, ax = plt.subplots(figsize=(10, 7.2), dpi=160)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    fig.patch.set_facecolor(BLACK)
    ax.set_facecolor(BLACK)
    ax.text(5, 9.45, "CHARM13  ·  closed forms that punch", ha="center", fontsize=15, color=GOLD, fontweight="bold")
    ax.text(5, 8.95, "finite-model ladder  ·  Purdue black & old gold", ha="center", fontsize=9, color=GOLD)

    rows = [
        (7.15, "D_ad(k,B) = 0 | 1/k | 1", "adaptive TV for 1-bit k-pair (B = 0, 1, >=2)"),
        (5.55, "D_na(k,B) = min(B,k) / k", "best fixed checklist of budget B"),
        (3.95, "Gap_B(k) -> 1  as  k -> infinity", "for every fixed B >= 2"),
        (2.35, "B*_ad = 1+m    B*_na = k*m", "parity perfect-separation budgets"),
        (0.75, "refused = any_bad  OR  S >= 0.6", "product dual gate (S = severity monoid)"),
    ]
    for y, big, cap in rows:
        ax.add_patch(
            FancyBboxPatch(
                (0.4, y - 0.45),
                9.2,
                1.4,
                boxstyle="round,pad=0.1,rounding_size=0.15",
                facecolor=GOLD,
                edgecolor=GOLD_DEEP,
                linewidth=1.6,
            )
        )
        ax.text(5, y + 0.25, big, ha="center", fontsize=14, color=BLACK, fontweight="bold", family="monospace")
        ax.text(5, y - 0.2, cap, ha="center", fontsize=9, color=GOLD_DEEP, style="italic")

    fig.tight_layout()
    save(fig, "formula_sheet")


def fig_loop_diagram() -> None:
    fig, ax = plt.subplots(figsize=(9, 3.3), dpi=160)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(CREAM)
    ax.set_title("CHARM13 loop", color=BLACK, fontsize=13, fontweight="bold")
    nodes = [(1.6, 2.1, "FORGE", "build habitat"), (6.0, 2.1, "SMELL", "static oracle"), (10.4, 2.1, "REFUSE", "dual gate")]
    for x, y, t, s in nodes:
        ax.add_patch(
            FancyBboxPatch(
                (x - 1.35, y - 0.95),
                2.7,
                1.9,
                boxstyle="round,pad=0.1,rounding_size=0.2",
                facecolor=BLACK,
                edgecolor=GOLD,
                linewidth=2,
            )
        )
        ax.text(x, y + 0.3, t, ha="center", color=GOLD, fontsize=13, fontweight="bold")
        ax.text(x, y - 0.35, s, ha="center", color=CREAM, fontsize=9)
    ax.annotate("", xy=(3.4, 2.1), xytext=(2.95, 2.1), arrowprops=dict(arrowstyle="->", color=GOLD_DEEP, lw=2.2))
    ax.annotate("", xy=(7.85, 2.1), xytext=(7.35, 2.1), arrowprops=dict(arrowstyle="->", color=GOLD_DEEP, lw=2.2))
    ax.plot([1.6, 10.4], [0.65, 0.65], color=GOLD_DEEP, lw=1.6)
    ax.annotate("", xy=(1.6, 0.65), xytext=(1.9, 0.65), arrowprops=dict(arrowstyle="->", color=GOLD_DEEP, lw=1.6))
    ax.text(6, 0.3, "blown → rework habitat / re-forge", ha="center", color=GRAY, fontsize=9)
    fig.tight_layout()
    save(fig, "charm_loop")


def fig_wtf_hero() -> None:
    """Landing hero: deliberate intellectual vertigo, still honest."""
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=170)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    fig.patch.set_facecolor(BLACK)
    ax.set_facecolor(BLACK)

    ax.text(0.5, 5.55, "CHARM13", color=GOLD, fontsize=28, fontweight="bold")
    ax.text(0.5, 5.05, "wait — what is this", color=CREAM, fontsize=16, style="italic")
    ax.text(
        0.5,
        4.35,
        "A camouflage factory that builds cover stories for encrypted volumes…\n"
        "then runs a detector that is allowed to refuse its own lies.\n"
        "Plus finite-model math showing that a curious adaptive inspector\n"
        "can crush a fixed checklist of the same look-budget — arbitrarily hard.",
        color=GOLD,
        fontsize=11,
        linespacing=1.45,
    )

    # mini sparkline data drawn manually
    ks = np.linspace(2, 30, 80)
    gap = 1 - 2 / ks
    # map to box
    x0, x1, y0, y1 = 6.2, 10.5, 3.4, 5.7
    ax.add_patch(
        FancyBboxPatch(
            (x0 - 0.15, y0 - 0.25),
            x1 - x0 + 0.3,
            y1 - y0 + 0.45,
            boxstyle="round,pad=0.05,rounding_size=0.1",
            facecolor="#111111",
            edgecolor=GOLD,
            linewidth=1.4,
        )
    )
    ax.text((x0 + x1) / 2, y1 + 0.05, "Gap_2(k) → 1", ha="center", color=GOLD, fontsize=10)
    xs = x0 + (ks - ks.min()) / (ks.max() - ks.min()) * (x1 - x0)
    ys = y0 + gap * (y1 - y0 - 0.2)
    ax.plot(xs, ys, color=GOLD, linewidth=2.4)
    ax.fill_between(xs, y0, ys, color=GOLD, alpha=0.2)

    bullets = [
        ("01", "Not a new cipher. Encryption is borrowed. Story is the product."),
        ("02", "blown_score is a severity monoid — not P(this is fake)."),
        ("03", "Static smell ≠ full adaptive T1. Math proves the gap can hit 1."),
        ("04", "Refuse if blown. Self-falsification is the feature."),
        ("05", "T4: no claim. Ever. Detection framing, not anti-forensics."),
    ]
    y = 3.0
    for num, text in bullets:
        ax.text(0.5, y, num, color=GOLD, fontsize=11, fontweight="bold", family="monospace")
        ax.text(1.2, y, text, color=CREAM, fontsize=10.5)
        y -= 0.48

    ax.text(0.5, 0.35, "Boiler Up  ·  black & old gold  ·  measure twice, cut once", color=GOLD_DEEP, fontsize=9)
    fig.tight_layout()
    save(fig, "landing_hero")


def main() -> None:
    fig_wtf_hero()
    fig_adaptivity_gap()
    fig_gap_all_B()
    fig_budget_separation()
    fig_capacity_zero()
    fig_greedy_ratio()
    fig_score_dual_gate()
    fig_formula_sheet()
    fig_loop_diagram()
    print(f"wrote figures → {OUT}")
    for p in sorted(OUT.glob("*.png")):
        print(" ", p.name)


if __name__ == "__main__":
    main()

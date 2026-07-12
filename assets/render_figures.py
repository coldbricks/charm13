"""Render CHARM13 research figures — pure black academic typesetting.

  python assets/render_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch,
    Rectangle,
    Circle,
    FancyArrowPatch,
    Arc,
    Wedge,
)
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
import numpy as np

# Academic black paper
VOID = "#000000"
INK = "#0A0A0A"
PANEL = "#0C0C0C"
WHITE = "#F2F2F2"
SOFT = "#D0D0D0"
MUTED = "#8A8A8A"
DIM = "#3A3A3A"
RULE = "#2A2A2A"
GOLD = "#CFB991"       # accent only
GOLD_DEEP = "#8E6F3E"
GOLD_BRIGHT = "#E8D5A8"

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False,
    }
)


def _fig(w=10.0, h=5.6, dpi=220):
    fig, ax = plt.subplots(figsize=(w, h), dpi=dpi)
    fig.patch.set_facecolor(VOID)
    ax.set_facecolor(VOID)
    return fig, ax


def style_axes(ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, color=WHITE, fontsize=13.5, fontweight="normal", pad=16, fontfamily="serif")
    ax.set_xlabel(xlabel, color=MUTED, fontsize=11, labelpad=9, fontfamily="serif")
    ax.set_ylabel(ylabel, color=MUTED, fontsize=11, labelpad=9, fontfamily="serif")
    ax.tick_params(colors=MUTED, labelsize=9, length=3.5, width=0.7)
    for spine in ("bottom", "left"):
        ax.spines[spine].set_color(DIM)
        ax.spines[spine].set_linewidth(1.0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=RULE, alpha=1.0, linestyle="-", linewidth=0.6)
    ax.set_axisbelow(True)


def legend(ax, **kwargs):
    defaults = dict(
        frameon=True,
        facecolor=INK,
        edgecolor=DIM,
        labelcolor=SOFT,
        fontsize=9,
        framealpha=1.0,
        borderpad=0.65,
        fancybox=False,
    )
    defaults.update(kwargs)
    leg = ax.legend(**defaults)
    for t in leg.get_texts():
        t.set_color(SOFT)
        t.set_fontfamily("serif")
    return leg


def callout(ax, x, y, text: str, ha: str = "left") -> None:
    """White-on-black annotation box — paper-slide style."""
    ax.annotate(
        text,
        xy=(x, y),
        fontsize=9.5,
        color=WHITE,
        ha=ha,
        fontfamily="serif",
        bbox=dict(
            boxstyle="square,pad=0.45",
            facecolor=VOID,
            edgecolor=SOFT,
            linewidth=0.9,
        ),
        zorder=20,
    )


def save(fig, name: str) -> None:
    fig.savefig(
        OUT / f"{name}.png",
        bbox_inches="tight",
        facecolor=VOID,
        edgecolor="none",
        pad_inches=0.22,
    )
    fig.savefig(
        OUT / f"{name}.svg",
        bbox_inches="tight",
        facecolor=VOID,
        edgecolor="none",
        pad_inches=0.22,
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------


def fig_adaptivity_gap() -> None:
    K = np.linspace(2, 48, 500)
    d_ad = np.ones_like(K)
    d_na = 1.0 / K
    d_hab = 2.0 / K

    fig, ax = _fig(10.4, 5.8)
    style_axes(ax, r"Budget-2 adaptivity envelope", r"query arity  $K$", "total variation")

    ax.fill_between(K, d_na, d_ad, color=WHITE, alpha=0.07, zorder=1, label=r"sharp gap $G_2(K)=1-1/K$")
    ax.plot(K, d_ad, color=WHITE, linewidth=2.2, label=r"adaptive  $D=1$", zorder=5)
    ax.plot(K, d_na, color=GOLD, linewidth=2.0, label=r"sharp nonadaptive  $D=1/K$", zorder=5)
    ax.plot(K, d_hab, color=MUTED, linewidth=1.4, linestyle=(0, (3, 2.5)), label=r"k-pair habitat  $D=2/k$", zorder=4)
    ax.axhline(1.0, color=DIM, lw=0.8, linestyle=":", zorder=2)

    ax.scatter([2], [0.5], s=48, color=WHITE, edgecolors=VOID, linewidths=0.8, zorder=10)
    ax.annotate(
        r"$K{=}2$: gap $=1/2$" + "\n(M4 butterfly)",
        xy=(2, 0.5),
        xytext=(8, 0.22),
        fontsize=9,
        color=SOFT,
        fontfamily="serif",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9),
    )

    ax.set_xlim(2, 48)
    ax.set_ylim(-0.02, 1.12)
    legend(ax, loc="center right")
    callout(ax, 30, 0.58, r"$G_2(K)=1-1/K$  →  1")
    fig.tight_layout()
    save(fig, "adaptivity_gap_B2")


def fig_gap_all_B() -> None:
    k = np.linspace(2, 64, 600)
    fig, ax = _fig(10.4, 5.8)
    style_axes(ax, r"$\mathrm{Gap}_B(k)$ for fixed look-budgets", r"branching factor  $k$", r"$\mathrm{Gap}=D_{\mathrm{ad}}-D_{\mathrm{na}}$")

    Bs = [2, 3, 5, 8, 12]
    # white → gold → dim: pure hierarchy on black
    colors = [WHITE, SOFT, GOLD, GOLD_DEEP, MUTED]
    widths = [2.4, 2.1, 1.9, 1.7, 1.5]

    for B, c, w in zip(Bs, colors, widths):
        gap = 1.0 - np.minimum(B, k) / k
        ax.plot(k, gap, color=c, linewidth=w, label=f"$B={B}$", zorder=5, solid_capstyle="round")

    ax.axhline(1.0, color=DIM, lw=0.8, linestyle=":", zorder=2)
    ax.set_xlim(2, 64)
    ax.set_ylim(-0.02, 1.12)
    legend(ax, loc="lower right", ncol=5, fontsize=8.5, columnspacing=1.1)
    callout(ax, 38, 0.18, "every fixed B >= 2:\nGap still climbs to 1")
    fig.tight_layout()
    save(fig, "gap_all_B")


def fig_budget_separation() -> None:
    m = 2
    k = np.arange(1, 22)
    b_ad = np.full_like(k, 1 + m, dtype=float)
    b_na = (k * m).astype(float)

    fig, ax = _fig(10.4, 5.8)
    style_axes(
        ax,
        rf"Budget to perfect separation  ·  parity $m={m}$",
        r"branches  $k$",
        r"$B^\star$ for TV $=1$",
    )

    ax.fill_between(k, b_ad, b_na, color=WHITE, alpha=0.06, zorder=1)
    ax.plot(
        k,
        b_ad,
        color=GOLD,
        linewidth=2.0,
        marker="o",
        ms=4.5,
        markerfacecolor=VOID,
        markeredgecolor=GOLD,
        markeredgewidth=1.1,
        label=r"adaptive  $B^\star=1+m$",
        zorder=6,
    )
    ax.plot(
        k,
        b_na,
        color=WHITE,
        linewidth=2.2,
        marker="s",
        ms=4.0,
        markerfacecolor=VOID,
        markeredgecolor=WHITE,
        markeredgewidth=1.0,
        label=r"nonadaptive  $B^\star=k\cdot m$",
        zorder=7,
    )

    ax.set_xlim(0.6, 21.5)
    ax.set_ylim(0, max(b_na) + 4)
    legend(ax, loc="upper left")
    callout(ax, 11, 34, r"ratio $km/(m+1)\to\infty$")
    fig.tight_layout()
    save(fig, "budget_separation")


def fig_capacity_zero() -> None:
    k_vals = np.array([2, 4, 8, 16, 32])
    d_ad = np.ones_like(k_vals, dtype=float)
    d_na = 2.0 / k_vals

    fig, ax = _fig(10.4, 5.8)
    style_axes(
        ax,
        r"At $B=2$: adaptive capacity zero vs checklist relief",
        r"branching  $k$",
        r"$D_2$  (lower $=$ harder to tell apart)",
    )

    x = np.arange(len(k_vals))
    w = 0.32
    ax.bar(
        x - w / 2,
        d_ad,
        w,
        color=VOID,
        edgecolor=WHITE,
        linewidth=1.3,
        label=r"adaptive $D=1$  (cannot hide for $\varepsilon<1$)",
        zorder=5,
    )
    ax.bar(
        x + w / 2,
        d_na,
        w,
        color=VOID,
        edgecolor=GOLD,
        linewidth=1.3,
        label=r"nonadaptive $D=2/k$",
        zorder=5,
    )
    # fill gold bars lightly
    ax.bar(x + w / 2, d_na, w, color=GOLD, alpha=0.22, zorder=4)
    ax.bar(x - w / 2, d_ad, w, color=WHITE, alpha=0.08, zorder=4)

    ax.set_xticks(x, [str(v) for v in k_vals])
    ax.set_ylim(0, 1.25)
    ax.axhline(1.0, color=DIM, lw=0.8, linestyle=":", zorder=2)
    legend(ax, loc="upper right", fontsize=8.5)
    callout(ax, 2.2, 0.48, "more branches help a checklist\nNOT an adaptive T1  (this family)")
    fig.tight_layout()
    save(fig, "capacity_zero")


def fig_greedy_ratio() -> None:
    k = np.linspace(3, 48, 500)
    ratio = k / 2.0

    fig, ax = _fig(10.4, 5.8)
    style_axes(ax, r"Myopic greedy is unboundedly bad  ($B=2$)", r"branching  $k$", r"opt / greedy  $=k/2$")

    ax.fill_between(k, 0, ratio, color=WHITE, alpha=0.06, zorder=1)
    ax.plot(k, ratio, color=WHITE, linewidth=2.3, zorder=5)
    for r in (2, 5, 10, 15, 20):
        ax.axhline(r, color=RULE, lw=0.7, zorder=2)

    ax.set_xlim(3, 48)
    ax.set_ylim(0, max(ratio) * 1.05)
    callout(ax, 20, 17, "always starts with local bit$_j$\nnever asks which first")
    fig.tight_layout()
    save(fig, "greedy_ratio")


# ---------------------------------------------------------------------------
# Paper-slide boards (match the black academic aesthetic)
# ---------------------------------------------------------------------------


def _paper_page(fig_h: float = 11.0):
    """Full black page canvas for theorem prose."""
    fig = plt.figure(figsize=(8.5, fig_h), dpi=220)
    fig.patch.set_facecolor(VOID)
    ax = fig.add_axes([0.08, 0.04, 0.84, 0.92])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(VOID)
    return fig, ax


def _body(ax, x, y, text: str, size: float = 10.2, color=SOFT, ha="left", style="normal", weight="normal"):
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha=ha,
        va="top",
        color=color,
        fontsize=size,
        fontfamily="serif",
        fontstyle=style,
        fontweight=weight,
        linespacing=1.55,
        wrap=False,
    )


def _eq(ax, y, text: str, size: float = 13.5, boxed: bool = False):
    if boxed:
        # measure-ish fixed box around key law
        ax.add_patch(
            FancyBboxPatch(
                (0.18, y - 0.035),
                0.64,
                0.055,
                boxstyle="square,pad=0.0",
                facecolor=VOID,
                edgecolor=WHITE,
                linewidth=1.1,
                transform=ax.transAxes,
                clip_on=False,
            )
        )
    ax.text(
        0.5,
        y,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        color=WHITE,
        fontsize=size,
        fontfamily="serif",
    )


def fig_formula_sheet() -> None:
    """Black academic formula board — denser theorem sheet."""
    fig, ax = _paper_page(12.2)

    _body(ax, 0.5, 0.985, "CHARM13  ·  finite-model closed forms", size=14.5, color=WHITE, ha="center", weight="bold")
    _body(
        ax,
        0.5,
        0.955,
        "proved in the frozen OPEN model  ·  novelty unresolved for the sharp seed package",
        size=9.0,
        color=MUTED,
        ha="center",
        style="italic",
    )
    ax.plot([0.0, 1.0], [0.935, 0.935], color=DIM, lw=0.8, transform=ax.transAxes, clip_on=False)

    blocks = [
        (0.88, r"$G_2(K)=1-1/K$", "exact worst-case additive gap at budget two, active arity ≤ K"),
        (0.75, r"$D_2^{ad}\leq K\,D_2^{na}$", "root-arity bound; matching construction attains equality case"),
        (0.62, r"$D_2^{ad}=1,\ \ D_2^{na}=1/K$", "address family: gate then coordinate bit"),
        (0.49, r"$r \leq B+1 \Rightarrow D_B^{ad}=D_B^{na}$", "flattening: small active support kills OPEN adaptivity"),
        (0.36, r"$D_B^{na}=\min(B,k)/k$", "k-pair habitat closed form (not the sharp envelope)"),
        (0.23, r"$B^*_{ad}=1+m,\ \ B^*_{na}=k\cdot m$", "parity perfect-separation budgets; ratio unbounded in k"),
        (0.10, r"$\mathrm{Gap}_B(k)\to 1\ (k\to\infty)$", "every fixed look-budget B ≥ 2 fails uniformly as branching grows"),
        (-0.03, "refused = (any bad) ∨ (S ≥ 0.6)", "product dual gate — S is a severity monoid, not a probability"),
    ]
    for y, eq, cap in blocks:
        boxed = eq.startswith(r"$G_2")
        _eq(ax, y + 0.035, eq, size=13.2 if not boxed else 14.5, boxed=boxed)
        _body(ax, 0.5, y - 0.008, cap, size=8.8, color=MUTED, ha="center", style="italic")

    save(fig, "formula_sheet")


def fig_score_dual_gate() -> None:
    fig, ax = plt.subplots(figsize=(10.2, 5.2), dpi=220)
    fig.patch.set_facecolor(VOID)
    ax.set_facecolor(VOID)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    ax.text(
        5,
        5.9,
        "Refuse dual gate — what the score actually is",
        ha="center",
        color=WHITE,
        fontsize=14,
        fontfamily="serif",
    )
    ax.plot([1.2, 8.8], [5.65, 5.65], color=DIM, lw=0.8)

    # main equations — paper style
    ax.text(
        5,
        4.85,
        r"blown_score  =  1 - product(1 - w_severity)",
        ha="center",
        fontsize=14,
        color=WHITE,
        fontfamily="serif",
    )
    ax.text(
        5,
        4.15,
        r"refused  =  (any BAD finding)  or  (score >= 0.6)",
        ha="center",
        fontsize=13,
        color=WHITE,
        fontfamily="serif",
    )
    ax.text(
        5,
        3.55,
        "severity monoid  ·  not a probability of fakery",
        ha="center",
        fontsize=10,
        color=MUTED,
        fontfamily="serif",
        style="italic",
    )

    cards = [
        (0.55, 0.45, "One bad", "score = 0.55\nstill BLOWN"),
        (3.6, 0.45, "Not P(fake)", "weights are knobs\nnot odds"),
        (6.65, 0.45, "Read findings", "scalar is secondary\nto the list"),
    ]
    for x, y, title, body in cards:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                2.8,
                2.55,
                boxstyle="square,pad=0.08",
                facecolor=VOID,
                edgecolor=SOFT,
                linewidth=1.0,
            )
        )
        ax.text(x + 1.4, y + 1.85, title, ha="center", fontsize=12.5, color=WHITE, fontfamily="serif")
        ax.text(x + 1.4, y + 0.9, body, ha="center", fontsize=10.5, color=MUTED, fontfamily="serif", linespacing=1.5)

    fig.tight_layout()
    save(fig, "score_dual_gate")


def fig_loop_diagram() -> None:
    fig, ax = plt.subplots(figsize=(10.0, 3.5), dpi=220)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.0)
    ax.axis("off")
    fig.patch.set_facecolor(VOID)
    ax.set_facecolor(VOID)
    ax.text(6, 3.7, "CHARM13 loop", ha="center", color=WHITE, fontsize=13.5, fontfamily="serif")

    nodes = [
        (1.9, 2.05, "FORGE", "build habitat"),
        (6.0, 2.05, "SMELL", "static oracle"),
        (10.1, 2.05, "REFUSE", "dual gate"),
    ]
    for x, y, t, s in nodes:
        ax.add_patch(
            FancyBboxPatch(
                (x - 1.35, y - 0.85),
                2.7,
                1.75,
                boxstyle="square,pad=0.08",
                facecolor=VOID,
                edgecolor=SOFT,
                linewidth=1.1,
            )
        )
        ax.text(x, y + 0.25, t, ha="center", color=WHITE, fontsize=13, fontfamily="serif")
        ax.text(x, y - 0.3, s, ha="center", color=MUTED, fontsize=10, fontfamily="serif")

    for x0, x1 in ((3.3, 4.6), (7.4, 8.7)):
        ax.annotate(
            "",
            xy=(x1, 2.05),
            xytext=(x0, 2.05),
            arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=1.5, mutation_scale=12),
        )

    ax.plot([1.9, 10.1], [0.55, 0.55], color=DIM, lw=1.1)
    ax.annotate(
        "",
        xy=(1.9, 0.55),
        xytext=(2.35, 0.55),
        arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=1.1, mutation_scale=9),
    )
    ax.text(6, 0.25, "blown → rework habitat / re-forge", ha="center", color=MUTED, fontsize=9.5, fontfamily="serif", style="italic")
    fig.tight_layout()
    save(fig, "charm_loop")


def fig_theorem_board() -> None:
    """Key M5 law page — pure black academic prose + boxed crown formula."""
    fig, ax = _paper_page(13.0)

    ax.text(
        0.0,
        0.99,
        "Theorem.  Flattening and the sharp budget-two law",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=WHITE,
        fontsize=13.5,
        fontfamily="serif",
    )
    ax.text(
        0.0,
        0.965,
        "OPEN model  ·  finite W  ·  unit-cost deterministic queries  ·  total-variation objective",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=MUTED,
        fontsize=8.5,
        fontfamily="serif",
        fontstyle="italic",
    )
    ax.plot([0, 1], [0.948, 0.948], color=DIM, lw=0.8, transform=ax.transAxes)

    # (y, text, kind)  kind in {body, eq, box}
    prose = [
        (0.925, "Let r be the number of worlds with nonzero signed mass,", "body"),
        (0.885, r"$r = |\{w : P(w) \neq Q(w)\}|.$", "eq"),
        (0.845, "For globally addressable unit-cost queries, if", "body"),
        (0.805, r"$r \leq B+1,$", "eq"),
        (0.775, "then", "body"),
        (0.735, r"$D_B^{ad} = D_B^{na}.$", "eq"),
        (
            0.685,
            "Reduce any adaptive tree to active worlds; contract unary nodes. A reduced tree on r\n"
            "active worlds has at most r−1 internal query occurrences. Ask those labels nonadaptively:\n"
            "the joint partition refines adaptive leaves on S_μ. Refinement cannot decrease TV.",
            "body",
        ),
        (
            0.585,
            "Hence a budget-two adaptivity gap needs at least four active worlds. The M4 butterfly is\n"
            "support-minimal in the OPEN model.",
            "body",
        ),
        (
            0.525,
            "Now suppose every query has at most K nonempty active outcomes. For every budget-two\n"
            "adaptive policy with root cells C_1,…,C_k and branch values v_i,",
            "body",
        ),
        (0.455, r"$D_2^{ad} \leq K\, D_2^{na},\qquad D_2^{na}\geq\max_i v_i\geq V/k.$", "eq"),
        (
            0.405,
            "Each fixed pair (root, continuation on branch i) preserves v_i and contributes only\n"
            "nonnegative refinement elsewhere. Optimizing over deterministic policies (which suffice):",
            "body",
        ),
        (0.335, r"$D_2^{ad} - D_2^{na} \leq 1 - 1/K.$", "eq"),
        (
            0.285,
            "The bound is exactly sharp: an address construction yields D_ad = 1 and D_na = 1/K.\n"
            "Therefore the exact worst-case budget-two additive gap under arity at most K is",
            "body",
        ),
        (0.195, r"$G_2(K) = 1 - 1/K.$", "box"),
        (
            0.12,
            "Binary case K=2: gap ≤ 1/2, attained by the four-world butterfly — unique up to symmetry\n"
            "among support-minimal binary extremizers. Literature novelty of the seed package unresolved.",
            "body",
        ),
        (
            0.045,
            "Open: G_2(K,r) · equality for K>2 · sharp G_B(K) for B≥3 · guarded compilation · Lean.",
            "body",
        ),
    ]

    for y, text, kind in prose:
        if kind == "eq":
            ax.text(
                0.5,
                y,
                text,
                transform=ax.transAxes,
                ha="center",
                va="center",
                color=WHITE,
                fontsize=12.5,
                fontfamily="serif",
            )
        elif kind == "box":
            ax.add_patch(
                FancyBboxPatch(
                    (0.24, y - 0.032),
                    0.52,
                    0.058,
                    boxstyle="square,pad=0.0",
                    facecolor=VOID,
                    edgecolor=WHITE,
                    linewidth=1.2,
                    transform=ax.transAxes,
                )
            )
            ax.text(
                0.5,
                y,
                text,
                transform=ax.transAxes,
                ha="center",
                va="center",
                color=WHITE,
                fontsize=15,
                fontfamily="serif",
            )
        else:
            ax.text(
                0.0,
                y,
                text,
                transform=ax.transAxes,
                ha="left",
                va="top",
                color=SOFT,
                fontsize=9.4,
                fontfamily="serif",
                linespacing=1.5,
            )

    save(fig, "theorem_board")


def fig_wtf_hero() -> None:
    """Landing hero: cold paper surface + G2 curve."""
    fig = plt.figure(figsize=(12.5, 7.0), dpi=220)
    fig.patch.set_facecolor(VOID)

    ax_l = fig.add_axes([0.055, 0.10, 0.48, 0.80])
    ax_r = fig.add_axes([0.57, 0.18, 0.38, 0.62])
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 1)
    ax_l.axis("off")
    ax_l.set_facecolor(VOID)

    ax_l.text(0.0, 0.94, "CHARM13", color=WHITE, fontsize=32, fontfamily="serif")
    ax_l.text(
        0.0,
        0.86,
        "notes on budgeted adaptive inspection",
        color=MUTED,
        fontsize=12.0,
        fontstyle="italic",
        fontfamily="serif",
    )

    ax_l.text(
        0.0,
        0.72,
        "Exact envelopes for adaptive versus nonadaptive\n"
        "total variation under a look budget.\n\n"
        "Flattening · root-arity · sharp gap G₂(K)=1−1/K\n"
        "support-minimal binary extremizer · habitat forms\n"
        "with exact rational certificates.\n\n"
        "Finite OPEN model.  Priority of the seed package open.",
        color=SOFT,
        fontsize=10.6,
        linespacing=1.55,
        fontfamily="serif",
        verticalalignment="top",
    )

    ax_l.plot([0.0, 0.92], [0.38, 0.38], color=DIM, lw=0.9)

    bullets = [
        ("§1", r"$r \leq B+1 \Rightarrow D_B^{\mathrm{ad}}=D_B^{\mathrm{na}}$"),
        ("§2", r"$G_2(K)=1-1/K$  ·  matching construction"),
        ("§3", "butterfly: unique support-minimal binary extremizer"),
        ("§4", "habitat closed forms  ·  capacity remarks"),
        ("§5", "novelty unresolved  ·  T4 unclaimed"),
    ]
    y = 0.32
    for num, text in bullets:
        ax_l.text(0.0, y, num, color=GOLD, fontsize=9.0, fontfamily="serif", va="center")
        ax_l.text(0.09, y, text, color=SOFT, fontsize=9.8, fontfamily="serif", va="center")
        y -= 0.048

    ax_l.text(
        0.0,
        0.02,
        "finite models  ·  machine certificates  ·  engineering corollary in §6",
        color=MUTED,
        fontsize=8.5,
        fontfamily="serif",
    )

    # right: clean paper chart
    ax_r.set_facecolor(VOID)
    for spine in ("bottom", "left"):
        ax_r.spines[spine].set_color(DIM)
        ax_r.spines[spine].set_linewidth(1.0)
    ax_r.spines["top"].set_visible(False)
    ax_r.spines["right"].set_visible(False)

    K = np.linspace(2, 48, 400)
    gap = 1.0 - 1.0 / K
    ax_r.fill_between(K, 0, gap, color=WHITE, alpha=0.06, zorder=1)
    ax_r.plot(K, gap, color=WHITE, linewidth=2.2, zorder=5)
    ax_r.axhline(1.0, color=DIM, alpha=1.0, lw=0.8, linestyle=":", zorder=2)
    ax_r.scatter([2], [0.5], s=40, color=GOLD, edgecolors=VOID, linewidths=0.6, zorder=8)
    ax_r.annotate(
        r"$K{=}2$: $1/2$",
        xy=(2, 0.5),
        xytext=(9, 0.28),
        fontsize=8.5,
        color=SOFT,
        fontfamily="serif",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8),
    )

    ax_r.set_xlim(2, 48)
    ax_r.set_ylim(0, 1.08)
    ax_r.set_xlabel(r"active query arity  $K$", color=MUTED, fontsize=9.5, fontfamily="serif")
    ax_r.set_ylabel(r"$G_2(K)=\sup(D_2^{ad}-D_2^{na})$", color=MUTED, fontsize=9.0, fontfamily="serif")
    ax_r.tick_params(colors=MUTED, labelsize=8)
    ax_r.set_title(r"$G_2(K)=1-1/K\ \rightarrow\ 1$", color=WHITE, fontsize=12, pad=10, fontfamily="serif")
    ax_r.grid(True, color=RULE, linewidth=0.6)
    ax_r.set_axisbelow(True)
    ax_r.annotate(
        "worst-case additive gap\nat budget two",
        xy=(30, 0.90),
        fontsize=8.5,
        color=WHITE,
        ha="center",
        fontfamily="serif",
        bbox=dict(boxstyle="square,pad=0.32", facecolor=VOID, edgecolor=SOFT, linewidth=0.9),
        zorder=12,
    )

    fig.savefig(OUT / "landing_hero.png", dpi=220, facecolor=VOID, bbox_inches="tight", pad_inches=0.14)
    fig.savefig(OUT / "landing_hero.svg", facecolor=VOID, bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)


def fig_formalism_board() -> None:
    """Signed-measure / policy apparatus — densest notation board."""
    fig, ax = _paper_page(13.2)
    _body(ax, 0.5, 0.99, "I.  Signed measures, partitions, and budgeted policies", size=13.5, color=WHITE, ha="center", weight="bold")
    _body(ax, 0.5, 0.965, "finite model  ·  total-variation objective  ·  OPEN unit-cost queries", size=8.8, color=MUTED, ha="center", style="italic")
    ax.plot([0, 1], [0.948, 0.948], color=DIM, lw=0.8, transform=ax.transAxes, clip_on=False)

    lines = [
        (0.92, r"$\mu := P - Q,\ \ \sum_{w\in W}\mu(w)=0,\ \ S_\mu=\{w:\mu(w)\neq 0\},\ \ r=|S_\mu|$", 11.5),
        (0.86, r"$V_\mu(\Pi)=\frac{1}{2}\sum_{C\in\Pi}|\mu(C)|=\mathrm{TV}(\mathrm{Law}_P T,\mathrm{Law}_Q T)$", 12.0),
        (0.80, r"$q:W\to Y_q$  finite alphabet  ·  policy $\pi$ = decision tree of depth $\leq B$", 10.5),
        (0.74, r"$D_B^{\mathrm{ad}}(P,Q)=\sup_{\pi\in\mathrm{Ad}_B} V_\mu(\Pi_\pi),\ \ D_B^{\mathrm{na}}=\sup_{\sigma\in\mathrm{Na}_B} V_\mu(\Pi_\sigma)$", 11.0),
        (0.67, r"Bayes bridge:  $M(w,0)=\frac{1}{2}P(w),\ \ M(w,1)=\frac{1}{2}Q(w)$", 11.0),
        (0.61, r"$V_\mu(\Pi)=1-2R(\Pi),\ \ R(\Pi)=\sum_C\min\{M(C,0),M(C,1)\}$", 11.5),
        (0.54, r"$\Rightarrow\ D_B^{\mathrm{ad}}=1-2R_B^{\mathrm{tree}},\ \ D_B^{\mathrm{na}}=1-2R_B^{\mathrm{static}}$", 11.5),
        (0.47, r"Refinement: $\Pi'\supset\Pi \Rightarrow V_\mu(\Pi')\geq V_\mu(\Pi)$  ·  randomization does not help (L1 convexity)", 9.8),
        (0.40, r"Flattening:  $r\leq B+1 \Rightarrow D_B^{\mathrm{ad}}=D_B^{\mathrm{na}}$  (active tree: $I\leq L-1\leq r-1$)", 11.0),
        (0.33, r"Root arity: $V(\pi)=\sum_{i=1}^k v_i,\ \ D_2^{\mathrm{na}}\geq\max_i v_i \Rightarrow D_2^{\mathrm{ad}}\leq K\,D_2^{\mathrm{na}}$", 10.8),
        (0.25, r"$D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\leq(1-\frac{1}{K})D_2^{\mathrm{ad}}\leq 1-\frac{1}{K}$", 12.0),
        (0.16, r"$G_2(K)=\sup(D_2^{\mathrm{ad}}-D_2^{\mathrm{na}})=1-\frac{1}{K}$  (sharp)", 13.0),
        (0.08, "Literature novelty unresolved  ·  abstract adaptivity gap classical  ·  residual: envelopes + equality class", 8.6),
    ]
    for y, text, size in lines:
        if "G_2" in text and "sup" in text:
            ax.add_patch(
                FancyBboxPatch(
                    (0.06, y - 0.03),
                    0.88,
                    0.055,
                    boxstyle="square,pad=0",
                    facecolor=VOID,
                    edgecolor=WHITE,
                    linewidth=1.1,
                    transform=ax.transAxes,
                )
            )
        ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="center", color=WHITE if size >= 11 else SOFT, fontsize=size, fontfamily="serif")

    save(fig, "formalism_board")


def fig_address_construction() -> None:
    """Matching construction for G_2(K) — full definition board."""
    fig, ax = _paper_page(12.5)
    _body(ax, 0.5, 0.985, "II.  Matching construction  ·  address family", size=13.5, color=WHITE, ha="center", weight="bold")
    _body(ax, 0.5, 0.955, r"for every $K\geq 2$:  $D_2^{\mathrm{ad}}=1$,  $D_2^{\mathrm{na}}=1/K$", size=10, color=MUTED, ha="center", style="italic")
    ax.plot([0, 1], [0.935, 0.935], color=DIM, lw=0.8, transform=ax.transAxes, clip_on=False)

    eqs = [
        (0.88, r"$W_K=\{(i,x): i\in\{1,\ldots,K\},\ x\in\{0,1\}^K\}$"),
        (0.78, r"$P(i,x)=\frac{1}{K\,2^{K-1}}\,1_{x_i=0},\quad Q(i,x)=\frac{1}{K\,2^{K-1}}\,1_{x_i=1}$"),
        (0.68, r"$g(i,x)=i,\quad b_j(i,x)=x_j\quad(j=1,\ldots,K)$"),
        (0.58, r"Adaptive: ask $g$; if $g=i$ ask $b_i$.  Supports of transcript laws disjoint $\Rightarrow D_2^{\mathrm{ad}}=1$."),
        (0.48, r"Nonadaptive pairs: $(g,b_j)$ or $(b_j,b_l)$ each give $\mathrm{TV}=1/K$."),
        (0.38, r"Signed law for $(b_j,b_l)$: $\mu_{jl}(0,0)=\frac{1}{K},\ \mu_{jl}(1,1)=-\frac{1}{K},\ \mu_{jl}(0,1)=\mu_{jl}(1,0)=0$"),
        (0.28, r"Hence $D_2^{\mathrm{na}}=1/K$  and  $G_2(K)=1-1/K$ is attained."),
        (0.16, r"$K=2$: binary queries, four active worlds, gap $=1/2$  (butterfly geometry)."),
        (0.06, "Proof package: research/m5/SEED_THEOREMS.md  ·  certificates: m5_exact.py", 9.0),
    ]
    for item in eqs:
        y, text = item[0], item[1]
        size = item[2] if len(item) > 2 else 11.0
        color = MUTED if size < 10 else WHITE
        ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="center", color=color, fontsize=size, fontfamily="serif")

    save(fig, "address_construction")


def fig_butterfly_board() -> None:
    """Four-world uniqueness table."""
    fig, ax = _paper_page(11.5)
    _body(ax, 0.5, 0.98, "III.  Support-minimal binary extremizer", size=13.5, color=WHITE, ha="center", weight="bold")
    _body(ax, 0.5, 0.95, r"unique up to symmetry when $r=4$, binary OPEN queries, $D_2^{\mathrm{ad}}=1$, $D_2^{\mathrm{na}}\leq 1/2$", size=9, color=MUTED, ha="center", style="italic")
    ax.plot([0, 1], [0.93, 0.93], color=DIM, lw=0.8, transform=ax.transAxes, clip_on=False)

    # table header
    headers = ["world", "P", "Q", "g", "l", "r"]
    rows = [
        ["A", "1/2", "0", "0", "0", "0"],
        ["B", "0", "1/2", "0", "1", "0"],
        ["C", "1/2", "0", "1", "0", "1"],
        ["D", "0", "1/2", "1", "0", "0"],
    ]
    xs = [0.08, 0.28, 0.42, 0.56, 0.70, 0.84]
    y0 = 0.86
    for x, h in zip(xs, headers):
        ax.text(x, y0, h, transform=ax.transAxes, ha="center", color=GOLD, fontsize=11, fontfamily="serif")
    ax.plot([0.05, 0.95], [0.83, 0.83], color=DIM, lw=0.7, transform=ax.transAxes, clip_on=False)
    for i, row in enumerate(rows):
        y = 0.76 - i * 0.08
        for x, cell in zip(xs, row):
            ax.text(x, y, cell, transform=ax.transAxes, ha="center", color=WHITE, fontsize=12, fontfamily="serif")

    notes = [
        (0.40, r"Root $g$ splits $\{A,B\}$ vs $\{C,D\}$; continuations $l,r$ separate within-branch atoms."),
        (0.32, r"Balance forces $p=q=\frac{1}{2}$ on each root branch (else some fixed pair exceeds $1/2$)."),
        (0.24, r"Off-branch constants of $l,r$ must cross-collide; same-sign collision $\Rightarrow D^{\mathrm{na}}=1$."),
        (0.16, r"Symmetries: world relabel, $P\leftrightarrow Q$, branch swap, output complements, query rename."),
        (0.06, "Thm 7.1 · research/m5/SEED_THEOREMS.md  ·  simultaneously support-minimal and gap-maximal", 9.0),
    ]
    for item in notes:
        y, text = item[0], item[1]
        size = item[2] if len(item) > 2 else 10.0
        ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="center", color=SOFT if size >= 10 else MUTED, fontsize=size, fontfamily="serif")

    save(fig, "butterfly_board")


def fig_stability_board() -> None:
    """First stability / gain-sensitive support bound."""
    fig, ax = _paper_page(11.0)
    _body(ax, 0.5, 0.975, "IV.  Stability and gain-sensitive support", size=13.5, color=WHITE, ha="center", weight="bold")
    _body(ax, 0.5, 0.945, "near-extremal policies are forced to balance and localize", size=9.2, color=MUTED, ha="center", style="italic")
    ax.plot([0, 1], [0.925, 0.925], color=DIM, lw=0.8, transform=ax.transAxes, clip_on=False)

    block = [
        (0.87, r"Binary root, depth two: $V=v_0+v_1$,  $N=D_2^{\mathrm{na}}$.  Assume $N\leq V/2+\varepsilon$."),
        (0.78, r"Then $|v_0-v_1|\leq 2\varepsilon$  and off-branch leakage $e_{1-b}^{(b)}\leq 2\varepsilon$."),
        (0.68, r"Gain form: $b_i=\frac{1}{2}|\mu(C_i)|$,  $g_i=v_i-b_i\geq 0$,  $m=\#\{i:g_i>0\}$."),
        (0.58, r"$D_2^{\mathrm{na}}\geq V_0+\max_i g_i \geq V_0+\frac{D_2(\pi)-V_0}{m},\quad V_0=\sum_i b_i$"),
        (0.48, r"Each positive-gain cell holds both signs $\Rightarrow m\leq\min\{K,\lfloor r/2\rfloor\}$."),
        (0.36, r"Open extremal curve:"),
        (0.28, r"$G_2(K,r)=\sup\{D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}:\ \mathrm{arity}\leq K,\ |S_\mu|\leq r\}$"),
        (0.18, r"Known: $G_2(K,r)=0$ for $r\leq 3$;  $G_2(2,4)=1/2$;  $G_2(K,\infty)=1-1/K$."),
        (0.08, "Full metric stability and matching constructions for every $(K,r)$: open.", 9.2),
    ]
    for item in block:
        y, text = item[0], item[1]
        size = item[2] if len(item) > 2 else 11.0
        if "G_2(K,r)" in text:
            ax.add_patch(
                FancyBboxPatch(
                    (0.05, y - 0.03),
                    0.90,
                    0.055,
                    boxstyle="square,pad=0",
                    facecolor=VOID,
                    edgecolor=SOFT,
                    linewidth=1.0,
                    transform=ax.transAxes,
                )
            )
        ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="center", color=WHITE, fontsize=size, fontfamily="serif")

    save(fig, "stability_board")


def fig_habitat_closed_forms() -> None:
    """Dense closed-form wall for k-pair and parity."""
    fig, ax = _paper_page(12.0)
    _body(ax, 0.5, 0.98, "V.  Habitat closed forms  (application geometry)", size=13.2, color=WHITE, ha="center", weight="bold")
    _body(ax, 0.5, 0.95, r"not the sharp universal envelope — filesystem-shaped query structure", size=9, color=MUTED, ha="center", style="italic")
    ax.plot([0, 1], [0.93, 0.93], color=DIM, lw=0.8, transform=ax.transAxes, clip_on=False)

    wall = [
        (0.88, r"$k$-pair: $J\sim\mathrm{Unif}\{1..k\}$; $H_0$ vs $H_1$ differ on bit$_J$; off-branch $\to\mathrm{na}$"),
        (0.80, r"$D_B^{\mathrm{ad}}=1_{B\geq 2}+\frac{1}{k}1_{B=1},\quad D_B^{\mathrm{na}}=\frac{\min(B,k)}{k}$"),
        (0.71, r"$\mathrm{Gap}_B(k)=1-\frac{\min(B,k)}{k}\to 1$ as $k\to\infty$  ($\forall B\geq 2$)"),
        (0.62, r"Myopic local-first: ratio $\mathrm{OPT}/\mathrm{greedy}=k/2\to\infty$"),
        (0.53, r"Capacity: $\forall\varepsilon<1$, no $k$ with $D_2^{\mathrm{ad}}(k)\leq\varepsilon$  (adaptive capacity 0)"),
        (0.43, r"Parity $m$-bit: local marginals match; branch parity differs"),
        (0.34, r"$B^*_{\mathrm{ad}}=1+m,\quad B^*_{\mathrm{na}}=k\cdot m,\quad \frac{B^*_{\mathrm{na}}}{B^*_{\mathrm{ad}}}=\frac{km}{m+1}\to\infty$"),
        (0.24, r"Query complexity (const TV): nonadaptive $\Omega(k)$ vs adaptive $O(1)$"),
        (0.14, r"Nesting: $k$-pair $\equiv$ parity at $m=1$"),
        (0.05, "Product scar: static smell is nonadaptive; gate-before-local is doctrine, not vibes.", 9.0),
    ]
    for item in wall:
        y, text = item[0], item[1]
        size = item[2] if len(item) > 2 else 11.0
        ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="center", color=WHITE if size >= 10 else MUTED, fontsize=size, fontfamily="serif")

    save(fig, "habitat_forms")


def fig_support_curve() -> None:
    """Known points / envelope sketch for G_2(K,r)."""
    fig, ax = _fig(10.6, 6.0)
    style_axes(ax, r"Support-constrained gap envelope (partial)", r"active support size  $r$", r"upper bound on $G_2$")

    r = np.arange(2, 33)
    # flattening: r <= 3 => 0 at B=2
    flat = np.where(r <= 3, 0.0, np.nan)
    # trivial: gap <= 1
    # root-arity independent of r: G <= 1-1/K for each K
    for K, c, ls in [(2, WHITE, "-"), (3, GOLD, "-"), (4, SOFT, "--"), (8, MUTED, ":")]:
        ub = np.where(r <= 3, 0.0, 1.0 - 1.0 / K)
        # gain bound m <= floor(r/2) softens slightly for small r vs large K
        mcap = np.minimum(K, np.floor(r / 2.0))
        # crude envelope from gain averaging: gap <= 1 - 1/m when ad=1 possible
        soft = np.where(r <= 3, 0.0, 1.0 - 1.0 / np.maximum(mcap, 1))
        env = np.minimum(ub, soft)
        ax.plot(r, env, color=c, lw=2.0 if K <= 3 else 1.5, linestyle=ls, label=rf"$K={K}$ envelope sketch", zorder=5)

    ax.scatter([4], [0.5], s=70, color=GOLD, edgecolors=VOID, linewidths=0.8, zorder=10)
    ax.annotate(
        r"butterfly $(K{=}2,r{=}4)$" + "\n" + r"$G=1/2$ exact",
        xy=(4, 0.5),
        xytext=(10, 0.22),
        fontsize=9,
        color=SOFT,
        fontfamily="serif",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9),
    )
    ax.axhline(0, color=DIM, lw=0.7)
    ax.set_xlim(2, 32)
    ax.set_ylim(-0.05, 1.08)
    legend(ax, loc="lower right")
    callout(ax, 18, 0.72, "exact G₂(K,r) open\nfor most (K,r)")
    fig.tight_layout()
    save(fig, "support_curve")


def fig_deep_equation_wall() -> None:
    """Single intimidating multi-column wall of identities."""
    fig = plt.figure(figsize=(12.5, 8.2), dpi=220)
    fig.patch.set_facecolor(VOID)
    ax = fig.add_axes([0.04, 0.04, 0.92, 0.92])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(VOID)

    ax.text(0.5, 0.97, "CHARM13  ·  identity wall", ha="center", color=WHITE, fontsize=16, fontfamily="serif", transform=ax.transAxes)
    ax.text(0.5, 0.935, "finite OPEN model  ·  all displayed identities proved or certified in-repo", ha="center", color=MUTED, fontsize=9, fontstyle="italic", fontfamily="serif", transform=ax.transAxes)
    ax.plot([0.02, 0.98], [0.91, 0.91], color=DIM, lw=0.8, transform=ax.transAxes)

    left = [
        r"$\mu=P-Q$",
        r"$V_\mu(\Pi)=\frac{1}{2}\sum|\mu(C)|$",
        r"$D=1-2R$",
        r"$r\leq B+1\Rightarrow D^{ad}=D^{na}$",
        r"$D_2^{ad}\leq K\,D_2^{na}$",
        r"$G_2(K)=1-1/K$",
        r"$G_2(2)=\frac{1}{2}$",
    ]
    mid = [
        r"$D_B^{ad}\in\{0,1/k,1\}$",
        r"$D_B^{na}=\min(B,k)/k$",
        r"$\mathrm{Gap}_B\to 1$",
        r"$\mathrm{OPT}/\mathrm{greedy}=k/2$",
        r"$B^*_{ad}=1+m$",
        r"$B^*_{na}=km$",
        r"$\mathrm{Cap}_{ad}(\varepsilon<1)=0$",
    ]
    right = [
        r"$S=1-\prod(1-w_i)$",
        r"refuse $=(\exists\mathrm{bad})\vee(S\geq 0.6)$",
        r"$w_{\mathrm{bad}}=0.55$",
        r"$w_{\mathrm{warn}}=0.25$",
        r"$w_{\mathrm{info}}=0.05$",
        r"smell $\in\mathrm{Na}$",
        r"T4: unclaimed",
    ]
    cols = [(0.17, left, "core"), (0.50, mid, "habitat"), (0.83, right, "oracle")]
    for x, col, title in cols:
        ax.text(x, 0.875, title, ha="center", color=GOLD, fontsize=11, fontfamily="serif", transform=ax.transAxes)
        y = 0.80
        for eq in col:
            ax.text(x, y, eq, ha="center", color=WHITE, fontsize=12.5, fontfamily="serif", transform=ax.transAxes)
            y -= 0.095

    ax.plot([0.02, 0.98], [0.10, 0.10], color=DIM, lw=0.8, transform=ax.transAxes)
    ax.text(
        0.5,
        0.05,
        r"catalog: research/THEOREMS.md   ·   proofs: m5/SEED_THEOREMS.md   ·   certificates: m5_exact + ladder",
        ha="center",
        color=MUTED,
        fontsize=8.5,
        fontfamily="serif",
        transform=ax.transAxes,
    )
    fig.savefig(OUT / "equation_wall.png", dpi=220, facecolor=VOID, bbox_inches="tight", pad_inches=0.16)
    fig.savefig(OUT / "equation_wall.svg", facecolor=VOID, bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)


def _register_local_fonts() -> dict[str, str]:
    """Register personal faces from assets/fonts/ if present (gitignored binaries).

    Returns map role -> font family name for matplotlib.
    """
    from matplotlib import font_manager

    font_dir = Path(__file__).resolve().parent / "fonts"
    registry: dict[str, str] = {}
    candidates = {
        "brush": ["Sabarian.ttf", "Sabarian.otf"],
        "tag": ["Mitshuka_PERSONAL_USE_ONLY.otf", "Mitshuka.otf"],
        "display": ["TheMiladiator.ttf"],
    }
    for role, files in candidates.items():
        for fname in files:
            path = font_dir / fname
            if path.is_file():
                try:
                    font_manager.fontManager.addfont(str(path))
                    prop = font_manager.FontProperties(fname=str(path))
                    registry[role] = prop.get_name()
                except Exception:
                    pass
                break
    # system fallbacks (always legal to ship figures rendered with these)
    names = {f.name for f in font_manager.fontManager.ttflist}
    if "brush" not in registry:
        registry["brush"] = next((n for n in ("Ink Free", "Segoe Print") if n in names), "DejaVu Sans")
    if "tag" not in registry:
        registry["tag"] = next((n for n in ("Segoe Print", "Ink Free") if n in names), registry["brush"])
    if "display" not in registry:
        registry["display"] = next((n for n in ("Segoe Script", "Ink Free") if n in names), registry["brush"])
    return registry


def _scrawl(
    ax,
    x,
    y,
    text: str,
    *,
    font: str,
    size: float,
    color=SOFT,
    rot: float = 0.0,
    alpha: float = 1.0,
    ha="center",
    va="center",
):
    """Double-pass ink so it feels written, not typeset."""
    ax.text(
        x + 0.005,
        y - 0.004,
        text,
        ha=ha,
        va=va,
        color=DIM,
        fontsize=size,
        fontfamily=font,
        rotation=rot,
        alpha=0.5 * alpha,
        zorder=6,
    )
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va=va,
        color=color,
        fontsize=size,
        fontfamily=font,
        rotation=rot,
        alpha=alpha,
        zorder=7,
    )


def _snake_head(ax, tip, direction, scale=0.11, color=SOFT, eye=GOLD):
    """Low-poly friendly snake head (inspiration: dual geometric ouroboros plate)."""
    ang = np.arctan2(direction[1], direction[0])
    c, s = np.cos(ang), np.sin(ang)
    # triangle-ish head in local coords
    local = np.array(
        [
            [scale * 1.15, 0.0],
            [-scale * 0.55, scale * 0.55],
            [-scale * 0.25, 0.0],
            [-scale * 0.55, -scale * 0.55],
        ]
    )
    R = np.array([[c, -s], [s, c]])
    pts = (local @ R.T) + np.asarray(tip)
    ax.fill(pts[:, 0], pts[:, 1], facecolor=VOID, edgecolor=color, linewidth=1.35, zorder=9)
    # eye
    eye_local = np.array([scale * 0.25, scale * 0.18])
    ex, ey = eye_local @ R.T + np.asarray(tip)
    ax.add_patch(Circle((ex, ey), scale * 0.12, facecolor=eye, edgecolor=VOID, linewidth=0.4, zorder=10))


def fig_cyclic_gate_ouroboros() -> None:
    """Cyclic gate + dual ouroboros — black/gold plate inspired by user refs.

    Geometry from the dual-snake circle-of-fifths plates; scrawl from local personal
    fonts when present (not redistributed). Pedagogical analogue only.
    """
    rng = np.random.default_rng(21)
    faces = _register_local_fonts()
    brush, tag, display = faces["brush"], faces["tag"], faces["display"]

    K = 12
    fifths = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
    rim_scraps = [
        "g=i",
        "b_i",
        "1/K",
        "TV=1",
        "B=2",
        "OPEN",
        "ad",
        "na",
        "G2",
        "flat",
        "spoke",
        "pair",
    ]

    fig = plt.figure(figsize=(11.0, 11.2), dpi=220)
    fig.patch.set_facecolor(VOID)
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.90])
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.60, 1.45)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(VOID)

    # Title — display brush, a little crooked
    _scrawl(ax, 0, 1.32, "cyclic gate", font=display, size=22, color=WHITE, rot=rng.uniform(-2, 2))
    _scrawl(
        ax,
        0,
        1.18,
        "address construction  ·  K-wheel  ·  dual ouroboros",
        font=tag,
        size=11,
        color=MUTED,
        rot=rng.uniform(-1.2, 1.2),
    )

    # --- dual ouroboros body (two arcs, heads top & bottom) ---
    R_snake = 1.18
    th = np.linspace(0, 2 * np.pi, 400)
    # slight scallop like the faceted plate
    scallop = 1.0 + 0.035 * np.sin(6 * th)
    sx = R_snake * scallop * np.cos(th)
    sy = R_snake * scallop * np.sin(th)
    ax.plot(sx, sy, color=SOFT, lw=2.4, solid_capstyle="round", zorder=4)
    # gold braid highlight
    ax.plot(
        (R_snake * 0.97) * scallop * np.cos(th),
        (R_snake * 0.97) * scallop * np.sin(th),
        color=GOLD,
        lw=1.1,
        alpha=0.85,
        zorder=5,
    )
    # heads at top (pi/2) and bottom (-pi/2)
    for ang, dsign in ((np.pi / 2, 1.0), (-np.pi / 2, -1.0)):
        tip = np.array([R_snake * np.cos(ang), R_snake * np.sin(ang)])
        # tangent direction for head orientation (clockwise-ish bite)
        tang = np.array([-np.sin(ang), np.cos(ang)]) * dsign
        _snake_head(ax, tip, tang, scale=0.13, color=SOFT, eye=GOLD)

    # outer formula band (etched rim energy from refs)
    R_band = 1.02
    for j, scrap in enumerate(rim_scraps):
        a = np.pi / 2 - 2 * np.pi * (j + 0.5) / K
        x, y = R_band * 1.28 * np.cos(a), R_band * 1.28 * np.sin(a)
        rot = np.degrees(a) - 90
        _scrawl(ax, x, y, scrap, font=tag, size=8.2, color=MUTED, rot=rot * 0.35 + rng.uniform(-6, 6), alpha=0.92)

    # --- inner gold radial wheel (K=12) ---
    R_outer = 0.88
    R_inner = 0.22
    # rings
    ax.add_patch(Circle((0, 0), R_outer, facecolor=VOID, edgecolor=GOLD, linewidth=2.6, zorder=3))
    ax.add_patch(Circle((0, 0), R_outer * 0.93, facecolor=VOID, edgecolor=GOLD_DEEP, linewidth=1.0, zorder=3))
    ax.add_patch(Circle((0, 0), R_inner, facecolor=VOID, edgecolor=GOLD, linewidth=1.8, zorder=6))

    for j in range(K):
        a0 = np.pi / 2 - 2 * np.pi * j / K
        a1 = np.pi / 2 - 2 * np.pi * (j + 1) / K
        # spoke
        ax.plot(
            [R_inner * 1.05 * np.cos(a0), R_outer * 0.98 * np.cos(a0)],
            [R_inner * 1.05 * np.sin(a0), R_outer * 0.98 * np.sin(a0)],
            color=GOLD,
            lw=1.35,
            solid_capstyle="round",
            zorder=4,
        )
        # fifths label mid-segment
        am = (a0 + a1) / 2
        rl = 0.58
        _scrawl(
            ax,
            rl * np.cos(am),
            rl * np.sin(am),
            fifths[j],
            font=brush,
            size=13,
            color=WHITE,
            rot=np.degrees(am) - 90,
        )
        # tiny index
        _scrawl(
            ax,
            0.78 * np.cos(am),
            0.78 * np.sin(am),
            str(j + 1),
            font=tag,
            size=7,
            color=GOLD,
            rot=0,
            alpha=0.85,
        )

    # center hub — gate then bit
    _scrawl(ax, 0, 0.05, "g", font=display, size=18, color=WHITE, rot=-2)
    _scrawl(ax, 0, -0.10, "b_i", font=brush, size=12, color=GOLD, rot=3)

    # margin essays — wacky, not creepy
    essays = [
        (-1.42, 0.40, "ask the wheel\nfirst", brush, -7),
        (1.38, 0.25, "two pins\nmiss the pie", tag, 6),
        (-1.35, -0.55, "adaptive:\none spoke", brush, 4),
        (1.32, -0.65, "bounds meet:\ntail in mouth", tag, -5),
    ]
    for x, y, t, fnt, rot in essays:
        _scrawl(ax, x, y, t, font=fnt, size=10, color=SOFT, rot=rot)

    # sober footer
    ax.text(
        0,
        -1.42,
        r"$G_2(K)=1-1/K$   ·   matching construction closes the bound   ·   analogue only",
        ha="center",
        color=GOLD,
        fontsize=9.2,
        fontfamily="serif",
    )
    ax.text(
        0,
        -1.52,
        "personal faces used locally if present · binaries not shipped",
        ha="center",
        color=DIM,
        fontsize=7.5,
        fontfamily="serif",
        fontstyle="italic",
    )

    fig.savefig(OUT / "cyclic_gate_ouroboros.png", dpi=220, facecolor=VOID, bbox_inches="tight", pad_inches=0.16)
    fig.savefig(OUT / "cyclic_gate_ouroboros.svg", facecolor=VOID, bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)


def fig_ouroboros_gap() -> None:
    """Ouroboros as G2(K)→1: the gap curve closing toward unity."""
    fig, ax = _fig(10.2, 5.8)
    style_axes(
        ax,
        r"Ouroboros of the gap:  $G_2(K)=1-1/K$ eats toward $1$",
        r"arity  $K$",
        r"$G_2(K)$",
    )
    K = np.linspace(2, 48, 400)
    gap = 1.0 - 1.0 / K
    ax.fill_between(K, 0, gap, color=WHITE, alpha=0.06, zorder=1)
    ax.plot(K, gap, color=WHITE, lw=2.2, zorder=5)
    ax.axhline(1.0, color=DIM, lw=0.8, linestyle=":", zorder=2)
    # bite markers
    for k, lab in [(2, r"$K{=}2$"), (12, r"$K{=}12$"), (48, r"$K\to\infty$")]:
        g = 1 - 1 / k
        ax.scatter([k], [g], s=42, color=GOLD, edgecolors=VOID, linewidths=0.7, zorder=8)
    ax.annotate(
        "tail in mouth:\nconstruction meets bound",
        xy=(36, 1 - 1 / 36),
        xytext=(18, 0.35),
        fontsize=9.5,
        color=SOFT,
        fontfamily="serif",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9),
        bbox=dict(boxstyle="square,pad=0.35", facecolor=VOID, edgecolor=SOFT, linewidth=0.9),
    )
    callout(ax, 8, 0.78, r"$G_2\to 1$")
    fig.tight_layout()
    save(fig, "ouroboros_gap")


def main() -> None:
    fig_wtf_hero()
    fig_adaptivity_gap()
    fig_gap_all_B()
    fig_budget_separation()
    fig_capacity_zero()
    fig_greedy_ratio()
    fig_support_curve()
    fig_score_dual_gate()
    fig_formula_sheet()
    fig_loop_diagram()
    fig_theorem_board()
    fig_formalism_board()
    fig_address_construction()
    fig_butterfly_board()
    fig_stability_board()
    fig_habitat_closed_forms()
    fig_deep_equation_wall()
    fig_cyclic_gate_ouroboros()
    fig_ouroboros_gap()
    print(f"wrote figures → {OUT}")
    for p in sorted(OUT.glob("*.png")):
        print(" ", p.name)


if __name__ == "__main__":
    main()

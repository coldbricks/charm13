"""Render CHARM13 research figures — pure black academic typesetting.

  python assets/render_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
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
    """Black academic formula board — paper-slide energy."""
    fig, ax = _paper_page(10.5)

    _body(ax, 0.5, 0.97, "CHARM13  ·  closed forms", size=15, color=WHITE, ha="center", weight="bold")
    _body(ax, 0.5, 0.935, "finite-model ladder  ·  proved in the frozen OPEN model", size=9.5, color=MUTED, ha="center", style="italic")
    ax.plot([0.0, 1.0], [0.91, 0.91], color=DIM, lw=0.8, transform=ax.transAxes, clip_on=False)

    blocks = [
        (0.84, r"$G_2(K)=1-1/K$", "sharp budget-2 adaptivity gap under active arity at most K"),
        (0.68, r"$D_2^{ad}=1,\ \ D_2^{na}=1/K$", "matching address-function construction"),
        (0.52, r"$r \leq B+1 \Rightarrow D_B^{ad}=D_B^{na}$", "flattening: small active support kills the OPEN gap"),
        (0.36, r"$D_B^{na}=\min(B,k)/k$", "k-pair habitat closed form (not the sharp envelope)"),
        (0.20, r"$B^*_{ad}=1+m,\ \ B^*_{na}=k\cdot m$", "parity perfect-separation budgets"),
        (0.04, "refused = (any bad)  or  (S >= 0.6)", "product dual gate — S is a severity monoid, not a probability"),
    ]
    for y, eq, cap in blocks:
        _eq(ax, y + 0.04, eq, size=14.5, boxed=(eq.startswith(r"$G_2")))
        _body(ax, 0.5, y - 0.01, cap, size=9.5, color=MUTED, ha="center", style="italic")

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
    fig, ax = _paper_page(12.0)

    ax.text(
        0.0,
        0.985,
        "Flattening and the sharp budget-two law",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=WHITE,
        fontsize=14.5,
        fontfamily="serif",
    )
    ax.plot([0, 1], [0.955, 0.955], color=DIM, lw=0.8, transform=ax.transAxes)

    # (y, text, kind)  kind in {body, eq, box}
    prose = [
        (0.93, "Let r be the number of worlds with nonzero signed mass,", "body"),
        (0.885, r"$r = |\{w : P(w) \neq Q(w)\}|.$", "eq"),
        (0.84, "For globally addressable unit-cost queries, if", "body"),
        (0.795, r"$r \leq B+1,$", "eq"),
        (0.76, "then", "body"),
        (0.715, r"$D_B^{ad} = D_B^{na}.$", "eq"),
        (
            0.66,
            "Take any adaptive policy tree, discard branches carrying no signed mass, and contract\n"
            "nodes with only one active child. A reduced tree on r active worlds has at most r-1\n"
            "internal query occurrences. Ask those queries nonadaptively: the joint partition refines\n"
            "the adaptive leaf partition on active worlds. Refinement can only increase total variation.",
            "body",
        ),
        (
            0.545,
            "Hence a budget-two adaptivity gap needs at least four active worlds. The M4 witness is\n"
            "support-minimal in the OPEN model.",
            "body",
        ),
        (
            0.475,
            "Now suppose every query has at most K nonempty active outcomes. For every budget-two\n"
            "adaptive policy,",
            "body",
        ),
        (0.41, r"$D_2^{ad} \leq K\, D_2^{na}.$", "eq"),
        (
            0.355,
            "Split adaptive value into root-branch contributions V = v1 + ... + vk. Each fixed pair\n"
            "(root, continuation on branch i) preserves vi, so Dna >= max vi >= V/k.",
            "body",
        ),
        (0.285, "Consequently", "body"),
        (0.24, r"$D_2^{ad} - D_2^{na} \leq 1 - 1/K.$", "eq"),
        (
            0.175,
            "The bound is exactly sharp: there is a construction with Dad = 1 and Dna = 1/K.\n"
            "The exact worst-case budget-two additive gap is",
            "body",
        ),
        (0.08, r"$G_2(K) = 1 - 1/K.$", "box"),
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
                fontsize=13.5,
                fontfamily="serif",
            )
        elif kind == "box":
            ax.add_patch(
                FancyBboxPatch(
                    (0.26, y - 0.035),
                    0.48,
                    0.065,
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
                fontsize=10.0,
                fontfamily="serif",
                linespacing=1.55,
            )

    save(fig, "theorem_board")


def fig_wtf_hero() -> None:
    """Landing hero: black paper + clean G2 curve."""
    fig = plt.figure(figsize=(12.5, 7.0), dpi=220)
    fig.patch.set_facecolor(VOID)

    ax_l = fig.add_axes([0.055, 0.10, 0.48, 0.80])
    ax_r = fig.add_axes([0.57, 0.18, 0.38, 0.62])
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 1)
    ax_l.axis("off")
    ax_l.set_facecolor(VOID)

    ax_l.text(0.0, 0.94, "CHARM13", color=WHITE, fontsize=34, fontfamily="serif")
    ax_l.text(0.0, 0.85, "wait — what is this", color=MUTED, fontsize=15, fontstyle="italic", fontfamily="serif")

    ax_l.text(
        0.0,
        0.70,
        "A camouflage factory for encrypted volumes that builds\n"
        "on-disk cover stories — then runs a detector allowed to\n"
        "refuse its own lies.\n\n"
        "Finite-model math: a curious adaptive inspector can beat\n"
        "a fixed checklist of the same look-budget — arbitrarily hard.",
        color=SOFT,
        fontsize=10.8,
        linespacing=1.55,
        fontfamily="serif",
        verticalalignment="top",
    )

    ax_l.plot([0.0, 0.92], [0.40, 0.40], color=DIM, lw=0.9)

    bullets = [
        ("01", "Not a new cipher — story is the product"),
        ("02", "Score is a severity monoid, not P(fake)"),
        ("03", "Static smell ≠ adaptive T1 (gap can hit 1)"),
        ("04", "Refuse if blown — self-falsification"),
        ("05", "T4: no claim. Detection framing only"),
    ]
    y = 0.34
    for num, text in bullets:
        ax_l.text(0.0, y, num, color=GOLD, fontsize=9.5, fontfamily="monospace", va="center")
        ax_l.text(0.09, y, text, color=SOFT, fontsize=10.2, fontfamily="serif", va="center")
        y -= 0.052

    ax_l.text(
        0.0,
        0.02,
        "Boiler Up  ·  Purdue black & old gold  ·  measure twice, cut once",
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

    ax_r.set_xlim(2, 48)
    ax_r.set_ylim(0, 1.08)
    ax_r.set_xlabel(r"query arity  $K$", color=MUTED, fontsize=9.5, fontfamily="serif")
    ax_r.set_ylabel(r"$G_2(K)$", color=MUTED, fontsize=9.5, fontfamily="serif")
    ax_r.tick_params(colors=MUTED, labelsize=8)
    ax_r.set_title(r"$G_2(K)=1-1/K\ \rightarrow\ 1$", color=WHITE, fontsize=12, pad=10, fontfamily="serif")
    ax_r.grid(True, color=RULE, linewidth=0.6)
    ax_r.set_axisbelow(True)
    ax_r.annotate(
        "checklist loses\nas habitats branch",
        xy=(32, 0.93),
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
    fig_theorem_board()
    print(f"wrote figures → {OUT}")
    for p in sorted(OUT.glob("*.png")):
        print(" ", p.name)


if __name__ == "__main__":
    main()

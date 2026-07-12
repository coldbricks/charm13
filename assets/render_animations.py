"""Animated GIFs for CHARM13 research figures (Purdue black & gold)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

BLACK = "#0A0A0A"
GOLD = "#CFB991"
GOLD_DEEP = "#8E6F3E"
CREAM = "#F7F1E5"
GRAY = "#8A8070"

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def _style(ax, title, xlabel, ylabel):
    ax.set_facecolor(CREAM)
    ax.set_title(title, color=BLACK, fontsize=12, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, color=GRAY, fontsize=10)
    ax.set_ylabel(ylabel, color=GRAY, fontsize=10)
    ax.tick_params(colors=GRAY, labelsize=8)
    for s in ax.spines.values():
        s.set_color(GOLD_DEEP)
    ax.grid(True, color=GOLD, alpha=0.35, linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)


def anim_gap_growth() -> None:
    """Gap curve draws itself as k increases."""
    k_full = np.linspace(2, 48, 80)
    fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=110)
    fig.patch.set_facecolor(BLACK)

    (line_ad,) = ax.plot([], [], color=BLACK, lw=2.4, label="adaptive D = 1")
    (line_na,) = ax.plot([], [], color=GOLD_DEEP, lw=2.4, label="nonadaptive D = 2/k")
    fill = None

    def init():
        _style(ax, "Adaptivity gap growing with branching k  (B = 2)", "k", "advantage")
        ax.set_xlim(2, 48)
        ax.set_ylim(-0.02, 1.08)
        ax.legend(loc="center right", frameon=True, facecolor="white", edgecolor=GOLD_DEEP, fontsize=9)
        ax.axhline(1, color=BLACK, alpha=0.25, lw=0.8)
        return line_ad, line_na

    def update(frame):
        nonlocal fill
        k = k_full[: frame + 2]
        d_ad = np.ones_like(k)
        d_na = 2.0 / k
        line_ad.set_data(k, d_ad)
        line_na.set_data(k, d_na)
        if fill is not None:
            fill.remove()
        fill = ax.fill_between(k, d_na, d_ad, color=GOLD, alpha=0.4)
        return line_ad, line_na, fill

    ani = animation.FuncAnimation(
        fig, update, frames=len(k_full) - 1, init_func=init, blit=False, interval=40
    )
    path = OUT / "anim_gap_growth.gif"
    ani.save(path, writer=animation.PillowWriter(fps=22))
    plt.close(fig)
    print("wrote", path)


def anim_gap_approaches_one() -> None:
    """Single curve Gap(k) climbing toward 1 with a moving marker."""
    k = np.linspace(2, 60, 100)
    gap = 1 - 2 / k
    fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=110)
    fig.patch.set_facecolor(BLACK)
    _style(ax, "Gap_2(k)  →  1", "branching k", "Gap")
    ax.set_xlim(2, 60)
    ax.set_ylim(0, 1.05)
    ax.plot(k, gap, color=GOLD_DEEP, lw=1.2, alpha=0.35)
    (trail,) = ax.plot([], [], color=BLACK, lw=2.6)
    (dot,) = ax.plot([], [], "o", color=GOLD, ms=9, markeredgecolor=BLACK, markeredgewidth=1)
    txt = ax.text(0.98, 0.12, "", transform=ax.transAxes, ha="right", color=BLACK,
                  fontsize=10, bbox=dict(boxstyle="round,pad=0.35", facecolor=GOLD, edgecolor=BLACK))

    def update(i):
        trail.set_data(k[: i + 1], gap[: i + 1])
        dot.set_data([k[i]], [gap[i]])
        txt.set_text(f"k = {k[i]:.0f}   Gap = {gap[i]:.3f}")
        return trail, dot, txt

    ani = animation.FuncAnimation(fig, update, frames=len(k), interval=35, blit=False)
    path = OUT / "anim_gap_to_one.gif"
    ani.save(path, writer=animation.PillowWriter(fps=24))
    plt.close(fig)
    print("wrote", path)


def anim_budget_race() -> None:
    """Bars grow: B_ad* flat, B_na* races up with k."""
    ks = np.arange(1, 16)
    m = 2
    b_ad = 1 + m
    b_na = ks * m
    fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=110)
    fig.patch.set_facecolor(BLACK)
    _style(ax, "Budget race: adaptive vs nonadaptive (parity m=2)", "k", "B* for perfect TV")
    ax.set_xlim(0.5, 15.5)
    ax.set_ylim(0, max(b_na) + 2)
    bars_na = ax.bar(ks, np.zeros_like(ks), color=BLACK, width=0.45, label="nonadaptive B* = k·m")
    bars_ad = ax.bar(ks + 0.0, np.zeros_like(ks), color=GOLD_DEEP, width=0.45, label="adaptive B* = 1+m", alpha=0.0)
    # use lines instead for clearer animation
    ax.clear()
    _style(ax, "Budget race: adaptive vs nonadaptive (parity m=2)", "branches k", "B* for TV = 1")
    ax.set_xlim(0.5, 15.5)
    ax.set_ylim(0, max(b_na) + 3)
    (ln_ad,) = ax.plot([], [], color=GOLD_DEEP, lw=2.8, marker="o", ms=5, label="adaptive B* = 1+m")
    (ln_na,) = ax.plot([], [], color=BLACK, lw=2.8, marker="s", ms=5, label="nonadaptive B* = k·m")
    fill_poly = None
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor=GOLD_DEEP, fontsize=9)

    def update(i):
        nonlocal fill_poly
        x = ks[: i + 1]
        ln_ad.set_data(x, np.full_like(x, b_ad, dtype=float))
        ln_na.set_data(x, b_na[: i + 1])
        if fill_poly is not None:
            fill_poly.remove()
        fill_poly = ax.fill_between(x, b_ad, b_na[: i + 1], color=GOLD, alpha=0.35)
        return ln_ad, ln_na, fill_poly

    ani = animation.FuncAnimation(fig, update, frames=len(ks), interval=120, blit=False)
    path = OUT / "anim_budget_race.gif"
    ani.save(path, writer=animation.PillowWriter(fps=8))
    plt.close(fig)
    print("wrote", path)


def anim_capacity() -> None:
    """Bars animate: adaptive stuck at 1, nonadaptive drops."""
    k_vals = [2, 4, 8, 16, 32]
    d_na = [2 / k for k in k_vals]
    fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=110)
    fig.patch.set_facecolor(BLACK)
    x = np.arange(len(k_vals))
    w = 0.35

    def update(frame):
        ax.clear()
        _style(ax, "At B=2: adaptive stuck at 1, checklist risk falls", "k", "D2")
        ax.set_ylim(0, 1.2)
        # progressive reveal of groups
        n = min(frame + 1, len(k_vals))
        ax.bar(x[:n] - w / 2, [1] * n, w, color=BLACK, label="adaptive D = 1")
        ax.bar(x[:n] + w / 2, d_na[:n], w, color=GOLD_DEEP, label="nonadaptive D = 2/k")
        ax.set_xticks(x, [str(k) for k in k_vals])
        ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor=GOLD_DEEP, fontsize=9)
        return []

    ani = animation.FuncAnimation(fig, update, frames=len(k_vals) + 2, interval=450, blit=False)
    path = OUT / "anim_capacity_zero.gif"
    ani.save(path, writer=animation.PillowWriter(fps=2))
    plt.close(fig)
    print("wrote", path)


def anim_loop_pulse() -> None:
    """Simple three-node pulse FORGE → SMELL → REFUSE."""
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=110)
    fig.patch.set_facecolor(CREAM)
    nodes = [(0.15, 0.5), (0.5, 0.5), (0.85, 0.5)]
    labels = ["FORGE", "SMELL", "REFUSE"]
    subs = ["construct", "oracle", "dual gate"]

    def update(frame):
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(CREAM)
        ax.set_title("CHARM13 loop", color=BLACK, fontsize=12, fontweight="bold")
        active = frame % 3
        for i, ((x, y), lab, sub) in enumerate(zip(nodes, labels, subs)):
            face = BLACK if i == active else "#1a1a1a"
            edge = GOLD if i == active else GOLD_DEEP
            lw = 2.5 if i == active else 1.2
            from matplotlib.patches import FancyBboxPatch

            ax.add_patch(
                FancyBboxPatch(
                    (x - 0.11, y - 0.18),
                    0.22,
                    0.36,
                    boxstyle="round,pad=0.02,rounding_size=0.03",
                    facecolor=face,
                    edgecolor=edge,
                    linewidth=lw,
                )
            )
            ax.text(x, y + 0.05, lab, ha="center", color=GOLD, fontsize=10, fontweight="bold")
            ax.text(x, y - 0.08, sub, ha="center", color=CREAM, fontsize=8)
        ax.annotate("", xy=(0.37, 0.5), xytext=(0.28, 0.5), arrowprops=dict(arrowstyle="->", color=GOLD_DEEP, lw=2))
        ax.annotate("", xy=(0.72, 0.5), xytext=(0.63, 0.5), arrowprops=dict(arrowstyle="->", color=GOLD_DEEP, lw=2))
        ax.text(0.5, 0.12, "blown → rework → forge again", ha="center", color=GRAY, fontsize=9)
        return []

    ani = animation.FuncAnimation(fig, update, frames=12, interval=280, blit=False)
    path = OUT / "anim_loop.gif"
    ani.save(path, writer=animation.PillowWriter(fps=3))
    plt.close(fig)
    print("wrote", path)


def main() -> None:
    anim_gap_growth()
    anim_gap_approaches_one()
    anim_budget_race()
    anim_capacity()
    anim_loop_pulse()
    print("GIFs ready in", OUT)


if __name__ == "__main__":
    main()

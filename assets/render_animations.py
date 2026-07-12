"""Animated GIFs for CHARM13 — pure black academic style."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
import numpy as np

VOID = "#000000"
WHITE = "#F2F2F2"
SOFT = "#D0D0D0"
MUTED = "#8A8A8A"
DIM = "#3A3A3A"
RULE = "#2A2A2A"
GOLD = "#CFB991"
GOLD_DEEP = "#8E6F3E"

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm"})


def _style(ax, title, xlabel, ylabel):
    ax.set_facecolor(VOID)
    ax.set_title(title, color=WHITE, fontsize=12.5, pad=12, fontfamily="serif")
    ax.set_xlabel(xlabel, color=MUTED, fontsize=10, fontfamily="serif")
    ax.set_ylabel(ylabel, color=MUTED, fontsize=10, fontfamily="serif")
    ax.tick_params(colors=MUTED, labelsize=8)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(DIM)
        ax.spines[s].set_linewidth(1.0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=RULE, linewidth=0.55)
    ax.set_axisbelow(True)


def _legend(ax, **kw):
    defaults = dict(
        frameon=True,
        facecolor=VOID,
        edgecolor=DIM,
        labelcolor=SOFT,
        fontsize=8.5,
        framealpha=1.0,
        fancybox=False,
    )
    defaults.update(kw)
    leg = ax.legend(**defaults)
    for t in leg.get_texts():
        t.set_color(SOFT)
        t.set_fontfamily("serif")
    return leg


def anim_gap_growth() -> None:
    k_full = np.linspace(2, 48, 90)
    fig, ax = plt.subplots(figsize=(9.0, 4.8), dpi=130)
    fig.patch.set_facecolor(VOID)

    (line_ad,) = ax.plot([], [], color=WHITE, lw=2.2, label=r"adaptive $D=1$")
    (line_na,) = ax.plot([], [], color=GOLD, lw=2.0, label=r"sharp nonadaptive $D=1/K$")
    (line_hab,) = ax.plot([], [], color=MUTED, lw=1.4, linestyle=(0, (3, 2.5)), label=r"k-pair $D=2/k$")
    fill = None

    def init():
        _style(ax, r"Adaptivity gap growing with arity  ($B=2$)", r"$K$", "advantage")
        ax.set_xlim(2, 48)
        ax.set_ylim(-0.02, 1.12)
        ax.axhline(1, color=DIM, lw=0.8, linestyle=":")
        _legend(ax, loc="center right")
        return line_ad, line_na, line_hab

    def update(frame):
        nonlocal fill
        k = k_full[: frame + 2]
        d_ad = np.ones_like(k)
        d_na = 1.0 / k
        d_hab = 2.0 / k
        line_ad.set_data(k, d_ad)
        line_na.set_data(k, d_na)
        line_hab.set_data(k, d_hab)
        if fill is not None:
            fill.remove()
        fill = ax.fill_between(k, d_na, d_ad, color=WHITE, alpha=0.07, zorder=1)
        return line_ad, line_na, line_hab, fill

    ani = animation.FuncAnimation(
        fig, update, frames=len(k_full) - 1, init_func=init, blit=False, interval=35
    )
    path = OUT / "anim_gap_growth.gif"
    ani.save(path, writer=animation.PillowWriter(fps=24))
    plt.close(fig)
    print("wrote", path)


def anim_gap_approaches_one() -> None:
    k = np.linspace(2, 60, 110)
    gap = 1.0 - 1.0 / k
    fig, ax = plt.subplots(figsize=(9.0, 4.8), dpi=130)
    fig.patch.set_facecolor(VOID)
    _style(ax, r"$G_2(K)=1-1/K$  →  1", r"query arity  $K$", r"$G_2$")
    ax.set_xlim(2, 60)
    ax.set_ylim(0, 1.08)
    ax.axhline(1, color=DIM, lw=0.8, linestyle=":")
    ax.plot(k, gap, color=DIM, lw=1.1, alpha=0.9)
    (trail,) = ax.plot([], [], color=WHITE, lw=2.3)
    (dot,) = ax.plot([], [], "o", color=GOLD, ms=8, markeredgecolor=VOID, markeredgewidth=0.9)
    txt = ax.text(
        0.97,
        0.12,
        "",
        transform=ax.transAxes,
        ha="right",
        color=WHITE,
        fontsize=10,
        fontfamily="serif",
        bbox=dict(boxstyle="square,pad=0.35", facecolor=VOID, edgecolor=SOFT, linewidth=0.9),
    )
    fill = None

    def update(i):
        nonlocal fill
        if fill is not None:
            fill.remove()
        fill = ax.fill_between(k[: i + 1], 0, gap[: i + 1], color=WHITE, alpha=0.06, zorder=1)
        trail.set_data(k[: i + 1], gap[: i + 1])
        trail.set_zorder(6)
        dot.set_data([k[i]], [gap[i]])
        txt.set_text(f"K = {k[i]:.0f}   G₂ = {gap[i]:.3f}")
        return trail, dot, txt, fill

    ani = animation.FuncAnimation(fig, update, frames=len(k), interval=30, blit=False)
    path = OUT / "anim_gap_to_one.gif"
    ani.save(path, writer=animation.PillowWriter(fps=26))
    plt.close(fig)
    print("wrote", path)


def anim_budget_race() -> None:
    ks = np.arange(1, 18)
    m = 2
    b_ad = 1 + m
    b_na = ks * m
    fig, ax = plt.subplots(figsize=(9.0, 4.8), dpi=130)
    fig.patch.set_facecolor(VOID)
    _style(ax, "Budget race: adaptive vs nonadaptive (parity m=2)", r"branches  $k$", r"$B^\star$ for TV $=1$")
    ax.set_xlim(0.5, 17.5)
    ax.set_ylim(0, max(b_na) + 4)
    (ln_ad,) = ax.plot(
        [],
        [],
        color=GOLD,
        lw=2.0,
        marker="o",
        ms=4.5,
        markerfacecolor=VOID,
        markeredgecolor=GOLD,
        markeredgewidth=1.0,
        label=r"adaptive $B^\star=1+m$",
    )
    (ln_na,) = ax.plot(
        [],
        [],
        color=WHITE,
        lw=2.1,
        marker="s",
        ms=4,
        markerfacecolor=VOID,
        markeredgecolor=WHITE,
        markeredgewidth=0.9,
        label=r"nonadaptive $B^\star=k\cdot m$",
    )
    fill = None
    _legend(ax, loc="upper left")

    def update(i):
        nonlocal fill
        x = ks[: i + 1].astype(float)
        y_ad = np.full_like(x, float(b_ad))
        y_na = b_na[: i + 1].astype(float)
        ln_ad.set_data(x, y_ad)
        ln_na.set_data(x, y_na)
        if fill is not None:
            fill.remove()
        fill = ax.fill_between(x, y_ad, y_na, color=WHITE, alpha=0.06, zorder=1)
        return ln_ad, ln_na, fill

    ani = animation.FuncAnimation(fig, update, frames=len(ks), interval=110, blit=False)
    path = OUT / "anim_budget_race.gif"
    ani.save(path, writer=animation.PillowWriter(fps=9))
    plt.close(fig)
    print("wrote", path)


def anim_capacity() -> None:
    k_vals = [2, 4, 8, 16, 32]
    d_na = [2 / k for k in k_vals]
    fig, ax = plt.subplots(figsize=(9.0, 4.8), dpi=130)
    fig.patch.set_facecolor(VOID)
    x = np.arange(len(k_vals))
    w = 0.32

    def update(frame):
        ax.clear()
        _style(ax, r"At $B=2$: adaptive stuck at 1, checklist risk falls", r"$k$", r"$D_2$")
        ax.set_ylim(0, 1.25)
        ax.axhline(1.0, color=DIM, lw=0.8, linestyle=":")
        n = min(frame + 1, len(k_vals))
        ax.bar(
            x[:n] - w / 2,
            [1] * n,
            w,
            facecolor=VOID,
            edgecolor=WHITE,
            linewidth=1.2,
            label=r"adaptive $D=1$",
        )
        ax.bar(
            x[:n] + w / 2,
            d_na[:n],
            w,
            facecolor=VOID,
            edgecolor=GOLD,
            linewidth=1.2,
            label=r"nonadaptive $D=2/k$",
        )
        ax.bar(x[:n] + w / 2, d_na[:n], w, color=GOLD, alpha=0.22, zorder=0)
        ax.set_xticks(x, [str(k) for k in k_vals])
        _legend(ax, loc="upper right")
        return []

    ani = animation.FuncAnimation(fig, update, frames=len(k_vals) + 2, interval=420, blit=False)
    path = OUT / "anim_capacity_zero.gif"
    ani.save(path, writer=animation.PillowWriter(fps=2))
    plt.close(fig)
    print("wrote", path)


def anim_loop_pulse() -> None:
    fig, ax = plt.subplots(figsize=(9.0, 3.3), dpi=130)
    fig.patch.set_facecolor(VOID)
    nodes = [(0.15, 0.52), (0.5, 0.52), (0.85, 0.52)]
    labels = ["FORGE", "SMELL", "REFUSE"]
    subs = ["construct", "oracle", "dual gate"]

    def update(frame):
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(VOID)
        ax.set_title("CHARM13 loop", color=WHITE, fontsize=12.5, fontfamily="serif")
        active = frame % 3
        ax.plot([0.15, 0.85], [0.16, 0.16], color=DIM, lw=1.1)
        ax.annotate(
            "",
            xy=(0.15, 0.16),
            xytext=(0.20, 0.16),
            arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=1.1, mutation_scale=9),
        )
        ax.text(0.5, 0.06, "blown → rework", ha="center", color=MUTED, fontsize=8.5, fontfamily="serif", style="italic")
        for i, ((x, y), lab, sub) in enumerate(zip(nodes, labels, subs)):
            is_on = i == active
            edge = WHITE if is_on else DIM
            lw = 1.6 if is_on else 1.0
            ax.add_patch(
                FancyBboxPatch(
                    (x - 0.115, y - 0.18),
                    0.23,
                    0.38,
                    boxstyle="square,pad=0.02",
                    facecolor=VOID,
                    edgecolor=edge,
                    linewidth=lw,
                )
            )
            ax.text(
                x,
                y + 0.06,
                lab,
                ha="center",
                color=WHITE if is_on else SOFT,
                fontsize=11,
                fontfamily="serif",
            )
            ax.text(x, y - 0.08, sub, ha="center", color=MUTED if not is_on else SOFT, fontsize=8, fontfamily="serif")
        for x0, x1 in ((0.27, 0.38), (0.62, 0.73)):
            ax.annotate(
                "",
                xy=(x1, 0.52),
                xytext=(x0, 0.52),
                arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=1.4, mutation_scale=10),
            )
        return []

    ani = animation.FuncAnimation(fig, update, frames=12, interval=380, blit=False)
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
    print(f"done → {OUT}")


if __name__ == "__main__":
    main()

"""Animated GIFs for CHARM13 — pure black academic style.

High-framerate 2D trails + a few 3D orbiting surfaces (not everything).
  python assets/render_animations.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
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

# Monochrome + gold ramp for 3D surfaces
_CMAP = LinearSegmentedColormap.from_list(
    "charm_void",
    [VOID, "#1a1a1a", DIM, MUTED, GOLD_DEEP, GOLD, WHITE],
    N=256,
)


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


def _save_gif(ani, path: Path, fps: int = 14) -> None:
    """Default ~14 fps — readable for math trails; override per anim if needed."""
    ani.save(path, writer=animation.PillowWriter(fps=fps))
    print("wrote", path, f"@ {fps}fps")


def _style_3d(ax, title: str) -> None:
    ax.set_facecolor(VOID)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor(DIM)
    ax.yaxis.pane.set_edgecolor(DIM)
    ax.zaxis.pane.set_edgecolor(DIM)
    ax.tick_params(colors=MUTED, labelsize=7, pad=1)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.zaxis.label.set_color(MUTED)
    ax.title.set_color(WHITE)
    ax.set_title(title, fontsize=12, pad=10, fontfamily="serif")
    try:
        ax.set_box_aspect((1.15, 1.0, 0.72))
    except Exception:
        pass


# ---------------------------------------------------------------------------
# 2D — high frame rate
# ---------------------------------------------------------------------------


def anim_gap_growth() -> None:
    k_full = np.linspace(2, 48, 160)
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=140)
    fig.patch.set_facecolor(VOID)

    (line_ad,) = ax.plot([], [], color=WHITE, lw=2.3, label=r"adaptive $D=1$")
    (line_na,) = ax.plot([], [], color=GOLD, lw=2.1, label=r"sharp nonadaptive $D=1/K$")
    (line_hab,) = ax.plot([], [], color=MUTED, lw=1.5, linestyle=(0, (3, 2.5)), label=r"k-pair $D=2/k$")
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
        fill = ax.fill_between(k, d_na, d_ad, color=WHITE, alpha=0.08, zorder=1)
        return line_ad, line_na, line_hab, fill

    ani = animation.FuncAnimation(
        fig, update, frames=len(k_full) - 1, init_func=init, blit=False, interval=1000 / 14
    )
    _save_gif(ani, OUT / "anim_gap_growth.gif", fps=14)
    plt.close(fig)


def anim_gap_approaches_one() -> None:
    k = np.linspace(2, 64, 180)
    gap = 1.0 - 1.0 / k
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=140)
    fig.patch.set_facecolor(VOID)
    _style(ax, r"$G_2(K)=1-1/K$  $\rightarrow$  1", r"query arity  $K$", r"$G_2$")
    ax.set_xlim(2, 64)
    ax.set_ylim(0, 1.08)
    ax.axhline(1, color=DIM, lw=0.8, linestyle=":")
    ax.plot(k, gap, color=DIM, lw=1.0, alpha=0.85)
    (trail,) = ax.plot([], [], color=WHITE, lw=2.4)
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
        fill = ax.fill_between(k[: i + 1], 0, gap[: i + 1], color=WHITE, alpha=0.07, zorder=1)
        trail.set_data(k[: i + 1], gap[: i + 1])
        trail.set_zorder(6)
        dot.set_data([k[i]], [gap[i]])
        txt.set_text(f"K = {k[i]:.0f}   G₂ = {gap[i]:.4f}")
        return trail, dot, txt, fill

    ani = animation.FuncAnimation(fig, update, frames=len(k), interval=1000 / 14, blit=False)
    _save_gif(ani, OUT / "anim_gap_to_one.gif", fps=14)
    plt.close(fig)


def anim_budget_race() -> None:
    # Smooth continuous race, not discrete steps
    ks = np.linspace(1, 20, 120)
    m = 2
    b_ad = np.full_like(ks, 1 + m)
    b_na = ks * m
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=140)
    fig.patch.set_facecolor(VOID)
    _style(ax, r"Budget race  ·  parity $m=2$", r"branches  $k$", r"$B^\star$ for TV $=1$")
    ax.set_xlim(0.8, 20.2)
    ax.set_ylim(0, float(b_na.max()) + 4)
    (ln_ad,) = ax.plot([], [], color=GOLD, lw=2.2, label=r"adaptive $B^\star=1+m$")
    (ln_na,) = ax.plot([], [], color=WHITE, lw=2.2, label=r"nonadaptive $B^\star=k\cdot m$")
    fill = None
    _legend(ax, loc="upper left")
    call = ax.text(
        0.97,
        0.22,
        "",
        transform=ax.transAxes,
        ha="right",
        color=WHITE,
        fontsize=9.5,
        fontfamily="serif",
        bbox=dict(boxstyle="square,pad=0.32", facecolor=VOID, edgecolor=SOFT, linewidth=0.9),
    )

    def update(i):
        nonlocal fill
        x = ks[: i + 1]
        y_ad = b_ad[: i + 1]
        y_na = b_na[: i + 1]
        ln_ad.set_data(x, y_ad)
        ln_na.set_data(x, y_na)
        if fill is not None:
            fill.remove()
        fill = ax.fill_between(x, y_ad, y_na, color=WHITE, alpha=0.07, zorder=1)
        ratio = y_na[-1] / y_ad[-1]
        call.set_text(rf"$k={x[-1]:.1f}$  ·  ratio $={ratio:.1f}$")
        return ln_ad, ln_na, fill, call

    ani = animation.FuncAnimation(fig, update, frames=len(ks), interval=1000 / 14, blit=False)
    _save_gif(ani, OUT / "anim_budget_race.gif", fps=14)
    plt.close(fig)


def anim_capacity() -> None:
    # Morph bars smoothly via height interpolation
    k_vals = np.array([2, 4, 8, 16, 32, 48], dtype=float)
    d_na_final = 2.0 / k_vals
    n_frames = 90
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=140)
    fig.patch.set_facecolor(VOID)
    x = np.arange(len(k_vals))
    w = 0.34

    def update(frame):
        ax.clear()
        _style(ax, r"Capacity zero under adaptive $B=2$", r"branching  $k$", r"$D_2$")
        ax.set_ylim(0, 1.25)
        ax.axhline(1.0, color=DIM, lw=0.8, linestyle=":")
        t = frame / (n_frames - 1)
        # ease-out
        t = 1 - (1 - t) ** 2
        d_ad = np.ones_like(k_vals) * t + (1 - t) * 0.15
        d_na = d_na_final * t + (1 - t) * 0.9
        ax.bar(x - w / 2, d_ad, w, facecolor=VOID, edgecolor=WHITE, linewidth=1.25, label=r"adaptive $D=1$")
        ax.bar(x + w / 2, d_na, w, facecolor=GOLD, alpha=0.28, edgecolor=GOLD, linewidth=1.2, label=r"nonadaptive $D=2/k$")
        ax.set_xticks(x, [str(int(k)) for k in k_vals])
        _legend(ax, loc="upper right")
        return []

    ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=1000 / 12, blit=False)
    _save_gif(ani, OUT / "anim_capacity_zero.gif", fps=12)
    plt.close(fig)


def anim_greedy_blowup() -> None:
    k = np.linspace(3, 52, 160)
    ratio = k / 2.0
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=140)
    fig.patch.set_facecolor(VOID)
    _style(ax, r"Myopic greedy ratio $\to\infty$", r"branching  $k$", r"OPT / greedy $=k/2$")
    ax.set_xlim(3, 52)
    ax.set_ylim(0, float(ratio.max()) * 1.05)
    for r in (2, 5, 10, 15, 20):
        ax.axhline(r, color=RULE, lw=0.65, zorder=2)
    (trail,) = ax.plot([], [], color=WHITE, lw=2.4)
    (dot,) = ax.plot([], [], "o", color=GOLD, ms=7.5, markeredgecolor=VOID, markeredgewidth=0.8)
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
        fill = ax.fill_between(k[: i + 1], 0, ratio[: i + 1], color=WHITE, alpha=0.07, zorder=1)
        trail.set_data(k[: i + 1], ratio[: i + 1])
        trail.set_zorder(6)
        dot.set_data([k[i]], [ratio[i]])
        txt.set_text(f"k = {k[i]:.0f}   ratio = {ratio[i]:.2f}")
        return trail, dot, txt, fill

    ani = animation.FuncAnimation(fig, update, frames=len(k), interval=1000 / 14, blit=False)
    _save_gif(ani, OUT / "anim_greedy_blowup.gif", fps=14)
    plt.close(fig)


def anim_dual_envelope() -> None:
    K = np.linspace(2, 52, 160)
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=140)
    fig.patch.set_facecolor(VOID)
    (ln_sharp,) = ax.plot([], [], color=WHITE, lw=2.3, label=r"sharp $G_2=1-1/K$")
    (ln_hab,) = ax.plot([], [], color=GOLD, lw=2.1, label=r"habitat $1-2/k$")
    fill_s = None
    fill_h = None

    def init():
        _style(ax, r"Two envelopes at $B=2$", r"arity / branching", r"additive gap")
        ax.set_xlim(2, 52)
        ax.set_ylim(-0.02, 1.12)
        ax.axhline(1, color=DIM, lw=0.8, linestyle=":")
        _legend(ax, loc="center right")
        return ln_sharp, ln_hab

    def update(frame):
        nonlocal fill_s, fill_h
        x = K[: frame + 2]
        g_s = 1.0 - 1.0 / x
        g_h = np.maximum(1.0 - 2.0 / x, 0.0)
        ln_sharp.set_data(x, g_s)
        ln_hab.set_data(x, g_h)
        if fill_s is not None:
            fill_s.remove()
        if fill_h is not None:
            fill_h.remove()
        fill_s = ax.fill_between(x, 0, g_s, color=WHITE, alpha=0.05, zorder=1)
        fill_h = ax.fill_between(x, 0, g_h, color=GOLD, alpha=0.10, zorder=2)
        return ln_sharp, ln_hab, fill_s, fill_h

    ani = animation.FuncAnimation(
        fig, update, frames=len(K) - 1, init_func=init, blit=False, interval=1000 / 14
    )
    _save_gif(ani, OUT / "anim_dual_envelope.gif", fps=14)
    plt.close(fig)


def anim_loop_pulse() -> None:
    fig, ax = plt.subplots(figsize=(9.2, 3.4), dpi=140)
    fig.patch.set_facecolor(VOID)
    nodes = [(0.15, 0.52), (0.5, 0.52), (0.85, 0.52)]
    labels = ["FORGE", "SMELL", "REFUSE"]
    subs = ["construct", "oracle", "dual gate"]
    n_frames = 48  # smooth pulse cycle

    def update(frame):
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(VOID)
        ax.set_title("CHARM13 loop", color=WHITE, fontsize=12.5, fontfamily="serif")
        phase = (frame / n_frames) * 3.0
        ax.plot([0.15, 0.85], [0.16, 0.16], color=DIM, lw=1.1)
        ax.annotate(
            "",
            xy=(0.15, 0.16),
            xytext=(0.20, 0.16),
            arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=1.1, mutation_scale=9),
        )
        ax.text(0.5, 0.06, "blown → rework", ha="center", color=MUTED, fontsize=8.5, fontfamily="serif", style="italic")
        for i, ((x, y), lab, sub) in enumerate(zip(nodes, labels, subs)):
            # soft highlight near phase
            dist = min(abs(phase - i), abs(phase - i - 3), abs(phase - i + 3))
            glow = max(0.0, 1.0 - dist * 1.4)
            edge = WHITE if glow > 0.55 else DIM
            lw = 1.0 + 0.9 * glow
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
                color=WHITE if glow > 0.4 else SOFT,
                fontsize=11,
                fontfamily="serif",
            )
            ax.text(x, y - 0.08, sub, ha="center", color=SOFT if glow > 0.4 else MUTED, fontsize=8, fontfamily="serif")
        for x0, x1 in ((0.27, 0.38), (0.62, 0.73)):
            ax.annotate(
                "",
                xy=(x1, 0.52),
                xytext=(x0, 0.52),
                arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=1.4, mutation_scale=10),
            )
        return []

    ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=1000 / 10, blit=False)
    _save_gif(ani, OUT / "anim_loop.gif", fps=10)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3D — selective (the ones that earn the dimension)
# ---------------------------------------------------------------------------


def anim_gap_surface_3d() -> None:
    """Orbiting surface: Gap_B(k) = 1 - min(B,k)/k over (B, k)."""
    B = np.linspace(2, 16, 48)
    k = np.linspace(2, 48, 56)
    BB, KK = np.meshgrid(B, k)
    ZZ = 1.0 - np.minimum(BB, KK) / KK

    fig = plt.figure(figsize=(9.4, 6.4), dpi=130)
    fig.patch.set_facecolor(VOID)
    ax = fig.add_subplot(111, projection="3d")
    _style_3d(ax, r"$\mathrm{Gap}_B(k)=1-\min(B,k)/k$")
    ax.set_xlabel(r"$B$", fontfamily="serif", labelpad=6)
    ax.set_ylabel(r"$k$", fontfamily="serif", labelpad=6)
    ax.set_zlabel(r"Gap", fontfamily="serif", labelpad=4)
    ax.set_zlim(0, 1.05)

    surf = ax.plot_surface(
        BB,
        KK,
        ZZ,
        cmap=_CMAP,
        linewidth=0,
        antialiased=True,
        rstride=1,
        cstride=1,
        alpha=0.95,
        shade=True,
    )
    # ridge line at B=2
    k_line = np.linspace(2, 48, 80)
    ax.plot(np.full_like(k_line, 2.0), k_line, 1.0 - 2.0 / k_line, color=GOLD, lw=2.0, zorder=10)

    n_frames = 120
    elev0, azim0 = 22, -55

    def update(frame):
        az = azim0 + frame * (360.0 / n_frames)
        elev = elev0 + 6.0 * np.sin(2 * np.pi * frame / n_frames)
        ax.view_init(elev=elev, azim=az)
        return (surf,)

    ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=1000 / 12, blit=False)
    _save_gif(ani, OUT / "anim_gap_surface_3d.gif", fps=12)
    plt.close(fig)


def anim_g2_surface_3d() -> None:
    """Orbiting surface sketch of support/arity envelope upper bound.

    Z = min(1 - 1/K, 1 - 1/max(1, floor(r/2))) with Z=0 for r<=3.
    """
    K = np.linspace(2, 16, 40)
    r = np.linspace(2, 28, 48)
    KK, RR = np.meshgrid(K, r)
    mcap = np.minimum(KK, np.floor(RR / 2.0))
    mcap = np.maximum(mcap, 1.0)
    ZZ = np.minimum(1.0 - 1.0 / KK, 1.0 - 1.0 / mcap)
    ZZ = np.where(RR <= 3, 0.0, ZZ)

    fig = plt.figure(figsize=(9.4, 6.4), dpi=130)
    fig.patch.set_facecolor(VOID)
    ax = fig.add_subplot(111, projection="3d")
    _style_3d(ax, r"Envelope sketch for $G_2(K,r)$  (partial; exact curve open)")
    ax.set_xlabel(r"$K$", fontfamily="serif", labelpad=6)
    ax.set_ylabel(r"$r$", fontfamily="serif", labelpad=6)
    ax.set_zlabel(r"ub", fontfamily="serif", labelpad=4)
    ax.set_zlim(0, 1.05)

    surf = ax.plot_surface(
        KK, RR, ZZ, cmap=_CMAP, linewidth=0, antialiased=True, rstride=1, cstride=1, alpha=0.95, shade=True
    )
    # butterfly point
    ax.scatter([2], [4], [0.5], color=GOLD, s=48, depthshade=False, zorder=20)

    n_frames = 120
    elev0, azim0 = 24, -48

    def update(frame):
        az = azim0 + frame * (360.0 / n_frames)
        elev = elev0 + 5.5 * np.sin(2 * np.pi * frame / n_frames)
        ax.view_init(elev=elev, azim=az)
        return (surf,)

    ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=1000 / 12, blit=False)
    _save_gif(ani, OUT / "anim_g2_support_3d.gif", fps=12)
    plt.close(fig)


def anim_parity_ratio_3d() -> None:
    """Surface of B*_na / B*_ad = (k m)/(m+1) over (k, m) — climbs hard."""
    k = np.linspace(1, 24, 44)
    m = np.linspace(1, 12, 36)
    KK, MM = np.meshgrid(k, m)
    ZZ = (KK * MM) / (MM + 1.0)
    # log for visual drama while keeping math honest via label
    ZZ_log = np.log10(ZZ)

    fig = plt.figure(figsize=(9.4, 6.4), dpi=130)
    fig.patch.set_facecolor(VOID)
    ax = fig.add_subplot(111, projection="3d")
    _style_3d(ax, r"$\log_{10}(B^\star_{\mathrm{na}}/B^\star_{\mathrm{ad}})=\log_{10}(km/(m+1))$")
    ax.set_xlabel(r"$k$", fontfamily="serif", labelpad=6)
    ax.set_ylabel(r"$m$", fontfamily="serif", labelpad=6)
    ax.set_zlabel(r"$\log_{10}$ ratio", fontfamily="serif", labelpad=4)

    surf = ax.plot_surface(
        KK, MM, ZZ_log, cmap=_CMAP, linewidth=0, antialiased=True, rstride=1, cstride=1, alpha=0.95, shade=True
    )

    n_frames = 110
    elev0, azim0 = 26, -60

    def update(frame):
        az = azim0 + frame * (360.0 / n_frames)
        elev = elev0 + 5.0 * np.sin(2 * np.pi * frame / n_frames)
        ax.view_init(elev=elev, azim=az)
        return (surf,)

    ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=1000 / 12, blit=False)
    _save_gif(ani, OUT / "anim_parity_ratio_3d.gif", fps=12)
    plt.close(fig)


def anim_cyclic_gate_walk() -> None:
    """Walk the cyclic gate with scrawly labels (wacky, not creepy)."""
    from matplotlib import font_manager

    names = {f.name for f in font_manager.fontManager.ttflist}
    hand = next((n for n in ("Ink Free", "Segoe Print", "Lucida Handwriting") if n in names), "DejaVu Sans")

    K = 12
    fifths = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
    n_frames = 96
    fig = plt.figure(figsize=(7.2, 7.4), dpi=120)
    fig.patch.set_facecolor(VOID)
    ax = fig.add_subplot(111)
    R = 0.78
    rng = np.random.default_rng(7)
    # pre-jitter station angles once so the wheel feels hand-drawn but stable
    jitter = rng.uniform(-0.025, 0.025, size=K)

    def update(frame):
        ax.clear()
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.35, 1.25)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_facecolor(VOID)
        fig.patch.set_facecolor(VOID)
        ax.text(
            0,
            1.12,
            "wheel walk  ·  ask g, then the tooth",
            ha="center",
            color=WHITE,
            fontsize=13,
            fontfamily=hand,
        )
        # wobbly ring
        th = np.linspace(0, 2 * np.pi, 180)
        wob = 1.0 + 0.02 * np.sin(4 * th)
        ax.plot(1.05 * wob * np.cos(th), 1.05 * wob * np.sin(th), color=DIM, lw=1.1)
        active = (frame // (n_frames // K)) % K
        for j in range(K):
            theta = np.pi / 2 - 2 * np.pi * j / K + jitter[j]
            x, y = R * np.cos(theta), R * np.sin(theta)
            on = j == active
            ax.add_patch(
                plt.Circle(
                    (x, y),
                    0.11,
                    fill=False,
                    edgecolor=GOLD if on else (WHITE if j % 3 == 0 else DIM),
                    lw=1.7 if on else 1.0,
                )
            )
            ax.text(
                x,
                y,
                fifths[j],
                ha="center",
                va="center",
                color=WHITE if on else MUTED,
                fontsize=10 if on else 8,
                fontfamily=hand,
                rotation=float(np.degrees(theta) - 90) * 0.12,
            )
            if on:
                ax.plot([0, 0.62 * x], [0, 0.62 * y], color=GOLD, lw=1.5, solid_capstyle="round")
        ax.add_patch(plt.Circle((0, 0), 0.24, fill=False, edgecolor=SOFT, lw=1.1))
        ax.text(0, 0.05, "g ???", ha="center", color=WHITE, fontsize=13, fontfamily=hand)
        ax.text(0, -0.12, f"tooth {active+1}", ha="center", color=GOLD, fontsize=10, fontfamily=hand)
        ax.text(
            0,
            -1.22,
            "named spoke → TV=1   ·   two pins can't hold the rim",
            ha="center",
            color=MUTED,
            fontsize=9,
            fontfamily=hand,
        )
        return []

    ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=1000 / 12, blit=False)
    _save_gif(ani, OUT / "anim_cyclic_gate.gif", fps=12)
    plt.close(fig)


def main() -> None:
    # 2D high-fps
    anim_gap_growth()
    anim_gap_approaches_one()
    anim_budget_race()
    anim_capacity()
    anim_greedy_blowup()
    anim_dual_envelope()
    anim_loop_pulse()
    anim_cyclic_gate_walk()
    # 3D selective
    anim_gap_surface_3d()
    anim_g2_surface_3d()
    anim_parity_ratio_3d()
    print(f"done → {OUT}")


if __name__ == "__main__":
    main()

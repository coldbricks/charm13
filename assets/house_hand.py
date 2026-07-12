"""CHARM13 house hand — original stroke lettering (inspired, not derived).

Brushy / crooked / lab-notebook energy for cyclic-gate figures.
Glyphs are original polylines in a unit cell [0,1]x[0,1]; no third-party font files.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
from matplotlib.collections import LineCollection

# Each glyph: list of strokes; each stroke is Nx2 array in unit box (x right, y up).
# Designed by hand for this project — not extracted from Sabarian/Mitshuka/Miladiator.

def _s(*pts: tuple[float, float]) -> np.ndarray:
    return np.asarray(pts, dtype=float)


# Minimal alphabet + digits we actually need on the wheel
_GLYPHS: dict[str, list[np.ndarray]] = {
    "A": [_s((0.08, 0.05), (0.42, 0.95), (0.78, 0.08)), _s((0.22, 0.38), (0.62, 0.38))],
    "B": [
        _s((0.18, 0.08), (0.18, 0.92)),
        _s((0.18, 0.92), (0.58, 0.92), (0.72, 0.78), (0.58, 0.55), (0.18, 0.55)),
        _s((0.18, 0.55), (0.62, 0.55), (0.78, 0.32), (0.58, 0.08), (0.18, 0.08)),
    ],
    "C": [_s((0.78, 0.78), (0.55, 0.95), (0.22, 0.82), (0.12, 0.5), (0.22, 0.18), (0.55, 0.05), (0.78, 0.22))],
    "D": [
        _s((0.18, 0.08), (0.18, 0.92)),
        _s((0.18, 0.92), (0.52, 0.92), (0.78, 0.68), (0.78, 0.32), (0.52, 0.08), (0.18, 0.08)),
    ],
    "E": [
        _s((0.72, 0.92), (0.2, 0.92), (0.2, 0.08), (0.72, 0.08)),
        _s((0.2, 0.5), (0.58, 0.5)),
    ],
    "F": [
        _s((0.22, 0.08), (0.22, 0.92), (0.75, 0.92)),
        _s((0.22, 0.52), (0.6, 0.52)),
    ],
    "G": [
        _s((0.78, 0.72), (0.55, 0.95), (0.22, 0.8), (0.12, 0.48), (0.25, 0.12), (0.55, 0.05), (0.8, 0.22), (0.8, 0.45), (0.5, 0.45)),
    ],
    "H": [
        _s((0.18, 0.08), (0.18, 0.92)),
        _s((0.72, 0.08), (0.72, 0.92)),
        _s((0.18, 0.5), (0.72, 0.5)),
    ],
    "I": [_s((0.35, 0.08), (0.35, 0.92)), _s((0.18, 0.92), (0.55, 0.92)), _s((0.18, 0.08), (0.55, 0.08))],
    "K": [
        _s((0.18, 0.08), (0.18, 0.92)),
        _s((0.72, 0.92), (0.22, 0.5), (0.75, 0.08)),
    ],
    "L": [_s((0.22, 0.92), (0.22, 0.08), (0.72, 0.08))],
    "N": [_s((0.18, 0.08), (0.18, 0.92), (0.72, 0.08), (0.72, 0.92))],
    "O": [_s((0.5, 0.95), (0.22, 0.78), (0.12, 0.5), (0.22, 0.2), (0.5, 0.05), (0.78, 0.2), (0.88, 0.5), (0.78, 0.78), (0.5, 0.95))],
    "P": [
        _s((0.2, 0.08), (0.2, 0.92)),
        _s((0.2, 0.92), (0.6, 0.92), (0.75, 0.75), (0.6, 0.55), (0.2, 0.55)),
    ],
    "S": [_s((0.72, 0.82), (0.5, 0.95), (0.25, 0.85), (0.25, 0.65), (0.7, 0.45), (0.7, 0.2), (0.4, 0.05), (0.15, 0.18))],
    "T": [_s((0.15, 0.92), (0.8, 0.92)), _s((0.48, 0.92), (0.48, 0.08))],
    "V": [_s((0.12, 0.92), (0.45, 0.08), (0.82, 0.92))],
    "W": [_s((0.08, 0.92), (0.25, 0.08), (0.45, 0.55), (0.65, 0.08), (0.88, 0.92))],
    "a": [
        _s((0.7, 0.55), (0.45, 0.7), (0.22, 0.5), (0.28, 0.22), (0.55, 0.1), (0.75, 0.28), (0.72, 0.08)),
    ],
    "b": [
        _s((0.22, 0.95), (0.22, 0.08)),
        _s((0.22, 0.55), (0.55, 0.68), (0.72, 0.45), (0.55, 0.12), (0.22, 0.2)),
    ],
    "d": [
        _s((0.72, 0.95), (0.72, 0.08)),
        _s((0.72, 0.55), (0.4, 0.68), (0.2, 0.42), (0.35, 0.12), (0.72, 0.22)),
    ],
    "e": [_s((0.7, 0.42), (0.25, 0.42), (0.3, 0.65), (0.55, 0.72), (0.75, 0.55), (0.55, 0.12), (0.22, 0.22))],
    "g": [
        _s((0.72, 0.55), (0.45, 0.7), (0.22, 0.48), (0.35, 0.15), (0.65, 0.12), (0.75, 0.35)),
        _s((0.72, 0.55), (0.72, -0.05), (0.4, -0.12), (0.22, 0.05)),
    ],
    "h": [
        _s((0.22, 0.95), (0.22, 0.08)),
        _s((0.22, 0.48), (0.5, 0.65), (0.72, 0.48), (0.72, 0.08)),
    ],
    "i": [_s((0.4, 0.08), (0.4, 0.55)), _s((0.4, 0.72), (0.4, 0.78))],
    "k": [
        _s((0.22, 0.08), (0.22, 0.95)),
        _s((0.68, 0.68), (0.28, 0.42), (0.7, 0.08)),
    ],
    "l": [_s((0.4, 0.08), (0.4, 0.95))],
    "m": [
        _s((0.12, 0.08), (0.12, 0.55)),
        _s((0.12, 0.48), (0.28, 0.65), (0.42, 0.4)),
        _s((0.42, 0.48), (0.58, 0.65), (0.75, 0.4), (0.75, 0.08)),
    ],
    "n": [
        _s((0.2, 0.08), (0.2, 0.58)),
        _s((0.2, 0.48), (0.48, 0.65), (0.7, 0.48), (0.7, 0.08)),
    ],
    "o": [_s((0.45, 0.68), (0.22, 0.5), (0.28, 0.18), (0.55, 0.08), (0.75, 0.28), (0.7, 0.58), (0.45, 0.68))],
    "p": [
        _s((0.22, 0.65), (0.22, -0.08)),
        _s((0.22, 0.55), (0.55, 0.68), (0.72, 0.45), (0.55, 0.15), (0.22, 0.22)),
    ],
    "s": [_s((0.65, 0.6), (0.4, 0.7), (0.22, 0.55), (0.6, 0.35), (0.65, 0.15), (0.35, 0.05), (0.18, 0.15))],
    "t": [_s((0.4, 0.95), (0.4, 0.12), (0.6, 0.08)), _s((0.22, 0.7), (0.58, 0.7))],
    "u": [
        _s((0.2, 0.65), (0.2, 0.25), (0.4, 0.08), (0.65, 0.22), (0.7, 0.65)),
    ],
    "w": [_s((0.1, 0.65), (0.25, 0.1), (0.4, 0.45), (0.55, 0.1), (0.75, 0.65))],
    "x": [_s((0.2, 0.65), (0.7, 0.1)), _s((0.7, 0.65), (0.2, 0.1))],
    "y": [_s((0.18, 0.65), (0.42, 0.28), (0.7, 0.65)), _s((0.42, 0.28), (0.35, -0.08))],
    "0": [_s((0.5, 0.95), (0.2, 0.75), (0.15, 0.4), (0.3, 0.1), (0.55, 0.05), (0.8, 0.25), (0.82, 0.65), (0.55, 0.95))],
    "1": [_s((0.35, 0.75), (0.5, 0.95), (0.5, 0.08)), _s((0.3, 0.08), (0.7, 0.08))],
    "2": [_s((0.2, 0.75), (0.4, 0.95), (0.7, 0.8), (0.65, 0.5), (0.25, 0.08), (0.78, 0.08))],
    "/": [_s((0.65, 0.95), (0.25, 0.05))],
    "=": [_s((0.18, 0.6), (0.75, 0.6)), _s((0.18, 0.35), (0.75, 0.35))],
    "_": [_s((0.15, 0.12), (0.75, 0.12))],
    "-": [_s((0.2, 0.48), (0.75, 0.48))],
    ".": [_s((0.4, 0.12), (0.48, 0.12))],
    ",": [_s((0.45, 0.2), (0.35, 0.0))],
    "?": [_s((0.25, 0.75), (0.4, 0.95), (0.7, 0.85), (0.65, 0.55), (0.45, 0.4)), _s((0.45, 0.18), (0.45, 0.1))],
    "!": [_s((0.45, 0.95), (0.45, 0.35)), _s((0.45, 0.15), (0.45, 0.08))],
    "+": [_s((0.45, 0.15), (0.45, 0.85)), _s((0.15, 0.5), (0.75, 0.5))],
    "(": [_s((0.6, 0.95), (0.35, 0.7), (0.3, 0.4), (0.4, 0.1))],
    ")": [_s((0.3, 0.95), (0.55, 0.7), (0.6, 0.4), (0.5, 0.1))],
    "#": [
        _s((0.3, 0.1), (0.4, 0.9)),
        _s((0.55, 0.1), (0.65, 0.9)),
        _s((0.15, 0.65), (0.8, 0.65)),
        _s((0.15, 0.35), (0.8, 0.35)),
    ],
    " ": [],
}


def _densify(stroke: np.ndarray, n: int = 24) -> np.ndarray:
    if len(stroke) < 2:
        return stroke
    out = []
    for i in range(len(stroke) - 1):
        t = np.linspace(0, 1, n, endpoint=False)
        seg = (1 - t)[:, None] * stroke[i] + t[:, None] * stroke[i + 1]
        out.append(seg)
    out.append(stroke[-1:])
    return np.vstack(out)


def draw_text(
    ax,
    x: float,
    y: float,
    text: str,
    *,
    scale: float = 0.12,
    color: str = "#F2F2F2",
    ghost: str = "#3A3A3A",
    rot_deg: float = 0.0,
    tracking: float = 0.72,
    lw: float = 1.35,
    rng: np.random.Generator | None = None,
    zorder: int = 8,
) -> None:
    """Draw house-hand text centered near (x, y). Multi-pass ink + slight stroke jitter."""
    if rng is None:
        rng = np.random.default_rng(abs(hash((round(x, 3), round(y, 3), text))) % (2**32))

    text = str(text)
    # measure width
    n = max(len(text), 1)
    width = n * scale * tracking
    # baseline-left of first glyph
    x0 = x - width / 2
    y0 = y - scale / 2

    ang = np.deg2rad(rot_deg)
    c, s = np.cos(ang), np.sin(ang)
    R = np.array([[c, -s], [s, c]])

    segs_main: list[np.ndarray] = []
    segs_ghost: list[np.ndarray] = []

    cursor = 0.0
    for ch in text:
        strokes = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or _GLYPHS.get(ch.lower())
        if strokes is None:
            # unknown: small tick
            strokes = [_s((0.3, 0.2), (0.5, 0.8), (0.7, 0.2))]
        for st in strokes:
            st = _densify(st, n=18)
            # brush pressure: slight normal noise
            if len(st) > 2:
                noise = rng.normal(0, 0.012, size=st.shape)
                st = st + noise
            # map unit cell -> world
            local = np.column_stack([st[:, 0] * scale + cursor, st[:, 1] * scale])
            # center of this string already accounted via x0,y0
            pts = (local @ R.T) + np.array([x0, y0])
            segs_main.append(pts)
            segs_ghost.append(pts + np.array([scale * 0.04, -scale * 0.03]))
        cursor += scale * tracking

    if segs_ghost:
        ax.add_collection(
            LineCollection(segs_ghost, colors=ghost, linewidths=lw * 0.85, alpha=0.45, zorder=zorder - 1, capstyle="round", joinstyle="round")
        )
    if segs_main:
        ax.add_collection(
            LineCollection(segs_main, colors=color, linewidths=lw, alpha=1.0, zorder=zorder, capstyle="round", joinstyle="round")
        )


def draw_lines(
    ax,
    lines: Iterable[str],
    x: float,
    y: float,
    *,
    scale: float = 0.09,
    line_gap: float = 0.12,
    **kwargs,
) -> None:
    lines = list(lines)
    h = (len(lines) - 1) * line_gap
    for i, line in enumerate(lines):
        draw_text(ax, x, y + h / 2 - i * line_gap, line, scale=scale, **kwargs)

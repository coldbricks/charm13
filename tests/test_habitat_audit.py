"""Mission 2: every habitat forges without BLOWN under skip_size."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from charm.forge import TEMPLATES, forge  # noqa: E402
from charm.smell import smell_report  # noqa: E402


def test_all_habitats_forge_clean(tmp_path: Path):
    for t in TEMPLATES:
        out = tmp_path / t
        r = forge(
            out,
            template=t,
            size_mb=300,
            seed=13,
            placeholder=True,
            force=True,
            unsafe_size=True,
            write_seed=False,
        )
        assert r.blown is False, f"{t} blown={r.blown_score} {r.smell_text}"
        rep = smell_report(out, template=t, skip_size=True)
        assert rep.blown is False, f"{t} re-smell blown codes={[f.code for f in rep.findings]}"


def test_transplant_cram_blows_steam(tmp_path: Path):
    out = tmp_path / "steam"
    forge(
        out,
        template="steam_depot",
        size_mb=300,
        seed=1,
        placeholder=True,
        force=True,
        unsafe_size=True,
    )
    (out / "evil.cram").write_bytes(b"\x00" * 1000)
    rep = smell_report(out, template="steam_depot", skip_size=True)
    assert rep.blown is True

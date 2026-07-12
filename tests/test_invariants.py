"""Invariant checks from docs/MASTER.md."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from charm.caliper import pick_extension, resolve_band  # noqa: E402
from charm.forgery import make_identity  # noqa: E402
from charm.props import payload_filename  # noqa: E402


def test_volume_extensions_not_magic_specialists():
    for name in ("wgs_lab", "adobe_cache", "photo_library", "sql_backup"):
        band = resolve_band(name)
        for ext in band.extensions:
            assert ext not in (".cram", ".bam", ".vcf", ".fq.gz", ".png", ".pdf")


def test_payload_name_no_giab():
    for seed in range(20):
        ident = make_identity(seed=seed, kind="wgs_lab")
        name = payload_filename("wgs_lab", ident).lower()
        assert "na24385" not in name
        assert "hg002" not in name


def test_pick_extension_stable():
    a = pick_extension("generic", 13)
    b = pick_extension("generic", 13)
    assert a == b

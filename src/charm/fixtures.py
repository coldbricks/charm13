"""Synthetic cover fixtures for bench and tests."""

from __future__ import annotations

import hashlib
from pathlib import Path


FIXTURE_NAMES = (
    "bad_giab_cram",
    "bad_single_cram",
    "clean_opaque",
    "clean_adobe",
)


def write_fixture(name: str, root: Path) -> Path:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if name == "bad_giab_cram":
        return _bad_giab_cram(root)
    if name == "bad_single_cram":
        return _bad_single_cram(root)
    if name == "clean_opaque":
        return _clean_opaque(root)
    if name == "clean_adobe":
        return _clean_adobe(root)
    raise ValueError(f"unknown fixture {name!r}")


def _bad_giab_cram(root: Path) -> Path:
    al = root / "aligned"
    raw = root / "raw_data"
    al.mkdir(parents=True, exist_ok=True)
    raw.mkdir(parents=True, exist_ok=True)
    (al / "NA24385.hg38.cram").write_bytes(b"\x00" * (2 * 1024 * 1024))
    for i, name in enumerate(("a.fq.gz", "b.fq.gz", "c.fq.gz")):
        (raw / name).write_bytes(bytes([i + 1]) * 36)
    (root / "README.txt").write_text("demo pack sample NA24385\n", encoding="utf-8")
    (root / "md5sums.txt").write_text(
        "deadbeef  aligned/NA24385.hg38.cram\n", encoding="utf-8"
    )
    return root


def _bad_single_cram(root: Path) -> Path:
    """One specialist lie — must BLOWN under any-bad law."""
    al = root / "aligned"
    al.mkdir(parents=True, exist_ok=True)
    (al / "job.cram").write_bytes(b"\x00" * (2 * 1024 * 1024))
    (root / "README.txt").write_text("handoff\n", encoding="utf-8")
    return root


def _clean_opaque(root: Path) -> Path:
    al = root / "aligned"
    al.mkdir(parents=True, exist_ok=True)
    notes = root / "notes"
    notes.mkdir(exist_ok=True)
    payload = al / "NG0CADD15.mm2.sortdup.bqsr.pack.dat"
    # non-constant head for clean entropy
    payload.write_bytes(os_urandom_mix(1024 * 1024))
    (root / "README.txt").write_text("opaque pack handoff\n", encoding="utf-8")
    (notes / "transfer_log.txt").write_text("raw omitted\n", encoding="utf-8")
    (root / "qc").mkdir(exist_ok=True)
    (root / "qc" / "coverage_summary.txt").write_text("note\tstub\n", encoding="utf-8")
    h = hashlib.md5(payload.read_bytes()).hexdigest()
    (root / "md5sums.txt").write_text(
        f"{h}  aligned/{payload.name}\n", encoding="utf-8"
    )
    return root


def _clean_adobe(root: Path) -> Path:
    mcf = root / "Media Cache Files"
    mcf.mkdir(parents=True, exist_ok=True)
    (root / "Media Cache").mkdir(exist_ok=True)
    payload = mcf / "CacheF_deadbeefcafe.bin"
    payload.write_bytes(os_urandom_mix(512 * 1024))
    (root / "Media Cache" / "idx.txt").write_text("peak cache\n", encoding="utf-8")
    return root


def os_urandom_mix(n: int) -> bytes:
    import os

    return os.urandom(n)

"""Bench calibration must not drift."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from charm.bench import run_bench  # noqa: E402


def test_bench_expectations():
    rows = run_bench()
    assert rows, "no bench rows"
    failed = [r.name for r in rows if not r.pass_]
    assert not failed, f"bench failed: {failed}"

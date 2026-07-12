"""Smell + blown_score tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from charm.smell import (  # noqa: E402
    BLOWN_THRESHOLD,
    SmellFinding,
    blown_score,
    is_blown,
    smell_report,
)


def test_blown_score_empty():
    assert blown_score([]) == 0.0


def test_any_bad_is_blown():
    findings = [SmellFinding("bad", "cram_magic", "x", path_key="a")]
    assert blown_score(findings) == pytest.approx(0.55)
    assert is_blown(findings) is True


def test_three_warns_not_enough_alone():
    findings = [
        SmellFinding("warn", "a", "a", path_key="1"),
        SmellFinding("warn", "b", "b", path_key="2"),
        SmellFinding("warn", "c", "c", path_key="3"),
    ]
    s = blown_score(findings)
    assert s < BLOWN_THRESHOLD
    assert is_blown(findings) is False


def test_fake_cram_is_blown(tmp_path: Path):
    d = tmp_path / "nebula_wgs"
    al = d / "aligned"
    al.mkdir(parents=True)
    raw = d / "raw_data"
    raw.mkdir()
    payload = al / "NA24385.hg38.cram"
    payload.write_bytes(b"\x00" * (2 * 1024 * 1024))
    (raw / "a.fq.gz").write_bytes(b"x" * 36)
    (raw / "b.fq.gz").write_bytes(b"y" * 36)
    (raw / "c.fq.gz").write_bytes(b"z" * 36)
    (d / "README.txt").write_text("giab demo\n", encoding="utf-8")

    report = smell_report(d, template="wgs_lab", skip_size=True)
    assert report.blown is True
    assert report.blown_score >= 0.55


def test_single_cram_lie_is_blown(tmp_path: Path):
    d = tmp_path / "one"
    al = d / "aligned"
    al.mkdir(parents=True)
    (al / "job.cram").write_bytes(b"\x00" * (1024 * 1024))
    (d / "README.txt").write_text("x\n", encoding="utf-8")
    report = smell_report(d, template="wgs_lab", skip_size=True)
    assert report.blown is True
    assert any(f.code in ("cram_magic", "format_magic") for f in report.findings)


def test_clean_dat_pack(tmp_path: Path):
    d = tmp_path / "pack"
    al = d / "aligned"
    al.mkdir(parents=True)
    import os

    payload = al / "NGDEADBEEF.pack.dat"
    payload.write_bytes(os.urandom(1024 * 1024))
    (d / "README.txt").write_text("opaque pack handoff\n", encoding="utf-8")
    (d / "notes").mkdir()
    (d / "notes" / "transfer_log.txt").write_text("ok\n", encoding="utf-8")

    report = smell_report(d, template="wgs_lab", skip_size=True)
    assert report.blown is False


def test_habitat_clash_cram_in_adobe(tmp_path: Path):
    d = tmp_path / "cache"
    d.mkdir()
    (d / "foo.cram").write_bytes(b"\x00" * 100)
    report = smell_report(d, template="adobe_cache", skip_size=True)
    assert report.blown is True
    codes = {f.code for f in report.findings}
    assert "habitat_clash" in codes or "cram_magic" in codes

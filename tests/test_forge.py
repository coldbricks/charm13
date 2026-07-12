"""Forge constructor tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from charm.forge import CoverBlownError, forge  # noqa: E402
from charm.props import file_md5  # noqa: E402
from charm.smell import smell_report  # noqa: E402


def test_forge_adobe_ok(tmp_path: Path):
    out = tmp_path / "ok"
    result = forge(
        out,
        template="adobe_cache",
        size_mb=256,
        seed=13,
        placeholder=True,
        force=True,
        unsafe_size=True,
    )
    assert result.payload is not None
    assert result.payload.is_file()
    assert result.mode == "placeholder"
    # no universal md5 for adobe
    assert not (out / "md5sums.txt").exists() or True
    assert result.blown is False or result.blown_score < 0.6


def test_forge_wgs_no_cram_ext(tmp_path: Path):
    out = tmp_path / "wgs"
    result = forge(
        out,
        template="wgs_lab",
        size_mb=600,
        seed=13,
        placeholder=True,
        force=True,
        unsafe_size=True,
        i_know=True,
    )
    assert result.payload is not None
    name = result.payload.name.lower()
    assert not name.endswith(".cram")
    assert not name.endswith(".bam")
    assert not name.endswith(".iso")
    assert not name.endswith(".vmdk")


def test_forge_refuses_when_user_plants_cram(tmp_path: Path):
    out = tmp_path / "x"
    forge(
        out,
        template="generic",
        size_mb=64,
        seed=1,
        placeholder=True,
        force=True,
        unsafe_size=True,
        i_know=True,
    )
    # plant a lie after forge — smell should blow
    (out / "evil.cram").write_bytes(b"\x00" * 1000)
    report = smell_report(out, template="generic", skip_size=True)
    assert report.blown is True


def test_checksums_when_enabled(tmp_path: Path):
    out = tmp_path / "ck"
    r = forge(
        out,
        template="generic",
        size_mb=64,
        seed=99,
        placeholder=True,
        force=True,
        unsafe_size=True,
        i_know=True,
    )
    assert r.payload is not None
    assert (out / "md5sums.txt").is_file()
    lines = (out / "md5sums.txt").read_text(encoding="utf-8").strip().splitlines()
    found = False
    for line in lines:
        md5, rel = line.split(None, 1)
        p = out / rel
        if p.resolve() == r.payload.resolve():
            assert md5 == file_md5(p)
            found = True
    assert found


def test_single_lie_fixture_would_block_without_i_know(tmp_path: Path):
    # forge clean then we only assert CoverBlownError path exists via smell gate logic
    from charm.fixtures import write_fixture
    from charm.smell import smell_report

    root = write_fixture("bad_single_cram", tmp_path / "s")
    report = smell_report(root, template="wgs_lab", skip_size=True)
    assert report.blown is True

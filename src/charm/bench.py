"""Calibration bench — score known fixtures."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

from charm.fixtures import FIXTURE_NAMES, write_fixture
from charm.smell import BLOWN_THRESHOLD, smell_report


@dataclass
class BenchRow:
    name: str
    score: float
    blown: bool
    expect_blown: bool
    codes: list[str]
    pass_: bool


EXPECT_BLOWN = {
    "bad_giab_cram": True,
    "bad_single_cram": True,
    "clean_opaque": False,
    "clean_adobe": False,
}

TEMPLATE = {
    "bad_giab_cram": "wgs_lab",
    "bad_single_cram": "wgs_lab",
    "clean_opaque": "wgs_lab",
    "clean_adobe": "adobe_cache",
}


def run_bench(tmp: Path | None = None) -> list[BenchRow]:
    own = tmp is None
    if own:
        tmp_ctx = tempfile.TemporaryDirectory(prefix="charm_bench_")
        base = Path(tmp_ctx.__enter__())
    else:
        tmp_ctx = None
        base = tmp
        base.mkdir(parents=True, exist_ok=True)

    rows: list[BenchRow] = []
    try:
        for name in FIXTURE_NAMES:
            root = base / name
            write_fixture(name, root)
            report = smell_report(
                root, template=TEMPLATE[name], skip_size=True
            )
            expect = EXPECT_BLOWN[name]
            ok = report.blown is expect
            rows.append(
                BenchRow(
                    name=name,
                    score=report.blown_score,
                    blown=report.blown,
                    expect_blown=expect,
                    codes=sorted({f.code for f in report.findings}),
                    pass_=ok,
                )
            )
    finally:
        if tmp_ctx is not None:
            tmp_ctx.__exit__(None, None, None)
    return rows


def format_table(rows: list[BenchRow]) -> str:
    lines = [
        "charm bench",
        f"threshold={BLOWN_THRESHOLD} (any bad also blows)",
        "",
        f"{'fixture':<18} {'score':>7} {'blown':>6} {'expect':>6} {'pass':>5}  codes",
        "-" * 72,
    ]
    for r in rows:
        lines.append(
            f"{r.name:<18} {r.score:>7.3f} {str(r.blown):>6} "
            f"{str(r.expect_blown):>6} {('ok' if r.pass_ else 'FAIL'):>5}  "
            f"{','.join(r.codes) if r.codes else '-'}"
        )
    n_fail = sum(1 for r in rows if not r.pass_)
    lines.append("")
    lines.append(f"result: {len(rows) - n_fail}/{len(rows)} expectations met")
    return "\n".join(lines)

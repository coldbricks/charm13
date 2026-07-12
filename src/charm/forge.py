"""forge — build cover tree + optional volume."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from charm.caliper import resolve_band, validate_size_mb
from charm.forgery import make_identity
from charm.kernel import create_container, create_sparse_placeholder, find_veracrypt
from charm.props import (
    apply_identity_times,
    build_decoys,
    payload_filename,
    payload_relpath,
    write_checksums,
    write_tree,
)
from charm.smell import SmellFinding, SmellReport, blown_score, format_report, smell_report
from charm.caliper import all_templates


TEMPLATES = all_templates()


class CoverBlownError(RuntimeError):
    def __init__(self, report: SmellReport, root: Path):
        self.report = report
        self.root = root
        super().__init__(
            f"cover blown (score={report.blown_score:.3f}, any_bad="
            f"{any(f.severity == 'bad' for f in report.findings)}); "
            f"tree at {root} (pass --i-know to keep)"
        )


@dataclass
class ForgeResult:
    root: Path
    payload: Path | None
    seed: int
    template: str
    size_mb: int
    mode: str
    smell_text: str
    blown_score: float
    blown: bool


def forge(
    out_dir: Path,
    *,
    template: str = "adobe_cache",
    size_mb: int | None = None,
    seed: int | None = None,
    password: str | None = None,
    placeholder: bool = False,
    tree_only: bool = False,
    force: bool = False,
    i_know: bool = False,
    unsafe_size: bool = False,
    write_seed: bool = False,
) -> ForgeResult:
    if template not in TEMPLATES:
        raise ValueError(f"unknown template {template!r}; choose from {TEMPLATES}")

    band = resolve_band(template)
    if size_mb is None:
        size_mb = band.default_mb

    size_notes = validate_size_mb(template, size_mb)
    if size_notes and not tree_only:
        for n in size_notes:
            if "ceiling" in n and not unsafe_size:
                raise ValueError(n + " (use --unsafe-size)")

    ident = make_identity(seed=seed, kind=template)
    root = out_dir.resolve()
    if root.exists() and any(root.iterdir()) and not force:
        raise FileExistsError(f"refusing non-empty directory without --force: {root}")
    if root.exists() and force:
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)

    payload_name = payload_filename(template, ident)
    decoys = build_decoys(template, ident, payload_name)
    write_tree(root, decoys)

    rel = payload_relpath(template, payload_name, ident)
    payload_path = root / rel
    payload_path.parent.mkdir(parents=True, exist_ok=True)

    mode = "tree_only"
    payload: Path | None = None
    if not tree_only:
        payload = payload_path
        if placeholder or password is None:
            create_sparse_placeholder(payload, size_mb, force=True)
            mode = "placeholder"
        else:
            if find_veracrypt() is None:
                raise RuntimeError(
                    "password given but VeraCrypt not found; "
                    "use --placeholder or install VeraCrypt"
                )
            create_container(payload, size_mb, password, force=True)
            mode = "veracrypt"

    if band.write_checksums:
        write_checksums(root, payload, template)

    apply_identity_times(root, ident)

    skip_size = tree_only
    report = smell_report(root, template=template, skip_size=skip_size)

    findings = list(report.findings)
    have_size = {f.code for f in findings}
    for n in size_notes:
        if "ceiling" in n and "size_high" in have_size:
            continue
        if "floor" in n and "size_low" in have_size:
            continue
        sev = "bad" if "ceiling" in n else "warn"
        findings.append(SmellFinding(sev, "caliper", n, path_key="caliper"))

    score = blown_score(findings)
    report = SmellReport(findings, score)
    smell_text = format_report(findings, score, report.threshold, report.blown)

    # Operator receipt is optional — default off (T1 quietness).
    if write_seed:
        seed_path = root / ".charm_seed"
        seed_path.write_text(
            f"seed={ident.seed}\ntemplate={template}\n"
            f"payload={payload_name if payload else ''}\nmode={mode}\n"
            f"blown_score={score:.4f}\nblown={report.blown}\n",
            encoding="utf-8",
        )

    if report.blown and not i_know:
        raise CoverBlownError(report, root)

    return ForgeResult(
        root=root,
        payload=payload,
        seed=ident.seed,
        template=template,
        size_mb=size_mb,
        mode=mode,
        smell_text=smell_text,
        blown_score=score,
        blown=report.blown,
    )

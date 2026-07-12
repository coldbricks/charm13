"""Cover smell tests — detection predicate + blown_score."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from charm.caliper import resolve_band
from charm.ecology import HABITAT, SPECIALIST, family_for_name, specialist_ext_for_name

WEIGHTS = {"bad": 0.55, "warn": 0.25, "info": 0.05}
# Any single bad is enough to blow; warn stacks can also blow at 0.6.
BLOWN_THRESHOLD = 0.6

GIAB_TOKENS = (
    "na24385",
    "hg002",
    "na12878",
    "hg001",
    "na24143",
    "hg003",
    "hg004",
    "hg005",
)


@dataclass
class SmellFinding:
    severity: str  # info | warn | bad
    code: str
    detail: str
    path_key: str = ""  # for dedupe


@dataclass
class SmellReport:
    findings: list[SmellFinding]
    blown_score: float
    threshold: float = BLOWN_THRESHOLD

    @property
    def blown(self) -> bool:
        if any(f.severity == "bad" for f in self.findings):
            return True
        return self.blown_score >= self.threshold

    def text(self) -> str:
        return format_report(self.findings, self.blown_score, self.threshold, self.blown)


def blown_score(findings: list[SmellFinding]) -> float:
    remain = 1.0
    for f in findings:
        w = WEIGHTS.get(f.severity, 0.05)
        remain *= 1.0 - w
    score = 1.0 - remain
    return min(1.0, max(0.0, score))


def is_blown(findings: list[SmellFinding], score: float | None = None) -> bool:
    if any(f.severity == "bad" for f in findings):
        return True
    if score is None:
        score = blown_score(findings)
    return score >= BLOWN_THRESHOLD


def smell_path(
    path: Path,
    template: str | None = None,
    *,
    skip_size: bool = False,
) -> list[SmellFinding]:
    return smell_report(path, template=template, skip_size=skip_size).findings


def smell_report(
    path: Path,
    template: str | None = None,
    *,
    skip_size: bool = False,
) -> SmellReport:
    findings: list[SmellFinding] = []
    path = path.resolve()

    if not path.exists():
        findings = [SmellFinding("bad", "missing", f"path does not exist: {path}")]
        score = blown_score(findings)
        return SmellReport(findings, score)

    if path.is_file():
        findings.extend(_smell_file(path, template, skip_size=skip_size))
        findings.extend(_smell_siblings(path.parent, path))
        findings.extend(_smell_path_tokens(path))
        findings = _dedupe(findings)
        score = blown_score(findings)
        return SmellReport(findings, score)

    files = [p for p in path.rglob("*") if p.is_file()]
    # keep .charm_seed visible to T1 oracle
    if not files:
        findings.append(SmellFinding("warn", "empty_tree", "directory has no files"))
        score = blown_score(findings)
        return SmellReport(findings, score)

    if template is None:
        findings.append(
            SmellFinding(
                "warn",
                "no_habitat",
                "no -t template: habitat law not applied; pass -t for full oracle",
            )
        )

    for p in files:
        findings.extend(_smell_path_tokens(p))
        findings.extend(_smell_tool_fingerprint(p))

    big = sorted(files, key=lambda p: p.stat().st_size, reverse=True)
    largest = big[0]
    findings.extend(_smell_file(largest, template, skip_size=skip_size))
    findings.extend(_smell_tree_balance(files, largest))
    findings.extend(_smell_tree_siblings(files, largest, template))
    findings.extend(_smell_specialist_lies(files))
    findings.extend(_smell_habitat(files, template))
    findings.extend(_smell_checksums(path, files))
    findings.extend(_smell_zero_fill(largest))

    findings = _dedupe(findings)
    score = blown_score(findings)
    return SmellReport(findings, score)


def _dedupe(findings: list[SmellFinding]) -> list[SmellFinding]:
    # one finding per (code, path_key) preferring higher severity
    rank = {"bad": 0, "warn": 1, "info": 2}
    best: dict[tuple[str, str], SmellFinding] = {}
    for f in findings:
        key = (f.code, f.path_key or f.detail)
        prev = best.get(key)
        if prev is None or rank.get(f.severity, 9) < rank.get(prev.severity, 9):
            best[key] = f
    # also collapse same code+same file basename in detail
    by_code_path: dict[tuple[str, str], SmellFinding] = {}
    for f in best.values():
        pk = f.path_key or ""
        key2 = (f.code, pk)
        prev = by_code_path.get(key2)
        if prev is None or rank.get(f.severity, 9) < rank.get(prev.severity, 9):
            by_code_path[key2] = f
    return list(by_code_path.values())


def _smell_path_tokens(path: Path) -> list[SmellFinding]:
    out: list[SmellFinding] = []
    # basename components only (reduce FP on unrelated parent dirs)
    parts = path.name.lower().replace("_", "-").split("-")
    name = path.name.lower()
    for token in GIAB_TOKENS:
        if token in name or token in parts:
            out.append(
                SmellFinding(
                    "bad",
                    "giab_token",
                    f"{path.name}: well-known reference token '{token}'",
                    path_key=path.name.lower(),
                )
            )
    return out


def _smell_tool_fingerprint(path: Path) -> list[SmellFinding]:
    if path.name == ".charm_seed":
        return [
            SmellFinding(
                "warn",
                "tool_fingerprint",
                ".charm_seed present (CHARM operator receipt)",
                path_key=".charm_seed",
            )
        ]
    return []


def _smell_file(
    path: Path, template: str | None, *, skip_size: bool
) -> list[SmellFinding]:
    out: list[SmellFinding] = []
    size = path.stat().st_size
    mb = size / (1024 * 1024)
    name = path.name.lower()
    pk = path.name.lower()

    head = b""
    if size > 0:
        with path.open("rb") as f:
            head = f.read(8)

    # specialist magic only via _smell_specialist_lies for consistency
    sample = b""
    if size > 0:
        with path.open("rb") as f:
            sample = f.read(65536)
    if len(sample) >= 256:
        uniq = len(set(sample))
        if uniq > 240 and mb > 100:
            out.append(
                SmellFinding(
                    "info",
                    "high_entropy",
                    f"{path.name}: high byte diversity in first 64KiB",
                    path_key=pk,
                )
            )

    if template and not skip_size:
        band = resolve_band(template)
        if mb < band.min_mb:
            out.append(
                SmellFinding(
                    "warn",
                    "size_low",
                    f"{mb:.0f} MiB under {band.name} floor {band.min_mb} MiB",
                    path_key=pk,
                )
            )
        if mb > band.max_mb:
            out.append(
                SmellFinding(
                    "bad",
                    "size_high",
                    f"{mb:.0f} MiB over {band.name} ceiling {band.max_mb} MiB",
                    path_key=pk,
                )
            )
    elif not skip_size and mb > 200 * 1024:
        out.append(
            SmellFinding(
                "warn",
                "huge",
                f"{mb:.0f} MiB is unusually large without a habitat band",
                path_key=pk,
            )
        )

    if name.endswith((".hc", ".tc", ".vc", ".vera")):
        out.append(
            SmellFinding(
                "info",
                "known_volume_name",
                f"{path.name}: name resembles a known container extension",
                path_key=pk,
            )
        )

    return out


def _smell_zero_fill(path: Path) -> list[SmellFinding]:
    """Large low-entropy payload smells like placeholder theater."""
    try:
        size = path.stat().st_size
    except OSError:
        return []
    if size < 64 * 1024 * 1024:
        return []
    with path.open("rb") as f:
        sample = f.read(256 * 1024)
    if not sample:
        return []
    uniq = len(set(sample))
    if uniq <= 4:
        return [
            SmellFinding(
                "bad",
                "zero_fill",
                f"{path.name}: large file with near-constant bytes (placeholder/sparse smell)",
                path_key=path.name.lower(),
            )
        ]
    if uniq < 16:
        return [
            SmellFinding(
                "warn",
                "low_entropy",
                f"{path.name}: large file with very low byte diversity",
                path_key=path.name.lower(),
            )
        ]
    return []


def _smell_siblings(parent: Path, payload: Path) -> list[SmellFinding]:
    try:
        sibs = [p for p in parent.iterdir() if p.is_file()]
    except OSError as e:
        return [SmellFinding("warn", "listdir", str(e))]
    return _toy_sibling_check(sibs, payload)


def _smell_tree_siblings(
    files: list[Path], largest: Path, template: str | None
) -> list[SmellFinding]:
    if template == "incomplete_download":
        return []
    return _toy_sibling_check(files, largest)


def _toy_sibling_check(files: list[Path], payload: Path) -> list[SmellFinding]:
    """
    Theater pattern: huge payload + only tiny stubs.
    If any mid-size companion exists (1 KiB .. 8 MiB), treat as less suspicious.
    """
    out: list[SmellFinding] = []
    try:
        psz = payload.stat().st_size
        pres = payload.resolve()
    except OSError:
        return out
    if psz < 256 * 1024 * 1024:
        return out

    others = []
    for p in files:
        try:
            if p.resolve() == pres:
                continue
            if p.name in (".charm_seed",):
                continue
            others.append(p)
        except OSError:
            continue

    tiny = [p for p in others if p.stat().st_size < 512]
    mid = [p for p in others if 1024 <= p.stat().st_size <= 8 * 1024 * 1024]
    if len(tiny) >= 4 and len(mid) == 0:
        out.append(
            SmellFinding(
                "warn",
                "toy_siblings",
                "large payload with only sub-512-byte companions (no mid-size decoys)",
                path_key=payload.name.lower(),
            )
        )
    return out


def _smell_tree_balance(files: list[Path], largest: Path) -> list[SmellFinding]:
    out: list[SmellFinding] = []
    total = sum(p.stat().st_size for p in files)
    if total <= 0:
        return out
    share = largest.stat().st_size / total
    # fire from 1 GiB (defaults matter)
    if share > 0.99 and largest.stat().st_size > 1 * 1024 * 1024 * 1024:
        out.append(
            SmellFinding(
                "warn",
                "monolith",
                f"{largest.name} is {share * 100:.1f}% of tree bytes",
                path_key=largest.name.lower(),
            )
        )
    return out


def _smell_checksums(root: Path, files: list[Path]) -> list[SmellFinding]:
    out: list[SmellFinding] = []
    sums = root / "md5sums.txt"
    if not sums.is_file():
        return out
    try:
        lines = sums.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as e:
        return [SmellFinding("warn", "listdir", str(e))]

    import hashlib

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        expect, rel = parts
        rel = rel.lstrip("*").strip()
        target = root / rel
        if not target.is_file():
            out.append(
                SmellFinding(
                    "bad",
                    "checksum_mismatch",
                    f"md5sums lists missing file: {rel}",
                    path_key=rel,
                )
            )
            continue
        h = hashlib.md5()
        with target.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        got = h.hexdigest()
        if got.lower() != expect.lower():
            out.append(
                SmellFinding(
                    "bad",
                    "checksum_mismatch",
                    f"{rel}: md5 {got} != listed {expect}",
                    path_key=rel,
                )
            )
    return out


def _smell_specialist_lies(files: list[Path]) -> list[SmellFinding]:
    out: list[SmellFinding] = []
    for path in files:
        if path.stat().st_size == 0:
            continue
        name = path.name
        ext = specialist_ext_for_name(name)
        if ext is None:
            continue
        fam, magic = SPECIALIST[ext]
        with path.open("rb") as f:
            head = f.read(16)

        ok = True
        code = "format_magic"
        if fam == "bam":
            ok = head[:2] == b"\x1f\x8b" or head.startswith(b"BAM")
            code = "bam_magic"
        elif fam in ("mp4", "mov"):
            ok = len(head) >= 8 and head[4:8] == b"ftyp"
        elif fam == "webp":
            ok = head.startswith(b"RIFF") and b"WEBP" in head[:16]
        elif fam == "pe":
            ok = head[:2] == b"MZ"
        elif fam == "iso":
            # no reliable cheap magic; treat volume-sized fake iso as opaque lie
            if path.stat().st_size >= 64 * 1024 * 1024:
                # sample mid-file for zeros
                with path.open("rb") as f:
                    f.seek(min(32 * 1024, path.stat().st_size - 1))
                    mid = f.read(4096)
                if mid and len(set(mid)) <= 4:
                    ok = False
                    code = "format_magic"
                else:
                    continue
            else:
                continue
        elif magic is not None:
            ok = head.startswith(magic)
            if fam == "cram":
                code = "cram_magic"
            elif fam == "gzip":
                code = "gzip_magic"
        else:
            # specialist name, no magic — still flag large files as opaque required
            if path.stat().st_size >= 32 * 1024 * 1024:
                out.append(
                    SmellFinding(
                        "bad",
                        "opaque_required",
                        f"{path.name}: specialist-looking name without checkable magic "
                        f"(family {fam}); use opaque ext for volumes",
                        path_key=path.name.lower(),
                    )
                )
            continue

        if not ok:
            out.append(
                SmellFinding(
                    "bad",
                    code,
                    f"{path.name}: extension claims {fam} but header does not match",
                    path_key=path.name.lower(),
                )
            )
    return out


def _smell_habitat(files: list[Path], template: str | None) -> list[SmellFinding]:
    if not template or template not in HABITAT:
        return []
    if template == "incomplete_download":
        # still allow mess, but specialist lies handled elsewhere
        return []
    home = HABITAT[template]
    out: list[SmellFinding] = []
    for path in files:
        fam = family_for_name(path.name)
        if fam is None:
            continue
        if fam == "gzip" and template not in ("wgs_lab", "sql_backup", "docker_cache"):
            continue
        if home:
            if fam not in home:
                out.append(
                    SmellFinding(
                        "bad",
                        "habitat_clash",
                        f"{path.name}: family '{fam}' unnatural in habitat '{template}'",
                        path_key=path.name.lower(),
                    )
                )
        else:
            # empty habitat: any specialist is clash
            out.append(
                SmellFinding(
                    "bad",
                    "habitat_clash",
                    f"{path.name}: family '{fam}' unnatural in habitat '{template}' "
                    "(opaque-only habitat)",
                    path_key=path.name.lower(),
                )
            )
    return out


def format_report(
    findings: list[SmellFinding],
    score: float | None = None,
    threshold: float = BLOWN_THRESHOLD,
    blown: bool | None = None,
) -> str:
    if score is None:
        score = blown_score(findings)
    if blown is None:
        blown = is_blown(findings, score)
    # Dual gate: any bad OR score ≥ threshold. Score is a severity monoid, not P(generated).
    note = (
        "score=severity monoid (not a probability); "
        f"refuse if any bad OR score>={threshold}; "
        "static suite ≠ full adaptive T1 bound (docs/T1_BUDGET.md)"
    )
    if not findings:
        state = "BLOWN" if blown else "ok"
        return (
            f"smell: clean  blown_score={score:.3f} [{state}]  "
            f"(threshold {threshold}; {note})"
        )
    order = {"bad": 0, "warn": 1, "info": 2}
    findings = sorted(findings, key=lambda f: order.get(f.severity, 9))
    lines = ["smell report"]
    for f in findings:
        lines.append(f"  [{f.severity}] {f.code}: {f.detail}")
    bad = sum(1 for f in findings if f.severity == "bad")
    warn = sum(1 for f in findings if f.severity == "warn")
    state = "BLOWN" if blown else "ok"
    lines.append(
        f"summary: {bad} bad, {warn} warn, {len(findings)} total  "
        f"blown_score={score:.3f} [{state}]  ({note})"
    )
    return "\n".join(lines)

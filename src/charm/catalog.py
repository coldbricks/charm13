"""Smell code catalog — what each finding means."""

from __future__ import annotations

CATALOG: dict[str, dict[str, str]] = {
    "missing": {
        "sev": "bad",
        "tier": "T0",
        "means": "Path does not exist.",
        "fix": "Nothing to evaluate.",
    },
    "cram_magic": {
        "sev": "bad",
        "tier": "T1",
        "means": "Name claims CRAM; first bytes are not CRAM.",
        "fix": "Do not use .cram for opaque volumes. Use .dat/.bin/.img.",
    },
    "bam_magic": {
        "sev": "bad",
        "tier": "T1",
        "means": "Name claims BAM; header is not BAM/BGZF.",
        "fix": "Same as cram_magic: stop lying with specialist extensions.",
    },
    "gzip_magic": {
        "sev": "bad",
        "tier": "T1",
        "means": "Name claims gzip; bytes are not 1f 8b.",
        "fix": "Toy .fq.gz / .vcf.gz placeholders blow the cover.",
    },
    "giab_token": {
        "sev": "bad",
        "tier": "T1",
        "means": "Path uses a famous public reference sample id.",
        "fix": "Never NA24385/HG002/etc. Forge already avoids these.",
    },
    "size_high": {
        "sev": "bad",
        "tier": "T1",
        "means": "Payload larger than template size band ceiling.",
        "fix": "Pick a template that matches size, or shrink the volume.",
    },
    "size_low": {
        "sev": "warn",
        "tier": "T1",
        "means": "Payload smaller than template floor (story mismatch).",
        "fix": "Increase size or use a smaller-band template.",
    },
    "caliper": {
        "sev": "warn",
        "tier": "T1",
        "means": "Size band validator note from forge.",
        "fix": "Align --size-mb with template or pass --unsafe-size knowingly.",
    },
    "toy_siblings": {
        "sev": "warn",
        "tier": "T1",
        "means": "Huge file next to many sub-512B toys.",
        "fix": "Either grow decoys or use incomplete_download intentionally.",
    },
    "monolith": {
        "sev": "warn",
        "tier": "T1",
        "means": "One file is almost the entire tree by bytes.",
        "fix": "Add plausible bulk or accept the warn for single-blob packs.",
    },
    "high_entropy": {
        "sev": "info",
        "tier": "T1",
        "means": "Looks compressed or encrypted (high byte diversity).",
        "fix": "Normal for volumes. Not decisive alone.",
    },
    "huge": {
        "sev": "warn",
        "tier": "T0",
        "means": "Very large file without a template band.",
        "fix": "Pass -t so size is judged in context.",
    },
    "empty_tree": {
        "sev": "warn",
        "tier": "T0",
        "means": "Directory has no files.",
        "fix": "Forge a cover or point smell at the right path.",
    },
    "known_volume_name": {
        "sev": "info",
        "tier": "T1",
        "means": "Filename looks like a known container type (.hc, .tc, .vc).",
        "fix": "Prefer boring names from forge templates.",
    },
    "checksum_mismatch": {
        "sev": "bad",
        "tier": "T1",
        "means": "md5sums.txt does not match file bytes.",
        "fix": "Regenerate with forge; do not hand-edit checksums.",
    },
    "format_magic": {
        "sev": "bad",
        "tier": "T1",
        "means": "Extension claims a real file format; header disagrees.",
        "fix": "Use opaque extensions for volumes, or ship real format bytes.",
    },
    "habitat_clash": {
        "sev": "bad",
        "tier": "T1",
        "means": "File family does not belong in the claimed habitat.",
        "fix": "Pick a matching template or remove the foreign specialist files.",
    },
    "zero_fill": {
        "sev": "bad",
        "tier": "T1",
        "means": "Large near-constant payload (placeholder/sparse theater).",
        "fix": "Use a real encrypted volume, not zero-filled sparse files.",
    },
    "low_entropy": {
        "sev": "warn",
        "tier": "T1",
        "means": "Large payload with very low byte diversity.",
        "fix": "Real ciphertext is high entropy.",
    },
    "tool_fingerprint": {
        "sev": "warn",
        "tier": "T1",
        "means": ".charm_seed operator receipt present in the tree.",
        "fix": "Move or delete before handoff if you care about T1 quietness.",
    },
    "no_habitat": {
        "sev": "warn",
        "tier": "T1",
        "means": "smell without -t skips habitat law.",
        "fix": "Pass -t matching the claimed story.",
    },
    "opaque_required": {
        "sev": "bad",
        "tier": "T1",
        "means": "Specialist-looking name without checkable magic.",
        "fix": "Use opaque extensions for volumes.",
    },
    "score_semantics": {
        "sev": "info",
        "tier": "T1",
        "means": (
            "blown_score is a severity monoid (noisy-OR of engineering weights), "
            "not a calibrated probability of generation. Refuse = any bad OR score≥0.6."
        ),
        "fix": "Read findings; do not treat the scalar as P(generated). See docs/T1_BUDGET.md.",
    },
    "adaptive_t1": {
        "sev": "info",
        "tier": "T1",
        "means": (
            "charm smell is a nonadaptive checklist. Research (research/m5, LADDER_MASTER) "
            "proves a sharp budget-2 adaptivity envelope G_2(K)=1-1/K under arity-K OPEN "
            "queries, and on synthetic branch/parity habitats adaptive short inspections "
            "can be arbitrarily stronger than fixed checklists of the same look-count."
        ),
        "fix": (
            "Prefer gate/branch coherence before local magic; global relations matter. "
            "Clean smell is necessary refuse machinery, not a complete adaptive T1 bound."
        ),
    },
    "gate_before_local": {
        "sev": "info",
        "tier": "T1",
        "means": (
            "When a habitat has many paths, asking which path is live before local "
            "header checks is the adaptive pattern that static local-only stacks miss."
        ),
        "fix": "Ensure manifests/pointers match the payload path; see docs/T1_BUDGET.md.",
    },
    "listdir": {
        "sev": "warn",
        "tier": "T0",
        "means": "Could not list directory.",
        "fix": "Permissions or path issue.",
    },
}


def explain(code: str) -> str:
    meta = CATALOG.get(code)
    if not meta:
        return f"{code}: unknown code (no catalog entry)"
    return (
        f"{code}\n"
        f"  severity  {meta['sev']}\n"
        f"  tier      {meta['tier']}\n"
        f"  means     {meta['means']}\n"
        f"  fix       {meta['fix']}"
    )


def list_codes() -> list[str]:
    return sorted(CATALOG.keys())

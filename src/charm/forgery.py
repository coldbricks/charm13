"""Random but coherent cover-story fields."""

from __future__ import annotations

import hashlib
import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta


_LABS = (
    "North Pier Sequencing",
    "Basin Bioanalytics",
    "Redwood Molecular",
    "Harborline Genomics Core",
    "Kiln Street Labs",
    "Cascade Sample Ops",
)

_CITIES = (
    "San Diego, CA",
    "Boston, MA",
    "Austin, TX",
    "Seattle, WA",
    "Cambridge, UK",
    "Heidelberg, DE",
)

_PIPELINES = (
    "BWA-MEM 0.7.17 + GATK 4.3",
    "minimap2 2.26 + GATK 4.4",
    "DRAGEN host 4.2",
    "MegaBOLT WGS 1.x",
)

_ANALYSTS = (
    "r.kim",
    "j.alvarez",
    "m.okafor",
    "s.brennan",
    "a.petrov",
)

_CACHE_VENDORS = (
    "Adobe",
    "Steam",
    "NVIDIA",
    "Unity",
    "Autodesk",
)


@dataclass(frozen=True)
class CoverIdentity:
    seed: int
    sample_id: str
    project_id: str
    lab: str
    site: str
    pipeline: str
    analyst: str
    email: str
    created: datetime
    modified: datetime
    vendor: str

    def short_hash(self, n: int = 8) -> str:
        h = hashlib.sha256(f"{self.seed}:{self.sample_id}".encode()).hexdigest()
        return h[:n]


def _rng(seed: int | None) -> random.Random:
    if seed is None:
        seed = random.SystemRandom().randint(0, 2**31 - 1)
    return random.Random(seed), seed


def make_identity(seed: int | None = None, kind: str = "wgs") -> CoverIdentity:
    rng, seed_i = _rng(seed)
    created = datetime.now() - timedelta(
        days=rng.randint(30, 900),
        hours=rng.randint(0, 23),
        minutes=rng.randint(0, 59),
    )
    modified = created + timedelta(days=rng.randint(0, 40), hours=rng.randint(0, 12))

    if kind in ("wgs_lab", "incomplete_download"):
        sample = f"PRO{rng.randint(0, 999999):06d}"
        project = f"NG{rng.randint(0, 99999999):08X}"[:10]
    elif kind == "steam_depot":
        sample = str(rng.randint(1000000, 9999999))
        project = f"depot_{rng.randint(100, 999)}"
    else:
        sample = "".join(rng.choice(string.ascii_lowercase) for _ in range(8))
        project = f"job_{rng.randint(10000, 99999)}"

    lab = rng.choice(_LABS)
    analyst = rng.choice(_ANALYSTS)
    domain = lab.lower().replace(" ", "").replace(",", "")[:12] + ".example"
    return CoverIdentity(
        seed=seed_i,
        sample_id=sample,
        project_id=project,
        lab=lab,
        site=rng.choice(_CITIES),
        pipeline=rng.choice(_PIPELINES),
        analyst=analyst,
        email=f"{analyst}@{domain}",
        created=created,
        modified=modified,
        vendor=rng.choice(_CACHE_VENDORS),
    )


def fake_md5(seed: int, name: str) -> str:
    return hashlib.md5(f"{seed}:{name}".encode()).hexdigest()


def fake_sha256(seed: int, name: str) -> str:
    return hashlib.sha256(f"{seed}:{name}".encode()).hexdigest()

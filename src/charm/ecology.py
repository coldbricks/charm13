"""
File ecology — what "natural" means for covers.

WGS/genomics is one habitat. There are many. Blown if the tree
does not look like it belongs in the claimed habitat.
"""

from __future__ import annotations

# Extensions that imply a parser and a magic number.
# Opaque volumes must NOT use these unless magic is real.
SPECIALIST: dict[str, tuple[str, bytes | None]] = {
    # genomics
    ".cram": ("cram", b"CRAM"),
    ".bam": ("bam", None),  # BAM or BGZF — special-cased
    ".bai": ("bai", None),
    ".crai": ("crai", None),
    ".vcf": ("vcf", None),
    ".bcf": ("bcf", None),
    ".fastq": ("fastq", None),
    ".fq": ("fq", None),
    # compressed text often paired with above
    ".fastq.gz": ("gzip", b"\x1f\x8b"),
    ".fq.gz": ("gzip", b"\x1f\x8b"),
    ".vcf.gz": ("gzip", b"\x1f\x8b"),
    # containers / archives
    ".zip": ("zip", b"PK"),
    ".7z": ("7z", b"7z\xbc\xaf\x27\x1c"),
    ".gz": ("gzip", b"\x1f\x8b"),
    ".pdf": ("pdf", b"%PDF"),
    ".png": ("png", b"\x89PNG\r\n\x1a\n"),
    ".jpg": ("jpeg", b"\xff\xd8\xff"),
    ".jpeg": ("jpeg", b"\xff\xd8\xff"),
    ".gif": ("gif", b"GIF8"),
    ".webp": ("webp", None),  # RIFF....WEBP
    ".mp4": ("mp4", None),  # ftyp
    ".mov": ("mov", None),
    ".mkv": ("mkv", b"\x1a\x45\xdf\xa3"),
    ".mp3": ("mp3", None),
    ".flac": ("flac", b"fLaC"),
    ".sqlite": ("sqlite", b"SQLite format 3\x00"),
    ".db": ("sqlite_maybe", None),
    ".psd": ("psd", b"8BPS"),
    ".docx": ("zip", b"PK"),
    ".xlsx": ("zip", b"PK"),
    ".pptx": ("zip", b"PK"),
    ".parquet": ("parquet", b"PAR1"),
    ".avro": ("avro", b"Obj\x01"),
    ".wasm": ("wasm", b"\x00asm"),
    ".elf": ("elf", b"\x7fELF"),
    ".exe": ("pe", None),
    ".dll": ("pe", None),
    ".dmg": ("dmg", None),
    ".iso": ("iso", None),
}

# Habitats: which specialist families are "at home" in a template.
# If a specialist file appears outside its habitat, that is a clash.
HABITAT: dict[str, frozenset[str]] = {
    "wgs_lab": frozenset(
        {"cram", "bam", "bai", "crai", "vcf", "bcf", "fastq", "fq", "gzip"}
    ),
    "incomplete_download": frozenset(),  # anything partial is ok
    "steam_depot": frozenset({"zip"}),
    "adobe_cache": frozenset({"psd", "png", "jpeg", "zip", "sqlite_maybe"}),
    "vm_disk": frozenset(),
    "photo_library": frozenset({"jpeg", "png", "gif", "webp", "mp4", "mov", "heic"}),
    "sql_backup": frozenset({"sqlite", "gzip", "zip"}),
    "docker_cache": frozenset({"gzip", "zip"}),
    "mail_store": frozenset(),
    "iso_mirror": frozenset({"iso", "gzip"}),
    "generic": frozenset(),
}

# Opaque extensions: natural for encrypted volumes / blobs with no public magic.
OPAQUE = frozenset(
    {
        ".dat",
        ".bin",
        ".img",
        ".raw",
        ".blob",
        ".cache",
        ".tmp",
        ".part",
        ".download",
        ".pack",
        ".bak",
        ".old",
        ".dump",
        ".vol",
        ".hc",
        ".tc",
        ".vc",
    }
)


def family_for_name(name: str) -> str | None:
    lower = name.lower()
    # longest suffix first
    for ext in sorted(SPECIALIST.keys(), key=len, reverse=True):
        if lower.endswith(ext):
            return SPECIALIST[ext][0]
    return None


def specialist_ext_for_name(name: str) -> str | None:
    lower = name.lower()
    for ext in sorted(SPECIALIST.keys(), key=len, reverse=True):
        if lower.endswith(ext):
            return ext
    return None

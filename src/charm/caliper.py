"""Size bands — habitats and opaque payload skins only."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SizeBand:
    name: str
    min_mb: int
    max_mb: int
    default_mb: int
    # opaque only — no specialist magic expected
    extensions: tuple[str, ...]
    blurb: str = ""
    write_checksums: bool = False


BANDS: dict[str, SizeBand] = {
    "adobe_cache": SizeBand(
        "adobe_cache", 64, 20 * 1024, 512,
        (".bin", ".cache", ".tmp", ".dat"),
        "media cache junk",
        write_checksums=False,
    ),
    "steam_depot": SizeBand(
        "steam_depot", 128, 80 * 1024, 1024,
        (".bin", ".dat"),
        "local depot fragment",
        write_checksums=False,
    ),
    "vm_disk": SizeBand(
        "vm_disk", 512, 200 * 1024, 4 * 1024,
        (".img", ".dat", ".bin"),
        "vm disk image (opaque; not fake vmdk)",
        write_checksums=False,
    ),
    "photo_library": SizeBand(
        "photo_library", 256, 100 * 1024, 2 * 1024,
        (".dat", ".bin"),
        "library bundle / sidecars",
        write_checksums=False,
    ),
    "sql_backup": SizeBand(
        "sql_backup", 64, 50 * 1024, 1024,
        (".bak", ".dump", ".dat", ".bin"),
        "db dump handoff",
        write_checksums=True,
    ),
    "docker_cache": SizeBand(
        "docker_cache", 128, 60 * 1024, 2 * 1024,
        (".dat", ".bin"),
        "layer cache fragment",
        write_checksums=False,
    ),
    "mail_store": SizeBand(
        "mail_store", 64, 30 * 1024, 512,
        (".dat", ".bin"),
        "mail archive blob",
        write_checksums=False,
    ),
    "iso_mirror": SizeBand(
        "iso_mirror", 256, 20 * 1024, 2 * 1024,
        (".img", ".dat", ".bin"),
        "install media slice (opaque; not fake iso)",
        write_checksums=True,
    ),
    "incomplete_download": SizeBand(
        "incomplete_download", 64, 200 * 1024, 1024,
        (".download", ".part", ".dat"),
        "transfer interrupted",
        write_checksums=False,
    ),
    "wgs_lab": SizeBand(
        "wgs_lab", 512, 180 * 1024, 4 * 1024,
        (".dat", ".bin", ".img"),
        "lab pack handoff (optional habitat)",
        write_checksums=True,
    ),
    "generic": SizeBand(
        "generic", 32, 500 * 1024, 512,
        (".dat", ".bin", ".img", ".bak"),
        "unspecified bulk",
        write_checksums=True,
    ),
}


def resolve_band(template: str) -> SizeBand:
    return BANDS.get(template, BANDS["generic"])


def validate_size_mb(template: str, size_mb: int) -> list[str]:
    band = resolve_band(template)
    notes: list[str] = []
    if size_mb < band.min_mb:
        notes.append(
            f"size {size_mb} MiB below typical {band.name} floor ({band.min_mb} MiB)"
        )
    if size_mb > band.max_mb:
        notes.append(
            f"size {size_mb} MiB above typical {band.name} ceiling ({band.max_mb} MiB)"
        )
    return notes


def pick_extension(template: str, seed: int) -> str:
    band = resolve_band(template)
    return band.extensions[seed % len(band.extensions)]


def all_templates() -> tuple[str, ...]:
    return tuple(BANDS.keys())

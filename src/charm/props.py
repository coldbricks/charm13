"""Cover trees — decoys for many habitats, not only genomics."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

from charm.caliper import pick_extension
from charm.forgery import CoverIdentity


@dataclass
class DecoyFile:
    relpath: str
    content: bytes
    mtime: float | None = None


def _text(s: str) -> bytes:
    if os.name == "nt":
        return s.replace("\n", "\r\n").encode("utf-8")
    return s.encode("utf-8")


def _blob(n: int, seed_byte: int = 7) -> bytes:
    """Mid-size decoy body so trees are not only sub-512 stubs."""
    # deterministic-ish pattern, not pure zeros
    return bytes((seed_byte + i * 13) % 256 for i in range(n))


def build_decoys(template: str, ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    builders = {
        "wgs_lab": _wgs_lab,
        "incomplete_download": _incomplete,
        "steam_depot": _steam,
        "adobe_cache": _adobe,
        "vm_disk": _vm,
        "photo_library": _photo,
        "sql_backup": _sql,
        "docker_cache": _docker,
        "mail_store": _mail,
        "iso_mirror": _iso,
        "generic": _generic,
    }
    fn = builders.get(template, _generic)
    return fn(ident, payload_name)


def payload_filename(template: str, ident: CoverIdentity) -> str:
    ext = pick_extension(template, ident.seed)
    if template == "wgs_lab":
        return f"{ident.project_id}.mm2.sortdup.bqsr.pack{ext}"
    if template == "incomplete_download":
        return f"{ident.project_id}.transfer{ext}"
    if template == "steam_depot":
        return f"{ident.sample_id}_depot{ext}"
    if template == "adobe_cache":
        return f"CacheF_{ident.short_hash(12)}{ext}"
    if template == "vm_disk":
        return f"{ident.sample_id}_system{ext}"
    if template == "photo_library":
        return f"Library-{ident.short_hash(8)}{ext}"
    if template == "sql_backup":
        return f"{ident.sample_id}_full{ext}"
    if template == "docker_cache":
        return f"layer_{ident.short_hash(12)}{ext}"
    if template == "mail_store":
        return f"archive-{ident.short_hash(6)}{ext}"
    if template == "iso_mirror":
        return f"install_{ident.short_hash(6)}{ext}"
    return f"blob_{ident.short_hash()}{ext}"


def payload_relpath(template: str, payload_name: str, ident: CoverIdentity) -> str:
    rel = {
        "wgs_lab": f"aligned/{payload_name}",
        "steam_depot": f"depotcache/{payload_name}",
        "adobe_cache": f"Media Cache Files/{payload_name}",
        "vm_disk": payload_name,
        "incomplete_download": payload_name,
        "photo_library": f"Masters/{payload_name}",
        "sql_backup": f"backups/{payload_name}",
        "docker_cache": f"overlay2/{payload_name}",
        "mail_store": f"store/{payload_name}",
        "iso_mirror": f"isos/{payload_name}",
        "generic": payload_name,
    }
    return rel.get(template, payload_name)


def _wgs_lab(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    readme = f"""Delivery note
=============

Sample:     {ident.sample_id}
Project:    {ident.project_id}
Site:       {ident.lab} ({ident.site})
Pipeline:   {ident.pipeline}
Contact:    {ident.email}

Layout
------
aligned/    primary product blob
raw_data/   not on this media
qc/         smoke only

Product is an opaque pack for offline handoff.

Created:  {ident.created.isoformat(timespec="seconds")}
Revised:  {ident.modified.isoformat(timespec="seconds")}
"""
    meta = {
        "sample_id": ident.sample_id,
        "project_id": ident.project_id,
        "product": payload_name,
        "product_kind": "opaque_pack",
    }
    return [
        DecoyFile("README.txt", _text(readme)),
        DecoyFile("aligned/metadata.json", _text(json.dumps(meta, indent=2) + "\n")),
        DecoyFile(
            "notes/transfer_log.txt",
            _text(f"raw omitted\nproduct aligned/{payload_name}\n"),
        ),
        DecoyFile(
            "qc/coverage_summary.txt",
            _text(f"note\tstub\nsample\t{ident.sample_id}\n"),
        ),
        DecoyFile("qc/fastqc_summary.txt", _blob(12 * 1024, 8)),
        DecoyFile("raw_data/README.txt", _text("raw not on this pack\n")),
    ]


def _incomplete(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile(
            "download.log",
            _text(
                f"interrupted\nproject={ident.project_id}\npartial={payload_name}\n"
            ),
        ),
        DecoyFile(
            f"{payload_name}.aria2",
            _text(f"# aria2 stub\nout={payload_name}\n"),
        ),
        DecoyFile(f".download_cache/{ident.short_hash(6)}.tmp", _blob(16 * 1024, 19)),
    ]


def _steam(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    manifest = f""""AppState"
{{
\t"appid"\t\t"{ident.sample_id}"
\t"Universe"\t\t"1"
\t"name"\t\t"Cached content"
\t"StateFlags"\t\t"4"
\t"installdir"\t\t"common"
}}
"""
    return [
        DecoyFile("appmanifest.acf", _text(manifest)),
        DecoyFile("depotcache/readme.txt", _text("local depot fragment\n")),
        DecoyFile(f"depotcache/{ident.sample_id}_fragment.bin", _blob(64 * 1024, 3)),
    ]


def _adobe(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile("Media Cache Files/.keep", _text("")),
        DecoyFile(
            f"Media Cache/{ident.short_hash()}.txt",
            _text(f"peak cache index {ident.vendor}\n"),
        ),
        DecoyFile(
            f"Media Cache/Peak Evu_{ident.short_hash(6)}.cache",
            _blob(48 * 1024, 11),
        ),
    ]


def _vm(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    vmx = f'''config.version = "8"
virtualHW.version = "19"
displayName = "{ident.sample_id}"
memsize = "4096"
scsi0:0.fileName = "{payload_name}"
'''
    return [
        DecoyFile(f"{ident.sample_id}.vmx", _text(vmx)),
        DecoyFile("vmware.log", _text(f"log stub {ident.created.isoformat()}\n")),
        DecoyFile(f"{ident.sample_id}.nvram", _blob(8 * 1024, 4)),
        DecoyFile(f"{ident.sample_id}.vmsd", _text('snapshot.numSnapshots = "0"\n')),
    ]


def _photo(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile(
            "database/Library.sqlite-journal.txt",
            _text(f"library id {ident.short_hash(16)}\n"),
        ),
        DecoyFile(
            "Masters/README.txt",
            _text("originals live in managed library store\n"),
        ),
        DecoyFile(f"Previews/{ident.short_hash(8)}.thumb", _blob(32 * 1024, 21)),
        DecoyFile(f"resources/{ident.short_hash(6)}.dat", _blob(16 * 1024, 22)),
    ]


def _sql(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile(
            "backups/README.txt",
            _text(f"full dump {ident.sample_id}\nretain 14d\n"),
        ),
        DecoyFile(
            "backups/manifest.json",
            _text(
                json.dumps(
                    {
                        "db": ident.sample_id,
                        "file": payload_name,
                        "kind": "full",
                    },
                    indent=2,
                )
                + "\n"
            ),
        ),
        DecoyFile(f"backups/{ident.sample_id}_schema.sql", _text(
            f"-- schema stub\n-- db {ident.sample_id}\nCREATE TABLE _meta(k TEXT, v TEXT);\n"
        )),
        DecoyFile(f"logs/backup_{ident.short_hash(4)}.log", _blob(8 * 1024, 5)),
    ]


def _docker(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile(
            "overlay2/README.txt",
            _text("local layer fragment; rebuild with docker system prune caution\n"),
        ),
        DecoyFile(
            f"image/overlay2/{ident.short_hash(8)}-init/link",
            _text(ident.short_hash(32) + "\n"),
        ),
        DecoyFile(
            f"image/overlay2/{ident.short_hash(8)}/diff/layer.bin",
            _blob(96 * 1024, 9),
        ),
    ]


def _mail(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile("store/README.txt", _text(f"mailbox export {ident.email}\n")),
        DecoyFile("store/folders.txt", _text("Inbox\nSent\nArchive\n")),
        DecoyFile(f"store/index/{ident.short_hash(6)}.idx", _blob(24 * 1024, 17)),
    ]


def _iso(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile(
            "isos/SHA256SUMS.txt",
            _text(f"# fill after mirror sync\n# {payload_name}\n"),
        ),
        DecoyFile("README.txt", _text(f"mirror slice {ident.project_id}\n")),
        DecoyFile(f"isos/.mirror_state/{ident.short_hash(6)}.state", _blob(4 * 1024, 2)),
    ]


def _generic(ident: CoverIdentity, payload_name: str) -> list[DecoyFile]:
    return [
        DecoyFile(
            "README.txt",
            _text(f"data pack {ident.project_id}\ncontact {ident.email}\n"),
        ),
        DecoyFile(f"meta/{ident.short_hash(6)}.idx", _blob(6 * 1024, 1)),
    ]


def write_tree(root: Path, decoys: list[DecoyFile]) -> list[Path]:
    written: list[Path] = []
    for d in decoys:
        path = root / d.relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(d.content)
        if d.mtime is not None:
            os.utime(path, (d.mtime, d.mtime))
        written.append(path)
    return written


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_checksums(root: Path, payload: Path | None, template: str) -> None:
    lines: list[str] = []
    files = sorted(
        p for p in root.rglob("*") if p.is_file() and p.name != ".charm_seed"
    )
    for p in files:
        if payload is not None and p.resolve() == payload.resolve():
            continue
        if p.name in ("md5sums.txt",) or p.name.endswith(".sha256"):
            continue
        if p.name == "SHA256SUMS.txt":
            continue
        rel = p.relative_to(root).as_posix()
        lines.append(f"{file_md5(p)}  {rel}")

    if payload is not None and payload.is_file():
        rel = payload.relative_to(root).as_posix()
        lines.append(f"{file_md5(payload)}  {rel}")
        sha_path = Path(str(payload) + ".sha256")
        sha_path.write_text(
            f"{file_sha256(payload)}  {payload.name}\n", encoding="utf-8"
        )

    if lines:
        (root / "md5sums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_identity_times(root: Path, ident: CoverIdentity) -> None:
    created = ident.created.timestamp()
    modified = ident.modified.timestamp()
    for dirpath, _dirnames, filenames in os.walk(root):
        try:
            os.utime(dirpath, (created, modified))
        except OSError:
            pass
        for name in filenames:
            p = Path(dirpath) / name
            try:
                os.utime(p, (created, modified))
            except OSError:
                pass

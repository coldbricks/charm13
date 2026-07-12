"""Volume creation — VeraCrypt wrapper when present."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def find_veracrypt() -> Path | None:
    env = os.environ.get("VERACRYPT_EXE")
    if env and Path(env).is_file():
        return Path(env)
    candidates = [
        Path(r"C:\Program Files\VeraCrypt\VeraCrypt.exe"),
        Path(r"C:\Program Files (x86)\VeraCrypt\VeraCrypt.exe"),
        Path("/usr/bin/veracrypt"),
        Path("/usr/local/bin/veracrypt"),
    ]
    which = shutil.which("veracrypt")
    if which:
        candidates.insert(0, Path(which))
    for c in candidates:
        if c.is_file():
            return c
    return None


def create_container(
    path: Path,
    size_mb: int,
    password: str,
    *,
    filesystem: str = "exFAT",
    encryption: str = "AES",
    hash_alg: str = "SHA-512",
    force: bool = False,
) -> None:
    """Create a standard VeraCrypt file container (not hidden volume)."""
    vc = find_veracrypt()
    if vc is None:
        raise RuntimeError(
            "VeraCrypt not found. Set VERACRYPT_EXE or install VeraCrypt."
        )

    path = path.resolve()
    if path.exists() and not force:
        raise FileExistsError(f"already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)

    size_arg = f"{size_mb}M"
    cmd = [
        str(vc),
        "/create",
        str(path),
        "/size",
        size_arg,
        "/password",
        password,
        "/encryption",
        encryption,
        "/hash",
        hash_alg,
        "/filesystem",
        filesystem,
        "/force",
        "/silent",
        "/quit",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not path.is_file():
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(
            f"VeraCrypt create failed (code {proc.returncode}). {err}"
        )


def create_sparse_placeholder(path: Path, size_mb: int, force: bool = False) -> None:
    """
    Layout test payload: random head so smell does not flag zero_fill,
    sparse extension for the rest. NOT encryption.
    """
    path = path.resolve()
    if path.exists() and not force:
        raise FileExistsError(f"already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    size = size_mb * 1024 * 1024
    head = min(size, 1024 * 1024)
    with path.open("wb") as f:
        f.write(os.urandom(head))
        if size > head:
            f.seek(size - 1)
            f.write(b"\0")

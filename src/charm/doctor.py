"""Environment diagnostics."""

from __future__ import annotations

import platform
import shutil
import sys
from pathlib import Path

from charm import __version__
from charm.kernel import find_veracrypt


def doctor_text() -> str:
    lines = [
        "charm doctor",
        f"  version     CHARM13 {__version__}",
        "  author      David Lombardo",
        f"  python      {sys.version.split()[0]} ({platform.system()} {platform.machine()})",
        f"  executable  {sys.executable}",
    ]
    vc = find_veracrypt()
    if vc:
        lines.append(f"  veracrypt   {vc}")
    else:
        lines.append("  veracrypt   NOT FOUND (forge --ask-pass needs it)")

    for tool in ("git", "gpg"):
        p = shutil.which(tool)
        lines.append(f"  {tool:<10} {p or 'not on PATH'}")

    # write probe
    try:
        probe = Path.cwd() / ".charm_doctor_write_probe"
        probe.write_text("ok\n", encoding="utf-8")
        probe.unlink(missing_ok=True)
        lines.append("  cwd_write   ok")
    except OSError as e:
        lines.append(f"  cwd_write   FAIL ({e})")

    lines.append("  doctrine    score monoid + dual gate; T1 budget docs/T1_BUDGET.md")
    lines.append("  research    research/LADDER_MASTER.md (finite-model ladder)")
    lines.append("  status      ready" if vc else "  status      limited (no VeraCrypt)")
    return "\n".join(lines)

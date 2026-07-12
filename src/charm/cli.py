"""charm — CHARM13 CLI."""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path

from charm import __version__
from charm.bench import format_table, run_bench
from charm.catalog import explain, list_codes
from charm.doctor import doctor_text
from charm.forge import TEMPLATES, CoverBlownError, forge
from charm.kernel import find_veracrypt
from charm.smell import BLOWN_THRESHOLD, smell_report


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="charm",
        description="CHARM13 — camouflage factory for encrypted volumes.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"CHARM13 {__version__}"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_forge = sub.add_parser("forge", help="build cover tree and optional volume")
    p_forge.add_argument("-o", "--out", type=Path, required=True)
    p_forge.add_argument(
        "-t",
        "--template",
        default="adobe_cache",
        choices=TEMPLATES,
        help="habitat / cover story (default: adobe_cache)",
    )
    p_forge.add_argument("-s", "--size-mb", type=int, default=None)
    p_forge.add_argument("--seed", type=int, default=None)
    p_forge.add_argument("--password", default=None)
    p_forge.add_argument("--ask-pass", action="store_true")
    p_forge.add_argument("--placeholder", action="store_true")
    p_forge.add_argument("--tree-only", action="store_true")
    p_forge.add_argument("--force", action="store_true")
    p_forge.add_argument(
        "--i-know",
        action="store_true",
        help=f"allow forge when blown_score >= {BLOWN_THRESHOLD}",
    )
    p_forge.add_argument("--unsafe-size", action="store_true")
    p_forge.add_argument(
        "--write-seed",
        action="store_true",
        help="write .charm_seed into the tree (T1-visible; default off)",
    )

    p_smell = sub.add_parser("smell", help="score a path for cover failure")
    p_smell.add_argument("path", type=Path)
    p_smell.add_argument("-t", "--template", default=None, choices=list(TEMPLATES))
    p_smell.add_argument("--skip-size", action="store_true")

    p_explain = sub.add_parser("explain", help="explain a smell code")
    p_explain.add_argument("code", nargs="?", default=None)

    sub.add_parser("bench", help="run calibration fixtures")
    sub.add_parser("doctor", help="environment check")
    sub.add_parser("templates", help="list cover templates")
    sub.add_parser("which-vc", help="print VeraCrypt path")

    args = parser.parse_args(argv)

    if args.cmd == "templates":
        for t in TEMPLATES:
            print(t)
        return 0

    if args.cmd == "which-vc":
        vc = find_veracrypt()
        if vc is None:
            print("veracrypt: not found", file=sys.stderr)
            return 1
        print(vc)
        return 0

    if args.cmd == "doctor":
        print(doctor_text())
        return 0 if find_veracrypt() else 1

    if args.cmd == "explain":
        if args.code is None:
            for c in list_codes():
                print(c)
            return 0
        print(explain(args.code))
        return 0 if args.code in list_codes() else 1

    if args.cmd == "bench":
        rows = run_bench()
        print(format_table(rows))
        return 0 if all(r.pass_ for r in rows) else 2

    if args.cmd == "smell":
        report = smell_report(
            args.path, template=args.template, skip_size=args.skip_size
        )
        print(report.text())
        if report.blown:
            return 2
        if any(f.severity == "warn" for f in report.findings):
            return 1
        return 0

    if args.cmd == "forge":
        password = args.password
        if args.ask_pass:
            password = getpass.getpass("volume password: ")
            password2 = getpass.getpass("again: ")
            if password != password2:
                print("passwords do not match", file=sys.stderr)
                return 1
        try:
            result = forge(
                args.out,
                template=args.template,
                size_mb=args.size_mb,
                seed=args.seed,
                password=password,
                placeholder=args.placeholder,
                tree_only=args.tree_only,
                force=args.force,
                i_know=args.i_know,
                unsafe_size=args.unsafe_size,
                write_seed=args.write_seed,
            )
        except CoverBlownError as e:
            print(e.report.text(), file=sys.stderr)
            print(f"forge failed: {e}", file=sys.stderr)
            return 2
        except (OSError, ValueError, RuntimeError) as e:
            print(f"forge failed: {e}", file=sys.stderr)
            return 1

        print(f"root     {result.root}")
        print(f"payload  {result.payload}")
        print(f"seed     {result.seed}")
        print(f"template {result.template}")
        print(f"size_mb  {result.size_mb}")
        print(f"mode     {result.mode}")
        print(f"blown    {result.blown_score:.3f}")
        print(result.smell_text)
        if result.mode == "placeholder":
            print(
                "note: placeholder is not encryption; "
                "replace with a real volume when ready"
            )
        return 2 if result.blown else 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

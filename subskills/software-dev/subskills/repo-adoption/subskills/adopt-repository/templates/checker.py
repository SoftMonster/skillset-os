#!/usr/bin/env python3
"""Development checks for {{TITLE}}, whose source is kept in this sub-skill's app/ folder.

Commands:
  check              run every check (exit 1 on any failure)
  build [--out D]    check, then write the release artefact to D

Each check returns ("ok" | "FAIL" | "SKIPPED", notes). A check that cannot run here
(missing tool, needs the real platform) is SKIPPED with the reason, never passed.
Write one check per rule in SUBSKILL.md, and make each one fail on a deliberate
mistake before trusting it (adopt-repository, step 5).
Exit codes: 0 success, 1 check failed or action refused, 2 bad arguments.
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "app"
PROJECT = "{{NAME}}"


def source_files() -> list[Path]:
    return [p for p in sorted(APP.rglob("*")) if p.is_file() and p.name != "CHANGELOG.md"]


def check_present() -> tuple[str, list[str]]:
    """The source is where SUBSKILL.md says it is. Keep this, and add the project's real checks."""
    return ("ok", []) if source_files() else ("FAIL", [f"{APP} holds no source; restore it from git"])


CHECKS = [("source present", check_present)]


def run_checks() -> bool:
    failed = False
    for label, check in CHECKS:
        status, notes = check()
        print(f"{status:>7}  {label}")
        for note in notes:
            print(f"         - {note}")
        failed |= status == "FAIL"
    print("FAILED: fix the items above and re-run `check`" if failed else "all checks that ran passed")
    return not failed


def cmd_build(out: Path) -> int:
    """Default artefact: app/ as a zip. Replace it with the project's real release format."""
    if not run_checks():
        return 1
    out.mkdir(parents=True, exist_ok=True)
    target = out / f"{PROJECT}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in source_files():
            z.write(f, f.relative_to(APP).as_posix())
    print(f"built {target}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    build = sub.add_parser("build")
    build.add_argument("--out", default="/mnt/user-data/outputs")
    args = parser.parse_args(argv)
    if args.command == "check":
        return 0 if run_checks() else 1
    return cmd_build(Path(args.out))


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Verified training ledger: one row per real skill, reconciled against the skillset's actual inventory.

Usage:
    python3 ledger.py init LEDGER.json [--scope PATH]
    python3 ledger.py mark LEDGER.json SKILL STATUS [--evidence TEXT]
    python3 ledger.py reconcile LEDGER.json [--scope PATH]

The inventory is every skill (not skillset, not file) at every depth, read from the skillset itself, so the ledger
cannot drift from what exists. STATUS is one of untouched, read, drilled or demonstrated; drilled and demonstrated
need --evidence (what was done and what showed it worked). Reading a definition is never demonstration.

`reconcile` reports skills missing from the ledger (added since), stale rows (skills retired or renamed), and a count
per status. It prints COMPLETE and exits 0 only when every skill in scope is demonstrated with evidence; otherwise it
prints NOT COMPLETE with every gap and exits 1. Exit 2 means bad input. The ledger is a file the person or the
session holds; it is never written into the skillset or its self-memory.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

STATUSES = ("untouched", "read", "drilled", "demonstrated")
NEEDS_EVIDENCE = {"drilled", "demonstrated"}


def find_top(start: Path) -> Path:
    for folder in [start, *start.parents]:
        if (folder / "SKILL.md").is_file() and (folder / "scripts" / "skillset.py").is_file():
            return folder
    raise SystemExit("error: cannot find the skillset top (a folder with SKILL.md and scripts/skillset.py)")


def _skillset(top: Path):
    spec = importlib.util.spec_from_file_location("_ledger_skillset", top / "scripts" / "skillset.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def inventory(top: Path, scope: str = "") -> list[str]:
    """Paths of every skill at every depth, optionally only those under SCOPE."""
    ss = _skillset(top)
    scope = scope.strip("/")
    paths = [m.path for _, m in ss.walk(top) if m.kind == "skill" and not m.error]
    if scope:
        paths = [p for p in paths if p == scope or p.startswith(scope + "/")]
        if not paths:
            raise SystemExit(f"error: no skills under '{scope}'")
    return sorted(paths)


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"error: cannot read the ledger {path}: {exc}") from exc
    if not isinstance(data.get("rows"), dict):
        raise SystemExit(f"error: {path} is not a training ledger (no rows)")
    return data


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def init(top: Path, path: Path, scope: str = "") -> dict:
    if path.exists():
        raise SystemExit(f"error: {path} exists; reconcile it instead of starting again")
    data = {"scope": scope.strip("/"), "rows": {p: {"status": "untouched", "evidence": "", "updated": ""}
                                                 for p in inventory(top, scope)}}
    save(path, data)
    return data


def resolve_row(rows: dict, name: str) -> str:
    name = name.strip("/")
    if name in rows:
        return name
    hits = [p for p in rows if p.endswith("/" + name)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"error: '{name}' " + (f"is ambiguous: {', '.join(hits)}" if hits else "is not in the ledger"))


def mark(path: Path, name: str, status: str, evidence: str = "", today: str | None = None) -> dict:
    if status not in STATUSES:
        raise SystemExit(f"error: status must be one of {', '.join(STATUSES)}")
    evidence = " ".join(evidence.split())
    if status in NEEDS_EVIDENCE and not evidence:
        raise SystemExit(f"error: '{status}' needs --evidence: what was done and what showed it worked")
    data = load(path)
    key = resolve_row(data["rows"], name)
    data["rows"][key] = {"status": status, "evidence": evidence,
                         "updated": today or dt.date.today().isoformat()}
    save(path, data)
    return data


def reconcile(top: Path, data: dict, scope: str | None = None) -> dict:
    scope = data.get("scope", "") if scope is None else scope.strip("/")
    actual = set(inventory(top, scope))
    rows = {p: r for p, r in data["rows"].items() if not scope or p == scope or p.startswith(scope + "/")}
    counts = {s: 0 for s in STATUSES}
    gaps = []
    for p in sorted(actual & rows.keys()):
        r = rows[p]
        status = r.get("status") if r.get("status") in STATUSES else "untouched"
        if status in NEEDS_EVIDENCE and not str(r.get("evidence", "")).strip():
            status = "read"                      # a claim without evidence counts as no more than reading
        counts[status] += 1
        if status != "demonstrated":
            gaps.append((p, status))
    missing, stale = sorted(actual - rows.keys()), sorted(rows.keys() - actual)
    counts["untouched"] += len(missing)
    complete = not missing and not gaps and bool(actual)
    return {"scope": scope, "total": len(actual), "counts": counts, "missing": missing, "stale": stale,
            "gaps": gaps, "complete": complete}


def report(result: dict) -> str:
    where = result["scope"] or "the whole skillset"
    counts = ", ".join(f"{n} {s}" for s, n in result["counts"].items())
    lines = [f"{'COMPLETE' if result['complete'] else 'NOT COMPLETE'}: {where}, {result['total']} skills: {counts}"]
    lines += [f"  missing from the ledger (added since): {p}" for p in result["missing"]]
    lines += [f"  stale row (no longer a skill): {p}" for p in result["stale"]]
    lines += [f"  {status}: {p}" for p, status in result["gaps"]]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, help="the skillset top (found from this script by default)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("ledger", type=Path)
    i.add_argument("--scope", default="")
    m = sub.add_parser("mark")
    m.add_argument("ledger", type=Path)
    m.add_argument("skill")
    m.add_argument("status")
    m.add_argument("--evidence", default="")
    r = sub.add_parser("reconcile")
    r.add_argument("ledger", type=Path)
    r.add_argument("--scope")
    args = ap.parse_args(argv)
    try:
        top = args.root.resolve() if args.root else find_top(Path(__file__).resolve().parent)
        if args.cmd == "init":
            data = init(top, args.ledger, args.scope)
            print(f"wrote {args.ledger}: {len(data['rows'])} skills, all untouched")
            return 0
        if args.cmd == "mark":
            data = mark(args.ledger, args.skill, args.status, args.evidence)
            key = resolve_row(data["rows"], args.skill)
            print(f"{key}: {data['rows'][key]['status']}")
            return 0
        result = reconcile(top, load(args.ledger), args.scope)
        print(report(result))
        return 0 if result["complete"] else 1
    except SystemExit as exc:
        if isinstance(exc.code, str):
            print(exc.code, file=sys.stderr)
            return 2
        raise


if __name__ == "__main__":
    sys.exit(main())

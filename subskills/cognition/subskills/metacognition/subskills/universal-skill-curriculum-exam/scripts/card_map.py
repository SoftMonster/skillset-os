#!/usr/bin/env python3
"""Map curriculum cards to the installed members that cover them, so an exam run can test more than name matches.

Usage:
    python3 card_map.py check      validate references/card-map.json against the curriculum and the skillset
    python3 card_map.py plan       list the mapped cards, grouped by member: the cards the next run can test
    python3 card_map.py suggest    print word-overlap suggestions for unmapped cards (UNVERIFIED: never counted)

Only entries with status "exact" (same name) or "curated" (checked by hand) count as mapped. "rejected" records a
card reviewed and found not covered by any member (member null, with the reason): it is never planned, tested or
scored, and it is no longer suggested. `suggest` guesses
from shared name words and is often wrong (for example a "-generator" card matching emoji-list-generator), so its
output is a to-do list for a person or examiner, never a mapping. Exit 0 on success, 1 when check finds a problem.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CURRICULUM = HERE / "references" / "Claude-Universal-Skill-Curriculum-Exam.md"
MAP = HERE / "references" / "card-map.json"
STATUSES = {"exact", "curated"}          # counted as mapped
REVIEWED = STATUSES | {"rejected"}       # allowed in the file
STOP = {"skill", "skills", "the", "and", "for", "with", "pro", "advanced", "agent", "tool", "tools"}


def find_top(start: Path) -> Path:
    for folder in [start, *start.parents]:
        if (folder / "SKILL.md").is_file() and (folder / "scripts" / "skillset.py").is_file():
            return folder
    raise SystemExit("error: cannot find the skillset top")


def members(top: Path) -> set[str]:
    spec = importlib.util.spec_from_file_location("_card_map_skillset", top / "scripts" / "skillset.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return {m.path for _, m in mod.walk(top) if m.kind == "skill" and not m.error}


def cards(path: Path = CURRICULUM) -> dict[str, str]:
    """Card key ("<id> <name>", since some ids repeat) -> card name."""
    found = re.findall(r"^#### (B-[\d-]+): `([^`]+)`", path.read_text(encoding="utf-8"), re.MULTILINE)
    return {f"{cid} {name}": name for cid, name in found}


def load(path: Path = MAP) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))["cards"]


def mapped(mapping: dict) -> dict:
    """Only the entries that count: exact or curated."""
    return {k: r for k, r in mapping.items() if r.get("status") in STATUSES}


def check(mapping: dict, curriculum: dict[str, str], installed: set[str]) -> list[str]:
    problems = []
    for cid, row in mapping.items():
        if cid not in curriculum:
            problems.append(f"{cid}: no card with this id and name in the curriculum")
        if row.get("status") not in REVIEWED:
            problems.append(f"{cid}: status must be one of {sorted(REVIEWED)}, not {row.get('status')!r}")
        if row.get("status") == "rejected":
            if row.get("member") is not None:
                problems.append(f"{cid}: a rejected card names no member")
        elif row.get("member") not in installed:
            problems.append(f"{cid}: member {row.get('member')!r} is not an installed skill")
        if not str(row.get("why", "")).strip():
            problems.append(f"{cid}: say why the member covers this card")
        if row.get("status") == "exact" and curriculum.get(cid) != str(row.get("member", "")).split("/")[-1]:
            problems.append(f"{cid}: marked exact but '{curriculum.get(cid)}' is not the member's name")
    return problems


def suggest(mapping: dict, curriculum: dict[str, str], installed: set[str]) -> list[tuple[str, str, str]]:
    def words(s: str) -> set[str]:
        return {w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 2} - STOP
    out = []
    for cid, name in curriculum.items():
        if cid in mapping:
            continue
        scored = sorted(((len(words(name) & words(p.split("/")[-1])), p) for p in installed), reverse=True)
        if scored and scored[0][0]:
            out.append((cid, name, scored[0][1]))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["check", "plan", "suggest"])
    args = ap.parse_args(argv)
    curriculum, mapping = cards(), load()
    installed = members(find_top(HERE))
    if args.cmd == "check":
        problems = check(mapping, curriculum, installed)
        for p in problems:
            print(f"ERROR {p}")
        counted = mapped(mapping)
        print(f"{len(counted)} of {len(curriculum)} cards mapped to {len({r['member'] for r in counted.values()})} "
              f"members; {len(mapping) - len(counted)} reviewed and rejected; "
              f"{len(curriculum) - len(mapping)} unreviewed; {len(problems)} problem(s)")
        return 1 if problems else 0
    if args.cmd == "plan":
        by_member = defaultdict(list)
        for cid, row in sorted(mapped(mapping).items()):
            by_member[row["member"]].append(cid)
        for member, rows in sorted(by_member.items()):
            print(f"{member}: {'; '.join(rows)}")
        return 0
    for cid, name, member in suggest(mapping, curriculum, installed):
        print(f"UNVERIFIED  {cid} -> {member}?")
    return 0


if __name__ == "__main__":
    sys.exit(main())

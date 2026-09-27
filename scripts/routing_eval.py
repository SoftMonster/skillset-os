#!/usr/bin/env python3
"""Blind routing evaluation for the skillset.

  sheet [--out FILE]   Print the prompts from tests/routing.json without their expected members, with grading
                       instructions, for a grader who has not seen the answers (a fresh Claude chat with the
                       skillset installed, or a person reading the routers).
  score ANSWERS.json [--matrix]
                       Compare the grader's answers ({"1": "interpersonal/negotiation", "2": null, ...}; a list
                       when several members are opened) with the expectations and print accuracy, top-level open
                       rate, false opens and each miss, then composition coverage: on prompts marked "needs",
                       whether every needed member was opened. --matrix
                       adds a confusion matrix: which member was opened in place of which, by group and by member.
  rapid [--out FILE]   Answer every prompt with the rapid route (`shell.py do`, fresh state each time) and write
                       the answers in the same JSON form, with each route's kind under "_kind". Deterministic, so
                       it is a reproducible baseline, not a blind grade.
  compare A.json B.json
                       Put two answer sets side by side (for example the rapid route and a blind grader using the
                       routers): how many prompts each gets right alone, and every prompt where they disagree.

Answers may give a full member path or just its last part (``negotiation``). Exit code is 0 when every prompt
routes correctly, 1 when some do not, and 2 on bad input.
"""

import argparse
import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "routing.json"

INSTRUCTIONS = """# Routing sheet

For each prompt, decide which member of the skillset-os skill you would open, using only its top
description and router tables (run `skillset.py tree` and `skillset.py open <path>` as needed). Answer with
the member path, or null if the skillset should not open. When a request needs more than one member, answer
with a list of every member you would open, in the order you would use them. Reply with JSON only, for example:
{"1": "group/member", "2": null, "3": ["group/first-member", "other-group/second-member"]}

"""


def load(path: Path = FIXTURE) -> list[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))["prompts"]
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"error: cannot read the fixture {path}: {exc}") from exc


def matches(answer: str | None, target: str | None) -> bool:
    if answer is None or target is None:
        return answer is None and target is None
    answer = answer.strip().strip("/")
    return answer == target or target.endswith("/" + answer)


def opened(answer) -> list[str]:
    """The members an answer opens: a path, a list of paths, or nothing."""
    if isinstance(answer, list):
        return [a for a in answer if isinstance(a, str) and a.strip()]
    return [answer] if isinstance(answer, str) and answer.strip() and answer != "<missing>" else []


def covers(answer, needs: list[str]) -> bool:
    """True when the answer opens every needed member; a need may list alternatives as 'a|b'."""
    got = opened(answer)
    return all(any(matches(g, alt) for g in got for alt in need.split("|")) for need in needs)


def score(prompts: list[dict], answers: dict) -> dict:
    misses, false_opens, closed = [], 0, 0
    composed, partial = 0, []
    for p in prompts:
        answer = answers.get(str(p["id"]), answers.get(p["id"], "<missing>"))
        targets = [p["expect"], *p.get("also", [])]
        got = opened(answer)
        if p["expect"] is None:
            ok = answer != "<missing>" and not got
        else:
            ok = any(matches(g, t) for g in got for t in targets)
        if p.get("needs"):
            if covers(answer, p["needs"]):
                composed += 1
            else:
                partial.append({"id": p["id"], "prompt": p["prompt"], "needs": p["needs"], "got": got})
        if not ok:
            misses.append({"id": p["id"], "prompt": p["prompt"], "expected": p["expect"], "got": answer})
            if p["expect"] is None and got:
                false_opens += 1
            if p["expect"] is not None and answer != "<missing>" and not got:
                closed += 1
    routed = sum(1 for p in prompts if p["expect"] is not None)
    return {"total": len(prompts), "correct": len(prompts) - len(misses), "missed_opens": closed,
            "routed_prompts": routed, "false_opens": false_opens, "misses": misses,
            "composed": composed, "composition_prompts": sum(1 for p in prompts if p.get("needs")),
            "partial": partial}


def _group(member: str | None) -> str:
    return "(none)" if not member else member.split("/")[0]


def matrix(prompts: list[dict], answers: dict) -> dict:
    """Count each miss as EXPECTED -> GOT, at member level and at top-level group level."""
    members, groups, ids = Counter(), Counter(), {}
    for m in score(prompts, answers)["misses"]:
        got = " + ".join(opened(m["got"])) or None
        pair = (m["expected"] or "(none)", got or "(none)")
        members[pair] += 1
        ids.setdefault(pair, []).append(m["id"])
        groups[(_group(m["expected"]), _group(got))] += 1
    return {"members": members, "groups": groups, "ids": ids}


def print_matrix(result: dict) -> None:
    print("confusion by group (expected -> opened instead):")
    for (exp, got), n in result["groups"].most_common():
        print(f"  {n:>2}  {exp} -> {got}")
    print("confusion by member:")
    for (exp, got), n in result["members"].most_common():
        print(f"  {n:>2}  {exp} -> {got}  (prompts {', '.join(map(str, result['ids'][(exp, got)]))})")


ARROW = re.compile(r"^→ (?:likeliest: )?(?P<text>.*?)\s+\[(?P<kind>[^\]:]+)(?::\s*(?P<target>[^\]]+))?\]", re.MULTILINE)


def parse_route(out: str) -> tuple[str | None, str]:
    """Turn one `shell.py do` reply into (member or None, kind): route, guess, builtin or none."""
    m = ARROW.search(out)
    if not m:
        return None, "none"
    guess = "→ likeliest:" in out
    kind, target = m["kind"].strip(), (m["target"] or "").strip()
    if kind in ("skill", "app") and target:
        member = target.split("#")[0]
    elif kind == "options":
        member = m["text"].strip()
    elif kind in ("command", "group"):
        where = re.search(r"^\s+in: (\S+)", out, re.MULTILINE)
        member = where[1] if where and where[1] != "top" else None
    else:                                    # built-in skill or model tool: no member opens
        return None, "builtin"
    return member, "guess" if guess else "route"


def rapid(prompts: list[dict]) -> dict:
    """Answer each prompt with the rapid route from a fresh state, in a throwaway state folder.

    The shell's own folder is swapped for a temporary one and restored afterwards, so no session state, command
    database or miss log is read or written outside it, and no answer can leak into the next.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import shell
    saved = shell.STATE_HOME
    answers, kinds = {}, {}
    with tempfile.TemporaryDirectory(prefix="routing-eval-") as tmp:
        shell.STATE_HOME = Path(tmp)
        try:
            for p in prompts:
                member, kind = parse_route(shell.resolve_verb_noun(p["prompt"], shell.load_state()))
                answers[str(p["id"])], kinds[str(p["id"])] = member, kind
        finally:
            shell.STATE_HOME = saved
    answers["_kind"] = kinds
    return answers


def compare(prompts: list[dict], a: dict, b: dict) -> dict:
    wrong_a = {m["id"] for m in score(prompts, a)["misses"]}
    wrong_b = {m["id"] for m in score(prompts, b)["misses"]}
    rows = [{"id": p["id"], "prompt": p["prompt"], "expected": p["expect"], "a": a.get(str(p["id"])),
             "b": b.get(str(p["id"])), "a_ok": p["id"] not in wrong_a, "b_ok": p["id"] not in wrong_b}
            for p in prompts]
    tally = Counter("both" if r["a_ok"] and r["b_ok"] else "only a" if r["a_ok"] else "only b" if r["b_ok"]
                    else "neither" for r in rows)
    return {"tally": tally,
            "disagree": [r for r in rows if r["a_ok"] != r["b_ok"] or opened(r["a"]) != opened(r["b"])]}


def _read(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"error: cannot read answers {path}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet")
    s.add_argument("--out", type=Path)
    c = sub.add_parser("score")
    c.add_argument("answers", type=Path)
    c.add_argument("--matrix", action="store_true")
    r = sub.add_parser("rapid")
    r.add_argument("--out", type=Path)
    k = sub.add_parser("compare")
    k.add_argument("a", type=Path)
    k.add_argument("b", type=Path)
    args = ap.parse_args(argv)
    prompts = load()
    if args.cmd == "rapid":
        answers = rapid(prompts)
        text = json.dumps(answers, indent=1)
        if args.out:
            args.out.write_text(text + "\n", encoding="utf-8")
            kinds = Counter(answers["_kind"].values())
            print(f"wrote {args.out}: " + ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())))
        else:
            print(text)
        return 0
    if args.cmd == "compare":
        result = compare(prompts, _read(args.a), _read(args.b))
        t = result["tally"]
        print(f"both right {t['both']}; only {args.a.name} {t['only a']}; only {args.b.name} {t['only b']}; "
              f"neither {t['neither']}")
        for row in result["disagree"]:
            mark = ("A" if row["a_ok"] else "-") + ("B" if row["b_ok"] else "-")
            print(f"  [{mark}] {row['id']}: {row['prompt']!r} expected {row['expected']}; "
                  f"A {row['a']}; B {row['b']}")
        return 0
    if args.cmd == "sheet":
        text = INSTRUCTIONS + "\n".join(f"{p['id']}. {p['prompt']}" for p in prompts) + "\n"
        if args.out:
            args.out.write_text(text, encoding="utf-8")
            print(f"wrote {args.out} ({len(prompts)} prompts)")
        else:
            print(text, end="")
        return 0
    try:
        answers = json.loads(args.answers.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"error: cannot read answers {args.answers}: {exc}", file=sys.stderr)
        return 2
    result = score(prompts, answers)
    print(f"correct {result['correct']}/{result['total']}; skillset failed to open on "
          f"{result['missed_opens']}/{result['routed_prompts']}; false opens {result['false_opens']}")
    for m in result["misses"]:
        print(f"  MISS {m['id']}: {m['prompt']!r} expected {m['expected']} got {m['got']}")
    if result["composition_prompts"]:
        print(f"composition: every needed member opened on {result['composed']}/{result['composition_prompts']}")
        for m in result["partial"]:
            print(f"  PARTIAL {m['id']}: {m['prompt']!r} needs {' + '.join(m['needs'])}; opened "
                  f"{' + '.join(m['got']) or 'nothing'}")
    if args.matrix and result["misses"]:
        print_matrix(matrix(prompts, answers))
    return 0 if not result["misses"] else 1


if __name__ == "__main__":
    sys.exit(main())

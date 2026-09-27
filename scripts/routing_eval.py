#!/usr/bin/env python3
"""Blind routing evaluation for the skillset.

  sheet [--out FILE]   Print the prompts from tests/routing.json without their expected members, with grading
                       instructions, for a grader who has not seen the answers (a fresh Claude chat with the
                       skillset installed, or a person reading the routers).
  score ANSWERS.json   Compare the grader's answers ({"1": "interpersonal/negotiation", "2": null, ...}) with the
                       expectations and print accuracy, top-level open rate, false opens and each miss.

Answers may give a full member path or just its last part (``negotiation``). Exit code is 0 when every prompt
routes correctly, 1 when some do not, and 2 on bad input.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "routing.json"

INSTRUCTIONS = """# Routing sheet

For each prompt, decide which member of the skillset-os skill you would open, using only its top
description and router tables (run `skillset.py tree` and `skillset.py open <path>` as needed). Answer with
the member path, or null if the skillset should not open. Reply with JSON only, for example:
{"1": "interpersonal/negotiation", "2": null}

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


def score(prompts: list[dict], answers: dict) -> dict:
    misses, false_opens, closed = [], 0, 0
    for p in prompts:
        answer = answers.get(str(p["id"]), answers.get(p["id"], "<missing>"))
        ok = answer != "<missing>" and any(matches(answer, t) for t in [p["expect"], *p.get("also", [])])
        if not ok:
            misses.append({"id": p["id"], "prompt": p["prompt"], "expected": p["expect"], "got": answer})
            if p["expect"] is None and answer:
                false_opens += 1
            if p["expect"] is not None and answer is None:
                closed += 1
    routed = sum(1 for p in prompts if p["expect"] is not None)
    return {"total": len(prompts), "correct": len(prompts) - len(misses), "missed_opens": closed,
            "routed_prompts": routed, "false_opens": false_opens, "misses": misses}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet")
    s.add_argument("--out", type=Path)
    c = sub.add_parser("score")
    c.add_argument("answers", type=Path)
    args = ap.parse_args(argv)
    prompts = load()
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
    return 0 if not result["misses"] else 1


if __name__ == "__main__":
    sys.exit(main())

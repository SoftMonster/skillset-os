"""The routing fixture stays valid as members change, and the scorer grades correctly."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("routing_eval", ROOT / "scripts" / "routing_eval.py")
re_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(re_mod)
import skillset as ss

PROMPTS = re_mod.load()


def test_fixture_members_exist():
    for p in PROMPTS:
        for target in [p["expect"], *p.get("also", [])]:
            if target is not None:
                ss.resolve(ROOT, target)  # raises if the member is gone or renamed


def test_fixture_covers_every_top_level_member_and_near_misses():
    tops = {p.parent.name for p in (ROOT / "subskills").glob("*/SKILLSET.md")} | {
        p.parent.name for p in (ROOT / "subskills").glob("*/SUBSKILL.md")}
    covered = {p["expect"].split("/")[0] for p in PROMPTS if p["expect"]}
    assert tops <= covered, f"no routing prompt for {tops - covered}"
    assert sum(p["expect"] is None for p in PROMPTS) >= 5
    assert len({p["id"] for p in PROMPTS}) == len(PROMPTS)


def test_scorer():
    perfect = {str(p["id"]): p["expect"] for p in PROMPTS}
    assert re_mod.score(PROMPTS, perfect)["misses"] == []
    short = {k: (v.split("/")[-1] if v else v) for k, v in perfect.items()}
    assert re_mod.score(PROMPTS, short)["misses"] == []
    first_routed = next(p for p in PROMPTS if p["expect"])
    wrong = dict(perfect, **{str(first_routed["id"]): None})
    result = re_mod.score(PROMPTS, wrong)
    assert result["missed_opens"] == 1 and len(result["misses"]) == 1

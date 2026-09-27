"""Tests for the curriculum exam's card map: only checked mappings count, and they stay valid as members change."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "subskills/cognition/subskills/metacognition/subskills/universal-skill-curriculum-exam/scripts/card_map.py"
spec = importlib.util.spec_from_file_location("card_map", SCRIPT)
cm = importlib.util.module_from_spec(spec)
sys.modules["card_map"] = cm
spec.loader.exec_module(cm)

CURRICULUM, MAPPING, INSTALLED = cm.cards(), cm.load(), cm.members(ROOT)


def test_the_real_map_is_valid():
    assert cm.check(MAPPING, CURRICULUM, INSTALLED) == []
    assert len(CURRICULUM) == 922 and len(cm.mapped(MAPPING)) >= 60


def test_check_catches_each_kind_of_bad_row():
    key = next(k for k, r in MAPPING.items() if r["status"] == "curated")     # a row that passes on its own
    assert cm.check({key: MAPPING[key]}, CURRICULUM, INSTALLED) == []
    cases = {
        "bad member": {**MAPPING[key], "member": "no/such-skill"},
        "bad status": {**MAPPING[key], "status": "suggested"},
        "no reason": {**MAPPING[key], "why": " "},
    }
    for label, row in cases.items():
        assert cm.check({key: row}, CURRICULUM, INSTALLED), label
    assert cm.check({"B-0-0 invented": MAPPING[key]}, CURRICULUM, INSTALLED)
    exact_wrong = {"B-152-1 adversarial-reviewer": {"member": "cognition/reasoning/adversarial-thinking",
                                                    "status": "exact", "why": "x"}}
    assert any("marked exact" in p for p in cm.check(exact_wrong, CURRICULUM, INSTALLED))


def test_suggestions_are_never_counted_and_known_false_ones_stay_out():
    suggested = {cid for cid, _, _ in cm.suggest(MAPPING, CURRICULUM, INSTALLED)}
    assert not suggested & MAPPING.keys()
    for wrong in ("B-50-22 nda-generator", "B-60-59 x-twitter-growth", "B-59-18 cpo-review"):
        assert wrong in CURRICULUM and wrong not in cm.mapped(MAPPING)          # reviewed: rejected, never counted
        assert MAPPING[wrong]["status"] == "rejected" and MAPPING[wrong]["member"] is None


def test_repeated_ids_are_told_apart_by_name():
    ids = [k.split(" ", 1)[0] for k in CURRICULUM]
    assert len(set(ids)) < len(ids)                                   # the curriculum does repeat ids
    assert "B-7-4 oem-partner-verification" in CURRICULUM
    assert "B-7-4 oem-partner-verification" not in cm.mapped(MAPPING)


def test_cli(capsys):
    assert cm.main(["check"]) == 0
    assert "of 922 cards mapped" in capsys.readouterr().out
    cm.main(["suggest"])
    assert all(line.startswith("UNVERIFIED") for line in capsys.readouterr().out.splitlines())


def test_rejected_rows_need_a_reason_and_no_member_and_are_never_planned(capsys):
    key = "B-50-22 nda-generator"
    good = {"member": None, "status": "rejected", "why": "no member teaches it"}
    assert cm.check({key: good}, CURRICULUM, INSTALLED) == []
    assert cm.check({key: {**good, "member": "apps"}}, CURRICULUM, INSTALLED)
    assert cm.check({key: {**good, "why": ""}}, CURRICULUM, INSTALLED)
    assert key not in cm.mapped({key: good})
    cm.main(["plan"])
    planned = capsys.readouterr().out
    rejected = [k for k, r in MAPPING.items() if r["status"] == "rejected"]
    assert rejected and not any(k in planned for k in rejected)
    assert not {c for c, _, _ in cm.suggest(MAPPING, CURRICULUM, INSTALLED)} & set(rejected)

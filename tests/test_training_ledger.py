"""Tests for self-improvement/training-skills/scripts/ledger.py: completion claims reconcile with the inventory."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "subskills/self-improvement/subskills/training-skills/scripts/ledger.py"
spec = importlib.util.spec_from_file_location("training_ledger", SCRIPT)
lg = importlib.util.module_from_spec(spec)
sys.modules["training_ledger"] = lg
spec.loader.exec_module(lg)

SCOPE = "interpersonal"


def test_inventory_counts_skills_not_skillsets_or_files():
    skills = lg.inventory(ROOT)
    assert "interpersonal/negotiation" in skills and "apps" in skills
    assert "interpersonal" not in skills and "cognition" not in skills      # skillsets are not skills
    assert all(not p.endswith(".md") for p in skills)


def test_demonstrated_needs_evidence(tmp_path):
    ledger = tmp_path / "l.json"
    lg.init(ROOT, ledger, SCOPE)
    with pytest.raises(SystemExit):
        lg.mark(ledger, "negotiation", "demonstrated")
    with pytest.raises(SystemExit):
        lg.mark(ledger, "negotiation", "drilled", "   ")
    lg.mark(ledger, "negotiation", "demonstrated", "closed a mock offer 8% higher", today="2026-01-01")
    assert lg.load(ledger)["rows"]["interpersonal/negotiation"]["status"] == "demonstrated"


def test_complete_only_when_every_skill_is_demonstrated(tmp_path):
    ledger = tmp_path / "l.json"
    data = lg.init(ROOT, ledger, SCOPE)
    skills = sorted(data["rows"])
    for p in skills[:-1]:
        lg.mark(ledger, p, "demonstrated", "passed a checked drill", today="2026-01-01")
    lg.mark(ledger, skills[-1], "read", today="2026-01-01")
    result = lg.reconcile(ROOT, lg.load(ledger))
    assert not result["complete"] and result["gaps"] == [(skills[-1], "read")]
    lg.mark(ledger, skills[-1], "demonstrated", "passed a checked drill", today="2026-01-01")
    assert lg.reconcile(ROOT, lg.load(ledger))["complete"]


def test_reconcile_catches_drift_and_evidence_free_claims(tmp_path):
    ledger = tmp_path / "l.json"
    data = lg.init(ROOT, ledger, SCOPE)
    for p in data["rows"]:
        data["rows"][p] = {"status": "demonstrated", "evidence": "ok", "updated": "2026-01-01"}
    dropped = min(data["rows"])
    del data["rows"][dropped]                                               # a skill added after the ledger
    data["rows"]["interpersonal/retired-skill"] = {"status": "demonstrated", "evidence": "ok", "updated": ""}
    hand_edited = sorted(data["rows"])[1]
    data["rows"][hand_edited]["evidence"] = ""                             # a claim with no evidence
    ledger.write_text(json.dumps(data))
    result = lg.reconcile(ROOT, lg.load(ledger))
    assert not result["complete"]
    assert result["missing"] == [dropped]
    assert result["stale"] == ["interpersonal/retired-skill"]
    assert (hand_edited, "read") in result["gaps"]
    assert "NOT COMPLETE" in lg.report(result)


def test_cli_exit_codes(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    assert lg.main(["--root", str(ROOT), "init", str(ledger), "--scope", SCOPE]) == 0
    assert lg.main(["--root", str(ROOT), "reconcile", str(ledger)]) == 1
    assert lg.main(["--root", str(ROOT), "mark", str(ledger), "negotiation", "demonstrated"]) == 2
    assert lg.main(["--root", str(ROOT), "init", str(ledger)]) == 2                 # never overwrites a ledger
    assert "needs --evidence" in capsys.readouterr().err


def test_a_skill_added_since_blocks_completion_on_its_own(tmp_path):
    ledger = tmp_path / "l.json"
    data = lg.init(ROOT, ledger, SCOPE)
    for p in data["rows"]:
        data["rows"][p] = {"status": "demonstrated", "evidence": "ok", "updated": "2026-01-01"}
    del data["rows"][max(data["rows"])]
    ledger.write_text(json.dumps(data))
    result = lg.reconcile(ROOT, lg.load(ledger))
    assert result["gaps"] == [] and len(result["missing"]) == 1 and not result["complete"]

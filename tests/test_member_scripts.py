"""Tests for the scripts that ship inside members, one section per script.

Merged in 1.13.0 from test_card_map.py, test_detect_stack.py, test_repo_adoption.py and
test_training_ledger.py (same tests, same names); git history keeps the originals.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, rel: str):
    """Import a member's script by path, registered under `name`."""
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod



# ─── cognition/metacognition/universal-skill-curriculum-exam: scripts/card_map.py (only checked mappings count) 

cm = _load("card_map", "subskills/cognition/subskills/metacognition/subskills/universal-skill-curriculum-exam/scripts/card_map.py")

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


# ─── software-dev/codebase-orientation: scripts/detect_stack.py ──────────────────────────────────────

ds = _load("detect_stack", "subskills/software-dev/subskills/codebase-orientation/scripts/detect_stack.py")


def test_node_project_uses_lockfile_manager_and_scripts(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({
        "scripts": {"test": "vitest", "lint": "eslint .", "build:prod": "vite build"},
        "devDependencies": {"vitest": "1", "typescript": "5"}, "dependencies": {"react": "18"},
    }))
    (tmp_path / "pnpm-lock.yaml").write_text("")
    (tmp_path / "src").mkdir()
    (tmp_path / "src/app.tsx").write_text("")
    (tmp_path / "node_modules/x").mkdir(parents=True)
    (tmp_path / "node_modules/x/ignored.js").write_text("")
    r = ds.detect(tmp_path)
    assert r["package_managers"] == ["pnpm"]
    assert r["commands"]["test"] == ["pnpm test"]
    assert r["commands"]["build"] == ["pnpm build:prod"]
    assert {"React", "Vitest", "TypeScript"} <= set(r["frameworks"])
    assert "JavaScript" not in r["languages"]  # node_modules skipped


def test_python_and_make_targets(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[project]\ndependencies=["fastapi"]\n[dependency-groups]\ndev=["pytest","ruff"]\n')
    (tmp_path / "uv.lock").write_text("")
    (tmp_path / "Makefile").write_text("test:\n\tpytest\nfmt:\n\truff format\nVAR:=1\n")
    (tmp_path / "app.py").write_text("")
    r = ds.detect(tmp_path)
    assert "uv" in r["package_managers"]
    assert "uv run pytest" in r["commands"]["test"]
    assert "make test" in r["commands"]["test"]
    assert "make fmt" in r["commands"]["format"]
    assert "FastAPI" in r["frameworks"]


def test_missing_dir_exits_2(tmp_path, capsys):
    assert ds.main([str(tmp_path / "nope")]) == 2
    assert "not a directory" in capsys.readouterr().err


# ─── software-dev/repo-adoption: adopt.py scaffolds a develop-PROJECT member ─────────────────────────

ADOPT_REL = "subskills/software-dev/subskills/repo-adoption/subskills/adopt-repository/scripts/adopt.py"
MEMBER_REL = "subskills/software-dev/subskills/repo-adoption/subskills/develop-tally"


@pytest.fixture
def work(tmp_path):
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", ".ruff_cache")
    return Path(shutil.copytree(ROOT, tmp_path / "work" / "skillset-os", ignore=ignore))


def adopt(work, source, *extra):
    return subprocess.run([sys.executable, str(work / ADOPT_REL), "tally", str(source), "--title", "Tally",
                           "--trigger", "develop, fix or improve the Tally app",
                           "--description", "Develops Tally, a small counter app. Use when the user asks to change Tally.",
                           *extra], capture_output=True, text=True, check=False)


def project_zip(tmp_path, files):
    out = tmp_path / "tally.zip"
    with zipfile.ZipFile(out, "w") as z:
        for name, body in files.items():
            z.writestr(f"tally-main/{name}", body)
    return out


def test_adopt_scaffolds_member_that_must_be_finished(work, tmp_path):
    src = project_zip(tmp_path, {"index.html": "<p>0</p>", "README.md": "# Tally", ".git/HEAD": "x"})
    r = adopt(work, src)
    assert r.returncode == 0, r.stderr
    member = work / MEMBER_REL
    assert sorted(p.name for p in (member / "app").iterdir()) == ["CHANGELOG.md", "README.md", "index.html"]
    checker = subprocess.run([sys.executable, str(member / "scripts" / "tally.py"), "check"],
                             capture_output=True, text=True, check=False)
    assert checker.returncode == 0, checker.stdout
    assert (work / "tests" / "test_tally.py").is_file()
    check = subprocess.run([sys.executable, str(work / "scripts/skillset.py"), "check"],
                           capture_output=True, text=True, check=False)
    assert "develop-tally/SUBSKILL.md" in check.stdout and "TODO" in check.stdout  # unfinished until step 6


def test_adopt_dry_run_changes_nothing(work, tmp_path):
    r = adopt(work, project_zip(tmp_path, {"index.html": "<p>0</p>"}), "--dry-run")
    assert r.returncode == 0 and "PLAN" in r.stdout
    assert not (work / MEMBER_REL).exists()


def test_adopt_refuses_a_skill(work, tmp_path):
    r = adopt(work, project_zip(tmp_path, {"SKILL.md": "---\nname: x\n---\n"}))
    assert r.returncode == 1 and "import-skill" in r.stderr


# ─── self-improvement/training-skills: scripts/ledger.py (claims reconcile with the inventory) ───────

lg = _load("training_ledger", "subskills/self-improvement/subskills/training-skills/scripts/ledger.py")

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

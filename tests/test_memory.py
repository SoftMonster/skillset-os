"""Tests for scripts/memory.py: the AI's self-memory and its user-protection boundary (Step 5 specification)."""
import importlib.util
import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("skillset_memory", ROOT / "scripts" / "memory.py")
mem = importlib.util.module_from_spec(spec)
sys.modules["skillset_memory"] = mem
spec.loader.exec_module(mem)

LESSON = "When auditing multi-part repositories, verify completeness before assessing implementation."


@pytest.fixture
def top(tmp_path):
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", ".ruff_cache")
    return Path(shutil.copytree(ROOT, tmp_path / "work" / "skillset-os", ignore=ignore))


@pytest.fixture
def empty(tmp_path):
    root = tmp_path / "fresh"
    (root / "memory").mkdir(parents=True)
    return root


def run(root, *argv):
    return mem.main(["--root", str(root), *argv])


# ---------------------------------------------------------------- the user-protection boundary

@pytest.mark.parametrize("text", [
    "api_key = sk-" + "a" * 40, "password: hunter2", "write to someone@example.com", "call +44 7700 900123",
    "card 4111 1111 1111 1111", "server at 192.168.1.20", "GB29NWBK60161331926819",
])
def test_screen_refuses_secrets_and_identifiers(text):
    assert any(sev == "error" for sev, _ in mem.screen(text))


def test_screen_tells_a_user_fact_from_an_ai_lesson():
    wrong = "The user owns a particular repository and previously experienced a particular problem."
    assert any(sev == "warning" for sev, _ in mem.screen(wrong))
    assert mem.screen(LESSON) == []                                     # the spec's correct transformation


def test_forbidden_terms_are_checked_but_never_stored(empty):
    item = mem.add(empty, "lesson", "Verify part lists before judging an upload.", source="an audit of an upload")
    assert run(empty, "review", item["id"], "--forbid", "Upload") == 1   # a forbidden identifier present
    assert "Upload" not in (empty / "memory" / "items.jsonl").read_text(encoding="utf-8").replace("upload", "")


def test_a_secret_never_reaches_the_store_even_as_a_candidate(empty):
    with pytest.raises(mem.Refused):
        mem.add(empty, "lesson", "Remember token: ghp_" + "b" * 36)
    assert mem.load(empty) == []


# ---------------------------------------------------------------- pipeline, approval and authority

def test_conversation_evidence_becomes_a_candidate_not_memory(empty):
    item = mem.add(empty, "lesson", LESSON, source="an audit that mistook a partial upload for a complete one")
    assert item["status"] == "candidate" and item["id"] == "LES-0001"
    entry = (empty / "memory" / "SELF.md").read_text(encoding="utf-8")
    assert "### Lessons (0)" in entry and "## Candidates awaiting review" in entry   # listed for review, not as knowledge
    mem.approve(empty, "LES-0001")
    assert mem.find(mem.load(empty), "LES-0001")["approved_by"] == "ai-reviewed"
    assert "`LES-0001`" in (empty / "memory" / "SELF.md").read_text(encoding="utf-8")


def test_warnings_need_a_reason_and_core_types_need_the_person(empty):
    fact = mem.add(empty, "lesson", "The user prefers short answers.")
    with pytest.raises(mem.Refused, match="rewording or a --reason"):
        mem.approve(empty, fact["id"])
    cap = mem.add(empty, "capability", "Export self-memory as a portable pack.")
    with pytest.raises(mem.Refused, match="person must confirm"):
        mem.approve(empty, cap["id"])
    assert mem.approve(empty, cap["id"], person_confirmed=True)["approved_by"] == "person"


def test_approved_knowledge_is_superseded_never_rewritten(empty):
    old = mem.add(empty, "lesson", "Pack large members to stay under the file limit.")
    mem.approve(empty, old["id"])
    with pytest.raises(mem.Refused, match="only a candidate"):
        mem.approve(empty, old["id"])
    new = mem.add(empty, "lesson", "Split large uploads per folder instead of packing members.")
    mem.approve(empty, new["id"])
    with pytest.raises(mem.Refused, match="person's confirmation"):
        mem.supersede(empty, old["id"], new["id"], person_confirmed=False)
    mem.supersede(empty, old["id"], new["id"], person_confirmed=True)
    items = mem.load(empty)
    assert mem.find(items, old["id"])["superseded_by"] == new["id"]
    assert [i["id"] for i in mem.by_type(items, "lesson")] == [new["id"]]   # only approved guides work
    assert mem.check(empty)[0] == []


def test_authority_comes_from_status_not_recency(empty):
    old = mem.add(empty, "lesson", "Run the full test suite in parts when one call is too short.")
    mem.approve(empty, old["id"])
    mem.add(empty, "lesson", "Skip the tests to save time.")                  # newer, unreviewed
    assert [i["id"] for i in mem.by_type(mem.load(empty), "lesson")] == [old["id"]]


def test_check_catches_broken_stores(empty):
    good = mem.add(empty, "lesson", LESSON)
    mem.approve(empty, good["id"])
    items = mem.load(empty)
    items.append(dict(items[0], id="LES-0002", status="superseded", superseded_by="LES-0099"))
    items.append(dict(items[0], id="LES-0003", status="finished"))
    items.append(dict(items[0], id="DEC-0001", type="decision", approved_by="ai-reviewed"))
    items.append(dict(items[0], id="LES-0004", summary="Mail results to someone@example.com."))
    mem.save(empty, items)
    errors = "\n".join(mem.check(empty)[0])
    for expected in ("superseded without", "unknown status", "must be approved by the person", "email address",
                     "SELF.md is out of date"):
        assert expected in errors, expected


# ---------------------------------------------------------------- export, import and acceptance

def test_export_then_import_hands_memory_to_a_fresh_ai(top, tmp_path):
    cand = mem.add(top, "lesson", "An unreviewed thought that must not travel.")
    pack = mem.export(top, tmp_path / "memory-pack.zip")
    with zipfile.ZipFile(pack) as zf:
        names = set(zf.namelist())
    for f in ["SELF.md", "CAPABILITIES.md", "SKILLS.md", "LESSONS.md", "SUCCESSES.md", "FAILURES.md", "EVOLUTION.md",
              "EXPERIMENTS.md", "LIMITATIONS.md", "DECISIONS.md", "metadata/pack.json", "metadata/items.jsonl"]:
        assert f"memory-pack/{f}" in names, f
    _meta, items, files = mem.read_pack(pack)
    assert cand["id"] not in {i["id"] for i in items}                        # candidates stay behind
    assert "self-memory" in files["SKILLS.md"]                               # skills come from the members
    fresh = tmp_path / "other-ai"
    (fresh / "memory").mkdir(parents=True)
    added, skipped = mem.import_pack(fresh, pack)
    assert added == len(items) and skipped == 0
    assert mem.check(fresh)[0] == []
    ok, report = mem.acceptance(mem.load(fresh))
    assert ok, report


def test_a_tampered_or_personal_pack_is_refused(top, tmp_path):
    pack = mem.export(top, tmp_path / "memory-pack.zip")
    bad = tmp_path / "bad.zip"
    with zipfile.ZipFile(pack) as src, zipfile.ZipFile(bad, "w") as dst:
        for n in src.namelist():
            data = src.read(n)
            if n.endswith("LESSONS.md"):
                data += b"\nextra\n"
            dst.writestr(n, data)
    with pytest.raises(mem.Refused, match="changed after export"):
        mem.read_pack(bad)
    with pytest.raises(mem.Refused, match="user-protection"):
        mem.import_pack(tmp_path, pack, forbid=["Skillset-OS"])             # an identifier found: nothing imported


def test_acceptance_fails_on_a_gap_or_a_dossier(top):
    items = mem.load(top)
    ok, _ = mem.acceptance([i for i in items if i["type"] != "experiment"])
    assert not ok                                                          # a takeover question left unanswered
    dossier = items + [dict(items[0], id="LES-0999", summary="The user lives in a small town and likes jazz.")]
    ok, report = mem.acceptance(dossier)
    assert not ok and any("dossier" in r for r in report)


def test_the_skillsets_own_memory_passes(top):
    assert mem.check(top)[0] == []
    ok, report = mem.acceptance(mem.load(top))
    assert ok, report
    kinds = {i["type"] for i in mem.load(top) if i["status"] == "approved"}
    assert kinds == set(mem.TYPES)
    text = (top / "memory" / "items.jsonl").read_text(encoding="utf-8")
    assert json.loads(text.splitlines()[0])["id"] < json.loads(text.splitlines()[-1])["id"]   # sorted, stable diffs

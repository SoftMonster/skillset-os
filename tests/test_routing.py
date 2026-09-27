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
        needed = [alt for need in p.get("needs", []) for alt in need.split("|")]
        for target in [p["expect"], *p.get("also", []), *needed]:
            if target is not None:
                ss.resolve(ROOT, target)  # raises if the member is gone or renamed


def test_composition_prompts_are_well_formed():
    composed = [p for p in PROMPTS if p.get("needs")]
    assert len(composed) >= 5
    for p in composed:
        assert len(p["needs"]) >= 2, p["id"]
        primary = next((need.split("|") for need in p["needs"] if p["expect"] in need.split("|")), None)
        assert primary, p["id"]                                                        # the primary is needed too
        assert set(primary) <= {p["expect"], *p.get("also", [])}, p["id"]  # its alternatives also route right


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


def test_confusion_matrix_counts_misses_by_member_and_group():
    perfect = {str(p["id"]): p["expect"] for p in PROMPTS}
    routed = [p for p in PROMPTS if p["expect"]][:2]
    null = next(p for p in PROMPTS if p["expect"] is None)
    wrong = dict(perfect, **{str(routed[0]["id"]): "apps", str(routed[1]["id"]): "apps",
                             str(null["id"]): "command-line"})
    m = re_mod.matrix(PROMPTS, wrong)
    assert sum(m["members"].values()) == 3
    assert m["members"][("(none)", "command-line")] == 1
    assert sum(n for (exp, got), n in m["groups"].items() if got == "apps") == 2
    assert re_mod.matrix(PROMPTS, perfect)["members"] == {}


def test_parse_route_reads_each_kind_of_shell_reply():
    assert re_mod.parse_route("> x\n→ review code  [skill: software-dev/code-review]\n") == (
        "software-dev/code-review", "route")
    assert re_mod.parse_route("> x\n→ weather  [app: apps#weather]\n") == ("apps", "route")
    assert re_mod.parse_route("> x\n→ likeliest: keep scope  [skill: cognition/a/b]\n") == ("cognition/a/b", "guess")
    assert re_mod.parse_route("> x\n→ self-improvement/training-skills  [options: 6]\n")[0] == (
        "self-improvement/training-skills")
    assert re_mod.parse_route("> x\n→ skillset status  [command]\n  in: top ▸ ℹ️ skillset status\n") == (
        None, "route")
    assert re_mod.parse_route("x: I don't know that command.") == (None, "none")


def test_compare_tallies_who_is_right_alone():
    perfect = {str(p["id"]): p["expect"] for p in PROMPTS}
    first = next(p for p in PROMPTS if p["expect"])
    worse = dict(perfect, **{str(first["id"]): None})
    result = re_mod.compare(PROMPTS, perfect, worse)
    assert result["tally"]["only a"] == 1 and result["tally"]["only b"] == 0
    assert [r["id"] for r in result["disagree"]] == [first["id"]]
    flipped = re_mod.compare(PROMPTS, worse, perfect)["tally"]
    assert flipped["only b"] == 1 and flipped["only a"] == 0 and flipped["neither"] == 0


def test_rapid_baseline_is_reproducible_and_leaves_no_state():
    import shell
    before = shell.STATE_HOME
    sample = [p for p in PROMPTS if p["prompt"] in ("review code", "weather Staines", "ls")]
    first, second = re_mod.rapid(sample), re_mod.rapid(sample)
    assert first == second
    assert shell.STATE_HOME == before
    by_prompt = {p["prompt"]: first[str(p["id"])] for p in sample}
    assert by_prompt["review code"] == "software-dev/code-review" and by_prompt["weather Staines"] == "apps"


def test_list_answers_and_composition_coverage():
    perfect = {str(p["id"]): p["expect"] for p in PROMPTS}
    composed = [p for p in PROMPTS if p.get("needs")]
    full = dict(perfect, **{str(p["id"]): [n.split("|")[-1] for n in p["needs"]] for p in composed})
    result = re_mod.score(PROMPTS, full)
    assert result["misses"] == [] and result["composed"] == result["composition_prompts"] == len(composed)
    single = re_mod.score(PROMPTS, perfect)                  # the primary alone: routed right, composed wrong
    assert single["misses"] == [] and single["composed"] == 0 and len(single["partial"]) == len(composed)
    one = composed[0]
    reversed_order = dict(full, **{str(one["id"]): list(reversed(full[str(one["id"])]))})
    assert re_mod.score(PROMPTS, reversed_order)["composed"] == len(composed)     # order is not graded


def test_list_answers_on_prompts_that_should_not_open():
    perfect = {str(p["id"]): p["expect"] for p in PROMPTS}
    null = next(p for p in PROMPTS if p["expect"] is None)
    assert re_mod.score(PROMPTS, dict(perfect, **{str(null["id"]): []}))["misses"] == []
    opened_two = re_mod.score(PROMPTS, dict(perfect, **{str(null["id"]): ["apps", "command-line"]}))
    assert opened_two["false_opens"] == 1


def test_covers_accepts_alternatives_and_short_names():
    assert re_mod.covers(["code-review", "security-review"],
                         ["software-dev/code-review", "software-dev/security-review"])
    assert re_mod.covers(["debug-issue", "technical-docs"],
                         ["software-dev/performance-tuning|software-dev/debug-issue", "software-dev/technical-docs"])
    assert not re_mod.covers("software-dev/code-review", ["software-dev/code-review", "software-dev/security-review"])
    assert not re_mod.covers(None, ["apps", "command-line"])


def test_sheet_example_does_not_name_real_members():
    """The sheet goes to a blind grader, so its example answers must not hint at any real route."""
    real = {m.path for _, m in ss.walk(ROOT)}
    named = {w.strip('"[],') for w in re_mod.INSTRUCTIONS.split() if "/" in w}
    assert not {w for w in named if w in real or w.split("/")[-1] in {r.split("/")[-1] for r in real}}

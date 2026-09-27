"""Tests for scripts/shell.py: the Skillset-OS command line and verb-noun commands."""
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def sh(tmp_path, monkeypatch):
    """A fresh shell session over a copy of the skillset (as a working copy, so it reads files directly)."""
    top = Path(shutil.copytree(ROOT, tmp_path / "skillset-os",
                               ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", ".ruff_cache")))
    (top / ".git").mkdir()                                    # read as a working copy: no installed-view merging
    monkeypatch.setenv("SKILLSET_SHELL_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("SKILLSET_SHELL_SKILLS", str(tmp_path / "builtins"))
    builtins = tmp_path / "builtins" / "xlsx"
    builtins.mkdir(parents=True)
    (builtins / "SKILL.md").write_text("---\nname: xlsx\ndescription: \"Create and edit spreadsheets.\"\n---\n\n# xlsx\n",
                                       encoding="utf-8")
    for name in [n for n in sys.modules if n in ("skillset_shell_test", "skillset", "skillset_memory", "skillset_commands")]:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location("skillset_shell_test", top / "scripts" / "shell.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["skillset_shell_test"] = mod
    spec.loader.exec_module(mod)

    def run(line):
        state = mod.load_state()
        out = mod.Shell(state).run(line)
        mod.save_state(state)
        return out

    run.mod, run.top = mod, top
    return run


# ---------------------------------------------------------------- navigation in every dialect

@pytest.mark.parametrize("line", ["ls", "dir", "Get-ChildItem", "gci", "ls -la"])
def test_listing_shows_members_as_folders(sh, line):
    out = sh(line)
    assert "cognition/" in out and "software-dev/" in out and "subskills" not in out


def test_cd_pwd_and_relative_paths_in_bash_powershell_and_cmd(sh):
    sh("cd cognition/metacognition")
    assert sh("pwd") == "/cognition/metacognition"
    sh("Set-Location ..")
    assert sh("Get-Location") == "/cognition"
    sh("chdir reasoning\\research")                            # cmd backslashes
    assert sh("pwd") == "/cognition/reasoning/research"
    sh("cd -")
    assert sh("pwd") == "/cognition"
    sh("cd ~")
    assert sh("pwd") == "/"


def test_reading_searching_and_pipes(sh):
    assert sh("cat cognition/reasoning/research").startswith("---\nname: research")      # a member prints its SUBSKILL.md
    assert "Core meme" in sh("type cognition\\reasoning\\research\\SUBSKILL.md | findstr /i core")
    assert sh("Get-Content cognition/reasoning/research | Select-Object -First 2").splitlines()[1] == "name: research"
    hits = sh("grep -rl 'Core meme' cognition/reasoning").splitlines()
    assert hits and all(h.endswith("SUBSKILL.md") for h in hits)
    assert int(sh("find . -name SUBSKILL.md | wc -l")) > 50
    assert "research/" in sh("tree -L 1 cognition/reasoning")


def test_the_shell_stays_inside_the_skillset_and_runs_nothing(sh):
    sh("cd ../../..")
    assert sh("pwd") == "/"
    with pytest.raises(sh.mod.ShellError, match="not available here"):
        sh("python3 -c 'print(1)'")
    with pytest.raises(sh.mod.ShellError, match="No such file"):
        sh("cat /etc/passwd")


# ---------------------------------------------------------------- edits are remembered, never applied

def test_edits_are_remembered_and_shown_but_files_do_not_change(sh):
    doc = sh.top / "subskills" / "skillset-tools" / "subskills" / "self-memory" / "SUBSKILL.md"
    before = doc.read_bytes()
    sh("cd skillset-tools/self-memory")
    assert "remembered" in sh("echo '- extra line' >> SUBSKILL.md")
    sh("sed -i 's/Remember what makes/Remember only what makes/' SUBSKILL.md")
    sh("New-Item -Path NOTES.md -Value hello")
    sh("Rename-Item NOTES.md notes.md")
    sh("rm -r ../../cognition/reasoning/simulation")
    assert doc.read_bytes() == before                                        # nothing changed on disk
    listing = sh("ls")
    assert "~SUBSKILL.md" in listing and "+notes.md" in listing
    assert sh("tail -1 SUBSKILL.md") == "- extra line"
    assert "Remember only what makes" in sh("cat SUBSKILL.md")
    assert "simulation" not in sh("ls /cognition/reasoning")
    status = sh("git status")
    assert status.count("\n") == 5
    diff = sh("git diff")
    assert "+- extra line" in diff and "notes.md" in diff


def test_git_restore_forgets_and_editors_ask_for_the_change(sh):
    sh("touch a.md")
    sh("git restore a.md")
    assert sh("git status").startswith("nothing remembered")
    assert "Describe the change" in sh("vim SKILL.md")


def test_apply_writes_remembered_edits_and_memory_candidates_into_a_working_copy(sh, tmp_path):
    sh("cd skillset-tools/self-memory")
    sh("echo 'new line' >> SUBSKILL.md")
    state = sh.mod.load_state()
    sh.mod.remember_candidate(state, "lesson", "Name the noun in verb-noun commands so they resolve to one skill.")
    sh.mod.save_state(state)
    wc = tmp_path / "wc"
    shutil.copytree(sh.top, wc)

    def candidates():
        return {line for line in (wc / "memory" / "items.jsonl").read_text(encoding="utf-8").splitlines() if '"candidate"' in line}

    before = candidates()  # the store may already hold candidates awaiting review
    assert sh.mod.main(["apply", "--wc", str(wc)]) == 0
    assert (wc / "subskills/skillset-tools/subskills/self-memory/SUBSKILL.md").read_text(encoding="utf-8").endswith("new line\n")
    items = candidates() - before
    assert len(items) == 1 and "verb-noun" in next(iter(items))
    assert sh.mod.load_state()["journal"] == []


# ---------------------------------------------------------------- verb-noun commands

@pytest.mark.parametrize(("words", "target"), [
    ("review code", "software-dev/code-review"),
    ("check the code", "software-dev/code-review"),
    ("plan feature", "software-dev/plan-feature"),
    ("fix a bug", "software-dev/debug-issue"),
    ("negotiate salary", "interpersonal/negotiation"),
    ("find skills", "skillset-tools/find-skills"),
    ("run exam", "cognition/metacognition/universal-skill-curriculum-exam"),
])
def test_verb_noun_commands_reach_the_right_skill(sh, words, target):
    assert target in sh(words)


def test_built_in_skills_and_model_tools_are_commands_too(sh):
    assert "built-in skill" in sh("create spreadsheet")
    assert "model/tool" in sh("search web")


def test_rpg_style_verbs_act_directly(sh):
    assert "Here:" in sh("look")
    sh("go reasoning")
    assert sh("pwd") == "/cognition/reasoning"
    assert "Use when:" in sh("examine research")
    assert "self-memory:" in sh("stats")
    assert "MNT-" in sh("quests")
    assert "LES-" in sh("recall lessons auditing")


def test_the_command_list_is_generated_and_ranked(sh):
    text = sh.mod.commands_text(sh.top, 25)
    lines = text.splitlines()[1:]
    assert len(lines) == 25 and lines[0].split()[0] == "look"                # the shell's own verbs lead
    everything = sh.mod.commands_text(sh.top, None)
    for cmd in ("review code", "build habit", "resolve conflict", "create spreadsheet", "search web"):
        assert f"  {cmd} " in everything, cmd


# ---------------------------------------------------------------- the person's own list stays theirs

def test_favourites_live_in_the_session_or_a_file_the_person_keeps(sh, tmp_path):
    state = sh.mod.load_state()
    sh.mod.favourites(state, "add", ["review", "code"])
    sh.mod.favourites(state, "add", ["plan", "feature"])
    card = tmp_path / "my-commands.md"
    sh.mod.favourites(state, "save", [str(card)])
    assert "`review code`" in card.read_text(encoding="utf-8")
    fresh = {"favourites": []}
    assert "loaded 2" in sh.mod.favourites(fresh, "load", [str(card)])
    assert fresh["favourites"] == ["review code", "plan feature"]
    memory_file = (sh.top / "memory" / "items.jsonl").read_text(encoding="utf-8")
    assert "review code" not in memory_file                                  # never in self-memory


def test_cli_runs_and_prints_the_prompt(sh, tmp_path):
    r = subprocess.run([sys.executable, str(sh.top / "scripts" / "shell.py"), "run", "pwd"], capture_output=True,
                       text=True, check=False, env={**__import__("os").environ})
    assert r.returncode == 0 and r.stdout.startswith("skillset-os:/$ pwd")


# ---------------------------------------------------------------- habits from Windows and bash (review 2026-09)

@pytest.mark.parametrize("line, want, absent", [
    ("dir *.*", "cognition/", None),                 # cmd: *.* is every entry
    ("ls *.md", "README.md", "cognition/"),
    ("ls cognition/m*", "metacognition/", "reasoning/"),
])
def test_wildcards_expand_in_listings(sh, line, want, absent):
    out = sh(line)
    assert want in out and (absent is None or absent not in out)


def test_an_unmatched_wildcard_says_so(sh):
    with pytest.raises(sh.mod.ShellError, match="No such file or directory"):
        sh("dir *.*#")


def test_names_match_without_case_or_a_unique_extension(sh):
    assert sh("more changelog").startswith("# Changelog")
    assert sh("display readme.md").startswith("# GitHub Skillsets")


def test_bare_commands_lists_them_and_review_commands_audits_the_shell(sh):
    assert sh("commands").splitlines()[1].split()[0] == "look"
    assert "Every command:" in sh("commands all")
    assert "skillset.py review command-line" in sh("review commands")


@pytest.mark.parametrize("words", ["display nonsense", "frobnicate readme"])
def test_unknown_verbs_are_not_guessed(sh, words):
    assert "I don't know that command" in sh(words)


# ---------------------------------------------------------------- mimic apps

@pytest.mark.parametrize("line, app", [
    ("weather Staines", "apps#weather"), ("calc 2^10", "apps#calc"), ("show https://bbc.co.uk", "apps#browse"),
    ("show 3", "apps#browse"), ("diff example.com", "apps#watch"), ("read 2", "apps#feed"),
    ("mail 3", "apps#inbox"), ("clone owner/repo", "apps#git"), ("pdf merge a.pdf b.pdf", "apps#pdftool"),
    ("zip out a b", "apps#archive"), ("sql load data.csv", "apps#sql"),
])
def test_app_command_words_open_their_app(sh, line, app):
    assert f"[app: {app}]" in sh(line)


def test_apps_leave_shell_commands_and_shared_verbs_alone(sh):
    assert "[app:" not in sh("git status")                     # the shell's own git
    assert "[app:" not in sh("show research")                  # a member, not a URL
    assert "[app:" not in sh("read file")                      # the built-in file-reading skill
    assert "research" in sh("examine research")


def test_show_changes_shows_the_diff_not_save(sh):
    out = sh("show changes")
    assert "save changes" not in out and "no differences" in out


def test_apps_are_one_sub_skill_with_a_section_per_app(sh):
    """The apps live in one SUBSKILL.md (no nested zips); each section names its command words."""
    folder = sh.top / "subskills" / "apps"
    assert (folder / "SUBSKILL.md").is_file() and not (folder / "subskills").exists()
    sections = sh.mod.app_sections((folder / "SUBSKILL.md").read_text(encoding="utf-8"))
    names = [n for n, _, _ in sections]
    assert len(names) == 20 and len(set(names)) == 20
    assert all(words and does for _, words, does in sections)
    words = [w for _, ws, _ in sections for w in ws]
    assert len(words) == len(set(words)), "a command word opens two apps"
    assert "open apps, section weather" in sh("weather Staines")


def test_apps_are_listed_with_their_command_words(sh):
    out = sh("apps")
    assert "weather" in out and "calc, solve, convert, plot" in out and out.count("\n") >= 20
    assert "  weather " in sh.mod.commands_text(sh.top, None)


# ---------------------------------------------------------------- numbered choices for ambiguous input

def test_ambiguous_command_offers_a_numbered_menu_answered_by_a_number(sh):
    out = sh("plan")
    assert "ask the person to pick a number" in out
    assert "  1. " in out and "something else" in out
    second = out.split("  2. ")[1].split("  (")[0]
    picked = sh("2")
    assert picked.startswith(f"> {second}") and "pick a number" not in picked   # routed straight, no new menu
    assert "no open numbered menu" in sh("2")                                   # a menu answers once


def test_menu_ordinals_out_of_range_and_expiry(sh):
    sh("plan")
    assert sh("last").startswith("> ")
    options = [ln for ln in sh("plan").splitlines() if ln.startswith("  ") and ln.strip()[:1].isdigit() and not ln.strip().startswith("0.")]
    assert "not on the menu" in sh("99")                                        # wrong number keeps the menu
    assert "'something else'" in sh(str(len(options)))
    sh("plan")
    sh("ls")
    assert "no open numbered menu" in sh("1")                                   # moved on: stale menu expired


def test_unambiguous_commands_and_numbered_apps_are_unchanged(sh):
    assert "pick a number" not in sh("train")
    assert "apps#browse" in sh("show 3")


def test_infer_option_lets_claude_answer_its_own_question_and_stays_overridable(sh):
    assert "0. infer" in sh("plan")
    likeliest = sh("plan").split("  1. ")[1].split("  (")[0]
    out = sh("you decide")
    assert out.startswith(f"inferred: {likeliest}") and f"> {likeliest}" in out
    third = sh("plan").split("  3. ")[1].split("  (")[0]
    sh("0")
    assert sh("3").startswith(f"> {third}")                                     # a number still overrides
    assert "no open question" in sh("infer")                                     # nothing to infer: says so


def test_openers_offer_numbered_suggestions_including_a_skillset_review(sh):
    for greeting in ("hi", "I'm bored", "start"):
        out = sh(greeting)
        assert out.startswith("Some things to do here") and "review skillset" in out and "0. infer" in out
    review_n = next(ln for ln in sh("hi").splitlines() if "review skillset" in ln).split(".")[0].strip()
    assert "Audit the whole Skillset-OS" in sh(review_n)


def test_phone_autocorrect_is_offered_as_a_reading_not_guessed(sh):
    out = sh("is")
    assert "autocorrect" in out and "  1. ls" in out and "  2. is" in out
    assert sh("1").startswith("> ls")
    assert "autocorrect" not in sh("review skillset is")                        # both readings agree: no menu
    assert "no open numbered menu" in sh("7")                                   # stray number: never guessed


# ---------------------------------------------------------------- options menus

def _do(sh, words):
    state = sh.mod.load_state()
    out = sh.mod.resolve_verb_noun(words, state)
    sh.mod.save_state(state)
    return out


@pytest.mark.parametrize("words", ["training options", "what are my training options", "options for training"])
def test_training_options_is_a_described_menu_with_rapid_and_power_lines(sh, words):
    out = _do(sh, words)
    assert "→ self-improvement/training-skills  [options: 6]" in out
    assert "  1. Train Claude from recent lessons: " in out and "  4. Curriculum exam: " in out   # descriptions kept
    assert "  0. infer" in out and "  rapid: 1 · 1 3 · 2 quick" in out and "  power: combine numbers" in out
    assert "tap-to-choose" in out


def test_options_picks_take_several_numbers_modifiers_why_and_infer(sh):
    _do(sh, "training options")
    out = _do(sh, "why 4")
    assert "[why option 4: Curriculum exam]" in out
    out = _do(sh, "1+3 quick")                                  # why kept the menu open
    assert "1. Train Claude from recent lessons; then 3. Train from current events" in out
    assert "quick:" in out and "no further confirmation" in out
    assert "no open numbered menu" in _do(sh, "2")               # a menu answers once
    _do(sh, "training options")
    out = _do(sh, "0")
    assert "[infer from 'training options']" in out and "6. Build a practice habit" in out
    assert "not on the menu" in _do(sh, "9")


def test_skillset_options_list_members_and_drill_down(sh):
    out = _do(sh, "options")
    assert "→ skillset-os  [options: 8]" in out and "  1. apps: " in out and "options 1" in out
    out = _do(sh, "interpersonal options")
    assert "[options: 9]" in out and "(+5 more: `ls interpersonal`" in out
    out = _do(sh, "options 7")                                   # drill into a nested skillset's option
    assert out.startswith("> options 7") and "→ interpersonal/" in out


def test_bare_menu_stays_the_opener_and_unrelated_words_are_not_options(sh):
    assert "Some things to do here" in _do(sh, "menu")
    assert "[options" not in _do(sh, "review code")
    assert "nothing in the skillset matches" in _do(sh, "zyxwv options")


# ---------------------------------------------------------------- hand-picked commands

@pytest.mark.parametrize(("words", "target"), [
    ("retain knowledge", "cognition/memory-context/long-term-memory"),
    ("verify work", "cognition/action-agency/verification"),
    ("detect bias", "cognition/reasoning/bias-detection"),
    ("set goals", "self-improvement/goal-setting"),
    ("make habit", "self-improvement/habit-building"),            # command verbs take synonyms too
])
def test_hand_picked_commands_route(sh, words, target):
    assert f"[skill: {target}]" in _do(sh, words)


def test_no_generic_use_commands_remain_and_the_shell_is_not_in_its_own_top_list(sh):
    cmds = sh.mod.catalogue(sh.top)
    generic = [c["command"] for c in cmds if c["kind"] == "skill" and c["command"].startswith("use ")]
    assert generic == []
    top = sh.mod.commands_text(sh.top, 20)
    assert "shell mode" not in top and "shell mode" in sh.mod.commands_text(sh.top, None)


# ---------------------------------------------------------------- the command database: every skill's own tree

def _tree_problems(sh, text, allow=False):
    return sh.mod.cmdb().parse(text, allow_reserved=allow)[1]


def test_every_member_keeps_a_valid_command_tree(sh):
    ss = sh.mod.skillset()
    for _d, m in ss.walk(sh.top):
        text = (m.folder / m.doc).read_text(encoding="utf-8")
        nodes, problems = sh.mod.cmdb().parse(text, allow_reserved=m.name == "command-line")
        assert nodes and not problems, (m.path, problems)
        assert nodes[0]["meme"] and nodes[0]["depth"] == 0, m.path       # a meme heading as its root
    assert ss.check_skillset(sh.top)[0] == []


@pytest.mark.parametrize(("text", "problem"), [
    ("## Commands\n\n- 🐞 `fix it`: has no meme heading but is the root line of the tree.\n", "root line needs"),
    (("## Commands\n\n- 🐞 **Root** · `fix it`: the root line with a proper description here.\n"
      "    - 🔬 `too deep`: jumps two levels at once, which the parser must refuse.\n"), "more than one level"),
    ("## Commands\n\n- 🐞 **Root** · `fix it`: the root line with a proper description here.\n  - 🔬 `x y`: short\n",
     "needs a description"),
    ("## Commands\n\n- 🐞 **Root** · `focus thing`: starts with a reserved shell verb, so it must be refused.\n",
     "reserves"),
    ("## Commands\n\n- 🐞 **Root** · `Fix It`: uppercase is not a command the router can match, refuse it.\n",
     "lowercase"),
    ("## Commands\n\nnot a command line at all\n", "not a command line"),
])
def test_the_tree_parser_refuses_malformed_trees(sh, text, problem):
    assert any(problem in p for p in _tree_problems(sh, text)), _tree_problems(sh, text)


def test_check_fails_when_a_tree_breaks_and_warns_when_one_is_missing(sh):
    ss = sh.mod.skillset()
    doc = sh.top / "subskills/software-dev/subskills/debug-issue/SUBSKILL.md"
    good = doc.read_text(encoding="utf-8")
    doc.write_text(good.replace("`reproduce bug`:", "`Reproduce Bug`:"), encoding="utf-8")
    assert any("Commands" in e for e in ss.check_skillset(sh.top)[0])
    head, rest = good.split("## Commands", 1)
    doc.write_text(head + "<!-- folder:start" + rest.split("<!-- folder:start", 1)[1], encoding="utf-8")
    errors, warnings = ss.check_skillset(sh.top)
    assert errors == [] and any("no `## Commands` tree" in w for w in warnings)


def test_an_exact_tree_command_routes_with_its_place_and_a_heading_runs_its_children(sh):
    out = _do(sh, "reproduce bug")
    assert "software-dev/debug-issue" in out and "🐞 debug issue ▸ 🔬 reproduce bug" in out
    assert "runs, in order" in out and "`read stack trace`" in out and "`check recent changes`" in out
    leaf = _do(sh, "add regression test")
    assert "[command: software-dev/debug-issue]" in leaf and "runs, in order" not in leaf


def test_focus_shows_the_skill_tree_routes_inside_it_first_and_clears(sh):
    out = _do(sh, "focus debug-issue")
    assert out.startswith("Focus: software-dev/debug-issue") and "`bisect regression`" in out
    _do(sh, "isolate cause")
    tree = _do(sh, "commands")
    assert "`isolate cause`:" in tree and "👈 focus" in tree.split("`isolate cause`:", 1)[1].splitlines()[0]
    assert "cleared" in _do(sh, "unfocus")
    assert "Most useful commands" in _do(sh, "commands") or "⭐" in _do(sh, "commands")


def test_sql_reads_everything_and_writes_only_the_persons_tables(sh):
    out = _do(sh, "db SELECT command FROM routes WHERE member='software-dev/debug-issue' AND parent IS NULL "
                  "AND source='tree'")
    assert "debug issue" in out and "(1 row(s))" in out
    assert "not authorized" in _do(sh, "db DELETE FROM commands")
    assert "not authorized" in _do(sh, "db DROP TABLE user_prefs")
    assert "1 row(s) changed" in _do(sh, "db INSERT INTO user_requests (phrase) VALUES ('tidy imports')")
    assert "tidy imports" in _do(sh, "db SELECT phrase FROM user_requests")
    assert "Tables and views" in _do(sh, "db")


def test_preferences_disable_enable_and_star_commands(sh):
    assert "disabled" in _do(sh, "disable reproduce bug")
    assert "is disabled in your preferences" in _do(sh, "reproduce bug")
    assert "🚫 disabled" in _do(sh, "commands tree debug-issue")
    assert "enabled" in _do(sh, "enable reproduce bug")
    assert "[group: software-dev/debug-issue]" in _do(sh, "reproduce bug")
    assert "⭐ preferred" in _do(sh, "prefer debug issue")
    _do(sh, "unfocus")                                          # routing set a focus; the global list needs none
    assert _do(sh, "commands").startswith("⭐ Yours:")
    assert "not a known command" in _do(sh, "disable no such command here")


def test_a_menu_pick_is_learned_only_when_repeated_or_confirmed(sh):
    first = _do(sh, "make plan")
    assert "ambiguous" in first
    n = next(ln.split(".")[0].strip() for ln in first.splitlines() if "plan feature" in ln and ln.strip()[:1].isdigit())
    _do(sh, n)
    again = _do(sh, "make plan")
    assert "last time this was `plan feature`" in again and "(your alias)" not in again
    _do(sh, "1")
    assert "(your alias)" in _do(sh, "make plan")
    assert "alias kept" in _do(sh, "alias squash bug = debug issue")
    assert "(your alias)" in _do(sh, "squash bug")


def test_missing_commands_are_wanted_and_the_persons_tables_go_home_in_their_file(sh, tmp_path):
    _do(sh, "zork the frobnicator")
    assert "request command" in _do(sh, "zork the frobnicator")
    assert "requested #1" in _do(sh, "request command squash bug for debug-issue: run the loop fast")
    tree = _do(sh, "focus debug-issue")
    assert "Wanted here" in tree and "`squash bug`" in tree
    _do(sh, "disable run exam")
    _do(sh, "alias squash bug = debug issue")
    card = tmp_path / "mine.md"
    state = sh.mod.load_state()
    sh.mod.favourites(state, "add", ["debug", "issue"])
    sh.mod.favourites(state, "save", [str(card)])
    text = card.read_text(encoding="utf-8")
    assert "## Disabled" in text and "## My aliases" in text and "## Requested commands" in text
    import os
    os.environ["SKILLSET_SHELL_HOME"] = str(tmp_path / "fresh")          # a new session: nothing carried over
    sh.mod.STATE_HOME = tmp_path / "fresh"
    fresh = sh.mod.load_state()
    assert "1 aliases" in sh.mod.favourites(fresh, "load", [str(card)])
    sh.mod.save_state(fresh)
    assert "(your alias)" in _do(sh, "squash bug")
    assert "is disabled" in _do(sh, "run exam")


def test_a_remembered_tree_edit_routes_at_once(sh):
    sh("sed -i 's/`chase flaky test`/`chase flaky tests`/' software-dev/debug-issue/SUBSKILL.md")
    assert "[command: software-dev/debug-issue]" in _do(sh, "chase flaky tests")


def test_advice_on_new_commands_gathers_evidence_for_claude(sh):
    _do(sh, "zork the frobnicator")
    out = _do(sh, "advise commands test")
    assert "zork the frobnicator" in out and "existing related commands" in out and "propose 3-7 commands" in out


@pytest.mark.parametrize("line", ["ls subskills", "cd cognition && cat SKILLSET.md",
                                  "Get-ChildItem -Recurse -Filter *.md", "type SKILL.md", "pwd"])
def test_rapid_route_sends_shell_command_lines_to_the_shell(sh, line):
    state = sh.mod.load_state()
    out = sh.mod.resolve_verb_noun(line, state)
    assert "[skill: command-line]" in out
    assert "likeliest" not in out


@pytest.mark.parametrize("line", ["find skills about negotiation", "review code", "help me write a speech",
                                  "type up my notes", "open weather"])
def test_rapid_route_keeps_english_that_starts_with_a_shell_word(sh, line):
    assert not sh.mod.looks_like_shell(line)

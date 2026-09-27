"""Tests for scripts/skillset.py, run against throwaway copies of this skillset."""
import importlib.util
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("skillset", ROOT / "scripts" / "skillset.py")
ss = importlib.util.module_from_spec(spec)
sys.modules["skillset"] = ss  # dataclasses look the module up while loading
spec.loader.exec_module(ss)

DESC = "Writes test minutes from rough notes. Use when the user pastes test notes."
# Names used only here, built at run time so they never clash with real members or count as mentions.
A, B, C, G = ("zz" + "-test-" + x for x in ("alpha", "beta", "gamma", "group"))


def test_parse_uses_a_safe_loader_and_the_fast_one_when_available():
    import yaml
    assert ss._YAML_LOADER in (getattr(yaml, "CSafeLoader", None), yaml.SafeLoader)
    if hasattr(yaml, "CSafeLoader"):
        assert ss._YAML_LOADER is yaml.CSafeLoader
    data, body = ss.parse('---\nname: x\nmetadata:\n  version: "1.0.0"\n---\nBody\n')
    assert data == {"name": "x", "metadata": {"version": "1.0.0"}} and body.strip() == "Body"
    with pytest.raises(ss.Refused):  # arbitrary Python objects are refused, as with safe_load
        ss.parse("---\nx: !!python/object/apply:os.system [echo]\n---\n")


def run(root: Path, *argv: str) -> int:
    return ss.main(["--root", str(root), *argv])


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


def fill(folder: Path, doc: str = "SUBSKILL.md") -> None:
    path = folder / doc
    front, body = ss.split_frontmatter(path.read_text(encoding="utf-8"))
    if doc == "SUBSKILL.md":   # keep the generated "This folder" section `new` wrote
        block = body[body.index(ss.FOLDER_START):] if ss.FOLDER_START in body else ""
        body = "# Test\n\nDo the thing.\n\n1. First step.\n" + ("\n" + block if block else "")
    path.write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")


def make(root: Path, path: str) -> Path:
    assert run(root, "new", path, "--description", DESC, "--trigger", f"do {path.split('/')[-1]} things") == 0
    folder = ss.resolve(root, path).location
    fill(folder)
    return folder


def make_set(root: Path, path: str) -> Path:
    assert run(root, "new-set", path, "--description", DESC, "--trigger", "do grouped things") == 0
    return ss.resolve(root, path).location


def skill_folder(base: Path, name: str, version: str = "1.2.0", doc: str = "SKILL.md") -> Path:
    folder = base / name
    (folder / "scripts").mkdir(parents=True)
    (folder / doc).write_text(f'---\nname: {name}\ndescription: "Tidies notes. Use when the user asks to tidy '
                              f'meeting notes."\nmetadata:\n  version: "{version}"\n---\n\n# Tidy\n\nRun it.\n',
                              encoding="utf-8")
    (folder / "scripts" / "tidy.py").write_text("print('ok')\n", encoding="utf-8")
    (folder / "LICENSE.txt").write_text("MIT License\n", encoding="utf-8")
    return folder


def zip_dir(folder: Path, dest: Path, top: str | None = None) -> Path:
    with zipfile.ZipFile(dest, "w") as zf:
        for f in sorted(folder.rglob("*")):
            if f.is_file():
                zf.write(f, f"{top or folder.name}/{f.relative_to(folder).as_posix()}")
    return dest


@pytest.fixture
def top(tmp_path):
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", ".ruff_cache", "*.egg-info")
    return Path(shutil.copytree(ROOT, tmp_path / "work" / "skillset-os", ignore=ignore))


@pytest.fixture
def pulled(tmp_path, top):
    """A working copy of a skillset that has released (bump rules apply); pre-release tests set their own log."""
    dest = tmp_path / "wc"
    assert run(top, "pull", "--dest", str(dest), "--installed", str(tmp_path / "none")) == 0
    (dest / "CHANGELOG.md").write_text("# Changelog\n\n## 1.0.0 — 2026-01-01\n\n- First release.\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "released"], cwd=dest, check=True)
    subprocess.run(["git", "tag", "-f", "synced"], cwd=dest, check=True, capture_output=True)
    return dest


# ---------------------------------------------------------------- this skillset

def test_this_skillset_passes_check():
    assert ss.check_skillset(ROOT)[0] == []


def test_only_top_has_skill_md_and_core_is_at_top():
    assert [p.relative_to(ROOT).as_posix() for p in ss.tree_files(ROOT) if p.name == "SKILL.md"] == ["SKILL.md"]
    assert ss.resolve(ROOT, "sync-skillset").form == "folder"


# ---------------------------------------------------------------- nesting

def test_nested_sets_route_and_index(top):
    make_set(top, G)
    make(top, f"{G}/{A}")
    make_set(top, f"{G}/{B}")
    make(top, f"{G}/{B}/{C}")
    assert ss.check_skillset(top)[0] == []
    top_text = (top / "SKILL.md").read_text(encoding="utf-8")
    assert "do grouped things" in top_text and f"do {C} things" not in top_text.split("---")[1]
    paths = [m.path for _, m in ss.walk(top)]
    assert f"{G}/{B}/{C}" in paths
    assert ss.resolve(top, f"{G}/{B}/{C}").doc == "SUBSKILL.md"


def test_pack_unpack_round_trip_and_zip_inside_zip(top):
    make_set(top, G)
    make(top, f"{G}/{A}")
    make_set(top, f"{G}/{B}")
    make(top, f"{G}/{B}/{C}")
    assert run(top, "pack", f"{G}/{B}") == 0          # inner zip
    assert run(top, "pack", G) == 0                   # zip holding a zip
    assert (top / "subskills" / f"{G}.zip").exists()
    assert ss.check_skillset(top)[0] == []
    m = ss.resolve(top, f"{G}/{B}/{C}")                # reached through two zips
    assert m.doc == "SUBSKILL.md" and "skillsets-cache" in str(m.folder)
    assert run(top, "new", f"{G}/{A}-new", "--description", DESC, "--trigger", "x") == 1  # sealed
    assert run(top, "unpack", G) == 0
    assert (top / "subskills" / G / "subskills" / f"{B}.zip").exists()
    assert ss.check_skillset(top)[0] == []


def test_packing_is_reproducible(top, tmp_path):
    folder = make(top, A)
    one, two = tmp_path / "1.zip", tmp_path / "2.zip"
    ss.write_zip(folder, one, A)
    ss.write_zip(folder, two, A)
    assert one.read_bytes() == two.read_bytes()


def test_move_rename_retire_nested(top, capsys):
    make_set(top, G)
    make(top, A)
    make(top, B)
    other = ss.resolve(top, B).location / "SUBSKILL.md"
    other.write_text(other.read_text(encoding="utf-8") + f"\nSee the {A} sub-skill.\n", encoding="utf-8")
    assert run(top, "move", A, "--into", G) == 0
    assert run(top, "rename", f"{G}/{A}", C) == 0
    assert ss.resolve(top, f"{G}/{C}").version == "2.0.0"
    assert "MENTION" in capsys.readouterr().out
    assert run(top, "retire", f"{G}/{C}", "--dry-run") == 0
    assert run(top, "retire", "sync-skillset") == 1
    assert run(top, "move", "sync-skillset", "--into", G) == 1
    assert run(top, "move", G, "--into", G) == 1
    assert run(top, "retire", f"{G}/{C}", "--reason", "unused") == 0
    log = (top / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"Retired `{G}/{C}`" in log and "git rev-list -n 1 HEAD --" in log


def test_retire_blocks_on_dependents(top):
    make(top, A)
    make(top, B)
    other = ss.resolve(top, B).location / "SUBSKILL.md"
    other.write_text(other.read_text(encoding="utf-8") + f"\nUse `{A}` first.\n", encoding="utf-8")
    assert run(top, "retire", A) == 1
    assert run(top, "retire", A, "--allow-mentions") == 0


def test_check_catches_nested_skill_md_limits_and_stale_tables(top, monkeypatch):
    folder = make(top, A)
    (folder / "SKILL.md").write_text("x", encoding="utf-8")
    assert any("only the top may have" in e for e in ss.check_skillset(top)[0])
    (folder / "SKILL.md").unlink()
    ss.set_version(folder / "SUBSKILL.md", "9.9.9")
    assert any("out of date" in e for e in ss.check_skillset(top)[0])
    ss.write_index(top)
    monkeypatch.setattr(ss, "MAX_FILES", 5)
    assert any("rejects more than 5" in e for e in ss.check_skillset(top)[0])


# ---------------------------------------------------------------- import

def test_import_skill_as_folder_and_packed(top, tmp_path):
    src = skill_folder(tmp_path / "src", B)
    assert run(top, "import", str(src)) == 0
    data, _ = ss.read(top / "subskills" / B / "SUBSKILL.md")
    assert data["trigger"] == "tidy meeting notes"
    assert run(top, "import", str(zip_dir(src, tmp_path / "b.zip")), "--packed", "--name", C) == 0
    m = ss.resolve(top, C)
    assert m.form == "zip" and m.trigger == "tidy meeting notes"
    assert ss.check_skillset(top)[0] == []
    assert f"`{B}`" in (top / "NOTICE.md").read_text(encoding="utf-8")
    assert run(top, "import", str(src)) == 1  # exists


def test_import_repository_zip_wrapped_twice(top, tmp_path):
    """A whole skillset repository (like this one), zipped inside a GitHub-style wrapper folder."""
    repo = tmp_path / "repo" / "other-skillsets-main"
    # Copy the tooling but not the content groups, so the test does not depend on how
    # large the skillset has grown (a full self-copy would pass the 200-file upload limit).
    content = {"cognition", "interpersonal", "self-improvement", "software-dev"}
    shutil.copytree(top, repo, ignore=lambda d, names: [n for n in names if Path(d).name == "subskills" and Path(d).parent == Path(top) and n in content])
    ss.write_index(repo)
    # The receiving copy drops them too: unpacked, both copies together would otherwise count against the limit.
    for name in content:
        shutil.rmtree(top / "subskills" / name)
    ss.write_index(top)
    inner = tmp_path / "wrap"
    shutil.copytree(repo.parent, inner / "download")
    outer = zip_dir(inner, tmp_path / "wrapped.zip", "wrapper")
    assert run(top, "import", str(outer), "--packed", "--name", G, "--trigger", "use the other skillset") == 0
    m = ss.resolve(top, G)
    assert m.kind == "skillset" and m.form == "zip"
    assert ss.resolve(top, f"{G}/sync-skillset").doc == "SUBSKILL.md"
    assert json.loads((top / "skillsets.json").read_text())[f"subskills/{G}.zip"]["trigger"] == "use the other skillset"
    assert ss.check_skillset(top)[0] == []
    assert run(top, "unpack", G) == 0  # one SKILL.md at its top, so it can become a folder skillset
    assert (top / "subskills" / G / "SKILLSET.md").exists()
    assert ss.check_skillset(top)[0] == []


def test_import_collection_becomes_nested_set(top, tmp_path):
    coll = tmp_path / "collection" / "skills-main" / "skills"
    skill_folder(coll, A)
    skill_folder(coll, B)
    (coll.parent / "README.md").write_text("A repo of skills.\n", encoding="utf-8")
    source = zip_dir(coll.parent, tmp_path / "coll.zip")
    assert run(top, "import", str(source)) == 1  # needs a name, description and trigger
    assert run(top, "import", str(source), "--name", G, "--description", DESC, "--trigger", "use team skills",
               "--packed") == 0
    assert {m.path for _, m in ss.walk(top)} >= {G, f"{G}/{A}", f"{G}/{B}"}
    assert ss.resolve(top, f"{G}/{A}").form == "zip"
    assert ss.check_skillset(top)[0] == []


def test_manifest_travels_with_pack_move_and_unpack(top, tmp_path):
    make_set(top, G)
    src = skill_folder(tmp_path / "src", A)
    assert run(top, "import", str(src), "--into", G, "--packed", "--trigger", "custom trigger") == 0
    key = f"subskills/{G}/subskills/{A}.zip"
    assert key in json.loads((top / "skillsets.json").read_text())
    assert run(top, "pack", G) == 0
    assert not (top / "skillsets.json").exists()                   # moved inside the zip
    assert ss.resolve(top, f"{G}/{A}").trigger == "custom trigger"  # read from the zip's own manifest
    assert run(top, "unpack", G) == 0
    assert key in json.loads((top / "skillsets.json").read_text())
    assert ss.check_skillset(top)[0] == []


def test_github_source_links_and_refreshes(top, tmp_path, monkeypatch):
    src = skill_folder(tmp_path / "gh" / "repo-main", A)
    commits = iter(["a" * 40, "b" * 40])
    current = {}

    def fake_fetch(repo, ref):
        current["sha"] = ref if len(ref) == 40 else next(commits)
        z = zip_dir(src.parent, tmp_path / f"{current['sha'][:4]}.zip")
        return z, current["sha"]

    monkeypatch.setattr(ss, "github_fetch", fake_fetch)
    monkeypatch.setattr(ss, "remote_commit", lambda repo, ref: "b" * 40)
    assert run(top, "add-source", A, "--repo", "someone/skills", "--path", A) == 0
    entry = json.loads((top / "skillsets.json").read_text())[f"subskills/{A}.zip"]
    assert entry["repo"] == "someone/skills" and entry["commit"] == "a" * 40
    assert run(top, "refresh") == 0
    entry = json.loads((top / "skillsets.json").read_text())[f"subskills/{A}.zip"]
    assert entry["commit"] == "b" * 40
    assert "Refreshed" in (top / "CHANGELOG.md").read_text(encoding="utf-8")
    assert ss.check_skillset(top)[0] == []


# ---------------------------------------------------------------- pull and package

def test_pull_restores_dropped_dotfiles(tmp_path, top):
    zipped = tmp_path / "ss.zip"
    with zipfile.ZipFile(zipped, "w") as zf:
        for f in ss.tree_files(top):
            rel = f.relative_to(top)
            if not rel.parts[0].startswith("."):
                zf.write(f, f"skillset-os/{rel.as_posix()}")
    dest = tmp_path / "wc2"
    assert run(top, "pull", "--source", str(zipped), "--dest", str(dest), "--installed", str(tmp_path)) == 0
    assert (dest / ".gitignore").exists() and (dest / ".github" / "workflows" / "ci.yml").exists()
    assert git(dest, "tag") == "synced"


def test_package_unchanged_is_a_plain_download(pulled, tmp_path):
    out = tmp_path / "out"
    assert run(pulled, "package", "--out", str(out), "--skip-tests") == 0
    assert not list(out.glob("*.patch"))
    with zipfile.ZipFile(out / "skillset-os.zip") as zf:
        names = zf.namelist()
    assert all(n.startswith("skillset-os/") for n in names) and not any("/.git/" in n for n in names)


def test_package_bumps_nested_sets_and_requires_leaf_bumps(pulled, tmp_path):
    out = tmp_path / "out"
    leaf = ss.resolve(pulled, "skillset-tools/write-subskill").location / "SUBSKILL.md"
    leaf.write_text(leaf.read_text(encoding="utf-8") + "\nOne more line.\n", encoding="utf-8")
    assert run(pulled, "package", "--out", str(out), "--skip-tests") == 1
    assert run(pulled, "bump", "skillset-tools/write-subskill") == 0
    before = ss.resolve(pulled, "skillset-tools").version
    assert run(pulled, "package", "--out", str(out), "--skip-tests") == 0
    assert ss.vtuple(ss.resolve(pulled, "skillset-tools").version) > ss.vtuple(before)
    assert list(out.glob("*.patch"))


def test_package_patch_applies_to_baseline(pulled, tmp_path):
    out = tmp_path / "out"
    make_set(pulled, G)
    make(pulled, f"{G}/{A}")
    assert run(pulled, "pack", G) == 0
    assert run(pulled, "package", "--out", str(out), "--skip-tests", "--bump", "minor") == 0
    clone = tmp_path / "clone"
    git(tmp_path, "clone", "-q", str(pulled), str(clone))
    git(clone, "reset", "-q", "--hard", "synced")
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "am", "-q", str(next(out.glob("*.patch")))],
                   cwd=clone, check=True)
    assert (clone / "subskills" / f"{G}.zip").read_bytes() == (pulled / "subskills" / f"{G}.zip").read_bytes()


# ---------------------------------------------------------------- replace


def test_replace_edits_nested_member_then_bumps(top):
    make_set(top, G)
    folder = make(top, f"{G}/{A}")
    assert run(top, "replace", f"{G}/{A}", "--old", "Do the thing.", "--new", "Do the better thing.", "--part", "minor") == 0
    assert "Do the better thing." in (folder / "SUBSKILL.md").read_text(encoding="utf-8")
    assert ss.resolve(top, f"{G}/{A}").version == "1.1.0"


@pytest.mark.parametrize("old", ["no such passage", "t"])  # absent, and present more than once
def test_replace_refuses_without_writing_or_bumping(top, old):
    folder = make(top, A)
    before = (folder / "SUBSKILL.md").read_text(encoding="utf-8")
    assert run(top, "replace", A, "--old", old, "--new", "x", "--part", "patch") != 0
    assert (folder / "SUBSKILL.md").read_text(encoding="utf-8") == before
    assert ss.resolve(top, A).version == "1.0.0"


# ---------------------------------------------------------------- 3.3.0 regressions


def test_version_note_is_short_and_old_wording_still_stripped():
    assert len(ss.VERSION_NOTE.format(v="10.10.10")) < 100
    old = ("Does things. (Version 1.0.1; prefer the copy with the highest version if several copies of this skill are "
           "listed, and treat an unnumbered copy as older.)")
    assert ss.VERSION_NOTE_RE.sub("", old) == "Does things."
    assert ss.VERSION_NOTE_RE.sub("", "Does things. " + ss.VERSION_NOTE.format(v="2.0.0")) == "Does things."


def test_todo_check_flags_placeholders_not_prose(top):
    folder = make(top, A)
    doc = folder / "SUBSKILL.md"
    doc.write_text(doc.read_text(encoding="utf-8") + "\nKeep a short notes or TODO file.\n", encoding="utf-8")
    assert not [e for e in ss.check_skillset(top)[0] if "TODO" in e]
    doc.write_text(doc.read_text(encoding="utf-8") + "\nTODO: finish this step.\n", encoding="utf-8")
    assert [e for e in ss.check_skillset(top)[0] if "TODO" in e]


def test_scripts_stay_executable_through_zip_and_pull(top, tmp_path):
    script = top / "scripts" / "skillset.py"
    script.chmod(0o644)  # simulate an upload that dropped the bit
    zipped = tmp_path / "ss.zip"
    ss.write_zip(top, zipped, "skillset-os")
    dest = tmp_path / "wc"
    assert run(top, "pull", "--source", str(zipped), "--dest", str(dest), "--installed", str(tmp_path / "none")) == 0
    assert (dest / "scripts" / "skillset.py").stat().st_mode & 0o111


def test_build_zips_what_git_would_commit_and_overwrites(top, tmp_path):
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=top, check=True)
    (top / ".env").write_text("SECRET=1\n", encoding="utf-8")          # ignored by the template's .env rule
    (top / "notes.txt").write_text("untracked, not ignored\n", encoding="utf-8")
    ss.write_index(top)                                                 # restores .gitignore from the template
    assert run(top, "build") == 0
    out = top / "skillset-os.zip"
    names = set(zipfile.ZipFile(out).namelist())
    assert "skillset-os/notes.txt" in names and "skillset-os/SKILL.md" in names
    # no secrets, and no zip except packed members (subskills/**/NAME.zip), e.g. its own output
    assert not any(n.endswith(".env") for n in names)
    assert not any(n.endswith(".zip") and "/subskills/" not in n for n in names), sorted(n for n in names if n.endswith(".zip"))
    assert git(top, "status", "--porcelain", "--ignored", "skillset-os.zip").startswith("!!")  # gitignored
    (top / "notes.txt").unlink()
    assert run(top, "build") == 0                                       # overwrites
    assert "skillset-os/notes.txt" not in zipfile.ZipFile(out).namelist()


# ---------------------------------------------------------------- folder sections, contents, review, split uploads

def test_every_folder_member_has_its_this_folder_section(top):
    ss.write_index(top)
    for _, m in ss.walk(top):
        if m.form == "folder" and top in m.location.parents:
            assert ss.folder_block(m.path) in (m.folder / m.doc).read_text(encoding="utf-8"), m.path
    assert ss.folder_block(".") in (top / "SKILL.md").read_text(encoding="utf-8")
    leaf = next(m for _, m in ss.walk(top) if m.kind == "skill" and m.form == "folder" and top in m.location.parents)
    doc = leaf.folder / leaf.doc
    doc.write_text(ss.strip_folder_block(doc.read_text(encoding="utf-8")), encoding="utf-8")
    assert any("This folder" in e for e in ss.check_skillset(top)[0])     # required
    ss.write_index(top)
    assert not ss.check_skillset(top)[0]                                  # and restored by index


def test_contents_lists_files_with_a_line_each(top, capsys):
    assert run(top, "contents", "software-dev/repo-adoption/adopt-repository") == 0
    out = capsys.readouterr().out
    assert "adopt.py" in out and "Adopt a repository" in out and "SUBSKILL.md" in out
    assert run(top, "contents", "scripts") == 0                           # any folder, not only members
    assert "skillset.py" in capsys.readouterr().out
    assert run(top, "contents", "cognition", "--depth", "1") == 0         # a skillset shows its members
    assert "[skillset" in capsys.readouterr().out


def test_review_reports_real_problems(top, capsys):
    folder = top / "subskills" / "interpersonal"
    (folder / "broken.py").write_text("def f(:\n", encoding="utf-8")
    (folder / "bad.json").write_text("{nope", encoding="utf-8")
    (folder / "key.txt").write_text("token ghp_" + "a" * 36 + "\n", encoding="utf-8")
    assert run(top, "review", "interpersonal") == 1
    out = capsys.readouterr().out
    assert "Python syntax error" in out and "invalid JSON" in out and "secret" in out
    for f in ("broken.py", "bad.json", "key.txt"):
        (folder / f).unlink()
    assert run(top, "review", "interpersonal") == 0


def test_package_does_not_demand_bumps_for_folder_sections_alone(pulled):
    doc = next(pulled.rglob("SUBSKILL.md"))
    doc.write_text(ss.strip_folder_block(doc.read_text(encoding="utf-8")), encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=pulled, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x"], cwd=pulled, check=True)
    subprocess.run(["git", "tag", "-f", "synced"], cwd=pulled, check=True, capture_output=True)
    assert run(pulled, "package", "--skip-tests", "--out", str(pulled.parent / "out"), "--message", "sections") == 0


def test_big_skillset_uploads_as_parts_that_merge_back(top, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(ss, "SPLIT_AT", 50)   # cognition (69 files) splits again, one level down; leaves top-level headroom
    out = tmp_path / "up"
    out.mkdir()
    assert run(top, "build", "--out", str(out / "skillset-os.zip"), "--split") == 0
    zips = sorted(out.glob("*.zip"))
    assert len(zips) > 2
    installed = tmp_path / "skills" / "user"
    installed.mkdir(parents=True)
    counted = 0
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            assert len(names) <= ss.MAX_FILES
            counted += len(names)
            zf.extractall(installed)
    for part in installed.iterdir():
        data, body = ss.read(part / "SKILL.md")
        assert not ss.check_name(str(data["name"])), data["name"]
        desc = " ".join(str(data["description"]).split())
        assert len(desc) <= ss.MAX_DESCRIPTION and "<" not in desc and ">" not in desc
        if part.name != "skillset-os":
            assert data["metadata"]["part-of"] == "skillset-os"
            assert "audit" in desc and "When asked to review or audit it" in body and "When asked what is here" in body
    assert "## Installed in parts" in (installed / "skillset-os" / "SKILL.md").read_text(encoding="utf-8")
    script = installed / "skillset-os" / "scripts" / "skillset.py"
    r = subprocess.run([sys.executable, str(script), "open", "software-dev/code-review"], capture_output=True, text=True, check=False)
    assert r.returncode == 0 and "SUBSKILL.md" in r.stdout, r.stderr
    dest = tmp_path / "wc"
    r = subprocess.run([sys.executable, str(script), "pull", "--dest", str(dest), "--installed", str(tmp_path / "skills")],
                       capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stderr
    original = {f.relative_to(top).as_posix(): f.read_bytes() for f in ss.tree_files(top)}
    merged = {f.relative_to(dest).as_posix(): f.read_bytes() for f in ss.tree_files(dest)}
    assert merged == original                                            # every file back, unchanged


# ---------------------------------------------------------------- release integrity of split uploads

def _build_parts(top, tmp_path, monkeypatch):
    monkeypatch.setattr(ss, "SPLIT_AT", 50)   # cognition (69 files) splits again, one level down; leaves top-level headroom
    out = tmp_path / "up"
    out.mkdir()
    assert run(top, "build", "--out", str(out / "skillset-os.zip"), "--split") == 0
    return sorted(out.glob("*.zip"))


def _install(zips, dest):
    dest.mkdir(parents=True, exist_ok=True)
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            zf.extractall(dest)
    return dest / "skillset-os" / "scripts" / "skillset.py"


def test_every_upload_carries_the_same_parts_manifest(top, tmp_path, monkeypatch):
    zips = _build_parts(top, tmp_path, monkeypatch)
    manifests = set()
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            manifests.add(zf.read(f"{z.stem}/PARTS.json"))
    assert len(manifests) == 1
    data = json.loads(manifests.pop())
    assert len(data["parts"]) == len(zips) and {p["name"] for p in data["parts"]} == {z.stem for z in zips}


def test_check_on_a_lone_main_upload_names_the_missing_parts(top, tmp_path, monkeypatch):
    zips = _build_parts(top, tmp_path, monkeypatch)
    script = _install([z for z in zips if z.stem == "skillset-os"], tmp_path / "alone" / "user")
    r = subprocess.run([sys.executable, str(script), "check"], capture_output=True, text=True, check=False)
    assert r.returncode == 1
    assert "parts missing" in r.stdout and "skillset-os-repo.zip" in r.stdout and "broken link" not in r.stdout
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=script.parent.parent,
                       capture_output=True, text=True, check=False)
    assert r.returncode == 5 and "NOT RUN: split upload" in r.stdout, r.stdout[-500:]   # explains, doesn't crash


def test_check_passes_with_every_part_and_catches_a_changed_one(top, tmp_path, monkeypatch):
    zips = _build_parts(top, tmp_path, monkeypatch)
    script = _install(zips, tmp_path / "all" / "user")
    r = subprocess.run([sys.executable, str(script), "check"], capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout[-800:]
    victim = next(f for p in sorted((tmp_path / "all" / "user").iterdir()) if p.name != "skillset-os"
                  for f in p.rglob("SUBSKILL.md"))
    victim.write_text(victim.read_text(encoding="utf-8") + "\nedited\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(script), "check"], capture_output=True, text=True, check=False)
    assert r.returncode == 1 and "differs from PARTS.json" in r.stdout


def test_release_gate_refuses_uploads_that_do_not_rebuild_the_skillset(top, tmp_path, monkeypatch):
    real = ss.write_zip

    def lossy(folder, dest, top_name, files=None):
        files = sorted(files if files is not None else ss.tree_files(folder))
        if dest.name.endswith("-cognition.zip"):
            files = files[:-1]                                   # a file lost on the way into the zip
        return real(folder, dest, top_name, files)

    monkeypatch.setattr(ss, "write_zip", lossy)
    monkeypatch.setattr(ss, "SPLIT_AT", 50)   # cognition (69 files) splits again, one level down; leaves top-level headroom
    out = tmp_path / "up"
    out.mkdir()
    assert run(top, "build", "--out", str(out / "skillset-os.zip"), "--split") == 1


def test_a_never_released_skillset_stays_unreleased_until_release(pulled):
    (pulled / "CHANGELOG.md").write_text("# Changelog\n\n## Unreleased\n\n- First version.\n", encoding="utf-8")
    ss.set_version(pulled / "SKILL.md", "1.0.0")
    ss.write_index(pulled)
    subprocess.run(["git", "add", "-A"], cwd=pulled, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "fresh"], cwd=pulled, check=True)
    subprocess.run(["git", "tag", "-f", "synced"], cwd=pulled, check=True, capture_output=True)
    doc = next(pulled.rglob("SUBSKILL.md"))
    doc.write_text(doc.read_text(encoding="utf-8") + "\nA new line.\n", encoding="utf-8")   # no bump needed yet
    out = str(pulled.parent / "out")
    assert run(pulled, "package", "--skip-tests", "--out", out, "--message", "first change") == 0
    log = (pulled / "CHANGELOG.md").read_text(encoding="utf-8")
    assert ss.top_info(pulled)[1] == "1.0.0" and "## Unreleased" in log and "- first change." in log
    assert run(pulled, "package", "--skip-tests", "--out", out, "--release") == 0
    log = (pulled / "CHANGELOG.md").read_text(encoding="utf-8")
    assert ss.top_info(pulled)[1] == "1.0.0" and "## 1.0.0 — " in log and "## Unreleased" not in log
    doc.write_text(doc.read_text(encoding="utf-8") + "\nAfter the release.\n", encoding="utf-8")
    assert run(pulled, "bump", doc.parent.relative_to(pulled / "subskills").as_posix().replace("subskills/", ""),
               "--part", "patch") == 0
    assert run(pulled, "package", "--skip-tests", "--out", out, "--message", "after release") == 0
    log = (pulled / "CHANGELOG.md").read_text(encoding="utf-8")                # the same working copy, released
    assert ss.top_info(pulled)[1] == "1.0.1" and "## 1.0.1 — " in log and "## Unreleased" not in log
    doc.write_text(doc.read_text(encoding="utf-8") + "\nA second change.\n", encoding="utf-8")
    assert run(pulled, "bump", doc.parent.relative_to(pulled / "subskills").as_posix().replace("subskills/", ""),
               "--part", "patch") == 0
    assert run(pulled, "package", "--skip-tests", "--out", out, "--message", "second release") == 0
    log = (pulled / "CHANGELOG.md").read_text(encoding="utf-8")                # 1.0.1 already shipped: bump again
    assert ss.top_info(pulled)[1] == "1.0.2" and "## 1.0.2 — " in log and "## Unreleased" not in log


# ---------------------------------------------------------------- one upload: groups zipped inside it

def _build_packed(top, tmp_path, monkeypatch, limit=100):
    monkeypatch.setattr(ss, "SPLIT_AT", limit)
    out = tmp_path / "up"
    out.mkdir()
    assert run(top, "build", "--out", str(out / "skillset-os.zip"), "--pack-groups") == 0
    return sorted(out.glob("*.zip"))


def test_over_the_limit_the_default_is_plain_part_skills_with_no_zipped_members(top, tmp_path, monkeypatch):
    monkeypatch.setattr(ss, "SPLIT_AT", 100)
    out = tmp_path / "up"
    out.mkdir()
    assert run(top, "build", "--out", str(out / "skillset-os.zip")) == 0
    zips = sorted(out.glob("*.zip"))
    assert len(zips) > 1                                        # separate skills, each a plain folder
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            assert not [n for n in zf.namelist() if n.endswith(".zip")], z.name   # nothing Claude cannot load
            assert "skillset-os/PACKED.json" not in zf.namelist()


def test_check_warns_that_a_zipped_member_is_not_a_usable_skill(top):
    shutil.make_archive(str(top / "subskills" / "apps"), "zip", top / "subskills", "apps")
    shutil.rmtree(top / "subskills" / "apps")
    ss.write_index(top)
    _, warnings = ss.check_skillset(top)
    assert any("apps is a zip" in w and "cannot load a zip as a skill" in w for w in warnings)


def test_over_the_limit_the_upload_stays_one_skill_with_zipped_groups(top, tmp_path, monkeypatch):
    zips = _build_packed(top, tmp_path, monkeypatch)
    assert [z.name for z in zips] == ["skillset-os.zip"]
    with zipfile.ZipFile(zips[0]) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        packed = json.loads(zf.read("skillset-os/PACKED.json"))
        top_doc = zf.read("skillset-os/SKILL.md").decode("utf-8")
    assert len(names) <= 100 and "skillset-os/subskills/cognition.zip" in names
    assert "subskills/cognition" in [e["path"] for e in packed["packed"]]   # the largest group goes first
    assert "subskills/cognition.zip" in top_doc and "## Packed groups" in top_doc   # routers point at the zip


def test_an_installed_packed_upload_reads_checks_and_pulls_back_exactly(top, tmp_path, monkeypatch):
    zips = _build_packed(top, tmp_path, monkeypatch)
    installed = tmp_path / "skills" / "user"
    installed.mkdir(parents=True)
    with zipfile.ZipFile(zips[0]) as zf:
        zf.extractall(installed)
    script = installed / "skillset-os" / "scripts" / "skillset.py"
    r = subprocess.run([sys.executable, str(script), "open", "cognition/reasoning/research"], capture_output=True,
                       text=True, check=False)
    assert r.returncode == 0 and "SUBSKILL.md" in r.stdout, r.stderr
    r = subprocess.run([sys.executable, str(script), "check"], capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout[-600:]
    dest = tmp_path / "wc"
    r = subprocess.run([sys.executable, str(script), "pull", "--dest", str(dest), "--installed", str(tmp_path / "skills")],
                       capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stderr
    original = {f.relative_to(top).as_posix(): f.read_bytes() for f in ss.tree_files(top)}
    assert {f.relative_to(dest).as_posix(): f.read_bytes() for f in ss.tree_files(dest)} == original


def test_a_changed_packed_group_fails_check(top, tmp_path, monkeypatch):
    zips = _build_packed(top, tmp_path, monkeypatch)
    installed = tmp_path / "skills" / "user"
    installed.mkdir(parents=True)
    with zipfile.ZipFile(zips[0]) as zf:
        zf.extractall(installed)
    inner = installed / "skillset-os" / "subskills" / "cognition.zip"
    with zipfile.ZipFile(inner, "a") as zf:
        zf.writestr("cognition/EXTRA.md", "added after packaging\n")
    script = installed / "skillset-os" / "scripts" / "skillset.py"
    r = subprocess.run([sys.executable, str(script), "check"], capture_output=True, text=True, check=False)
    assert r.returncode == 1 and "differs from PACKED.json" in r.stdout


def test_release_gate_refuses_a_packed_group_that_lost_a_file(top, tmp_path, monkeypatch):
    real = ss.write_zip

    def lossy(folder, dest, top_name, files=None):
        files = sorted(files if files is not None else ss.tree_files(folder))
        if dest.name == "cognition.zip":
            files = files[:-1]
        return real(folder, dest, top_name, files)

    monkeypatch.setattr(ss, "write_zip", lossy)
    monkeypatch.setattr(ss, "SPLIT_AT", 100)
    out = tmp_path / "up"
    out.mkdir()
    assert run(top, "build", "--out", str(out / "skillset-os.zip"), "--pack-groups") == 1


# ---------------------------------------------------------------- editions

def test_shared_edition_builds_patched_and_leaves_the_source_alone(top, tmp_path):
    if not (top / "editions" / "shared" / "edition.json").is_file():
        pytest.skip("no shared edition in this skillset")
    before = {f.relative_to(top).as_posix(): f.read_bytes() for f in ss.tree_files(top)}
    out = tmp_path / "out" / "skillset-os-shared.zip"
    assert run(top, "build", "--edition", "shared", "--out", str(out)) == 0
    assert {f.relative_to(top).as_posix(): f.read_bytes() for f in ss.tree_files(top)} == before
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
        doc = zf.read("skillset-os/SKILL.md").decode("utf-8")
    assert not any(n.startswith("skillset-os/editions/") for n in names)
    assert "shared edition" in doc and "## Shared edition" in doc
    assert "say hi, start or I am bored" not in doc
    assert "say hi, start or I am bored" in (top / "SKILL.md").read_text(encoding="utf-8")


def test_edition_refuses_when_its_source_text_has_drifted(top, tmp_path):
    spec_dir = top / "editions" / "probe"
    spec_dir.mkdir(parents=True)
    (spec_dir / "edition.json").write_text(json.dumps({"patches": [
        {"file": "SKILL.md", "old": "text that is not in the skill anywhere", "new": "x"}]}), encoding="utf-8")
    assert run(top, "build", "--edition", "probe", "--out", str(tmp_path / "p.zip")) == 1
    assert not (tmp_path / "skillset-os-probe.zip").exists()


# ---------------------------------------------------------------- plugin (the shared edition doubles as it)

def _plugin_zip(top, tmp_path):
    if not ss.plugin_editions(top):
        pytest.skip("no edition carries a plugin.json")
    out = tmp_path / "skillset-os-shared.zip"
    assert run(top, "build", "--plugin", "--out", str(out)) == 0
    return out


def test_the_plugin_zip_fits_the_claude_ai_plugin_upload(top, tmp_path):
    # claude.ai's Upload plugin wants .claude-plugin/plugin.json at the zip root or inside one top-level folder,
    # with nothing beside that folder (its Skills page rejects any zip holding a plugin manifest)
    out = _plugin_zip(top, tmp_path)
    with zipfile.ZipFile(out) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
    assert {n.split("/", 1)[0] for n in names} == {"skillset-os"}
    assert [n for n in names if n.endswith("plugin.json")] == ["skillset-os/.claude-plugin/plugin.json"]


def test_the_shared_edition_zip_is_the_plugin(top, tmp_path):
    out = _plugin_zip(top, tmp_path)
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        plugin = json.loads(zf.read("skillset-os/.claude-plugin/plugin.json"))
        market = json.loads(zf.read("skillset-os/.claude-plugin/marketplace.json"))
        doc = zf.read("skillset-os/SKILL.md").decode("utf-8")
    name, version = ss.top_info(top)
    assert plugin["name"] == name and plugin["version"] == version
    assert market["plugins"][0]["source"] == "./" and market["plugins"][0]["name"] == name
    assert not (ss.PLUGIN_OWNED - {"name", "version"}) & set(plugin)      # no components: the root SKILL.md loads
    assert not any(n.startswith(("skillset-os/skills/", "skillset-os/bin/")) for n in names)
    assert "## Shared edition" in doc and "sponsors/Softmonster" not in doc
    assert not (top / ".claude-plugin").exists()                          # generated, never stored


def test_the_plugin_is_exactly_the_shared_edition_plus_its_manifests(top, tmp_path):
    out = _plugin_zip(top, tmp_path)
    edition = ss.plugin_editions(top)[0]
    stage = tmp_path / "stage" / "skillset-os"
    ss.stage_edition(top, edition, stage, ss.committable_files(top))
    want = {f.relative_to(stage).as_posix(): f.read_bytes() for f in ss.tree_files(stage)}
    with zipfile.ZipFile(out) as zf:
        got = {n.split("/", 1)[1]: zf.read(n) for n in zf.namelist() if not n.endswith("/")}
    extra = sorted(set(got) - set(want))
    assert extra == [".claude-plugin/marketplace.json", ".claude-plugin/plugin.json"]
    assert {k: v for k, v in got.items() if k in want} == want


def test_the_installed_plugin_tree_still_passes_check(top, tmp_path):
    out = _plugin_zip(top, tmp_path)
    installed = tmp_path / "skills"
    with zipfile.ZipFile(out) as zf:
        zf.extractall(installed)
    script = installed / "skillset-os" / "scripts" / "skillset.py"
    r = subprocess.run([sys.executable, str(script), "check"], capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout[-600:]


def test_plugin_refuses_a_spec_that_declares_components_or_a_bad_homepage(top, tmp_path):
    if not ss.plugin_editions(top):
        pytest.skip("no edition carries a plugin.json")
    spec_path = top / "editions" / ss.plugin_editions(top)[0] / "plugin.json"
    good = spec_path.read_text(encoding="utf-8")
    try:
        for bad in ({"skills": "./subskills"}, {"version": "9.9.9"}, {"homepage": "not a url"}):
            spec = json.loads(good)
            spec["manifest"].update(bad)
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            out = tmp_path / "p.zip"
            assert run(top, "build", "--plugin", "--out", str(out)) == 1, bad
            assert not out.exists()
    finally:
        spec_path.write_text(good, encoding="utf-8")


def test_check_refuses_reserved_and_duplicate_commands(top):
    doc = top / "subskills" / "self-improvement" / "subskills" / "goal-setting" / "SUBSKILL.md"
    good = doc.read_text(encoding="utf-8")
    try:
        for bad, why in (("remember goals", "reserves"), ("goal options", "reserves"), ("verify work", "already"),
                         ("Set Goals!", "lowercase")):
            doc.write_text(good.replace('command: "set goals"', f'command: "{bad}"'), encoding="utf-8")
            errors, warnings = ss.check_skillset(top)
            found = errors if why != "already" else warnings          # duplicates warn; they still route
            assert any("goal-setting: command" in e and why in e for e in found), (bad, found)
    finally:
        doc.write_text(good, encoding="utf-8")


# ---------------------------------------------------------------- upstream: shared fixes into the source

@pytest.fixture
def shared_wc(top, tmp_path):
    """A working copy pulled from the shared edition, as someone using the plugin would have it."""
    z = tmp_path / "shared.zip"
    assert run(top, "build", "--edition", "shared", "--out", str(z)) == 0
    dest = tmp_path / "shared-wc"
    assert run(top, "pull", "--source", str(z), "--dest", str(dest), "--installed", str(tmp_path / "none")) == 0
    return dest


def test_upstream_carries_shared_fixes_into_the_source_in_its_own_wording(top, shared_wc):
    member = "subskills/self-improvement/subskills/habit-building/SUBSKILL.md"
    (shared_wc / member).write_text((shared_wc / member).read_text(encoding="utf-8") + "\n- A shared fix.\n",
                                    encoding="utf-8")
    doc = shared_wc / "SKILL.md"
    doc.write_text(doc.read_text(encoding="utf-8").replace("Skillset-OS is plain Markdown and Python,",
                                                           "Skillset-OS is plain Markdown and Python (fixed),"),
                   encoding="utf-8")
    assert run(shared_wc, "upstream", "--into", str(top)) == 0
    assert "- A shared fix." in (top / member).read_text(encoding="utf-8")
    source = (top / "SKILL.md").read_text(encoding="utf-8")
    assert "Python (fixed)," in source                                     # shared-and-source text flows
    assert "## Shared edition" not in source and 'edition: "shared"' not in source   # edition wording stays out
    assert "sponsors/Softmonster" in source                                # the source keeps its own wording
    assert (top / "editions" / "shared" / "edition.json").is_file() and not (top / ".claude-plugin").exists()
    assert ss.check_skillset(top)[0] == []


def test_upstream_refuses_to_leak_edition_only_wording(top, shared_wc):
    doc = shared_wc / "SKILL.md"
    doc.write_text(doc.read_text(encoding="utf-8").replace("- **Care first.**", "- **Care first, edited.**"),
                   encoding="utf-8")
    before = (top / "SKILL.md").read_text(encoding="utf-8")
    assert run(shared_wc, "upstream", "--into", str(top)) == 1            # a conflict to merge by hand
    assert (top / "SKILL.md").read_text(encoding="utf-8") == before       # nothing of the edition leaked in
    assert (top / "SKILL.md.rej").is_file()


def test_upstream_with_no_changes_and_its_refusals(top, shared_wc, capsys):
    assert run(shared_wc, "upstream", "--into", str(top)) == 0
    assert "nothing to push" in capsys.readouterr().out
    assert run(top, "upstream", "--into", str(top)) == 1                  # the source is not an edition copy
    assert run(shared_wc, "upstream", "--into", str(shared_wc)) == 1      # --into must be the source


def test_reverse_patch_survives_reordered_front_matter_keys():
    new = '  edition: "shared"\n  summary: "X (shared edition): one'
    old = '  summary: "X: one'
    text = 'metadata:\n  version: "1"\n  summary: "X (shared edition): one skill."\n  edition: "shared"\n---\n'
    assert ss.reverse_patch(text, new, old) == 'metadata:\n  version: "1"\n  summary: "X: one skill."\n---\n'
    assert ss.reverse_patch("unrelated text", new, old) is None

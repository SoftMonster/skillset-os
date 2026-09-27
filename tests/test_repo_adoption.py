"""Tests for software-dev/repo-adoption: adopt.py scaffolds a develop-PROJECT member from a project."""
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


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

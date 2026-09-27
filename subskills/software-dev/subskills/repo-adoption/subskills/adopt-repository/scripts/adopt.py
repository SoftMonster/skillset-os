#!/usr/bin/env python3
"""Adopt a repository or app into the skillset as a develop-PROJECT sub-skill.

  adopt.py NAME SOURCE --title TITLE --trigger PHRASE --description TEXT [--set PATH] [--dry-run]

NAME     the project slug, e.g. tally (the member becomes develop-tally)
SOURCE   a .zip, a folder, or a GitHub repository as owner/repo or https://github.com/owner/repo
--set    the nested skillset that holds adopted projects (default software-dev/repo-adoption)

It unwraps wrapper folders, drops VCS and build clutter, refuses sources that are skills
then creates the member with skillset.py, copies
the source into its app/ folder, and writes SUBSKILL.md, app/CHANGELOG.md,
scripts/NAME.py (checker skeleton) and tests/test_NAME.py from the templates. It ends with
an inventory of the source and the stack detected by codebase-orientation's detect_stack.py.
--dry-run prints the inventory and the plan without changing anything.

Run it on the skillset working copy (the folder above scripts/skillset.py), never the
installed copy. Needs git only for GitHub sources; github.com is reachable from the sandbox.
Exit codes: 0 success, 1 refused, 2 bad arguments.
"""
from __future__ import annotations

import argparse
import collections
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TEMPLATES = HERE / "templates"
CLUTTER = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv", ".pytest_cache", ".ruff_cache",
           ".mypy_cache", ".DS_Store", "Thumbs.db", ".idea", ".vscode"}
SKILL_FILES = {"SKILL.md", "SUBSKILL.md", "SKILLSET.md"}
SPLIT_AT = 190  # over this many files the upload zips its largest groups inside itself (skillset.py)
GITHUB_RE = re.compile(r"^(?:https://github\.com/)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?$")


class Refused(Exception):
    """Adoption cannot go ahead; the message says what to do instead."""


def find_top(start: Path) -> Path:
    for folder in [start, *start.parents]:
        if (folder / "SKILL.md").is_file() and (folder / "scripts" / "skillset.py").is_file():
            return folder
    raise Refused("no skillset found above this script; run the adopt.py inside the working copy")


def fetch(source: str, tmp: Path) -> Path:
    """The source as a plain folder, whatever form it came in."""
    path = Path(source)
    if path.is_dir():
        return path
    if path.is_file() and zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            z.extractall(tmp / "src")
        return tmp / "src"
    m = GITHUB_RE.match(source)
    if m and not path.exists():
        dest = tmp / m.group(2)
        r = subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/{m.group(1)}/{m.group(2)}.git",
                            str(dest)], capture_output=True, text=True, check=False)
        if r.returncode:
            raise Refused(f"git clone failed: {r.stderr.strip().splitlines()[-1]}; check the name, or attach a zip")
        return dest
    raise Refused(f"{source} is not a folder, a zip or owner/repo")


def unwrap(folder: Path) -> Path:
    """Descend through single wrapper folders (GitHub's repo-main/, a zip's top folder)."""
    while True:
        entries = [p for p in folder.iterdir() if p.name not in CLUTTER and not p.name.startswith("__MACOSX")]
        if len(entries) == 1 and entries[0].is_dir():
            folder = entries[0]
        else:
            return folder


def source_files(folder: Path) -> list[Path]:
    return [p for p in sorted(folder.rglob("*"))
            if p.is_file() and not (set(p.relative_to(folder).parts) & CLUTTER)
            and "__MACOSX" not in p.relative_to(folder).parts]


def upload_count(top: Path) -> int:
    r = subprocess.run([sys.executable, str(top / "scripts" / "skillset.py"), "check"],
                       capture_output=True, text=True, check=False)
    m = re.search(r"(\d+) files", r.stdout + r.stderr)
    if not m:
        raise Refused("skillset.py check did not report a file count; run it and fix what it says first")
    return int(m.group(1))


def inventory(folder: Path, files: list[Path]) -> str:
    size = sum(f.stat().st_size for f in files)
    exts = collections.Counter(f.suffix.lower() or f.name for f in files).most_common(8)
    big = sorted(files, key=lambda f: f.stat().st_size, reverse=True)[:5]
    lines = [f"{len(files)} files, {size / 1024:.0f} KB",
             "types: " + ", ".join(f"{e} ×{n}" for e, n in exts),
             "largest: " + ", ".join(f"{f.relative_to(folder).as_posix()} ({f.stat().st_size // 1024} KB)" for f in big)]
    return "\n".join(lines)


def member_folder(top: Path, member: str) -> Path:
    folder = top
    for part in member.split("/"):
        folder = folder / "subskills" / part
    return folder


def fill(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def adopt(args, top: Path) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.name):
        raise Refused("NAME must be lowercase letters, digits and hyphens, e.g. tally")
    member = f"{args.set}/develop-{args.name}"
    folder = member_folder(top, member)
    if folder.exists():
        raise Refused(f"{member} already exists; change it with its own develop member, or retire it first")
    if not member_folder(top, args.set).is_dir():
        raise Refused(f"no nested skillset {args.set}; create it with organise-skillsets or pass --set")
    with tempfile.TemporaryDirectory() as tmp:
        src = unwrap(fetch(args.source, Path(tmp)))
        files = source_files(src)
        if not files:
            raise Refused(f"{args.source} holds no files")
        skills = [f.relative_to(src).as_posix() for f in files if f.name in SKILL_FILES]
        if skills:
            shown = ", ".join(skills[:3]) + (f" and {len(skills) - 3} more" if len(skills) > 3 else "")
            raise Refused(f"{args.source} contains {shown}: it is a skill or skillset, not a project; use import-skill")
        total = upload_count(top) + len(files) + 4  # + SUBSKILL.md, CHANGELOG.md, checker, test
        print(inventory(src, files))
        stack = HERE.parent.parent.parent / "codebase-orientation" / "scripts" / "detect_stack.py"
        if stack.is_file():
            print(subprocess.run([sys.executable, str(stack), str(src)], capture_output=True, text=True, check=False).stdout.strip())
        if total > SPLIT_AT:
            print(f"NOTE the skillset will hold {total} files, so its upload zips its largest groups inside itself")
        script = args.name.replace("-", "") + ".py"
        print(f"PLAN {member}: {len(files)} files → app/, scripts/{script}, tests/test_{args.name.replace('-', '_')}.py")
        if args.dry_run:
            return
        r = subprocess.run([sys.executable, str(top / "scripts" / "skillset.py"), "new", member,
                            "--description", args.description, "--trigger", args.trigger],
                           capture_output=True, text=True, check=False)
        if r.returncode:
            raise Refused(f"skillset.py new refused: {(r.stdout + r.stderr).strip()}")
        for f in files:
            dest = folder / "app" / f.relative_to(src)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
    values = {"TITLE": args.title, "NAME": args.name, "MEMBER": member, "SCRIPT": script,
              "FOLDER": "/subskills/".join(member.split("/"))}
    doc = folder / "SUBSKILL.md"
    front = doc.read_text(encoding="utf-8").split("\n---\n", 1)[0] + "\n---\n\n"
    doc.write_text(front + fill((TEMPLATES / "DEVELOP.md").read_text(encoding="utf-8"), values), encoding="utf-8")
    (folder / "app" / "CHANGELOG.md").write_text(
        f"# {args.title} changelog\n\nNewest first, one entry per release.\n\n## Adopted\n\n"
        f"- Imported into the skillset from {Path(args.source).name}. No code changes.\n", encoding="utf-8")
    (folder / "scripts").mkdir(exist_ok=True)
    checker = folder / "scripts" / script
    checker.write_text(fill((TEMPLATES / "checker.py").read_text(encoding="utf-8"), values), encoding="utf-8")
    checker.chmod(0o755)
    test = top / "tests" / f"test_{args.name.replace('-', '_')}.py"
    rel = checker.relative_to(top).as_posix()
    test.write_text(f'"""Checks for {member}: the adopted source must pass its own checker."""\n'
                    "import subprocess\nimport sys\nfrom pathlib import Path\n\n"
                    f'CHECKER = Path(__file__).resolve().parent.parent / "{rel}"\n\n\n'
                    f"def test_{args.name.replace('-', '_')}_checks_pass():\n"
                    "    r = subprocess.run([sys.executable, str(CHECKER), \"check\"], capture_output=True, text=True, check=False)\n"
                    "    assert r.returncode == 0, r.stdout + r.stderr\n", encoding="utf-8")
    print(f"adopted {member}. NEXT (adopt-repository steps 4-7): read the source, write the rules and checks in "
          f"scripts/{script}, fill every TODO in SUBSKILL.md, then skillset.py check")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name")
    parser.add_argument("source")
    parser.add_argument("--title", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--set", default="software-dev/repo-adoption")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        adopt(args, find_top(HERE))
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

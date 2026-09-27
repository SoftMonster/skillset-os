#!/usr/bin/env python3
"""Tooling for a skillset: one uploadable skill made of sub-skills and nested skillsets.

A skillset folder has a router (SKILL.md at the top, SKILLSET.md when nested) and a
subskills/ folder of members. Each member is one of:
  subskills/<name>/SUBSKILL.md        a sub-skill (folder)
  subskills/<name>/SKILLSET.md        a nested skillset (folder, with its own subskills/)
  subskills/<name>.zip                a packed member: a skill, a skillset or a whole
                                      repository, possibly holding further zips inside
Packed members may be linked to a GitHub repository (see add-source and refresh).
skillsets.json at the top records linked repositories and trigger overrides for packed
members. Members are addressed by path: "team/meeting-minutes".

Commands (run `skillset.py COMMAND --help` for options):
  check        Validate everything, at every depth, including inside zips.
  index        Regenerate the top description, every router table and the dotfiles.
  tree         Show the whole skillset, descending into nested skillsets and zips.
  open PATH    Print the instructions file for a member, extracting zips as needed.
  new PATH     Create a sub-skill.            new-set PATH  Create a nested skillset.
  bump PATH    Raise a member's version.      rename PATH NEW / move PATH --into SET
  retire PATH  Remove a member.               pack PATH / unpack PATH
  import SRC   Add a skill, skillset, repository or collection (folder or zip).
  add-source NAME --repo OWNER/REPO   Link a GitHub repository.   refresh [PATH]
  pull         Copy a skillset into a git working copy.
  package      Version, test, commit, and write the upload zip (also the GitHub copy) and a patch.

The top is the folder above this script unless --root is given.
Exit codes: 0 success, 1 check failed or action refused, 2 bad arguments.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import io
import json
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - fallback for bare Python
    yaml = None

HERE = Path(__file__).resolve().parent
TOP_ROUTER, SET_ROUTER, LEAF = "SKILL.md", "SKILLSET.md", "SUBSKILL.md"
MEMBERS = "subskills"
MANIFEST = "skillsets.json"
CACHE = Path(tempfile.gettempdir()) / "skillsets-cache"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED_WORDS = ("claude", "anthropic")
MAX_DESCRIPTION, WARN_DESCRIPTION = 1024, 900
MAX_TRIGGER = 160
MAX_LINES = 500
# claude.ai's uploader has been reported to reject zips with more than 200 files; the API caps skills at 30 MB.
MAX_FILES, WARN_FILES = 200, 170
MAX_BYTES = 30 * 1024 * 1024
CORE = {"sync-skillset", "command-line"}   # always at the top, never packed
TABLE_START, TABLE_END = "<!-- subskills:start -->", "<!-- subskills:end -->"
# Every folder member (and the top) carries a generated "This folder" section, so each one can list,
# discuss and review its own folder when asked. `index` writes it; `check` requires it.
FOLDER_START, FOLDER_END = "<!-- folder:start -->", "<!-- folder:end -->"
# An upload over SPLIT_AT files stays ONE skill: its largest groups are zipped inside it (read through
# `skillset.py open`, which unzips with Python) and `pull` unpacks them again. With --split it is instead the
# main skill plus one part skill per member folder. Either way the repository itself stays plain folders.
SPLIT_AT = 190
PART_KEY = "part-of"
# Kept short: it is part of the 1024-character description. The pattern also matches the older, longer wording.
VERSION_NOTE = "(Version {v}; if several copies are listed, use the highest version; unnumbered is oldest.)"
VERSION_NOTE_RE = re.compile(r"\s*\(Version [\d.]+; (?:prefer the copy|if several copies)[^)]*\)")
SKIP_PARTS = {".git", "__pycache__", "node_modules", ".pytest_cache", ".ruff_cache", ".venv", "venv"}
SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}
DOTFILES = {"gitignore": ".gitignore", "ci.yml": ".github/workflows/ci.yml", "FUNDING.yml": ".github/FUNDING.yml"}
TODO_RE = re.compile(r"\bTODO:")  # the templates' placeholders; plain prose such as "a TODO file" is fine
LINK_RE = re.compile(r"\]\(([^)#\s]+)\)")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)  # fixed timestamps make packed zips byte-for-byte reproducible


class Refused(RuntimeError):
    """A check failed or an action was refused; the message says what to do."""


# ================================================================ frontmatter and files

def split_frontmatter(text: str) -> tuple[str, str]:
    text = text.replace("\r\n", "\n").lstrip("\ufeff")
    if not text.startswith("---\n"):
        raise Refused("file must start with a '---' frontmatter line")
    end = text.find("\n---", 4)
    if end == -1:
        raise Refused("frontmatter has no closing '---' line")
    return text[4:end], text[end + 4:].lstrip("-").lstrip("\n")


def _simple_yaml(block: str) -> dict:
    data: dict = {}
    parent = None
    for raw in block.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        key, _, value = raw.strip().partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        if raw.startswith((" ", "\t")) and parent is not None:
            data[parent][key] = value
        elif not value:
            parent, data[key] = key, {}
        else:
            parent, data[key] = None, value
    return data


def parse(text: str) -> tuple[dict, str]:
    block, body = split_frontmatter(text)
    if yaml is None:
        return _simple_yaml(block), body
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as exc:
        raise Refused(f"frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise Refused("frontmatter is not a set of key: value lines")
    return data, body


def read(path: Path) -> tuple[dict, str]:
    return parse(path.read_text(encoding="utf-8"))


def quote(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def version_of(data: dict) -> str:
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    return str(meta.get("version") or data.get("version") or "1.0.0")


def vtuple(version: str | None) -> tuple[int, ...]:
    parts = [int(p) for p in re.findall(r"\d+", version or "1.0.0")[:3]]
    return tuple(parts + [0] * (3 - len(parts)))


def bumped(version: str, part: str) -> str:
    major, minor, patch = vtuple(version)
    return {"major": f"{major + 1}.0.0", "minor": f"{major}.{minor + 1}.0"}.get(part, f"{major}.{minor}.{patch + 1}")


def set_front(path: Path, key: str, value: str) -> None:
    """Set a top-level frontmatter key (added after description if missing)."""
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    end = text.find("\n---", 4)
    front, rest = text[:end], text[end:]
    line = f"{key}: {quote(value)}"
    if re.search(rf"^{re.escape(key)}:", front, re.MULTILINE):
        front = re.sub(rf"^{re.escape(key)}:.*$", lambda _: line, front, count=1, flags=re.MULTILINE)
    else:
        front = front.rstrip("\n") + "\n" + line
    path.write_text(front + rest, encoding="utf-8")


def set_version(path: Path, new: str) -> None:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    end = text.find("\n---", 4)
    front, rest = text[:end], text[end:]
    if re.search(r"^metadata:\s*$", front, re.MULTILINE):
        if re.search(r"^\s+version:", front, re.MULTILINE):
            front = re.sub(r"^(\s+version:\s*).*$", lambda m: f'{m.group(1)}"{new}"', front, count=1,
                           flags=re.MULTILINE)
        else:
            front = re.sub(r"^metadata:\s*$", f'metadata:\n  version: "{new}"', front, count=1, flags=re.MULTILINE)
    else:
        front = re.sub(r"^version:.*\n?", "", front, flags=re.MULTILINE).rstrip("\n")
        front += f'\nmetadata:\n  version: "{new}"'
    path.write_text(front + rest, encoding="utf-8")


def tree_files(folder: Path) -> list[Path]:
    """Files under FOLDER that belong in an upload (caches and VCS folders left out)."""
    out = []
    for f in sorted(folder.rglob("*")):
        rel = f.relative_to(folder)
        if (not f.is_file() or set(rel.parts) & SKIP_PARTS or f.name in SKIP_FILES or f.suffix == ".pyc"
                or rel.parts[0].endswith(".egg-info")):
            continue
        out.append(f)
    return out


def check_name(name: str) -> list[str]:
    problems = []
    if not NAME_RE.match(name):
        problems.append(f"name '{name}' must be lowercase letters, digits and single hyphens")
    if len(name) > 64:
        problems.append(f"name '{name}' is over 64 characters")
    problems += [f"name '{name}' must not contain '{w}'" for w in RESERVED_WORDS if w in name]
    return problems


def shorten(text: str, limit: int = 120) -> str:
    text = text.strip().rstrip(".").strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-")


def derive_trigger(description: str) -> str:
    """A short 'Use when' phrase from a description: its when-clause, else its first sentence."""
    description = VERSION_NOTE_RE.sub("", description).strip().strip('"')
    m = re.search(r"\b(?:should )?use (?:this skill |this |it )?(?:when|whenever|any ?time|if)\s+(.+?)(?:\.\s|\.$|$)",
                  description, re.IGNORECASE)
    if m:
        clause = re.sub(r"^(?:the user |a user |someone |they )?(?:asks? to|wants? to:?|is asked to|asked to)\s+", "",
                        m.group(1).strip(), flags=re.IGNORECASE)
        return shorten(clause, MAX_TRIGGER)
    first = re.split(r"(?<=\.)\s", description, maxsplit=1)[0]
    return shorten(first[:1].lower() + first[1:]) if first else ""


# ================================================================ zips

def safe_names(zf: zipfile.ZipFile) -> list[str]:
    names = [n for n in zf.namelist() if not n.endswith("/")]
    for n in names:
        if n.startswith("/") or ".." in Path(n).parts:
            raise Refused(f"zip entry {n!r} points outside the archive")
    return names


def extract_all(zf: zipfile.ZipFile, dest: Path) -> None:
    """Extract every entry and restore the executable bit, which zipfile.extractall drops."""
    zf.extractall(dest)
    for info in zf.infolist():
        if not info.is_dir() and (info.external_attr >> 16) & 0o111:
            target = dest / info.filename
            target.chmod(target.stat().st_mode | 0o755)


def extract(zip_path: Path) -> Path:
    """Extract a zip into the content-addressed cache and return its single top folder."""
    digest = hashlib.sha1(zip_path.read_bytes()).hexdigest()[:16]
    dest = CACHE / digest
    if not (dest / ".complete").exists():
        shutil.rmtree(dest, ignore_errors=True)
        try:
            with zipfile.ZipFile(zip_path) as zf:
                safe_names(zf)
                extract_all(zf, dest)
        except zipfile.BadZipFile as exc:
            raise Refused(f"{zip_path.name} is not a valid zip: {exc}") from exc
        (dest / ".complete").write_text("", encoding="utf-8")
    tops = [p for p in dest.iterdir() if p.name != ".complete"]
    if len(tops) != 1 or not tops[0].is_dir():
        raise Refused(f"{zip_path.name} must hold exactly one top-level folder")
    return tops[0]


def write_zip(folder: Path, dest: Path, top: str, files: list[Path] | None = None) -> int:
    """Zip FOLDER (or just FILES inside it) as TOP/..., deterministically (sorted entries, fixed timestamps)."""
    files = sorted(files) if files is not None else tree_files(folder)
    tmp = dest.with_name(dest.name + ".part")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            info = zipfile.ZipInfo(f"{top}/{f.relative_to(folder).as_posix()}", ZIP_TIME)
            data = f.read_bytes()
            executable = f.stat().st_mode & 0o111 or data[:2] == b"#!"  # scripts stay runnable even if a copy lost the bit
            info.external_attr = (0o755 if executable else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
    tmp.replace(dest)
    return len(files)


# ================================================================ the model

def instructions_in(folder: Path) -> tuple[str, str] | None:
    """(file, kind) of the instructions at FOLDER's top, or None."""
    if (folder / LEAF).is_file():
        return LEAF, "skill"
    if (folder / SET_ROUTER).is_file():
        return SET_ROUTER, "skillset"
    if (folder / TOP_ROUTER).is_file():
        return TOP_ROUTER, "skillset" if (folder / MEMBERS).is_dir() else "skill"
    return None


def load_manifest(root: Path) -> dict:
    path = root / MANIFEST
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise Refused(f"{MANIFEST} is not valid JSON: {exc}") from exc
    return data if isinstance(data, dict) else {}


def save_manifest(root: Path, data: dict) -> None:
    path = root / MANIFEST
    if data:
        path.write_text(json.dumps(dict(sorted(data.items())), indent=2) + "\n", encoding="utf-8")
    elif path.exists():
        path.unlink()


def take_subtree(manifest: dict, rel: str) -> dict:
    """Remove and return entries under REL/, keyed relative to REL."""
    prefix = rel + "/"
    moved = {k[len(prefix):]: manifest.pop(k) for k in [k for k in manifest if k.startswith(prefix)]}
    return moved


def put_subtree(manifest: dict, rel: str, entries: dict) -> None:
    for k, v in entries.items():
        manifest[f"{rel}/{k}"] = v


@dataclass
class Member:
    name: str
    form: str                    # "folder" | "zip"
    location: Path               # the member folder, or the .zip file
    rel: str                     # location relative to the top, "" for the top itself
    path: str                    # member path from the top: "team/minutes"
    kind: str = "skill"          # "skill" | "skillset"
    folder: Path | None = None   # folder holding the instructions (extracted for zips)
    doc: str = ""
    description: str = ""
    trigger: str = ""
    version: str = "1.0.0"
    source: dict = field(default_factory=dict)
    error: str = ""

    @property
    def label(self) -> str:
        return f"{self.kind}{' (zip)' if self.form == 'zip' else ''}"


def load_member(location: Path, rel: str, path: str, manifest: dict) -> Member:
    form = "zip" if location.suffix == ".zip" else "folder"
    name = location.stem if form == "zip" else location.name
    m = Member(name=name, form=form, location=location, rel=rel, path=path,
               source=manifest.get(rel, {}) if rel else {})
    try:
        folder = extract(location) if form == "zip" else location
        found = instructions_in(folder)
        if not found:
            raise Refused(f"no {LEAF}, {SET_ROUTER} or {TOP_ROUTER} at its top")
        m.folder, (m.doc, m.kind) = folder, found
        if form == "zip" and folder.name != name:
            raise Refused(f"its top folder is '{folder.name}', not '{name}'")
        data, _ = read(folder / m.doc)
        m.description = VERSION_NOTE_RE.sub("", " ".join(str(data.get("description") or "").split())).strip()
        m.trigger = " ".join(str(m.source.get("trigger") or data.get("trigger") or
                                 derive_trigger(m.description)).split()).rstrip(".")
        m.version = version_of(data)
        if m.doc != TOP_ROUTER and str(data.get("name") or name) != name:
            # (a packed standalone skill or repository keeps its own SKILL.md name; the member name wins)
            raise Refused(f"name '{data.get('name')}' does not match '{name}'")
    except Refused as exc:
        m.error = str(exc)
    return m


def context_for(folder: Path, root: Path, ctx: tuple[Path, dict]) -> tuple[Path, dict]:
    """Inside a zip, a skillset with its own skillsets.json (a packed repository) uses that manifest."""
    if root not in folder.parents and folder != root and (folder / MANIFEST).is_file():
        return folder, load_manifest(folder)
    return ctx


def members_of(set_folder: Path, root: Path, set_path: str, manifest: dict) -> list[Member]:
    """Members of SET_FOLDER; ROOT is the folder MANIFEST's keys are relative to."""
    base = set_folder / MEMBERS
    if not base.is_dir():
        return []
    out = []
    for loc in sorted(base.iterdir(), key=lambda p: p.name):
        if loc.name.startswith(".") or loc.name == "__pycache__":
            continue
        if loc.is_dir() or loc.suffix == ".zip":
            name = loc.stem if loc.suffix == ".zip" else loc.name
            rel = loc.relative_to(root).as_posix() if root in loc.parents else ""
            out.append(load_member(loc, rel, f"{set_path}/{name}".strip("/"), manifest))
    return out


def walk(root: Path, manifest: dict | None = None):
    """Yield (depth, member) for every member at every depth, including inside zips."""
    manifest = load_manifest(root) if manifest is None else manifest

    def visit(set_folder: Path, set_path: str, depth: int, ctx: tuple[Path, dict]):
        for m in members_of(set_folder, ctx[0], set_path, ctx[1]):
            yield depth, m
            if m.kind == "skillset" and m.folder is not None and not m.error:
                yield from visit(m.folder, m.path, depth + 1, context_for(m.folder, root, ctx))

    yield from visit(root, "", 0, (root, manifest))


def resolve(root: Path, path: str, manifest: dict | None = None) -> Member:
    """Find the member at PATH ('a/b/c'), extracting zips on the way."""
    manifest = load_manifest(root) if manifest is None else manifest
    folder, current, ctx = root, None, (root, manifest)
    names = [p for p in path.strip("/").split("/") if p]
    if not names:
        raise Refused("give a member path such as 'team/meeting-minutes'")
    for i, name in enumerate(names):
        matches = [m for m in members_of(folder, ctx[0], "/".join(names[:i]), ctx[1]) if m.name == name]
        if not matches:
            raise Refused(f"no member '{name}' in {'/'.join(names[:i]) or 'the top skillset'}")
        current = matches[0]
        if current.error:
            raise Refused(f"{current.path}: {current.error}")
        if i < len(names) - 1:
            if current.kind != "skillset":
                raise Refused(f"'{current.path}' is a sub-skill, not a skillset")
            folder = current.folder
            ctx = context_for(folder, root, ctx)
    return current


def set_folder_for(root: Path, set_path: str) -> Path:
    """The editable folder of the skillset at SET_PATH ('' is the top)."""
    if not set_path.strip("/"):
        return root
    m = resolve(root, set_path)
    if m.kind != "skillset":
        raise Refused(f"'{set_path}' is a sub-skill, not a skillset")
    if m.form == "zip" or root not in m.location.parents:
        raise Refused(f"'{m.path}' is packed (or inside a packed member); run `skillset.py unpack {m.path}` first")
    return m.location


def editable(root: Path, path: str) -> Member:
    m = resolve(root, path)
    if root not in m.location.parents:
        raise Refused(f"'{m.path}' is inside a packed member; unpack its parent first")
    return m


# ================================================================ routers

def router_table(members: list[Member]) -> str:
    lines = [TABLE_START, "| Member | Kind | Version | Use when |", "|---|---|---|---|"]
    for m in members:
        target = f"{MEMBERS}/{m.location.name}" + (f"/{m.doc}" if m.form == "folder" else "")
        desc = (m.description or m.error).replace("|", "\\|")
        lines.append(f"| [{m.name}]({target}) | {m.label} | {m.version} | {desc} |")
    return "\n".join(lines + [TABLE_END])


def top_description(summary: str, members: list[Member], version: str) -> str:
    triggers = "; ".join(m.trigger for m in members if m.trigger)
    return f"{summary.strip()} Use when the user wants to: {triggers}. {VERSION_NOTE.format(v=version)}"


def replace_table(body: str, table: str) -> str:
    if TABLE_START in body and TABLE_END in body:
        head, rest = body.split(TABLE_START, 1)
        return head + table + rest.split(TABLE_END, 1)[1]
    return body


def render_top(root: Path, manifest: dict) -> str:
    data, body = read(root / TOP_ROUTER)
    members = members_of(root, root, "", manifest)
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    version, summary = str(meta.get("version") or "1.0.0"), str(meta.get("summary") or "")
    lines = ["---", f"name: {data.get('name', '')}",
             f"description: {quote(top_description(summary, members, version))}"]
    lines += [f"{k}: {quote(data[k])}" for k in ("license", "compatibility", "allowed-tools") if k in data]
    lines += ["metadata:", f"  version: {quote(version)}", f"  summary: {quote(summary)}"]
    lines += [f"  {k}: {quote(v)}" for k, v in meta.items() if k not in {"version", "summary"}]
    lines.append("---")
    return with_folder_block("\n".join(lines) + "\n\n" + replace_table(body, router_table(members)).lstrip("\n"), ".")


def render_set(set_folder: Path, root: Path, set_path: str, manifest: dict) -> str:
    text = (set_folder / SET_ROUTER).read_text(encoding="utf-8").replace("\r\n", "\n")
    return with_folder_block(replace_table(text, router_table(members_of(set_folder, root, set_path, manifest))), set_path)


def folder_sets(root: Path, manifest: dict) -> list[tuple[Path, str]]:
    """Every nested skillset stored as a folder inside the top (editable routers)."""
    return [(m.location, m.path) for _, m in walk(root, manifest)
            if m.kind == "skillset" and m.form == "folder" and root in m.location.parents]


def expected_dotfiles(root: Path) -> dict[str, str]:
    out = {}
    for template, target in DOTFILES.items():
        src = root / "scripts" / "templates" / template
        if src.exists():
            out[target] = src.read_text(encoding="utf-8")
    return out


def write_index(root: Path) -> None:
    manifest = load_manifest(root)
    for folder, path in sorted(folder_sets(root, manifest), key=lambda x: -x[1].count("/")):
        (folder / SET_ROUTER).write_text(render_set(folder, root, path, manifest), encoding="utf-8")
    (root / TOP_ROUTER).write_text(render_top(root, manifest), encoding="utf-8")
    for _, m in walk(root, manifest):   # sub-skills: the generated "This folder" section
        if m.kind == "skill" and m.form == "folder" and root in m.location.parents and not m.error:
            doc = m.folder / m.doc
            text = doc.read_text(encoding="utf-8")
            if with_folder_block(text, m.path) != text:
                doc.write_text(with_folder_block(text, m.path), encoding="utf-8")
    for target, text in expected_dotfiles(root).items():
        path = root / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if (root / "memory").is_dir() and (HERE / "memory.py").is_file():
        memory_module().write_entry(root)          # memory/SELF.md, the self-memory entry point


def memory_module():
    """scripts/memory.py (the AI's self-memory), loaded from beside this file."""
    mod = sys.modules.get("skillset_memory")
    if mod is None:
        spec = importlib.util.spec_from_file_location("skillset_memory", HERE / "memory.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["skillset_memory"] = mod
        spec.loader.exec_module(mod)
    return mod


def former_names(root: Path) -> set[str]:
    """Names the top skill had before a rename (metadata.former-names, comma-separated)."""
    data, _ = read(root / TOP_ROUTER)
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    return {n.strip() for n in str(meta.get("former-names") or "").split(",") if n.strip()}


def top_info(root: Path) -> tuple[str, str]:
    data, _ = read(root / TOP_ROUTER)
    return str(data.get("name") or ""), version_of(data)


# ================================================================ folder sections, contents, review

def folder_block(path: str) -> str:
    where = path or "."
    return (f"{FOLDER_START}\n## This folder\n\n"
            f"Asked what this folder holds, or to review it, look before answering. "
            f"`python3 <top>/scripts/skillset.py contents {where}` lists every file in it with a line on what each is, and "
            f"`python3 <top>/scripts/skillset.py review {where}` audits them for problems. Then read the files the question "
            f"needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.\n"
            f"{FOLDER_END}")


def strip_folder_block(text: str) -> str:
    if FOLDER_START in text and FOLDER_END in text:
        head, rest = text.split(FOLDER_START, 1)
        return head.rstrip("\n") + "\n" + rest.split(FOLDER_END, 1)[1].lstrip("\n")
    return text


def with_folder_block(text: str, path: str) -> str:
    block = folder_block(path)
    if FOLDER_START in text and FOLDER_END in text:
        head, rest = text.split(FOLDER_START, 1)
        return head + block + rest.split(FOLDER_END, 1)[1]
    return text.rstrip("\n") + "\n\n" + block + "\n"


SECRET_RE = re.compile(r"(sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|"
                       r"-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,})")
DOCSTRING_RE = re.compile(r'^\s*(?:"{3}|\'{3})\s*(.+)', re.MULTILINE)


def summary_of(f: Path) -> str:
    """One line saying what a file is, from its own text."""
    if f.suffix == ".zip":
        try:
            with zipfile.ZipFile(f) as zf:
                return f"zip, {sum(1 for n in zf.namelist() if not n.endswith('/'))} files"
        except zipfile.BadZipFile:
            return "zip (unreadable)"
    try:
        text = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return "binary"
    if f.suffix == ".md":
        try:
            front, body = split_frontmatter(text)
        except Refused:
            front, body = "", text
        if front:
            try:
                desc = str(parse(text)[0].get("description") or "")
            except Refused:
                desc = ""
            if desc:
                return shorten(first_sentence(VERSION_NOTE_RE.sub("", " ".join(desc.split()))), 100)
        for line in body.splitlines():
            if line.startswith("#"):
                return shorten(line.lstrip("# ").strip(), 100)
    if f.suffix == ".json":
        try:
            data = json.loads(text)
        except ValueError:
            return "JSON (invalid)"
        if isinstance(data, dict):
            return shorten("JSON: " + ", ".join(list(data)[:8]), 100)
        return f"JSON list of {len(data)}" if isinstance(data, list) else "JSON"
    if f.suffix == ".py":
        m = DOCSTRING_RE.search(text)
        if m and text.lstrip().startswith(('"""', "'''", "#!", "#", "from __future__")):
            return shorten(m.group(1).strip().strip('"\''), 100)
    for line in text.splitlines():
        t = line.strip()
        if not t or t.startswith("#!"):
            continue
        t = re.sub(r"^(//+|/\*+|\*+|#+|<!--+|--)\s*", "", t)
        t = re.sub(r"\s*(\*/|-->)$", "", t).strip(" =-")
        if t:
            return shorten(t, 100)
    return "empty" if not text.strip() else ""


def target_folder(root: Path, path: str) -> tuple[Path, Member | None, str]:
    """PATH is '.', a member path ('team/minutes') or a folder path inside the skillset."""
    if path.strip("/") in ("", "."):
        return root, None, "."
    direct = root / path
    if direct.is_dir() and root.resolve() in direct.resolve().parents:
        own = next((m for _, m in walk(root) if m.form == "folder" and m.location.resolve() == direct.resolve()), None)
        return direct, own, path.strip("/")
    m = resolve(root, path)
    return m.folder, m, m.path


def cmd_contents(args) -> int:
    root = args.root
    folder, m, where = target_folder(root, args.path)
    if m is not None:
        print(f"{where}: {m.label} {m.name} {m.version}. {m.description}")
    elif folder == root:
        name, version = top_info(root)
        print(f"{name} {version} (the top skillset)")
    else:
        print(f"{where}: a folder inside the skillset")
    members = {mm.location.resolve(): mm for _, mm in walk(root) if mm.location.resolve() != folder.resolve()}
    count = 0

    def show(d: Path, indent: int) -> None:
        nonlocal count
        for p in sorted(d.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            if p.name in SKIP_FILES or p.name in SKIP_PARTS or (p.name.startswith(".") and p.name != ".gitignore"):
                continue
            pad = "  " * indent
            if p.resolve() in members:
                mm = members[p.resolve()]
                print(f"{pad}{p.name}{'/' if p.is_dir() else ''}  [{mm.label} {mm.version}] {shorten(mm.description, 90)}")
                count += 1
                continue
            if p.is_dir():
                print(f"{pad}{p.name}/  ({len(tree_files(p))} files)")
                if args.depth is None or indent < args.depth or p.name == MEMBERS:   # a skillset's members always show
                    show(p, indent + 1)
                continue
            lines = ""
            if p.suffix not in (".zip", ".png", ".jpg", ".gif", ".pdf"):
                try:
                    lines = f"{p.read_text(encoding='utf-8').count(chr(10)) + 1} lines, "
                except (UnicodeDecodeError, OSError):
                    pass
            print(f"{pad}{p.name}  ({lines}{p.stat().st_size / 1024:.1f} KB)  {summary_of(p)}")
            count += 1

    show(folder, 1)
    print(f"{count} entries. A member is listed once; `contents <member path>` looks inside it.")
    return 0


def review_folder(root: Path, folder: Path) -> list[tuple[str, str, str]]:
    """Automatic findings for FOLDER: (severity, where, message), severity 'error' or 'warning'."""
    out: list[tuple[str, str, str]] = []

    def rel(p: Path) -> str:
        return p.relative_to(root).as_posix() if root in p.parents else p.as_posix()

    for _, m in walk(root):
        if m.location == folder or folder in m.location.parents:
            e, w = check_member(m, root)
            out += [("error", m.path, x.split(": ", 1)[-1]) for x in e]
            out += [("warning", m.path, x.split(": ", 1)[-1]) for x in w]
    node = shutil.which("node")
    for f in tree_files(folder):
        where = rel(f)
        size = f.stat().st_size
        if size == 0:
            out.append(("warning", where, "empty file"))
            continue
        if size > 1_000_000:
            out.append(("warning", where, f"large file ({size / 1e6:.1f} MB)"))
        if f.suffix == ".zip":
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SECRET_RE.search(text):
            out.append(("error", where, "looks like it contains a secret (key or token); remove it and rotate it"))
        template = "templates" in f.relative_to(root).parts   # placeholders there are on purpose
        if f.suffix == ".md" and not template:
            if text.count("\n") > MAX_LINES:
                out.append(("warning", where, f"over {MAX_LINES} lines"))
            for number, line in code_free_lines(text):
                if TODO_RE.search(line):
                    out.append(("warning", f"{where}:{number}", "still has a TODO"))
                for target in LINK_RE.findall(line):
                    if not target.startswith(("http:", "https:", "mailto:", "/", "$", "~")) and "*" not in target \
                            and not (f.parent / target).exists():
                        out.append(("error", f"{where}:{number}", f"broken link {target}"))
        elif f.suffix == ".py":
            try:
                compile(text, str(f), "exec")
            except SyntaxError as exc:
                out.append(("error", f"{where}:{exc.lineno}", f"Python syntax error: {exc.msg}"))
        elif f.suffix == ".json":
            try:
                json.loads(text)
            except ValueError as exc:
                out.append(("error", where, f"invalid JSON: {exc}"))
        elif f.suffix in (".js", ".mjs") and node:
            r = subprocess.run([node, "--check", str(f)], capture_output=True, text=True, check=False)
            if r.returncode:
                msg = next((ln for ln in r.stderr.splitlines() if "Error" in ln), r.stderr.strip()[:120])
                out.append(("error", where, f"JavaScript syntax error: {msg}"))
    return list(dict.fromkeys(out))


def cmd_review(args) -> int:
    root = args.root
    folder, _m, where = target_folder(root, args.path)
    findings = review_folder(root, folder)
    errors = [f for f in findings if f[0] == "error"]
    for sev, w, msg in sorted(findings, key=lambda x: (x[0] != "error", x[1])):
        print(f"{sev.upper():7} {w}: {msg}")
    print(f"{where}: {len(errors)} error(s), {len(findings) - len(errors)} warning(s) in {len(tree_files(folder))} files.")
    print("These are the automatic checks only. Now read the files for clarity, accuracy, contradictions, duplication "
          "and anything out of date, and report every finding by severity with its file, line and a concrete fix.")
    return 1 if errors else 0


# ================================================================ check

def code_free_lines(text: str) -> list[tuple[int, str]]:
    out, in_fence = [], False
    for number, line in enumerate(text.split("\n"), start=1):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append((number, re.sub(r"`[^`]*`", "", line)))
    return out


def check_scripts(root: Path) -> list[str]:
    errors, node = [], shutil.which("node")
    for f in tree_files(root):
        rel = f.relative_to(root).as_posix()
        if f.suffix == ".py":
            try:
                py_compile.compile(str(f), doraise=True, cfile=str(Path(tempfile.gettempdir()) / "skillset_check.pyc"))
            except py_compile.PyCompileError as exc:
                errors.append(f"{rel}: Python syntax error: {exc.msg.strip().splitlines()[-1]}")
        elif f.suffix == ".sh":
            r = subprocess.run(["bash", "-n", str(f)], capture_output=True, text=True, check=False)
            if r.returncode:
                errors.append(f"{rel}: shell syntax error: {r.stderr.strip()}")
        elif f.suffix in {".js", ".mjs", ".cjs"} and node:
            r = subprocess.run([node, "--check", str(f)], capture_output=True, text=True, check=False)
            if r.returncode:
                errors.append(f"{rel}: JavaScript syntax error: {r.stderr.strip().splitlines()[0]}")
    return errors


def check_member(m: Member, root: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    where = m.path
    if m.error:
        return [f"{where}: {m.error}"], []
    errors += [f"{where}: {p}" for p in check_name(m.name)]
    if not m.description:
        errors.append(f"{where}: description is empty")
    if not m.trigger:
        errors.append(f"{where}: no trigger; add one" + (f" with `skillset.py import --replace` or in {MANIFEST}"
                                                        if m.form == "zip" else " to its frontmatter"))
    elif len(m.trigger) > MAX_TRIGGER:
        errors.append(f"{where}: trigger is {len(m.trigger)} characters (max {MAX_TRIGGER})")
    for label, value in (("description", m.description), ("trigger", m.trigger)):
        if "<" in value or ">" in value:
            errors.append(f"{where}: {label} contains < or >")
    inside_top = root in m.location.parents
    if m.form == "folder" and inside_top:
        text = (m.folder / m.doc).read_text(encoding="utf-8")
        for number, line in code_free_lines(text):
            if TODO_RE.search(line):
                errors.append(f"{where}/{m.doc}:{number}: still has a TODO")
        if text.count("\n") > MAX_LINES:
            warnings.append(f"{where}: {m.doc} is over {MAX_LINES} lines; move detail into files beside it")
        if folder_block(m.path) not in text:
            errors.append(f"{where}: its \"This folder\" section is missing or out of date; run `skillset.py index`")
        for number, line in code_free_lines(text):
            for target in LINK_RE.findall(line):
                if not target.startswith(("http:", "https:", "mailto:", "/", "$", "~")) and "*" not in target \
                        and not (m.folder / target).exists():
                    errors.append(f"{where}/{m.doc}:{number}: broken link {target}")
        if m.kind == "skillset":
            if TABLE_START not in text:
                errors.append(f"{where}: {SET_ROUTER} has no router table markers")
            elif not (m.folder / MEMBERS).is_dir() or not any((m.folder / MEMBERS).iterdir()):
                warnings.append(f"{where}: skillset has no members yet")
    return errors, warnings


def check_skillset(root: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    top = root / TOP_ROUTER
    if not top.is_file():
        return [f"no {TOP_ROUTER} in {root}"], []
    try:
        data, body = read(top)
        manifest = load_manifest(root)
    except Refused as exc:
        return [str(exc)], []
    errors += [f"{TOP_ROUTER}: {p}" for p in check_name(str(data.get("name") or ""))]
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    if not meta.get("version"):
        errors.append(f"{TOP_ROUTER}: metadata.version is missing")
    if not meta.get("summary"):
        errors.append(f"{TOP_ROUTER}: metadata.summary is missing (it starts the generated description)")
    description = " ".join(str(data.get("description") or "").split())
    if len(description) > MAX_DESCRIPTION:
        errors.append(f"{TOP_ROUTER}: description is {len(description)} characters (max {MAX_DESCRIPTION}); shorten "
                      "triggers, or group members into nested skillsets (each contributes one trigger)")
    elif len(description) > WARN_DESCRIPTION:
        warnings.append(f"{TOP_ROUTER}: description is {len(description)}/{MAX_DESCRIPTION} characters; tighten "
                        "triggers or group members into a nested skillset")
    if "<" in description or ">" in description:
        errors.append(f"{TOP_ROUTER}: description contains < or >, which the uploader rejects")
    if TABLE_START not in body:
        errors.append(f"{TOP_ROUTER}: router table markers are missing")

    stale = render_top(root, manifest) != top.read_text(encoding="utf-8").replace("\r\n", "\n")
    for folder, path in folder_sets(root, manifest):
        if render_set(folder, root, path, manifest) != (folder / SET_ROUTER).read_text(encoding="utf-8"):
            stale = True
    if stale:
        errors.append("a router table or the top description is out of date; run `skillset.py index`")

    seen: dict[str, str] = {}
    for _, m in walk(root, manifest):
        e, w = check_member(m, root)
        errors += e
        warnings += w
        parent = m.path.rsplit("/", 1)[0] if "/" in m.path else ""
        key = f"{parent}/{m.name}"
        if key in seen:
            errors.append(f"{m.path}: two members share this name ({seen[key]} and {m.location.name})")
        seen[key] = m.location.name
    for f in tree_files(root):
        if f.name == MANIFEST and f.parent != root:
            errors.append(f"{f.relative_to(root).as_posix()}: nested {MANIFEST} inside the top; its entries belong "
                          f"in the top {MANIFEST}")
    for rel in manifest:
        if not (root / rel).exists():
            errors.append(f"{MANIFEST}: entry '{rel}' does not match any member")

    for f in tree_files(root):
        rel = f.relative_to(root)
        if f.name == TOP_ROUTER and rel != Path(TOP_ROUTER):
            errors.append(f"{rel.as_posix()}: only the top may have a {TOP_ROUTER} outside zips; rename it to "
                          f"{LEAF} or {SET_ROUTER}, or pack its member")
    for number, line in code_free_lines(top.read_text(encoding="utf-8")):
        for target in LINK_RE.findall(line):
            if not target.startswith(("http:", "https:", "/")) and not (root / target).exists():
                errors.append(f"{TOP_ROUTER}:{number}: broken link {target}")
    errors += check_scripts(root)
    if (root / "memory").is_dir() and (HERE / "memory.py").is_file():
        m_errors, m_warnings = memory_module().check(root)
        errors += [f"memory: {e}" for e in m_errors]
        warnings += [f"memory: {w}" for w in m_warnings]
    for target, text in expected_dotfiles(root).items():
        path = root / target
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            errors.append(f"{target} differs from scripts/templates; run `skillset.py index`")
    files = tree_files(root)
    size = sum(f.stat().st_size for f in files)
    try:
        packs = plan_packing(root, files)
        rels = [f.relative_to(root).as_posix() for f in files]
        in_upload = len(rels) - sum(1 for r in rels for g in packs if r.startswith(g + "/")) + len(packs) + (1 if packs else 0)
        if in_upload > MAX_FILES:
            errors.append(f"the upload would hold {in_upload} files; claude.ai rejects more than {MAX_FILES}")
        if packs:
            warnings.append(f"{len(files)} files (over {SPLIT_AT}), so the upload zips {len(packs)} group(s) inside it: "
                            + ", ".join(packs) + ". Reading them needs code execution")
    except Refused as exc:
        errors.append(str(exc))
    if size > MAX_BYTES:
        errors.append(f"upload would be {size / 1e6:.1f} MB; keep it under {MAX_BYTES // (1024 * 1024)} MB")
    return errors, warnings


# ================================================================ git, changelog, mentions

def git(root: Path, *args: str, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if check and r.returncode:
        raise Refused(f"git {' '.join(args)} failed: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def has_git(root: Path) -> bool:
    return (root / ".git").exists() and shutil.which("git") is not None


def ident(root: Path) -> list[str]:
    return [] if git(root, "config", "user.name", check=False) else \
        ["-c", "user.name=Claude", "-c", "user.email=claude@example.invalid"]


def ref_exists(root: Path, ref: str) -> bool:
    return has_git(root) and not subprocess.run(["git", "rev-parse", "--verify", "-q", ref], cwd=root,
                                                capture_output=True, check=False).returncode


def file_at(root: Path, ref: str, rel: str) -> str | None:
    r = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=root, capture_output=True, text=True, check=False)
    return None if r.returncode else r.stdout


def tracked(root: Path, rel: str) -> bool:
    return has_git(root) and bool(git(root, "ls-files", rel, check=False))


def remove(root: Path, location: Path) -> None:
    rel = location.relative_to(root).as_posix()
    if tracked(root, rel):
        git(root, "rm", "-r", "-q", "--cached", rel)
    if location.is_dir():
        shutil.rmtree(location)
    elif location.exists():
        location.unlink()


def changelog_add(root: Path, line: str) -> None:
    path = root / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Changelog\n"
    if line in text:
        return
    if "## Unreleased\n\n" in text:
        text = text.replace("## Unreleased\n\n", f"## Unreleased\n\n{line}\n", 1)
    elif "\n## " in text:
        head, tail = text.split("\n## ", 1)
        text = f"{head.rstrip()}\n\n## Unreleased\n\n{line}\n\n## {tail}"
    else:
        text = f"{text.rstrip()}\n\n## Unreleased\n\n{line}\n"
    path.write_text(text, encoding="utf-8")


def changelog_release(root: Path, version: str) -> None:
    path = root / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## Unreleased" in text and f"## {version} " not in text:
        today = dt.datetime.now(dt.timezone.utc).date().isoformat()
        path.write_text(text.replace("## Unreleased", f"## {version} — {today}", 1), encoding="utf-8")


def first_sentence(text: str) -> str:
    m = re.match(r"(.+?\.)(\s|$)", text)
    return m.group(1) if m else text


def mention_re(name: str) -> re.Pattern:
    n = re.escape(name)
    return re.compile(rf"{MEMBERS}/{n}(?![\w-])|`{n}`|(?<![\w-]){n} (?:sub-skill|skillset)")


def find_mentions(root: Path, name: str, own: Path) -> tuple[list[str], list[str]]:
    """(blocking, informational) mentions of a member outside itself; routers' tables are ignored."""
    pattern = mention_re(name)
    blocking, info = [], []
    for f in tree_files(root):
        rel = f.relative_to(root)
        if (own == f or own in f.parents or f.name in {"CHANGELOG.md", "NOTICE.md", MANIFEST}
                or f.suffix in {".zip", ".png", ".jpg", ".pdf"}):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if f.name in {TOP_ROUTER, SET_ROUTER} and TABLE_START in text:
            head, rest = text.split(TABLE_START, 1)
            table, tail = rest.split(TABLE_END, 1)
            text = head + "\n" * table.count("\n") + tail
            text = re.sub(r"^description:.*$", "description:", text, count=1, flags=re.MULTILINE)
        for number, line in enumerate(text.split("\n"), start=1):
            if pattern.search(line):
                hit = f"{rel.as_posix()}:{number}: {line.strip()[:100]}"
                (blocking if rel.parts[0] in {MEMBERS, "tests", "scripts"} or f.name == TOP_ROUTER
                 else info).append(hit)
    return blocking, info


# ================================================================ import helpers

def locate_source(path: Path, max_unwrap: int = 99) -> Path:
    """A folder for PATH (extracting zips), descending through single wrapper folders (at most MAX_UNWRAP)."""
    if path.is_file():
        if path.suffix not in {".zip", ".skill"}:
            raise Refused(f"{path.name} is not a folder, .zip or .skill file")
        tmp = Path(tempfile.mkdtemp(prefix="skillset-import-"))
        with zipfile.ZipFile(path) as zf:
            safe_names(zf)
            extract_all(zf, tmp)
        path = tmp
    while not instructions_in(path) and max_unwrap > 0:
        max_unwrap -= 1
        children = [c for c in path.iterdir() if not c.name.startswith(".") and c.name != "__MACOSX"]
        if len(children) == 1 and children[0].is_dir():
            path = children[0]
        else:
            break
    return path


def collection_members(folder: Path) -> list[Path]:
    """Skill folders inside a collection (a repository or folder of skills with no router at its top)."""
    found = sorted({md.parent for md in folder.rglob(TOP_ROUTER) if not set(md.relative_to(folder).parts) &
                    SKIP_PARTS})
    return [f for f in found if not any(o in f.parents for o in found)]


def stray_routers(folder: Path, doc: str) -> list[str]:
    """SKILL.md files other than the top one, outside zips: they break a folder-form import."""
    return [f.relative_to(folder).as_posix() for f in tree_files(folder)
            if f.name == TOP_ROUTER and f != folder / doc]


def place_member(root: Path, source: Path, set_path: str, name: str, *, packed: bool, trigger: str | None,
                 replace: bool, origin: dict | None = None) -> Member:
    """Add SOURCE (a folder with instructions at its top) as member NAME of the skillset at SET_PATH."""
    found = instructions_in(source)
    if not found:
        raise Refused(f"{source} has no {LEAF}, {SET_ROUTER} or {TOP_ROUTER} at its top")
    doc, kind = found
    problems = check_name(name)
    if not set_path and name in CORE:
        problems.append(f"'{name}' is a core member name")
    data, _ = read(source / doc)
    version = version_of(data)
    set_dir = set_folder_for(root, set_path)
    base = set_dir / MEMBERS
    existing = [p for p in (base / name, base / f"{name}.zip") if p.exists()]
    manifest = load_manifest(root)
    if existing:
        old = load_member(existing[0], existing[0].relative_to(root).as_posix(), name, manifest)
        if not replace:
            problems.append(f"'{f'{set_path}/{name}'.strip('/')}' already exists; pass --replace to update it")
        elif not old.error and vtuple(version) < vtuple(old.version) and not origin:
            problems.append(f"the source ({version}) is older than the current member ({old.version})")
    description = VERSION_NOTE_RE.sub("", " ".join(str(data.get("description") or "").split())).strip()
    own_trigger = str(data.get("trigger") or "")
    chosen = (trigger or own_trigger or derive_trigger(description)).rstrip(".")
    if not chosen:
        problems.append("could not derive a trigger from the description; pass --trigger")
    if len(chosen) > MAX_TRIGGER:
        problems.append(f"trigger is {len(chosen)} characters (max {MAX_TRIGGER}); pass a shorter --trigger")
    if not packed:
        strays = stray_routers(source, doc)
        if strays:
            problems.append(f"it contains other {TOP_ROUTER} files ({', '.join(strays[:3])}); the upload allows "
                            "only one outside zips, so import it with --packed")
    if problems:
        raise Refused("; ".join(problems))

    for p in existing:
        manifest.pop(p.relative_to(root).as_posix(), None)
        remove(root, p)
    base.mkdir(parents=True, exist_ok=True)
    if packed:
        dest = base / f"{name}.zip"
        if doc != TOP_ROUTER and str(data.get("name") or name) != name:
            work = Path(tempfile.mkdtemp(prefix="skillset-pack-")) / name
            shutil.copytree(source, work, ignore=shutil.ignore_patterns(*SKIP_PARTS, "*.pyc"))
            text = (work / doc).read_text(encoding="utf-8")
            (work / doc).write_text(re.sub(r"^name:.*$", f"name: {name}", text, count=1, flags=re.MULTILINE),
                                    encoding="utf-8")
            source = work
        write_zip(source, dest, name)
        entry = dict(origin or {})
        if trigger or not own_trigger:
            entry["trigger"] = chosen
        if entry:
            manifest[dest.relative_to(root).as_posix()] = entry
    else:
        dest = base / name
        shutil.copytree(source, dest, ignore=shutil.ignore_patterns(*SKIP_PARTS, "*.pyc"))
        if (dest / MANIFEST).is_file():  # a repository's own links now live in the top manifest
            put_subtree(manifest, dest.relative_to(root).as_posix(), load_manifest(dest))
            (dest / MANIFEST).unlink()
        new_doc = SET_ROUTER if kind == "skillset" else LEAF
        if doc != new_doc:
            (dest / doc).rename(dest / new_doc)
        path = dest / new_doc
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        front, body = split_frontmatter(text)
        front = re.sub(r"^name:.*$", f"name: {name}", front, count=1, flags=re.MULTILINE)
        front = re.sub(r"^description:.*?(?=^\S|\Z)", f"description: {quote(description)}\n", front, count=1,
                       flags=re.MULTILINE | re.DOTALL).rstrip("\n")
        if kind == "skillset" and TABLE_START not in body:
            body = body.rstrip("\n") + f"\n\n## Members\n\n{TABLE_START}\n{TABLE_END}\n"
        path.write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")
        set_front(path, "trigger", chosen)
        if "version" not in json.dumps(data):
            set_version(path, "1.0.0")
        if origin:
            manifest[dest.relative_to(root).as_posix()] = dict(origin)
    save_manifest(root, manifest)
    rel = dest.relative_to(root).as_posix()
    return load_member(dest, rel, f"{set_path}/{name}".strip("/"), load_manifest(root))


def note_licence(root: Path, m: Member) -> None:
    licences = sorted(p.name for p in (m.folder or m.location).glob("LICENSE*"))
    notice = root / "NOTICE.md"
    if licences and notice.exists() and f"`{m.path}`" not in notice.read_text(encoding="utf-8"):
        with notice.open("a", encoding="utf-8") as fh:
            fh.write(f"- `{m.path}`: imported with its own licence ({', '.join(licences)}), which still applies.\n")


# ================================================================ GitHub sources

def github_fetch(repo: str, ref: str) -> tuple[Path, str]:
    """Download OWNER/REPO at REF from codeload.github.com; return (zip file, commit)."""
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
        raise Refused(f"--repo must look like owner/name, not {repo!r}")
    url = f"https://codeload.github.com/{repo}/zip/{ref}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "skillset-os"}),
                                    timeout=60) as resp:
            data = resp.read()
    except urllib.error.HTTPError as exc:
        hint = " (private repositories cannot be fetched: download the zip and use `import --packed`)" \
            if exc.code == 404 else ""
        raise Refused(f"could not download {repo}@{ref}: HTTP {exc.code}{hint}") from exc
    except urllib.error.URLError as exc:
        raise Refused(f"could not reach GitHub ({exc.reason}); check the network settings allow github.com") from exc
    tmp = Path(tempfile.mkdtemp(prefix="skillset-gh-")) / "repo.zip"
    tmp.write_bytes(data)
    commit = zipfile.ZipFile(io.BytesIO(data)).comment.decode(errors="ignore").strip()
    return tmp, commit


def remote_commit(repo: str, ref: str) -> str | None:
    """The commit REF points at, via git ls-remote (no API rate limits); None if unknown."""
    if re.fullmatch(r"[0-9a-f]{40}", ref):
        return ref
    if not shutil.which("git"):
        return None
    r = subprocess.run(["git", "ls-remote", f"https://github.com/{repo}", ref, f"refs/tags/{ref}^{{}}"],
                       capture_output=True, text=True, timeout=60, check=False)
    lines = [ln.split("\t") for ln in r.stdout.strip().splitlines() if "\t" in ln]
    peeled = [sha for sha, name in lines if name.endswith("^{}")]
    return (peeled or [sha for sha, _ in lines] or [None])[0]


def fetch_source(root: Path, set_path: str, name: str, origin: dict, packed: bool, trigger: str | None,
                 replace: bool) -> Member:
    zip_file, commit = github_fetch(origin["repo"], origin.get("commit") or origin["ref"])
    folder = locate_source(zip_file, max_unwrap=1)  # GitHub zips have exactly one wrapper: owner-repo-ref/
    if origin.get("path"):
        folder = folder / origin["path"]
        if not folder.is_dir():
            raise Refused(f"{origin['repo']} has no folder {origin['path']!r}")
    if not instructions_in(folder):
        raise Refused(f"{origin['repo']} has no skill or skillset at {origin.get('path') or 'its top'}; point "
                      "--path at one, or import it as a collection with `import`")
    entry = {k: v for k, v in origin.items() if k in {"repo", "ref", "path"} and v}
    entry["commit"] = commit or origin.get("commit", "")
    return place_member(root, folder, set_path, name, packed=packed, trigger=trigger, replace=replace, origin=entry)


# ================================================================ commands

def split_path(path: str) -> tuple[str, str]:
    path = path.strip("/")
    return (path.rsplit("/", 1)[0], path.rsplit("/", 1)[1]) if "/" in path else ("", path)


def cmd_check(args) -> int:
    if parts_manifest(args.root) is not None:          # an installed split upload: all parts, exact, first
        problems, _parts = verify_parts(args.root)
        if problems:
            for p in problems:
                print(f"ERROR {p}")
            return 1
        args.root = installed_view(args.root)
    elif (args.root / PACKED_FILE).is_file() and not (args.root / ".git").exists():
        try:                                            # an installed packed upload: every zip must be exact
            args.root = installed_view(args.root)
        except Refused as exc:
            print(f"ERROR {exc}")
            return 1
    errors, warnings = check_skillset(args.root)
    for e in errors:
        print(f"ERROR {e}")
    for w in warnings:
        print(f"WARN  {w}")
    name, version = top_info(args.root)
    count = sum(1 for _ in walk(args.root))
    print(f"{name} {version}: {count} members at all depths, {len(tree_files(args.root))} files, "
          f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def cmd_index(args) -> int:
    write_index(args.root)
    data, _ = read(args.root / TOP_ROUTER)
    print(f"index written: description {len(' '.join(str(data.get('description')).split()))}/{MAX_DESCRIPTION} "
          "characters")
    return 0


def cmd_tree(args) -> int:
    name, version = top_info(args.root)
    print(f"{name} {version}")
    for depth, m in walk(args.root):
        if args.depth is not None and depth >= args.depth:
            continue
        linked = f"  ← {m.source['repo']}@{m.source.get('commit', '')[:10]}" if m.source.get("repo") else ""
        detail = f"ERROR {m.error}" if m.error else f"{m.version}  {m.trigger}"
        print(f"{'  ' * (depth + 1)}{m.name}  [{m.label}]  {detail}{linked}")
    return 0


def cmd_open(args) -> int:
    m = resolve(args.root, args.path)
    print(m.folder / m.doc)
    print(f"# {m.path}: {m.label} {m.version}. Paths in it are relative to {m.folder}")
    return 0


def cmd_new(args, kind: str = "skill") -> int:
    root = args.root
    set_path, name = split_path(args.path)
    problems = check_name(name)
    set_dir = set_folder_for(root, set_path)
    if (set_dir / MEMBERS / name).exists() or (set_dir / MEMBERS / f"{name}.zip").exists():
        problems.append(f"'{args.path}' already exists")
    if not set_path and name in CORE:
        problems.append(f"'{name}' is a core member name")
    for label, value in (("description", args.description), ("trigger", args.trigger)):
        if "<" in value or ">" in value:
            problems.append(f"{label} contains < or >")
    if len(args.trigger) > MAX_TRIGGER:
        problems.append(f"trigger is {len(args.trigger)} characters (max {MAX_TRIGGER})")
    if problems:
        raise Refused("; ".join(problems))
    dest = set_dir / MEMBERS / name
    dest.mkdir(parents=True)
    template = "SKILLSET.md" if kind == "skillset" else "SUBSKILL.md"
    text = (root / "scripts" / "templates" / template).read_text(encoding="utf-8")
    for key, value in {"NAME": name, "TITLE": args.title or name.replace("-", " ").capitalize(),
                       "DESCRIPTION": args.description.replace('"', '\\"'),
                       "TRIGGER": args.trigger.rstrip(".").replace('"', '\\"')}.items():
        text = text.replace("{{" + key + "}}", value)
    doc = SET_ROUTER if kind == "skillset" else LEAF
    (dest / doc).write_text(text, encoding="utf-8")
    if kind == "skillset":
        (dest / MEMBERS).mkdir()
    changelog_add(root, f"- Added {'skillset' if kind == 'skillset' else 'sub-skill'} `{args.path.strip('/')}` 1.0.0: "
                        f"{first_sentence(args.description)}")
    write_index(root)
    print(f"created {dest.relative_to(root).as_posix()}/{doc}; replace every TODO, then run `skillset.py check`")
    return 0


def cmd_bump(args) -> int:
    m = editable(args.root, args.path)
    if m.form == "zip":
        raise Refused(f"'{m.path}' is packed; its version comes from inside. Unpack it to edit, or re-import it")
    new = bumped(m.version, args.part)
    set_version(m.folder / m.doc, new)
    changelog_add(args.root, f"- Updated `{m.path}` to {new}" + (f": {args.message}" if args.message else "."))
    write_index(args.root)
    print(f"{m.path}: {m.version} → {new}")
    return 0


def cmd_replace(args) -> int:
    """Replace one exact passage in a member's file, then optionally bump it.

    The member is found by its path (nested paths included), so its file is never guessed. Nothing is
    written unless the passage occurs exactly once, and the bump runs only after the edit is on disk.
    """
    m = editable(args.root, args.path)
    if m.form == "zip":
        raise Refused(f"'{m.path}' is packed; unpack it before editing")
    target = m.folder / (args.file or m.doc)
    if not target.is_file():
        raise Refused(f"'{m.path}' has no {args.file or m.doc}")
    old = Path(args.old_file).read_text(encoding="utf-8") if args.old_file else args.old
    new = Path(args.new_file).read_text(encoding="utf-8") if args.new_file else args.new
    if old is None or new is None:
        raise Refused("give the passage with --old or --old-file, and its replacement with --new or --new-file")
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise Refused(f"the passage occurs {count} times in {target.relative_to(args.root)}; it must occur exactly once, so nothing was changed")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"edited {target.relative_to(args.root)}")
    if args.part:
        return cmd_bump(argparse.Namespace(root=args.root, path=args.path, part=args.part, message=args.message))
    return 0


def relocate(root: Path, m: Member, set_dir: Path, new_name: str) -> Path:
    """Move member M into SET_DIR under NEW_NAME, keeping git history and manifest entries."""
    dest = set_dir / MEMBERS / (f"{new_name}.zip" if m.form == "zip" else new_name)
    if dest.exists() or (set_dir / MEMBERS / (new_name if m.form == "zip" else f"{new_name}.zip")).exists():
        raise Refused(f"'{new_name}' already exists there")
    dest.parent.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(root)
    entry = manifest.pop(m.rel, None)
    subtree = take_subtree(manifest, m.rel)
    if m.form == "zip" and new_name != m.name:
        work = Path(tempfile.mkdtemp(prefix="skillset-rename-")) / new_name
        shutil.copytree(m.folder, work)
        if m.doc != TOP_ROUTER:
            text = (work / m.doc).read_text(encoding="utf-8")
            (work / m.doc).write_text(re.sub(r"^name:.*$", f"name: {new_name}", text, count=1, flags=re.MULTILINE),
                                      encoding="utf-8")
        write_zip(work, dest, new_name)
        remove(root, m.location)
    elif tracked(root, m.rel):
        git(root, "mv", m.rel, dest.relative_to(root).as_posix())
    else:
        m.location.rename(dest)
    if entry is not None:
        manifest[dest.relative_to(root).as_posix()] = entry
    put_subtree(manifest, dest.relative_to(root).as_posix(), subtree)
    save_manifest(root, manifest)
    return dest


def cmd_rename(args) -> int:
    root = args.root
    m = editable(root, args.path)
    set_path, _ = split_path(m.path)
    problems = check_name(args.new)
    if m.path in CORE:
        problems.append(f"'{m.path}' is a core member and keeps its name")
    if problems:
        raise Refused("; ".join(problems))
    dest = relocate(root, m, set_folder_for(root, set_path), args.new)
    new_path = f"{set_path}/{args.new}".strip("/")
    if m.form == "folder":
        pattern = mention_re(m.name)
        for f in tree_files(dest):
            if f.suffix == ".zip":
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            updated = re.sub(rf"^name:\s*{re.escape(m.name)}\s*$", f"name: {args.new}", text, count=1,
                             flags=re.MULTILINE)
            updated = pattern.sub(lambda x: x.group(0).replace(m.name, args.new), updated)
            if updated != text:
                f.write_text(updated, encoding="utf-8")
        new_version = bumped(m.version, "major")
        set_version(dest / m.doc, new_version)
    else:
        new_version = m.version
    notice = root / "NOTICE.md"
    if notice.exists():
        notice.write_text(notice.read_text(encoding="utf-8").replace(f"`{m.path}`", f"`{new_path}`"), "utf-8")
    changelog_add(root, f"- Renamed `{m.path}` to `{new_path}` ({m.version} → {new_version}).")
    write_index(root)
    print(f"renamed {m.path} → {new_path}")
    blocking, info = find_mentions(root, m.name, dest)
    for hit in blocking + info:
        print(f"MENTION {hit}")
    print(f"NEXT update the {len(blocking + info)} mention(s) above" if blocking or info else "NEXT run check")
    return 0


def cmd_move(args) -> int:
    root = args.root
    m = editable(root, args.path)
    if m.path in CORE:
        raise Refused(f"'{m.path}' is a core member and stays at the top")
    target = set_folder_for(root, args.into)
    if target == m.location or m.location in target.parents:
        raise Refused("a skillset cannot be moved into itself")
    relocate(root, m, target, m.name)
    new_path = f"{args.into.strip('/')}/{m.name}".strip("/")
    changelog_add(root, f"- Moved `{m.path}` to `{new_path}`.")
    write_index(root)
    print(f"moved {m.path} → {new_path}")
    return 0


def cmd_retire(args) -> int:
    root = args.root
    m = editable(root, args.path)
    if m.path in CORE:
        raise Refused(f"'{m.path}' is a core member; the skillset cannot sync without it")
    blocking, info = find_mentions(root, m.name, m.location)
    print(f"member      {m.path}  [{m.label}]  version {m.version}")
    for hit in blocking:
        print(f"DEPENDENT   {hit}")
    for hit in info:
        print(f"MENTION     {hit}")
    if args.dry_run:
        print("DRY RUN     nothing changed")
        return 0
    if blocking and not args.allow_mentions:
        raise Refused(f"{len(blocking)} mention(s) in other members, scripts, tests or routers (DEPENDENT above). "
                      "Update those first, or pass --allow-mentions if they are harmless.")
    manifest = load_manifest(root)
    manifest.pop(m.rel, None)
    take_subtree(manifest, m.rel)
    save_manifest(root, manifest)
    remove(root, m.location)
    extra = (f"; replaced by `{args.replaced_by}`" if args.replaced_by else "") + \
            (f"; {args.reason.rstrip('.')}" if args.reason else "")
    restore = f"git checkout $(git rev-list -n 1 HEAD -- {m.rel})^ -- {m.rel}"
    changelog_add(root, f"- Retired `{m.path}` (last version {m.version}{extra}). Restore in a clone with "
                        f"`{restore}`.")
    write_index(root)
    print(f"retired {m.path}")
    return 0


def cmd_pack(args) -> int:
    root = args.root
    m = editable(root, args.path)
    if m.form == "zip":
        raise Refused(f"'{m.path}' is already packed")
    if m.path in CORE:
        raise Refused(f"'{m.path}' is a core member and stays unpacked")
    dest = m.location.with_name(f"{m.name}.zip")
    manifest = load_manifest(root)
    subtree = take_subtree(manifest, m.rel)
    if subtree:  # links inside the member travel with it
        (m.location / MANIFEST).write_text(json.dumps(dict(sorted(subtree.items())), indent=2) + "\n",
                                           encoding="utf-8")
    count = write_zip(m.location, dest, m.name)
    entry = manifest.pop(m.rel, None)
    if entry:
        manifest[dest.relative_to(root).as_posix()] = entry
    save_manifest(root, manifest)
    remove(root, m.location)
    changelog_add(root, f"- Packed `{m.path}` into a zip ({count} files).")
    write_index(root)
    print(f"packed {m.path}: {count} files → {dest.relative_to(root).as_posix()} (1 file in the upload)")
    return 0


def cmd_unpack(args) -> int:
    root = args.root
    m = editable(root, args.path)
    if m.form != "zip":
        raise Refused(f"'{m.path}' is not packed")
    set_path, _ = split_path(m.path)
    manifest = load_manifest(root)
    entry = manifest.get(m.rel, {})
    if entry.get("repo"):
        print(f"NOTE {m.path} was linked to {entry['repo']}; unpacking detaches it (refresh will skip it)")
    work = Path(tempfile.mkdtemp(prefix="skillset-unpack-")) / m.name
    shutil.copytree(m.folder, work)
    place_member(root, work, set_path, m.name, packed=False, trigger=entry.get("trigger") or m.trigger,
                 replace=True)
    manifest = load_manifest(root)
    manifest.pop(f"{m.rel[:-4]}", None)
    save_manifest(root, manifest)
    changelog_add(root, f"- Unpacked `{m.path}` into a folder.")
    write_index(root)
    print(f"unpacked {m.path} → {m.rel[:-4]}")
    return 0


def cmd_import(args) -> int:
    root = args.root
    source = locate_source(Path(args.source).resolve())
    if instructions_in(source):
        data, _ = read(source / instructions_in(source)[0])
        name = args.name or str(data.get("name") or source.name)
        if instructions_in(source)[0] == TOP_ROUTER and not NAME_RE.match(name):
            name = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        m = place_member(root, source, args.into.strip("/"), name, packed=args.packed, trigger=args.trigger,
                         replace=args.replace)
        note_licence(root, m)
        changelog_add(root, f"- Imported `{m.path}` {m.version} as a {m.label}.")
        imported = [m]
    else:
        skills = collection_members(source)
        if not skills:
            raise Refused(f"no skill or skillset found in {args.source}")
        if not (args.name and args.description and args.trigger):
            listing = ", ".join(s.name for s in skills[:12]) + (" ..." if len(skills) > 12 else "")
            raise Refused(f"{args.source} is a collection of {len(skills)} skills ({listing}); pass --name, "
                          "--description and --trigger to import it as a nested skillset")
        set_path = f"{args.into.strip('/')}/{args.name}".strip("/")
        ns = argparse.Namespace(root=root, path=set_path, description=args.description, trigger=args.trigger,
                                title=None)
        if (set_folder_for(root, args.into) / MEMBERS / args.name).exists() and args.replace:
            remove(root, set_folder_for(root, args.into) / MEMBERS / args.name)
        cmd_new(ns, kind="skillset")
        router = set_folder_for(root, set_path) / SET_ROUTER
        text = router.read_text(encoding="utf-8")
        body = (f"# {args.name.replace('-', ' ').capitalize()}\n\nSkills imported from "
                f"{Path(args.source).name}. Pick the member whose \"Use when\" matches the request, then read it.\n")
        router.write_text(text.split("\n# ", 1)[0] + "\n" + body + f"\n## Members\n\n{TABLE_START}\n{TABLE_END}\n",
                          encoding="utf-8")
        imported, skipped = [], []
        for folder in skills:
            data, _ = read(folder / TOP_ROUTER)
            name = str(data.get("name") or folder.name)
            try:
                m = place_member(root, folder, set_path, name, packed=args.packed, trigger=None, replace=False)
            except Refused as exc:
                skipped.append(f"{name}: {exc}")
                continue
            note_licence(root, m)
            imported.append(m)
        for s in skipped:
            print(f"SKIPPED {s}")
        changelog_add(root, f"- Imported `{set_path}`: a collection of {len(imported)} skills.")
    write_index(root)
    for m in imported:
        print(f"imported {m.path}  [{m.label}]  {m.version}  trigger: {m.trigger}")
    print("NEXT check the triggers read well, run `skillset.py check`, and after uploading delete or switch off any "
          "standalone copies so they do not trigger twice")
    return 0


def cmd_add_source(args) -> int:
    origin = {"repo": args.repo, "ref": args.ref, "path": args.path or ""}
    set_path, name = split_path(args.name)
    m = fetch_source(args.root, set_path, name, origin, packed=not args.folder, trigger=args.trigger,
                     replace=args.replace)
    note_licence(args.root, m)
    changelog_add(args.root, f"- Linked `{m.path}` to {args.repo}@{args.ref} ({m.source.get('commit', '')[:10]}).")
    write_index(args.root)
    print(f"linked {m.path}  [{m.label}]  {m.version}  ← {args.repo}@{args.ref} {m.source.get('commit', '')[:10]}")
    return 0


def cmd_refresh(args) -> int:
    root = args.root
    manifest = load_manifest(root)
    wanted = {p.strip("/") for p in args.paths}
    changed = 0
    for rel, entry in sorted(manifest.items()):
        if not entry.get("repo"):
            continue
        location = root / rel
        m = load_member(location, rel, "", manifest)
        parts = rel.split("/")
        path = "/".join(parts[i + 1].removesuffix(".zip") for i in range(0, len(parts) - 1, 2))
        if wanted and path not in wanted:
            continue
        latest = remote_commit(entry["repo"], entry.get("ref", "main"))
        if latest and latest == entry.get("commit"):
            print(f"up to date  {path}  {entry['repo']}@{entry.get('ref')} {latest[:10]}")
            continue
        set_path, name = split_path(path)
        new = fetch_source(root, set_path, name, {**entry, "commit": latest or ""}, packed=m.form == "zip",
                           trigger=entry.get("trigger"), replace=True)
        if new.source.get("commit") == entry.get("commit"):
            print(f"up to date  {path}")
            continue
        changed += 1
        changelog_add(root, f"- Refreshed `{path}` from {entry['repo']}@{entry.get('ref')} "
                            f"({entry.get('commit', '')[:10]} → {new.source.get('commit', '')[:10]}, "
                            f"version {m.version} → {new.version}).")
        print(f"refreshed   {path}  {entry.get('commit', '')[:10]} → {new.source.get('commit', '')[:10]}")
    write_index(root)
    print(f"{changed} linked member(s) updated")
    return 0


def cmd_pull(args) -> int:
    source = Path(args.source).resolve() if args.source else args.root
    if source.is_file():
        source = locate_source(source)
    if not (source / TOP_ROUTER).exists() or not (source / MEMBERS).is_dir():
        raise Refused(f"{source} is not a skillset (needs {TOP_ROUTER} and {MEMBERS}/)")
    name, version = top_info(source)
    dest = (args.dest or Path("/home/claude") / name).resolve()
    if dest.exists():
        if not args.force:
            raise Refused(f"{dest} already exists; use it, or pass --force to replace it")
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    parts = find_parts(source, [source.parent, args.installed, args.installed / "user"])
    merge_parts(source, dest, parts)                      # an upload split into parts becomes one working copy
    if (dest / PACKED_FILE).is_file():
        print(f"unpacked {restore_packed(dest)} zipped group(s) into folders")
    for target in tree_files(dest):
        runnable = target.stat().st_mode & 0o111 or target.read_bytes()[:2] == b"#!"  # uploads can drop the bit
        target.chmod(0o755 if runnable else 0o644)  # installed copies are read-only
    if parts:
        print(f"merged {len(parts)} installed part(s): " + ", ".join(p for _, p in parts))
    write_index(dest)  # restores dotfiles an upload may have dropped
    if shutil.which("git"):
        git(dest, "init", "-q", "-b", "main")
        git(dest, "add", "-A")
        git(dest, *ident(dest), "commit", "-q", "-m", f"baseline: {name} {version}")
        git(dest, "tag", "synced")
    print(f"pulled {name} {version} → {dest}")
    for parent in sorted({p.parent for p in list(args.installed.glob("*/SKILL.md")) +
                          list(args.installed.glob("*/*/SKILL.md"))}):
        if (parent / MEMBERS).is_dir() and parent.resolve() != source.resolve():
            other_name, other_version = top_info(parent)
            if other_name == name or other_name in former_names(source):
                if other_name != name:
                    print(f"installed {parent} is the old name '{other_name}': remove it (and its parts) in Customize → Skills")
                relation = "newer" if vtuple(other_version) > vtuple(version) else \
                    "older" if vtuple(other_version) < vtuple(version) else "same version"
                print(f"installed {parent} {other_version} ({relation})")
    print(f"NEXT work in {dest}; finish with `python3 {dest}/scripts/skillset.py package`")
    return 0


def changed_members(root: Path, since: str) -> tuple[list[str], list[str]]:
    """Folder members changed since SINCE: (sub-skills needing a bump, skillsets to auto-bump)."""
    changed = git(root, "diff", "--cached", "--name-only", since).splitlines()
    leaves, sets = set(), set()
    for p in changed:
        parts = p.split("/")
        for i, part in enumerate(parts[:-1]):
            if part != MEMBERS or i + 1 >= len(parts) - 1:
                continue
            rel = "/".join(parts[:i + 2])
            location = root / rel
            if not location.is_dir():
                continue
            found = instructions_in(location)
            if found and found[1] == "skillset":
                sets.add(rel)
            elif found:
                leaves.add(rel)
    return sorted(leaves), sorted(sets, key=lambda r: -r.count("/"))


def committable_files(root: Path) -> list[Path]:
    """Files git would commit: tracked plus untracked-but-not-ignored. Without git, the upload file set."""
    if (root / ".git").exists() and shutil.which("git"):
        listed = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split("\0")
        return [root / rel for rel in listed if rel and (root / rel).is_file()
                and not set(Path(rel).parts) & SKIP_PARTS and Path(rel).name not in SKIP_FILES]
    return tree_files(root)


# ================================================================ split uploads

PARTS_FILE = "PARTS.json"   # in every upload of a split skillset: which parts exist, and what each must hold


def tree_digest(folder: Path) -> tuple[str, int]:
    """(sha256 over every file's path and content, file count), ignoring PARTS_FILE itself."""
    h, n = hashlib.sha256(), 0
    for f in sorted(tree_files(folder), key=lambda p: p.relative_to(folder).as_posix()):
        rel = f.relative_to(folder).as_posix()
        if rel == PARTS_FILE:
            continue
        h.update(rel.encode("utf-8") + b"\0" + hashlib.sha256(f.read_bytes()).digest())
        n += 1
    return h.hexdigest(), n


def parts_manifest(root: Path) -> dict | None:
    f = root / PARTS_FILE
    if not f.is_file():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise Refused(f"{PARTS_FILE} is unreadable ({exc}); get the upload again") from exc


def verify_parts(root: Path, search: list[Path] | None = None) -> tuple[list[str], list[tuple[Path, str]]]:
    """For an installed split upload: (problems, the parts found). No problems means every part is present and exact."""
    manifest = parts_manifest(root)
    if manifest is None:
        return [], []
    search = search if search is not None else [root.parent, Path("/mnt/skills"), Path("/mnt/skills/user")]
    name = manifest.get("skillset", "")
    repo = f"{name}-repo.zip"
    problems = []
    entries = manifest.get("parts", [])
    main = next((e for e in entries if e.get("prefix") == ""), None)
    if main and tree_digest(root) != (main["sha256"], main["files"]):
        problems.append(f"this upload ({main['name']}) differs from its {PARTS_FILE}: changed after packaging, or "
                        "mixed with another build")
    found = {prefix: folder for folder, prefix in find_parts(root, search)}
    missing = [e for e in entries if e.get("prefix") and e["prefix"] not in found]
    if missing:
        problems.insert(0, f"split upload: {len(missing)} of {len(entries)} parts missing "
                           f"({', '.join(e['name'] for e in missing)}). This {manifest.get('version', '')} upload is one "
                           f"of {len(entries)} skills; install them all, or review or archive {repo}, the complete tree")
    for e in entries:
        if e.get("prefix") and e["prefix"] in found and tree_digest(found[e["prefix"]]) != (e["sha256"], e["files"]):
            problems.append(f"part {e['name']} differs from {PARTS_FILE}: changed after packaging, or from another build")
    return problems, [(found[e["prefix"]], e["prefix"]) for e in entries if e.get("prefix") in found]


def verify_uploads(root: Path, files: list[Path], uploads: list[tuple[Path, int]]) -> None:
    """The release gate: unpack what was written, put it back together, and require it to be the source exactly."""
    with tempfile.TemporaryDirectory() as tmp:
        installed = Path(tmp) / "skills"
        for path, _ in uploads:
            with zipfile.ZipFile(path) as zf:
                extract_all(zf, installed)
        name = top_info(root)[0]
        main = installed / name
        problems, parts = verify_parts(main, [installed])
        if problems:
            raise Refused("the uploads just written do not verify: " + "; ".join(problems))
        merged = Path(tmp) / "merged"
        merge_parts(main, merged, parts)
        if (merged / PACKED_FILE).is_file():
            restore_packed(merged)
        want = {f.relative_to(root).as_posix(): f.read_bytes() for f in files}
        got = {f.relative_to(merged).as_posix(): f.read_bytes() for f in tree_files(merged)}
        if want != got:
            lost = sorted(set(want) - set(got))[:3]
            extra = sorted(set(got) - set(want))[:3]
            changed = sorted(k for k in set(want) & set(got) if want[k] != got[k])[:3]
            raise Refused(f"the uploads do not rebuild the skillset (missing {lost}, extra {extra}, changed {changed}); "
                          "nothing should be delivered")
        errors, _ = check_skillset(merged)
        if errors:
            raise Refused("the rebuilt skillset fails its checks: " + "; ".join(errors[:3]))



def plan_parts(root: Path, files: list[Path]) -> list[tuple[str, list[Path]]]:
    """Split the upload when it is over SPLIT_AT files: [(folder prefix, files)], '' being the main skill.

    A unit over the limit gives every member folder at its level its own part (core members stay in the main
    skill); any part still over the limit is split the same way, one level down."""
    rels = {f.relative_to(root).as_posix(): f for f in files}
    parts: dict[str, set[str]] = {}

    def split(prefix: str, owned: set[str]) -> set[str]:
        if len(owned) <= SPLIT_AT:
            return owned
        base = (prefix + "/" if prefix else "") + MEMBERS + "/"
        folders = sorted({base + r[len(base):].split("/")[0] for r in owned
                          if r.startswith(base) and "/" in r[len(base):]})
        folders = [d for d in folders if not (prefix == "" and d.split("/")[-1] in CORE)]
        if not folders:
            raise Refused(f"'{prefix or 'the top'}' holds {len(owned)} files and has no member folder to split off "
                          f"(the limit per upload part is {SPLIT_AT}); pack its largest member")
        for d in folders:
            sub = {r for r in owned if r.startswith(d + "/")}
            owned = owned - sub
            parts[d] = split(d, sub)
        if len(owned) > SPLIT_AT:
            raise Refused(f"'{prefix or 'the top'}' still holds {len(owned)} files of its own after splitting")
        return owned

    main = split("", set(rels))
    out = [("", [rels[r] for r in sorted(main)])]
    out += [(d, [rels[r] for r in sorted(fs)]) for d, fs in sorted(parts.items())]
    return out


def part_name(top: str, prefix: str) -> str:
    """skillset-os + subskills/software-dev/subskills/tools -> skillset-os-software-dev-tools."""
    name = f"{top}-" + "-".join(p for p in prefix.split("/") if p != MEMBERS)
    return name if len(name) <= 64 else name[:55].rstrip("-") + "-" + hashlib.sha1(prefix.encode()).hexdigest()[:8]


def part_wrapper(root: Path, top: str, version: str, prefix: str, files: list[Path], inner: list[str]) -> str:
    """The generated SKILL.md of an upload part: it discusses and audits its folder."""
    loc = root / prefix
    found = instructions_in(loc)
    path = "/".join(p for p in prefix.split("/") if p != MEMBERS)
    what, rows = "", []
    if found:
        data, _ = read(loc / found[0])
        what = shorten(first_sentence(VERSION_NOTE_RE.sub("", " ".join(str(data.get("description") or "").split()))), 180)
        if found[1] == "skillset":
            for m in members_of(loc, root, path, load_manifest(root)):
                n = sum(1 for f in files if m.location in f.parents or f == m.location)
                rows.append(f"| `{m.path}` | {m.label} | {m.version} | {n} | {shorten(m.description, 110).replace('|', '/')} |")
    desc = (f"Part of the {top} skillset {version}: the folder {path} ({len(files)} files). {what} Lists and discusses "
            f"what that folder holds, and audits it for quality and problems, when asked what is in "
            f"{path.split('/')[-1]} or to review, audit or check it. Its skills are used through the main {top} skill.")
    desc = shorten(" ".join(desc.replace("<", "(").replace(">", ")").split()), MAX_DESCRIPTION)
    body = [f"# {top} part: `{prefix}/`", "",
            (f"This upload holds `{prefix}/` of the **{top}** skillset {version}, with every path unchanged. It was split "
            f"off because the whole skillset has more than {SPLIT_AT} files and claude.ai accepts at most {MAX_FILES} per "
            f"skill. Install it together with the main `{top}` skill, whose `scripts/skillset.py` treats all installed "
            "parts as one skillset."), ""]
    if inner:
        body += ["Deeper folders were split off again into their own parts: " + ", ".join(f"`{p}/`" for p in inner) + ".", ""]
    body += ["## What this folder holds", ""]
    if rows:
        body += ["| Member | Kind | Version | Files | What it is |", "|---|---|---|---|---|", *rows, ""]
    elif what:
        body += [what, ""]
    body += ["## When asked what is here", "",
             (f"Look, don't recall. Run `python3 <main {top} skill>/scripts/skillset.py contents {path}`, or list "
             f"`{prefix}/` next to this file, and read the files the question is about. Answer from what they say."), "",
             "## When asked to review or audit it", "",
             (f"1. Run `python3 <main {top} skill>/scripts/skillset.py review {path}` for the automatic findings: broken "
             "links, missing descriptions or triggers, over-long instructions, leftover TODOs, scripts that do not "
             "compile, invalid JSON and anything that looks like a secret."),
             ("2. Then read each member's instructions and supporting files yourself. Check that descriptions are accurate "
             "and specific, that steps are clear, complete and consistent with each other and with the rest of the "
             "skillset, that examples and commands are correct, and that nothing is out of date or duplicated."),
             ("3. Report every finding by severity (problem, risk, suggestion), each with its file and line and a concrete "
             "fix. Change nothing unless asked; changes go through the main skill's `sync-skillset` member, in the "
             "full working copy it pulls."), ""]
    front = ["---", f"name: {part_name(top, prefix)}", f"description: {quote(desc)}", "metadata:",
             f"  {PART_KEY}: {quote(top)}", f"  part-path: {quote(prefix)}", f"  version: {quote(version)}", "---", ""]
    return "\n".join(front + body)


def is_part_zip(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as zf:
            docs = [n for n in zf.namelist() if n.count("/") == 1 and n.endswith("/" + TOP_ROUTER)]
            return any(f"{PART_KEY}:" in zf.read(n).decode("utf-8", "replace") for n in docs)
    except (zipfile.BadZipFile, OSError):
        return False


PACKED_FILE = "PACKED.json"   # in an upload whose largest groups were zipped to fit claude.ai's file limit
PACKED_NOTE = "\n## Packed groups\n"


def plan_packing(root: Path, files: list[Path]) -> list[str]:
    """Member folders to zip inside the upload, largest first, until it holds at most SPLIT_AT files."""
    rels = [f.relative_to(root).as_posix() for f in files]
    count = len(rels) + 1                                   # + PACKED.json
    if count - 1 <= SPLIT_AT:
        return []
    base = MEMBERS + "/"
    groups: dict[str, int] = {}
    for r in rels:
        if r.startswith(base) and "/" in r[len(base):]:
            name = r[len(base):].split("/")[0]
            if name not in CORE:
                groups[base + name] = groups.get(base + name, 0) + 1
    chosen = []
    for g, n in sorted(groups.items(), key=lambda x: (-x[1], x[0])):
        if count <= SPLIT_AT:
            break
        chosen.append(g)
        count -= n - 1
    if count > SPLIT_AT:
        raise Refused(f"even with every group zipped the upload would hold {count} files (limit {SPLIT_AT}); "
                      "move top-level files into members, or package with --split")
    return sorted(chosen)


def write_packed_upload(root: Path, main_path: Path, top: str, version: str, files: list[Path],
                        packs: list[str]) -> int:
    """One upload: the tree with PACKS zipped in place, routers regenerated for them, and PACKED.json."""
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp) / top
        for f in files:
            (staged / f.relative_to(root)).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, staged / f.relative_to(root))
        manifest = load_manifest(staged)
        before = dict(manifest)
        entries = []
        for rel in packs:
            loc = staged / rel
            digest, count = tree_digest(loc)
            subtree = take_subtree(manifest, rel)
            if subtree:                                     # links inside the group travel with it, as `pack` does
                (loc / MANIFEST).write_text(json.dumps(dict(sorted(subtree.items())), indent=2) + "\n", encoding="utf-8")
            write_zip(loc, loc.with_name(loc.name + ".zip"), loc.name)
            entry = manifest.pop(rel, None)
            if entry:
                manifest[rel + ".zip"] = entry
            shutil.rmtree(loc)
            entries.append({"path": rel, "files": count, "sha256": digest, "nested_manifest": bool(subtree)})
        if manifest != before:
            save_manifest(staged, manifest)
        write_index(staged)                                 # routers now point at the zips
        doc = staged / TOP_ROUTER
        note = [PACKED_NOTE.strip("\n"), "",
                ("To fit claude.ai's file limit, these groups are zipped inside this upload: "
                 + ", ".join(f"`{e['path']}.zip`" for e in entries)
                 + ". Read their members with `python3 <top>/scripts/skillset.py open <path>`, which unzips them with "
                 "Python (so code execution must be on); `tree`, `contents` and `review` see through them too. "
                 f"`pull` unpacks them into ordinary folders for editing, and `{PACKED_FILE}` lets `check` confirm "
                 "each zip holds exactly what was packaged.")]
        doc.write_text(doc.read_text(encoding="utf-8").rstrip("\n") + "\n" + "\n".join(note) + "\n", encoding="utf-8")
        (staged / PACKED_FILE).write_text(json.dumps({"skillset": top, "version": version, "packed": entries},
                                                     indent=2) + "\n", encoding="utf-8")
        return write_zip(staged, main_path, top, tree_files(staged))


def restore_packed(dest: Path) -> int:
    """Turn a packed upload (a writable copy) back into the plain tree: unzip each group and verify it."""
    data = json.loads((dest / PACKED_FILE).read_text(encoding="utf-8"))
    manifest = load_manifest(dest)
    before = dict(manifest)
    for e in data.get("packed", []):
        folder, z = dest / e["path"], dest / (e["path"] + ".zip")
        if not z.is_file():
            raise Refused(f"packed group {e['path']}.zip is missing from this upload")
        with zipfile.ZipFile(z) as zf:
            extract_all(zf, folder.parent)
        z.unlink()
        nested = folder / MANIFEST
        if e.get("nested_manifest") and nested.is_file():
            put_subtree(manifest, e["path"], json.loads(nested.read_text(encoding="utf-8")))
            nested.unlink()
        entry = manifest.pop(e["path"] + ".zip", None)
        if entry:
            manifest[e["path"]] = entry
        if tree_digest(folder) != (e["sha256"], e["files"]):
            raise Refused(f"packed group {e['path']}.zip differs from {PACKED_FILE}: changed after packaging, or "
                          "from another build")
    if manifest != before:
        save_manifest(dest, manifest)
    (dest / PACKED_FILE).unlink()
    doc = dest / TOP_ROUTER
    text = doc.read_text(encoding="utf-8")
    if PACKED_NOTE in text:
        doc.write_text(text.split(PACKED_NOTE)[0].rstrip("\n") + "\n", encoding="utf-8")
    write_index(dest)
    return len(data.get("packed", []))


def write_uploads(root: Path, out_dir: Path, top: str, version: str, files: list[Path],
                  main_path: Path | None = None, split: bool = False) -> list[tuple[Path, int]]:
    """Write the upload zip(s): one when the skillset fits in SPLIT_AT files, else the main skill plus parts."""
    main_path = (main_path or out_dir / f"{top}.zip").resolve()
    files = [f for f in files if f.resolve() != main_path and not f.name.endswith((".zip.part",))
             and not (f.parent.resolve() == main_path.parent and is_part_zip(f))]
    for old in out_dir.glob(f"{top}-*.zip"):           # parts of an earlier build
        if is_part_zip(old):
            old.unlink()
    if len(files) <= SPLIT_AT:
        return [(main_path, write_zip(root, main_path, top, files))]
    if not split:
        return [(main_path, write_packed_upload(root, main_path, top, version, files, plan_packing(root, files)))]
    plan = plan_parts(root, files)
    if len(plan) == 1:
        return [(main_path, write_zip(root, main_path, top, files))]
    prefixes = [p for p, _ in plan if p]
    uploads = []
    with tempfile.TemporaryDirectory() as tmp:
        def stage(dest: Path, fs: list[Path]) -> None:
            for f in fs:
                (dest / f.relative_to(root)).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest / f.relative_to(root))
        staged = Path(tmp) / top
        stage(staged, plan[0][1])
        top_doc = staged / TOP_ROUTER
        note = ["", "## Installed in parts", "",
                (f"This upload of {top} {version} is one of {len(plan)} skills: the skillset has more than {SPLIT_AT} "
                 "files, so these folders are in separate skills. Install all of them. `scripts/skillset.py` finds them "
                 f"wherever they are installed, so `check`, `open`, `contents`, `review` and `pull` see one skillset, and "
                 f"`{PARTS_FILE}` lets `check` confirm each part is complete and unchanged. Reviewing this upload on its own? "
                 f"It is incomplete by design; the complete tree is `{top}-repo.zip`."), ""]
        note += [f"- `{p}/` in the skill **{part_name(top, p)}**" for p in prefixes]
        top_doc.write_text(top_doc.read_text(encoding="utf-8").rstrip("\n") + "\n" + "\n".join(note) + "\n",
                           encoding="utf-8")
        dirs = [("", top, staged)]
        for prefix, pfiles in plan[1:]:
            pname = part_name(top, prefix)
            pdir = Path(tmp) / pname
            stage(pdir, pfiles)
            inner = [p for p in prefixes if p.startswith(prefix + "/")]
            (pdir / TOP_ROUTER).write_text(part_wrapper(root, top, version, prefix, pfiles, inner), encoding="utf-8")
            dirs.append((prefix, pname, pdir))
        manifest = {"skillset": top, "version": version, "parts": []}
        for prefix, pname, d in dirs:
            digest, count = tree_digest(d)
            manifest["parts"].append({"name": pname, "prefix": prefix, "files": count, "sha256": digest})
        text = json.dumps(manifest, indent=2) + "\n"
        for prefix, pname, d in dirs:
            (d / PARTS_FILE).write_text(text, encoding="utf-8")
            dest = main_path if prefix == "" else out_dir / f"{pname}.zip"
            uploads.append((dest, write_zip(d, dest, pname, tree_files(d))))
    return uploads


def find_parts(root: Path, search: list[Path]) -> list[tuple[Path, str]]:
    """Installed upload parts of the skillset at ROOT: [(part folder, its path prefix)]."""
    name, version = top_info(root)
    found = set()
    for base in search:
        if not base.is_dir():
            continue
        for doc in list(base.glob(f"*/{TOP_ROUTER}")) + list(base.glob(f"*/*/{TOP_ROUTER}")):
            if doc.parent.resolve() == root.resolve():
                continue
            try:
                data, _ = read(doc)
            except Refused:
                continue
            meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
            if str(meta.get(PART_KEY) or "") != name or not meta.get("part-path"):
                continue
            if version_of(data) != version:
                print(f"note: {doc.parent} is part of {name} {version_of(data)}, not {version}; skipped", file=sys.stderr)
                continue
            found.add((doc.parent.resolve(), str(meta["part-path"])))
    return sorted(found, key=lambda x: x[1])


def merge_parts(root: Path, dest: Path, parts: list[tuple[Path, str]]) -> None:
    """Copy the main skill and its parts into DEST as one skillset (dropping the upload-only notes)."""
    for base, skip in [(root, None)] + [(p, Path(TOP_ROUTER)) for p, _ in parts]:
        for f in tree_files(base):
            rel = f.relative_to(base)
            if rel == skip or rel == Path(PARTS_FILE):
                continue
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
    top = dest / TOP_ROUTER
    text = top.read_text(encoding="utf-8")
    if "\n## Installed in parts\n" in text:
        top.write_text(text.split("\n## Installed in parts\n")[0].rstrip("\n") + "\n", encoding="utf-8")


def installed_view(root: Path) -> Path:
    """The skillset as one tree: ROOT itself, or a merged copy when its parts are installed beside it."""
    if parts_manifest(root) is not None:
        _problems, parts = verify_parts(root)
    else:
        parts = find_parts(root, [root.parent, Path("/mnt/skills"), Path("/mnt/skills/user")])
    if not parts and not (root / PACKED_FILE).is_file():
        return root
    name, version = top_info(root)
    dest = CACHE / f"merged-{name}-{version}"
    if dest.exists():
        shutil.rmtree(dest)
    merge_parts(root, dest, parts)
    if (dest / PACKED_FILE).is_file():
        restore_packed(dest)                    # zipped groups become folders again, verified against PACKED.json
    return dest


def cmd_build(args) -> int:
    """Zip the skillset as it would be committed into an upload for Claude, overwriting the last build.

    Only files git would commit go in, so gitignored secrets such as .env never reach an upload. The default
    output, <root>/<name>.zip, is itself gitignored (/*.zip), so building never dirties the repository.
    """
    root = args.root
    errors, _ = check_skillset(root)
    if errors:
        raise Refused(f"{len(errors)} check error(s); run `skillset.py check` and fix them before building")
    name, version = top_info(root)
    out = (args.out or root / f"{name}.zip").resolve()
    files = [f for f in committable_files(root) if f.resolve() != out and not f.name.endswith(".zip.part")]
    if not (root / ".git").exists():
        print("note: no git repository here, so .gitignore could not be applied; check the file list", file=sys.stderr)
    uploads = write_uploads(root, out.parent, name, version, files, main_path=out, split=args.split)
    verify_uploads(root, [f for f in files if f.resolve() != out.resolve() and not is_part_zip(f)], uploads)
    for p, count in uploads:
        print(f"built {p} ({count} files, version {version}); upload it in Customize → Skills")
    if len(uploads) > 1:
        print(f"note one skillset in {len(uploads)} uploads; install them all. {out.name} alone is incomplete by design")
    return 0


def cmd_package(args) -> int:
    root = args.root
    write_index(root)
    name, version = top_info(root)
    since = args.since or ("synced" if ref_exists(root, "synced") else None)
    if since and not ref_exists(root, since):
        raise Refused(f"--since {since} is not a commit in this working copy")
    changed: list[str] = []
    log_now = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    log_base = (file_at(root, since, "CHANGELOG.md") if since and ref_exists(root, since) else None) or log_now
    never_released = "## Unreleased" in log_base and not re.search(r"^## \d+\.\d+\.\d+ ", log_base, re.MULTILINE)
    prerelease = never_released and not args.release
    if never_released:
        # Before the first release everything stays at its starting version: no bumps are demanded or made, and
        # changes collect under "## Unreleased" until `package --release` ships that version as it is.
        if since:
            git(root, "add", "-A")
            changed = git(root, "diff", "--cached", "--name-only", since).splitlines()
        if prerelease:
            if args.message and (changed or not since):
                changelog_add(root, f"- {args.message.rstrip('.')}.")
            print(f"pre-release: {name} stays {version}, unreleased (`package --release` ships it)")
        since_for_bumps = None
    else:
        since_for_bumps = since
    if since_for_bumps:
        git(root, "add", "-A")
        changed = git(root, "diff", "--cached", "--name-only", since).splitlines()
        leaves, sets = changed_members(root, since)
        stale = []
        for rel in leaves:
            doc = instructions_in(root / rel)[0]
            before = file_at(root, since, f"{rel}/{doc}")
            only_doc = [c for c in changed if c.startswith(rel + "/")] == [f"{rel}/{doc}"]
            if before is not None and only_doc and strip_folder_block(before) == \
                    strip_folder_block((root / rel / doc).read_text(encoding="utf-8")):
                continue   # only its generated "This folder" section changed
            if before is not None and vtuple(version_of(read(root / rel / doc)[0])) <= \
                    vtuple(version_of(parse(before)[0])):
                stale.append(rel)
        if stale:
            git(root, "reset", "-q")
            raise Refused("these sub-skills changed without a version bump: " + ", ".join(stale) +
                          ". Run `skillset.py bump PATH --part patch|minor` for each, then package again.")
        for rel in sets:  # nested skillsets rise automatically with their contents
            before = file_at(root, since, f"{rel}/{SET_ROUTER}")
            now = version_of(read(root / rel / SET_ROUTER)[0])
            if before is not None and vtuple(now) <= vtuple(version_of(parse(before)[0])):
                set_version(root / rel / SET_ROUTER, bumped(now, "patch"))
                print(f"skillset {rel} → {bumped(now, 'patch')}")
        before_top = file_at(root, since, TOP_ROUTER)
        base = version_of(parse(before_top)[0]) if before_top else "0"
        if never_released and vtuple(version) >= vtuple(base) and not args.bump:
            pass   # the first release is the version the skillset starts at (a fresh 1.0.0 ships as 1.0.0)
        elif changed and vtuple(version) <= vtuple(base):
            version = bumped(max(version, base, key=vtuple), args.bump or "patch")
    elif args.bump and not prerelease:
        version = bumped(version, args.bump)
    if version != top_info(root)[1]:
        set_version(root / TOP_ROUTER, version)
        print(f"version → {version}")
    if not prerelease and (changed or not since or never_released):
        if args.message:
            changelog_add(root, f"- {args.message.rstrip('.')}.")
        changelog_release(root, version)
    write_index(root)

    errors, warnings = check_skillset(root)
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        raise Refused("check failed:\n" + "\n".join(f"  - {e}" for e in errors))
    print("ok   check")
    if not args.skip_tests:
        if shutil.which("ruff"):
            r = subprocess.run(["ruff", "check", "."], cwd=root, capture_output=True, text=True, check=False)
            if r.returncode:
                raise Refused(f"ruff failed:\n{r.stdout}{r.stderr}")
            print("ok   ruff")
        if (root / "tests").is_dir():
            r = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root, capture_output=True, text=True,
                               check=False)
            if r.returncode:
                raise Refused(f"pytest failed:\n{r.stdout[-3000:]}{r.stderr[-1000:]}")
            print(f"ok   pytest: {r.stdout.strip().splitlines()[-1]}")

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    written = []
    if has_git(root):
        git(root, "add", "-A")
        if git(root, "status", "--porcelain"):
            git(root, *ident(root), "commit", "-q", "-m",
                f"release: {name} {version}" + (f": {args.message}" if args.message else ""))
            print(f"ok   commit {git(root, 'log', '--oneline', '-1')}")
        if since and git(root, "rev-list", "--count", f"{since}..HEAD") != "0":
            patch = out / f"{name}-{version}.patch"
            patch.write_text(git(root, "format-patch", "--binary", f"{since}..HEAD", "--stdout") + "\n",
                             encoding="utf-8")
            written.append(patch)
    files = committable_files(root)
    uploads = write_uploads(root, out, name, version, files, split=args.split)
    verify_uploads(root, [f for f in files if not (f.suffix == ".zip" and f.parent == root)], uploads)
    print(f"ok   release gate: the {len(uploads)} upload(s) unpack and merge back into this exact skillset")
    written[0:0] = [p for p, _ in uploads]
    if (root / "memory").is_dir() and (HERE / "memory.py").is_file():
        mem = memory_module()
        pack = mem.export(root, out / "memory-pack.zip")
        ok, report = mem.acceptance(mem.read_pack(pack)[1])
        if not ok:
            raise Refused("the self-memory pack fails its acceptance test: " + "; ".join(r for r in report if r.startswith("FAIL")))
        written.append(pack)
        print("ok   memory-pack.zip: the takeover questions can be answered, and no personal dossier travels with it")
    for p, count in uploads:
        print(f"ok   {p.name}: {count} files, version {version}")
    if len(uploads) > 1 or len(files) > SPLIT_AT:
        repo_zip = out / f"{name}-repo.zip"            # the plain tree in one zip, for GitHub (the upload differs)
        count = write_zip(root, repo_zip, name)
        written.insert(len(uploads), repo_zip)
        print(f"ok   {repo_zip.name}: {count} files, the plain tree for GitHub and for review")
        if len(uploads) > 1:
            print(f"note {len(uploads)} uploads: packaged with --split, so each part is its own skill. Upload all of "
                  f"them. To review or archive the skillset, use {repo_zip.name}: {name}.zip alone is incomplete.")
        else:
            print(f"note one upload with zipped groups (over {SPLIT_AT} files). Reading them needs code execution. "
                  f"For GitHub or a review, use {repo_zip.name}.")
    print("\nDELIVERED")
    for p in written:
        print(f"  {p}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=HERE.parent, help="top folder (default: the folder above scripts/)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("index")
    p = sub.add_parser("tree")
    p.add_argument("--depth", type=int)
    p = sub.add_parser("open")
    p.add_argument("path")
    p = sub.add_parser("contents", help="list a folder's files with a line on what each is")
    p.add_argument("path", nargs="?", default=".", help="member path, folder inside the skillset, or . for the top")
    p.add_argument("--depth", type=int, help="how many folder levels to show (default: all)")
    p = sub.add_parser("review", help="audit a folder's files for problems")
    p.add_argument("path", nargs="?", default=".", help="member path, folder inside the skillset, or . for the top")
    for cmd in ("new", "new-set"):
        p = sub.add_parser(cmd)
        p.add_argument("path", help="member path, e.g. team/meeting-minutes")
        p.add_argument("--description", required=True)
        p.add_argument("--trigger", required=True, help="short 'Use when' phrase for the parent's description")
        p.add_argument("--title")
    p = sub.add_parser("bump")
    p.add_argument("path")
    p.add_argument("--part", choices=["patch", "minor", "major"], default="patch")
    p.add_argument("--message")
    p = sub.add_parser("replace", help="replace one exact passage in a member's file, then optionally bump it")
    p.add_argument("path", help="member path, e.g. cognition/reasoning/research")
    p.add_argument("--old", help="the exact passage; it must occur exactly once")
    p.add_argument("--new", help="the replacement")
    p.add_argument("--old-file", help="read the passage from this file instead (for multi-line text)")
    p.add_argument("--new-file", help="read the replacement from this file instead")
    p.add_argument("--file", help="a file in the member's folder other than its instructions file")
    p.add_argument("--part", choices=["patch", "minor", "major"], help="bump the member after a successful edit")
    p.add_argument("--message", help="changelog line for the bump")
    p = sub.add_parser("build", help="zip the skillset as it would be committed into an upload for Claude")
    p.add_argument("--out", type=Path, help="output zip (default: <root>/<name>.zip, which is gitignored)")
    p.add_argument("--split", action="store_true", help="over the limit, write part skills instead of zipping groups")
    p = sub.add_parser("rename")
    p.add_argument("path")
    p.add_argument("new")
    p = sub.add_parser("move")
    p.add_argument("path")
    p.add_argument("--into", required=True, help="destination skillset path ('' for the top)")
    p = sub.add_parser("retire")
    p.add_argument("path")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--reason")
    p.add_argument("--replaced-by")
    p.add_argument("--allow-mentions", action="store_true")
    for cmd in ("pack", "unpack"):
        sub.add_parser(cmd).add_argument("path")
    p = sub.add_parser("import")
    p.add_argument("source", help="skill, skillset, repository or collection: folder, .zip or .skill")
    p.add_argument("--into", default="", help="skillset to import into (default: the top)")
    p.add_argument("--name")
    p.add_argument("--trigger")
    p.add_argument("--description", help="for a collection: the new nested skillset's description")
    p.add_argument("--packed", action="store_true", help="store as a zip (one file in the upload)")
    p.add_argument("--replace", action="store_true")
    p = sub.add_parser("add-source")
    p.add_argument("name", help="member path, e.g. team/their-skills")
    p.add_argument("--repo", required=True, help="GitHub owner/name")
    p.add_argument("--ref", default="main", help="branch, tag or commit (default: main)")
    p.add_argument("--path", help="folder inside the repository holding the skill or skillset")
    p.add_argument("--trigger")
    p.add_argument("--folder", action="store_true", help="store unpacked instead of as a zip")
    p.add_argument("--replace", action="store_true")
    p = sub.add_parser("refresh")
    p.add_argument("paths", nargs="*", help="linked members to refresh (default: all)")
    p = sub.add_parser("pull")
    p.add_argument("--source", help="skillset folder or zip (default: the one this script is in)")
    p.add_argument("--dest", type=Path, help="working copy (default: /home/claude/NAME)")
    p.add_argument("--force", action="store_true")
    p.add_argument("--installed", type=Path, default=Path("/mnt/skills"), help="where to look for other copies")
    p = sub.add_parser("package")
    p.add_argument("--out", type=Path, default=Path("/mnt/user-data/outputs"))
    p.add_argument("--bump", choices=["patch", "minor", "major"], help="top version part (default: patch)")
    p.add_argument("--message", help="one line for the changelog and commit")
    p.add_argument("--since", help="commit to diff against (default: the 'synced' tag made by pull)")
    p.add_argument("--skip-tests", action="store_true", help="skip ruff and pytest (used by the tests)")
    p.add_argument("--split", action="store_true", help="over the limit, write part skills instead of zipping groups")
    p.add_argument("--release", action="store_true", help="ship a never-released skillset's version (else it stays unreleased)")
    args = ap.parse_args(argv)
    args.root = args.root.resolve()
    commands = {"check": cmd_check, "index": cmd_index, "tree": cmd_tree, "open": cmd_open, "new": cmd_new,
                "new-set": lambda a: cmd_new(a, kind="skillset"), "bump": cmd_bump, "replace": cmd_replace, "build": cmd_build, "rename": cmd_rename,
                "move": cmd_move, "retire": cmd_retire, "pack": cmd_pack, "unpack": cmd_unpack,
                "import": cmd_import, "add-source": cmd_add_source, "refresh": cmd_refresh, "pull": cmd_pull,
                "package": cmd_package, "contents": cmd_contents, "review": cmd_review}
    if args.cmd != "pull" and not (args.root / TOP_ROUTER).exists():
        print(f"error: {args.root} has no {TOP_ROUTER}; pass --root with the skillset folder", file=sys.stderr)
        return 2
    if args.cmd in ("open", "tree", "contents", "review") and not (args.root / ".git").exists():
        args.root = installed_view(args.root)   # an installed upload split into parts reads as one skillset
    try:
        return commands[args.cmd](args)
    except Refused as exc:
        print(f"REFUSED {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

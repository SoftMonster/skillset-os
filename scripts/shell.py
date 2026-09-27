#!/usr/bin/env python3
"""Skillset-OS shell: a command line over the AI's own skills.

It shows the skillset as a file system (members as folders, their SUBSKILL.md and files inside) and understands
the everyday commands of bash/sh/zsh, PowerShell and Windows cmd: ls/dir/Get-ChildItem, cd/Set-Location,
pwd, cat/type/Get-Content, head, tail, tree, find, grep/Select-String/findstr, wc, stat, which/Get-Command,
man/help, history, alias, echo, with simple pipes (| grep, head, tail, sort, uniq, wc).

Nothing runs on the real system and no file changes. Edits (touch, echo > file, sed -i, rm, mv, cp, mkdir,
Set-Content, Add-Content, New-Item, Remove-Item...) are REMEMBERED in a journal and shown as if applied;
`apply --wc DIR` writes them into a working copy when an updated repository is requested.

Anything that is not a shell command is read as a VERB-NOUN command ("review code", "plan feature",
"create spreadsheet", "recall lessons") and resolved to the member, built-in skill or model tool that does it.

Usage:
  shell.py run "<command line>"          run one command line (state persists between calls)
  shell.py do "<verb noun>"              resolve a verb-noun command
  shell.py commands [--top N] [--all]    the most useful commands, generated from what the skillset knows
  shell.py edit PATH (--content TEXT | --content-file F | --delete)   record a full-content edit
  shell.py journal | diff | drop N | clear-journal
  shell.py apply --wc DIR                write the remembered edits into a working copy
  shell.py favourites add|remove|list|save|load|clear [...]   the person's own command list (session only)
  shell.py mode [shell|english|auto]     how messages are read
  shell.py reset                         forget the session (cwd, history, journal, favourites)
State lives in $SKILLSET_SHELL_HOME (default /home/claude/.skillset-shell): this session only, never self-memory.
"""
from __future__ import annotations

import argparse
import difflib
import fnmatch
import importlib.util
import json
import os
import re
import shlex
import shutil
import signal
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MEMBERS = "subskills"
STATE_HOME = Path(os.environ.get("SKILLSET_SHELL_HOME", "/home/claude/.skillset-shell"))
INSTALLED_SKILLS = [Path(p) for p in os.environ.get(
    "SKILLSET_SHELL_SKILLS", "/mnt/skills/public:/mnt/skills/examples:/mnt/skills/user:/mnt/skills/plugins").split(":")]
FAV_FILE = "my-commands.md"
FAV_MARK = "<!-- skillset-os command list -->"


class ShellError(Exception):
    """A command failed; the message is what the shell prints."""


# ================================================================ helpers loaded from beside this file

def _load(name: str, filename: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def skillset():
    mod = sys.modules.get("skillset")
    if mod is not None and Path(getattr(mod, "__file__", "")).resolve() == (HERE / "skillset.py"):
        return mod
    return _load("skillset", "skillset.py")


def memory():
    return _load("skillset_memory", "memory.py")


def cmdb():
    return _load("skillset_commands", "commands.py")


def db(view: View):
    """The command database for VIEW's tree, rebuilt when any member's file (or a remembered edit) changes it."""
    ss = skillset()
    docs = [("", view.root / "SKILL.md")]
    for _d, m in ss.walk(view.root):
        if not m.error and m.folder is not None:
            docs.append((m.path, m.folder / m.doc))
    return cmdb().open_db(STATE_HOME / "commands.db", docs, lambda: catalogue(view.root))


def db_quiet(state: dict):
    """The database, or None where it cannot be opened (a bare state, a missing tree)."""
    try:
        return db(View(state))
    except Exception:  # noqa: BLE001 - the session list still works without the database
        return None


# ================================================================ session state

def load_state() -> dict:
    f = STATE_HOME / "state.json"
    state = {"cwd": "/", "stack": [], "history": [], "journal": [], "aliases": {}, "favourites": [], "mode": "auto"}
    if f.is_file():
        try:
            state.update(json.loads(f.read_text(encoding="utf-8")))
        except ValueError:
            pass
    return state


def save_state(state: dict) -> None:
    STATE_HOME.mkdir(parents=True, exist_ok=True)
    (STATE_HOME / "state.json").write_text(json.dumps(state, indent=1), encoding="utf-8")


# ================================================================ the view: skillset + remembered edits

def base_root() -> Path:
    """The skillset as one plain tree (installed parts merged and zips opened), read-only."""
    ss = skillset()
    return ROOT if (ROOT / ".git").exists() else ss.installed_view(ROOT)


def apply_journal(target: Path, journal: list[dict]) -> list[str]:
    """Apply remembered edits to TARGET (a writable tree). Returns notes about memory candidates."""
    notes = []
    for op in journal:
        kind, rel = op["op"], op.get("path", "")
        dest = target / rel if rel else target
        if target.resolve() not in (dest.resolve().parents) and dest.resolve() != target.resolve():
            raise ShellError(f"{rel}: outside the skillset")
        if kind in ("write", "append", "touch"):
            dest.parent.mkdir(parents=True, exist_ok=True)
            if kind == "write":
                dest.write_text(op["content"], encoding="utf-8")
            elif kind == "append":
                with dest.open("a", encoding="utf-8") as fh:
                    fh.write(op["content"])
            elif not dest.exists():
                dest.write_text("", encoding="utf-8")
        elif kind == "replace":
            if dest.is_file():
                text = dest.read_text(encoding="utf-8")
                dest.write_text(re.sub(op["pattern"], op["replacement"], text, count=0 if op.get("all") else 1),
                                encoding="utf-8")
        elif kind == "delete":
            if dest.is_dir():
                shutil.rmtree(dest)
            elif dest.exists():
                dest.unlink()
        elif kind in ("move", "copy"):
            to = target / op["to"]
            to.parent.mkdir(parents=True, exist_ok=True)
            if kind == "move" and dest.exists():
                shutil.move(str(dest), str(to))
            elif dest.is_dir():
                shutil.copytree(dest, to, dirs_exist_ok=True)
            elif dest.exists():
                shutil.copy2(dest, to)
        elif kind == "mkdir":
            dest.mkdir(parents=True, exist_ok=True)
        elif kind == "memory":
            notes.append(op["summary"])
    return notes


class View:
    """The tree the shell shows: the skillset with the journal applied on top (in a scratch copy)."""

    def __init__(self, state: dict):
        self.base = base_root()
        self.journal = state["journal"]
        if self.journal:
            self._tmp = tempfile.TemporaryDirectory()
            self.root = Path(self._tmp.name) / "view"
            shutil.copytree(self.base, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            apply_journal(self.root, self.journal)
        else:
            self.root = self.base

    def changed(self, real: Path) -> str:
        """'+' added, '~' changed, '' unchanged (relative to the skillset without the journal)."""
        if not self.journal:
            return ""
        rel = real.relative_to(self.root)
        orig = self.base / rel
        if not orig.exists():
            return "+"
        if real.is_file() and orig.is_file() and real.read_bytes() != orig.read_bytes():
            return "~"
        return ""

    # ---- virtual paths: members appear as folders, without the subskills/ layer
    def real(self, vpath: str, fuzzy: bool = True) -> Path:
        cur = self.root
        for seg in [s for s in vpath.replace("\\", "/").split("/") if s not in ("", ".")]:
            if seg == "..":
                raise ShellError("internal: unnormalised path")
            member = cur / MEMBERS / seg
            if member.is_dir():
                cur = member
            elif (cur / seg).exists():
                cur = cur / seg
            else:
                pool = list((cur / MEMBERS).glob("*")) + list(cur.glob("*")) if cur.is_dir() and fuzzy else []
                matches = [p for p in pool if p.name.lower() == seg.lower()]
                if not matches and "." not in seg:                       # "changelog" finds CHANGELOG.md, as on Windows
                    matches = [p for p in pool if p.is_file() and p.stem.lower() == seg.lower()]
                if len(matches) == 1:
                    cur = matches[0]
                else:
                    raise ShellError(f"{vpath}: No such file or directory")
        return cur

    def virtual(self, real: Path) -> str:
        parts = [p for p in real.relative_to(self.root).parts if p != MEMBERS]
        return "/" + "/".join(parts)

    def entries(self, real: Path) -> list[tuple[str, Path, bool, bool]]:
        """(name, path, is_dir, is_member) for a folder, members first."""
        out = []
        if (real / MEMBERS).is_dir():
            for p in sorted((real / MEMBERS).iterdir()):
                if p.is_dir() and not p.name.startswith("."):
                    out.append((p.name, p, True, True))
        for p in sorted(real.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            if p.name in (MEMBERS, "__pycache__", ".git") or p.name.startswith(".") and p.name != ".gitignore":
                continue
            out.append((p.name, p, p.is_dir(), False))
        return out


def norm(cwd: str, path: str) -> str:
    """Join and normalise a virtual path (handles ., .., ~, drive letters, backslashes)."""
    path = (path or "").replace("\\", "/")
    path = re.sub(r"^[A-Za-z]:", "", path)
    if path in ("~", "") or path.startswith("~/"):
        path = "/" + path[2:]
    parts = [] if path.startswith("/") else [p for p in cwd.split("/") if p]
    for seg in path.split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            if parts:
                parts.pop()
        else:
            parts.append(seg)
    return "/" + "/".join(parts)


# ================================================================ command dialects

ALIASES = {
    # listing and moving around
    "ls": "ls", "dir": "ls", "ll": "ls", "la": "ls", "gci": "ls", "get-childitem": "ls", "l": "ls",
    "cd": "cd", "chdir": "cd", "set-location": "cd", "sl": "cd", "pushd": "pushd", "popd": "popd",
    "pwd": "pwd", "get-location": "pwd", "gl": "pwd",
    # reading
    "cat": "cat", "type": "cat", "get-content": "cat", "gc": "cat", "more": "cat", "less": "cat", "bat": "cat",
    "display": "cat", "view": "cat",
    "head": "head", "tail": "tail", "select-object": "head", "select": "head", "tree": "tree", "find": "find", "fd": "find", "locate": "find",
    "grep": "grep", "egrep": "grep", "rg": "grep", "ack": "grep", "select-string": "grep", "sls": "grep",
    "findstr": "grep", "wc": "wc", "measure-object": "wc", "stat": "stat", "get-item": "stat", "gi": "stat",
    "file": "file", "du": "du", "open": "open", "start": "open", "invoke-item": "open", "ii": "open",
    "xdg-open": "open", "sort": "sort", "sort-object": "sort", "uniq": "uniq", "get-unique": "uniq",
    # about the shell and the AI
    "help": "help", "?": "help", "man": "man", "get-help": "man", "info": "man", "tldr": "man",
    "which": "which", "where": "which", "get-command": "which", "gcm": "which", "whereis": "which",
    "whoami": "whoami", "uname": "uname", "ver": "uname", "hostname": "uname", "history": "history",
    "get-history": "history", "h": "history", "clear": "clear", "cls": "clear", "clear-host": "clear",
    "echo": "echo", "write-output": "echo", "write-host": "echo", "printf": "echo", "alias": "alias",
    "set-alias": "alias", "unalias": "unalias", "env": "env", "printenv": "env", "exit": "exit",
    "logout": "exit", "quit": "exit",
    # editing: remembered in the journal
    "touch": "touch", "new-item": "newitem", "ni": "newitem", "rm": "rm", "del": "rm", "erase": "rm",
    "remove-item": "rm", "ri": "rm", "rmdir": "rm", "rd": "rm", "unlink": "rm", "mv": "mv", "move": "mv",
    "move-item": "mv", "mi": "mv", "ren": "mv", "rename": "mv", "rename-item": "mv", "rni": "mv", "cp": "cp",
    "copy": "cp", "copy-item": "cp", "cpi": "cp", "mkdir": "mkdir", "md": "mkdir", "set-content": "setcontent",
    "sc": "setcontent", "add-content": "addcontent", "ac": "addcontent", "out-file": "setcontent",
    "sed": "sed", "nano": "editor", "vim": "editor", "vi": "editor", "nvim": "editor", "emacs": "editor",
    "notepad": "editor", "code": "editor", "edit": "editor", "tee": "tee", "git": "git",
}
NOT_HERE = {"curl", "wget", "python", "python3", "node", "npm", "pip", "sudo", "ssh", "scp", "make", "bash", "sh",
            "zsh", "pwsh", "powershell", "cmd", "chmod", "chown", "kill", "ps", "top", "apt", "brew", "docker",
            "kubectl", "invoke-webrequest", "iwr", "invoke-expression", "iex", "start-process", "reg", "net"}
FILTERS = {"grep", "head", "tail", "sort", "uniq", "wc"}
AMBIGUOUS = {"type", "find", "open", "start", "file", "sort", "edit", "more", "less", "copy", "move", "rename",
             "display", "view"}  # also English verbs


def split_line(line: str) -> list[str]:
    """Split on | ; && outside quotes."""
    parts, buf, quote = [], "", None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            buf += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf += ch
        elif ch == "|" and line[i:i + 2] != "||":
            parts.append(("|", buf))
            buf = ""
        elif ch == ";" or line[i:i + 2] == "&&":
            parts.append((";", buf))
            buf = ""
            if line[i:i + 2] == "&&":
                i += 1
        else:
            buf += ch
        i += 1
    parts.append((";", buf))
    return parts


def tokens(text: str) -> list[str]:
    # Windows paths (..\reasoning\x) become forward slashes before bash-style quoting eats the backslashes.
    text = re.sub(r"\\(?=[\w.*?-])", "/", text)
    try:
        return shlex.split(text, posix=True)
    except ValueError:
        return text.split()


def split_redirect(text: str) -> tuple[str, str | None, str | None]:
    """'echo hi >> f' -> ('echo hi', '>>', 'f'), outside quotes."""
    quote = None
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == ">":
            mode = ">>" if text[i:i + 2] == ">>" else ">"
            target = text[i + len(mode):].strip()
            return text[:i].rstrip(), mode, (tokens(target) or [None])[0]
    return text, None, None


def flags_and_args(argv: list[str]) -> tuple[set[str], list[str], dict[str, str]]:
    flags, args, named = set(), [], {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if re.match(r"^-{1,2}[A-Za-z]", a) or re.match(r"^/[A-Za-z?]$", a):
            key = a.lstrip("-/").lower()
            if a.startswith("-") and not a.startswith("--") and 1 < len(key) <= 3 and key.isalpha() and key not in ("gt", "lt", "eq"):
                flags.update(key)                                  # -rl is -r -l (and PowerShell words stay whole)
            if i + 1 < len(argv) and key in ("path", "value", "filter", "name", "destination", "newname", "pattern",
                                             "first", "last", "n", "itemtype", "include", "encoding", "literalpath"):
                named[key] = argv[i + 1]
                i += 2
                continue
            flags.add(key)
        else:
            args.append(a)
        i += 1
    return flags, args, named


# ================================================================ the shell

class Shell:
    def __init__(self, state: dict):
        self.state = state
        self.view = View(state)

    @property
    def cwd(self) -> str:
        return self.state["cwd"]

    def path(self, arg: str) -> tuple[str, Path]:
        v = norm(self.cwd, arg)
        return v, self.view.real(v)

    def rel(self, real: Path) -> str:
        return real.relative_to(self.view.root).as_posix()

    def target_rel(self, arg: str) -> tuple[str, str]:
        """For an edit: (virtual path, real path relative to the skillset), for files that may not exist yet."""
        v = norm(self.cwd, arg)
        parent_v, name = v.rsplit("/", 1)
        parent = self.view.real(parent_v or "/")
        return v, (parent / name).relative_to(self.view.root).as_posix()

    def remember(self, op: dict, what: str) -> str:
        self.state["journal"].append(op)
        self.view = View(self.state)                                 # later commands see the remembered edit
        return f"remembered: {what}\n(nothing was changed; `git status` lists remembered edits, and asking for an updated repository applies them)"

    # ---- run one command line
    def run(self, line: str) -> str:
        line = line.strip()
        if not line:
            return ""
        self.state["history"] = (self.state["history"] + [line])[-200:]
        out_all, piped = [], None
        for sep, part in split_line(line):
            part = part.strip()
            if not part:
                continue
            text = self.one(part, piped)
            if sep == "|":
                piped = text
            else:
                piped = None
                out_all.append(text)
        return "\n".join(t for t in out_all if t).rstrip("\n")

    def one(self, text: str, stdin: str | None) -> str:
        body, redirect, target = split_redirect(text)
        argv = tokens(body)
        if not argv:
            return ""
        if argv[0].lower() in self.state["aliases"]:
            argv = tokens(self.state["aliases"][argv[0].lower()]) + argv[1:]
        name = argv[0].lower()
        self.invoked = name
        cmd = ALIASES.get(name)
        if len(argv) == 1 and name in OPENER_WORDS:                   # bare "start" or "hi" opens the suggestions
            cmd = None
        if cmd is None:
            if name in NOT_HERE:
                raise ShellError(f"{argv[0]}: not available here. This shell only navigates Skillset-OS and never runs "
                                 "programs; say what you want in plain English instead.")
            return resolve_verb_noun(" ".join(argv), self.state, self.view)
        if name in AMBIGUOUS and len(argv) > 1 and not stdin and not argv[1].startswith("-") and self._is_verb_noun(argv):
            return resolve_verb_noun(" ".join(argv), self.state, self.view)   # "find skills", "open a pull request"
        self.state.pop("menu", None)                               # a shell command moves on from any menu
        out = getattr(self, "c_" + cmd)(argv[1:], stdin)
        if redirect:
            if not target:
                raise ShellError("syntax error near unexpected token `newline'")
            v, rel = self.target_rel(target)
            content = out if out.endswith("\n") or not out else out + "\n"
            op = {"op": "append" if redirect == ">>" else "write", "path": rel, "content": content}
            return self.remember(op, f"{'append to' if redirect == '>>' else 'write'} {v}")
        return out

    def _is_verb_noun(self, argv: list[str]) -> bool:
        try:
            self.path(argv[1])
            return False
        except ShellError:
            return True

    # ---- navigation
    def c_ls(self, argv, stdin):
        flags, args, named = flags_and_args(argv)
        recursive = bool({"r", "recurse", "s"} & flags)
        long = bool({"l", "la", "al", "lh"} & flags) or "force" in flags
        target = named.get("path") or (args[0] if args else ".")
        pattern = named.get("filter") or named.get("include")
        if not pattern and any(ch in target for ch in "*?["):       # ls *.md, dir *.*, ls cognition/*
            folder, _, pattern = target.replace("\\", "/").rpartition("/")
            target = folder or "."
        if pattern in ("*.*", "*."):                                 # cmd: *.* means every entry
            pattern = "*"
        _v, real = self.path(target)
        if real.is_file():
            return real.name
        lines = []

        def listing(folder: Path, prefix: str):
            for name, p, is_dir, is_member in self.view.entries(folder):
                if pattern and not fnmatch.fnmatch(name.lower(), pattern.lower()) and not (recursive and is_dir):
                    continue
                mark = self.view.changed(p)
                shown = f"{prefix}{name}{'/' if is_dir else ''}"
                if not pattern or fnmatch.fnmatch(name.lower(), (pattern or "*").lower()):
                    if long:
                        what = "member" if is_member else ("dir" if is_dir else f"{p.stat().st_size:>7}")
                        lines.append(f"{mark or ' '} {what:>7}  {shown}")
                    else:
                        lines.append(f"{mark}{shown}")
                if recursive and is_dir:
                    listing(p, prefix + name + "/")
        listing(real, "")
        if pattern and not lines:
            raise ShellError(f"{pattern}: No such file or directory")
        return "\n".join(lines)

    def c_cd(self, argv, stdin):
        _flags, args, named = flags_and_args(argv)
        target = named.get("path") or (args[0] if args else "/")
        if target == "-":
            target = self.state.get("oldpwd", "/")
        v, real = self.path(target)
        if not real.is_dir():
            raise ShellError(f"cd: {target}: Not a directory")
        self.state["oldpwd"], self.state["cwd"] = self.cwd, v
        return ""

    def c_pushd(self, argv, stdin):
        self.state["stack"].append(self.cwd)
        return self.c_cd(argv, stdin) or " ".join([self.cwd] + self.state["stack"][::-1])

    def c_popd(self, argv, stdin):
        if not self.state["stack"]:
            raise ShellError("popd: directory stack empty")
        self.state["cwd"] = self.state["stack"].pop()
        return self.cwd

    def c_pwd(self, argv, stdin):
        return self.cwd

    # ---- reading
    def _files(self, argv, named_key="path"):
        _flags, args, named = flags_and_args(argv)
        names = ([named[named_key]] if named.get(named_key) else []) + args
        out = []
        for a in names:
            _v, real = self.path(a)
            if real.is_dir():
                doc = next((real / d for d in ("SUBSKILL.md", "SKILLSET.md", "SKILL.md") if (real / d).is_file()), None)
                if not doc:
                    raise ShellError(f"{a}: Is a directory")
                real = doc
            out.append(real)
        return out

    def c_cat(self, argv, stdin):
        flags, args, named = flags_and_args(argv)
        if not args and not named and stdin is not None:
            return stdin
        texts = [p.read_text(encoding="utf-8", errors="replace") for p in self._files(argv)]
        text = "".join(texts)
        if "n" in flags:
            text = "\n".join(f"{i:6}\t{ln}" for i, ln in enumerate(text.splitlines(), 1))
        if named.get("totalcount") or named.get("first"):
            text = "\n".join(text.splitlines()[:int(named.get("first") or named.get("totalcount"))])
        return text.rstrip("\n")

    def _count(self, argv, default=10):
        flags, args, named = flags_and_args(argv)
        n = default
        for a in list(args):
            if re.fullmatch(r"-?\d+", a):
                n = abs(int(a))
                args.remove(a)
        for f in flags:
            if re.fullmatch(r"n?\d+", f):
                n = int(f.lstrip("n"))
        n = int(named.get("n") or named.get("first") or named.get("last") or n)
        return n, args

    def c_head(self, argv, stdin):
        if any(a.lower() == "-last" for a in argv):
            return self.c_tail(argv, stdin)
        n, args = self._count(argv)
        text = stdin if not args and stdin is not None else "\n".join(p.read_text(encoding="utf-8") for p in self._files(args))
        return "\n".join(text.splitlines()[:n])

    def c_tail(self, argv, stdin):
        n, args = self._count(argv)
        text = stdin if not args and stdin is not None else "\n".join(p.read_text(encoding="utf-8") for p in self._files(args))
        return "\n".join(text.splitlines()[-n:])

    def c_tree(self, argv, stdin):
        argv, depth = list(argv), 0
        for i, a in enumerate(argv):
            if a in ("-L", "-l", "--level", "-Depth", "-depth") and i + 1 < len(argv) and argv[i + 1].isdigit():
                depth = int(argv[i + 1])
                del argv[i:i + 2]
                break
        flags, args, _named = flags_and_args(argv)
        members_only = "d" in flags
        v, real = self.path(args[0] if args else ".")
        lines = [v]

        def walk(folder: Path, pad: str, level: int):
            entries = [e for e in self.view.entries(folder) if e[2] or not members_only]
            for i, (name, p, is_dir, is_member) in enumerate(entries):
                last = i == len(entries) - 1
                lines.append(f"{pad}{'└── ' if last else '├── '}{self.view.changed(p)}{name}{'/' if is_dir else ''}")
                if is_dir and (not depth or level < depth):
                    walk(p, pad + ("    " if last else "│   "), level + 1)
        walk(real, "", 1)
        return "\n".join(lines)

    def c_find(self, argv, stdin):
        _flags, args, named = flags_and_args(argv)
        start = args[0] if args and not args[0].startswith("*") else "."
        pattern = named.get("name") or named.get("filter") or next((a for a in args if "*" in a or "?" in a), "*")
        want_dir = named.get("type") == "d"
        _v, real = self.path(start)
        out = []
        for p in sorted(real.rglob("*")):
            if "__pycache__" in p.parts or ".git" in p.parts or p.name == MEMBERS:
                continue
            if fnmatch.fnmatch(p.name.lower(), pattern.lower()) and (not want_dir or p.is_dir()):
                out.append(self.view.changed(p) + self.view.virtual(p))
        return "\n".join(out)

    def c_grep(self, argv, stdin):
        flags, args, named = flags_and_args(argv)
        if named.get("pattern"):
            args.insert(0, named["pattern"])
        if not args:
            raise ShellError("usage: grep [-i] [-r] [-n] [-l] PATTERN [PATH...]")
        pattern, paths = args[0], args[1:] or ([named["path"]] if named.get("path") else [])
        insensitive = bool({"i", "ignore-case"} & flags) or (getattr(self, "invoked", "") in ("select-string", "sls", "findstr")
                                                              and "casesensitive" not in flags)
        if "simplematch" in flags or "f" in flags:
            pattern = re.escape(pattern)
        rx = re.compile(pattern, re.IGNORECASE if insensitive else 0)
        invert, count_only, names_only = "v" in flags, "c" in flags, "l" in flags
        if stdin is not None and not paths:
            lines = [ln for ln in stdin.splitlines() if bool(rx.search(ln)) != invert]
            return str(len(lines)) if count_only else "\n".join(lines)
        files = []
        for a in paths or ["."]:
            _v, real = self.path(a)
            if real.is_dir():
                files += [p for p in sorted(real.rglob("*")) if p.is_file() and "__pycache__" not in p.parts]
            else:
                files.append(real)
        out = []
        for f in files:
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            hits = [(i, ln) for i, ln in enumerate(text.splitlines(), 1) if bool(rx.search(ln)) != invert]
            if not hits:
                continue
            vf = self.view.virtual(f)
            if names_only:
                out.append(vf)
            elif count_only:
                out.append(f"{vf}:{len(hits)}")
            else:
                out += [f"{vf}:{i}:{ln}" if "n" in flags or len(files) > 1 else ln for i, ln in hits]
        return "\n".join(out)

    def c_wc(self, argv, stdin):
        flags, args, _named = flags_and_args(argv)
        texts = [(None, stdin)] if not args and stdin is not None else [(a, p.read_text(encoding="utf-8")) for a, p in
                                                                          zip(args, self._files(args))]
        out = []
        for name, t in texts:
            counts = (t.count("\n") + (0 if t.endswith("\n") or not t else 1), len(t.split()), len(t.encode()))
            if "l" in flags or "line" in flags:
                out.append(f"{counts[0]}" + (f" {name}" if name else ""))
            else:
                out.append(f"{counts[0]:>7} {counts[1]:>7} {counts[2]:>7}" + (f" {name}" if name else ""))
        return "\n".join(out)

    def c_sort(self, argv, stdin):
        flags, _a, _n = flags_and_args(argv)
        lines = sorted((stdin or "").splitlines(), reverse="r" in flags or "descending" in flags)
        return "\n".join(lines)

    def c_uniq(self, argv, stdin):
        out, prev = [], object()
        for ln in (stdin or "").splitlines():
            if ln != prev:
                out.append(ln)
            prev = ln
        return "\n".join(out)

    def c_stat(self, argv, stdin):
        out = []
        for a in flags_and_args(argv)[1] or ["."]:
            v, real = self.path(a)
            kind = "member folder" if (real / "SUBSKILL.md").is_file() or (real / "SKILLSET.md").is_file() else \
                ("directory" if real.is_dir() else "file")
            size = sum(p.stat().st_size for p in real.rglob("*") if p.is_file()) if real.is_dir() else real.stat().st_size
            out.append(f"  File: {v}\n  Type: {kind}\n  Size: {size} bytes" + (f"\n Edits: {self.view.changed(real)}" if self.view.changed(real) else ""))
        return "\n".join(out)

    def c_file(self, argv, stdin):
        out = []
        for a in flags_and_args(argv)[1]:
            v, real = self.path(a)
            if real.is_dir():
                out.append(f"{v}: directory")
            else:
                out.append(f"{v}: {skillset().summary_of(real) or 'text'}")
        return "\n".join(out)

    def c_du(self, argv, stdin):
        v, real = self.path((flags_and_args(argv)[1] or ["."])[0])
        files = [p for p in real.rglob("*") if p.is_file()] if real.is_dir() else [real]
        return f"{sum(p.stat().st_size for p in files) // 1024 + 1}K\t{v} ({len(files)} files)"

    def c_open(self, argv, stdin):
        args = flags_and_args(argv)[1]
        v, real = self.path(args[0] if args else ".")
        doc = next((real / d for d in ("SUBSKILL.md", "SKILLSET.md", "SKILL.md") if (real / d).is_file()), None)
        if not doc:
            raise ShellError(f"open: {v} is not a skill (no SUBSKILL.md or SKILLSET.md)")
        return f"# {v}: read and follow this file; its paths are relative to its own folder\n" + \
            doc.read_text(encoding="utf-8").rstrip("\n")

    # ---- about the shell and the AI
    def c_help(self, argv, stdin):
        if argv:
            return self.c_man(argv, stdin)
        return HELP.strip()

    def c_man(self, argv, stdin):
        if not argv:
            return "What manual page do you want?"
        topic = argv[-1].lower()
        cmd = ALIASES.get(topic)
        if cmd:
            return f"{topic}: {MANUAL.get(cmd, 'see `help`')}" + (f" (same as `{cmd}`)" if cmd != topic else "")
        return resolve_verb_noun(" ".join(argv), self.state, self.view)

    def c_which(self, argv, stdin):
        out = []
        for a in flags_and_args(argv)[1]:
            cmd = ALIASES.get(a.lower())
            if cmd:
                out.append(f"{a}: shell built-in ({cmd})")
            else:
                out.append(resolve_verb_noun(a, self.state, self.view, brief=True))
        return "\n".join(out)

    def c_whoami(self, argv, stdin):
        name, version = skillset().top_info(self.view.root)
        items = memory().load(self.view.root)
        approved = [i for i in items if i["status"] == "approved"]
        return (f"{name} {version}: the AI's command line over its own skills\n"
                f"self-memory: {len(approved)} approved items (`stats` for more); skills: `inventory`")

    def c_uname(self, argv, stdin):
        name, version = skillset().top_info(self.view.root)
        return f"Skillset-OS {version} ({name}) virtual shell: bash, PowerShell and cmd dialects; nothing runs on the host"

    def c_history(self, argv, stdin):
        return "\n".join(f"{i:5}  {c}" for i, c in enumerate(self.state["history"], 1))

    def c_clear(self, argv, stdin):
        return "(screen cleared)"

    def c_echo(self, argv, stdin):
        return " ".join(a for a in argv if a not in ("-n", "-e"))

    def c_alias(self, argv, stdin):
        text = " ".join(argv)
        if not text:
            return "\n".join(f"alias {k}='{v}'" for k, v in sorted(self.state["aliases"].items())) or "(no aliases)"
        m = re.match(r"^(?:-name\s+)?([\w?.-]+)(?:\s*=\s*|\s+-value\s+|\s+)(.+)$", text, re.IGNORECASE)
        if not m:
            raise ShellError("usage: alias name='command'")
        self.state["aliases"][m.group(1).lower()] = m.group(2).strip("'\"")
        return ""

    def c_unalias(self, argv, stdin):
        for a in argv:
            self.state["aliases"].pop(a.lower(), None)
        return ""

    def c_env(self, argv, stdin):
        name, version = skillset().top_info(self.view.root)
        return "\n".join([f"SKILLSET={name}", f"VERSION={version}", f"PWD={self.cwd}", f"MODE={self.state['mode']}",
                          f"JOURNAL={len(self.state['journal'])}", "SHELL=skillset-os"])

    def c_exit(self, argv, stdin):
        self.state["mode"] = "english"
        return "left the command line; messages are read as plain English (`mode auto` or any command brings it back)"

    # ---- editing: remembered, never applied here
    def c_touch(self, argv, stdin):
        out = []
        for a in flags_and_args(argv)[1]:
            v, rel = self.target_rel(a)
            out.append(self.remember({"op": "touch", "path": rel}, f"create {v}"))
        return "\n".join(out)

    def c_newitem(self, argv, stdin):
        _flags, args, named = flags_and_args(argv)
        target = named.get("path") or named.get("name") or (args[0] if args else None)
        if not target:
            raise ShellError("New-Item: give -Path")
        v, rel = self.target_rel(target)
        if (named.get("itemtype") or "").lower() in ("directory", "dir", "folder"):
            return self.remember({"op": "mkdir", "path": rel}, f"create folder {v}")
        return self.remember({"op": "write", "path": rel, "content": named.get("value", "")}, f"create {v}")

    def c_rm(self, argv, stdin):
        flags, args, named = flags_and_args(argv)
        out = []
        for a in ([named["path"]] if named.get("path") else []) + args:
            v, real = self.path(a)
            if real.is_dir() and not ({"r", "rf", "fr", "recurse", "s"} & flags):
                raise ShellError(f"rm: cannot remove '{a}': Is a directory (use -r)")
            out.append(self.remember({"op": "delete", "path": self.rel(real)}, f"delete {v}"))
        return "\n".join(out)

    def c_mv(self, argv, stdin, op="move"):
        _flags, args, named = flags_and_args(argv)
        src = named.get("path") or (args[0] if args else None)
        dst = named.get("destination") or named.get("newname") or (args[1] if len(args) > 1 else None)
        if not src or not dst:
            raise ShellError(f"{op}: give a source and a destination")
        v, real = self.path(src)
        dv = norm(self.cwd, dst)
        try:
            dreal = self.view.real(dv, fuzzy=False)
            if dreal.is_dir():
                dv, dreal = dv.rstrip("/") + "/" + real.name, dreal / real.name
            drel = dreal.relative_to(self.view.root).as_posix()
        except ShellError:
            if "/" not in dst.replace("\\", "/"):                 # Rename-Item style: a new name beside it
                dv, drel = norm(self.cwd, "/".join(v.split("/")[:-1] + [dst])), (real.parent / dst).relative_to(self.view.root).as_posix()
            else:
                dv, drel = self.target_rel(dst)
        return self.remember({"op": op, "path": self.rel(real), "to": drel}, f"{op} {v} → {dv}")

    def c_cp(self, argv, stdin):
        return self.c_mv(argv, stdin, op="copy")

    def c_mkdir(self, argv, stdin):
        return "\n".join(self.remember({"op": "mkdir", "path": self.target_rel(a)[1]}, f"create folder {norm(self.cwd, a)}")
                         for a in flags_and_args(argv)[1])

    def c_setcontent(self, argv, stdin, op="write"):
        _flags, args, named = flags_and_args(argv)
        target = named.get("path") or named.get("literalpath") or named.get("filepath") or (args[0] if args else None)
        value = named.get("value") if "value" in named else (" ".join(args[1:]) if len(args) > 1 else stdin)
        if not target or value is None:
            raise ShellError("give a path and the content (-Value, or pipe it in)")
        v, rel = self.target_rel(target)
        content = value if value.endswith("\n") else value + "\n"
        return self.remember({"op": op, "path": rel, "content": content}, f"{'write' if op == 'write' else 'append to'} {v}")

    def c_addcontent(self, argv, stdin):
        return self.c_setcontent(argv, stdin, op="append")

    def c_tee(self, argv, stdin):
        flags, args, _n = flags_and_args(argv)
        if not args or stdin is None:
            raise ShellError("usage: ... | tee [-a] FILE")
        v, rel = self.target_rel(args[0])
        note = self.remember({"op": "append" if "a" in flags else "write", "path": rel,
                              "content": stdin if stdin.endswith("\n") else stdin + "\n"}, f"write {v}")
        return stdin + "\n" + note

    def c_sed(self, argv, stdin):
        flags, args, _n = flags_and_args(argv)
        if not args:
            raise ShellError("usage: sed [-i] 's/old/new/[g]' FILE")
        m = re.fullmatch(r"s(.)(.*?)(?<!\\)\1(.*?)(?<!\\)\1(g?)", args[0])
        if not m:
            raise ShellError("sed: only s/old/new/[g] substitutions are understood")
        pattern, repl, all_ = m.group(2), re.sub(r"\\(\d)", r"\\\1", m.group(3).replace("&", r"\g<0>")), bool(m.group(4))
        if "i" not in flags:
            text = stdin if stdin is not None else "".join(p.read_text(encoding="utf-8") for p in self._files(args[1:]))
            return re.sub(pattern, repl, text, count=0 if all_ else 1).rstrip("\n")
        out = []
        for a in args[1:]:
            v, real = self.path(a)
            out.append(self.remember({"op": "replace", "path": self.rel(real), "pattern": pattern,
                                      "replacement": repl, "all": all_}, f"edit {v} (s/{pattern}/{m.group(3)}/)"))
        return "\n".join(out)

    def c_editor(self, argv, stdin):
        target = (flags_and_args(argv)[1] or [None])[0]
        if not target:
            raise ShellError("give a file to edit")
        v, _rel = self.target_rel(target)
        return (f"editing {v}: this shell has no screen editor. Describe the change in plain English (or paste the "
                f"new content) and it will be remembered as an edit of {v}.")

    def c_git(self, argv, stdin):
        sub = (argv or ["status"])[0].lower()
        journal = self.state["journal"]
        if sub in ("status", "st"):
            if not journal:
                return "nothing remembered: the skillset is unchanged"
            return "remembered edits (not applied):\n" + "\n".join(f"  {i}. {describe(op)}" for i, op in enumerate(journal, 1))
        if sub == "diff":
            return journal_diff(self.view.base, journal) or "(no differences)"
        if sub in ("restore", "checkout", "reset"):
            if len(argv) > 1 and argv[1] not in ("--hard", "--", "."):
                keep = [op for op in journal if not op.get("path", "").endswith(argv[-1].lstrip("./"))]
                dropped = len(journal) - len(keep)
                self.state["journal"] = keep
                return f"forgot {dropped} remembered edit(s) to {argv[-1]}"
            self.state["journal"] = []
            return "forgot every remembered edit"
        if sub in ("add", "stage"):
            return "(every remembered edit is already staged)"
        if sub in ("commit", "push"):
            return (f"{len(journal)} remembered edit(s). They are applied only when an updated repository is requested: "
                    "say \"build the updated repository\" (or `save changes`).")
        if sub == "log":
            return "no history here: Skillset-OS keeps lessons in self-memory, not a change log (`recall`)"
        return f"git {sub}: not needed here (status, diff, restore and commit are understood)"


def describe(op: dict) -> str:
    if op["op"] in ("move", "copy"):
        return f"{op['op']} {op['path']} → {op['to']}"
    if op["op"] == "replace":
        return f"edit {op['path']} (s/{op['pattern']}/{op['replacement']}/{'g' if op.get('all') else ''})"
    if op["op"] == "memory":
        return f"remember ({op['type']}): {op['summary']}"
    return f"{op['op']} {op.get('path', '')}"


def journal_diff(base: Path, journal: list[dict]) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        after = Path(tmp) / "after"
        shutil.copytree(base, after, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        apply_journal(after, journal)
        out = []
        skip = {".git", "__pycache__"}
        paths = sorted({p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file() and not skip & set(p.parts)}
                       | {p.relative_to(after).as_posix() for p in after.rglob("*") if p.is_file() and not skip & set(p.parts)})
        for rel in paths:
            a, b = base / rel, after / rel
            ta = a.read_text(encoding="utf-8", errors="replace") if a.is_file() else ""
            tb = b.read_text(encoding="utf-8", errors="replace") if b.is_file() else ""
            if a.is_file() != b.is_file() and ta == tb:
                out.append(f"{'new' if b.is_file() else 'deleted'} file: {rel} (empty)")
            elif ta != tb:
                out += list(difflib.unified_diff(ta.splitlines(), tb.splitlines(), f"a/{rel}" if a.is_file() else "/dev/null",
                                                 f"b/{rel}" if b.is_file() else "/dev/null", lineterm=""))
        mem = [op for op in journal if op["op"] == "memory"]
        out += [f"+ self-memory candidate ({op['type']}): {op['summary']}" for op in mem]
        return "\n".join(out)


HELP = """
Skillset-OS command line. Your skills are the file system: members are folders, their SUBSKILL.md inside.
Bash, PowerShell and cmd spellings all work (ls = dir = Get-ChildItem, cat = type = Get-Content, ...).

  look / ls / dir            what is here           cd <member> / go <member>   move
  map / tree [-L 2]          the whole layout       pwd                         where am I
  cat / type <file>          read a file            open <member>               read its instructions
  grep / findstr / sls       search text            find <dir> -name '*.md'     find files
  inventory                  every skill            examine <member>            what one skill does
  stats / quests             self-memory, open maintenance        recall <topic>   search self-memory
  commands [--top 20]        the most useful commands, generated from what I know
  favourites add|list|save|load   your own list: this session, or a file you keep
  git status / git diff      remembered edits       save changes                apply them to a new repository

Edits (touch, echo > file, sed -i, rm, mv, cp, mkdir, Set-Content, New-Item ...) are remembered, never applied,
until you ask for an updated repository. Anything else in verb-noun form ("review code", "plan feature",
"create spreadsheet") is done with the skill that fits; plain English works as usual.
"""
MANUAL = {
    "ls": "list a folder: members first, then files. -l long, -R recursive, -Filter *.md",
    "cd": "change folder. Members are folders by name: cd cognition/reasoning; cd .. ; cd - ; cd ~",
    "cat": "print a file; on a member folder, prints its SUBSKILL.md or SKILLSET.md",
    "grep": "search: grep [-i] [-n] [-l] [-c] [-v] PATTERN [PATH]; also | grep PATTERN",
    "tree": "draw the layout: tree [-L N] [-d] [PATH]",
    "find": "find files: find [PATH] -name 'pattern' [-type d]",
    "open": "print a member's instructions to read and follow",
    "rm": "remember a deletion (applied only in an updated repository)",
    "sed": "sed 's/old/new/g' FILE prints; sed -i remembers the edit",
    "git": "status and diff show remembered edits; restore forgets them; commit explains how to apply them",
}


# ================================================================ verb-noun commands

VERB_SYNONYMS = {
    "check": "review", "audit": "review", "assess": "review", "inspect": "examine", "x": "examine", "describe": "examine",
    "l": "look", "i": "inventory", "inv": "inventory", "walk": "go", "enter": "go", "visit": "go", "make": "create",
    "build": "create", "generate": "create", "draft": "write", "compose": "write", "author": "write", "fix": "debug",
    "troubleshoot": "debug", "summarize": "summarise", "analyze": "analyse", "organize": "organise", "optimize": "improve",
    "study": "learn", "research": "research", "memorise": "remember", "memorize": "remember", "note": "remember",
    "lookup": "search", "google": "search", "show": "examine", "list": "list", "translate": "translate",
}
NOUN_STOP = {"a", "an", "the", "my", "your", "some", "of", "for", "to", "on", "in", "with", "and", "or", "this", "that",
             "me", "it", "new", "own", "them"}
META = [  # (command, how, description)
    ("look", "ls", "Describe where you are: the member here and what is inside."),
    ("map", "tree -L 2", "The layout of the whole skillset."),
    ("inventory", "inventory", "Every skill, with what it is for."),
    ("examine skill", "examine <member>", "What one skill does, and when it is used."),
    ("go skill", "cd <member>", "Move into a skill or skillset."),
    ("stats", "stats", "Self-memory in numbers, and the latest exam result."),
    ("quests", "quests", "Open maintenance items from self-memory."),
    ("recall lessons", "recall <topic>", "Search self-memory for what was learned."),
    ("remember lesson", "remember <type> <summary>", "Propose a self-memory candidate (applied with the other edits)."),
    ("list commands", "commands --top 20", "The most useful commands, generated from what the skillset knows."),
    ("apps", "apps", "The mimic apps, and the command words that open each one."),
    ("review commands", "skillset.py review command-line",
     "Audit the command-line skill and the command list it generates."),
    ("review skillset", "skillset.py review . and skillset.py check",
     "Audit the whole Skillset-OS for problems, then report issues, version and pending edits."),
    ("save changes", "save changes", "Apply the remembered edits to an updated repository and package it."),
    ("show changes", "git diff", "What the remembered edits would change."),
    ("save favourites", "favourites save", "Write your own command list to a file you keep."),
    ("load favourites", "favourites load <file>", "Bring back a command list you kept."),
    ("run exam", "open cognition/metacognition/universal-skill-curriculum-exam",
     "The timed self-examination, to monitor performance."),
    ("focus skill", "focus <skill or command>", "Set focus on a skill or command and show its command tree."),
    ("commands tree", "commands tree [skill|all]", "A skill's own commands as an emoji tree, with what is still wanted."),
    ("db query", "db <sql>", "Query the command database with SQL; your own tables are writable."),
    ("enable command", "enable|disable <command>", "Turn a command on or off for routing, in your preferences."),
    ("prefer command", "prefer|unprefer <command>", "Star a command so it leads your command list."),
    ("request command", "request command <phrase> [for <skill>] [: note]", "Ask for a command a skill should have."),
    ("advise commands", "advise commands [topic]", "Advice on new useful commands, from misses, requests and gaps."),
]
MODEL_TOOLS = [  # (command, how, description) — available when the chat has the tool
    ("search web", "web search", "Find current information on the web."),
    ("fetch page", "web fetch", "Read a web page in full."),
    ("summarise text", "model", "Summarise a text, file or conversation."),
    ("translate text", "model", "Translate between languages."),
    ("explain topic", "model", "Explain a concept at the right level."),
    ("write code", "model + code execution", "Write and run code."),
    ("analyse data", "code execution", "Load, analyse and chart data."),
    ("make chart", "chart or visualiser", "Plot numbers as a chart."),
    ("draw diagram", "visualiser", "Draw a diagram or flow."),
    ("draft email", "model", "Draft an email or message."),
    ("proofread text", "model", "Correct spelling, grammar and clarity."),
    ("brainstorm ideas", "model", "Generate and develop options."),
    ("create quiz", "quiz tool", "Make practice questions or flashcards."),
    ("find places", "places search", "Find places, shops or restaurants."),
    ("check weather", "weather tool", "Get the forecast for a place."),
    ("show images", "image search", "Find images that illustrate a topic."),
]
BUILTIN_VERBS = {"docx": "create document", "pdf": "create pdf", "pptx": "create presentation",
                 "xlsx": "create spreadsheet", "frontend-design": "design interface", "file-reading": "read file",
                 "pdf-reading": "read pdf", "product-self-knowledge": "explain claude-products",
                 "skill-creator": "create skill", "deep-research": "research topic", "doc-coauthoring": "write document",
                 "canvas-design": "design poster", "algorithmic-art": "create art", "mcp-builder": "build mcp-server",
                 "web-artifacts-builder": "build web-app", "theme-factory": "create theme", "internal-comms": "write announcement",
                 "financial-calculator": "calculate finances", "event-planning": "plan event", "meal-delivery": "order meal",
                 "grocery-shopping": "buy groceries", "brand-guidelines": "apply brand", "slack-gif-creator": "create gif"}
KNOWN_VERBS = {"review", "debug", "write", "plan", "design", "create", "scaffold", "implement", "refactor", "document",
               "secure", "tune", "orient", "adopt", "develop", "find", "import", "edit", "retire", "organise", "sync",
               "build", "test", "run", "reflect", "decide", "learn", "teach", "set", "manage", "handle", "support",
               "prepare", "negotiate", "resolve", "give", "keep", "catch", "think", "notice", "focus", "track",
               "remember", "reason", "simulate", "research", "detect", "spot", "protect", "escalate", "communicate",
               "calm", "mediate", "offload", "collaborate", "improve", "train", "grow", "use"}


def _words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in NOUN_STOP]


def _stem(w: str) -> str:
    for suf in ("ing", "ies", "es", "s"):
        if len(w) > 4 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w


# ---- apps: members whose description says "Use when a message starts with `word`"
APP_NEEDS_TARGET = {"show", "diff", "read"}    # also shell or English verbs: an app only with a URL or a number


def app_words(description: str) -> list[str]:
    """The command words that open an app, read from its own description."""
    m = re.search(r"starts with (.*?)(?:, or when|\. |$)", description or "")
    if not m:
        return []
    words = re.findall(r"`([A-Za-z][\w-]*)", m.group(1))
    if not words and "those commands" in m.group(1):                   # "starts with one of those commands"
        words = re.findall(r"`([A-Za-z][\w-]*)", description.split("Use when")[0])
    return list(dict.fromkeys(w.lower() for w in words))


APP_SECTION_RE = re.compile(
    r"^### ([a-z][\w-]*)\s*\n+\*\*Command words:\*\* (.+?)\s*\n+\*\*Does:\*\* (.+?)\s*$", re.MULTILINE)


def app_sections(text: str) -> list[tuple[str, list[str], str]]:
    """(app, command words, what it does) for each app section of a multi-app sub-skill such as `apps`."""
    return [(name, list(dict.fromkeys(w.lower() for w in re.findall(r"`([A-Za-z][\w-]*)", words))), does)
            for name, words, does in APP_SECTION_RE.findall(text or "")]


def find_app(root: Path, tokens: list[str]) -> dict | None:
    """The app a command line opens, or None. Shell commands and non-URL uses of shared verbs are left alone."""
    if not tokens:
        return None
    word = tokens[0].lower()
    if word in ALIASES:
        return None
    if word in APP_NEEDS_TARGET:
        arg = tokens[1] if len(tokens) > 1 else ""
        if not (arg.isdigit() or "://" in arg or re.match(r"^[\w-]+(\.[\w-]+)+(/\S*)?$", arg)):
            return None
    for c in catalogue(root):
        if c["kind"] == "app" and word in c["words"]:
            return c
    return None


def apps_text(root: Path) -> str:
    apps = [c for c in catalogue(root) if c["kind"] == "app"]
    if not apps:
        return "No apps are installed."
    width = max(len(app_name(c["target"])) for c in apps)
    return "Apps (type a command word to use one):\n" + "\n".join(
        f"  {app_name(c['target']):<{width}}  {', '.join(c['words'])}" for c in apps)


def app_name(target: str) -> str:
    """`apps#weather` -> weather; `team/minutes` -> minutes."""
    return target.split("#")[-1].split("/")[-1]


def catalogue(root: Path) -> list[dict]:
    """Every command this AI can take, generated from its skills, built-in skills, self-memory and tools."""
    ss = skillset()
    out = [{"command": c, "how": h, "description": d, "kind": "shell", "target": "", "order": n}
           for n, (c, h, d) in enumerate(META)]
    for depth, m in ss.walk(root):
        if m.error:
            continue
        parts = m.name.split("-")
        if m.kind == "skillset":
            verb, noun = "explore", m.name
        elif len(parts) > 1 and parts[0] in KNOWN_VERBS:
            verb, noun = parts[0], "-".join(parts[1:])
        elif len(parts) > 1 and parts[-1] in KNOWN_VERBS:              # code-review -> review code
            verb, noun = parts[-1], "-".join(parts[:-1])
        else:
            trig = _words(m.trigger)
            first = trig[0] if trig else "use"
            verb, noun = (first if first in KNOWN_VERBS else "use"), m.name
            if len(parts) > 1 and _stem(parts[-1])[:5] == verb[:5]:       # habit-building -> build habit
                noun = "-".join(parts[:-1])
            elif _stem(noun)[:5] == verb[:5]:                          # negotiation -> negotiate <what the trigger names>
                objects = [w for w in trig[1:] if w not in KNOWN_VERBS and w != "or"][:1]
                noun = "-".join(objects) or noun
        sections, own = [], ""
        if m.kind != "skillset" and m.folder is not None:
            try:
                text = (m.folder / m.doc).read_text(encoding="utf-8")
                sections = app_sections(text)
                own = str(ss.read(m.folder / m.doc)[0].get("command") or "").strip()
            except OSError:
                sections = []
        if own:                                                       # a hand-picked command beats the generated one
            verb, _, noun = own.partition(" ")
        if sections:                                                  # one sub-skill holding several apps
            for name, words, does in sections:
                out.append({"command": words[0] if words else name, "how": f"open {m.path}, section {name}",
                            "description": ss.shorten(does, 140), "kind": "app", "target": f"{m.path}#{name}",
                            "depth": depth, "trigger": m.trigger, "words": words})
            continue
        words = app_words(m.description) if m.kind != "skillset" else []
        out.append({"command": " ".join(words[:1]) or f"{verb} {noun}", "how": f"open {m.path}",
                    "description": ss.shorten(m.description, 140),
                    "kind": "app" if words else ("skillset" if m.kind == "skillset" else "skill"), "target": m.path,
                    "depth": depth, "trigger": m.trigger, "words": words})
    seen = set()
    for base in INSTALLED_SKILLS:
        if not base.is_dir():
            continue
        for doc in sorted(base.glob("*/SKILL.md")):
            name = doc.parent.name
            if name in seen or (doc.parent / "subskills").is_dir() or name.startswith(("github-skillsets", "skillset-os")):
                continue
            seen.add(name)
            try:
                data, _ = ss.read(doc)
                desc = ss.shorten(" ".join(str(data.get("description") or "").split()), 140)
            except Exception:  # noqa: BLE001, S112 - an unreadable outside skill is simply left out
                continue
            cmd = BUILTIN_VERBS.get(name) or (name.replace("-", " ", 1) if name.split("-")[0] in KNOWN_VERBS | {"file", "hire", "cancel", "return", "call", "import", "setup", "paint"} else f"use {name}")
            out.append({"command": cmd, "how": f"read {doc}", "description": desc, "kind": "built-in skill", "target": str(doc)})
    out += [{"command": c, "how": h, "description": d, "kind": "model/tool", "target": ""} for c, h, d in MODEL_TOOLS]
    return out


def rank(root: Path, cmds: list[dict]) -> list[dict]:
    """Order commands by usefulness, from evidence the skillset has about itself."""
    routes = {}
    fixture = root / "tests" / "routing.json"
    if fixture.is_file():
        try:
            for case in json.loads(fixture.read_text(encoding="utf-8")).get("prompts", []):
                for p in [case.get("expect")] + list(case.get("also") or []):
                    if p:
                        routes[p] = routes.get(p, 0) + 1
        except ValueError:
            pass
    try:
        items = [i for i in memory().load(root) if i["status"] == "approved"]
    except Exception:  # noqa: BLE001 - ranking still works without self-memory
        items = []
    for c in cmds:
        score = {"shell": 100, "app": 60, "model/tool": 55, "skill": 50, "skillset": 30, "built-in skill": 45}[c["kind"]]
        score -= c.get("order", 0) * 0.5                            # the shell's own verbs keep their listed order
        if c["target"] and c["kind"] == "skill":
            score += min(40, 10 * routes.get(c["target"], 0))       # asked for in realistic prompts
            score += min(20, 5 * sum(1 for i in items if c["target"] in " ".join(i.get("evidence") or []) + i["summary"]))
        c["score"] = score
    return sorted(cmds, key=lambda c: (-c["score"], c["command"]))


SHELL_ONLY_WORDS = {"ls", "ll", "la", "cd", "chdir", "pwd", "dir", "grep", "egrep", "findstr", "gci", "get-childitem",
                    "get-content", "set-location", "mkdir", "rmdir", "rm", "touch", "wc", "du", "printenv"}
SHELL_SYNTAX = re.compile(r"(?:&&|\|\||[|<>*]|(?:^|\s)--?[A-Za-z]|[/\\]|\b\w+\.\w{1,5}\b)")


def looks_like_shell(text: str) -> bool:
    """True when a message typed to the rapid route is really a shell command line (`ls subskills`,
    `cd cognition && cat SKILLSET.md`, `Get-ChildItem -Recurse -Filter *.md`), so it goes to the shell rather
    than being read as a verb-noun phrase. English words that are also shell aliases (find, open, help, type,
    cat...) count only with shell syntax after them."""
    first = (tokens(text) or [""])[0].lower()
    if first not in ALIASES:
        return False
    if first in SHELL_ONLY_WORDS:
        return True
    rest = text.strip()[len(first):]
    return "-" in first or bool(SHELL_SYNTAX.search(rest))


def resolve_verb_noun(text: str, state: dict, view: View | None = None, brief: bool = False,
                      menu: bool = True) -> str:
    view = view or View(state)
    words = _words(text)
    if not words:
        return ""
    if looks_like_shell(text):                                    # shell syntax: run it, do not guess a skill
        sh = Shell(state)
        sh.view = view
        first = (tokens(text) or [""])[0]
        return f"> {text}\n→ shell command `{first}`  [skill: command-line]\n" + sh.run(text)
    opener = opener_menu(words, state, view)
    if opener:
        return opener
    fixed = autocorrect_menu(text, words, state, view) if menu else None
    if fixed:
        return fixed
    menu_before = dict(state.get("menu") or {})
    picked = pick_from_menu(text, state)                          # "2", "last": answer to the last numbered choice
    if picked is not None and menu_before.get("learn") and not picked.startswith(("pick:", "inferred: ", "option: ")):
        con = db(view)                                            # the person chose: route that phrase there next time
        row = con.execute("SELECT member FROM routes WHERE command=? ORDER BY source DESC",
                          (cmdb().normal(picked),)).fetchone()
        if cmdb().learn(con, menu_before["for"], picked, row["member"] if row else None):
            state["learned"] = f"`{menu_before['for']}` now routes straight to `{picked}` (picked twice)"
    if picked is not None:
        if picked.startswith("inferred: "):
            choice = picked.split(": ", 1)[1]
            menu_kept = state.get("menu")
            routed = resolve_verb_noun(choice, state, view, brief, menu=False)
            state["menu"] = menu_kept
            return (f"inferred: {choice} (the likeliest reading). Tell the person which was chosen and why in "
                    f"one line; any number from the menu still overrides it.\n" + routed)
        if picked.startswith("pick:"):
            return picked
        if picked.startswith("option: "):
            return picked.split(": ", 1)[1]
        if (tokens(picked) or [""])[0].lower() in ALIASES:                    # a shell command such as `ls`
            sh = Shell(state)
            sh.view = view
            return f"> {picked}\n" + sh.one(picked, None)
        return resolve_verb_noun(picked, state, view, brief, menu=False)
    asked = options_request(text, words, state, view)
    if asked is not None:
        return asked
    state.pop("menu", None)                                        # new input: an older menu no longer applies
    app = find_app(view.root, text.split())
    if app:
        if brief:
            return f"{text}: app → {app['target']} ({app['how']})"
        return "\n".join([f"> {text}", f"→ {app_name(app['target'])}  [app: {app['target']}]",
                          f"  {app['description']}", f"  how: {app['how']}, then carry out the request with it"])
    verb = VERB_SYNONYMS.get(words[0], words[0])
    rest = words[1:]
    if words[0] == "apps" and not rest:
        return apps_text(view.root)
    if words[0] == "show" and rest[:1] in (["changes"], ["change"], ["edits"]):   # not "save changes"
        sh = Shell(state)
        sh.view = view
        return sh.c_git(["diff"], None)
    # the RPG-style verbs that act directly
    if verb == "look" and not rest:
        return look(view, state)
    if verb in ("map",) and not rest:
        return Shell(state).c_tree(["-L", "2"], None)
    if verb == "inventory" and not rest:
        return inventory(view.root)
    if verb == "stats" and not rest:
        return stats(view.root)
    if verb == "quests" and not rest:
        return quests(view.root)
    if verb in ("recall", "search") and rest and rest[0] in ("lesson", "lessons", "memory", "self"):
        rest = rest[1:]
        return recall(view.root, rest)
    if verb == "recall":
        return recall(view.root, rest)
    if verb == "go" and rest:
        target = find_member(view.root, rest)
        if target:
            sh = Shell(state)
            sh.view = view
            sh.c_cd(["/" + target], None)
            return look(view, state)
    if verb == "examine" and rest:
        target = find_member(view.root, rest)
        if target:
            return examine(view.root, target)
    if verb == "save" and rest and rest[0] in ("changes", "change", "edits", "repository", "repo"):
        return save_changes_text(state)
    if verb == "list" and rest and rest[0] in ("commands", "command"):
        return commands_text(view.root, None if "all" in rest else 20)
    if verb in ("commands", "command"):                              # the shell's own hint says `commands`
        return commands_verb(view, state, rest)
    own = database_verbs(text, words, state, view)                 # focus, db, enable, prefer, request, advise ...
    if own is not None:
        return own
    if verb == "remember" and rest:
        kinds = list(memory().TYPES)
        kind = rest[0] if rest[0] in kinds else "lesson"
        summary = text.split(None, 2 if rest[0] in kinds else 1)[-1].strip(" \"'")
        return remember_candidate(state, kind, summary)
    # rapid routing: an exact command from the database (inside the focus first), or the person's learned alias
    con = db(view)
    focus = (state.get("focus") or {}).get("member")
    found = cmdb().lookup(con, text, focus)
    if found["status"] == "hit":
        return route_text(con, found["rows"][0], text, state, brief, found["via"])
    if found["status"] == "disabled":
        return (f"{text}: `{found['rows'][0]['command']}` is disabled in your preferences. `enable "
                f"{found['rows'][0]['command']}` turns it back on; say it in plain English to use the skill anyway.")
    if found["status"] == "ambiguous" and menu:
        rows = found["rows"][:4]
        cmdb().log_miss(con, text, "ambiguous", [r["member"] for r in rows], focus)
        options = [{"command": r["command"], "how": f"open {r['member']}"} for r in rows]
        out = choice_menu(state, text, options)
        state["menu"]["learn"] = True
        state["menu"]["members"] = [r["member"] for r in rows]
        return f"> {text}\n`{text}` is a command in several skills; pick one (your pick is remembered):\n" + out
    # everything else: find the best command in the catalogue
    off = {r[0] for r in con.execute("SELECT command FROM user_prefs WHERE enabled=0")}
    cmds = [c for c in catalogue(view.root) if cmdb().normal(c["command"]) not in off]
    target_words = [_stem(w) for w in rest]
    scored = []
    for c in cmds:
        cverb, _, cnoun = c["command"].partition(" ")
        cverb = VERB_SYNONYMS.get(cverb, cverb)                      # "build habit" answers "make habit" too
        vscore = 3 if cverb == verb else (1 if verb in _words(c.get("trigger", "") + " " + c["description"])[:12] else 0)
        nwords = {_stem(w) for w in _words(cnoun.replace("-", " ") + " " + c.get("target", "").replace("/", " ").replace("-", " "))}
        dwords = {_stem(w) for w in _words(c.get("trigger", "") + " " + c["description"])}
        nscore = sum(3 if w in nwords else (1 if w in dwords else 0) for w in target_words)
        if vscore == 0 and nscore < 3:                               # unknown verb, weak noun: say so, don't guess
            continue
        if vscore + nscore and (nscore or not target_words):
            scored.append((vscore + nscore + (0.5 if c["kind"] == "skill" else 0), c))
    scored.sort(key=lambda x: (-x[0], x[1]["command"]))
    if not scored:
        near = near_commands(text, cmds) if menu else []
        cmdb().log_miss(con, text, "unknown", [c["command"] for c in near], focus)
        if not near:
            return (f"{text}: I don't know that command. Try `commands`, `help`, or just say it in plain English. "
                    f"It is noted as wanted: `request command {text}` keeps it for adding to a skill.")
        out = f"{text}: I don't know that command. Did you mean:\n" + choice_menu(state, text, near)
        state["menu"]["learn"] = True
        return out
    best = scored[0][1]
    if brief:
        return f"{text}: {best['kind']} → {best['command']} ({best['how']})"
    alts = [c for _, c in scored[1:4] if c["command"] != best["command"]]
    lines = [f"> {text}", f"→ {best['command']}  [{best['kind']}{': ' + best['target'] if best['target'] and best['kind'] != 'built-in skill' else ''}]",
             f"  {best['description']}", f"  how: {best['how']}, then carry out the request with it"]
    if menu and alts and scored[0][0] - scored[1][0] < 1.5:
        lines[1] = lines[1].replace("→", "→ likeliest:", 1)
        lines.append("  ambiguous, so ask the person to pick a number instead of guessing:")
        ranked = [best] + alts
        prior = cmdb().last_pick(con, text)
        if prior and any(c["command"] == prior for c in ranked):
            ranked = sorted(ranked, key=lambda c: c["command"] != prior)
            lines.append(f"  (last time this was `{prior}`; picking it again makes it a direct route)")
        lines.append(choice_menu(state, text, ranked))
        state["menu"]["learn"] = True
        cmdb().log_miss(con, text, "ambiguous", [c["command"] for c in [best] + alts], focus)
    return "\n".join(lines)


# ---------------------------------------------------------------- numbered choices for ambiguous input

MENU_WORDS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "last": -1}
INFER_WORDS = {"0", "infer", "you decide", "you choose", "your call", "auto", "whatever"}


def choice_menu(state: dict, text: str, options: list[dict]) -> str:
    """Number OPTIONS, remember them, and return the menu; the next bare number or "last" picks one."""
    state["menu"] = {"for": text, "options": [c["command"] for c in options]}
    rows = [f"  {i}. {c['command']}  ({c['how']})" for i, c in enumerate(options, 1)]
    rows.append(f"  {len(options) + 1}. something else (say it in plain English)")
    rows.append("  0. infer: Claude answers its own question, says which it chose and why")
    return "\n".join(rows)


def pick_from_menu(text: str, state: dict) -> str | None:
    """A bare number or ordinal answers the last menu: returns the chosen command, or a note when it can't."""
    word = " ".join(text.strip().lower().rstrip(".)!").split())
    menu = state.get("menu")
    if menu and menu.get("kind") == "options":
        chosen = options_pick(word, menu)
        if chosen is not None:
            if chosen.startswith("option: ") and "[why option" not in chosen and "[infer from" not in chosen:
                state.pop("menu", None)                  # a menu answers once; `why N` and `0` keep it open
            return chosen
    if not menu and word.isdigit():
        return "pick: there is no open numbered menu; ask the person what the number refers to"
    if not menu and word in INFER_WORDS:
        return "pick: there is no open question to infer an answer to; carry on with the request as asked"
    if not menu or not (word.isdigit() or word in MENU_WORDS or word in INFER_WORDS):
        return None
    options = menu["options"]
    if word in INFER_WORDS:                                        # the menu stays, so a number can still override
        return f"inferred: {options[0]}"
    n = int(word) if word.isdigit() else MENU_WORDS[word]
    if n == -1:
        n = len(options)
    state.pop("menu", None)                                        # a menu answers once
    if n == len(options) + 1:
        return f"pick: {n} is 'something else'; ask the person what they meant, in plain English"
    if not 1 <= n <= len(options):
        state["menu"] = menu
        return f"pick: {word} is not on the menu for '{menu['for']}' (1-{len(options) + 1})"
    return options[n - 1]


# ---------------------------------------------------------------- options menus: "<topic> options"

OPTION_WORDS = {"options", "option", "choices", "choice", "menu"}
OPTION_FILLER = {"what", "are", "is", "show", "give", "list", "any", "all", "which", "can", "do", "have", "i", "we",
                 "there", "please", "get", "see", "available", "possible", "m", "s"}
MODIFIERS = {"quick": "quick: the shortest useful version of each", "deep": "deep: the full version of each",
             "fast": "quick: the shortest useful version of each", "full": "deep: the full version of each"}
MAX_OPTIONS = 9


def options_request(text: str, words: list[str], state: dict, view: View) -> str | None:
    """`training options`, `options for habits`, `what are my options`, `options 2`: a described numbered menu."""
    if not words or not set(words) & OPTION_WORDS or not (words[0] in OPTION_WORDS or words[-1] in OPTION_WORDS):
        return None
    if words == ["menu"]:
        return None                                                # the opener menu owns a bare `menu`
    noun = [w for w in words if w not in OPTION_WORDS | OPTION_FILLER]
    menu = state.get("menu")
    if len(noun) == 1 and noun[0].isdigit() and menu and menu.get("kind") == "options":   # drill into option N
        n = int(noun[0])
        targets = menu.get("targets") or []
        if not 1 <= n <= len(targets):
            return f"options: {n} is not on the menu for '{menu['for']}' (1-{len(targets)})"
        if not targets[n - 1]:
            return (f"options: option {n} ({menu['options'][n - 1]}) has no options of its own; describe it in a few "
                    f"lines with its trade-offs, then offer to start it")
        return options_menu(view.root, targets[n - 1], text, state)
    target = options_target(view.root, noun)
    if target is None:
        return (f"{text}: nothing in the skillset matches '{' '.join(noun)}'. Offer options from general knowledge in the "
                f"same shape (numbered, one line each, a rapid-reply line), or ask what the options are for")
    return options_menu(view.root, target, text, state)


def options_target(root: Path, noun: list[str]) -> str | None:
    """The member a topic names: the top for no topic, then a member name, then the best trigger or description."""
    if not noun:
        return ""
    found = find_member(root, noun)
    if found:
        return found
    stems = {_stem(w) for w in noun}
    best, best_score = None, 0
    for _d, m in skillset().walk(root):
        if m.error or not m.path:
            continue
        text = {_stem(w) for w in _words(m.trigger + " " + m.description)}
        score = len(stems & text) + (0.1 if m.kind == "skillset" else 0)
        if score > best_score:
            best, best_score = m.path, score
    return best if best_score >= 1 else None


def member_options(root: Path, target: str) -> list[tuple[str, str, str | None]]:
    """(label, description, member it opens or None): the member's "## Options" list, else its members."""
    ss = skillset()
    members = [m for _d, m in ss.walk(root) if not m.error]
    here = next((m for m in members if m.path == target), None) if target else None
    folder = here.folder if here else root
    doc = next((folder / d for d in ("SUBSKILL.md", "SKILLSET.md", "SKILL.md") if folder and (folder / d).is_file()),
               None)
    if doc:
        body = doc.read_text(encoding="utf-8")
        section = re.search(r"^## Options\n(.*?)(?=^## |\Z)", body, re.MULTILINE | re.DOTALL)
        if section:
            rows = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*[:.]?\s*(.*)$", section.group(1), re.MULTILINE)
            if rows:
                return [(label.rstrip(":"), desc.strip(), None) for label, desc in rows]
    children = [m for m in members if m.path and (m.path.rsplit("/", 1)[0] if "/" in m.path else "") == target]
    return [(m.name, m.trigger or ss.shorten(" ".join(m.description.split()), 90), m.path) for m in children]


def options_menu(root: Path, target: str, text: str, state: dict) -> str:
    everything = member_options(root, target)
    options, hidden = everything[:MAX_OPTIONS], len(everything) - MAX_OPTIONS
    where = target or "skillset-os"
    if not options:
        state.pop("menu", None)
        return (f"> {text}\n→ {where}  [options]\n  it lists no options and holds no members; describe its main "
                f"choices from its instructions in the same shape, or just do the task with it")
    state["menu"] = {"for": text, "kind": "options", "target": target,
                     "options": [label for label, _d, _t in options], "targets": [t for _l, _d, t in options]}
    n = len(options)
    lines = [f"> {text}", f"→ {where}  [options: {n}]"]
    lines += [f"  {i}. {label}: {desc}" if desc else f"  {i}. {label}" for i, (label, desc, _t) in enumerate(options, 1)]
    if hidden > 0:
        lines.append(f"  (+{hidden} more: `ls {where}` lists them all; name one to use it)")
    lines.append("  0. infer: Claude picks the likeliest, says which and why in one line")
    rapid = ["1"] + (["1 3"] if n >= 3 else []) + ["2 quick" if n >= 2 else "1 quick", f"{min(n, 4)} deep", "0",
                                                   f"why {min(n, 2)}"]
    if any(t for _l, _d, t in options):
        rapid.append("options 1")
    lines.append("  rapid: " + " · ".join(rapid))
    drill = ", options N opens an option's own options" if any(t for _l, _d, t in options) else ""
    lines.append(f"  power: combine numbers (1 3, 1+3), add quick or deep, why N explains one{drill}, 0 hands the "
                 "choice back, or type anything else")
    lines.append("  how: show every option with its description, then the rapid and power lines; where the chat has a "
                 "tap-to-choose tool, also offer up to four options there as short labels. Act on the reply at once")
    return "\n".join(lines)


def options_pick(word: str, menu: dict) -> str | None:
    """Answers to an options menu: `2`, `1 3`, `1+3 quick`, `why 2`, `0`. None when the reply is something else."""
    labels, targets = menu["options"], menu.get("targets") or [None] * len(menu["options"])
    where = menu.get("target") or "skillset-os"
    if word in INFER_WORDS:
        listed = "; ".join(f"{i}. {label}" for i, label in enumerate(labels, 1))
        return (f"option: → {where}  [infer from '{menu['for']}']\n  pick the likeliest of: {listed}. Say which and "
                f"why in one line, then do it now; the person can still type another number")
    m = re.fullmatch(r"(why\s+)?(\d+(?:\s*[ ,+&]\s*\d+)*)(?:\s+(quick|deep|fast|full))?", word)
    if not m:
        return None
    nums = [int(x) for x in re.findall(r"\d+", m.group(2))]
    bad = [x for x in nums if not 1 <= x <= len(labels)]
    if bad:
        return f"pick: {bad[0]} is not on the menu for '{menu['for']}' (1-{len(labels)}, or 0 to infer)"
    if m.group(1):
        x = nums[0]
        return (f"option: → {targets[x - 1] or where}  [why option {x}: {labels[x - 1]}]\n  explain in two or three "
                f"lines what it involves, what it gives and what it costs; the menu stays open")
    mod = MODIFIERS.get(m.group(3) or "", "")
    picks = [f"{x}. {labels[x - 1]}" + (f" → {targets[x - 1]}" if targets[x - 1] else "") for x in nums]
    return (f"option: > {word}\n→ {where}  [chosen from '{menu['for']}': " + "; then ".join(picks) + "]\n"
            + (f"  {mod}\n" if mod else "")
            + "  how: open the member" + ("s" if len({targets[x - 1] for x in nums} - {None}) > 1 else "") + " and do "
            + ("these now, in that order" if len(nums) > 1 else "it now") + "; no further confirmation needed")


OPENER_WORDS = {"hi", "hello", "hey", "start", "menu", "bored", "suggest", "suggestions", "begin"}
OPENER_CHOICES = [("look", "explore the skillset like a text adventure"), ("apps", "the twenty in-chat apps"),
                  ("train practise", "train a skill, yours or Claude's"),
                  ("review skillset", "check Skillset-OS for issues, version and pending edits")]


def opener_menu(words: list[str], state: dict, view: View) -> str | None:
    """A greeting or "I'm bored" gets numbered suggestions, one of them always a review of Skillset-OS."""
    core = [w for w in words if w not in {"i", "im", "am", "m", "so", "just", "there", "claude"}]
    if not core or len(core) > 2 or core[0] not in OPENER_WORDS:
        return None
    options = [{"command": c, "how": why} for c, why in OPENER_CHOICES]
    return "Some things to do here; pick a number:\n" + choice_menu(state, " ".join(words), options)


# words phone autocorrect is known to swap in for command words: typed -> likely meant
AUTOCORRECT = {"is": "ls", "Is": "ls", "od": "os", "so": "os", "cd.": "cd", "vat": "cat", "fins": "find", "fo": "go"}


def autocorrect_menu(text: str, words: list[str], state: dict, view: View) -> str | None:
    """Offer an autocorrect repair as a numbered reading instead of routing the swapped word blindly."""
    raw = text.split()
    swapped = [AUTOCORRECT.get(w, AUTOCORRECT.get(w.lower(), w)) for w in raw]
    if swapped == raw:
        return None
    repaired = " ".join(swapped)
    first = swapped[0].lower()
    if first not in ALIASES and not any(c["command"] == repaired.lower() for c in catalogue(view.root)) \
            and not (len(raw) > 1 and raw[-1].lower() in AUTOCORRECT and swapped[-1] == "os"):
        return None
    literal = resolve_verb_noun(text, state, view, brief=True, menu=False).split(": ", 1)[-1]
    menu_kept = state.get("menu")
    if repaired.split()[0].lower() not in ALIASES and \
            resolve_verb_noun(repaired, state, view, brief=True, menu=False).split(": ", 1)[-1] == literal:
        state["menu"] = menu_kept
        return None                                                # both readings land in the same place
    state["menu"] = menu_kept
    options = [{"command": repaired, "how": f"'{text}' looks autocorrected"},
               {"command": text, "how": f"as typed: {literal}"}]
    return f"'{text}' may be a phone autocorrect. Which did you mean?\n" + choice_menu(state, text, options)


def near_commands(text: str, cmds: list[dict], limit: int = 3) -> list[dict]:
    """Commands whose name looks like TEXT, for a numbered "did you mean" instead of a dead end."""
    import difflib
    by_name = {}
    for c in cmds:
        by_name.setdefault(c["command"], c)
    names = difflib.get_close_matches(text.lower(), list(by_name), n=limit, cutoff=0.6)
    return [by_name[n] for n in names]


def find_member(root: Path, words: list[str]) -> str | None:
    ss = skillset()
    want = "-".join(words)
    best, best_score = None, 0
    for _d, m in ss.walk(root):
        if m.error:
            continue
        score = 3 if m.name == want or m.path == want.replace("-", "/") else sum(w in m.name.split("-") for w in words)
        score += 0.1 if m.kind == "skillset" else 0
        if score > best_score:
            best, best_score = m.path, score
    return best if best_score >= 1 else None


def look(view: View, state: dict) -> str:
    real = view.real(state["cwd"])
    doc = next((real / d for d in ("SUBSKILL.md", "SKILLSET.md", "SKILL.md") if (real / d).is_file()), None)
    head = state["cwd"]
    if doc:
        data, _ = skillset().read(doc)
        head += f": {skillset().shorten(' '.join(str(data.get('description') or '').split()), 220)}"
    names = [f"{n}{'/' if d else ''}" for n, _p, d, _m in view.entries(real)]
    return head + "\n" + ("Here: " + "  ".join(names) if names else "Nothing here.")


def inventory(root: Path) -> str:
    ss = skillset()
    return "\n".join(f"{'  ' * d}{m.name}  [{m.label}] {m.trigger}" for d, m in ss.walk(root) if not m.error)


def examine(root: Path, path: str) -> str:
    m = skillset().resolve(root, path)
    lines = [f"{m.path}  [{m.label} {m.version}]", m.description, f"Use when: {m.trigger}", f"Read it: open {m.path}"]
    return "\n".join(lines)


def stats(root: Path) -> str:
    mem = memory()
    items = mem.load(root)
    approved = [i for i in items if i["status"] == "approved"]
    line = ", ".join(f"{k} {sum(1 for i in approved if i['type'] == k)}" for k in mem.TYPES)
    exams = [i for i in approved if i["type"] == "experiment" and "exam" in (i["summary"] + i.get("detail", "")).lower()]
    last = exams[-1]["summary"] if exams else "no curriculum exam recorded yet (`run exam`)"
    return f"self-memory: {len(approved)} approved ({line})\nlatest exam: {last}"


def quests(root: Path) -> str:
    items = [i for i in memory().load(root) if i["status"] == "approved" and i["type"] == "maintenance"]
    return "\n".join(f"[ ] {i['id']} {i['summary']}" for i in items) or "no open maintenance"


def recall(root: Path, words: list[str]) -> str:
    items = [i for i in memory().load(root) if i["status"] == "approved"]
    if words:
        items = [i for i in items if all(_stem(w) in memory().item_text(i).lower() for w in words)]
    return "\n".join(f"{i['id']:9} {i['summary']}" for i in items[:25]) or "nothing in self-memory matches"


def remember_candidate(state: dict, kind: str, summary: str) -> str:
    problems = [m for sev, m in memory().screen(summary) if sev == "error"]
    if problems:
        return "not remembered: " + "; ".join(problems)
    warns = [m for sev, m in memory().screen(summary) if sev == "warning"]
    state["journal"].append({"op": "memory", "type": kind, "summary": summary})
    return (f"remembered as a self-memory candidate ({kind}); it is added, screened and reviewed when the edits are "
            "applied" + (f"\nnote: {warns[0]}" if warns else ""))


def save_changes_text(state: dict) -> str:
    n = len(state["journal"])
    if not n:
        return "nothing remembered to save"
    return (f"{n} remembered edit(s) ready. To get an updated repository: pull a working copy (sync-skillset), then "
            "`python3 <top>/scripts/shell.py apply --wc <working copy>`, check, and package.")


def commands_text(root: Path, top: int | None, con=None) -> str:
    cmds = rank(root, catalogue(root))
    mine = []
    if con is not None:
        mine = [r for r in con.execute("SELECT command, description FROM routes WHERE favourite=1 AND enabled=1 "
                                       "GROUP BY command HAVING MAX(source='tree') = (source='tree') ORDER BY command")]
        off = {r[0] for r in con.execute("SELECT command FROM user_prefs WHERE enabled=0")}
        cmds = [c for c in cmds if c["command"] not in off]
    if top:                                   # the shell itself is not a command to suggest from inside the shell
        cmds = [c for c in cmds if c.get("target") != "command-line"][:top]
    width = max(len(c["command"]) for c in cmds)
    head = ("Most useful commands, generated from the installed skills, built-in skills, self-memory and routing "
            "evidence:" if top else "Every command:")
    body = head + "\n" + "\n".join(f"  {c['command']:<{width}}  {c['kind']:<14} {c['description']}" for c in cmds)
    if mine:
        body = "⭐ Yours:\n" + "\n".join(f"  {r[0]}  {r[1][:100]}" for r in mine) + "\n\n" + body
    if top and con is not None:
        body += ("\n\nEvery skill keeps a tree of its own commands: `commands tree <skill>`, `focus <skill>`, or "
                 "`db <sql>` to query them.")
    return body


# ================================================================ the command database: trees, focus, preferences

def route_text(con, row, text: str, state: dict, brief: bool = False, via: str = "exact") -> str:
    """What a routed command does, with its place in the skill's tree; sets the focus there."""
    c = cmdb()
    member, kind = row["member"], row["kind"]
    if row["source"] == "tree" and row["parent"] is None:          # a skill's root command names the skill itself
        own = con.execute("SELECT kind FROM commands WHERE member=? AND source='catalogue' AND kind IN "
                          "('skill','skillset','app')", (member,)).fetchone()
        kind = own["kind"] if own else ("skillset" if con.execute(
            "SELECT 1 FROM commands WHERE member LIKE ? AND source='tree' LIMIT 1", (member + "/%",)).fetchone() else "skill")
    if brief:
        return f"{text}: {kind} → {row['command']} ({row['how'] or 'open ' + member})"
    if row["source"] == "tree":
        state["focus"] = {"member": member, "command": row["command"]}
    elif kind in ("skill", "skillset") and member:
        state["focus"] = {"member": member, "command": None}
    path = " ▸ ".join(f"{r['emoji']} {r['command']}" for r in c.ancestry(con, row)) if row["source"] == "tree" else ""
    where = member.split("#")[0] if member else ""
    lines = [f"> {text}", f"→ {row['command']}  [{kind}{': ' + member if member and kind != 'built-in skill' else ''}]"
             + ("  (your alias)" if via == "alias" else "")]
    if path:
        lines.append(f"  in: {where or 'top'} ▸ {path}")
    lines.append(f"  {row['description']}")
    if row["source"] == "tree":
        lines.append(f"  how: open {where or 'the top SKILL.md'} and follow it, doing what this command's description "
                     "says; ask only for input the description names and the person has not given")
        kids = c.children(con, row["id"])
        if kids:
            lines.append("  runs, in order (skip any the person has already done; disabled ones are skipped):")
            lines += [f"    {i}. {k['emoji']} `{k['command']}`: {k['description']}" for i, k in
                      enumerate([k for k in kids if k["enabled"]], 1)]
        lines.append(f"  focus: {where or 'top'} ▸ {row['command']}  (`commands` shows the tree here; `unfocus` clears)")
    else:
        lines.append(f"  how: {row['how'] or 'open ' + member}, then carry out the request with it")
    return "\n".join(lines)


def focus_text(con, state: dict) -> str:
    c = cmdb()
    f = state.get("focus") or {}
    member = f.get("member")
    if member is None:
        return "no focus set: `focus <skill or command>` sets one; `commands` lists the most useful commands"
    tree = c.member_tree(con, member)
    if f.get("command"):                                 # the whole skill, with the focused command marked
        tree = [ln + "  👈 focus" if f"`{f['command']}`:" in ln and "👈" not in "".join(tree) else ln for ln in tree]
    head = f"Focus: {member or 'top'}" + (f" ▸ {f['command']}" if f.get("command") else "")
    empty = (f"(this member has no Commands tree yet: `request command <phrase> for {member}` or add a "
             "`## Commands` section)")
    out = [head, "", *(tree or [empty])]
    want = c.wanted(con, member or None)
    if want:
        out += ["", "Wanted here (missing or ambiguous, still intended):"] + want
    out += ["", ("Type any command above; `unfocus` clears the focus; `why <command>` explains one; "
                 "`db <sql>` queries the database.")]
    return "\n".join(out)


def commands_verb(view: View, state: dict, rest: list[str]) -> str:
    """`commands` [all | top | tree [member] | sql ...]; with a focus, the focused tree."""
    con = db(view)
    c = cmdb()
    if rest[:1] == ["sql"] or rest[:1] == ["db"]:
        return c.run_sql(con, " ".join(rest[1:]))
    if rest[:1] in (["tree"], ["trees"]):
        target = rest[1:]
        if not target:
            return focus_text(con, state) if state.get("focus") else "\n".join(c.member_tree(con, "", 1))
        if target == ["all"]:
            out = []
            for r in con.execute("SELECT member FROM commands WHERE source='tree' AND parent IS NULL ORDER BY member"):
                out += c.member_tree(con, r[0], 9, with_members=False)
            return "\n".join(out)
        member = find_member(view.root, target)
        if member is None:
            return f"no skill matches {' '.join(target)}"
        return "\n".join(c.member_tree(con, member))
    if rest and rest[0] in ("all", "every"):
        return commands_text(view.root, None)
    if state.get("focus") and not rest:
        return focus_text(con, state)
    return commands_text(view.root, 20, con)


def database_verbs(text: str, words: list[str], state: dict, view: View) -> str | None:
    """The command database's own verbs, or None when TEXT is not one of them."""
    c = cmdb()
    verb, rest = words[0], words[1:]
    raw = text.strip()
    after = raw.split(None, 1)[1].strip() if len(raw.split(None, 1)) > 1 else ""
    if verb == "db":
        return c.run_sql(db(view), after)
    if verb == "unfocus":
        state.pop("focus", None)
        return "focus cleared; commands route across the whole skillset again"
    if verb == "focus":
        con = db(view)
        if not rest:
            return focus_text(con, state)
        found = c.lookup(con, after, (state.get("focus") or {}).get("member"))
        if found["status"] in ("hit", "disabled"):
            row = found["rows"][0]
            state["focus"] = {"member": row["member"], "command": row["command"] if row["source"] == "tree" else None}
            return focus_text(con, state)
        member = find_member(view.root, rest)
        if member is not None:
            state["focus"] = {"member": member, "command": None}
            return focus_text(con, state)
        return None                                     # "focus attention" and friends: an ordinary command
    if verb == "why" and rest and not rest[0].isdigit():
        con = db(view)
        rows = con.execute("SELECT * FROM routes WHERE command=?", (c.normal(after),)).fetchall()
        if not rows:
            return f"`{after}` is not a known command. `advise commands {after}` suggests some."
        out = []
        for r in rows:
            out.append(f"`{r['command']}` [{r['kind']}{': ' + r['member'] if r['member'] else ''}]"
                       + ("" if r["enabled"] else " 🚫 disabled") + (" ⭐" if r["favourite"] else ""))
            if r["source"] == "tree":
                out.append("  " + " ▸ ".join(f"{a['emoji']} {a['meme'] or a['command']}" for a in c.ancestry(con, r)))
            out.append(f"  {r['description']}")
        return "\n".join(out)
    if verb in ("enable", "disable", "prefer", "unprefer") and rest:
        con = db(view)
        target = c.normal(after)
        if not c.known(con, target):
            return (f"`{target}` is not a known command, so there is nothing to {verb}. "
                    f"`request command {target}` asks for it.")
        if verb in ("enable", "disable"):
            c.set_pref(con, target, enabled=int(verb == "enable"))
            return f"{'enabled' if verb == 'enable' else 'disabled'}: `{target}` (this session; `save favourites` keeps it)"
        c.set_pref(con, target, favourite=int(verb == "prefer"))
        favs = state.setdefault("favourites", [])
        if verb == "prefer" and target not in favs:
            favs.append(target)
        if verb == "unprefer":
            state["favourites"] = [f for f in favs if f != target]
        return f"{'⭐ preferred' if verb == 'prefer' else 'no longer preferred'}: `{target}`"
    if verb == "alias" and "=" in raw:
        con = db(view)
        phrase, command = (x.strip(" `\"'") for x in after.split("=", 1))
        if not c.known(con, command):
            return f"`{command}` is not a known command; an alias must point at one"
        row = con.execute("SELECT member FROM routes WHERE command=? ORDER BY source DESC", (c.normal(command),)).fetchone()
        c.learn(con, phrase, command, row["member"], confirmed=True)
        return f"alias kept for this session: `{c.normal(phrase)}` → `{c.normal(command)}`"
    if verb == "request" and rest[:1] in (["command"], ["commands"]):
        body = after.split(None, 1)[1] if len(after.split(None, 1)) > 1 else ""
        note = ""
        if ":" in body:
            body, note = (x.strip() for x in body.split(":", 1))
        member = None
        m = re.match(r"^(.*?)\s+for\s+(\S+)$", body)
        if m:
            member = find_member(view.root, re.split(r"[/\-\s]+", m[2])) or m[2]
            body = m[1]
        if not body.strip():
            return "request command <phrase> [for <skill>] [: what it should do]"
        con = db(view)
        n = c.request(con, body, member or (state.get("focus") or {}).get("member"), note)
        return (f"requested #{n}: `{c.normal(body)}`" + (f" for {member}" if member else "")
                + ". It shows under Wanted in that skill's tree; `save changes` can add it to the skill's Commands "
                  "section for good, and `save favourites` keeps the request in your file.")
    if verb in ("advise", "suggest", "recommend", "ideas") and rest[:1] in (["command"], ["commands"]):
        return c.advice(db(view), " ".join(rest[1:]) or None)
    if verb == "new" and rest[:1] in (["command"], ["commands"]):
        return c.advice(db(view), " ".join(rest[1:]) or None)
    return None


# ================================================================ favourites: the person's own list

def favourites(state: dict, action: str, args: list[str]) -> str:
    favs = state["favourites"]
    if action == "add":
        cmd = " ".join(args).strip()
        if not cmd:
            return "give the command to add"
        if cmd not in favs:
            favs.append(cmd)
        con = db_quiet(state) if "journal" in state else None
        if con is not None:
            cmdb().set_pref(con, cmd, favourite=1)
        return f"added for this session: {cmd} (`favourites save` writes a file you keep)"
    if action == "remove":
        cmd = " ".join(args).strip()
        state["favourites"] = [f for f in favs if f != cmd]
        return f"removed: {cmd}"
    if action == "clear":
        state["favourites"] = []
        return "cleared"
    if action == "list":
        return "\n".join(f"{i}. {f}" for i, f in enumerate(favs, 1)) or "no favourites this session"
    if action == "save":
        out = Path(args[0]) if args else Path("/mnt/user-data/outputs") / FAV_FILE
        out.parent.mkdir(parents=True, exist_ok=True)
        text = [FAV_MARK, "# My Skillset-OS commands", "",
                ("Your list, kept by you. Skillset-OS does not store it: upload this file and say \"load my commands\" "
                "to bring it back."), ""] + [f"- `{f}`" for f in favs]
        con = db_quiet(state) if "journal" in state else None
        extra = []
        if con is not None:
            _fav, extra = cmdb().export_lines(con)
            text += [ln for ln in _fav if ln.replace("⭐ ", "") not in text]
        out.write_text("\n".join(text + extra) + "\n", encoding="utf-8")
        return f"wrote {out} ({len(favs)} commands" + (", with your disabled commands, aliases and requests" if extra else "") + ")"
    if action == "load":
        if not args:
            return "give the file to load"
        text = Path(args[0]).read_text(encoding="utf-8")
        head = re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]
        con = db_quiet(state) if "journal" in state else None
        counts = cmdb().import_text(con, text) if con is not None else {}
        loaded = re.findall(r"^\s*[-*]\s*(?:⭐\s*)?`([^`]+)`", head, re.MULTILINE) or [ln.strip("-* ").strip() for ln in head.splitlines()
                                                                     if ln.strip() and not ln.startswith(("#", "<!--"))]
        for f in loaded:
            if f not in favs:
                favs.append(f)
            if con is not None:
                cmdb().set_pref(con, f, favourite=1)
        more = ", ".join(f"{v} {k}" for k, v in counts.items() if v)
        return f"loaded {len(loaded)} commands for this session" + (f" (and {more})" if more else "")
    return "favourites add|remove|list|save [FILE]|load FILE|clear"


# ================================================================ command line of the tool itself

def main(argv: list[str] | None = None) -> int:
    if hasattr(signal, "SIGPIPE") and __name__ == "__main__":
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)             # `| head` ends quietly
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("line", nargs="+")
    p = sub.add_parser("do")
    p.add_argument("words", nargs="+")
    p = sub.add_parser("commands")
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--all", action="store_true")
    p = sub.add_parser("edit")
    p.add_argument("path")
    p.add_argument("--content")
    p.add_argument("--content-file")
    p.add_argument("--delete", action="store_true")
    sub.add_parser("journal")
    sub.add_parser("diff")
    p = sub.add_parser("drop")
    p.add_argument("n", type=int)
    sub.add_parser("clear-journal")
    p = sub.add_parser("apply")
    p.add_argument("--wc", required=True, type=Path)
    p = sub.add_parser("favourites")
    p.add_argument("action", nargs="?", default="list")
    p.add_argument("args", nargs="*")
    p = sub.add_parser("db")
    p.add_argument("query", nargs="*")
    p = sub.add_parser("tree")
    p.add_argument("member", nargs="*")
    p = sub.add_parser("mode")
    p.add_argument("value", nargs="?", choices=["shell", "english", "auto"])
    sub.add_parser("reset")
    args = ap.parse_args(argv)
    state = load_state()
    code = 0
    try:
        if args.cmd == "run":
            sh = Shell(state)
            line = " ".join(args.line)
            if state["mode"] == "english" and ALIASES.get((tokens(line) or [""])[0].lower()):
                state["mode"] = "auto"
            print(f"skillset-os:{state['cwd']}$ {line}")
            out = sh.run(line)
            if out:
                print(out)
        elif args.cmd == "do":
            out = resolve_verb_noun(" ".join(args.words), state)
            if state.get("learned"):
                out += "\n  learned: " + state.pop("learned")
            save_state(state)                           # before printing: a closed pipe must not lose the focus
            print(out)
        elif args.cmd == "commands":
            view = View(state)
            print(commands_text(view.root, None if args.all else args.top, db(view)))
        elif args.cmd == "db":
            print(cmdb().run_sql(db(View(state)), " ".join(args.query)))
        elif args.cmd == "tree":
            print(commands_verb(View(state), state, ["tree"] + args.member))
        elif args.cmd == "edit":
            sh = Shell(state)
            v, rel = sh.target_rel(args.path)
            if args.delete:
                print(sh.remember({"op": "delete", "path": rel}, f"delete {v}"))
            else:
                content = Path(args.content_file).read_text(encoding="utf-8") if args.content_file else (args.content or "")
                print(sh.remember({"op": "write", "path": rel, "content": content}, f"write {v}"))
        elif args.cmd == "journal":
            print(Shell(state).c_git(["status"], None))
        elif args.cmd == "diff":
            print(journal_diff(base_root(), state["journal"]) or "(no differences)")
        elif args.cmd == "drop":
            op = state["journal"].pop(args.n - 1)
            print(f"forgot: {describe(op)}")
        elif args.cmd == "clear-journal":
            state["journal"] = []
            print("forgot every remembered edit")
        elif args.cmd == "apply":
            wc = args.wc.resolve()
            if not (wc / "SKILL.md").is_file() or not (wc / ".git").exists():
                raise ShellError(f"{wc} is not a working copy (pull one with sync-skillset first)")
            notes = apply_journal(wc, state["journal"])
            mem = memory()
            for op in [o for o in state["journal"] if o["op"] == "memory"]:
                item = mem.add(wc, op["type"], op["summary"], source="remembered from the command line")
                print(f"self-memory candidate {item['id']}: review and approve it with memory.py")
            print(f"applied {len(state['journal']) - len(notes)} edit(s) to {wc}; NEXT `skillset.py index`, `check`, then package")
            state["journal"] = []
        elif args.cmd == "favourites":
            print(favourites(state, args.action, args.args))
        elif args.cmd == "mode":
            if args.value:
                state["mode"] = args.value
            print(f"mode: {state['mode']} (auto: commands are run, plain English is answered as usual)")
        elif args.cmd == "reset":
            state = {"cwd": "/", "stack": [], "history": [], "journal": [], "aliases": {}, "favourites": [], "mode": "auto"}
            print("session forgotten")
    except ShellError as exc:
        print(str(exc))
        code = 1
    except (OSError, KeyError, IndexError) as exc:
        print(f"error: {exc}")
        code = 1
    save_state(state)
    return code


if __name__ == "__main__":
    sys.exit(main())

"""The command database: rapid routing from typed commands to the skills that do them.

Every member keeps its own `## Commands` section: an emoji tree of the commands that should trigger it, grouped
under emoji meme headings, nested as deep as the skill needs. Each line is one command:

    - 🐞 **Find it, fix it, prove it** · `debug issue`: what the skill does when this command is typed.
      - 🔬 `reproduce bug`: ...

A line with a **bold meme** is a heading (a group): its command sets focus on the group and runs the commands
under it in order. The first line is the member's root. The member file is the source of truth; this module
indexes every tree, plus the generated catalogue (shell verbs, apps, built-in skills, tools), into SQLite and
rebuilds it whenever a member file changes. The person's own tables (preferences, learned aliases, requests,
misses) survive rebuilds, stay in the session, and go home with them in a file they keep; they never enter
self-memory.

Routing order: the person's learned alias, then an exact enabled command (inside the current focus first),
then the caller's fuzzy matcher. Unknown and ambiguous phrases are logged as misses so intended commands are
maintained rather than lost.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from pathlib import Path

SECTION = "## Commands"
LINE_RE = re.compile(r"^(?P<indent> *)- (?P<emoji>\S+) (?:\*\*(?P<meme>[^*]+)\*\* · )?`(?P<command>[^`]+)`: (?P<desc>\S.*)$")
COMMAND_RE = re.compile(r"[a-z0-9][a-z0-9+#.-]*( [a-z0-9][a-z0-9+#.-]*){0,5}")
# first words that belong to the shell's own verbs: a tree command may not start with one
RESERVED_FIRST = {"focus", "unfocus", "db", "enable", "disable", "prefer", "unprefer", "alias", "unalias", "request",
                  "why", "go", "look", "recall", "remember", "save", "load", "commands", "command", "cd", "ls", "cat",
                  "open", "options", "menu", "infer", "start", "hi", "hello", "favourites", "exit", "help", "man"}
USER_TABLES = ("user_prefs", "user_aliases", "user_requests", "user_misses")
SCHEMA = """
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY, command TEXT NOT NULL, member TEXT NOT NULL, parent INTEGER, depth INTEGER NOT NULL,
    ord INTEGER NOT NULL, emoji TEXT, meme TEXT, description TEXT NOT NULL,
    kind TEXT NOT NULL,       -- group | command (from a Commands tree) | shell | app | skill | skillset | built-in skill | model/tool
    source TEXT NOT NULL,     -- tree | catalogue
    how TEXT
);
CREATE INDEX IF NOT EXISTS commands_by_phrase ON commands(command);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS user_prefs (command TEXT PRIMARY KEY, enabled INTEGER NOT NULL DEFAULT 1,
    favourite INTEGER NOT NULL DEFAULT 0, note TEXT);
CREATE TABLE IF NOT EXISTS user_aliases (phrase TEXT PRIMARY KEY, command TEXT NOT NULL, member TEXT);
CREATE TABLE IF NOT EXISTS user_requests (id INTEGER PRIMARY KEY, phrase TEXT NOT NULL, member TEXT, note TEXT,
    status TEXT NOT NULL DEFAULT 'open', created TEXT);
CREATE TABLE IF NOT EXISTS user_misses (phrase TEXT PRIMARY KEY, kind TEXT, count INTEGER NOT NULL DEFAULT 1,
    candidates TEXT, focus TEXT, resolved_to TEXT, last TEXT);
CREATE VIEW IF NOT EXISTS routes AS
    SELECT c.*, COALESCE(p.enabled, 1) AS enabled, COALESCE(p.favourite, 0) AS favourite
    FROM commands c LEFT JOIN user_prefs p ON p.command = c.command;
"""


# ================================================================ parsing a member's tree

def section(text: str) -> tuple[list[str], int] | None:
    """The lines of TEXT's Commands section and the line number it starts on, or None when it has none."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == SECTION:
            body = []
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("## ") or lines[j].startswith("<!-- folder:start"):
                    break
                body.append(lines[j])
            return body, i + 2
    return None


def parse(text: str, allow_reserved: bool = False) -> tuple[list[dict], list[str]]:
    """(nodes, problems) for the Commands tree in TEXT. Each node: depth, emoji, meme, command, description, parent.

    ALLOW_RESERVED is for the command-line member, which owns the shell's own verbs."""
    found = section(text)
    if found is None:
        return [], [f"no `{SECTION}` section"]
    body, start = found
    nodes, problems, stack = [], [], []
    for n, line in enumerate(body, start):
        if not line.strip():
            continue
        m = LINE_RE.match(line)
        if not m:
            problems.append(f"line {n}: not a command line (`- <emoji> [**meme** · ]`command`: description`)")
            continue
        indent = len(m["indent"])
        if indent % 2:
            problems.append(f"line {n}: indent by two spaces per level")
            continue
        depth = indent // 2
        if depth > len(stack):
            problems.append(f"line {n}: jumps more than one level deeper")
            continue
        if not nodes and depth:
            problems.append(f"line {n}: the first line is the root and is not indented")
        if nodes and depth == 0:
            problems.append(f"line {n}: only one root line; indent it under the root")
        cmd = " ".join(m["command"].split())
        if not COMMAND_RE.fullmatch(cmd):
            problems.append(f"line {n}: `{cmd}` must be one to six lowercase words")
        elif cmd.split()[0] in RESERVED_FIRST and not allow_reserved:
            problems.append(f"line {n}: `{cmd}` starts with `{cmd.split()[0]}`, a word the shell reserves")
        stack = stack[:depth]
        node = {"depth": depth, "emoji": m["emoji"], "meme": (m["meme"] or "").strip(), "command": cmd,
                "description": m["desc"].strip(), "parent": stack[-1] if stack else None, "line": n}
        nodes.append(node)
        stack.append(len(nodes) - 1)
    for i, node in enumerate(nodes):
        has_children = any(c["parent"] == i for c in nodes)
        if has_children and not node["meme"]:
            problems.append(f"line {node['line']}: `{node['command']}` has commands under it, so give it a "
                            "**meme** heading")
        if len(node["description"]) < 25:
            problems.append(f"line {node['line']}: `{node['command']}` needs a description of how the skill uses it")
    if nodes and not nodes[0]["meme"]:
        problems.append(f"line {nodes[0]['line']}: the root line needs a **meme** heading")
    seen: dict[str, int] = {}
    for node in nodes:
        if node["command"] in seen:
            problems.append(f"line {node['line']}: `{node['command']}` is listed twice")
        seen[node["command"]] = node["line"]
    return nodes, problems


# ================================================================ building the database

def normal(phrase: str) -> str:
    return " ".join(re.sub(r"[^\w+#.\- ]", " ", phrase.lower().replace("`", "")).split())


def fingerprint(docs: list[tuple[str, Path]], extra: str) -> str:
    h = hashlib.sha256(extra.encode())
    for path, doc in docs:
        h.update(path.encode())
        try:
            h.update(doc.read_bytes())
        except OSError:
            pass
    return h.hexdigest()


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def open_db(db_path: Path, docs: list[tuple[str, Path]], catalogue_fn, force: bool = False) -> sqlite3.Connection:
    """The database at DB_PATH, rebuilt from DOCS ((member path, instructions file)) when any of them changed.

    CATALOGUE_FN() returns the generated commands ({command, how, description, kind, target}); it is called only
    on a rebuild. User tables are kept across rebuilds."""
    con = connect(db_path)
    stamp = fingerprint(docs, "v1")
    row = con.execute("SELECT value FROM meta WHERE key='fingerprint'").fetchone()
    if row and row["value"] == stamp and not force:
        return con
    con.execute("DELETE FROM commands")
    for member, doc in docs:
        try:
            nodes, _ = parse(doc.read_text(encoding="utf-8"), allow_reserved=True)
        except OSError:
            continue
        ids: list[int] = []
        for n, node in enumerate(nodes):
            has_children = any(c["parent"] == n for c in nodes)
            cur = con.execute(
                "INSERT INTO commands (command, member, parent, depth, ord, emoji, meme, description, kind, source, how)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (node["command"], member, ids[node["parent"]] if node["parent"] is not None else None, node["depth"],
                 n, node["emoji"], node["meme"], node["description"], "group" if has_children else "command", "tree",
                 f"open {member}" if member else "read SKILL.md"))
            ids.append(cur.lastrowid)
    for n, c in enumerate(catalogue_fn()):
        con.execute("INSERT INTO commands (command, member, parent, depth, ord, emoji, meme, description, kind, source,"
                    " how) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (normal(c["command"]), c.get("target") or "", None, 0, n, "", "", c["description"], c["kind"],
                     "catalogue", c.get("how") or ""))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('fingerprint', ?)", (stamp,))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('built', ?)", (time.strftime("%Y-%m-%d %H:%M:%S"),))
    con.commit()
    return con


# ================================================================ routing

def children(con: sqlite3.Connection, node_id: int) -> list[sqlite3.Row]:
    return con.execute("SELECT * FROM routes WHERE parent=? ORDER BY ord", (node_id,)).fetchall()


def ancestry(con: sqlite3.Connection, row: sqlite3.Row) -> list[sqlite3.Row]:
    out = [row]
    while out[-1]["parent"] is not None:
        out.append(con.execute("SELECT * FROM routes WHERE id=?", (out[-1]["parent"],)).fetchone())
    return list(reversed(out))


def lookup(con: sqlite3.Connection, phrase: str, focus: str | None = None) -> dict:
    """Route PHRASE. Returns {status: hit|disabled|ambiguous|none, rows: [...], via: alias|exact|...}."""
    p = normal(phrase)
    alias = con.execute("SELECT * FROM user_aliases WHERE phrase=?", (p,)).fetchone()
    if alias:
        rows = con.execute("SELECT * FROM routes WHERE command=? AND (member=? OR ? IS NULL) ORDER BY source DESC",
                           (alias["command"], alias["member"], alias["member"])).fetchall()
        if rows:
            return {"status": "hit" if rows[0]["enabled"] else "disabled", "rows": rows[:1], "via": "alias"}
    rows = con.execute("SELECT * FROM routes WHERE command=?", (p,)).fetchall()
    if not rows:
        return {"status": "none", "rows": [], "via": ""}
    enabled = [r for r in rows if r["enabled"]]
    if not enabled:
        return {"status": "disabled", "rows": rows[:1], "via": "exact"}
    if focus:                                       # inside the focus first
        inside = [r for r in enabled if r["member"] == focus or r["member"].startswith(focus + "/")]
        if inside:
            enabled = inside
    tree = [r for r in enabled if r["source"] == "tree"]
    pool = tree or enabled
    targets = {(r["member"], r["source"]) for r in pool}
    if len({t[0] for t in targets}) > 1:
        return {"status": "ambiguous", "rows": pool, "via": "exact"}
    return {"status": "hit", "rows": pool[:1], "via": "exact"}


def log_miss(con: sqlite3.Connection, phrase: str, kind: str, candidates: list[str], focus: str | None) -> None:
    p = normal(phrase)
    if not p or len(p) > 80:
        return
    con.execute("INSERT INTO user_misses (phrase, kind, count, candidates, focus, last) VALUES (?,?,1,?,?,?) "
                "ON CONFLICT(phrase) DO UPDATE SET count=count+1, kind=excluded.kind, candidates=excluded.candidates,"
                " focus=excluded.focus, last=excluded.last",
                (p, kind, json.dumps(candidates), focus, time.strftime("%Y-%m-%d %H:%M")))
    con.commit()


def learn(con: sqlite3.Connection, phrase: str, command: str, member: str | None, confirmed: bool = False) -> bool:
    """The person picked COMMAND for PHRASE. The first pick is remembered and offered first next time; the same
    pick twice, or CONFIRMED (an explicit alias), makes PHRASE route straight there. Returns True once aliased."""
    p, c = normal(phrase), normal(command)
    if not p or p == c:
        return False
    before = con.execute("SELECT resolved_to FROM user_misses WHERE phrase=?", (p,)).fetchone()
    con.execute("INSERT INTO user_misses (phrase, kind, count, resolved_to, last) VALUES (?, 'picked', 0, ?, ?) "
                "ON CONFLICT(phrase) DO UPDATE SET resolved_to=excluded.resolved_to, last=excluded.last",
                (p, c, time.strftime("%Y-%m-%d %H:%M")))
    aliased = confirmed or bool(before and before["resolved_to"] == c)
    if aliased:
        con.execute("INSERT OR REPLACE INTO user_aliases VALUES (?,?,?)", (p, c, member))
    con.commit()
    return aliased


def last_pick(con: sqlite3.Connection, phrase: str) -> str | None:
    row = con.execute("SELECT resolved_to FROM user_misses WHERE phrase=?", (normal(phrase),)).fetchone()
    return row["resolved_to"] if row else None


# ================================================================ showing trees

def mark(row: sqlite3.Row) -> str:
    return ("" if row["enabled"] else " 🚫 disabled") + (" ⭐" if row["favourite"] else "")


def render_line(row: sqlite3.Row, depth: int) -> str:
    head = f"**{row['meme']}** · " if row["meme"] else ""
    return f"{'  ' * depth}- {row['emoji']} {head}`{row['command']}`: {row['description']}{mark(row)}"


def render_node(con: sqlite3.Connection, row: sqlite3.Row, depth: int = 0, max_depth: int = 9) -> list[str]:
    out = [render_line(row, depth)]
    if depth < max_depth:
        for child in children(con, row["id"]):
            out += render_node(con, child, depth + 1, max_depth)
    return out


def root_of(con: sqlite3.Connection, member: str) -> sqlite3.Row | None:
    return con.execute("SELECT * FROM routes WHERE member=? AND source='tree' AND parent IS NULL", (member,)).fetchone()


def member_tree(con: sqlite3.Connection, member: str, depth: int = 9, with_members: bool = True) -> list[str]:
    """MEMBER's own tree; for a skillset, each direct member's root (and one level more) under it."""
    root = root_of(con, member)
    if root is None:
        return []
    out = render_node(con, root, 0, depth)
    if with_members:
        prefix = member + "/" if member else ""
        subs = con.execute("SELECT * FROM routes WHERE source='tree' AND parent IS NULL AND member LIKE ? "
                           "ORDER BY member", (prefix + "%",)).fetchall()
        direct = [r for r in subs if r["member"] and r["member"] != member and "/" not in r["member"][len(prefix):]]
        if direct:
            out.append(f"  - 🗂️ **Members** · `commands tree {member or 'all'}`: each member's own commands, "
                       "one level shown; focus a member to see all of its tree.")
            for r in direct:
                out += render_node(con, r, 2, 3)
    return out


def wanted(con: sqlite3.Connection, member: str | None) -> list[str]:
    """Intended commands still missing or ambiguous, for MEMBER (or everywhere)."""
    rows = con.execute("SELECT * FROM user_requests WHERE status='open' AND (? IS NULL OR member=? OR member LIKE ?)",
                       (member, member, f"{member}/%")).fetchall()
    misses = con.execute("SELECT * FROM user_misses WHERE resolved_to IS NULL AND kind != 'picked' AND (? IS NULL OR focus=? OR focus LIKE ?)"
                         " ORDER BY count DESC LIMIT 12", (member, member, f"{member}/%")).fetchall()
    out = [f"- ❓ `{r['phrase']}`{' for ' + r['member'] if r['member'] else ''}: requested"
           f"{': ' + r['note'] if r['note'] else ''}" for r in rows]
    out += [f"- 🧩 `{r['phrase']}`: {r['kind']} ×{r['count']}"
            + (f", candidates {', '.join(json.loads(r['candidates'] or '[]')[:3])}" if r["candidates"] not in (None, "[]")
               else "") for r in misses]
    return out


# ================================================================ SQL, guarded

def _authorizer(action, arg1, arg2, db_name, trigger):
    reading = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}
    if action in reading:
        return sqlite3.SQLITE_OK
    if action in (sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE) and arg1 in USER_TABLES:
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_TRANSACTION or action == sqlite3.SQLITE_PRAGMA and arg1 in ("table_info", "table_list"):
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def run_sql(con: sqlite3.Connection, query: str, limit: int = 60) -> str:
    """Run QUERY: reads anywhere, writes only to the person's own tables. Returns a text table."""
    q = query.strip().rstrip(";")
    if not q:
        return schema_text(con)
    con.set_authorizer(_authorizer)
    try:
        cur = con.execute(q)
        rows = cur.fetchmany(limit + 1)
        con.commit()
    except sqlite3.DatabaseError as exc:
        return (f"sql refused or failed: {exc}. Reads work on every table and view; writes only on "
                f"{', '.join(USER_TABLES)}.")
    finally:
        con.set_authorizer(None)
    if cur.description is None:
        return f"ok: {cur.rowcount} row(s) changed"
    cols = [d[0] for d in cur.description]
    shown = [[("" if v is None else str(v)).replace("\n", " ")[:70] for v in r] for r in rows[:limit]]
    widths = [max(len(c), *(len(r[i]) for r in shown)) if shown else len(c) for i, c in enumerate(cols)]
    lines = ["  ".join(c.ljust(w) for c, w in zip(cols, widths)), "  ".join("-" * w for w in widths)]
    lines += ["  ".join(v.ljust(w) for v, w in zip(r, widths)) for r in shown]
    if len(rows) > limit:
        lines.append("... more rows (add LIMIT/OFFSET)")
    return "\n".join(lines) + f"\n({min(len(rows), limit)} row(s))"


def schema_text(con: sqlite3.Connection) -> str:
    n = con.execute("SELECT COUNT(*) FROM commands WHERE source='tree'").fetchone()[0]
    return "\n".join([
        f"Command database ({n} commands from the skills' own trees, plus the generated catalogue).",
        "Tables and views:",
        "  commands       id, command, member, parent, depth, ord, emoji, meme, description, kind, source, how",
        "  routes         commands + enabled, favourite (from your preferences): what routing uses",
        "  user_prefs     command, enabled, favourite, note                  (yours: writable)",
        "  user_aliases   phrase, command, member                            (yours: writable)",
        "  user_requests  id, phrase, member, note, status, created          (yours: writable)",
        "  user_misses    phrase, kind, count, candidates, focus, resolved_to, last   (yours: writable)",
        "Examples:",
        "  db SELECT command, description FROM routes WHERE member='software-dev/debug-issue' ORDER BY ord",
        "  db SELECT member, COUNT(*) n FROM commands WHERE source='tree' GROUP BY member ORDER BY n DESC",
        "  db SELECT * FROM routes WHERE favourite=1 OR enabled=0",
        "  db UPDATE user_misses SET resolved_to='debug issue' WHERE phrase='fix my bug'",
    ])


# ================================================================ the person's preferences

def set_pref(con: sqlite3.Connection, command: str, **fields) -> None:
    c = normal(command)
    con.execute("INSERT OR IGNORE INTO user_prefs (command) VALUES (?)", (c,))
    for key, value in fields.items():
        con.execute(f"UPDATE user_prefs SET {key}=? WHERE command=?", (value, c))
    con.commit()


def known(con: sqlite3.Connection, command: str) -> bool:
    return con.execute("SELECT 1 FROM commands WHERE command=?", (normal(command),)).fetchone() is not None


def request(con: sqlite3.Connection, phrase: str, member: str | None, note: str) -> int:
    cur = con.execute("INSERT INTO user_requests (phrase, member, note, created) VALUES (?,?,?,?)",
                      (normal(phrase), member, note, time.strftime("%Y-%m-%d %H:%M")))
    con.commit()
    return cur.lastrowid


def export_lines(con: sqlite3.Connection) -> list[str]:
    """The person's own tables as Markdown lines, read back by import_text."""
    out = []
    fav = con.execute("SELECT command FROM user_prefs WHERE favourite=1 ORDER BY command").fetchall()
    off = con.execute("SELECT command FROM user_prefs WHERE enabled=0 ORDER BY command").fetchall()
    ali = con.execute("SELECT * FROM user_aliases ORDER BY phrase").fetchall()
    req = con.execute("SELECT * FROM user_requests WHERE status='open' ORDER BY id").fetchall()
    if off:
        out += ["", "## Disabled", ""] + [f"- 🚫 `{r['command']}`" for r in off]
    if ali:
        out += ["", "## My aliases", ""] + [f"- `{r['phrase']}` → `{r['command']}`" + (f" in {r['member']}"
                                           if r["member"] else "") for r in ali]
    if req:
        out += ["", "## Requested commands", ""] + [f"- ❓ `{r['phrase']}`" + (f" for {r['member']}" if r["member"]
                                                   else "") + (f": {r['note']}" if r["note"] else "") for r in req]
    return [f"- ⭐ `{r['command']}`" for r in fav], out


def import_text(con: sqlite3.Connection, text: str) -> dict:
    """Read a kept command file back into the person's tables. Returns counts."""
    counts = {"disabled": 0, "aliases": 0, "requests": 0}
    part = ""
    for line in text.splitlines():
        if line.startswith("## "):
            part = line[3:].strip().lower()
            continue
        if part == "disabled":
            m = re.match(r"^\s*-\s*(?:🚫\s*)?`([^`]+)`", line)
            if m:
                set_pref(con, m[1], enabled=0)
                counts["disabled"] += 1
        elif part == "my aliases":
            m = re.match(r"^\s*-\s*`([^`]+)`\s*→\s*`([^`]+)`(?: in (\S+))?", line)
            if m:
                con.execute("INSERT OR REPLACE INTO user_aliases VALUES (?,?,?)", (normal(m[1]), normal(m[2]), m[3]))
                counts["aliases"] += 1
        elif part == "requested commands":
            m = re.match(r"^\s*-\s*(?:❓\s*)?`([^`]+)`(?: for (\S+?))?(?::\s*(.*))?$", line)
            if m:
                request(con, m[1], m[2], m[3] or "")
                counts["requests"] += 1
    con.commit()
    return counts


# ================================================================ advice about new commands

def advice(con: sqlite3.Connection, topic: str | None) -> str:
    """Evidence for open-ended advice on new commands: gaps, misses, requests, thin trees. Claude adds judgement."""
    like = f"%{normal(topic)}%" if topic else "%"
    thin = con.execute("SELECT member, COUNT(*) n FROM commands WHERE source='tree' AND member IN (SELECT member FROM "
                       "commands WHERE source='tree' AND (member LIKE :t OR command LIKE :t OR description LIKE :t)) "
                       "GROUP BY member ORDER BY n LIMIT 6", {"t": like}).fetchall()
    related = con.execute("SELECT DISTINCT command, member FROM commands WHERE source='tree' AND (command LIKE :t OR "
                          "description LIKE :t) LIMIT 8", {"t": like}).fetchall() if topic else []
    misses = con.execute("SELECT phrase, kind, count FROM user_misses WHERE resolved_to IS NULL ORDER BY count DESC "
                         "LIMIT 8").fetchall()
    reqs = con.execute("SELECT phrase, member, note FROM user_requests WHERE status='open' LIMIT 8").fetchall()
    fav = con.execute("SELECT member, COUNT(DISTINCT command) n FROM routes WHERE favourite=1 AND source='tree' "
                      "GROUP BY member ORDER BY n DESC LIMIT 5").fetchall()
    lines = [f"Evidence for new command ideas{' about ' + topic if topic else ''}:"]
    lines += ["  🧩 misses (typed, not found or ambiguous): " + (", ".join(f"`{r['phrase']}` ×{r['count']}"
                                                                      for r in misses) or "none yet")]
    lines += ["  ❓ open requests: " + (", ".join(f"`{r['phrase']}`" + (f" ({r['member']})" if r['member'] else "")
                                             for r in reqs) or "none")]
    lines += ["  🌱 thinnest related trees: " + (", ".join(f"{r['member'] or 'top'} ({r['n']})" for r in thin) or "none")]
    if related:
        lines += ["  🔗 existing related commands (avoid duplicates): " + ", ".join(f"`{r['command']}`" for r in related)]
    lines += ["  ⭐ where your favourites cluster: " + (", ".join(f"{r['member']} ({r['n']})" for r in fav) or "none")]
    lines.append("Now advise: propose 3-7 commands, each as a tree line (emoji, `verb noun`, how the skill uses it), "
                 "say which member and heading it belongs under, and why it would be used; offer `request command` "
                 "to keep any the person wants, or an edit to the member's Commands section to add them for good.")
    return "\n".join(lines)

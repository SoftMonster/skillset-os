#!/usr/bin/env python3
"""Skillset-OS self-memory: what the AI has learned about itself, kept so another AI can carry on.

The memory describes the AI and its operation: capabilities, skills, lessons, successes, failures,
experiments, evolution, limitations, maintenance and decisions. It is not a record of the user.
A conversation is evidence to learn from, never memory by itself.

Store: memory/items.jsonl, one item per line, sorted by id. memory/SELF.md is generated from it and is the
entry point for any AI loading this memory (progressive: SELF.md, then list/search, then show, then evidence).

Commands:
  add --type T --summary S [--detail D] [--source R] [--evidence E ...]   propose a candidate
  review ID [--forbid TERM ...]        screen a candidate against the user-protection boundary
  approve ID [--reason R] [--person-confirmed] [--forbid TERM ...]
                                       accept a candidate (the screen must pass; warnings need a reason;
                                       capability, evolution and decision items need the person's confirmation)
  supersede OLD --by NEW --person-confirmed   replace approved knowledge with a newer approved item
  set-status ID historical|archived --person-confirmed
  list [--type T] [--status S] [--all]  show items (approved by default)
  show ID                              one item with its provenance
  search TEXT [--all]                  find items by words
  check [--forbid TERM ...]            validate the store, its rules and SELF.md
  index                                regenerate memory/SELF.md
  export [--out memory-pack.zip]       package eligible memory for another AI
  import PACK [--as-candidates]        inherit memory from a pack
  acceptance [--pack PACK] [--forbid TERM ...]   can a fresh AI answer the takeover questions from it?

Approved content is never edited in place: a correction is a new item that supersedes the old one.
Authority comes from status and supersession, never from recency.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEMORY_DIR = "memory"
STORE = "items.jsonl"
ENTRY = "SELF.md"
PACK_TOP = "memory-pack"
PACK_FORMAT = "skillset-os-memory-pack"
PACK_VERSION = 1

TYPES = {  # type: (id prefix, pack file, heading, what it holds)
    "capability": ("CAP", "CAPABILITIES.md", "Capabilities", "What the AI can do."),
    "skill": ("SKL", "SKILLS.md", "Skills", "Reusable capabilities and skill definitions, with their status."),
    "lesson": ("LES", "LESSONS.md", "Lessons", "Reusable lessons learned from experience."),
    "success": ("SUC", "SUCCESSES.md", "Successes", "Approaches that demonstrably worked, and when."),
    "failure": ("FAI", "FAILURES.md", "Failures", "Approaches that failed, and why."),
    "experiment": ("EXP", "EXPERIMENTS.md", "Experiments", "Hypotheses tested, methods and results."),
    "evolution": ("EVO", "EVOLUTION.md", "Evolution", "Changes in capability or architecture."),
    "limitation": ("LIM", "LIMITATIONS.md", "Limitations", "Known weaknesses, uncertainty and failure modes."),
    "maintenance": ("MNT", "MAINTENANCE.md", "Maintenance", "Self-maintenance that is required or recommended."),
    "decision": ("DEC", "DECISIONS.md", "Decisions", "Authoritative decisions about the AI system itself."),
}
STATUSES = ("candidate", "approved", "historical", "superseded", "archived")
ACTIVE = ("approved",)                          # normal retrieval
EXPORTED = ("approved", "historical", "superseded")   # eligible for a pack (provenance included)
NEEDS_PERSON = {"capability", "evolution", "decision"}  # the AI may not approve these on its own
FIELDS = ("id", "type", "status", "summary", "detail", "source", "evidence", "validated", "created", "updated",
          "approved_by", "review_note", "supersedes", "superseded_by", "imported_from")
MAX_SUMMARY = 160

QUESTIONS = [  # the takeover questions a fresh AI must be able to answer, and where the answers live
    ("What capabilities do I have?", ["capability"]),
    ("What skills do I possess?", ["skill"]),
    ("What approaches have worked?", ["success"]),
    ("What approaches have failed?", ["failure"]),
    ("What lessons have I learned?", ["lesson"]),
    ("What experiments have I performed?", ["experiment"]),
    ("What limitations do I know about?", ["limitation"]),
    ("How have I evolved?", ["evolution"]),
    ("What should I be careful about when maintaining myself?", ["maintenance", "limitation"]),
]


class Refused(RuntimeError):
    """An action was refused; the message says why and what to do."""


# ================================================================ the user-protection screen

SECRET_RES = [
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}|"
                r"xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----"), "a key, token or private key"),
    (re.compile(r"\b(password|passwd|passcode|api[_ -]?key|secret|token)\s*[:=]\s*\S+", re.IGNORECASE), "a credential"),
]
PII_RES = [
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "an email address"),
    (re.compile(r"(?<![\w.])\+?\d[\d ()-]{8,}\d(?![\w.])"), "a phone number or long personal number"),
    (re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"), "a bank account number (IBAN)"),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "an IP address"),
    (re.compile(r"\b\d{1,5}\s+\w+\s+(street|st|road|rd|avenue|ave|lane|ln|drive|dr)\b", re.IGNORECASE), "a street address"),
]
# A fact about the user, not a lesson about the AI (spec: keep those as temporary task context).
USER_FACT_RE = re.compile(
    r"\b(the\s+)?(user|owner|person|customer|client|human)('s|s')?\s+(is|was|has|had|owns|owned|prefers|preferred|"
    r"likes|liked|dislikes|wants|wanted|lives|lived|works|worked|believes|thinks|feels|felt|said|told|asked for|"
    r"name|email|account|address|password|age|job|family|partner|repository|repo|project|computer|pc)\b", re.IGNORECASE)
PERSONAL_VOICE_RE = re.compile(r"\b(your|you're|you've|my|mine)\b", re.IGNORECASE)


def _luhn(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        n = int(ch)
        if alt:
            n = n * 2 - 9 if n > 4 else n * 2
        total, alt = total + n, not alt
    return total % 10 == 0


def screen(text: str, forbid: list[str] | None = None) -> list[tuple[str, str]]:
    """Check TEXT against the user-protection boundary: [(severity, message)], severity 'error' or 'warning'.

    Errors (never persisted): secrets, credentials, personal identifiers, and any FORBID term (for example the
    previous user's name or handle, given at review time and never stored). Warnings (need a reason to approve):
    wording that reads as a fact about the user rather than a lesson about the AI."""
    found: list[tuple[str, str]] = []
    for rx, what in SECRET_RES + PII_RES:
        if rx.search(text):
            found.append(("error", f"contains {what}; self-memory never stores it"))
    for m in re.finditer(r"\b(?:\d[ -]?){13,19}\b", text):
        digits = re.sub(r"\D", "", m.group(0))
        if 13 <= len(digits) <= 19 and _luhn(digits):
            found.append(("error", "contains a payment card number; self-memory never stores it"))
            break
    for term in forbid or []:
        if term.strip() and term.strip().lower() in text.lower():
            found.append(("error", "contains a term that identifies a person (from --forbid)"))
    if USER_FACT_RE.search(text):
        found.append(("warning", ("reads as a fact about the user; rewrite it as a lesson about the AI "
                                 "(\"When auditing multi-part repositories, verify completeness first\"), "
                                 "or keep it as temporary task context")))
    if PERSONAL_VOICE_RE.search(text):
        found.append(("warning", ("addresses or quotes a person (you/your/my); write self-memory about the AI's own "
                                 "operation")))
    return list(dict.fromkeys(found))


def item_text(item: dict) -> str:
    return " ".join(str(item.get(k) or "") for k in ("summary", "detail", "source", "validated", "review_note")) + " " + \
        " ".join(item.get("evidence") or [])


# ================================================================ the store

def store_path(root: Path) -> Path:
    return root / MEMORY_DIR / STORE


def load(root: Path) -> list[dict]:
    path = store_path(root)
    if not path.is_file():
        return []
    items = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                items.append(json.loads(line))
            except ValueError as exc:
                raise Refused(f"{MEMORY_DIR}/{STORE} line {n} is not valid JSON ({exc})") from exc
    return items


def save(root: Path, items: list[dict]) -> None:
    path = store_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(items, key=lambda i: i["id"])
    path.write_text("".join(json.dumps({k: i.get(k, _default(k)) for k in FIELDS}, ensure_ascii=False) + "\n"
                            for i in ordered), encoding="utf-8")


def _default(key: str):
    return [] if key in ("evidence", "supersedes") else ""


def today() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def find(items: list[dict], item_id: str) -> dict:
    for i in items:
        if i["id"] == item_id:
            return i
    raise Refused(f"no self-memory item {item_id}; `memory.py list --all` shows every id")


def new_id(items: list[dict], kind: str) -> str:
    prefix = TYPES[kind][0]
    used = [int(i["id"].split("-")[1]) for i in items if i["id"].startswith(prefix + "-")]
    return f"{prefix}-{(max(used) + 1) if used else 1:04d}"


def add(root: Path, kind: str, summary: str, detail: str = "", source: str = "", evidence: list[str] | None = None,
        validated: str = "") -> dict:
    kind = kind.lower()
    if kind not in TYPES:
        raise Refused(f"type must be one of {', '.join(TYPES)}")
    summary = " ".join(summary.split())
    if not summary or len(summary) > MAX_SUMMARY:
        raise Refused(f"the summary must be one line of 1 to {MAX_SUMMARY} characters")
    items = load(root)
    item = {k: _default(k) for k in FIELDS}
    item.update(id=new_id(items, kind), type=kind, status="candidate", summary=summary, detail=detail.strip(),
                source=source.strip(), evidence=list(evidence or []), validated=validated.strip(),
                created=today(), updated=today())
    problems = [m for sev, m in screen(item_text(item)) if sev == "error"]
    if problems:
        raise Refused("not stored: " + "; ".join(problems))  # a secret must not reach the file even as a candidate
    items.append(item)
    save(root, items)
    write_entry(root)
    return item


def approve(root: Path, item_id: str, reason: str = "", person_confirmed: bool = False,
            forbid: list[str] | None = None) -> dict:
    items = load(root)
    item = find(items, item_id)
    if item["status"] != "candidate":
        raise Refused(f"{item_id} is {item['status']}; only a candidate can be approved (correct approved "
                      "knowledge by adding a new item and superseding the old one)")
    if item["type"] in NEEDS_PERSON and not person_confirmed:
        raise Refused(f"a {item['type']} item changes what the AI is, so the person must confirm it: ask, then "
                      "approve with --person-confirmed")
    findings = screen(item_text(item), forbid)
    errors = [m for sev, m in findings if sev == "error"]
    warnings = [m for sev, m in findings if sev == "warning"]
    if errors:
        raise Refused("fails the user-protection screen: " + "; ".join(errors))
    if warnings and not reason.strip():
        raise Refused("needs rewording or a --reason: " + "; ".join(warnings))
    item.update(status="approved", updated=today(), approved_by="person" if person_confirmed else "ai-reviewed",
                review_note=reason.strip() if warnings else item.get("review_note", ""))
    save(root, items)
    write_entry(root)
    return item


def supersede(root: Path, old_id: str, new_id_: str, person_confirmed: bool) -> None:
    if not person_confirmed:
        raise Refused("replacing approved knowledge needs the person's confirmation: ask, then pass --person-confirmed")
    items = load(root)
    old, new = find(items, old_id), find(items, new_id_)
    if old["status"] != "approved" or new["status"] != "approved":
        raise Refused("both items must be approved (approve the replacement first)")
    if old_id == new_id_:
        raise Refused("an item cannot supersede itself")
    old.update(status="superseded", superseded_by=new_id_, updated=today())
    new["supersedes"] = sorted(set(new.get("supersedes") or []) | {old_id})
    new["updated"] = today()
    save(root, items)
    write_entry(root)


def set_status(root: Path, item_id: str, status: str, person_confirmed: bool) -> None:
    if status not in ("historical", "archived"):
        raise Refused("set-status only moves items to historical or archived")
    items = load(root)
    item = find(items, item_id)
    if item["status"] == "approved" and not person_confirmed:
        raise Refused("retiring approved knowledge needs the person's confirmation: pass --person-confirmed")
    item.update(status=status, updated=today())
    save(root, items)
    write_entry(root)


def check(root: Path, forbid: list[str] | None = None) -> tuple[list[str], list[str]]:
    """(errors, warnings) for the whole store: schema, statuses, ids, supersession, the screen and SELF.md."""
    errors, warnings = [], []
    try:
        items = load(root)
    except Refused as exc:
        return [str(exc)], []
    ids: dict[str, dict] = {}
    for i in items:
        iid = i.get("id", "?")
        missing = [k for k in ("id", "type", "status", "summary", "created") if not i.get(k)]
        if missing:
            errors.append(f"{iid}: missing {', '.join(missing)}")
            continue
        if iid in ids:
            errors.append(f"{iid}: duplicate id")
        ids[iid] = i
        if i["type"] not in TYPES:
            errors.append(f"{iid}: unknown type {i['type']}")
        elif not iid.startswith(TYPES[i["type"]][0] + "-"):
            errors.append(f"{iid}: id prefix does not match its type {i['type']}")
        if i["status"] not in STATUSES:
            errors.append(f"{iid}: unknown status {i['status']}")
        if len(i["summary"]) > MAX_SUMMARY:
            errors.append(f"{iid}: summary is over {MAX_SUMMARY} characters")
        for sev, msg in screen(item_text(i), forbid):
            if sev == "error":
                errors.append(f"{iid}: {msg}")
            elif i["status"] in ("approved", "historical") and not i.get("review_note"):
                warnings.append(f"{iid}: {msg}")
        if i["status"] == "approved" and i["type"] in NEEDS_PERSON and i.get("approved_by") != "person":
            errors.append(f"{iid}: a {i['type']} item must be approved by the person")
    for iid, i in ids.items():
        if i["status"] == "superseded":
            nxt = i.get("superseded_by")
            if not nxt or nxt not in ids:
                errors.append(f"{iid}: superseded without an existing superseded_by item")
        for old in i.get("supersedes") or []:
            if old not in ids or ids[old].get("superseded_by") != iid:
                errors.append(f"{iid}: supersedes {old}, which does not point back to it")
        seen, cur = set(), iid
        while cur in ids and ids[cur].get("superseded_by"):
            if cur in seen:
                errors.append(f"{iid}: supersession cycle")
                break
            seen.add(cur)
            cur = ids[cur]["superseded_by"]
    entry = root / MEMORY_DIR / ENTRY
    if items and (not entry.is_file() or entry.read_text(encoding="utf-8") != render_entry(root, items)):
        errors.append(f"{MEMORY_DIR}/{ENTRY} is out of date; run `skillset.py index` (or `memory.py index`)")
    return errors, warnings


# ================================================================ views

def by_type(items: list[dict], kind: str, statuses=ACTIVE) -> list[dict]:
    return [i for i in items if i["type"] == kind and i["status"] in statuses]


def provenance(i: dict) -> str:
    bits = [f"{i['status']}", f"learned {i['created']}"]
    if i.get("updated") and i["updated"] != i["created"]:
        bits.append(f"updated {i['updated']}")
    if i.get("source"):
        bits.append(f"from {i['source']}")
    if i.get("validated"):
        bits.append(f"validated: {i['validated']}")
    if i.get("approved_by"):
        bits.append(f"approved by {i['approved_by']}")
    if i.get("supersedes"):
        bits.append("supersedes " + ", ".join(i["supersedes"]))
    if i.get("superseded_by"):
        bits.append(f"superseded by {i['superseded_by']}")
    if i.get("imported_from"):
        bits.append(f"imported from {i['imported_from']}")
    return "; ".join(bits)


def render_item(i: dict) -> str:
    out = [f"### {i['id']}: {i['summary']}", ""]
    if i.get("detail"):
        out += [i["detail"], ""]
    if i.get("evidence"):
        out += ["Evidence: " + "; ".join(f"`{e}`" for e in i["evidence"]), ""]
    out += [f"*{provenance(i)}*", ""]
    return "\n".join(out)


def render_entry(root: Path, items: list[dict]) -> str:
    counts = {k: len(by_type(items, k)) for k in TYPES}
    lines = ["# Self-memory", "",
             "🧬 **Core meme:** Remember what makes the AI better, never a dossier on the person.", "",
             ("This is the AI's own persistent memory for Skillset-OS: its capabilities, skills, lessons, successes, "
             "failures, experiments, evolution, limitations, maintenance and decisions. It exists to improve the AI, "
             "not to accumulate knowledge about the user. Generated from `items.jsonl` by `index`; do not edit by hand."),
             "",
             "## Load it progressively", "",
             "1. Read this file: the rules and a one-line index of everything approved.",
             ("2. Find what the task needs: `python3 <top>/scripts/memory.py list --type lesson` or "
             "`memory.py search <words>`."),
             "3. Read the items you need in full: `memory.py show <id>`.",
             "4. Only then open the evidence an item cites, if you must check it.", "",
             "## Taking over", "",
             ("A new AI continues from here without the one that wrote it: understand the system (the top `SKILL.md`), "
             "discover capabilities and skills (below, and `skillset.py tree`), read the lessons, successes and "
             "failures relevant to the work, note the limitations and open maintenance items, continue, and record "
             "genuinely new self-knowledge through the pipeline below. `memory.py acceptance` checks that the takeover "
             "questions can be answered from this memory."), "",
             "## Rules", "",
             ("- **A conversation is evidence, not memory.** Reflect, extract candidates, classify, screen, approve, "
             "index; then it can be exported and imported. The `self-memory` member of `skillset-tools` walks "
             "through it."),
             ("- **The user-protection boundary:** no secrets or credentials, no identifying or sensitive personal "
             "information, no conversation kept because it happened, no profile of the user and no inferences about "
             "them. A fact about the user stays temporary task context; only a lesson about the AI qualifies."),
             ("- **Status decides authority, not recency.** Only approved items guide work. Historical items give "
             "context, superseded items point to their replacement, archived items are left out."),
             ("- **No silent rewrites.** Approved content is never edited; a correction is a new item that supersedes "
             "the old one. Capability, evolution and decision items, supersession and retirement need the person's "
             "confirmation."), "",
             "## Index", ""]
    for kind, (prefix, _f, heading, what) in TYPES.items():
        lines += [f"### {heading} ({counts[kind]})", "", what, ""]
        for i in by_type(items, kind):
            lines.append(f"- `{i['id']}` {i['summary']}")
        historical = by_type(items, kind, ("historical",))
        if historical:
            lines.append("- Historical: " + ", ".join(f"`{i['id']}`" for i in historical))
        lines.append("")
    pending = [i for i in items if i["status"] == "candidate"]
    if pending:
        lines += ["## Candidates awaiting review", ""] + [f"- `{i['id']}` ({i['type']}) {i['summary']}" for i in pending] + [""]
    return "\n".join(lines).rstrip("\n") + "\n"


def write_entry(root: Path) -> None:
    items = load(root)
    if items or (root / MEMORY_DIR).is_dir():
        (root / MEMORY_DIR).mkdir(parents=True, exist_ok=True)
        (root / MEMORY_DIR / ENTRY).write_text(render_entry(root, items), encoding="utf-8")


# ================================================================ export and import

def _skillset_module():
    spec = importlib.util.spec_from_file_location("skillset", HERE / "skillset.py")
    mod = sys.modules.get("skillset")
    if mod is not None and getattr(mod, "__file__", None) and Path(mod.__file__).resolve() == (HERE / "skillset.py"):
        return mod
    mod = importlib.util.module_from_spec(spec)
    sys.modules["skillset"] = mod
    spec.loader.exec_module(mod)
    return mod


def skill_rows(root: Path) -> list[str]:
    """Every member of the skillset as a skill the AI possesses: path, kind, version, what it is for."""
    try:
        ss = _skillset_module()
        rows = []
        for depth, m in ss.walk(root):
            rows.append(f"{'  ' * depth}- `{m.path}` ({m.label} {m.version}): {ss.shorten(m.description, 160)}")
        return rows
    except (OSError, ValueError, KeyError, RuntimeError, ImportError) as exc:  # the pack must still be written from memory alone
        return [f"- (the skillset could not be read here: {exc})"]


def pack_files(root: Path, items: list[dict]) -> dict[str, str]:
    eligible = [i for i in items if i["status"] in EXPORTED]
    name, version = _identity(root)
    files = {}
    counts = {k: len(by_type(eligible, k)) for k in TYPES}
    self_md = ["# Self-memory pack", "",
               (f"Operational memory of the **{name}** AI, skillset version {version}, exported {today()}. It describes the "
               "AI and how it works, not any user. Load it progressively: this file, then the file for what you need, "
               "then `metadata/items.jsonl` for the structured record and provenance."), "",
               "## Answering the takeover questions", ""]
    for q, kinds in QUESTIONS:
        where = ", ".join(TYPES[k][1] for k in kinds)
        self_md.append(f"- {q} → {where} ({sum(counts[k] for k in kinds)} approved items)")
    self_md += ["", "## Rules that travel with it", "",
                "- Only approved items guide work; historical items are context; superseded items name their replacement.",
                "- A conversation is evidence, not memory. New self-knowledge goes through review before it is kept.",
                "- Nothing here is a profile of a person, and nothing about a person should be added.", ""]
    files["SELF.md"] = "\n".join(self_md)
    for kind, (_p, fname, heading, what) in TYPES.items():
        body = [f"# {heading}", "", what, ""]
        if kind == "skill":
            body += ["## Skills in this skillset", ""] + skill_rows(root) + [""]
        active = by_type(eligible, kind)
        if active:
            body += ["## Approved", ""] + [render_item(i) for i in active]
        older = by_type(eligible, kind, ("historical", "superseded"))
        if older:
            body += ["## Historical and superseded (context only)", ""] + [render_item(i) for i in older]
        if not active and not older and kind != "skill":
            body += ["Nothing recorded yet.", ""]
        files[fname] = "\n".join(body).rstrip("\n") + "\n"
    files["metadata/items.jsonl"] = "".join(json.dumps({k: i.get(k, _default(k)) for k in FIELDS}, ensure_ascii=False)
                                            + "\n" for i in sorted(eligible, key=lambda i: i["id"]))
    meta = {"format": PACK_FORMAT, "format_version": PACK_VERSION, "skillset": name, "skillset_version": version,
            "exported": today(), "counts": {s: sum(1 for i in eligible if i["status"] == s) for s in EXPORTED},
            "files": {n: hashlib.sha256(t.encode("utf-8")).hexdigest() for n, t in sorted(files.items())},
            "protection": "every item passed the user-protection screen at export"}
    files["metadata/pack.json"] = json.dumps(meta, indent=2) + "\n"
    return files


def _identity(root: Path) -> tuple[str, str]:
    try:
        ss = _skillset_module()
        return ss.top_info(root)
    except (OSError, ValueError, KeyError, RuntimeError, ImportError):
        return "skillset-os", "unknown"


def export(root: Path, out: Path, forbid: list[str] | None = None) -> Path:
    items = load(root)
    errors, _w = check(root, forbid)
    if errors:
        raise Refused("self-memory fails its checks, so nothing was exported: " + "; ".join(errors[:5]))
    files = pack_files(root, items)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".part")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, text in sorted(files.items()):
            info = zipfile.ZipInfo(f"{PACK_TOP}/{name}", (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, text.encode("utf-8"))
    tmp.replace(out)
    return out


def read_pack(pack: Path) -> tuple[dict, list[dict], dict[str, str]]:
    if not zipfile.is_zipfile(pack):
        raise Refused(f"{pack} is not a zip")
    with zipfile.ZipFile(pack) as zf:
        files = {n[len(PACK_TOP) + 1:]: zf.read(n).decode("utf-8") for n in zf.namelist()
                 if n.startswith(PACK_TOP + "/") and not n.endswith("/")}
    if "metadata/pack.json" not in files:
        raise Refused(f"{pack.name} is not a self-memory pack (no {PACK_TOP}/metadata/pack.json)")
    meta = json.loads(files["metadata/pack.json"])
    if meta.get("format") != PACK_FORMAT or meta.get("format_version") != PACK_VERSION:
        raise Refused(f"{pack.name} is a {meta.get('format')} v{meta.get('format_version')} pack; this reads "
                      f"{PACK_FORMAT} v{PACK_VERSION}")
    for name, digest in meta.get("files", {}).items():
        if name not in files or hashlib.sha256(files[name].encode("utf-8")).hexdigest() != digest:
            raise Refused(f"{pack.name}: {name} is missing or was changed after export")
    items = [json.loads(line) for line in files.get("metadata/items.jsonl", "").splitlines() if line.strip()]
    return meta, items, files


def import_pack(root: Path, pack: Path, as_candidates: bool = False, forbid: list[str] | None = None) -> tuple[int, int]:
    meta, incoming, _files = read_pack(pack)
    for i in incoming:
        bad = [m for sev, m in screen(item_text(i), forbid) if sev == "error"]
        if bad:
            raise Refused(f"{pack.name}: {i.get('id')} fails the user-protection screen ({'; '.join(bad)}); nothing imported")
    items = load(root)
    have = {i["id"]: i for i in items}
    origin = f"{meta.get('skillset')} {meta.get('skillset_version')} pack of {meta.get('exported')}"
    added = skipped = 0
    for i in incoming:
        same = have.get(i["id"])
        core = {k: i.get(k) for k in ("type", "summary", "detail", "status")}
        if same and {k: same.get(k) for k in core} == core:
            skipped += 1
            continue
        if same and not as_candidates:
            raise Refused(f"{i['id']} already exists here with different content; import with --as-candidates to "
                          "review the incoming items instead")
        new = {k: i.get(k, _default(k)) for k in FIELDS}
        new["imported_from"] = origin
        if as_candidates:
            new.update(id=new_id(items, new["type"]), status="candidate", supersedes=[], superseded_by="",
                       approved_by="")
        items.append(new)
        have[new["id"]] = new
        added += 1
    save(root, items)
    write_entry(root)
    return added, skipped


def acceptance(items: list[dict], forbid: list[str] | None = None) -> tuple[bool, list[str]]:
    """Can a fresh AI answer the takeover questions from ITEMS, without inheriting a dossier on a person?"""
    report, ok = [], True
    active = [i for i in items if i["status"] in ACTIVE]
    for q, kinds in QUESTIONS:
        answers = [i for i in active if i["type"] in kinds]
        if not answers:
            ok = False
            report.append(f"FAIL {q} nothing approved of type {' or '.join(kinds)}")
        else:
            report.append(f"ok   {q} {len(answers)} item(s), e.g. {answers[0]['id']}: {answers[0]['summary']}")
    exposed = [(i["id"], m) for i in items for sev, m in screen(item_text(i), forbid) if sev == "error"]
    user_facts = [i["id"] for i in active for sev, _m in screen(item_text(i)) if sev == "warning" and not i.get("review_note")]
    if exposed:
        ok = False
        report.append("FAIL no personal dossier: " + "; ".join(f"{iid} {m}" for iid, m in exposed[:5]))
    elif user_facts:
        ok = False
        report.append("FAIL no personal dossier: items read as facts about the user: " + ", ".join(sorted(set(user_facts))))
    else:
        report.append(f"ok   no personal dossier: {len(items)} item(s) screened")
    return ok, report


# ================================================================ command line

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=HERE.parent, help="skillset folder (default: the one above scripts/)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("--type", required=True, choices=list(TYPES))
    p.add_argument("--summary", required=True)
    p.add_argument("--detail", default="")
    p.add_argument("--source", default="", help="what experience produced it, described without personal details")
    p.add_argument("--evidence", action="append", default=[], help="a file, test or check that supports it")
    p.add_argument("--validated", default="", help="how it was validated, if it was")
    for name in ("review", "approve"):
        p = sub.add_parser(name)
        p.add_argument("id")
        p.add_argument("--forbid", action="append", default=[], help="a term that must not appear (never stored)")
        if name == "approve":
            p.add_argument("--reason", default="", help="why a screen warning is acceptable")
            p.add_argument("--person-confirmed", action="store_true")
    p = sub.add_parser("supersede")
    p.add_argument("old")
    p.add_argument("--by", required=True)
    p.add_argument("--person-confirmed", action="store_true")
    p = sub.add_parser("set-status")
    p.add_argument("id")
    p.add_argument("status", choices=["historical", "archived"])
    p.add_argument("--person-confirmed", action="store_true")
    p = sub.add_parser("list")
    p.add_argument("--type", choices=list(TYPES))
    p.add_argument("--status", choices=list(STATUSES))
    p.add_argument("--all", action="store_true")
    p = sub.add_parser("show")
    p.add_argument("id")
    p = sub.add_parser("search")
    p.add_argument("text", nargs="+")
    p.add_argument("--all", action="store_true")
    p = sub.add_parser("check")
    p.add_argument("--forbid", action="append", default=[])
    sub.add_parser("index")
    p = sub.add_parser("export")
    p.add_argument("--out", type=Path, default=Path("/mnt/user-data/outputs/memory-pack.zip"))
    p.add_argument("--forbid", action="append", default=[])
    p = sub.add_parser("import")
    p.add_argument("pack", type=Path)
    p.add_argument("--as-candidates", action="store_true")
    p.add_argument("--forbid", action="append", default=[])
    p = sub.add_parser("acceptance")
    p.add_argument("--pack", type=Path)
    p.add_argument("--forbid", action="append", default=[])
    args = ap.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.cmd == "add":
            i = add(root, args.type, args.summary, args.detail, args.source, args.evidence, args.validated)
            print(f"candidate {i['id']} ({i['type']}): {i['summary']}\nNEXT `memory.py review {i['id']}`, then approve it")
        elif args.cmd == "review":
            i = find(load(root), args.id)
            findings = screen(item_text(i), args.forbid)
            for sev, msg in findings:
                print(f"{sev.upper():7} {msg}")
            if i["type"] in NEEDS_PERSON:
                print(f"NOTE    a {i['type']} item needs the person's confirmation to approve")
            print(f"{args.id}: {'passes the screen' if not findings else 'see above'}")
            return 1 if any(s == "error" for s, _ in findings) else 0
        elif args.cmd == "approve":
            i = approve(root, args.id, args.reason, args.person_confirmed, args.forbid)
            print(f"approved {i['id']} ({i['approved_by']})")
        elif args.cmd == "supersede":
            supersede(root, args.old, args.by, args.person_confirmed)
            print(f"{args.old} is superseded by {args.by}")
        elif args.cmd == "set-status":
            set_status(root, args.id, args.status, args.person_confirmed)
            print(f"{args.id} is now {args.status}")
        elif args.cmd in ("list", "search"):
            items = load(root)
            show_all = args.all
            if args.cmd == "list":
                items = [i for i in items if (not args.type or i["type"] == args.type)
                         and (i["status"] == args.status if args.status else (show_all or i["status"] in ACTIVE))]
            else:
                words = [w.lower() for w in args.text]
                items = [i for i in items if (show_all or i["status"] in ACTIVE)
                         and all(w in item_text(i).lower() for w in words)]
            for i in items:
                print(f"{i['id']:9} {i['type']:11} {i['status']:10} {i['summary']}")
            print(f"{len(items)} item(s)")
        elif args.cmd == "show":
            print(render_item(find(load(root), args.id)))
        elif args.cmd == "check":
            errors, warnings = check(root, args.forbid)
            for e in errors:
                print(f"ERROR {e}")
            for w in warnings:
                print(f"WARN  {w}")
            print(f"self-memory: {len(load(root))} items, {len(errors)} errors, {len(warnings)} warnings")
            return 1 if errors else 0
        elif args.cmd == "index":
            write_entry(root)
            print(f"wrote {MEMORY_DIR}/{ENTRY}")
        elif args.cmd == "export":
            out = export(root, args.out, args.forbid)
            print(f"exported {out}")
        elif args.cmd == "import":
            added, skipped = import_pack(root, args.pack, args.as_candidates, args.forbid)
            print(f"imported {added} item(s), {skipped} already present")
        elif args.cmd == "acceptance":
            items = read_pack(args.pack)[1] if args.pack else load(root)
            ok, report = acceptance(items, args.forbid)
            print("\n".join(report))
            print("acceptance: " + ("passed" if ok else "FAILED"))
            return 0 if ok else 1
    except Refused as exc:
        print(f"REFUSED {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

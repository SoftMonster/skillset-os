"""Guards for the content structure, so routing stays light as the skillset grows."""

import re
from pathlib import Path

TOP = Path(__file__).resolve().parents[1]
GROUP_LIMIT = 600  # characters; group descriptions are repeated in every parent router table


def _description(path: Path) -> str:
    match = re.search(r'^description: "(.*)"$', path.read_text(encoding="utf-8"), re.MULTILINE)
    assert match, f"{path} has no description"
    return match.group(1)


def test_group_descriptions_stay_short():
    long = {
        str(p.relative_to(TOP)): len(_description(p))
        for p in (TOP / "subskills").rglob("SKILLSET.md")
        if len(_description(p)) > GROUP_LIMIT
    }
    assert not long, f"shorten these group descriptions to {GROUP_LIMIT} characters or fewer: {long}"


def test_top_router_explains_layering():
    assert "## Choosing between skillsets" in (TOP / "SKILL.md").read_text(encoding="utf-8")


# Top-level nested skillsets, read from disk so a new group is covered automatically.
GROUPS = tuple(sorted(p.parent.name for p in (TOP / "subskills").glob("*/SKILLSET.md")))
LOCATED = re.compile(r"`([a-z0-9-]+(?:/[a-z0-9-]+)*)` (?:in|from) (?:the )?`?((?:" + "|".join(GROUPS) + r")[a-z0-9/-]*)`?")
PATHREF = re.compile(r"`((?:" + "|".join(GROUPS) + r")/[a-z0-9/-]+)`")


def _member_paths() -> set[str]:
    return {
        p.parent.relative_to(TOP / "subskills").as_posix().replace("/subskills/", "/")
        for p in (TOP / "subskills").rglob("*.md")
        if p.name in ("SUBSKILL.md", "SKILLSET.md")
    }


def _broken_references(paths: set[str], text: str) -> list[str]:
    broken = []
    for name, group in LOCATED.findall(text):
        found = {r for r in paths if r == name or r.endswith("/" + name)}
        if not any(r.startswith(group + "/") or f"/{group}/" in f"/{r}" for r in found):
            broken.append(f"`{name}` in {group}")
    broken += [f"`{ref}`" for ref in PATHREF.findall(text) if not any(r == ref or r.endswith("/" + ref) for r in paths)]
    return broken


def test_cross_references_resolve():
    paths = _member_paths()
    broken = {
        str(p.relative_to(TOP)): refs
        for p in (TOP / "subskills").rglob("*.md")
        if p.name in ("SUBSKILL.md", "SKILLSET.md") and (refs := _broken_references(paths, p.read_text(encoding="utf-8")))
    }
    assert not broken, f"these references name a member that does not exist there: {broken}"


def test_reference_check_catches_faults():
    paths = _member_paths()
    seeded = "`negotiation` in cognition/reasoning, `made-up-skill` in self-improvement, `cognition/reasoning/nonexistent`"
    assert len(_broken_references(paths, seeded)) == 3
    assert _broken_references(paths, "`negotiation` in interpersonal and `cognition/reasoning/research`") == []


def test_no_editing_artefacts():
    """Leftovers from scripted edits: runs of blank lines, and escaped quotes in body text."""
    found = []
    for p in TOP.rglob("*.md"):
        if ".git" in p.parts or "templates" in p.parts:
            continue
        text = p.read_text(encoding="utf-8")
        body = text.split("\n---\n", 1)[-1]
        if "\n\n\n" in text:
            found.append(f"{p.relative_to(TOP)}: blank-line run")
        if '\\"' in body:
            found.append(f"{p.relative_to(TOP)}: escaped quote in body")
    assert not found, found


def test_top_router_applies_memetic_ethics_throughout():
    top = (TOP / "SKILL.md").read_text(encoding="utf-8")
    assert "## Applies to every member: memetic ethics" in top
    assert "Claude's built-in values and Anthropic's guidelines always come first" in top


MEME = re.compile(r"^🧬 \*\*Core meme:\*\* (.+)$", re.MULTILINE)


def test_every_skill_has_a_short_unique_core_meme():
    """Each sub-skill's essence in one line that survives being passed on without context (memetic ethics)."""
    seen, problems = {}, []
    for p in (TOP / "subskills").rglob("SUBSKILL.md"):
        body = p.read_text(encoding="utf-8").split("\n---\n", 1)[-1]
        head = "\n".join(body.strip().splitlines()[:4])      # title, blank line, core meme
        match = MEME.search(head)
        rel = str(p.relative_to(TOP))
        if not match:
            problems.append(f"{rel}: no core meme directly under the title")
            continue
        meme = match.group(1).strip()
        if len(meme) > 100:
            problems.append(f"{rel}: core meme is {len(meme)} characters; keep it under 100")
        if meme in seen:
            problems.append(f"{rel}: same core meme as {seen[meme]}")
        seen[meme] = rel
    assert not problems, problems

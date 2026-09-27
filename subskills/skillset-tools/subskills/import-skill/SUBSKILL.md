---
name: import-skill
description: "Brings existing skills into the skillset: a standalone skill, another skillset, a whole repository, or a collection of skills. Each can come from a folder, a zip or .skill file (zips inside zips included), an installed skill, or a GitHub repository that stays linked and can be refreshed. Use when the user asks to import, add, merge, consolidate, nest or link an existing skill, skillset, zip or repository, or to replace standalone skills with the skillset. Do not use for writing a skill from scratch; use the write-subskill sub-skill."
trigger: "import, nest or link an existing skill, skillset, zip or GitHub repository"
metadata:
  version: "1.0.0"
---

# Import a skill, skillset or repository

🧬 **Core meme:** Bring skills in unchanged, and only when that's what's wanted.

To learn from other people's skills rather than copy them, use `find-skills` in this group: it applies their lessons across the repository in the skillset's own words. This member is for bringing skills in unchanged: the person's own skills, or a verbatim copy they explicitly ask for.

Bring outside skills in without changing what they do, so the person can delete the standalone copies and rely on the skillset alone.

Work in the working copy from `sync-skillset`. `<wc>` below is that folder, usually `/home/claude/skillset-os`.

## Rules

- **Never import Anthropic built-in skills.** Every account already has them, and several licences forbid copying. They live under `/mnt/skills/public` and `/mnt/skills/examples`.
- **Check the licence.** The person's own skills are fine. Third-party skills keep their licence file; do not import one whose licence forbids copying. If a third-party skill has no licence, ask first.
- **Change as little as possible.** An import only adapts names, adds a trigger and removes the standalone version note. Improvements are a separate edit.
- **Pack repositories; unpack skills.** A repository, or any source with more than one `SKILL.md`, must be imported packed (`--packed`): it stays sealed and counts as one file. A single skill reads most easily unpacked.
- **One copy afterwards.** Once uploaded, standalone copies must be deleted or switched off, or they compete with the skillset.

## What the source can be

| Source | What `import` makes |
|---|---|
| A skill (one `SKILL.md` or `SUBSKILL.md` at its top) | a sub-skill, as a folder or `--packed` zip |
| A skillset (a `SKILLSET.md`, or a `SKILL.md` with `subskills/`, like this repository) | a nested skillset, as a folder or zip, members and inner zips included |
| A collection (no instructions at its top, several skill folders inside, like a repository of skills) | a new nested skillset holding each skill as a member; needs `--name`, `--description` and `--trigger` |
| Any of these as a zip or `.skill`, however deeply wrapped | the same; single wrapper folders such as GitHub's `repo-main/` are skipped |
| A GitHub repository | a linked member, pinned to a commit and refreshable (`add-source`) |

## Workflow

```
- [ ] 1. Working copy (sync-skillset, step 1)
- [ ] 2. Find the source and where it goes
- [ ] 3. Import or link
- [ ] 4. Tidy and test
- [ ] 5. Package (sync-skillset, steps 3 and 4)
```

### 2. Find the source and where it goes

- **Installed**: uploaded skills are usually in `/mnt/skills/user/<name>`, plugin skills in `/mnt/skills/plugins/<name>`; list them with `ls /mnt/skills/*/`.
- **Attached**: a zip or `.skill` file in `/mnt/user-data/uploads/`.
- **GitHub**: `owner/name`, plus a branch or tag and, for a skill inside a bigger repository, the folder path.

Decide the destination with `python3 <wc>/scripts/skillset.py tree`: the top (default), or a nested skillset via `--into <path>`. Put related members together; if the top description is filling up, create a group first with `organise-skillsets`.

### 3. Import or link

```bash
# Skill, skillset, repository or collection, from a folder, zip or .skill
python3 <wc>/scripts/skillset.py import <path> [--into <set>] [--name <name>] [--trigger "<phrase>"] [--packed] [--replace]

# A collection needs its group described
python3 <wc>/scripts/skillset.py import <repo.zip> --name <group> --description "<what the group covers. Use when ...>" --trigger "<phrase>" [--packed]

# A linked GitHub repository (packed by default; --folder to unpack)
python3 <wc>/scripts/skillset.py add-source <path/name> --repo <owner/name> [--ref main] [--path <folder>] [--trigger "<phrase>"]
```

The trigger is derived from the source's "Use when ..." wording when it has one; pass `--trigger` when it cannot be, or when the result reads badly. It should be a short verb phrase in the person's words, because it becomes part of the parent's description. `--replace` updates an earlier import, but only with a version at least as new. Linked members are refreshed with `skillset.py refresh`, which re-downloads only when the commit changed.

### 4. Tidy and test

- For an unpacked import, text that still calls the skill's own file `SKILL.md` should now say `SUBSKILL.md` (or `SKILLSET.md`).
- If a sibling now overlaps, add "Do not use for ...; use the X sub-skill" clauses so the router can tell them apart.
- Run `python3 <wc>/scripts/skillset.py check` and `tree`, then open one imported member with `skillset.py open <path>` and walk through a realistic prompt.

Package with `--bump minor`. In the hand-over, list each standalone skill the person should delete or switch off after uploading.

## Gotchas

- Private GitHub repositories cannot be fetched. Ask the person to download the zip (Code → Download ZIP) and `import` it with `--packed`; it will not be linked.
- Scripts inside an imported skill that use a fixed path to their own folder, such as `/mnt/skills/user/<name>/`, break once the skill moves. Point them at the path `skillset.py open` prints, or keep the member packed and note it.
- A packed repository keeps its own `skillsets.json`, so members linked inside it stay linked and are shown by `tree`.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/import-skill` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/import-skill` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

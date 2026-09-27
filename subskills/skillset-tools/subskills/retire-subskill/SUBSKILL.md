---
name: retire-subskill
description: "Removes a member (a sub-skill, nested skillset or zip) from the skillset cleanly. It checks that nothing else depends on it, deletes it, and records a one-line restore command in the changelog, leaving the skillset ready to package. Use when the user asks to retire, remove, delete, drop, deprecate or get rid of a skill or sub-skill, says one is obsolete, unused or replaced by another, or wants a retired one back. Do not use to make a sub-skill do or trigger less; use the edit-subskill sub-skill for that."
trigger: "retire, remove or delete a skill, or bring a retired one back"
metadata:
  version: "1.1.0"
---

# Retire a sub-skill

🧬 **Core meme:** Check dependents first, remove cleanly, and leave a way back.

Take a member out of the skillset without breaking anything that relied on it, and leave a one-line way to bring it back.

Work in the working copy from `sync-skillset`. `<wc>` below is that folder, usually `/home/claude/skillset-os`.

## Rules

- **Always dry-run first.** It shows the version, the dependents and other mentions without changing anything.
- **Dependents come first.** If another sub-skill, a script, a test or the router prose mentions it, update that first (and bump that sub-skill). Otherwise the skillset points at something that no longer exists.
- **`sync-skillset` stays.** The skillset cannot be packaged or synced without it; `retire` refuses it.
- **Git history is the archive.** Nothing is kept in the upload, so retiring also frees room under the 200-file and 1024-character limits. A linked GitHub member's record is removed too.
- **Wanting less, not none, is an edit.** If the person wants it to trigger or do less, use `edit-subskill`.

## Workflow

```
- [ ] 1. Working copy (sync-skillset, step 1)
- [ ] 2. Dry run
- [ ] 3. Settle dependents and replacement
- [ ] 4. Retire
- [ ] 5. Package (sync-skillset, steps 3 and 4)
```

### 2. Dry run

```bash
python3 <wc>/scripts/skillset.py retire <path> --dry-run
```

`DEPENDENT` lines (other sub-skills, scripts, tests, router prose) block retirement; `MENTION` lines (README, docs) are for information. Members are addressed by path (`writing/blog-post`); find a loosely named one with `skillset.py tree`, and ask only if two fit. Retiring a nested skillset or a zip removes everything inside it, so list its members to the person first.

### 3. Settle dependents and replacement

- **Another sub-skill mentions it**: edit that mention away or point it at the replacement, then `skillset.py bump <other> --part patch --message "..."`.
- **A test or script uses it**: update or remove that code.
- **Harmless** (an example name in prose): pass `--allow-mentions`.

Fix README or docs lines that would now mislead. If another sub-skill takes over, make sure its trigger and description cover the retired one's situations.

### 4. Retire

```bash
python3 <wc>/scripts/skillset.py retire <path> [--replaced-by <other>] [--reason "<why>"]
```

It deletes the folder, records the last version and a restore command in the changelog, and updates the router. Then package with `--bump major`: removing a capability is a major change. In the hand-over, say what was retired, what replaces it, and which dependents changed.

## Bringing a retired sub-skill back

In the working copy (or the person's GitHub clone), run the restore command from the changelog line. `<member-folder>` is the member's location, such as `subskills/writing/subskills/blog-post` or `subskills/tools.zip`:

```bash
git checkout $(git rev-list -n 1 HEAD -- <member-folder>)^ -- <member-folder>
```

A working copy pulled from an upload has no history before the pull, so this usually runs in the person's GitHub clone. Ask them to attach the restored folder as a zip, or the whole GitHub zip, and pull from that. Then `skillset.py bump <path> --part minor --message "restored"` and package.

## Gotchas

- If `pytest` fails during packaging after a retirement, a test still exercises the sub-skill; it was a dependent, so update it in the same change.
- Retiring a sub-skill does not touch standalone copies of the same skill the person may still have installed; mention any `pull` reported.

## Commands

- 🌅 **Check dependents, remove cleanly, leave a way back** · `retire subskill`: Retires, removes or deletes a skill after a dry run and settling dependents, and can bring a retired one back.
  - 🧪 `dry run retire`: Lists what depends on the member before anything is removed.
  - ♻️ `restore subskill`: Brings a retired sub-skill back from history.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/retire-subskill` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/retire-subskill` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

---
name: edit-subskill
description: "Changes an existing sub-skill, a nested skillset's router text, or the skillset's own tooling. It makes the smallest edit that does what was asked, and renames the sub-skill when needed. It bumps the sub-skill's version, re-tests both the changed and unchanged behaviour, and leaves the skillset ready to package. Use when the user asks to edit, fix, improve, update, extend, tweak, rename, shorten or rewrite a skill or sub-skill, says one did the wrong thing or was not used when it should have been, or wants the skillset itself to work differently."
trigger: "edit, fix, improve or rename a skill, or fix one that did the wrong thing or was not used"
metadata:
  version: "1.1.0"
---

# Edit a sub-skill

🧬 **Core meme:** Make the smallest edit that does the job, then bump and re-test.

Change a sub-skill so it does what the person now wants, and nothing else changes by accident.

Work in the working copy from `sync-skillset`. `<wc>` below is that folder, usually `/home/claude/skillset-os`.

## Rules

- **Make the smallest edit that does the job.** Keep the author's structure and wording outside the part being changed.
- **Never lose routing.** When changing a trigger or description, keep every situation it already covered unless the person wants it gone.
- **Bump every changed sub-skill**: `patch` for fixes and wording, `minor` for new behaviour or new triggers, `major` for renames or changed outputs that other things depend on. `package` refuses changed sub-skills that were not bumped.
- **Respect other people's work.** For a sub-skill with its own licence file (usually imported), add rather than delete, and record each change in a `CHANGES.md` beside it, noting that the original licence still applies.
- **Edit sources, not generated text.** The top description and every router table come from each member's `trigger` and `description`, and the dotfiles from `scripts/templates/`. Change those, then `skillset.py index`.

## Workflow

```
- [ ] 1. Working copy (sync-skillset, step 1)
- [ ] 2. Find the sub-skill
- [ ] 3. Understand the change
- [ ] 4. Edit
- [ ] 5. Review the diff
- [ ] 6. Bump and test
- [ ] 7. Package (sync-skillset, steps 3 and 4)
```

### 2. Find the sub-skill

Run `python3 <wc>/scripts/skillset.py tree` and match the person's words against it; members are addressed by path, such as `writing/blog-post`. Ask only if two fit. A packed member (zip) must be unpacked before editing (`organise-skillsets`); a linked GitHub member should be changed upstream and refreshed, because unpacking detaches it. If they mean a standalone skill that is not in the skillset, bring it in with `import-skill` first. For a built-in Anthropic skill, explain that it cannot be edited; offer a new sub-skill with `write-subskill` instead.

### 3. Understand the change

Read the whole `SUBSKILL.md` and every file the change touches. Write down, in a sentence or two, what will change and what must stay the same. For "it did the wrong thing" or "it wasn't used", find the cause first: a missing trigger phrase, a description that loses to a sibling, an ambiguous step, a missing default, or a script bug. [recipes.md](recipes.md) covers the usual changes and which bump each needs; read it for anything beyond a one-line fix.

### 4. Edit

When the change applies a lesson found by `find-skills`, write it in the member's own voice and structure (never pasted from the source), and add the member and version to that lesson's entry in `docs/LEARNED-FROM.md`.

Make targeted replacements rather than rewriting whole files, with the replace command:

```bash
python3 <wc>/scripts/skillset.py replace <path> --old "<exact passage>" --new "<replacement>" [--part patch|minor|major --message "<why>"]
```

It finds the member's file from its path (nested paths included), refuses unless the passage occurs exactly once, and bumps only after the edit is written. Use `--old-file` and `--new-file` for multi-line passages. Prefer it to hand-built paths in ad-hoc scripts: guessing a nested path wrong, then bumping anyway, is the failure it prevents. After any scripted or batch edit, sweep the changed files for artefacts, since the tests fail on runs of three or more blank lines and on escaped quotes in body text; heredocs and appended templates are the usual source.

To rename:

```bash
python3 <wc>/scripts/skillset.py rename <old> <new>
```

It moves the folder, updates the sub-skill's own files, `NOTICE.md` and the changelog, bumps the major version and lists every remaining mention. Fix each one.

Changes to the skillset itself (the top `SKILL.md` prose, `scripts/skillset.py`, templates) and to nested skillsets' own text need no bump; `package` raises the top version and every changed nested skillset.

### 5. Review the diff

```bash
git -C <wc> add -N . && git -C <wc> diff --stat synced && git -C <wc> diff synced
```

Every hunk should trace back to the change you wrote down. Revert anything else.

### 6. Bump and test

Once `check` and the tests pass, and the edit enhances what a skill can do, offer the optional exam-to-memory loop ("The enhancement loop" in `cognition/metacognition/universal-skill-curriculum-exam`): take the exam, self-mark it (the person can pre-authorise this), then form and harvest memories.

```bash
python3 <wc>/scripts/skillset.py bump <name> --part patch|minor|major --message "<what changed>"
python3 <wc>/scripts/skillset.py check
```

Then test what changed and what should not have:

- **Changed behaviour**: walk through the prompt that exposed the problem using only what the sub-skill now says. After changing any trigger or description, check `tests/routing.json` still reflects the intended routes, and run a blind grade with `scripts/routing_eval.py` when the change is large. For a routing fix, route the prompt by hand from the top description through each router table.
- **Unchanged behaviour**: walk through one ordinary prompt it already handled well.
- **Scripts**: run each changed script on a realistic input; add or update a test in `<wc>/tests/` when the fix is worth protecting.

Report only tests that actually ran.

## Gotchas

- The installed skillset under `/mnt/skills` is read-only; editing there fails. Always use the working copy.
- Shortening a trigger or description is the most common way to lose routing; compare old and new side by side.
- A rename is major because anything that names the sub-skill breaks, including the person's habits.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/edit-subskill` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/edit-subskill` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

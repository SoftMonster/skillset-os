---
name: write-subskill
description: "Writes a new sub-skill for the skillset. It captures what the sub-skill should do, picks a clear name, and writes a trigger and description that route requests to it reliably. Then it writes a lean SUBSKILL.md with any scripts or reference files and tests it against realistic prompts. Use when the user asks to create, write, draft, build or add a new skill or sub-skill, or to turn a workflow or this conversation into one."
trigger: "write, add or draft a new skill, or turn a workflow or this chat into one"
metadata:
  version: "1.1.0"
---

# Write a sub-skill

🧬 **Core meme:** A clear trigger to be chosen, a lean body to be followed, tests to prove it.

Write a sub-skill that the skillset routes to at the right moments and that Claude follows reliably.

Work in the working copy from `sync-skillset`. `<wc>` below is that folder, usually `/home/claude/skillset-os`.

## How routing works here

The whole skillset is one skill, so Claude sees one description for all of it. That description is built from the **trigger** of each top-level member, a short phrase. When the skillset is chosen, Claude follows the router tables, top first and then any nested skillset's, using each member's **description**, until it opens the matching `SUBSKILL.md`. A sub-skill inside a nested skillset is reached through its group's trigger, so its own trigger feeds its group's table, not the top description. So:

- The **trigger** gets the skillset (or its group) chosen. Keep it short (under 160 characters, ideally under 80), in the words people use, starting with a verb: "write meeting minutes from rough notes".
- The **description** picks this sub-skill over its siblings: what it produces, then "Use when ...", and "Do not use for ..." when a sibling is close.

## Workflow

```
- [ ] 1. Working copy (sync-skillset, step 1)
- [ ] 2. Capture what it must do
- [ ] 3. Name and create
- [ ] 4. Write trigger and description
- [ ] 5. Write the body and files
- [ ] 6. Test
- [ ] 7. Package (sync-skillset, steps 3 and 4)
```

### 2. Capture what it must do

When the new sub-skill comes from lessons found by `find-skills`, write it from those lessons in the skillset's own words, and credit the sources in `docs/LEARNED-FROM.md`.

Mine the conversation first: for "turn this into a skill", the steps taken, the person's corrections, the approved formats and the tools used are the material. Pin down the task and output, when it should and should not be used, fixed conventions, and what needs a script. Ask at most one round of questions, only about what you cannot infer; state other assumptions in the hand-over.

### 3. Name and create

```bash
python3 <wc>/scripts/skillset.py new <name> --description "<description>" --trigger "<trigger>"
```

Choose a name that says what it does (`meeting-minutes`, not `helper`): lowercase, digits and hyphens. The path puts it at the top (`meeting-minutes`) or inside a nested skillset (`writing/meeting-minutes`); pick the group whose other members are most like it, as shown by `skillset.py tree`. It creates the member's `SUBSKILL.md` from the template, adds a changelog line and updates the routers. A packed group must be unpacked first (`organise-skillsets`).

### 4. Write trigger and description

Follow [writing-guide.md](writing-guide.md). Lean towards being chosen: a sub-skill that never triggers helps nobody. Check the trigger against three prompts that should reach it and three near-misses that should not, reading it next to its siblings in the parent's router table.

### 5. Write the body and files

Read [writing-guide.md](writing-guide.md) before writing the body. In short: open with the goal, then give an ordered workflow (with a checklist when there are more than three steps). Give one default instead of a menu, and a reason for each rule. Show a concrete example, and collect traps under Gotchas. Leave out anything Claude already knows.

Put scripts, references and templates in the sub-skill's own folder and link them relatively from `SUBSKILL.md`. Never name a file `SKILL.md` inside the skillset; `check` rejects it. Replace every placeholder the template left; `check` lists any that remain.

### 6. Test

Run `python3 <wc>/scripts/skillset.py check`, fix every error, then follow [testing.md](testing.md). For a script worth protecting, add a test to `<wc>/tests/`.

Then offer the optional exam-to-memory loop ("The enhancement loop" in `cognition/metacognition/universal-skill-curriculum-exam`): take the exam with the new member in scope, self-mark it (pre-authorisation allowed), then form and harvest memories.

## Gotchas

- Every top-level member's trigger lengthens the top description, which has a 1024-character limit. `index` prints how much is used. If it runs short, put the new sub-skill inside a nested skillset, or group existing members with `organise-skillsets`, rather than dropping triggers.
- A new sub-skill is new behaviour, so package with `--bump minor`.
- The sandbox network only reaches package registries and GitHub; a script calling other sites fails here. Say so in the sub-skill.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/write-subskill` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/write-subskill` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

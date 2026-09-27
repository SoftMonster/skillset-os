---
name: self-memory
description: "Keeps the AI's own persistent self-memory for Skillset-OS: turns a conversation's evidence into reviewed lessons, successes, failures, experiments, limitations and other self-knowledge, screens every item against the user-protection boundary, and exports or imports memory-pack.zip so another AI can carry on. Use when asked what Claude can do, what worked, what failed or what it has learned, to remember a lesson about its own work, to review or tidy its memory, to harvest lessons from memory into skill improvements, or to export, import or hand over its memory. Do not use for remembering facts about the person; those stay temporary task context."
trigger: "remember, recall, review, export or import what Claude has learned about itself"
command: "keep self-memory"
metadata:
  version: "1.2.0"
---

# Self-memory

🧬 **Core meme:** Remember what makes the AI better, never a dossier on the person.

Keep Skillset-OS's memory of itself: what it can do, what worked, what failed, what it learned, what it tried, how it changed, where it is weak and what needs maintenance. The memory exists to improve the AI and to let another AI carry on without the one that wrote it. It is never an archive about the user.

The store is `<top>/memory/items.jsonl`. The entry point is `<top>/memory/SELF.md`, generated from the store: read that first. The tool is `python3 <top>/scripts/memory.py` (`--help` lists its commands). Changes to the store happen in the working copy from `sync-skillset`, and are packaged like any other change.

## The boundary

Never store any of these, even as a candidate:

- secrets, passwords, keys or credentials;
- identifying or sensitive personal information;
- conversation kept only because it happened;
- a profile of the user, or inferences about their personality, beliefs, preferences or behaviour;
- user-specific facts that don't improve the AI's own operation.

**Tell a fact about the user from a lesson about the AI.** The first stays temporary task context; only the second can become memory. Conversation evidence: an incomplete multi-part repository was treated as complete. Wrong: "The user owns that repository and had that problem." Right: "When auditing multi-part repositories, verify completeness before assessing implementation."

## From conversation to memory

```
- [ ] 1. Conversation: treat it as evidence, not memory
- [ ] 2. Reflect: what did this show about the AI's own performance?
- [ ] 3. Extract: write each candidate as a general statement about the AI
- [ ] 4. Classify: pick its type
- [ ] 5. Screen and review
- [ ] 6. Approve
- [ ] 7. Index (automatic)
- [ ] 8. Export, when handing over
- [ ] 9. Import, when inheriting
```

**3–4. Extract and classify.** One item per lesson, with a summary of at most 160 characters. Types:

- `capability`: what the AI can do;
- `skill`: a reusable skill it has acquired or validated;
- `lesson`: a reusable lesson;
- `success`: a validated approach and when it works;
- `failure`: an approach that failed, and why;
- `experiment`: hypothesis, method and result;
- `evolution`: a change in capability or architecture;
- `limitation`: a known weakness, uncertainty or failure mode;
- `maintenance`: self-maintenance that is needed;
- `decision`: an authoritative decision about the system.

```bash
python3 <wc>/scripts/memory.py add --type lesson --summary "<general statement about the AI>" \
  --source "<what kind of experience produced it, without personal details>" --evidence "<file or test>"
```

The tool refuses to store anything that contains a secret or personal identifier.

**5. Screen and review.** Run `memory.py review <id>`, adding `--forbid "<name or handle>"` for any identifier known from the conversation. Forbidden terms are checked, never stored. Then read the item's meaning yourself, because the screen is pattern-based. A warning means the item reads as a fact about a person: rewrite it rather than overriding it.

**6. Approve.** Run `memory.py approve <id>`. The screen must pass. You may approve lessons, successes, failures, experiments, limitations, maintenance and skills yourself. **Capability, evolution and decision items change what the AI is: ask the person, then pass `--person-confirmed`.**

## Harvesting memory into skills

Memory records a lesson; a skill changes behaviour. A lesson that stays only in memory can repeat, because notes are read less reliably than instructions. Harvesting moves proven self-knowledge into the skills that should carry it.

1. **List** the approved and candidate lessons, failures and limitations: `memory.py list --type lesson` (and `--type failure`, `--type limitation`, `--status candidate --all`).
2. **Map** each to the one skill that owns that faculty (`skillset.py tree`), and read that skill first. Often part of the lesson is already there; add only the missing piece, and point to the home skill rather than copying it into others.
3. **Leave out** items that are not guidance: run records, maintenance notes, code decisions and superseded drafts stay as memory.
4. **Edit** with `edit-subskill` in `skillset-tools`, bump each changed member, and run `check` and the tests. If a skill grows past its length budget, trim rather than stack.
5. **Ask the person** to approve the changes before packaging (`ethical-skill-evolution` in safety-governance).

**Fed by the exam.** The enhancement loop ("The enhancement loop" in `cognition/metacognition/universal-skill-curriculum-exam`: exam, self-mark with pre-authorisation allowed, form memories, harvest) is the main source of evidence-backed items; harvest its results before packaging.

**Offer it often.** Whenever a conversation produces new lessons, failures or limitations, or lessons sit in memory that no skill yet reflects, include "Harvest memory into skills" among the closing suggestions.

## Status and authority

Only **approved** items guide work. **Historical** items are context. **Superseded** items name their replacement. **Archived** items are left out, and **candidates** are unreviewed. Recency never decides: an old approved lesson outranks a newer candidate.

Approved content is never edited in place. To correct it, add and approve the new item, then run `memory.py supersede <old> --by <new> --person-confirmed`. Retiring approved knowledge (`set-status <id> historical|archived`) also needs the person.

## Recall

Load progressively:

1. `memory/SELF.md`;
2. `memory.py list --type <type>` or `memory.py search <words>`;
3. `memory.py show <id>` for the full item and its provenance;
4. only then, the evidence it cites.

Answer "what can you do / what worked / what did you learn" from approved items, and say which ones.

## Handing over and taking over

- **Export:** `memory.py export --out /mnt/user-data/outputs/memory-pack.zip`. `sync-skillset` also writes it with every package. It carries the approved, historical and superseded items, but never candidates or archived ones. Its files are `SELF.md`, one file per type, `SKILLS.md` generated from the skillset's members, and `metadata/` with checksums and the structured record.
- **Import:** `memory.py import <pack>` verifies the checksums and screens every item. Use `--as-candidates` to review incoming items rather than trusting them.
- **Takeover:**
  1. Read the top `SKILL.md` and `memory/SELF.md`.
  2. Discover skills with `skillset.py tree`.
  3. Read the lessons, successes and failures relevant to the work, and the limitations and open maintenance items.
  4. Continue the work, recording only genuinely new self-knowledge.
- **Acceptance:** `memory.py acceptance [--pack <pack>] [--forbid <term>]` checks that the takeover questions can be answered (capabilities, skills, what worked, what failed, lessons, experiments, limitations, evolution, maintenance cautions) and that no personal dossier comes along.

## Gotchas

- `skillset.py check` includes `memory.py check`: schema, statuses, supersession links, the screen, and whether `SELF.md` is current. `skillset.py index` regenerates `SELF.md`.
- Don't record every observation. An item earns its place when it would change how the AI works next time.
- The screen can't know every name. Always pass the identifiers you know with `--forbid` when reviewing, exporting or running acceptance after a conversation that mentioned them. Its known blind spot is a bare proper name beside a preference verb ("<Name> prefers ..."): with no role word such as "user" or "customer", nothing flags it.
- If you change the screen's rules, test them on text you did not write while tuning. A rule that scored no false positives on its own examples flagged 86% of 735 sentences built from unrelated skill names.

## Commands

- 🧠 **Remember what improves the AI, never the person** · `keep self-memory`: Remembers, recalls, reviews, exports or imports what Claude has learned about itself, through candidate, screen, approve and index.
  - 📝 `add memory candidate`: Proposes a lesson, success, failure or other item about the AI as a candidate for review.
  - ✅ `review memory candidates`: Screens candidates against the user-protection boundary and approves, edits or rejects each.
  - 📤 `export memory pack`: Writes memory-pack.zip so another AI can take over.
  - 📥 `import memory pack`: Compares a memory pack with the store and imports only genuinely new items as candidates.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/self-memory` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/self-memory` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

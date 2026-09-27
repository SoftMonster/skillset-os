# Self-memory

🧬 **Core meme:** Remember what makes the AI better, never a dossier on the person.

This is the AI's own persistent memory for Skillset-OS: its capabilities, skills, lessons, successes, failures, experiments, evolution, limitations, maintenance and decisions. It exists to improve the AI, not to accumulate knowledge about the user. Generated from `items.jsonl` by `index`; do not edit by hand.

## Load it progressively

1. Read this file: the rules and a one-line index of everything approved.
2. Find what the task needs: `python3 <top>/scripts/memory.py list --type lesson` or `memory.py search <words>`.
3. Read the items you need in full: `memory.py show <id>`.
4. Only then open the evidence an item cites, if you must check it.

## Taking over

A new AI continues from here without the one that wrote it: understand the system (the top `SKILL.md`), discover capabilities and skills (below, and `skillset.py tree`), read the lessons, successes and failures relevant to the work, note the limitations and open maintenance items, continue, and record genuinely new self-knowledge through the pipeline below. `memory.py acceptance` checks that the takeover questions can be answered from this memory.

## Rules

- **A conversation is evidence, not memory.** Reflect, extract candidates, classify, screen, approve, index; then it can be exported and imported. The `self-memory` member of `skillset-tools` walks through it.
- **The user-protection boundary:** no secrets or credentials, no identifying or sensitive personal information, no conversation kept because it happened, no profile of the user and no inferences about them. A fact about the user stays temporary task context; only a lesson about the AI qualifies.
- **Status decides authority, not recency.** Only approved items guide work. Historical items give context, superseded items point to their replacement, archived items are left out.
- **No silent rewrites.** Approved content is never edited; a correction is a new item that supersedes the old one. Capability, evolution and decision items, supersession and retirement need the person's confirmation.

## Index

### Capabilities (9)

What the AI can do.

- `CAP-0001` Route a request through nested skillsets to the one member that fits it.
- `CAP-0002` Maintain its own skillset: write, edit, move, pack, import, retire and version members.
- `CAP-0004` List, discuss and audit any folder of itself with the contents and review commands.
- `CAP-0005` Learn from outside skills without copying them, and credit the source.
- `CAP-0006` Adopt an outside project as a develop member with its own checker and release workflow.
- `CAP-0007` Keep a portable self-memory that another AI can inherit through memory-pack.zip.
- `CAP-0009` Package itself as one upload at any size, zipping large groups inside it and unzipping them with Python to read.
- `CAP-0010` Examine its own skills against the Universal Skill Curriculum Exam in a timed, evidence-only, 30-minute run.
- `CAP-0011` Work as a command line over its own skills (bash, PowerShell, cmd) and resolve verb-noun commands to skills or tools.

### Skills (3)

Reusable capabilities and skill definitions, with their status.

- `SKL-0001` The skillset's members are its skills; SKILLS.md in a memory pack lists every one with its version.
- `SKL-0002` Self-memory keeping is a skill of its own: the self-memory member of skillset-tools.
- `SKL-0003` universal-skill-curriculum-exam: timed self-examination with a coverage ledger and a marking gate.

### Lessons (25)

Reusable lessons learned from experience.

- `LES-0001` When auditing multi-part repositories, verify completeness before assessing implementation.
- `LES-0002` Moving or renaming a member changes which requests reach it; re-check routing after any move.
- `LES-0003` Write triggers in everyday words; jargon routes worse.
- `LES-0004` Walk the routing fixture and scan for overlap to find missing hand-offs and cross-references.
- `LES-0005` Only blind grading counts as a routing score; self-grading overstates accuracy.
- `LES-0006` Give every skill a core meme: one line under 100 characters that keeps its meaning alone.
- `LES-0007` Make targeted edits with `skillset.py replace`, then sweep for artefacts after batch edits.
- `LES-0008` Give every checker a self-test that proves it can fail.
- `LES-0009` Keep one home per topic; fold overlapping members together instead of keeping near-duplicates.
- `LES-0010` Tests must not depend on the skillset's size.
- `LES-0011` Run the full test suite in parts when it exceeds one tool call; skip tests in package only after all pass.
- `LES-0012` Confirm the design once when a request keeps changing direction, before changing core packaging.
- `LES-0013` Removing something completely means scrubbing triggers, router text, tests, routing cases and history too.
- `LES-0014` Keep source modular even when a project ships as one file; mark file boundaries so it splits back exactly.
- `LES-0015` Build a runner when the sandbox cannot run a project; static checks alone miss behaviour bugs.
- `LES-0016` Treat a conversation as evidence, not memory: keep lessons about the AI, never facts about a person.
- `LES-0017` Pack in the upload, never in the repository: zips inside the upload keep one upload and a browsable repository.
- `LES-0018` Replace <x> placeholders in imported skill descriptions first; descriptions cannot hold angle brackets.
- `LES-0019` Pack an imported collection as one group zip; per-member zips can push the upload past 190 files.
- `LES-0020` Test shared verbs both ways after wiring new commands; show changes had silently resolved to save changes.
- `LES-0021` Merge many tiny sibling skills into one sub-skill with a section each; it cuts files enough to avoid zipping groups.
- `LES-0022` New hidden repo files must become scripts/templates entries in DOTFILES, or uploads drop them.
- `LES-0023` Derive a variant edition by exact-match patches that refuse on drift, never by forking the tree.
- `LES-0024` Before publishing, scan reference files for verbatim third-party text; keep names, drop copied descriptions.
- `LES-0025` Always quote heredocs (<<'EOF') when a script inserts Markdown; unquoted ones run backticks as commands.

### Successes (5)

Approaches that demonstrably worked, and when.

- `SUC-0001` Splitting large uploads into per-folder part skills kept every path and stayed under the file limit.
- `SUC-0002` A release gate that unpacks and merges the written zips catches a lost file before delivery.
- `SUC-0003` Learning from outside skills instead of importing them kept one voice and no foreign instructions.
- `SUC-0004` Grouping management members into a nested skillset roughly halved the top description.
- `SUC-0005` Mutation-testing new checks (breaking the feature on purpose) confirmed each test can fail.

### Failures (5)

Approaches that failed, and why.

- `FAI-0001` Packing a large member into a zip to beat the file limit hid its files on GitHub and slowed every change.
- `FAI-0002` Merging source files to cut the file count traded away modularity and was reverted.
- `FAI-0003` Judging a split upload from its main part alone made a complete skillset look broken.
- `FAI-0004` A generated section added to every member first demanded a version bump for each one.
- `FAI-0005` A first release would have shipped as 1.0.1 because package bumped before any release existed.

### Experiments (3)

Hypotheses tested, methods and results.

- `EXP-0001` Nested splitting: with the threshold lowered, an oversized group split one level further and merged back exactly.
- `EXP-0002` Installing all parts side by side and pulling rebuilt all files identically.
- `EXP-0003` A routing walkthrough over realistic prompts, including near-misses, exposed two missing hand-offs.

### Evolution (5)

Changes in capability or architecture.

- `EVO-0001` From a collection of standalone skills to one skill with nested skillsets and one tool.
- `EVO-0002` Uploads over 150 files became per-folder part skills with a parts manifest and a release gate.
- `EVO-0003` Change logs gave way to self-memory: lessons kept as knowledge, with provenance, instead of dated history.
- `EVO-0004` Every folder member gained a generated This folder section, so each can list and audit itself.
- `EVO-0005` Over-limit uploads moved from separate part skills to groups zipped inside one upload.

### Limitations (9)

Known weaknesses, uncertainty and failure modes.

- `LIM-0001` Cannot upload to claude.ai or push to GitHub; the person does both from the delivered files.
- `LIM-0003` One tool call is limited to about 300 seconds, so long test runs must be split.
- `LIM-0004` The sandbox reaches only package registries and GitHub; other sites fail from scripts.
- `LIM-0005` Uploads can drop executable bits and dotfiles; pull restores bits and templates avoid dotfiles.
- `LIM-0006` Routing quality is only as good as the fixture; unmeasured prompts may still misroute.
- `LIM-0007` The user-protection screen is pattern-based: it catches common identifiers, not every personal fact.
- `LIM-0008` claude.ai rejects skill uploads of more than about 200 files; a zip inside the upload counts as one file.
- `LIM-0009` Members zipped inside an upload can only be read with code execution on.
- `LIM-0010` The command line cannot run programs or open screen editors; edits must be described, then remembered.

### Maintenance (6)

Self-maintenance that is required or recommended.

- `MNT-0001` Keep headroom in the 1024-character top description; index prints how much is used.
- `MNT-0002` Re-check the routing fixture after any trigger, description or move.
- `MNT-0003` Add a routing confusion matrix to show which members get mistaken for each other.
- `MNT-0004` Design skill composition (building a chain of skills for one request) as a separate piece of work.
- `MNT-0005` After each change, record new self-knowledge through the memory pipeline, and supersede what it replaces.
- `MNT-0006` Rerun the curriculum exam after significant changes, and record each marked run as an experiment to track the trend.

### Decisions (19)

Authoritative decisions about the AI system itself.

- `DEC-0002` The name is skillset-os, shown as Skillset-OS.
- `DEC-0003` Only the top file is SKILL.md outside zips; members use SUBSKILL.md and SKILLSET.md.
- `DEC-0004` Zips are sealed and reproducible.
- `DEC-0005` Linked repositories are pinned to a commit without the rate-limited GitHub API.
- `DEC-0006` skillsets.json travels with members through pack, unpack, move and rename.
- `DEC-0007` Routers and the top description are generated from triggers and descriptions.
- `DEC-0008` Every change raises a version, except the first release of a never-released skillset.
- `DEC-0009` Built-in Anthropic skills are never imported, and names containing claude or anthropic are refused.
- `DEC-0010` sync-skillset is core: kept at the top, unpacked, and never retired, moved or packed.
- `DEC-0011` Learn from outside skills; do not copy them in.
- `DEC-0012` Layered content with light routers: practical skillsets over cognition, group descriptions capped at 600 characters.
- `DEC-0013` Routing is measured with a fixture and graded blind.
- `DEC-0014` Memetic ethics applies throughout, under Claude's built-in values and Anthropic's guidelines.
- `DEC-0015` Local builds come from git's view, so gitignored secrets never reach an upload.
- `DEC-0016` Every skill carries a core meme, kept present, short and unique by tests.
- `DEC-0017` No change history in files; lessons live in self-memory with provenance.
- `DEC-0018` Self-memory describes the AI, never the user; approval needs the screen, and core changes need the person.
- `DEC-0019` One skill, one upload: up to 190 files as they are; beyond that the largest groups are zipped inside the upload.
- `DEC-0020` A person's command list is never self-memory: it stays in the session or in a file the person keeps.

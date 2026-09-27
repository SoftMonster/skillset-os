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

### Capabilities (13)

What the AI can do.

- `CAP-0001` Route a request through nested skillsets to the one member that fits it.
- `CAP-0002` Maintain its own skillset: write, edit, move, pack, import, retire and version members.
- `CAP-0004` List, discuss and audit any folder of itself with the contents and review commands.
- `CAP-0005` Learn from outside skills without copying them, and credit the source.
- `CAP-0006` Adopt an outside project as a develop member with its own checker and release workflow.
- `CAP-0007` Keep a portable self-memory that another AI can inherit through memory-pack.zip.
- `CAP-0010` Examine its own skills against the Universal Skill Curriculum Exam in a timed, evidence-only, 30-minute run.
- `CAP-0011` Work as a command line over its own skills (bash, PowerShell, cmd) and resolve verb-noun commands to skills or tools.
- `CAP-0012` Package itself at any size as skills Claude can load: one upload, or plain-folder part skills past 190 files.
- `CAP-0013` Ship itself as a Claude plugin, validated with Claude Code's own validator and a real marketplace install.
- `CAP-0014` Answer '<topic> options' with a described numbered menu, rapid replies and power moves, from a member's Options list or its members.
- `CAP-0015` Every member has a natural verb-noun command, hand-picked in front matter and checked for reserved words and duplicates.
- `CAP-0016` Carry fixes from a shared copy into the personal source with `upstream`, reversing edition patches so no edition wording leaks.

### Skills (3)

Reusable capabilities and skill definitions, with their status.

- `SKL-0001` The skillset's members are its skills; SKILLS.md in a memory pack lists every one with its version.
- `SKL-0002` Self-memory keeping is a skill of its own: the self-memory member of skillset-tools.
- `SKL-0003` universal-skill-curriculum-exam: timed self-examination with a coverage ledger and a marking gate.

### Lessons (48)

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
- `LES-0018` Replace <x> placeholders in imported skill descriptions first; descriptions cannot hold angle brackets.
- `LES-0020` Test shared verbs both ways after wiring new commands; show changes had silently resolved to save changes.
- `LES-0021` Merge many tiny sibling skills into one sub-skill with a section each; it cuts files enough to avoid zipping groups.
- `LES-0022` New hidden repo files must become scripts/templates entries in DOTFILES, or uploads drop them.
- `LES-0023` Derive a variant edition by exact-match patches that refuse on drift, never by forking the tree.
- `LES-0024` Before publishing, scan reference files for verbatim third-party text; keep names, drop copied descriptions.
- `LES-0025` Always quote heredocs (<<'EOF') when a script inserts Markdown; unquoted ones run backticks as commands.
- `LES-0026` Ship the skillset as a plugin by adding .claude-plugin/ around the shared edition; a root SKILL.md loads as one skill.
- `LES-0027` Validate against the platform's own tool when it can be installed; Claude Code's CLI installs from npm here and validates plugins.
- `LES-0028` Before a release, sweep all files for status text the release makes false, including the top SKILL.md the AI answers from.
- `LES-0029` Answer 'how do I publish this' from current official docs: the Claude directory takes plugins, not standalone skills.
- `LES-0031` Stay under the file limit with plain folders: merge tiny skills or split into part skills; never zip to fit.
- `LES-0032` Import a collection as plain-folder members inside a nested skillset; a packed collection is storage its skills cannot be used from.
- `LES-0033` Judge released state from the changelog now as well as at the baseline; a release cut mid-chat must make later packages bump.
- `LES-0034` Plugin zips need .claude-plugin/plugin.json inside at most one top folder; skill uploads need the skill-name folder and no manifest.
- `LES-0035` Test every install route a deliverable claims in the real product; say which routes were verified and which were not.
- `LES-0036` Bump from the last release, not the chat's baseline: a version released earlier in the same working copy must not absorb new changes.
- `LES-0037` Menus earn fast choices only with descriptions: one line per option, then replies that work as typed.
- `LES-0038` A reply that says 'you can still pick another' must leave the menu open; test the state after each kind of answer.
- `LES-0039` When a test contradicts an explanation already given, correct the explanation to the person, not just the code.
- `LES-0040` Grep counts are not evidence until the matching line is read; a false positive nearly passed as a fallback.
- `LES-0041` Reverse edition patches line by line when the block fails: indexing reorders front-matter keys and breaks exact matches.
- `LES-0042` Reverse a patch only where it reverses on both sides of a diff; one-sided reversal injects the other side's wording.
- `LES-0043` Judge what has shipped from the committed changelog; an interrupted package can leave the file saying a version shipped when it did not.
- `LES-0044` Decide independently when external fact-checking materially improves reliability; do not wait for an explicit request.
- `LES-0045` Do not claim repository inspection, testing or verification until the relevant operation has actually occurred.
- `LES-0046` Distinguish a skill definition from demonstrated mastery of the skill.
- `LES-0047` Separate file counts from classified skill counts.
- `LES-0048` Batch size changes reporting cadence, not the requirement to train skills individually.
- `LES-0049` When a repository search returns no result, treat that as tool-path uncertainty rather than proof of absence.
- `LES-0050` Skill composition should preserve explicit hand-offs between component skills.
- `LES-0051` Before importing a memory pack, compare it with the store by summary: a pack from the same baseline adds nothing.

### Successes (6)

Approaches that demonstrably worked, and when.

- `SUC-0001` Splitting large uploads into per-folder part skills kept every path and stayed under the file limit.
- `SUC-0002` A release gate that unpacks and merges the written zips catches a lost file before delivery.
- `SUC-0003` Learning from outside skills instead of importing them kept one voice and no foreign instructions.
- `SUC-0004` Grouping management members into a nested skillset roughly halved the top description.
- `SUC-0005` Mutation-testing new checks (breaking the feature on purpose) confirmed each test can fail.
- `SUC-0006` Harvested another session's candidate memories: screened, de-duplicated, re-numbered and moved into four members.

### Failures (9)

Approaches that failed, and why.

- `FAI-0001` Packing a large member into a zip to beat the file limit hid its files on GitHub and slowed every change.
- `FAI-0002` Merging source files to cut the file count traded away modularity and was reverted.
- `FAI-0003` Judging a split upload from its main part alone made a complete skillset look broken.
- `FAI-0004` A generated section added to every member first demanded a version bump for each one.
- `FAI-0005` A first release would have shipped as 1.0.1 because package bumped before any release existed.
- `FAI-0006` Shipping the plugin as a second zip beside the shared edition gave one audience two near-identical downloads.
- `FAI-0007` Zipping groups inside the upload by default made members Claude could not load as skills.
- `FAI-0008` Claimed one zip worked as both skill upload and plugin after testing only the plugin validator, not the skill uploader.
- `FAI-0009` Named a source for `use tool` (a sandbox built-in) without checking; it was the tool-use member, caught by a test.

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
- `EVO-0006` Over-limit uploads moved back from zipped groups to plain-folder part skills, because Claude cannot load zips as skills.

### Limitations (13)

Known weaknesses, uncertainty and failure modes.

- `LIM-0001` Cannot upload to claude.ai or push to GitHub; the person does both from the delivered files.
- `LIM-0003` One tool call is limited to about 300 seconds, so long test runs must be split.
- `LIM-0004` The sandbox reaches only package registries and GitHub; other sites fail from scripts.
- `LIM-0005` Uploads can drop executable bits and dotfiles; pull restores bits and templates avoid dotfiles.
- `LIM-0006` Routing quality is only as good as the fixture; unmeasured prompts may still misroute.
- `LIM-0007` The user-protection screen is pattern-based: it catches common identifiers, not every personal fact.
- `LIM-0008` claude.ai rejects skill uploads of more than about 200 files; a zip inside the upload counts as one file.
- `LIM-0010` The command line cannot run programs or open screen editors; edits must be described, then remembered.
- `LIM-0011` Claude's skill system cannot load a zip as a skill; zipped members work only through skillset.py open with code execution.
- `LIM-0012` git tag fails in the sandbox without an identity; tags and GitHub releases are left to the person.
- `LIM-0013` claude.ai's Skills page rejects any zip holding .claude-plugin/plugin.json; a zip is a skill upload or a plugin, never both.
- `LIM-0014` Conversational skill training changes behavioural procedures but does not modify underlying model weights.
- `LIM-0015` The memory screen reads dates as long personal numbers and refuses them; cite sources without dates.

### Maintenance (7)

Self-maintenance that is required or recommended.

- `MNT-0001` Keep headroom in the 1024-character top description; index prints how much is used.
- `MNT-0002` Re-check the routing fixture after any trigger, description or move.
- `MNT-0003` Add a routing confusion matrix to show which members get mistaken for each other.
- `MNT-0004` Design skill composition (building a chain of skills for one request) as a separate piece of work.
- `MNT-0005` After each change, record new self-knowledge through the memory pipeline, and supersede what it replaces.
- `MNT-0006` Rerun the curriculum exam after significant changes, and record each marked run as an experiment to track the trend.
- `MNT-0007` Maintain a verified training ledger so completion claims can be reconciled against the actual repository inventory.

### Decisions (22)

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
- `DEC-0020` A person's command list is never self-memory: it stays in the session or in a file the person keeps.
- `DEC-0021` One upload up to 190 files; beyond that, plain-folder part skills. Zips are storage, never skills; --pack-groups is opt-in.
- `DEC-0023` Skillset-OS is portable: other AIs adopt it to the extent of their competence, putting their own values and maker's guidelines first.
- `DEC-0024` The shared edition ships as the Claude plugin only: one zip, installed at Customize > Plugins or from the plugin repository.
- `DEC-0025` The personal edition is the one source: fixes made in the shared edition go upstream into it every time, then it is packaged.

# Changelog

## 1.8.5 — 2026-09-27

- Self-memory: design principles confirmed as the tie-breaker (DEC-0026); one-call test run replaces the three-part split (MNT-0013 supersedes MNT-0009).

## 1.8.4 — 2026-09-27

- Routing 2x faster (C YAML loader, identical routes); design principles in ARCHITECTURE.md; self-memory from an outside AI review reconciled.

## 1.8.3 — 2026-09-27

- Rapid route sends shell command lines to the shell; routing fixture keys aligned with documented exam and self-memory behaviour; blind-grade results in self-memory.

## 1.8.2 — 2026-09-27

- Card map: every word-overlap suggestion reviewed by hand (64 of 922 cards mapped to 31 members, 126 rejected with reasons); rejected status; EXP-0009.
- Updated `cognition/metacognition/universal-skill-curriculum-exam` to 1.3.2: card map: all word-overlap suggestions reviewed; rejected status

## 1.8.1 — 2026-09-27

- Exam card map: 34 of 922 curriculum cards mapped by hand to the members that cover them; card_map.py check, plan and suggest; curriculum exam run 1 recorded (EXP-0008); MNT-0010 closed.
- Updated `cognition/metacognition/universal-skill-curriculum-exam` to 1.3.1: card map: test and score cards by the member that covers them

## 1.8.0 — 2026-09-27

- Verified training ledger; composition prompts with needs lists and coverage scoring; leak-free routing sheet; MNT-0003 and MNT-0007 closed.
- Updated `skillset-tools/write-subskill` to 1.4.0: composition prompts: needs lists and composition coverage
- Updated `self-improvement/training-skills` to 1.5.0: verified training ledger: init, mark with evidence, reconcile against the inventory

## 1.7.0 — 2026-09-27

- Routing confusion matrix, rapid-route baseline and compare in routing_eval.py; rapid-route experiment and fallback lesson in self-memory.
- Updated `skillset-tools/write-subskill` to 1.3.0: routing confusion matrix, rapid baseline and compare

## 1.6.3 — 2026-09-27

- Merge five self-memory items from a 1.0.0 branch: paging experiment, append-only context, three lessons.

## 1.6.2 — 2026-09-27

- Merge uploaded 1.0.0 snapshot: recover routing experiment EXP-0005 into self-memory.

## 1.6.1 — 2026-09-27

- approved command-database capability and evolution in self-memory.
- Self-memory: approved CAP-0017 (command-database routing) and EVO-0007 (every member keeps a Commands tree), confirmed by the person.

## 1.6.0 — 2026-09-27

- command trees in every skill and a SQLite command database for rapid routing.
- Every member keeps a `## Commands` emoji tree of the commands that trigger it, under meme headings, each saying how the skill uses it; a heading's command focuses its group and runs its children.
- A SQLite command database (`scripts/commands.py`) routes typed commands rapidly: aliases, then exact commands inside the focus, then the fuzzy matcher. New verbs: `focus`, `unfocus`, `commands tree`, `why`, `db <sql>`, `prefer`, `disable`, `enable`, `alias`, `request command`, `advise commands`.
- Missing and ambiguous commands are kept as Wanted; a menu pick repeated twice becomes a direct route. Preferences, aliases and requests travel in the person's own `my-commands.md`.
- Every sub-skill rose one minor version for its new Commands tree (command-line, write-subskill and edit-subskill also gained the instructions for it).
- `check` validates every tree (malformed is an error; missing, as in imported skills, or shared with another skill is a warning); templates start one.

## 1.5.1 — 2026-09-27

- Harvested another session's routing memories: re-numbered past id clashes, approved LES-0052, LES-0054 and MNT-0008, held LES-0053 and EXP-0004 as candidates; the apply test no longer assumes an empty candidate list.

## 1.5.0 — 2026-09-27

- Harvested another session's memory: nine screened lessons, a limitation and a maintenance item, carried into verification, research, skill-composition and training-skills.
- Updated `self-improvement/training-skills` to 1.3.0.
- Updated `cognition/action-agency/skill-composition` to 1.1.0.
- Updated `cognition/reasoning/research` to 1.1.0.
- Updated `cognition/action-agency/verification` to 1.1.0.

## 1.4.0 — 2026-09-27

- Shared fixes flow back: 'upstream' carries fixes from a shared copy into the personal source in its own wording, as a standing sync-skillset step; pull and package warn in an edition copy.
- Updated `skillset-tools/publish-plugin` to 1.1.0.
- Updated `sync-skillset` to 1.3.0.

## 1.3.0 — 2026-09-27

- Outstanding fixes: every member has a hand-picked command (no generic 'use' commands, the broken 'remember long-term-memory' replaced), the shell leaves itself out of its top list, options menus work without code execution, and the top description has headroom again.
- Updated `cognition/action-agency/tool-use` to 1.0.1.
- Updated `sync-skillset` to 1.2.2.
- Updated `software-dev/time-bounded-file-improvement` to 1.0.1.
- Updated `software-dev/software-dev-best-practices` to 1.0.1.
- Updated `software-dev/performance-tuning` to 1.0.1.
- Updated `software-dev/git-workflow` to 1.0.1.
- Updated `software-dev/codebase-orientation` to 1.0.1.
- Updated `software-dev/ci-cd-pipeline` to 1.0.1.
- Updated `skillset-tools/self-memory` to 1.1.1.
- Updated `skillset-tools/publish-plugin` to 1.0.2.
- Updated `self-improvement/training-skills` to 1.2.1.
- Updated `self-improvement/reflect-and-review` to 1.0.1.
- Updated `self-improvement/plan-and-prioritise` to 1.0.1.
- Updated `self-improvement/money-habits` to 1.0.1.
- Updated `self-improvement/mindset-resilience` to 1.0.1.
- Updated `self-improvement/life-vision` to 1.0.1.
- Updated `self-improvement/goal-setting` to 1.0.1.
- Updated `self-improvement/energy-and-wellbeing` to 1.0.1.
- Updated `self-improvement/decision-making` to 1.0.1.
- Updated `self-improvement/career-growth` to 1.0.1.
- Updated `interpersonal/workplace-relationships` to 1.0.1.
- Updated `interpersonal/social-confidence` to 1.0.1.
- Updated `interpersonal/influence-persuasion` to 1.0.1.
- Updated `interpersonal/friendships-connection` to 1.0.1.
- Updated `interpersonal/emotional-intelligence` to 1.0.1.
- Updated `interpersonal/difficult-conversations` to 1.0.1.
- Updated `interpersonal/close-relationships` to 1.0.1.
- Updated `interpersonal/boundaries-assertiveness` to 1.0.1.
- Updated `interpersonal/apologies-repair` to 1.0.1.
- Updated `interpersonal/active-listening` to 1.0.1.
- Updated `command-line` to 1.4.0.
- Updated `cognition/social-intelligence/social-cognition` to 1.0.1.
- Updated `cognition/social-intelligence/relationship-modelling` to 1.0.1.
- Updated `cognition/social-intelligence/intent-inference` to 1.1.1.
- Updated `cognition/social-intelligence/cultural-intelligence` to 1.0.1.
- Updated `cognition/social-intelligence/affective-understanding` to 1.0.1.
- Updated `cognition/safety-governance/transparency` to 1.0.1.
- Updated `cognition/safety-governance/threat-detection` to 1.0.1.
- Updated `cognition/safety-governance/safety-regulation` to 1.0.1.
- Updated `cognition/safety-governance/privacy-stewardship` to 1.0.1.
- Updated `cognition/safety-governance/manipulation-detection` to 1.0.1.
- Updated `cognition/safety-governance/human-escalation` to 1.0.1.
- Updated `cognition/safety-governance/ethical-skill-evolution` to 1.0.1.
- Updated `cognition/safety-governance/ethical-reasoning` to 1.0.1.
- Updated `cognition/safety-governance/boundary-management` to 1.0.1.
- Updated `cognition/reasoning/simulation` to 1.0.1.
- Updated `cognition/reasoning/second-order-reasoning` to 1.0.1.
- Updated `cognition/reasoning/reasoning` to 1.0.1.
- Updated `cognition/reasoning/creativity` to 1.0.1.
- Updated `cognition/reasoning/bias-detection` to 1.0.1.
- Updated `cognition/reasoning/adversarial-thinking` to 1.0.1.
- Updated `cognition/perception-sensing/uncertainty-awareness` to 1.0.1.
- Updated `cognition/perception-sensing/perception` to 1.0.1.
- Updated `cognition/perception-sensing/feedback-processing` to 1.0.1.
- Updated `cognition/metacognition/universal-skill-curriculum-exam` to 1.2.1.
- Updated `cognition/metacognition/metacognition` to 1.0.1.
- Updated `cognition/metacognition/exam-regression-battery` to 1.0.2.
- Updated `cognition/metacognition/continuous-self-correction` to 1.0.1.
- Updated `cognition/memory-context/working-memory` to 1.0.1.
- Updated `cognition/memory-context/semantic-understanding` to 1.0.1.
- Updated `cognition/memory-context/self-model` to 1.0.1.
- Updated `cognition/memory-context/long-term-memory` to 1.0.1.
- Updated `cognition/memory-context/context-awareness` to 1.0.1.
- Updated `cognition/human-ai-augmentation/scaffolding` to 1.0.1.
- Updated `cognition/human-ai-augmentation/human-ai-collaboration` to 1.0.1.
- Updated `cognition/human-ai-augmentation/cognitive-offloading` to 1.0.1.
- Updated `cognition/executive-function/proportionality` to 1.0.1.
- Updated `cognition/executive-function/planning` to 1.0.1.
- Updated `cognition/executive-function/long-term-orientation` to 1.0.1.
- Updated `cognition/executive-function/goal-alignment` to 1.0.1.
- Updated `cognition/executive-function/adaptation` to 1.0.1.
- Updated `cognition/executive-function/action-selection` to 1.0.1.
- Updated `cognition/communication-regulation/memetic-ethics` to 1.0.4.
- Updated `cognition/communication-regulation/emoji-list-generator` to 1.0.1.
- Updated `cognition/communication-regulation/communication` to 1.0.2.
- Updated `cognition/action-agency/verification` to 1.0.2.
- Updated `cognition/action-agency/skill-composition` to 1.0.1.
- Updated `cognition/action-agency/skill-acquisition` to 1.0.1.
- Updated `cognition/action-agency/evidence-hygiene` to 1.0.3.
- Updated `cognition/action-agency/error-correction` to 1.0.1.
- Updated `cognition/action-agency/agentic-execution` to 1.0.1.
- Updated `apps` to 1.1.1.

## 1.2.0 — 2026-09-27

- Options menus: '<topic> options' gives a described numbered menu with rapid replies and power moves; training has its own option list.
- Updated `self-improvement/training-skills` to 1.2.0.
- Updated `command-line` to 1.3.0.

## 1.1.1 — 2026-09-27

- Fix: a version already released in this working copy now bumps when new changes arrive.
- The shared edition zip is the Claude plugin: install it at Customize > Plugins, not Skills (the Skills page rejects plugin manifests).
- Updated `skillset-tools/publish-plugin` to 1.0.1.
- Updated `sync-skillset` to 1.2.1.

## 1.1.0 — 2026-09-27

- Fix: a release cut earlier in the same working copy now counts, so later packages bump.
- Zips are storage, never skills: over the limit, uploads split into plain-folder part skills; the shared edition is also the Claude plugin, in one download; other AIs can adopt the skillset; new skillset-tools/publish-plugin.
- Updated `command-line` to 1.2.0.
- Updated `software-dev/repo-adoption/adopt-repository` to 1.1.0.
- Updated `sync-skillset` to 1.2.0.
- Updated `skillset-tools/import-skill` to 1.1.0.
- Updated `skillset-tools/organise-skillsets` to 1.1.0.
- Added sub-skill `skillset-tools/publish-plugin` 1.0.0: Publishes the skillset as a Claude plugin and lists it in the Claude directory: checks the current directory rules, builds the shared edition (which doubles as the plugin), validates it with Claude Code's own validator, test-installs it, sets up the plugin repository, cuts the release and hands over the submission steps.

## 1.0.0 — 2026-09-27

- Release 1.0.0; the plugin is gated to equal the shared edition plus its manifests.
- Add the Claude plugin build: skillset-os-plugin.zip from the shared edition.
- Enhancement loop: skill enhancements offer exam, self-marking (pre-authorisation allowed), then forming and harvesting memories.
- Updated `skillset-tools/self-memory` to 1.1.0: Enhancement loop: exam, self-mark with pre-authorisation, form and harvest memories
- Updated `skillset-tools/find-skills` to 1.1.0: Enhancement loop: exam, self-mark with pre-authorisation, form and harvest memories
- Updated `skillset-tools/write-subskill` to 1.1.0: Enhancement loop: exam, self-mark with pre-authorisation, form and harvest memories
- Updated `skillset-tools/edit-subskill` to 1.1.0: Enhancement loop: exam, self-mark with pre-authorisation, form and harvest memories
- Updated `cognition/metacognition/universal-skill-curriculum-exam` to 1.2.0: Enhancement loop: exam, self-mark with pre-authorisation, form and harvest memories
- Liability review: disclaimers (no warranty, not professional advice, not affiliated with Anthropic, no data collected, donations buy nothing) in README, NOTICE, LICENSE and SKILL.md; copied third-party descriptions removed from the curriculum exam.
- Updated `cognition/metacognition/universal-skill-curriculum-exam` to 1.1.0: Removed third-party skill descriptions (capability cues); names only, with a provenance note
- Shared edition: skillset-os-shared.zip built from editions/shared patches (quiet style, narrower triggers, built-in tools first, care first, no in-chat donation prompts, full mode on request).
- Updated `sync-skillset` to 1.1.0: Hand-over covers edition uploads such as skillset-os-shared.zip
- Early access: status documented in README, NOTICE and SKILL.md; 1.0.0 stays unreleased until published.
- Donationware: Andrew Wright named as copyright holder; GitHub Sponsors (Softmonster) in LICENSE note, NOTICE, README badge and section, CONTRIBUTING, pyproject and `.github/FUNDING.yml` (restored from a template); one optional support suggestion per conversation in SKILL.md.
- Ambiguity routing: numbered menus with 0 infer, conversation openers with a Skillset-OS review, phone-autocorrect readings; apps date/confidence and deliverable-options rules; shorter training reports.
- Updated `self-improvement/training-skills` to 1.1.0: short drill reports, self-graded ticks disclosed, stop when lessons run out
- Updated `apps` to 1.1.0: date-and-confidence checks, and only offering deliverable next steps
- Updated `cognition/social-intelligence/intent-inference` to 1.1.0: resolve ambiguity with a numbered menu the person answers with one number
- Updated `command-line` to 1.1.0: ambiguous and near-miss commands resolve through a numbered menu answered by a bare number
- Harvest exam lessons into verification, evidence-hygiene, self-memory, edit-subskill, sync-skillset and the exam skill; add memory harvesting as a standing suggestion; trim memetic-ethics.
- Updated `sync-skillset` to 1.0.1.
- Updated `skillset-tools/edit-subskill` to 1.0.1.
- Updated `cognition/action-agency/evidence-hygiene` to 1.0.2.
- Updated `cognition/communication-regulation/memetic-ethics` to 1.0.3.
- Updated `skillset-tools/self-memory` to 1.0.2.
- Updated `cognition/communication-regulation/memetic-ethics` to 1.0.2.
- Updated `cognition/metacognition/universal-skill-curriculum-exam` to 1.0.1.
- Updated `skillset-tools/self-memory` to 1.0.1.
- Updated `cognition/action-agency/evidence-hygiene` to 1.0.1.
- Updated `cognition/action-agency/verification` to 1.0.1.
- Numbered next-step suggestions replace the fixed closing line; add evidence-hygiene and exam-regression-battery sub-skills.
- Updated `cognition/communication-regulation/communication` to 1.0.1.
- Updated `cognition/communication-regulation/memetic-ethics` to 1.0.1.
- Added sub-skill `cognition/action-agency/evidence-hygiene` 1.0.0: A pre-flight checklist for any claim of success: prove each check can fail, measure effects instead of exit codes, keep unknowns visible, evaluate on data you did not tune on, keep evidence cumulative, and route irreversible or promotion decisions to a human.
- Updated `cognition/metacognition/exam-regression-battery` to 1.0.1: description follows the Use-when convention (found by E45 skill tester)
- Added sub-skill `cognition/metacognition/exam-regression-battery` 1.0.0: Reruns every earlier self-examination check in seconds and reports PASS, FAIL or KNOWN with evidence, so each new exam run starts from reproduced evidence instead of losing it.
- apps: twenty mimic apps merged into one sub-skill with a section per app; no nested zips in the upload.
- Import 20 mimic apps as a packed apps skillset, wired into the command line; command-line review fixes.
- Imported 20 mimic apps as the nested skillset `apps`, packed as one file: archive, browse, calc, define, drive, ed, feed, git, img, inbox, near, pdftool, pics, pkg, score, sheet, sql, translate, watch, weather. Placeholders in their descriptions changed from `<x>` to `X` (descriptions cannot hold angle brackets), their install note now names Skillset-OS, and `git` hands shell and commit work to command-line and git-workflow. The command line opens an app from its command words, read from each description; new `apps` verb; fixed `show changes` resolving to `save changes`.
- Packed `apps` into a zip (22 files).
- Imported `apps`: a collection of 20 skills.
- Added skillset `apps` 1.0.0: Mimic apps: twenty short-command skills that behave like everyday apps inside the chat, built on Claude's own tools: archive (zip, unzip), browse (show a web page as Markdown), calc, define, drive (Google Drive), ed (line editor), feed (RSS), git (read public GitHub repositories), img (image editing), inbox (email and calendar), near (places and routes), pdftool, pics (image search), pkg (npm, PyPI, crates.io), score (sports), sheet (spreadsheets), sql, translate, watch (page changes) and weather.
- Command line review fixes: wildcards in `ls`/`dir` (`*.md`, cmd's `*.*`) with a message when nothing matches; names match without case or a unique extension (`more changelog`); `display` and `view` read files; bare `commands` and `commands all` list commands; new `review commands`; unknown verbs get "I don't know that command" instead of a low-confidence guess. Docs: favourites word order, adventure-style verbs vs plain replies, `open` with member names, known naming gaps. Fixed "skillset set" typo in `adopt-repository`.
- Command line: navigate the skills in bash, PowerShell or cmd syntax, remembered edits applied only on request, verb-noun commands resolved to skills, built-in skills and tools, a generated command list, and a person's command list kept only in the session or a file they hold.
- Added sub-skill `command-line` 1.0.0: Runs Skillset-OS as a command line as well as in plain English: navigates the skills as a file system in bash, PowerShell or cmd syntax (ls, cd, cat, dir, type, Get-ChildItem, grep, tree...), remembers edits without applying them until an updated repository is requested, turns verb-noun commands like review code, plan feature or create spreadsheet into the skill, built-in skill or tool that does them, generates the most useful commands from what the skillset knows, and keeps a person's own command list only for the session or in a file they hold.
- Imported universal-skill-curriculum-exam into cognition/metacognition for timed self-examination; exam technique moved beside it; results feed self-memory to monitor performance over time.
- Updated `cognition/metacognition/universal-skill-curriculum-exam` to 1.1.0: core meme, 30-minute deadline fix, Skillset-OS monitoring through self-memory
- Imported `cognition/metacognition/universal-skill-curriculum-exam` 1.0.0 as a skill.
- One upload at any size: up to 190 files as they are, beyond that the largest groups are zipped inside the upload and unzipped with Python to read; --split keeps separate part skills as an option; self-memory updated.
- AI self-memory (Step 5): memory store, user-protection screen, review and approval, supersession, SELF.md entry point, memory-pack.zip export and import, acceptance test; self-memory member; pre-release packaging.
- Added sub-skill `skillset-tools/self-memory` 1.0.0: Keeps the AI's own persistent self-memory for Skillset-OS: turns a conversation's evidence into reviewed lessons, successes, failures, experiments, limitations and other self-knowledge, screens every item against the user-protection boundary, and exports or imports memory-pack.zip so another AI can carry on.
- First version of Skillset-OS.

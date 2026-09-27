# Writing guide

Read this before writing a sub-skill's trigger, description or body.

## Contents

- How a sub-skill is loaded
- The trigger
- The description
- The body
- Resources: scripts, references, assets
- Anti-patterns
- Final checklist

## How a sub-skill is loaded

1. **Always**: Claude sees the skillset's name and description, built from the top-level members' triggers. This decides whether the skillset opens at all.
2. **When the skillset opens**: Claude reads the top `SKILL.md`, whose router table shows each member's description, and picks one; a nested skillset has its own table, so this repeats until a sub-skill is reached.
3. **On choosing it**: Claude reads the whole `SUBSKILL.md`.
4. **On demand**: files beside it are read only when `SUBSKILL.md` points to them and the task needs them. Scripts can be run without being read.

So the trigger must get the skillset (or its group) chosen, the description must win against sibling sub-skills, the body must be worth its tokens, and rarely needed detail goes in separate files.

## The trigger

A verb phrase in the words people actually type, under 160 characters (aim for under 80), no angle brackets:

> write meeting minutes from rough notes or a transcript

It is joined with the other triggers into one sentence, "Use when the user wants to: ...; ...". So write it to read naturally after "wants to:" and keep it free of semicolons.

## The description

**Formula**: *[What it does, naming concrete outputs.] Use when [situations, phrases, file types]. [Optional: Do not use for X; use the Y sub-skill instead.]*

- Third person ("Builds ...", "Reviews ..."), never "I" or "you".
- Put the distinctive words first: the file type, the tool, the domain term.
- Lean towards being chosen, and name adjacent situations it also handles.
- Add a "Do not use for" clause when a sibling sub-skill is close.
- No angle brackets.

Weak:

> Helps with reports.

Strong:

> Turns raw sales exports (CSV or XLSX) into the team's monthly sales report as a Word document with a summary table, regional charts and a commentary section in house style. Use when the user asks for the monthly or quarterly sales report, uploads a sales export and wants it written up, or asks to refresh last month's report with new numbers.

**Routing check.** Write three prompts that should reach the sub-skill and three near-misses that should not. For each, read the top description (does the skillset open?) and each router table on the way (is this the member you would pick?). Fix the trigger or description until the answers are right.

## The body

**Start with a core meme**: directly under the title, `🧬 **Core meme:**` and the skill's essence in one line under 100 characters that still makes sense quoted alone ("Make it tiny, tie it to a cue, and never miss twice"). It is what people and Claude remember and pass on; see `memetic-ethics` in cognition/communication-regulation.

**Open with the goal**: one or two sentences on what good output is and who it is for.

**Give an ordered workflow.** Number the steps. For more than three steps, include a copyable checklist so progress survives a long task.

**Set defaults, not menus.** "Use pdfplumber for text extraction" beats a list of five libraries. Mention an alternative only for a specific case ("for scanned PDFs, OCR with pytesseract").

**Explain why.** "Keep headings under 60 characters because the portal truncates them" lets Claude handle cases the rule never mentioned. Capitals and "NEVER" without a reason make Claude rigid in the wrong places.

**Match freedom to fragility.**
- Low freedom (exact commands, a script to run unchanged) for fragile or order-sensitive operations: migrations, file formats, uploads.
- High freedom (goals and criteria) for judgement work: writing, reviewing, designing.

**Show, don't describe.** An example of input and the expected output teaches format faster than paragraphs. For fixed formats, give a template to fill in.

**Build in checks.** For anything that can fail quietly, add a validate step and a "fix and re-run" loop: run the checker, fix what it reports, run it again.

**Collect gotchas.** A short section of traps (odd API behaviour, wrong-but-plausible approaches, past failures) is often the most valuable part of a skill.

**Cut what Claude knows.** Don't explain what a PDF is or how to write Python. Every line should change behaviour.

## Resources: scripts, references, assets

**Scripts** (a `scripts/` folder beside `SUBSKILL.md`): use for deterministic, repeated or fiddly work (parsing, validation, conversion, packaging).

- Give each a docstring and `--help`, clear error messages that say what to do next, and meaningful exit codes.
- Handle missing files and bad input explicitly instead of crashing.
- Explain magic numbers in a comment.
- State dependencies. The sandbox can install from PyPI and npm but cannot reach most other sites.
- Say in SUBSKILL.md whether to run the script or read it.

**References** (Markdown files beside `SUBSKILL.md`): long material needed only sometimes, such as API details, style rules or schemas.

- Link each one directly from SUBSKILL.md with a note on when to read it. Keep them one level deep, not references to references.
- Give a file over 100 lines a Contents list at the top.
- Name files by content: `invoice-schema.md`, not `doc2.md`.

**Assets** (an `assets/` folder beside `SUBSKILL.md`): templates, fonts, images and boilerplate used in the output rather than read.

Use forward slashes in all paths.

## Anti-patterns

- A vague description, or one saying only what the skill is and never when to use it.
- Walls of MUST and NEVER with no reasons.
- Offering several equal options where one default would do.
- Instructions overfitted to the one example that prompted the skill.
- Duplicating the same guidance in SUBSKILL.md and a reference file.
- A file named `SKILL.md` anywhere but the top of the skillset (outside zips): the uploader expects exactly one.
- Time-sensitive statements ("the new API released this month"). Write "current" behaviour and put legacy notes in a clearly marked section.
- Scripts that fail silently or print stack traces with no advice.
- Deeply nested reference chains.

## Final checklist

- [ ] Core meme under the title: one line, under 100 characters, meaningful on its own
- [ ] Trigger is a short verb phrase in the person's words
- [ ] Description says what and when, in the third person
- [ ] Routing check done: three should-reach and three near-miss prompts
- [ ] Body under 500 lines, workflow numbered, defaults given, reasons explained
- [ ] At least one concrete example or output template
- [ ] Gotchas section, if there are any known traps
- [ ] Every script run on a realistic input
- [ ] No TODO left; `skillset.py check` passes

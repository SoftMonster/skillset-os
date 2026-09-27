# Edit recipes

Common changes to a sub-skill, how to make each one without breaking anything else, and the version bump each needs.

## Contents

- Choosing the version bump
- The sub-skill was not used, or was used wrongly
- The sub-skill did the wrong thing
- Adding a step or a capability
- Fixing a script
- SUBSKILL.md is too long
- Renaming
- Someone else's work

## Choosing the version bump

| Change | Bump |
|---|---|
| Typo, clearer wording, a fixed script bug, a new gotcha | patch |
| New trigger situations, a new step or option, a new script or reference | minor |
| Rename, removed capability, changed output format that people or other skills rely on | major |

When unsure between two, take the higher one: it costs nothing and guarantees the new copy wins.

## The sub-skill was not used, or was used wrongly

Routing happens in two places, so find which one failed:

- **The skillset did not open**: the trigger of the top-level member on the route (the sub-skill, or the nested skillset holding it) lacks the person's wording. Add it, keeping the trigger a short verb phrase, and check the top description stays under 1024 characters (`skillset.py index` prints the length).
- **The skillset opened but another member was picked**: sharpen this sub-skill's `description`, and add a "Do not use for X; use the Y sub-skill instead." clause to the sibling that won.
- **Used for the wrong request**: add a "Do not use for" clause naming the situation that caught it.
- Keep all existing triggers, and check the change against the prompt that failed and one that already worked.

Bump: minor.

## The sub-skill did the wrong thing

Find which instruction led there before changing anything:

- **An ambiguous step**: rewrite that step with a concrete default and the reason for it.
- **A missing case**: add it to the step, or to Gotchas if it is a trap rather than a routine case.
- **Claude ignored a rule**: rules without reasons get bent. Add the reason; move the rule to where it applies, not a distant Rules list.
- **Wrong output format**: add a short example or template of the right output.

Don't add a rule in capitals when an explanation would do. Bump: patch, or minor if the output changes.

## Adding a step or a capability

- Put it where it happens in the workflow and renumber the steps and the checklist together.
- If it only applies sometimes, add it as a conditional branch ("For scanned PDFs, ...") or a reference file linked from the relevant step, not as a new always-run step.
- If people will ask for it in new words, add those words to the description.

Bump: minor.

## Fixing a script

- Reproduce the failure first with a small realistic input, then fix, then run the same input again.
- Keep the command-line interface compatible; if it must change, update every place SUBSKILL.md shows the command.
- Improve the error message for the case that failed so it says what to do next.
- Add a test under the skillset's `tests/` for the case.

Bump: patch, or minor if the script gains options.

## SUBSKILL.md is too long

Over about 500 lines, or when most of it is detail needed only sometimes:

- Keep the goal, rules, workflow and gotchas in SUBSKILL.md.
- Move long reference material (API details, style rules, schemas, big examples) into `<topic>.md` beside SUBSKILL.md, with a Contents list if it is over 100 lines.
- In SUBSKILL.md, link each moved file from the step that needs it, saying when to read it.
- Move the text unchanged, then check nothing was dropped with `git diff --stat` (lines removed from SUBSKILL.md should roughly equal lines added in references).

Bump: patch, since behaviour should not change.

## Renaming

Use `skillset.py rename`, which bumps the major version. Then fix each mention it lists, and update the title line in SUBSKILL.md if it repeats the old name. The skillset keeps its own name, so the upload simply replaces the old one.

## Someone else's work

For a sub-skill with its own licence file or one listed in `NOTICE.md` as imported:

- Add rather than remove: new steps, clarifications, extra triggers, fixes.
- Keep the author's wording outside the changed lines.
- If its licence requires modified files to say so (Apache-2.0 does, MIT does not), add that notice in the files themselves. Keep lessons from the change in self-memory (`skillset-tools/self-memory`), not in a change log.
- Never remove the licence file.
- If the licence forbids modification, don't edit; tell the person.

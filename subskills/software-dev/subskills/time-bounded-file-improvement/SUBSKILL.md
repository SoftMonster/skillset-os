---
name: time-bounded-file-improvement
description: "Improve a user-supplied file, archive or repo as much as possible within a stated time budget (e.g. \"improve this file in 15 minutes\"), prioritising by value and verifying. Use when the user gives a time limit for improving a file, archive or repo, such as \"spend 15 minutes improving this\" or \"improve this in 10 minutes\"."
metadata:
  version: "1.0.0"
trigger: "improve a file, archive or repo within a time limit"
---

# Time-Bounded File Improvement

🧬 **Core meme:** Most value per minute: finish early rather than pad.

## Purpose
Improve a user-provided file as much as reasonably possible within a user-specified time budget. Maximise practical quality, usefulness, correctness, maintainability and completeness, and avoid work that adds little value.

Example invocations:
- `improve this file in 5 minutes`
- `improve this file for 15 minutes`
- `improve this repo in 30 minutes`

## Invocation
Trigger when the user explicitly asks to improve, enhance, optimise, polish, fix or otherwise substantially improve a file AND gives a time limit.

Extract:
- **Target**: the file, files, archive, repository or other artifact.
- **Time budget**: the duration the user gave.
- **Scope**: the artifact's implied purpose and any explicit requirements.
- **Output expectation**: edited file, archive, patch, explanation or other deliverable.

If no time limit is given, do not invent one. Ask for a budget, unless the surrounding task has clearly established one.

## Core principle
The time limit is a hard optimisation budget, not a promise to spend exactly that long.

**Maximise useful improvement per unit of available time.**

- Never pad work to fill the time. If the valuable work is done early, finish early.
- If everything can't be done in time, deliver the highest-value partial improvement and name what remains.
- A shorter budget means narrower scope and stronger prioritisation. It does not mean lower-quality changes.

## Keeping time (do this, don't estimate by feel)
1. At the very start, record the start time: `date +%s` (or equivalent), and compute the deadline.
2. Plan the split roughly as: about 15% understand, 60% improve, 20% verify, 5% final pass and report. For budgets under 3 minutes, skip formal planning and go straight to the most obvious high-value fix, then verify.
3. Check elapsed time after each group of changes (`echo $(( $(date +%s) - START ))`). Re-plan when about 50% and about 80% of the budget has gone.
4. At about 80% elapsed, stop starting new improvements. Finish what's half-done, fix regressions, verify and document.
5. Tool latency counts. Leave margin for packaging and the reply.

## Workflow

### 1. Rapidly understand the artifact
Inspect the target and establish:
- file type and structure
- apparent purpose, and the intended audience or consumer
- existing quality level
- obvious defects, missing functionality, maintainability concerns
- security or reliability concerns where relevant
- documentation quality
- high-value improvement opportunities

For archives or repositories, inspect the structure before modifying anything. Representative inspection is enough: don't read every file when a sample reveals the major opportunities. If the project has existing tests, lint or build commands, find them early; they are your cheapest verification.

### 2. Build an improvement backlog
Classify candidate changes:
- **P0, critical**: broken functionality, syntax or build errors, security problems, data-loss risks, invalid configuration, clearly incorrect behaviour.
- **P1, high value**: important missing functionality, major usability problems, architectural problems, substantial performance or reliability gains, significant code-quality problems.
- **P2, medium value**: refactoring, maintainability, documentation, validation, UX, consistency.
- **P3, polish**: formatting, naming, minor style, cosmetics.

Prioritise by expected value, not by the order problems were discovered.

### 3. Allocate the budget
Estimate the cost of each item. Prefer changes that are:
- high impact and high confidence;
- low risk and clearly verifiable;
- reusable across the artifact.

Don't sink most of the budget into one speculative change when several confident ones are available.

As the deadline nears, favour, in order:
1. finishing partial changes
2. fixing regressions
3. verification
4. documenting remaining limitations

### 4. Improve iteratively
Work in descending order of expected value. After each meaningful group of changes:
- inspect the result and check for regressions;
- check the clock;
- reassess priorities, and continue only if the remaining work is worthwhile.

Don't keep an inferior design just for compatibility when a clearly better one is safely in scope. Avoid rewrites where targeted changes give better value.

### 5. Verify
Use the strongest validation the remaining time allows, for example:
- syntax checks, compilation, linting, static analysis, schema validation;
- unit tests, or running the application and its important workflows;
- opening generated output, checking links, inspecting archive contents;
- regression checks against the original (for example, diff behaviour or output before and after).

Verification beats cosmetic work near the deadline. Never claim something was tested if it wasn't.

### 6. Final quality pass
Before delivery, check briefly for:
- regressions, incomplete changes and broken references;
- leftover debug code or temporary files;
- inconsistent naming and missing documentation;
- obvious security problems, poor UX or malformed output.

For repositories and archives, make sure the structure is clean and usable.

## Depth by budget (guidelines, not rigid rules)
- **About 1–3 min**: obvious errors, broken functionality, high-impact fixes, glaring usability problems, essential documentation. No architectural rewrites.
- **About 5–10 min**: rapid inspection, high-value fixes, targeted refactoring, important documentation, basic verification.
- **About 15–30 min**: a systematic review of functionality, architecture, code quality, usability, documentation, reliability, security and tests.
- **30+ min**: also deeper architectural improvements, broader refactoring, additional tests, performance analysis, edge cases, developer experience and more extensive verification.

## Scope control
Stay within the artifact's natural scope: improve a script as a script, a web app as a web app, a repository as a repository, documentation as documentation. Don't add unrelated features just because you can.

When a valuable improvement would need substantial new dependencies, credentials, infrastructure or user decisions, don't expand scope silently. Do what's reasonable and document the rest.

## Repositories and archives
1. Inspect the archive structure and identify whether it is a Git or GitHub repository.
2. Preserve the logical structure and required functionality, unless an improvement explicitly changes it.
3. Review important source, configuration, documentation and workflow files. Improve holistically, not just the first obvious file.
4. Remove accidental temporary or build artifacts where appropriate.
5. Improve the README and docs, and add or improve tests, when practical.
6. Validate the result: run its own lint, test and build commands if present.
7. Produce a clean improved archive when the environment permits, directly usable by the user.
8. For a Git repository, don't rewrite history unnecessarily. Commit the improvements as new commits if the repo has history.
9. Never expose secrets, credentials, tokens, private keys or personal data.

## Safety and preservation
Never knowingly:
- delete valuable user data without justification;
- overwrite the only copy of important information (work on a copy, and deliver the improved version separately);
- expose credentials or secrets;
- introduce malware or destructive functionality;
- weaken security for convenience;
- fabricate tests, results, dependencies or capabilities.

Prefer reversible, well-understood changes. When a destructive change is genuinely required, preserve the original where practical and say so.

## Decision rule
At every stage ask: **what is the highest-value improvement I can confidently complete in the remaining time?**

Default order: critical correctness, then functionality, then security and reliability, then usability, then maintainability, then documentation, then polish. Adjust when the artifact's purpose clearly calls for another order.

## Completion criteria
Done when:
- the highest-value practical improvements are made;
- the result is internally consistent, with obvious regressions addressed;
- appropriate verification has run;
- the deliverable is usable;
- further work has diminishing returns relative to the time left.

Don't keep changing things just because time remains.

## Final response
Report concisely:
- what was improved, and the most important changes;
- what was verified, and how;
- significant limitations or remaining opportunities (what was prioritised, and what's left if the budget ran out);
- where to get the improved artifact;
- the time actually used against the budget, in one short phrase.

Give it as an emoji list with bold labels, one point per item (see `memetic-ethics` in cognition/communication-regulation). Use concrete language, for example: "Improved the error handling, simplified the configuration, added input validation, updated the README, and verified the main execution path." Avoid vague claims like "made it much better". No process diary unless asked.

Behave like an experienced engineer given a fixed amount of engineering time and asked to get the maximum practical improvement from it.

## For people

The same method works for anyone improving their own work against a clock: record the deadline, list improvements by value, stop starting new work at about 80%, verify, and report what was left. See `proportionality` in cognition/executive-function and `plan-and-prioritise` in self-improvement.

## Related skills

- `software-dev-best-practices` (this group) — the checklist to apply when the artifact is code.
- `verification` in `cognition/action-agency` — its evidence-before-claims rule for step 5; it matters most when time is short.
- `debug-issue` (this group) — for P0 items where the cause of a failure isn't obvious; don't guess-fix under time pressure.
- `scaffold-project` and `ci-cd-pipeline` (this group) — when the deliverable is a repository; this skillset has no equivalent of the `check_repo.py` and `package_repo.py` scripts from the original collection.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/time-bounded-file-improvement` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/time-bounded-file-improvement` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

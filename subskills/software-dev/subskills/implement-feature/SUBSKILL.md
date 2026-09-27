---
name: implement-feature
description: "Implements code changes that fit the existing codebase: follows its conventions, works in small verified increments, adds tests alongside, handles errors and edge cases, and leaves the code runnable and linted. Use when the user asks to write, build, add, implement, code or finish a feature, function, endpoint, component, script or ticket. Do not use for fixing a reported bug (debug-issue) or for restructuring without behaviour change (refactor-code)."
trigger: "write, build or implement code, a feature or a script"
metadata:
  version: "1.0.0"
---

# Implement a feature

🧬 **Core meme:** Fit the codebase, work in small verified steps, and write tests alongside.

Write code that a maintainer of this codebase would accept on first review: it does what was asked, looks like the code around it, is tested, handles failure, and leaves lint and tests green. Small verified steps beat one large untested change.

`<top>` is the installed skillset folder.

## Workflow

```
- [ ] 1. Know where you are
- [ ] 2. Confirm the target
- [ ] 3. Build in small increments
- [ ] 4. Harden
- [ ] 5. Verify
- [ ] 6. Deliver
```

1. **Know where you are.** For an existing repo, run `python3 <top>/subskills/software-dev/subskills/codebase-orientation/scripts/detect_stack.py <repo>` and read two or three files that do something similar to the task. Copy their patterns for naming, error handling, logging, config, dependency injection and test layout. For a snippet or a new script, match the language version and style the person shows.
2. **Confirm the target.** Restate the behaviour in one or two lines, including inputs, outputs and what happens on bad input. If the request is large or ambiguous, plan it with `plan-feature` first. Otherwise, proceed and state assumptions.
3. **Build in increments.** Start with the smallest slice that runs end to end, then extend. After each slice, run the relevant tests or the script. Write the test alongside the code (see `write-tests`), not at the end.
4. **Harden.** Walk the checklist below for the code you touched.
5. **Verify.** Run the project's formatter, linter, type checker and full test suite (commands from step 1). Fix everything you introduced. If something cannot run in the sandbox (needs a database, network or secrets), say exactly what was not verified.
6. **Deliver.** For a repo, give changed files or a patch (`git diff > change.patch`) plus a short summary: what changed, why, how it was tested, and any follow-ups. For short code (20 lines or less) answering a question, reply inline; otherwise create files.

## Hardening checklist

- Inputs validated at the boundary; errors raised with messages that say what to do.
- No silent failure: no bare `except`, empty `catch`, or ignored error return.
- Resources closed (files, connections, locks) via `with`, `defer`, `using` or `try/finally`.
- Edge cases: empty, one, many, very large, unicode, None/null, duplicates, concurrent calls.
- No secrets, credentials or environment-specific paths in code; configuration comes from env or config files.
- Untrusted input never reaches SQL, shell, file paths or HTML unescaped.
- Public functions have types and a docstring where the codebase uses them.

## Example summary

```
Added CSV export to /reports.
- reports/export.py: new `export_csv(report_id)` streams rows (no full load into memory).
- api/routes.py: GET /reports/{id}/export.csv, 404 on unknown id, 403 if not owner.
- tests/test_export.py: 5 tests (happy path, empty report, unicode, 404, 403).
Ran: ruff, mypy, pytest (142 passed). Not verified: S3 upload path (needs credentials).
```

## Gotchas

- Do not add a dependency for something the standard library or an existing dependency already does; if a new one is worth it, say why.
- Do not reformat or refactor unrelated code in the same change; it hides the real diff. Suggest it separately (`refactor-code`).
- Match the existing language version. Using syntax newer than the project targets (e.g. `match` in Python 3.9) breaks CI.
- When editing an uploaded file, edit the file itself and keep everything you did not need to change byte-for-byte identical.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/implement-feature` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/implement-feature` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

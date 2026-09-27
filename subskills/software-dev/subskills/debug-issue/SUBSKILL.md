---
name: debug-issue
description: "Finds and fixes the root cause of a bug with a disciplined loop: reproduce, read the evidence, form hypotheses, bisect or instrument to isolate, fix the cause rather than the symptom, and lock it in with a regression test. Use when the user reports a bug, error message, exception, stack trace, crash, hang, flaky or failing test, wrong output, or says something worked before and now does not. Do not use for slowness without errors; use performance-tuning."
trigger: "debug, fix or explain a bug, error, crash, stack trace or failing test"
metadata:
  version: "1.1.0"
---

# Debug an issue

🧬 **Core meme:** Reproduce, fix the root cause where it starts, and lock it in with a test.

Find the root cause, fix it there, and prove it cannot silently come back. A good result explains why the bug happened in one or two sentences, changes as little as possible, and includes a regression test that failed before the fix and passes after.

## Workflow

```
- [ ] 1. Reproduce
- [ ] 2. Read the evidence
- [ ] 3. Hypothesise and test
- [ ] 4. Fix the cause
- [ ] 5. Lock it in
- [ ] 6. Explain
```

1. **Reproduce.** Get a minimal, reliable reproduction: the exact command, input and environment. Run it in the sandbox when possible. If you cannot reproduce it, say what you tried and reason from the evidence instead of guessing a fix.
2. **Read the evidence.** Read the whole stack trace from the bottom-most frame in the person's own code, not the library frames. Read the error message literally. Check what changed recently (`git log -p --since`, dependency bumps, config, data).
3. **Hypothesise and test.** List two or three candidate causes, most likely first, and design a check that tells them apart: a print or log at the boundary, a debugger breakpoint, a unit test with the failing input, or `git bisect run <test>` when it worked before. Change one thing at a time. Keep going until one hypothesis explains *all* the symptoms.
4. **Fix the cause.** Fix it where the wrong value is produced, not where it is noticed. Avoid catching and ignoring the exception, adding a sleep, or special-casing the one failing input. If the proper fix is large, offer a clearly labelled stopgap plus the real fix.
5. **Lock it in.** Add a regression test named after the behaviour (`test_parse_date_accepts_leap_day`), confirm it fails without the fix, then passes with it. Run the full suite for collateral damage.
6. **Explain.** Use the report format below.

## Report format

An emoji list, so each point transmits on its own (see `memetic-ethics` in cognition/communication-regulation):

- 🐛 **Cause:** one or two sentences on why it broke.
- 🛠️ **Fix:** what changed and where (file:line), and why this is the right place.
- 🧪 **Test:** the regression test added and the command that runs it.
- 🔎 **Also check:** other places with the same pattern, if any.

## Common cause patterns

- Off-by-one and boundary errors; inclusive vs exclusive ranges; empty collections.
- Null/None/undefined flowing from an unchecked lookup, optional field or failed parse.
- Time: timezones, DST, naive vs aware datetimes, clock-dependent tests.
- Mutable shared state: default arguments, module globals, caches, class attributes.
- Async and concurrency: missing `await`, race conditions, unhandled promise rejections, deadlocks.
- Environment drift: different dependency versions, env vars, locale, file paths, OS line endings.
- Encoding: bytes vs str, UTF-8 vs Latin-1, BOMs.
- Floating point comparisons and money in floats.

## Gotchas

- Flaky tests are real bugs, usually time, order or shared state. Run the test in a loop (`pytest -p no:randomly --count 50` with pytest-repeat, or a shell loop) to reproduce before fixing.
- "Works on my machine" usually means environment drift. Compare versions and env explicitly.
- Heisenbugs that vanish when you add logging point to timing or concurrency.
- Do not declare victory because the error message changed; confirm the original reproduction now passes.
- For slowness with no error, use `performance-tuning` instead.

## Commands

- 🐞 **Find it, fix it, prove it** · `debug issue`: Runs the whole loop on the bug described or pasted: reproduce, read the evidence, test hypotheses, fix the cause, lock it in with a test, and report cause, fix and test.
  - 🔬 **Reproduce first** · `reproduce bug`: Gets a minimal, reliable reproduction (command, input, environment) and runs it in the sandbox when possible.
    - 📋 `read stack trace`: Reads the trace from the bottom-most frame in the person's own code, and the error message literally.
    - 🕰️ `check recent changes`: Looks at recent commits, dependency bumps, config and data changes that line up with when it broke.
  - 🎯 **Isolate the cause** · `isolate cause`: Lists two or three candidate causes and runs checks that tell them apart, one change at a time.
    - 🪓 `bisect regression`: Uses git bisect run with a failing test when it worked before, to find the breaking commit.
    - 🔁 `chase flaky test`: Runs the test in a loop to reproduce flakiness, then looks at time, order and shared state.
  - 🛠️ `fix root cause`: Fixes where the wrong value is produced, not where it shows; offers a labelled stopgap only when the real fix is large.
  - 🧪 `add regression test`: Adds a test named after the behaviour, shows it fails without the fix and passes with it, then runs the full suite.
  - 🧾 `explain bug`: Reports cause, fix (file:line), test and other places with the same pattern, as an emoji list.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/debug-issue` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/debug-issue` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

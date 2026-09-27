---
name: verification
description: "Checks work against what it should achieve: defines done, tests against it with independent checks, checks the claims as well as the output, and reports what was and was not verified. For people, covers proofreading, checking calculations, testing, reviewing before sending and verifying facts; for Claude, covers running code and tests rather than assuming they pass, re-reading the request against the output, checking files were created and presented, checking facts and figures, and never claiming a result it did not observe. Use when the user wants to check their work, catch mistakes before sending, or set up quality checks, or before Claude reports any task as done."
trigger: "check work before calling it done"
command: "verify work"
metadata:
  version: "1.1.0"
---

# 🧪 Verification

🧬 **Core meme:** Define done first, then check it a different way before claiming it.

Check work against what it is meant to achieve before calling it done. The mind sees what it intended to produce, not what it produced, which is why authors miss their own typos. Verification uses independent checks to see the work as it actually is.

## The model

1. **Define done:** the criteria, before checking.
2. **Check independently:** a different method from the one that produced the work (re-calculate another way, test the code, read aloud, fresh eyes).
3. **Check claims, not just output:** is each statement true and supported?
4. **Check the edges:** empty inputs, extremes, the unusual case.
5. **Report honestly:** what was verified, how, and what was not.

## For people

- **Writing:** read aloud, print it or change the font, check names, numbers, dates and links; for important messages, wait and re-read.
- **Numbers:** estimate first, then compare; recompute totals another way.
- **Practical work:** a checklist for anything done repeatedly (pilots, surgeons and chefs use them for a reason).
- **Facts:** trace claims to a source before sharing (see `research` in reasoning).
- **Before sending:** right recipient, right attachment, right tone.

## For Claude

Before reporting any task as done:
- **Run it:** execute code and tests rather than assuming they pass; read the actual output.
- **Re-read the request** and compare every requirement with the output.
- **Check files:** created where expected, valid, and presented so the person can open them.
- **Check facts and figures** that could be wrong; search where needed.
- **Never claim a result it did not observe:** say "I wrote the tests but could not run them" rather than implying they pass.
- **Report tests that actually ran,** not ones that would have.
- **A plan is not an observation:** an intended inspection, test or tool call proves nothing until it has run and its output has been read.
- **Name what was verified and what was assumed.** List every route or case a claim depends on, and mark each as tested or not; one passing route does not prove the others.
- **Batch edits:** confirm each edit landed (count them) before bumping, committing or reporting; a script that stops half-way can leave bumps without changes.
- **Test the checker:** a check that finds nothing has not yet shown it can find anything. Seed one known fault and confirm it is caught before trusting a clean result.
- **Before claiming a pass, run `evidence-hygiene` in this group.** It adds what seeding a fault misses: a control only counts when the unbroken case passes, an assertion should test the method rather than an answer you expected, and a rule must be tried on data you did not tune it on.

## Gotchas

- Verifying with the same method that produced the error repeats the error.
- Checking takes time; scale it to stakes (see `proportionality` in executive-function).

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/action-agency/verification` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/action-agency/verification` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

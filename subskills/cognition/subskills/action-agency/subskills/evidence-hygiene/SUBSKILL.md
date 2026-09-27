---
name: evidence-hygiene
description: "A pre-flight checklist for any claim of success: prove each check can fail, measure effects instead of exit codes, keep unknowns visible, evaluate on data you did not tune on, keep evidence cumulative, and route irreversible or promotion decisions to a human. Use when about to report a task, test, audit or exam result as passed. Do not use to fix a known error; use error-correction. For everyday checking of finished work, use verification; this is its stricter checklist for claims of success."
trigger: "check my evidence before I claim something works"
command: "weigh evidence"
metadata:
  version: "1.0.3"
---

# Evidence hygiene

🧬 **Core meme:** A pass means nothing until the check has been seen to fail.

Eight rules: six promoted because it was independently re-observed in at least three exam runs (runs 3–10, counted by line diff, not by carry-forward); rules 7–8 added in run 17 after a repeated mistake.

## Checklist

```
- [ ] 1. Negative control: the check rejects a deliberately broken input
- [ ] 2. Effect, not exit code: count commits, rows or files; never trust `cmd | tail` status, and never cut a verifier's output before reading its verdict
- [ ] 3. Unknowns visible: output says "Unknown", never an estimate dressed as data
- [ ] 4. Independent evaluation: test on data you did not see while building the rule
- [ ] 5. Cumulative: save the check as a module so the next run reruns it
- [ ] 6. Human gate: irreversible actions and promotions wait for a person; only rollback is automatic
- [ ] 7. Method, not answer: the assertion tests the declared rule, not a count or value I expected
- [ ] 8. Control validity: a control counts only when the main check passes on the unbroken input
```

## Why each rule exists

1. **Negative control.** A backup check passed a bundle truncated to zero refs (run 4), and a pre-freeze check passed with a deleted section (run 8).
2. **Effect, not exit code.** `git revert -q` and `recalc` both exited 0 on failure, and piped status reported `tail`'s result (runs 3, 6). Cutting output hides verdicts too: `| tail -1` dropped a review's error count four times in one session. Search for the verdict line (`grep -E "error|warning"`) instead of truncating.
3. **Unknowns visible.** A spreadsheet divided by an unknown customer total (run 3). The fix showed "Unknown" instead of guessing.
4. **Independent evaluation.** A privacy screen scored 0/3 false positives on a tuned set and 86% on independent data (run 7).
5. **Cumulative.** Runs 2–4 lost earlier evidence and scores stalled until a battery rebuilt it (run 4).
6. **Human gate.** A canary may roll back automatically; promotion, deletes and launches may not (runs 6–9).
7. **Method, not answer.** Run 16 asserted "gap > 2x" in a market model; run 17 asserted "4 risks treated" minutes after fixing the first. Both encoded an expected answer, and the lesson did not transfer until it became a checklist item.
8. **Control validity.** In run 17 a control "failed as expected" while the main check was already failing, which proved nothing.

## Gotchas

- A check that finds nothing may be checking nothing. Confirm that the denominator is non-zero.
- Carried-forward text inflates recurrence counts. Diff consecutive versions before counting.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/action-agency/evidence-hygiene` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/action-agency/evidence-hygiene` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

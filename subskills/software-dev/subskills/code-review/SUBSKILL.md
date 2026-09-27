---
name: code-review
description: "Reviews code, a diff or a pull request and returns findings ranked by severity (blocking, should fix, nit) with file and line references, the reason, and a concrete suggested change, covering correctness, security, performance, readability, tests and design. Use when the user asks to review, critique, check or give feedback on code, a PR, a merge request, a patch or a snippet, or asks whether code is good or ready to merge. Do not use for a dedicated security audit; use security-review."
trigger: "review code, a pull request or a diff"
metadata:
  version: "1.1.0"
---

# Code review

🧬 **Core meme:** Rank findings by severity, and give a fix with each.

Give a review that a busy author can act on in minutes: the problems that matter most come first, each with where it is, why it matters and a concrete fix. Be direct about real problems, generous about good work, and quiet about taste.

## Workflow

```
- [ ] 1. Understand intent and context
- [ ] 2. Read the change twice
- [ ] 3. Verify what you can
- [ ] 4. Write findings by severity
- [ ] 5. Give a verdict
```

1. **Intent.** Read the PR description, linked issue or the person's framing. A review against the wrong goal is noise. If there is a repo, look at the surrounding code, not only the diff, because most bugs live where the diff meets unchanged code.
2. **Read twice.** First pass for design: is this the right approach and the right place? Second pass line by line using [review-checklist.md](review-checklist.md).
3. **Verify.** When code is on disk, run the linter, type checker and tests. Write a quick test for any suspected bug. A finding you have demonstrated beats one you suspect; say which is which.
4. **Findings.** Use the format below. Order by severity, then by file. Merge repeated instances of one issue into a single finding that lists all the locations.
5. **Verdict.** End with one of **Approve**, **Approve with nits**, or **Request changes**, plus one sentence why. Mention one or two things done well, specifically.

## Severity

- **Blocking**: incorrect behaviour, data loss, security hole, broken build, missing migration, breaking API change without versioning.
- **Should fix**: likely bug on an edge path, missing tests for new logic, poor error handling, performance trap, confusing design that will spread.
- **Nit**: naming, small readability wins, style the linter does not enforce. Prefix with "nit:" and keep them few; if there are more than five, give the pattern once.

## Finding format

```
**[Blocking] SQL injection in search** — `api/search.py:42`
`query` is interpolated into the SQL string, so a user can run arbitrary SQL.
Suggest: use a bound parameter.
    cur.execute("SELECT * FROM items WHERE name LIKE %s", (f"%{query}%",))
```

**Memetic check before it's sent:** review comments travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Do not review what the linter or formatter already enforces; recommend adding the tool instead.
- "Consider refactoring this" is not actionable. Show the shape of the change or drop the comment.
- Separate facts from preferences. Phrase preferences as questions or nits.
- For large diffs (over about 400 lines), say which parts you reviewed deeply and which you skimmed, and suggest splitting the PR.
- For a full security audit rather than a review, use `security-review`.

## Commands

- 🔍 **Findings ranked, each with a fix** · `review code`: Reviews pasted code, a diff or a pull request: learns the intent, reads twice, verifies claims, and returns findings ranked by severity, each with a concrete fix, then a verdict.
  - 🎯 `state review-intent`: Establishes what the change is meant to do and what matters most (correctness, security, style) before judging it.
  - 👀 **Read and verify** · `read diff`: Runs the two below: a full read for understanding, then a second pass hunting defects, verifying suspicions by running or tracing code.
    - 🐛 `hunt defects`: Looks for bugs, edge cases, error handling gaps, concurrency and resource leaks, with file:line references.
    - 🔐 `spot security issues`: Flags injection, auth, secrets and unsafe input handling; hands deep audits to review security.
  - 🧾 `rank findings`: Sorts findings into blocker, major, minor and nit, each with the problem, why it matters and the fix.
  - ⚖️ `give verdict`: Ends with approve, approve with changes, or request changes, and the one thing to fix first.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/code-review` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/code-review` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

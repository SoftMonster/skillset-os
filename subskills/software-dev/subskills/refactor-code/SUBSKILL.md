---
name: refactor-code
description: "Restructures code without changing its behaviour: secures a safety net of tests first, then applies small named refactorings (extract, inline, rename, split module, replace conditional, remove duplication), verifying after each. Also handles language or framework modernisation and dead-code removal. Use when the user asks to refactor, clean up, simplify, tidy, decouple, modernise, reduce duplication or technical debt, or make code more readable or maintainable."
trigger: "refactor, clean up, restructure or modernise code without changing behaviour"
metadata:
  version: "1.0.0"
---

# Refactor code

🧬 **Core meme:** Secure tests first, then take small behaviour-preserving steps.

Improve the structure of code while keeping its observable behaviour identical, in steps small enough that each one is obviously safe. The result should be easier to read and change, and the diff should be easy to review.

## Workflow

```
- [ ] 1. Name the goal
- [ ] 2. Build a safety net
- [ ] 3. Refactor in small named steps
- [ ] 4. Verify after every step
- [ ] 5. Deliver with a map of the changes
```

1. **Goal.** Say what should get better and why: "split the 600-line `OrderService` so pricing can change without touching fulfilment". Refactoring without a goal drifts into rewriting.
2. **Safety net.** Find the tests covering the code. If coverage is thin, first add characterisation tests that pin current behaviour, including behaviour that looks wrong. Record any suspected bugs separately; do not fix them mid-refactor, because a behaviour change inside a refactor is invisible in review.
3. **Small named steps.** Apply one refactoring at a time from the catalogue below. Keep the code compiling and tests passing between steps. Prefer automated IDE-style moves (rename, extract) done carefully over hand rewrites.
4. **Verify.** Run the tests, linter and type checker after each step. If anything fails, undo that step rather than patching forward.
5. **Deliver.** Summarise the steps in order, what moved where, and confirm behaviour is unchanged (tests run, count passed). If a large refactor, suggest splitting into several PRs along the steps.

## Catalogue (most useful first)

- **Rename** to say what it is or does.
- **Extract function/method** for a block with a clear purpose; **inline** one that adds nothing.
- **Introduce parameter object** for a group of arguments that travel together.
- **Replace conditional with polymorphism or a lookup table** when the same switch appears in several places.
- **Guard clauses** instead of deep nesting.
- **Split module/class** along reasons to change; **move function** to the data it uses most.
- **Separate I/O from logic** (functional core, imperative shell) to make logic testable.
- **Remove dead code** after confirming no references (`grep -rn`, and dynamic uses such as reflection, string-built names or public API).
- **Replace magic numbers** with named constants.

## Modernisation

For language or framework upgrades (Python 2→3 idioms, callbacks→async/await, class components→hooks, JavaScript→TypeScript), convert one module at a time behind passing tests, and prefer official codemods (`pyupgrade`, `ruff --fix` with UP rules, `jscodeshift` transforms, `npx @next/codemod`) over hand edits.

## Gotchas

- Formatting changes mixed with structural changes make diffs unreadable. Run the formatter in a separate commit first.
- Public APIs (exported functions, HTTP endpoints, database columns) have callers you cannot see. Keep the old name as a deprecated alias or ask first.
- Performance can change even when behaviour does not; for hot paths, benchmark before and after.
- "While I'm here" fixes break the promise of unchanged behaviour. List them as follow-ups.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/refactor-code` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/refactor-code` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

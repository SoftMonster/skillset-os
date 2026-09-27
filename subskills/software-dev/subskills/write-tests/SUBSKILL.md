---
name: write-tests
description: "Writes and improves automated tests: picks the right level (unit, integration, end-to-end), follows the project's test framework and style, covers behaviour, edge cases and failure paths, and keeps tests fast, isolated and deterministic. Use when the user asks for tests, test cases, coverage, fixtures, mocks, property-based or snapshot tests, a test plan, or TDD, or wants flaky tests made reliable."
trigger: "write, add or improve tests and test coverage"
metadata:
  version: "1.0.0"
---

# Write tests

🧬 **Core meme:** Test behaviour, edges and failures, and keep tests fast and deterministic.

Write tests that catch real regressions and that the team will keep: they test behaviour rather than implementation, fail with a message that points at the problem, run fast, and never flake. Match the project's framework and style exactly.

## Workflow

```
- [ ] 1. Find the existing test setup
- [ ] 2. Decide what to test and at which level
- [ ] 3. Write the tests
- [ ] 4. Run them, and prove they can fail
- [ ] 5. Report coverage of behaviour
```

1. **Existing setup.** Find the framework, folder layout, naming, fixtures, factories and mocking style (open a couple of existing test files and the test config). Reuse existing fixtures rather than inventing parallel ones. With no tests yet, use the default for the language: pytest, Vitest (Jest if already present), `go test` with table tests, `cargo test`, JUnit 5.
2. **What and where.** List the behaviours: happy path, each branch, boundaries (empty, one, max, off-by-one), invalid input and error paths, and anything that previously broke. Test at the lowest level that can see the behaviour. Pure logic gets unit tests; code crossing a database, queue or HTTP boundary gets an integration test using the real thing where cheap (SQLite, testcontainers, an in-process server); critical user journeys get a few end-to-end tests.
3. **Write.** One behaviour per test, named as a sentence (`test_refund_rejected_after_30_days`). Arrange–Act–Assert with a blank line between. Build inputs with factories or builders, not giant literals. Mock only at boundaries you do not own (network, clock, randomness); never mock the unit under test. Parametrise instead of copy-pasting near-identical tests.
4. **Run, and prove they can fail.** Run the new tests and the full suite. For each important test, break the code briefly (flip a condition) and confirm the test fails with a useful message, then restore it. A test that cannot fail is worse than none.
5. **Report** what behaviours are now covered and what is deliberately not, plus the command to run them. Quote a coverage figure only if you actually measured it (`pytest --cov`, `vitest --coverage`).

## Example (pytest)

```python
import pytest
from shop.pricing import apply_discount

@pytest.mark.parametrize("total, code, expected", [
    (100, "SAVE10", 90),
    (100, None, 100),
    (5, "SAVE10", 5),          # below minimum spend: discount ignored
])
def test_apply_discount(total, code, expected):
    assert apply_discount(total, code) == expected

def test_unknown_code_raises_with_code_in_message():
    with pytest.raises(ValueError, match="BOGUS"):
        apply_discount(100, "BOGUS")
```

## Gotchas

- Flakiness comes from time, randomness, ordering, shared state and real network. Freeze the clock, seed randomness, isolate state per test, and fake the network.
- Snapshot tests are cheap to write and easy to rubber-stamp. Use them for stable, reviewed output only.
- Asserting on log strings or private attributes couples tests to implementation; assert on outputs and observable effects.
- Chasing a coverage percentage produces assertion-free tests. Coverage shows what is untested; it does not show what is tested well.
- For TDD requests, write the failing test first, show it failing, then write the minimum code to pass.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/write-tests` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/write-tests` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

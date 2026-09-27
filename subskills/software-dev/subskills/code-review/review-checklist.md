# Review checklist

Read during the line-by-line pass of a code review. Skip sections that do not apply.

## Correctness
- Does it do what the description says, for every branch?
- Boundaries: empty, single, maximum, negative, off-by-one, overflow.
- Null/None/undefined handling; optional fields; failed parses.
- Error paths: are errors caught at the right level, surfaced with context, not swallowed?
- Concurrency: shared mutable state, races, missing awaits, lock ordering, idempotency on retry.
- Time and money: timezones, DST, float money, rounding.
- Resource cleanup: files, connections, subscriptions, timers.

## Security
- Untrusted input into SQL, shell, file paths, templates, redirects, deserialisation, regex (ReDoS).
- Authorisation checked on the server for every new endpoint or action, per object not just per route.
- Secrets or tokens in code, logs, error messages or test fixtures.
- New dependencies: maintained, licence acceptable, pinned.

## Data and APIs
- Migrations: reversible, safe on a large live table, deployed in the right order with the code.
- Backward compatibility of API responses, events and stored formats.
- Validation at the boundary; consistent error shape.

## Performance
- Queries in loops (N+1), missing indexes for new filters, unbounded result sets without pagination.
- Work repeated per request that could be done once; large objects copied unnecessarily.
- Synchronous I/O on hot paths or event loops.

## Tests
- New logic has tests that would fail if it broke; error paths are tested.
- Tests are deterministic (no real clock, network or ordering dependence).
- Tests assert behaviour, not implementation details.

## Design and readability
- Is this the right layer and module? Does it duplicate something that exists?
- Names say what things are and do; functions do one thing.
- Comments explain why, not what; no commented-out code; TODOs have an owner or issue.
- Public API surface is as small as it can be.

## Operability
- Logging at the right level with useful context and no personal data.
- Metrics or traces for new critical paths; feature flag for risky changes.
- Config and docs updated (README, env example, changelog).

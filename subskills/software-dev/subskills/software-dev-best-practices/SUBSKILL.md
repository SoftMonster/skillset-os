---
name: software-dev-best-practices
description: "Best-practice engineering checklist to follow whenever developing computer software. Use this skill for ANY task that writes, edits, refactors, debugs, reviews, tests, packages or documents code, scripts, apps, APIs, repos or build/deploy configuration, in any language, even small scripts or one-line fixes, and even if the user doesn't mention best practices."
trigger: "follow engineering best practices on any code change"
metadata:
  version: "1.0.0"
---

# Software Development Best Practices

🧬 **Core meme:** Make the smallest change that produces the largest reliable improvement.

Core principle: 🧠 **Make the smallest change that produces the largest reliable improvement.**

Apply these proportionately: a ten-line script doesn't need the ceremony of a production service, but every item below should at least be considered.

## Before changing anything
- 🎯 **Define the goal** — understand what the software must actually achieve before changing it.
- 🔍 **Inspect before editing** — understand the architecture, dependencies, entry points, configuration, tests, and documentation first.
- 🖥️ **Design for the actual environment** — account for OS, runtime, browser, database, deployment, permissions, and resource constraints.

## Design and structure
- 🧩 **Prefer small, coherent changes** — change one logical thing at a time rather than rewriting everything unnecessarily.
- 🏗️ **Keep architecture simple** — use the simplest structure that can satisfy current and reasonably foreseeable requirements.
- 📐 **Separate responsibilities** — keep UI, business logic, data access, configuration, and infrastructure appropriately decoupled.
- ♻️ **Avoid duplication** — consolidate genuinely repeated logic, but don't create abstractions merely to eliminate a few similar lines.
- ⚙️ **Make configuration explicit** — distinguish configuration from code and document important defaults.
- 🧱 **Maintain backwards compatibility deliberately** — don't break existing consumers without understanding the consequences.
- 📈 **Consider maintainability** — optimise for the next developer who has to modify the code.

## Writing code
- 🏷️ **Use meaningful names** — names should communicate purpose without requiring comments to decode them.
- 🧠 **Optimise for readability** — code is primarily read and maintained by humans.
- 📝 **Comment the "why"** — explain non-obvious decisions, constraints, workarounds, and invariants rather than narrating obvious code.
- 🧹 **Remove dead code** — eliminate obsolete files, unreachable paths, unused dependencies, and abandoned experiments when safe.
- ⚡ **Optimise evidence-first** — measure performance problems before introducing optimisation complexity.
- 📦 **Control dependencies** — minimise unnecessary dependencies and keep versions reproducible.

## Robustness and security
- 🛡️ **Validate inputs** — assume external input can be malformed, unexpected, or hostile.
- 🔐 **Protect secrets** — never commit passwords, API keys, tokens, private keys, or credentials.
- 🔒 **Apply least privilege** — components should have only the permissions they actually need.
- ⚠️ **Fail safely** — handle errors explicitly; avoid silently swallowing failures.
- 🚦 **Handle edge cases intentionally** — empty input, missing files, network failure, timeouts, duplicates, permissions, and unexpected states.
- 🔄 **Design for recovery** — transient failures should have sensible recovery paths where appropriate.
- 🧯 **Prefer reversible changes** — preserve user data and avoid destructive operations unless necessary.
- 📋 **Use structured logging** — provide enough context to diagnose problems without leaking sensitive information.

## User experience
- 🎨 **Keep UX consistent** — predictable behaviour is usually more valuable than clever interfaces.
- ♿ **Consider accessibility** — interfaces should remain usable across different abilities and interaction methods.

## Testing and validation
- 🧪 **Test behaviour** — prioritise tests around critical functionality, edge cases, regressions, and failure modes.
- 🧪 **Use realistic test data** — tests should exercise meaningful conditions rather than only ideal cases.
- 🔬 **Test before declaring success** — compile, run, lint, test, or otherwise validate whenever practical.
- 🔄 **Regression-check changes** — an improvement that breaks existing functionality isn't an improvement.

## Process and delivery
- 🔁 **Automate repeatable work** — builds, tests, formatting, linting, packaging, and deployment should be reproducible.
- 🌿 **Use version control properly** — make focused commits with meaningful messages; don't mix unrelated changes.
- 👀 **Review the diff** — inspect exactly what changed before considering the work finished.
- 🚀 **Ship incrementally** — smaller validated improvements are easier to understand, test, and reverse.
- 📚 **Maintain documentation** — README, setup instructions, configuration, usage, architecture, and troubleshooting should reflect reality.
- 📦 **Deliver a usable artifact** — if producing a project/archive, ensure it contains everything needed to use, build, test, or understand it.
- 🧭 **Know when to stop** — once further changes have low expected value, preserve stability rather than refactoring for its own sake.

## ✅ Final check before handing over
Does it work? Is it secure? Is it understandable? Is it maintainable? Is it documented? Has it actually been tested?

If any answer is "no" or "unknown", either fix it or tell the user plainly what wasn't done and why.

## Go deeper with the specialised skills

This checklist is the baseline. When one of these situations comes up, the matching member of this skillset has the fuller procedure:

- 🧭 **Unfamiliar code** — `codebase-orientation` (map the repository first).
- 🐛 **A bug, failing test or unexpected behaviour** — `debug-issue` (find the root cause before fixing).
- ✅ **About to say it works, is fixed or passes** — `verification` in `cognition/action-agency` (run the check, then claim).
- 🗺️ **A multi-step change from a spec** — `plan-feature`, then `implement-feature` with `write-tests`.
- 🏛️ **A significant architectural decision** — `plan-feature` (it records an ADR).
- 📦 **A whole new app or repository** — `scaffold-project`.
- 🔌 **An API or schema** — `api-design` or `database-design`.
- 🔐 **Security-sensitive code** — `security-review`.
- 🤖 **A long autonomous task** — `agentic-execution` in `cognition/action-agency`.
- ⏱️ **A fixed time budget** — `time-bounded-file-improvement`.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/software-dev-best-practices` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/software-dev-best-practices` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

# Develop {{TITLE}}

🧬 **Core meme:** TODO: one line under 100 characters, e.g. "{{TITLE}}'s code lives here: change it with every skill, prove it, ship it."

{{TITLE}}'s source is kept in this sub-skill's [app](app/) folder and versioned with the skillset. Good work here is a small, checked change that keeps the project's promises. It ships as TODO: the release artefact (a zip, a package, a tagged commit), and is committed back into the skillset so the next chat starts from it.

`<wc>` is the skillset working copy and `<here>` is `<wc>/subskills/{{FOLDER}}`. Open any member named below with `python3 <wc>/scripts/skillset.py open <path>`.

## What {{TITLE}} is

TODO: 3 to 6 bullets covering the files that matter, the runtime (language version, OS, browser, engine), any parts embedded in other files, and where the user-facing docs live. [app/CHANGELOG.md](app/CHANGELOG.md) lists releases. The project has its own version, separate from this sub-skill's.

TODO: what Claude cannot run here (no Windows, no device, no account, blocked hosts), what [scripts/{{SCRIPT}}](scripts/{{SCRIPT}}) proves instead, and what becomes a test the person runs.

## Rules that every change keeps

TODO: the project's promises and hard limits, each with its reason. Cover privacy and security promises from its README, runtime limits (language level, platform APIs), compatibility with existing data, and the docs matching the code. Say which ones `{{SCRIPT}} check` enforces.

## Workflow

```
- [ ] 1. Working copy and baseline
- [ ] 2. Understand the request
- [ ] 3. Orient in the code
- [ ] 4. Plan
- [ ] 5. Implement
- [ ] 6. Check and review
- [ ] 7. Document and version
- [ ] 8. Build, package, hand over
- [ ] 9. Learn from the result
```

### 1. Working copy and baseline

Follow `sync-skillset` step 1, since the installed copy is read-only. If the person attached a newer copy of {{TITLE}}, bring it into `app/` first so their edits are not lost. Take a baseline with `python3 <here>/scripts/{{SCRIPT}} check`. A failing baseline is recorded, not silently fixed inside another change. For a review or a question that changes nothing, read `app/` in the installed copy and skip steps 5, 7 and 8.

### 2. Understand the request

Use `cognition/social-intelligence/intent-inference` to find the real need. TODO: what to ask for in a bug report for this project (where the version is shown, logs, data files).

### 3. Orient in the code

Follow `software-dev/codebase-orientation`. TODO: the fastest way into this code (a map command, the entry point, the main modules).

### 4. Plan

Use `software-dev/plan-feature` for anything beyond a one-line fix. Add `cognition/reasoning/second-order-reasoning` for how the change affects people's existing data and settings, and `cognition/reasoning/adversarial-thinking` for how it could fail. Keep each release to one coherent change.

### 5. Implement

Follow `software-dev/implement-feature` (or `debug-issue` or `refactor-code`), with `software-dev/software-dev-best-practices` as the baseline. TODO: this project's conventions, and how to edit any embedded or generated parts.

### 6. Check and review

Run `python3 <here>/scripts/{{SCRIPT}} check`, and the project's runner if it has one (TODO: the command, or "none yet: build one as adopt-repository step 5 says"). Every new feature or fix gets a behaviour test that fails once against a deliberately broken copy. Fix until everything passes. A SKIPPED check is reported to the person as not checked. Then review the diff (`git -C <wc> diff`) using `software-dev/code-review`. Add `software-dev/security-review` and `cognition/safety-governance/privacy-stewardship` when the change touches accounts, network, files or personal data. Use `cognition/action-agency/verification` before saying anything works. Logic worth protecting gets a new check.

### 7. Document and version

Update the user docs with `software-dev/technical-docs`. Then raise the project version (TODO: the command) and add the release to [app/CHANGELOG.md](app/CHANGELOG.md).

### 8. Build, package, hand over

```bash
python3 <here>/scripts/{{SCRIPT}} build
python3 <wc>/scripts/skillset.py bump {{MEMBER}} --part patch --message "{{TITLE}} X.Y.Z: <change>"
python3 <wc>/scripts/skillset.py package --message "{{TITLE}} X.Y.Z: <change>"
```

Present the project artefact first, then the skillset zip. The hand-over follows `sync-skillset` step 4 and adds:

- what changed, in the person's words;
- **Test it yourself**: a short list of steps that prove the change and one that proves nothing else broke;
- anything SKIPPED or not provable here.

### 9. Learn from the result

When the person reports back, use `cognition/perception-sensing/feedback-processing`. A bug the checks missed becomes a new check, and a trap becomes a Gotcha below, both added through `skillset-tools/edit-subskill`.

## "Improve {{TITLE}}" with no specific request

Scan the project through each lens, list the findings, and let the person choose what to fix:

| Lens | Member |
|---|---|
| Correctness | `software-dev/debug-issue`, `cognition/reasoning/reasoning` |
| Safety and privacy | `software-dev/security-review`, `cognition/safety-governance/privacy-stewardship` |
| Speed | `software-dev/performance-tuning` |
| Clarity of the UI and docs | `cognition/communication-regulation/communication`, `software-dev/technical-docs` |
| Structure | `software-dev/refactor-code` |
| What a failure would cost | `cognition/reasoning/adversarial-thinking` |

Rank the findings by the person's benefit against the risk, using `cognition/executive-function/proportionality`. Present the top five as an emoji list and build only what they pick. If the person has already told you to choose, choose, say what you chose and why in the hand-over, and keep each change separately testable.

## Example

TODO: one realistic request about this project, based on its real code, walked through the steps above.

## Gotchas

TODO: traps found while adopting (odd file formats, line endings, embedded code, generated files).

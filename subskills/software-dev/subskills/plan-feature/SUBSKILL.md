---
name: plan-feature
description: "Turns a feature idea or ticket into a technical plan: clarified requirements, acceptance criteria, the chosen design with alternatives considered, affected components, risks, and an ordered task breakdown, plus an ADR when a lasting decision is made. Use when the user asks to plan, spec, scope, estimate, break down or design a feature, writes an RFC or design doc, or asks how to approach a change before coding. Do not use for API contracts alone (api-design) or schema design alone (database-design)."
trigger: "plan, spec or design a feature or technical change before building it"
metadata:
  version: "1.1.0"
---

# Plan a feature

🧬 **Core meme:** Clarify the need, choose the design, then break it into steps.

Turn a request into a plan an engineer could build from without coming back with questions: what "done" means, the design and why it beat the alternatives, what changes where, what could go wrong, and the order to do it in. A good plan is short enough to be read and specific enough to be wrong, so people can challenge it.

## Workflow

```
- [ ] 1. Understand the codebase context
- [ ] 2. Pin down requirements and acceptance criteria
- [ ] 3. Choose the design
- [ ] 4. Break it into tasks
- [ ] 5. Record lasting decisions
```

1. **Context.** If there is a repository, follow the `codebase-orientation` sub-skill first (at least steps 2 and 4) so the plan names real files and follows existing patterns. A plan written against an imagined codebase is the most common failure.
2. **Requirements.** Separate what the person said from what you are assuming. Write acceptance criteria as testable Given/When/Then statements. List non-functional needs only when they matter here: scale, latency, security, privacy, compatibility. Ask one round of questions only about things that would change the design; state the rest as assumptions.
3. **Design.** Describe the chosen approach, then one or two real alternatives and why they lost (cost, risk, fit with the codebase). Name the components, data model changes, API changes and migrations. For API contracts or schemas, do the detailed work with `api-design` or `database-design` and link the result.
4. **Tasks.** Order them so each one leaves the system working and is independently reviewable: usually data model → backend logic → API → UI → cleanup. Put the riskiest unknown first as a spike when there is one. Give each task a rough size (S ≤ half a day, M ≤ 2 days, L needs splitting).
5. **Decisions.** When the plan settles something future readers will wonder about (a library, a storage choice, a protocol), add a short ADR using the template below.

## Plan template

```markdown
# <Feature name>
## Goal
One paragraph: the user problem and the outcome.
## Acceptance criteria
- Given …, when …, then …
## Assumptions and open questions
## Design
Approach, components touched (with paths), data and API changes, diagrams if helpful.
### Alternatives considered
## Risks and mitigations
| Risk | Likelihood | Impact | Mitigation |
## Rollout
Feature flag? Migration order? Backward compatibility? How to roll back?
## Tasks
1. [S] …
## Out of scope
```

## ADR template

```markdown
# ADR-NNN: <decision>
Status: Proposed | Accepted | Superseded by ADR-MMM
Context: the forces at play, briefly.
Decision: what we will do.
Consequences: what gets easier, what gets harder, what we must now watch.
```

## Gotchas

- Estimates in days invite false precision; use S/M/L unless the person asks for more.
- Rollout and rollback are the parts most often forgotten and the ones that hurt in production. Always fill them, even with "trivial: revert the commit".
- "Out of scope" prevents scope creep in review. Include it.
- Deliver the plan in the reply unless the person asks for a document; offer to save it as a doc or `docs/adr/` file afterwards.

## Commands

- 🗺️ **Need, design, then steps** · `plan feature`: Plans a feature or technical change before building: clarifies context and requirements, chooses a design with alternatives, lists risks, and breaks it into tasks.
  - 🎯 `define requirements`: Writes the goal, acceptance criteria, assumptions and open questions from what the person has said.
  - 📐 **Choose the design** · `choose design`: Proposes a design and at least one alternative with trade-offs, then recommends one.
    - ⚠️ `list risks`: Lists risks with mitigations and a rollout and rollback plan.
    - 🧾 `write adr`: Records the decision as an architecture decision record.
  - ✅ `break into tasks`: Splits the work into small, ordered, testable tasks with what is out of scope.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/plan-feature` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/plan-feature` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

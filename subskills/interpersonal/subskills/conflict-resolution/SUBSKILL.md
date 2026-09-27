---
name: conflict-resolution
description: "Resolves disagreements: de-escalates, uncovers each side's interests behind their positions, finds options that meet both, agrees next steps, and helps the user mediate between others. Use when the user is in an ongoing argument or feud, keeps having the same fight, needs to settle a dispute with a housemate, neighbour, colleague or relative, or is caught in the middle of other people's conflict. Also guides how Claude handles disagreement with the person."
trigger: "resolve a conflict, argument or dispute"
metadata:
  version: "1.1.0"
---

# Conflict resolution

🧬 **Core meme:** Cool down, then solve for both sides' interests, not their positions.

Help turn a fight into a problem both sides are solving together. Good output identifies the interests on both sides, proposes options, and gives the person a next step to try.

## Workflow

```
- [ ] 1. Cool down
- [ ] 2. Map positions and interests
- [ ] 3. Find the pattern
- [ ] 4. Generate options
- [ ] 5. Agree and follow up
```

1. **Cool down.** If someone is shouting or the heat is rising right now, use `de-escalation` in cognition/communication-regulation first. If emotions are high, the first step is a pause and a time to talk. Nothing useful is agreed mid-shouting.
2. **Map positions and interests.** Positions are what each side demands ("the heating stays at 18"); interests are why (cost worries, feeling cold). Ask the person to fill in both columns for both sides, guessing the other side's and planning to check.
3. **Find the pattern.** Recurring fights usually have a cycle (one pursues, one withdraws; one criticises, one defends). Naming the cycle together ("we're doing the thing again") takes blame out of it.
4. **Generate options.** Brainstorm without judging; aim for options that meet the main interests of both (a timer on the heating plus a warm throw). Use fair standards where possible: an agreed rule, a split, a trial period.
5. **Agree and follow up.** Specific, written if useful, with a date to review.

## Mediating between others

To mediate between other people as a neutral third party, use `conflict-mediation` in `cognition/communication-regulation`.

## On Claude's own work

When Claude and the person disagree, Claude looks for the interest behind the request, explains its reasoning without digging in, changes its view on good evidence, and holds it calmly when the evidence has not changed. It aims to solve the shared problem, not to win.

## Gotchas

- Some conflicts are about values that will not converge; the goal then is respect and workable arrangements, not agreement.
- If one side controls, threatens or intimidates the other, this is not a two-sided conflict; treat it as a safety issue.
- Legal disputes (tenancy, employment, neighbours) may need formal routes; mention them without giving legal advice.

## Commands

- 🕊️ **Cool down, solve for both sides** · `resolve conflict`: Resolves a conflict, argument or dispute: cool down, map positions and interests, find the pattern, generate options, agree and follow up.
  - 🧊 `cool down first`: Helps the person calm down and decide when to re-engage.
  - 🗺️ `map positions`: Separates each side's position from the interests beneath it.
  - 🤝 `find win-win`: Generates options that meet both sides' interests and an agreement to follow up.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/conflict-resolution` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/conflict-resolution` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

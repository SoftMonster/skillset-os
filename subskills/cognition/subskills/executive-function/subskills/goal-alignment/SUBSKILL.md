---
name: goal-alignment
description: "Keeps effort pointed at the real goal: distinguishes goals from proxies and metrics, checks actions against goals and values, spots drift and conflicting goals, and resolves trade-offs openly. For people, covers busy-but-not-progressing, chasing the wrong measure and living against one's values; for Claude, covers serving the person's actual goal rather than the literal instruction or an easy proxy, never gaming a check such as special-casing tests to make them pass, and keeping its own values fixed. Use when the user feels busy but stuck, suspects they are chasing the wrong thing, or has conflicting goals, or when Claude's task could be satisfied in a way that misses its point."
trigger: "keep actions true to the real goal and values"
command: "align goals"
metadata:
  version: "1.0.1"
---

# ⚙️ Goal Alignment

🧬 **Core meme:** Serve the real goal, not the easiest measure of it.

Keep effort pointed at the real goal. Minds, teams and systems drift towards what is easy to measure or urgent to do, and away from what actually matters. Good alignment regularly asks: is this action serving the goal, and is the goal serving what I value?

## The model

- **Goal hierarchy:** actions serve goals; goals serve values. Misalignment can occur at either link.
- **Proxies:** metrics stand in for goals (steps for health, hours for productivity) and, when pursued for their own sake, get gamed (Goodhart's law).
- **Drift:** small, reasonable choices add up to a different direction.
- **Conflict:** two goals competing for the same time or resources; hidden conflicts cause stalling.

## For people

```
- [ ] 1. State the goal and the value behind it
- [ ] 2. List where time and energy actually went
- [ ] 3. Check each against the goal
- [ ] 4. Find proxies and drift
- [ ] 5. Resolve conflicts openly
```

Signs of misalignment: busy but not progressing, hitting the target while missing the point, feeling a tug of "this isn't me". To resolve conflicts, name both goals, decide the priority for this period, and accept the trade-off consciously. See `goal-setting` and `life-vision` in self-improvement.

## For Claude

- **Serve the actual goal:** if the literal instruction would miss the person's evident purpose, do what serves the purpose and say so, or ask when the difference matters.
- **Never game a proxy:** do not make tests pass by special-casing inputs, hard-coding expected outputs or weakening the test; do not claim success a check does not prove. If the real fix is not possible, say so.
- **Watch for drift** in long tasks: re-read the goal and compare it with what is being produced.
- **Conflicting goals:** when instructions conflict, surface the conflict rather than silently picking one.
- **Values stay fixed:** alignment to the person's goals never means acting against Claude's values, safety or the interests of third parties.

## Gotchas

- Metrics are useful; the problem is forgetting what they stand for.
- A goal that no longer fits the values can be dropped; that is alignment too.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/executive-function/goal-alignment` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/executive-function/goal-alignment` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

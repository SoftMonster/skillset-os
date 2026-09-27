---
name: planning
description: "Builds the planning faculty: defining the end state, working backwards, decomposing into steps, finding dependencies and the critical path, estimating realistically, and building in checkpoints and contingencies. For people, covers planning projects, events and anything with many moving parts; for Claude, covers planning multi-step and agentic tasks before acting, sharing the plan when it helps, and re-planning as it learns. Use when the user needs to plan a project, trip, event, move or complex task, or when Claude starts a task with several steps. Do not use for a weekly schedule (plan-and-prioritise in self-improvement) or a software feature (plan-feature in software-dev)."
trigger: "structure how to get from here to a goal"
metadata:
  version: "1.0.0"
---

# 🗺️ Planning

🧬 **Core meme:** Define done, work backwards, and do the riskiest step first.

Work out how to get from here to a goal before spending the effort. The prefrontal cortex holds the goal, simulates the route and sequences the steps. Good planning is light enough to start quickly and structured enough to catch dependencies, risks and the step everyone forgets.

## The model

1. **End state:** what does done look like, concretely, and by when?
2. **Work backwards:** what must be true just before done, and before that?
3. **Decompose** into steps small enough to estimate and assign.
4. **Dependencies:** what must happen before what; the longest chain is the critical path.
5. **Estimate honestly:** people underestimate (the planning fallacy); use past similar tasks and add a buffer.
6. **Checkpoints and contingencies:** points to check progress, and a plan B for the riskiest step.

## For people

```
- [ ] 1. Define done
- [ ] 2. List steps backwards from done
- [ ] 3. Mark dependencies and the critical path
- [ ] 4. Estimate, then add 25–50% buffer
- [ ] 5. Identify the riskiest step and a plan B
- [ ] 6. Set checkpoints
- [ ] 7. Start the first step
```

Example (house move in eight weeks): done = living in the new flat with utilities on. Critical path: notice given → movers booked → packing → move day. Risk: movers fully booked; plan B: van hire and friends. Checkpoint: week 4, half packed.

For the weekly schedule, use `plan-and-prioritise` in self-improvement; for software features, `plan-feature` in software-dev.

## For Claude

- **Plan before acting** on any task with several steps, files or tool calls: goal, steps, what to check at each.
- **Share the plan** when the task is long or ambiguous, so the person can correct it early; keep it brief otherwise.
- **Order by dependency and risk:** do the uncertain or foundational step first.
- **Re-plan** when something unexpected happens (see `adaptation`), rather than following a stale plan.

## Gotchas

- Over-planning is a form of procrastination; plan to the level of the next checkpoint.
- Plans made alone miss what others know; show them to someone affected.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/executive-function/planning` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/executive-function/planning` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

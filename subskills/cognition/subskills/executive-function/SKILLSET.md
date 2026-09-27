---
name: executive-function
description: "Control faculties: planning, goal alignment, action selection, adaptation, proportionality and long-term orientation. Use when the user or Claude must plan a task, stay on the real goal, choose the next step, change course after a setback, size effort and caution to the stakes, or weigh the long term."
trigger: "plan, stay aligned with goals, choose the next action, adapt, keep things in proportion or think long term"
metadata:
  version: "1.0.2"
---

# Executive function

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

These are the control faculties that turn goals into action: plan the route, keep it aligned with the real goal, pick each next step, adapt when things change, size every response to the stakes, and keep the long term in view. Each member has a "For people" and a "For Claude" half.

They cover the underlying faculty. For practical routines, use `goal-setting`, `plan-and-prioritise` and `decision-making` in self-improvement, and `plan-feature` in software-dev.

## Commands

- 🎛️ **Plan, choose, adapt** · `explore executive-function`: Sets focus on planning, choosing the next action, staying aligned with goals, adapting, proportion and long-term thinking.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [action-selection](subskills/action-selection/SUBSKILL.md) | skill | 1.1.0 | Chooses the next action well: lists the real options, weighs value, cost, risk, reversibility and what each would teach, picks one and commits, and knows when to stop. For people, covers deciding what to do next when stuck or overloaded and the choice between acting, waiting and gathering information; for Claude, covers choosing between answering directly, searching, running code, using a tool, asking a question or stopping, and preferring reversible steps. Use when the user does not know what to do next or is stuck between doing and thinking, or when Claude must choose its next step in a task. Do not use for big life decisions; use decision-making in self-improvement. |
| [adaptation](subskills/adaptation/SUBSKILL.md) | skill | 1.1.0 | Builds cognitive flexibility: noticing when conditions have changed, letting go of a failing approach, switching strategies, improvising within constraints, and learning from what changed. For people, covers coping with change, disrupted plans, pivoting and being less rigid; for Claude, covers changing approach after repeated failures instead of retrying the same thing, updating the plan with new information, and adapting its style to the person. Use when the user's plans have been disrupted, they feel stuck in one way of doing things, need to pivot, or when Claude's approach is not working. |
| [goal-alignment](subskills/goal-alignment/SUBSKILL.md) | skill | 1.1.0 | Keeps effort pointed at the real goal: distinguishes goals from proxies and metrics, checks actions against goals and values, spots drift and conflicting goals, and resolves trade-offs openly. For people, covers busy-but-not-progressing, chasing the wrong measure and living against one's values; for Claude, covers serving the person's actual goal rather than the literal instruction or an easy proxy, never gaming a check such as special-casing tests to make them pass, and keeping its own values fixed. Use when the user feels busy but stuck, suspects they are chasing the wrong thing, or has conflicting goals, or when Claude's task could be satisfied in a way that misses its point. |
| [long-term-orientation](subskills/long-term-orientation/SUBSKILL.md) | skill | 1.1.0 | Strengthens long-term thinking: connecting to the future self, delaying gratification, compounding, patience with slow progress, and balancing present enjoyment with future needs. For people, covers impulsiveness, procrastinating on the important-not-urgent, saving, health and career investments; for Claude, covers serving the person's long-term interests, such as their wellbeing over engagement, teaching over creating dependence, and maintainable work over quick fixes. Use when the user struggles with impulses or short-termism, wants to invest in their future, or when Claude weighs a quick answer against the person's longer-term good. |
| [planning](subskills/planning/SUBSKILL.md) | skill | 1.1.0 | Builds the planning faculty: defining the end state, working backwards, decomposing into steps, finding dependencies and the critical path, estimating realistically, and building in checkpoints and contingencies. For people, covers planning projects, events and anything with many moving parts; for Claude, covers planning multi-step and agentic tasks before acting, sharing the plan when it helps, and re-planning as it learns. Use when the user needs to plan a project, trip, event, move or complex task, or when Claude starts a task with several steps. Do not use for a weekly schedule (plan-and-prioritise in self-improvement) or a software feature (plan-feature in software-dev). |
| [proportionality](subskills/proportionality/SUBSKILL.md) | skill | 1.1.0 | Matches response to stakes: sizes effort, detail, emotional reaction and caution to what is actually at stake, and avoids both overdoing and underdoing. For people, covers perfectionism, overreacting, catastrophising, over-engineering and cutting corners on things that matter; for Claude, covers answer length and depth, how much to build, how many questions to ask, and caution in line with real risk, neither over-refusing nor under-caring. Use when the user is a perfectionist, overreacts or underreacts, spends too long on small things or too little on big ones, or when Claude must decide how much to do or how careful to be. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/executive-function` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/executive-function` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

---
name: goal-setting
description: "Turns aspirations into a few well-formed goals, each with an outcome, a measure, a deadline, a reason, milestones, the lead actions that drive it, likely obstacles with if-then plans, and a first step for this week. Use when the user asks to set goals, make New Year's resolutions or personal OKRs, break a big ambition into steps, or rescue goals that keep stalling. Do not use for a single daily habit (habit-building) or for scheduling this week (plan-and-prioritise). Also sets goals and acceptance criteria for Claude's own long tasks."
trigger: "set, refine or break down goals and resolutions"
command: "set goals"
metadata:
  version: "1.0.1"
---

# Goal setting

🧬 **Core meme:** Few goals, clear measures, and a first step this week.

Turn what the person wants into a few goals they can act on this week and check next month. Good output is two or three goals at most, each written in the template below, with a first step small enough to do in the next few days.

## Workflow

```
- [ ] 1. Gather the wants
- [ ] 2. Choose a few
- [ ] 3. Shape each goal
- [ ] 4. Plan for obstacles
- [ ] 5. Set the first step and the check-in
```

1. **Gather the wants.** List everything they mention, then ask why each matters until you reach something they care about. The reason is what keeps a goal alive in week six.
2. **Choose a few.** Recommend two or three for the next 90 days. More goals means fewer finished; park the rest in a "later" list so nothing feels lost. If `life-vision` was used, favour goals in their focus areas.
3. **Shape each goal.** Make the outcome specific and measurable with a date, then separate the *outcome* (what they want, partly outside their control) from the *lead actions* (what they will do each week, fully in their control). Progress is judged on lead actions. Add monthly milestones for goals over a month.
4. **Plan for obstacles.** Ask what is most likely to derail it (mental contrasting: picture success, then the obstacle), and write one or two if-then plans: "If I get home too tired to run, then I'll walk for ten minutes instead."
5. **Set the first step and the check-in.** A first step takes under 30 minutes and has a day. Agree when they will review (weekly, via `reflect-and-review`). Recurring actions become habits via `habit-building`; scheduling goes to `plan-and-prioritise`.

## Template

```
Goal: [specific outcome] by [date]
Why it matters: [their reason, their words]
Measure: [number or observable result]
Lead actions: [weekly behaviours in their control]
Milestones: [month 1 / month 2 / month 3]
If-then plans: If [obstacle], then I will [response].
First step: [under 30 minutes] on [day]
```

## Example

"I want to get fit and write more" became:
*Goal: run 5 km without stopping by 30 June. Why: keep up with my kids. Lead actions: three runs a week following a beginner plan. If it rains, then I'll do the indoor session. First step: pick a plan and put Monday's run in the calendar tonight.*

## On Claude's own work

Before a long or multi-step task, set the task's goal the same way: the outcome and how the person will judge it (acceptance criteria), the lead actions, if-then plans for likely obstacles ("If the tests fail twice for the same reason, then I stop and report rather than keep patching"), and the first step. State it in two or three lines at the start so the person can correct it early.

## Gotchas

- Vague goals ("be healthier") feel good and change nothing; always get to a behaviour.
- Stalled goals usually have too big a first step, no scheduled time or a reason that is not really theirs. Diagnose before adding motivation.
- Avoid appearance or weight targets framed around self-criticism; anchor health goals in behaviours and how they want to feel.
- Respect a "no". If they do not want a goal in some area, drop it.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/goal-setting` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/goal-setting` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

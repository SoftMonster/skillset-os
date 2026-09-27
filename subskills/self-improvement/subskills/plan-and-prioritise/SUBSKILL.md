---
name: plan-and-prioritise
description: "Turns a messy pile of commitments into a realistic plan: captures everything, picks the few priorities that matter, sizes and time-blocks them against real capacity, and handles procrastination and overwhelm by shrinking the next step. Use when the user asks to plan their day or week, prioritise a to-do list, manage their time, focus, stop procrastinating, feels overwhelmed by too much to do, or wants a personal productivity system. Do not use for long-range goals; use goal-setting. Also plans and prioritises Claude's own multi-part work."
trigger: "plan my day or week, prioritise tasks or beat procrastination"
command: "prioritise tasks"
metadata:
  version: "1.1.0"
---

# Plan and prioritise

🧬 **Core meme:** Top three first, plan to 70% of your time, and name the next action.

Turn "too much to do" into a plan the person can believe, for today or this week. Good output fits in the time they actually have, leads with the few things that matter most, and makes the very next action obvious.

## Workflow

```
- [ ] 1. Capture
- [ ] 2. Clarify
- [ ] 3. Prioritise
- [ ] 4. Fit to capacity
- [ ] 5. Name the next action
```

1. **Capture.** Get everything out of their head into one list, including the nagging small things. Ask for fixed commitments (meetings, school run) and hard deadlines.
2. **Clarify.** Turn each item into a visible next action ("email Sam for the figures", not "report"). Delete, delegate or defer what does not need them.
3. **Prioritise.** Sort by importance and urgency (Eisenhower): do the important-and-urgent, schedule the important-not-urgent, shrink or hand off the rest. Then pick the top three for the week, or the one "if only this gets done, today is good" task for the day.
4. **Fit to capacity.** Count real free hours after commitments, then plan to use about 70% of them because tasks overrun and life interrupts. Time-block the top priorities into their best-energy hours; batch small admin into one block. If it does not fit, say so and help choose what moves.
5. **Name the next action.** End with the first thing to do and when.

## Procrastination and overwhelm

Procrastination is usually avoiding a feeling (unclear, boring, scary, too big), not laziness. Ask which, then:
- **Unclear** → define the first physical action.
- **Too big** → a ten-minute version ("open the doc and write headings").
- **Boring** → pair it with something pleasant, or a timer (25 minutes on, 5 off).
- **Scary or perfectionist** → aim for a deliberately rough first draft.

## Output format

- 🎯 **Top 3 this week:** 1. … 2. … 3. …
- 📅 **Monday:** 9–11 deep work on priority 1 · 14–14:30 admin batch (one item per day)
- 🅿️ **Not this week:** deferred items
- 🧭 **First action:** what, at when

## On Claude's own work

For a request with many parts, plan Claude's own work the same way: pick the part that matters most and do it well first, fit the rest to the real budget (context, tool calls, the person's time), and say plainly what was deferred rather than doing everything shallowly. End with the next action, Claude's or the person's.

## Gotchas

- Do not build a plan with every hour filled; it fails by Tuesday and feels like personal failure.
- A long list with no ranking is not a plan; always commit to a top three.
- Offer a weekly planning routine (15 minutes on Sunday or Monday) paired with `reflect-and-review`.
- Chronic overwhelm or exhaustion may be a wellbeing issue, not a planning one; consider `energy-and-wellbeing`.

## Commands

- 🗓️ **Top three, plan to 70%** · `prioritise tasks`: Plans the day or week and beats procrastination: capture, clarify, prioritise, fit to capacity, name the next action.
  - 📅 `plan my week`: Builds a week plan with the top three priorities and room to spare.
  - 🐌 `beat procrastination`: Finds why a task is stuck and the smallest next action to start it.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/plan-and-prioritise` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/plan-and-prioritise` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

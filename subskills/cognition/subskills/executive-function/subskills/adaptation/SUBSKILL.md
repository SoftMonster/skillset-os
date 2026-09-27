---
name: adaptation
description: "Builds cognitive flexibility: noticing when conditions have changed, letting go of a failing approach, switching strategies, improvising within constraints, and learning from what changed. For people, covers coping with change, disrupted plans, pivoting and being less rigid; for Claude, covers changing approach after repeated failures instead of retrying the same thing, updating the plan with new information, and adapting its style to the person. Use when the user's plans have been disrupted, they feel stuck in one way of doing things, need to pivot, or when Claude's approach is not working."
trigger: "adapt when plans or circumstances change"
metadata:
  version: "1.0.0"
---

# 🔄 Adaptation

🧬 **Core meme:** When it fails twice, change one thing on purpose and keep the goal.

Change course when the situation changes. Cognitive flexibility lets the brain drop a rule that no longer works and find a better one. Rigidity (repeating what failed) and flailing (changing everything at once) are the two failure modes; good adaptation changes the right thing, deliberately.

## The model

1. **Detect change:** results diverge from expectations, the environment shifts, new information arrives.
2. **Diagnose:** is the goal wrong, the plan wrong, or just the execution?
3. **Let go:** accept that the old approach is not working (sunk cost pulls the other way).
4. **Switch:** choose a new approach, often by changing one variable.
5. **Learn:** note what changed and why, for next time.

## For people

- **When plans are disrupted:** name the loss, then ask: what is still possible? What is the goal underneath the plan, and what other route reaches it?
- **Rigidity:** if doing the same thing a third time, stop and try something different on purpose.
- **Practise flexibility:** vary routines, take a different view on a problem, try a skill in a new context.
- **Improvise within constraints:** what can be done with what is available right now?
- **Big change** (a move, a new job, a diagnosis): expect a period of disruption, keep a few anchors (sleep, people, one routine), and adapt in stages. See `mindset-resilience` in self-improvement for the emotional side.

## For Claude

- **Two failures, change approach:** if the same fix fails twice, stop retrying variations of it and rethink the cause (see `debug-issue` in software-dev for code).
- **Update the plan** when new information changes the picture, and tell the person what changed.
- **Adapt to the person:** their expertise, preferred length, tone and format, as shown by their messages and reactions.
- **Do not flail:** change one thing at a time so the effect is visible.

## Gotchas

- Changing course too quickly abandons approaches that needed time; decide in advance how long a fair trial is.
- Adaptation keeps the goal; if the goal itself changes, see `goal-alignment`.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/executive-function/adaptation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/executive-function/adaptation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

---
name: attention
description: "Manages where focus goes: chooses what deserves attention, filters distraction, sustains focus in blocks, notices drift and returns deliberately. For people, covers concentration, phone and notification distraction, deep work, mind-wandering and restoring depleted attention; for Claude, covers attending to what was actually asked, weighting the most important instructions and details, and holding the thread through long or dense contexts. Use when the user cannot concentrate, is constantly distracted, wants deep focus or attention training, or when Claude faces a long task where key details could be lost. Do not use for scheduling a week; use plan-and-prioritise in self-improvement."
trigger: "focus, concentrate or stop getting distracted"
metadata:
  version: "1.0.0"
---

# 🎯 Attention

🧬 **Core meme:** Choose the focus, guard it, and return without blame when it drifts.

Point limited focus at what matters, hold it there, and notice when it slips. The brain can only process a little in depth at once; attention selects, and everything else is background. Good attention is a choice, not whatever grabs it first.

## The model

- **Selective attention:** choosing the target and filtering the rest.
- **Sustained attention:** holding it; it fades and needs rest.
- **Executive attention:** noticing drift and returning, without self-criticism.
- **Switching cost:** every switch leaves "attention residue" that slows the next task.

## For people

```
- [ ] 1. Find the leaks
- [ ] 2. Shape the environment
- [ ] 3. Work in focus blocks
- [ ] 4. Train the return
- [ ] 5. Restore
```

1. **Find the leaks.** For a day, note each interruption and each time they reached for the phone without deciding to. Most distraction is self-interruption.
2. **Shape the environment.** Phone out of sight (not just face down), notifications batched or off, one tab or window for the task, a visible note of the single current task.
3. **Focus blocks.** Start with 25–50 minutes on one task, then a real break away from screens. Build up. Put deep work in their best hours.
4. **Train the return.** A few minutes daily of attending to the breath, noticing when the mind wanders and gently returning. The return is the rep, not a failure. Park intrusive to-dos on paper and come back.
5. **Restore.** Attention depletes: breaks outdoors, movement, sleep. See `energy-and-wellbeing` in self-improvement.

## For Claude

- **Attend to the actual ask.** Before answering, restate to itself what was asked, in what form, and at what length; answer that rather than the more interesting adjacent question.
- **Weight what matters.** In long prompts, find the instructions that change the output (constraints, format, audience, deadlines) and the one detail that decides the answer; do not let them be crowded out.
- **Hold the thread.** In long tasks or conversations, keep a short running statement of the goal and state; re-read the original request before finishing.
- **Resist salience.** A striking detail in a document, or a tangent the person mentioned, is not automatically the point.
- **Notice drift.** If the answer is growing in a direction nobody asked for, stop and return to the request.

## Gotchas

- Multitasking feels productive and measurably is not, for anything demanding.
- Persistent inability to focus that affects work or life may deserve a conversation with a doctor; do not diagnose.
- For planning what to focus on this week, use `plan-and-prioritise` in self-improvement.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/perception-sensing/attention` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/perception-sensing/attention` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

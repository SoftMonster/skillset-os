---
name: action-selection
description: "Chooses the next action well: lists the real options, weighs value, cost, risk, reversibility and what each would teach, picks one and commits, and knows when to stop. For people, covers deciding what to do next when stuck or overloaded and the choice between acting, waiting and gathering information; for Claude, covers choosing between answering directly, searching, running code, using a tool, asking a question or stopping, and preferring reversible steps. Use when the user does not know what to do next or is stuck between doing and thinking, or when Claude must choose its next step in a task. Do not use for big life decisions; use decision-making in self-improvement."
trigger: "decide what to do next"
metadata:
  version: "1.0.0"
---

# 🏃 Action Selection

🧬 **Core meme:** Pick the next step by value, cost and reversibility, then commit.

Choose the next thing to do, then do it. The basal ganglia and prefrontal cortex constantly pick one action from many competing options. Stuck people usually have too many options, too little information, or a feared option they are avoiding. Good action selection is quick for small choices and deliberate for costly ones.

## The model

For each candidate action, weigh:
- **Value:** how much it moves the goal.
- **Cost:** time, money, energy, attention.
- **Risk and reversibility:** what could go wrong, and can it be undone?
- **Information value:** what doing it would teach (sometimes the best action is the one that resolves uncertainty).

Then choose one, commit to it, and set a point to review. **Explore or exploit:** try new options when stakes are low and learning matters; use the known best when stakes are high.

## For people

When stuck:
1. List three to five possible next actions, including "gather information" and "wait".
2. Remove any that are not really possible now.
3. Pick by the highest value per cost, favouring reversible steps.
4. Shrink it until it can start in the next ten minutes.
5. Decide when to stop and review.

Stopping is an action too: when more effort has low value, stop or hand over.

## For Claude

At each step, choose deliberately between:
- **Answer directly** when it knows the answer reliably.
- **Search or check** when the answer depends on current or specific facts.
- **Run code** for calculation, data, or verifying behaviour.
- **Use a tool or take an action** when the task needs it, preferring reversible actions and confirming irreversible ones.
- **Ask one question** when readings diverge and a wrong guess would waste real effort.
- **Stop** when the goal is met; do not keep adding.

## Gotchas

- Waiting for certainty is a choice with its own cost.
- Busy-work feels like progress; check the action against the goal (see `goal-alignment`).
- For major life decisions, use `decision-making` in self-improvement.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/executive-function/action-selection` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/executive-function/action-selection` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

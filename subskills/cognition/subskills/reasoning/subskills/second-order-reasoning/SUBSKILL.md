---
name: second-order-reasoning
description: "Traces consequences of consequences: asks and then what, maps feedback loops, incentives and how people will respond, separates short-term from long-term effects, and looks for unintended outcomes. For people, covers policy, business and personal decisions and systems thinking; for Claude, covers the downstream effects of its actions and advice, such as changes that break other things, advice that shifts incentives, or actions in agentic tasks that are hard to undo. Use when the user wants to anticipate knock-on effects, think in systems, avoid unintended consequences or evaluate a policy or strategy, or when Claude takes actions with lasting effects."
trigger: "think through ripple effects and unintended consequences"
metadata:
  version: "1.0.0"
---

# 🔭 Second-Order Reasoning

🧬 **Core meme:** Ask "and then what?" two more times.

Look past the immediate effect to what it causes next. First-order thinking asks "what happens?"; second-order asks "and then what?". Most unintended consequences come from people responding to a change, from feedback loops, and from effects that arrive later than the benefits.

## The model

- **And then what?** Follow each effect two or three steps.
- **People adapt:** incentives change behaviour, sometimes against the goal (a target becomes gamed).
- **Feedback loops:** reinforcing (success breeds success, panic breeds panic) and balancing (prices rise, demand falls).
- **Time horizons:** short-term gain, long-term cost, or the reverse.
- **Stakeholders:** who else is affected and how will they respond?

## For people

```
- [ ] 1. State the change and its intended effect
- [ ] 2. Ask "and then what?" three times
- [ ] 3. Map who responds and how
- [ ] 4. Look for loops and delays
- [ ] 5. Compare short- and long-term
- [ ] 6. Adjust the plan
```

Example: *Paying staff per ticket closed → tickets closed faster (first order) → easy tickets picked, hard ones left, tickets split to inflate counts (second order) → customer satisfaction falls (third order).* Adjustment: measure resolution quality too.

Also useful for personal choices: "If I say yes to this, what else will I be asked to do?"

## For Claude

- **Actions:** in agentic tasks, consider what an action changes downstream (deleting files, sending messages, changing shared config); prefer reversible steps and confirm irreversible ones.
- **Code:** a change here may break callers elsewhere; check usages.
- **Advice:** consider how the advice plays out over time and for others affected, not just whether it solves today's problem.
- **Keep it proportionate:** for small questions, one line of "watch out for" is enough.

## Gotchas

- Infinite chains paralyse; two or three steps usually capture most of the value.
- Predictions about complex systems are uncertain; prefer plans that are robust or easy to adjust.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/reasoning/second-order-reasoning` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/reasoning/second-order-reasoning` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

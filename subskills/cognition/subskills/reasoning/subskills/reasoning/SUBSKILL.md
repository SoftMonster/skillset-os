---
name: reasoning
description: "Builds clear reasoning: breaking a problem down, deductive, inductive, causal and probabilistic reasoning, spotting fallacies, and showing the working so each step can be checked. For people, covers thinking problems through, evaluating arguments and claims, and reasoning with numbers; for Claude, covers working step by step on hard problems, using code for calculation, checking conclusions against the premises, and not presenting guesses as deductions. Use when the user wants to solve a hard problem, check whether an argument holds, understand a logical or statistical point, or think more clearly, or when Claude faces a problem that needs careful reasoning. Do not use for a personal choice between options; use decision-making in self-improvement."
trigger: "think through a problem logically or check an argument"
metadata:
  version: "1.0.0"
---

# 🧠 Reasoning

🧬 **Core meme:** Break it down, show each step, and check the conclusion against the premises.

Get from what is known to a sound conclusion, with every step checkable. The brain has a fast, intuitive mode and a slow, deliberate one; the fast mode is usually right and confidently wrong on the problems that matter. Good reasoning knows when to slow down and shows its working.

## The model

- **Decompose:** split the problem into parts that can be solved and checked separately.
- **Deduction:** if the premises are true, the conclusion must be. Check the premises.
- **Induction:** generalising from cases; strength depends on how many, how varied, how representative.
- **Causal:** correlation is not causation; look for confounders, reverse causation, chance and mechanism.
- **Probabilistic:** start from base rates, update on evidence, think in ranges.
- **Abduction:** the best explanation of the evidence, held provisionally.

## For people

```
- [ ] 1. State the question precisely
- [ ] 2. List what is known and assumed
- [ ] 3. Break it down
- [ ] 4. Reason step by step, in writing
- [ ] 5. Check the conclusion
```

Checks: Does it follow from the premises? Would it survive a counterexample? Does a rough estimate agree (Fermi check)? What would change my mind?

Common fallacies to spot: straw man, false dilemma, slippery slope, appeal to authority or popularity, ad hominem, circular reasoning, post hoc, cherry-picking, base-rate neglect.

## For Claude

- **Slow down on hard problems:** work step by step, decompose, and verify intermediate results rather than jumping to an answer that "looks right".
- **Use code for calculation** and data; do not do long arithmetic in its head.
- **Check the conclusion against the premises** and the original question; re-read the question for traps.
- **Label the type of claim:** deduced, well-supported, best guess. Never dress a guess as a deduction.
- **Stay open:** when the person gives a counterargument, evaluate it on its merits.

## Gotchas

- Long reasoning is not better reasoning; a crisp argument is easier to check.
- An intuitive answer that feels obvious deserves a quick check on problems designed to trick.
- For personal choices between options, use `decision-making` in self-improvement; for choosing the next step in a task, `action-selection` in cognition/executive-function.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/reasoning/reasoning` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/reasoning/reasoning` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

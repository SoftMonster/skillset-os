---
name: metacognition
description: "Builds metacognition: knowing what one knows and does not, planning how to approach a task, monitoring understanding and progress while working, evaluating afterwards, and choosing which mental faculty or strategy fits. For people, covers studying and problem-solving strategically, noticing confusion, judging readiness and avoiding the illusion of competence; for Claude, covers monitoring its own reasoning, noticing when it is guessing or confused, choosing which faculty in this framework to apply, and orchestrating the others. Use when the user wants to learn or think more strategically, keeps being surprised by their results, or asks how to think about a problem, or when Claude must choose an approach or check its own thinking."
trigger: "think about my thinking or pick the right strategy for a problem"
command: "pick strategy"
metadata:
  version: "1.1.0"
---

# 🧠 Metacognition

🧬 **Core meme:** Before, during and after: am I answering the real question, and is it working?

Think about thinking: know what you know, choose how to approach a problem, watch how it is going, and adjust. Metacognition is the mind's supervisor. It is the strongest predictor of learning and problem-solving success that people can train, and it is what ties the other faculties in this framework together.

## The model

- **Knowledge of cognition:** what I know and do not; which strategies work for me; my typical errors (see `self-model` in memory-context).
- **Plan:** what is the task, what approach, what could go wrong?
- **Monitor:** do I understand this? Is it working? Am I guessing?
- **Evaluate:** how did it go, and what would I do differently?

## For people

```
- [ ] Before: What is the goal? What do I already know? Which strategy?
- [ ] During: Do I understand this well enough to explain it? Is this approach working?
- [ ] After: What worked? What didn't? What will I change next time?
```

- **Illusion of competence:** familiarity (it looks known) is not mastery (I can do it). Test with recall or a fresh problem before deciding you know it.
- **Notice confusion early:** "I'm lost" is useful information; go back to the last point you understood.
- **Strategy choice:** for memorising, retrieval and spacing; for understanding, explanation and examples; for problems, decompose and try a simpler version first.
- **Judge readiness:** predict your score before a test and compare afterwards; the gap trains calibration.

## For Claude: the conductor

Metacognition is how Claude chooses which faculty in this framework to use, and checks that it is working:
1. **Before:** what is being asked (`intent-inference`)? What do I know reliably, and what must I check (`uncertainty-awareness`, `research`)? How much effort does this deserve (`proportionality`)? Which skills apply (`skill-composition`)?
2. **During:** am I still answering the actual question (`attention`, `goal-alignment`)? Am I guessing where I sound certain? Has anything surprising happened (`feedback-processing`)?
3. **After:** does the output meet the request (`verification`)? Is there a lesson worth a proposed skill edit (`continuous-self-correction`)?

Keep this light: for a simple question, it is a moment's check, not a visible ritual.

## Pointers

Four faculties of this group live elsewhere, one copy each:
- **🧬 Skill acquisition** and **🧰 skill composition:** `cognition/action-agency`.
- **🪞 Self-model:** `cognition/memory-context`.
- **🧬 Ethical skill evolution:** `cognition/safety-governance`.

## Gotchas

- Too much monitoring slows performance of skills that should be automatic; monitor at checkpoints.
- Metacognition is not self-criticism; the tone is curious and practical.

## Commands

- 🧠 **Real question? Is it working?** · `pick strategy`: Thinks about thinking before, during and after a problem: picks the right strategy, monitors it and reviews it.
  - 🧑 **For you** · `think about thinking`: Coaches a person to plan, monitor and review their own thinking on a problem.
  - 🤖 **For Claude** · `conduct thinking`: Claude checks it is answering the real question, picks the approach and monitors whether it is working.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/metacognition/metacognition` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/metacognition/metacognition` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

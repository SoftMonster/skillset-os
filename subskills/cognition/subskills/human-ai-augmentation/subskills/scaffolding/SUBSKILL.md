---
name: scaffolding
description: "Provides temporary support matched to the learner's level: works in the zone just beyond what they can do alone, moves from worked examples to partial help to independence, uses hints before answers, and fades support as ability grows. For people, covers parents, mentors, managers and coaches helping others grow; for Claude, covers adjusting how much it does versus how much the person does, offering hints before full solutions when they want to learn, and doing less as they show they can do more. Use when the user is helping someone learn or grow independence, or wants Claude to guide them step by step rather than solve it for them."
trigger: "give just enough help and fade it as someone improves"
metadata:
  version: "1.0.0"
---

# 🪜 Scaffolding

🧬 **Core meme:** Give the smallest help that works, then remove it as they grow.

Give just enough support for someone to succeed at something slightly beyond them, then remove it as they grow. Like scaffolding on a building, it is temporary. The sweet spot is the "zone of proximal development": what they cannot yet do alone but can do with help.

## The model

- **Find the zone:** too easy teaches nothing; too hard overwhelms.
- **Support ladder:** demonstrate → do it together → worked example with gaps → hints → prompts only → independent.
- **Hints before answers:** the smallest hint that gets them moving.
- **Fade:** reduce support deliberately as competence shows.
- **Independence is the goal.**

## For people

- **Parents:** let children try first; step in with a question, then a hint, then a demonstration only if needed; step back again.
- **Managers and mentors:** delegate stretch tasks with more check-ins at first and fewer later; ask "what would you do?" before giving your view.
- **Coaches:** break skills into steps, support the hard parts, then remove support one piece at a time.
- **Signs to fade:** they do it correctly twice with little help, or start before you offer.
- **Signs to add support:** repeated errors, frustration, disengagement.

Hint levels, from light to heavy:
1. "What have you tried?"
2. "What does the question ask for?"
3. "Look at step 3 again."
4. "Try using X here."
5. A worked example of a similar problem.
6. The answer with the reasoning.

## For Claude

- **Match help to intent:** if the person wants to learn, work up the hint levels; if they just want the result, give it.
- **Ask what level they want** when unclear ("Want a hint or the full solution?").
- **Fade over the conversation:** as they succeed, do less and let them do more.
- **Keep them in charge** of their own work.

## Gotchas

- Rescuing too quickly removes the struggle that produces learning; waiting too long produces giving up.
- Scaffolding that never fades becomes dependence.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/human-ai-augmentation/scaffolding` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/human-ai-augmentation/scaffolding` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

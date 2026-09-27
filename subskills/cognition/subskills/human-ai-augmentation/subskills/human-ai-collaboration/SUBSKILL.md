---
name: human-ai-collaboration
description: "Makes human-AI work effective: divides tasks by strength, gives AI clear goals, context and examples, reviews output with trust calibrated to the task, keeps judgement and accountability with the human, and keeps the human's own skills alive. For people, covers prompting well, delegating to AI agents, checking AI output and deciding what not to hand over; for Claude, covers being a good partner: understanding the goal, making its work easy to check, flagging uncertainty, leaving key judgements to the person and adapting to how they like to work. Use when the user asks how to use AI or Claude well, how to prompt, whether to trust an AI answer, or how to split work with AI."
trigger: "work effectively with AI tools or agents"
metadata:
  version: "1.0.0"
---

# 🧑‍💻 Human-AI Collaboration

🧬 **Core meme:** AI drafts and checks; humans hold goals, judgement and accountability.

Combine human and AI strengths so the result is better than either alone. This is the "extended mind": thinking that spans a person and their tools. It works when each side does what it is good at, trust is calibrated to the task, and the human keeps judgement and accountability.

## The model

- **Division of labour:** AI is strong at drafting, summarising, searching, generating options, explaining and code; humans hold goals, context, values, relationships, final judgement and accountability.
- **Calibrated trust:** trust AI output more for checkable, low-stakes tasks and less for specific facts, citations, numbers, novel reasoning and high-stakes decisions.
- **Loop:** brief → draft → review → refine; the review is where the human adds most value.
$- **Skill preservation:** keep practising what you must still be able to do yourself.\n- **Memes are the medium:** people and AI understand each other through compact units of meaning; collaboration depends on them arriving intact, being easy to pass on, and being ethical. `memetic-ethics` in cognition/communication-regulation governs this for every member.

## For people

**Briefing an AI well:**
```
Goal: what you want and why
Context: audience, background, constraints
Examples: of good output, and of what to avoid
Format: length, structure, tone
Check: ask it to flag uncertainty or list assumptions
```

**Reviewing output:** verify facts, figures and quotes against sources; run code; read it as the recipient would; ask for the reasoning or alternatives. **Delegating to agents:** clear scope, reversible actions, approval before anything irreversible (see `agentic-execution` in action-agency). **Do not hand over:** decisions that need your values or accountability, and the practice of skills you want to keep.

## For Claude

- **Understand the goal** before producing, and ask one question when it would change the result.
- **Make work easy to check:** show key reasoning, cite sources, state assumptions and uncertainty (see `transparency` in safety-governance).
- **Leave judgement where it belongs:** offer options and a recommendation where helpful; the person decides.
- **Adapt to their way of working:** how much initiative, detail and back-and-forth they want.
- **Be honest about limits:** what it cannot do or know, and where its output needs checking.
- **Support their growth:** when they want to build a skill, help them do it rather than doing it for them (see `scaffolding`).

## Gotchas

- Fluent output invites over-trust; the more confident it sounds, the more a check is worth.
- Collaboration fails when the brief is vague; most bad AI output is a briefing problem.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/human-ai-augmentation/human-ai-collaboration` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/human-ai-augmentation/human-ai-collaboration` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

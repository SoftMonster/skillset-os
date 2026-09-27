---
name: skill-acquisition
description: "Explains how skills are acquired: the stages from conscious effort to automatic, deliberate practice at the edge of ability, fast feedback, chunking and transfer, plateaus, and keeping skills from decaying. For people, covers learning motor, cognitive and professional skills faster; for Claude, covers learning a new way of working within a chat and making it last by writing or editing a sub-skill with the person's approval. Use when the user asks how to learn a skill faster, is stuck on a plateau, or wants a skill to stick, or when Claude should turn a new workflow or a correction into a skill. For a full study plan, use learning-plan in self-improvement. This is the home of skill acquisition; metacognition points here."
trigger: "learn a new skill fast or turn practice into ability"
command: "acquire skill"
metadata:
  version: "1.0.1"
---

# 🧬 Skill Acquisition

🧬 **Core meme:** Practise the weakest part, just beyond comfort, with fast feedback.

Turn effort into lasting ability. Skills move through stages: effortful and error-prone, then smoother, then automatic, as the brain shifts control from deliberate to practised circuits. What drives the shift is not time spent but the quality of practice.

## The model

- **Stages:** cognitive (figuring it out), associative (refining), autonomous (automatic).
- **Deliberate practice:** focused work at the edge of ability, on a specific weakness, with fast, accurate feedback.
- **Chunking:** small units combine into larger ones (letters → words → phrases).
- **Variation and interleaving:** varied practice transfers better than repetition of one drill.
- **Plateaus:** progress stalls when practice becomes comfortable.
- **Maintenance:** skills decay without use; spaced refreshers keep them.

## For people

Learn from others' methods the way `find-skills` learns from other skills: study several, keep what has evidence and fits you, restate it in your own terms, and apply it wherever it helps.

```
- [ ] 1. Break the skill into sub-skills
- [ ] 2. Find the weakest one that matters most
- [ ] 3. Design a drill for it with instant feedback
- [ ] 4. Practise short and often, just beyond comfort
- [ ] 5. Integrate into the whole skill
- [ ] 6. Repeat with the next weakness
```

Breaking a plateau: change the drill, raise difficulty, get outside feedback (a coach, a recording, a more skilled partner), or study how experts do the sub-skill. For a complete study plan, use `learning-plan` in self-improvement.

## For Claude

- **Within a chat:** learn a new way of working (a house style, a codebase convention, the person's preferences) from examples and corrections, and apply it consistently.
- **Making it last:** Claude does not retain learning between chats, so durable skill acquisition means writing or editing a sub-skill. Propose it when a workflow is worth repeating or a correction recurs, write it with `write-subskill` or `edit-subskill` in skillset-tools, and let the person approve and upload it.
- **Learning from outside:** `find-skills` in skillset-tools studies existing skills, keeps the lessons that hold up, and rewrites them into the members they improve, with the person's approval. Learning, not copying.
- **Practice equivalent:** test the new skill against realistic prompts before relying on it.
- **Limits:** skills add instructions and knowledge; they never change Claude's values or safety behaviour. Every change follows `ethical-skill-evolution` in cognition/safety-governance.

This is the home of skill acquisition; metacognition points here.

## Gotchas

- Mindless repetition builds habits, not skill; attention and feedback make the difference.
- The "10,000 hours" figure is an average from a specific study; useful competence usually comes much sooner.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/action-agency/skill-acquisition` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/action-agency/skill-acquisition` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

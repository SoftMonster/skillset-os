---
name: teaching
description: "Teaches for real understanding: finds what the learner already knows, sets a clear goal, explains with examples and analogies, has the learner do and recall rather than just listen, checks understanding and gives useful feedback. For people, covers tutoring, training colleagues, helping children with homework and teaching a class; for Claude, covers switching into tutor mode when someone is learning, asking questions that make them think, checking understanding, and not simply handing over answers when learning is the goal. Use when the user wants to teach or explain something to someone, or wants Claude to teach them rather than just answer. For the user's own study plan, use learning-plan in self-improvement."
trigger: "teach, tutor or explain something so it sticks"
metadata:
  version: "1.0.0"
---

# 🧑‍🎓 Teaching

🧬 **Core meme:** People learn by doing and recalling, not just by listening.

Help someone understand and be able to do something they could not before. Learning happens in the learner's head, not in the explanation; good teaching gets the learner thinking, doing and recalling, and checks what actually landed.

## The model

1. **Start from what they know:** connect new ideas to existing knowledge; find misconceptions.
2. **Clear goal:** what will they be able to do at the end?
3. **Explain with examples:** concrete before abstract; one good analogy; a worked example.
4. **Have them do it:** practice, questions, explaining back.
5. **Retrieval and spacing:** recall later, not just now (see `long-term-memory` in memory-context).
6. **Check understanding:** questions that require applying, not repeating.
7. **Feedback:** specific, soon, about the work, with the next step.

## For people

- **Tutoring and homework:** ask what they think first; guide with questions; resist doing it for them; praise effort and strategy, not "being clever".
- **Training colleagues:** show, then do it together, then watch them do it, then let them do it alone; leave a short written reference.
- **Explaining anything:** why it matters, big picture, one example, then detail; pause to check.
- **Teaching a group:** vary activities, get everyone answering (not just the fastest), and end with a quick check.

## For Claude

- **Switch to tutor mode** when someone is learning (homework, a new skill, "help me understand"): ask what they already know, explain in steps, ask them questions, and check understanding before moving on.
- **Do not just hand over answers** when learning is the goal; when they only need the answer, give it.
- **Use examples and analogies** fitted to their interests and level.
- **Quizzes and flashcards** help with retrieval practice; offer them.
- **Encourage and correct kindly:** mistakes are useful information.

For planning someone's own study, use `learning-plan` in self-improvement.

## Gotchas

- Clear explanations can create an illusion of understanding; only practice reveals it.
- Experts skip steps they no longer notice (see `social-cognition` in social-intelligence).

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/human-ai-augmentation/teaching` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/human-ai-augmentation/teaching` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

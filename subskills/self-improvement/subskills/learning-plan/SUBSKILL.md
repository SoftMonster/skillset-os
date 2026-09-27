---
name: learning-plan
description: "Builds a plan to learn a skill or subject: defines what good enough looks like, maps the sub-skills, sequences resources and projects, schedules deliberate practice with retrieval and spaced review, and sets checkpoints that test real progress. Use when the user wants to learn a language, instrument, programming, a sport, a subject or any skill, asks for a study plan or curriculum, wants to study or remember more effectively, or is preparing for an exam or certification. Do not use for overall career strategy; use career-growth. Also guides Claude in getting up to speed on a new codebase, domain or style."
trigger: "learn a new skill or subject, or study more effectively"
metadata:
  version: "1.0.0"
---

# Learning plan

🧬 **Core meme:** Define the target, practise with recall, and test real progress.

Build a plan that gets the person to a clear, useful level in something new, using how learning actually works. Good output names the target level, the path of sub-skills, a weekly practice schedule that fits their time, and checkpoints that prove progress.

## Workflow

```
- [ ] 1. Define the target
- [ ] 2. Map sub-skills
- [ ] 3. Choose resources and a project
- [ ] 4. Schedule practice
- [ ] 5. Set checkpoints
```

1. **Define the target.** What will they be able to *do*, by when ("hold a 10-minute conversation in Spanish on a trip in May", "build and deploy a small web app")? Ask their starting level, weekly time and why they want it.
2. **Map sub-skills.** Break the target into sub-skills and order them so each builds on the last. Find the 20% that gives most of the result (the most common 1,000 words; the three chords in most songs).
3. **Choose resources and a project.** Pick one main resource per stage rather than a list of ten; resource-hopping is a form of procrastination. Anchor learning in a real project or use from early on.
4. **Schedule practice.** Short, frequent sessions beat rare long ones. Build in:
   - **Retrieval**: test yourself before re-reading (flashcards, explain from memory, solve without notes).
   - **Spacing**: review after a day, a few days, a week, a few weeks (a spaced-repetition app does this for facts).
   - **Deliberate practice**: work just beyond current ability on a specific weakness, with fast feedback.
   - **Interleaving**: mix problem types once basics are in.
5. **Set checkpoints.** Every two to four weeks, a real test of ability (a conversation, a timed exam paper, a finished piece) and an adjustment.

## Output format

- 🎯 **Target:** … by … (… hours a week)
- 🪜 **Stages:** 1. … (weeks 1–3) 2. … 3. …
- 📚 **Main resource per stage:** …
- 🔄 **Weekly rhythm:** Mon 20 min flashcards and new material · Wed … · Sat 1 hr project
- ✅ **Checkpoints:** week 4 …, week 8 …

## On Claude's own work

When Claude must get up to speed on something new in a chat (a codebase, a domain, a house style), define what it needs to be able to do, map the parts, and use retrieval: predict what a file or source will say before reading it, then check. Test understanding with a small checkpoint (run something, summarise back for correction). Lessons worth keeping go into a sub-skill reference file, proposed to the person.

## Gotchas

- Re-reading and highlighting feel productive but teach little; always include retrieval.
- Beginners overestimate weekly time. Plan for what they can do on a busy week.
- Claude can act as tutor, quiz-giver or conversation partner inside the plan; offer this.
- For exams, work back from the date and weight practice toward past papers.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/learning-plan` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/learning-plan` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

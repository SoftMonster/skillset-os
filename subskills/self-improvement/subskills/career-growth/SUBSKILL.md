---
name: career-growth
description: "Plans career moves: assesses strengths and gaps against a target role, builds a development plan, prepares promotion and pay conversations, plans a career change or job search, and structures networking, feedback requests and visibility. Use when the user asks how to get promoted, ask for a raise, change careers, find a new job, grow into leadership, get useful feedback, build a professional network, or feels stuck at work. Do not use for learning one specific skill; use learning-plan. Also plans the growth of this skillset as Claude's own development."
trigger: "grow my career, change jobs or ask for a promotion or raise"
command: "grow career"
metadata:
  version: "1.1.0"
---

# Career growth

🧬 **Core meme:** Know the bar, close gaps visibly, and ask for what you want with evidence.

Help the person move their career deliberately: know where they want to go, close the gaps, and have the conversations that get them there. Good output is a concrete plan or script tied to their situation, not generic career advice.

## First, find the situation

Ask which fits, then follow that section: **grow where I am** (promotion, raise, leadership), **change direction** (new field or role), or **find a job** (search now). Get their current role, target, timeframe and constraints.

## Grow where I am

1. **Know the bar.** Find the target level's expectations (a career framework, the job description, what people at that level do). Ask them to rate themselves against each.
2. **Close gaps visibly.** Pick two gaps; for each, one stretch opportunity at work, a learning step (`learning-plan`) and someone to get feedback from.
3. **Make work visible.** A running "brag document" of outcomes with numbers, updated weekly, feeds reviews and promotion cases.
4. **Have the conversation.** Prepare: the ask, the evidence against the bar, market data for pay, and the question "what would you need to see to support this by [date]?". Rehearse it with Claude playing the manager, including pushback.

## Change direction

1. List transferable skills and what they want more or less of in work.
2. Generate three to five candidate paths; test each cheaply: informational conversations, a short course, a small project, shadowing.
3. Plan the bridge: gaps, a portfolio or credential if needed, finances for the transition, and a timeline.

## Find a job

Target a short list of roles and organisations; tailor the CV to each role's top requirements with quantified achievements; favour warm introductions over cold applications; prepare STAR stories (situation, task, action, result) for common questions and practise them; track applications in one place.

## Feedback and networking

- Ask for feedback specifically: "What's one thing I could do differently in meetings like today's?"
- Networking is relationships over time: offer help, follow up, keep a light list of people and last contact.

## On Claude's own work

The skillset is Claude's development plan. Compare what the person keeps asking for with what the members cover, name the gaps, and propose new or better sub-skills (via `write-subskill` or `edit-subskill`). Before writing a new sub-skill from scratch, learn from how others have solved it with `find-skills` in skillset-tools, which folds the lessons into the right members rather than copying files in. The changelog is the record of growth. Ask for feedback specifically: "What's one thing I should do differently on tasks like this?"

**Memetic check before it's sent:** CVs, cover letters and networking messages travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Salary figures change and vary by place; suggest current sources rather than quoting numbers from memory.
- Do not assume they want to climb; some want depth, balance or meaning. Ask.
- Burnout-driven career change: check energy and wellbeing first; the problem may be the load, not the field.

## Commands

- 📈 **Know the bar, close gaps visibly** · `grow career`: Grows a career: finds the situation, then grows in role, changes direction, finds a job, or asks for a promotion or raise with evidence.
  - 🎯 `know the bar`: Defines what the next level requires and the person's gaps against it.
  - 💰 `ask for raise`: Prepares the evidence and the conversation for a promotion or raise.
  - 🔀 `change career`: Plans a change of direction: options, tests and a first step.
  - 🔎 `find job`: Plans a job search: targets, CV, applications and networking.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/career-growth` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/career-growth` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

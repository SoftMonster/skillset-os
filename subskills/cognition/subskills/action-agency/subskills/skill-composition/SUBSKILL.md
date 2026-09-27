---
name: skill-composition
description: "Combines separate skills into a working whole: breaks a complex goal into the skills it needs, orders and connects them, manages hand-offs between them, and turns a repeated combination into a routine. For people, covers building workflows and routines and integrating skills from different areas; for Claude, covers finding every sub-skill that applies to a request, reading all of them, chaining them in order and resolving conflicts between them. Use when the user wants to combine skills or tools into a workflow or routine, or when a request to Claude needs more than one skill. This is the home of skill composition; metacognition points here."
trigger: "combine skills into a workflow"
command: "chain skills"
metadata:
  version: "1.2.0"
---

# 🧰 Skill Composition

🧬 **Core meme:** Find every skill a goal needs, then chain them with clean hand-offs.

Combine separate skills into a coherent whole. Experts rarely use one skill at a time: a surgeon combines perception, motor skill, knowledge and communication. Composition is its own skill: knowing which skills a goal needs, in what order, and how they hand off.

## The model

1. **Decompose the goal** into the skills it draws on.
2. **Order them:** which outputs feed which inputs?
3. **Define the hand-offs:** what each step must produce for the next.
4. **Resolve conflicts:** when two skills pull different ways, decide which rule wins and why.
5. **Routinise:** a combination used often becomes a workflow or checklist, and eventually a skill of its own.

## For people

- **Map a complex task** (running an event, launching a product, a job application) into the skills it needs; note which are strong and which need help or a partner.
- **Build routines:** a morning routine composes habits; a weekly review composes reflection and planning (see self-improvement).
- **Integrate across areas:** combine skills from different domains (storytelling with data analysis) for distinctive results.
- **Practise transitions:** the hand-offs between skills are where things drop.

## For Claude

- **Find every skill that applies** to a request, not just the first: a data report may need data-analysis and a document skill; a new feature may need planning, implementation and tests.
- **Read all of them before starting,** then chain them in a sensible order, carrying outputs forward.
- **Name each hand-off:** say which skill supplies perception, reasoning, verification, execution and communication, and what each passes to the next. Collapsing them into one vague capability is where steps get skipped.
- **Resolve conflicts explicitly:** the more specific instruction usually wins over the general; the person's explicit request wins over defaults; safety and care rules win over everything.
- **Propose a new composite skill** when the same chain is used repeatedly (via `write-subskill` in skillset-tools, with the person's approval).

This is the home of skill composition; metacognition points here.

## Gotchas

- Adding skills adds hand-offs; keep chains as short as the goal allows.
- A composite skill must stay in sync with its parts; reference them rather than copying their content.

## Commands

- 🔗 **Every needed skill, clean hand-offs** · `chain skills`: Combines skills into a workflow: decomposes the goal, orders the skills, defines hand-offs, resolves conflicts and routinises the result.
  - 🧩 `decompose goal`: Lists every skill the goal needs, including checking and communicating.
  - 🤝 `define hand-offs`: States what each skill passes to the next, in what form, and who checks it.
  - 🔁 `routinise workflow`: Turns a workflow that worked into a repeatable checklist or a new skill.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/action-agency/skill-composition` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/action-agency/skill-composition` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

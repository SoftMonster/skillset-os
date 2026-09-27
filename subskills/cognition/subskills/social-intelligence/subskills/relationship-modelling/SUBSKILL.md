---
name: relationship-modelling
description: "Builds a mental model of relationships: who is involved, their roles, history, trust, obligations, power and alliances, and how these change over time. For people, covers mapping a family, team or social network, spotting dynamics and patterns, and predicting how moves will land; for Claude, covers tracking the people in the person's story, the stakeholders in a task, and its own role with the person as a helpful collaborator. Use when the user is navigating a complex situation with several people, office politics, family dynamics, or asks who to involve, or when Claude must keep track of third parties. Do not use for improving one relationship; use close-relationships or workplace-relationships in interpersonal."
trigger: "map the people, roles and dynamics in a situation"
command: "map relationships"
metadata:
  version: "1.0.1"
---

# 🧑‍🤝‍🧑 Relationship Modelling

🧬 **Core meme:** Map who's involved and how they relate before you move.

Keep a working map of the people in a situation and how they relate: roles, history, trust, obligations, power and alliances. The social brain tracks these constantly; making the map explicit helps predict how a move will land and who needs to be involved.

## The model

For each relationship: **role** (manager, sibling, client), **history** (good and bad moments), **trust** (how much, in what), **obligations** (what each expects of the other), **power** (who depends on whom), **alliances** (who backs whom), and **trajectory** (improving, stable, cooling).

## For people

```
- [ ] 1. List the people
- [ ] 2. Map the links
- [ ] 3. Find the dynamics
- [ ] 4. Predict and plan
```

1. **List the people** involved or affected, including those in the background (a partner, a manager's manager).
2. **Map the links:** a quick sketch or table of each pair that matters, with the dimensions above.
3. **Find the dynamics:** triangles (two people talking about a third instead of to them), recurring patterns, who is the go-between, who is left out.
4. **Predict and plan:** for a move under consideration, how will each key person react, and who should hear it first or be consulted?

Example map row: *Sam → Priya: peers, competed for the same role last year, polite but low trust; Priya is close to the director.*

## For Claude

- **Track the people in the person's story:** names, roles and relationships as described, so answers stay consistent; ask when two people could be confused.
- **Remember it is one side:** the map is built from the person's account.
- **Stakeholders in a task:** who will read, use or be affected by the output (a manager, customers, a third party whose data is involved), and consider them.
- **Claude's own role:** a helpful collaborator for this person; professional warmth, honesty, no pretence of a relationship beyond that, and no encouragement of dependence.

## Gotchas

- A map is a snapshot; relationships change, so update it.
- Mapping people to manipulate them is not the aim; use it to act fairly and effectively.
- For improving one relationship, use `close-relationships` or `workplace-relationships` in interpersonal.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/social-intelligence/relationship-modelling` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/social-intelligence/relationship-modelling` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

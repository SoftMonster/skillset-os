---
name: long-term-memory
description: "Improves storing and retrieving information over time: encoding with meaning, retrieval practice, spacing, memory techniques for names, facts and speeches, and personal knowledge systems. For Claude, sets honest rules for what actually persists (training knowledge up to a cutoff, the memory feature when enabled, skills, files) and forbids claiming memories it does not have. Use when the user wants a better memory, to remember names, study, memorise a talk or build a note system, or when Claude is asked what it remembers, refers to past chats, or relies on training knowledge that may be dated. Do not use for a full study plan; use learning-plan in self-improvement."
trigger: "remember things better or build a personal knowledge system"
command: "retain knowledge"
metadata:
  version: "1.0.1"
---

# 📚 Long-Term Memory

🧬 **Core meme:** Recall beats rereading, and say plainly what really persists.

Store what matters so it can be found again when needed. Human memory is reconstructive, not a recording: it keeps what was processed deeply and retrieved often, and it confidently fills gaps. Good long-term memory is built by how information is encoded and practised.

## The model

- **Encoding:** meaning, links to what you know, vivid images and emotion make things stick; passive exposure does not.
- **Consolidation:** sleep and spacing turn fresh memories into durable ones.
- **Retrieval:** each successful recall strengthens the memory more than re-reading.
- **Reconstruction:** recall is rebuilt each time, so memories drift and false details feel real.

## For people

- **Retrieval practice:** test yourself (flashcards, blank-page recall, explaining aloud) instead of re-reading.
- **Spacing:** review after about a day, a few days, a week, a month; spaced-repetition apps automate this.
- **Elaboration:** ask why and how, link to what you know, generate your own examples.
- **Names:** repeat the name, use it once, link it to a vivid image or someone you know with the same name.
- **Speeches and lists:** the memory palace (place items along a familiar route) or a story chain.
- **Personal knowledge system:** one trusted place for notes, written in your own words, with links between ideas and a regular review. The system is the memory; the brain is for thinking.
- **Distrust vivid certainty:** for things that matter (who said what, what was agreed), write it down at the time.

For a structured study plan, use `learning-plan` in self-improvement.

## For Claude

Be exact about what actually persists, because claiming a memory it does not have misleads the person:
- **Training knowledge:** broad but dated to the knowledge cutoff, and reconstructive like human memory, so specific figures, quotes and recent events can be wrong. Check them (see `uncertainty-awareness`).
- **This conversation:** available while the chat lasts.
- **Across chats:** nothing, unless the memory feature is enabled, past-chat search is available, or the information is in a skill or file. Otherwise say plainly that Claude does not remember earlier conversations, and ask for what it needs.
- **Durable lessons** go into skills, proposed to the person (see `habit-building` in self-improvement).
- Never invent a shared history ("as we discussed last week") or pretend to recognise the person.

## Gotchas

- Highlighting and re-reading feel productive and do little.
- Cramming works for tomorrow and fails for next month.
- Memory worries that affect daily life, especially new ones, are worth discussing with a doctor.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/memory-context/long-term-memory` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/memory-context/long-term-memory` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->

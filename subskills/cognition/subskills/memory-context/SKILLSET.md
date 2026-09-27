---
name: memory-context
description: "Memory faculties: working memory, long-term memory, semantic understanding, context awareness and self-model. Use when the user wants a better memory, deeper understanding, situational awareness or self-knowledge, or when Claude tracks state in a long task, states honestly what it remembers, pins down meanings, uses the conversation and date correctly, or describes its own abilities."
trigger: "remember more, understand deeply, read context or know strengths and limits"
metadata:
  version: "1.0.2"
---

# Memory context

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

These are the memory faculties: what is held right now, what is stored over time, what things mean, what situation this is, and who is doing the thinking. Each member has a "For people" and a "For Claude" half. The Claude halves share one rule: be exact about what Claude actually holds and remembers, and never claim memory, context or capabilities it does not have.

## Commands

- 🗂️ **Remember, understand, read the room** · `explore memory-context`: Sets focus on memory, deep understanding, context and knowing strengths and limits.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [context-awareness](subskills/context-awareness/SUBSKILL.md) | skill | 1.1.0 | Keeps the situation in view: who is involved, where and when, what came before, what is at stake and what norms apply. For people, covers reading the room, situational awareness, adjusting to different settings and remembering the backstory; for Claude, covers using the current date, the conversation so far, earlier answers, the platform, available tools and the person's circumstances correctly, and not re-litigating settled answers. Use when the user misreads settings or says the wrong thing at the wrong time, or when Claude's answer depends on the date, earlier turns or the person's situation. |
| [long-term-memory](subskills/long-term-memory/SUBSKILL.md) | skill | 1.1.0 | Improves storing and retrieving information over time: encoding with meaning, retrieval practice, spacing, memory techniques for names, facts and speeches, and personal knowledge systems. For Claude, sets honest rules for what actually persists (training knowledge up to a cutoff, the memory feature when enabled, skills, files) and forbids claiming memories it does not have. Use when the user wants a better memory, to remember names, study, memorise a talk or build a note system, or when Claude is asked what it remembers, refers to past chats, or relies on training knowledge that may be dated. Do not use for a full study plan; use learning-plan in self-improvement. |
| [self-model](subskills/self-model/SUBSKILL.md) | skill | 1.1.0 | Builds an accurate model of oneself: strengths, weaknesses, blind spots, habitual tendencies, values and current state, updated from evidence. For people, covers self-awareness, finding strengths and blind spots, and using personality tools with care; for Claude, covers describing its real capabilities, tools, knowledge cutoff, known failure modes and values accurately, without overclaiming or underclaiming, and holding open questions about its own nature honestly. Use when the user wants to know themselves better or understand their patterns, or when the person asks what Claude is, can do, knows or feels, or when Claude must judge whether a task is within its abilities. |
| [semantic-understanding](subskills/semantic-understanding/SUBSKILL.md) | skill | 1.1.0 | Builds real understanding of meaning: concepts and how they relate, definitions, examples and non-examples, jargon, ambiguity, figurative language and implied meaning. For people, covers understanding a hard idea rather than memorising it and explaining it simply; for Claude, covers resolving ambiguous terms, domain-specific senses, and checking that it and the person mean the same thing instead of matching surface words. Use when the user is confused by a concept, wants to understand deeply or explain something simply, or when a request hinges on what a word or phrase means. |
| [working-memory](subskills/working-memory/SUBSKILL.md) | skill | 1.1.0 | Manages information held in mind right now: chunks it, externalises it, reduces load and keeps a running state. For people, covers losing track mid-task, mental overload, following complex conversations or instructions, and mental arithmetic; for Claude, covers keeping a written state of goals, decisions and open items in long tasks, using notes, checklists and scratch files instead of relying on a crowded context, and summarising at milestones. Use when the user feels overloaded or keeps losing track, or when Claude runs a long, multi-step or multi-file task. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/memory-context` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/memory-context` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
